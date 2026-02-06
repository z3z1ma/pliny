from __future__ import annotations

import importlib
import os
import platform
from pathlib import Path
from typing import Any

from flask import Flask, Request, jsonify, render_template, request

from agent_loom.dashboard.auth import authorize_request
from agent_loom.dashboard.compound_fs import list_skills, read_instincts, read_skill
from agent_loom.dashboard.config import ServerConfig
from agent_loom.dashboard.http import err, ok
from agent_loom.dashboard.introspect import introspect_module
from agent_loom.dashboard.workspace_read import (
    WorkspaceReadError,
    detect_workspace_mode,
    poly_worktrees,
    repo_worktrees,
    services_index,
    worktree_diff,
    workspace_meta,
)

SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(SERVER_DIR, "templates")


def _is_loopback(host: str) -> bool:
    h = (host or "").strip().lower()
    return h in {"127.0.0.1", "localhost"}


def _require_token_default(host: str, require_token: bool) -> bool:
    if require_token:
        return True
    # If bound to non-loopback, require a token by default.
    return not _is_loopback(host)


def _subsystem_versions() -> dict[str, str]:
    # Keep this cheap and deterministic; no file system probing.
    versions: dict[str, str] = {}
    for name in ["ticket", "team", "memory", "workspace", "compound"]:
        try:
            mod = importlib.import_module(f"agent_loom.{name}.constants")
            versions[name] = str(getattr(mod, "SUBSYSTEM_VERSION", ""))
        except Exception:
            versions[name] = ""
    return versions


def _ensure_writes_enabled(cfg: ServerConfig) -> tuple[bool, dict[str, Any] | None]:
    if cfg.enable_writes:
        return True, None
    return False, err(code="WRITES_DISABLED", message="Writes are disabled")


def _require_auth(
    cfg: ServerConfig, req: Request
) -> tuple[bool, dict[str, Any] | None]:
    need = _require_token_default(str(req.host.split(":")[0]), cfg.require_token)
    res = authorize_request(req=req, token=cfg.token, require_token=need)
    if res.ok:
        return True, None
    return False, err(code="UNAUTHORIZED", message=res.reason)


def create_app(*, cfg: ServerConfig) -> Flask:
    app = Flask(__name__, template_folder=TEMPLATE_DIR)
    app.config["LOOM_SERVER_CFG"] = cfg

    @app.route("/")
    def dashboard() -> Any:
        return render_template("dashboard.html")

    @app.get("/api/v1/health")
    def health() -> Any:
        return jsonify(
            ok(
                data={
                    "platform": platform.platform(),
                    "python": platform.python_version(),
                    "repo_root": str(cfg.repo_root.resolve()),
                    "workspace_mode": cfg.workspace_mode,
                    "workspace_root": str(cfg.workspace_root.resolve())
                    if cfg.workspace_root is not None
                    else "",
                    "writes_enabled": bool(cfg.enable_writes),
                    "token_required": bool(
                        _require_token_default("127.0.0.1", cfg.require_token)
                    ),
                },
                meta={
                    "subsystem_versions": _subsystem_versions(),
                },
            )
        )

    @app.get("/api/v1/capabilities")
    def capabilities() -> Any:
        return jsonify(
            ok(
                data={
                    "writes": {"enabled": bool(cfg.enable_writes)},
                    "auth": {
                        "supported": ["bearer", "x-loom-token"],
                        "require_token": bool(cfg.require_token),
                    },
                    "endpoints": [
                        {"method": "GET", "path": "/api/v1/health"},
                        {"method": "GET", "path": "/api/v1/capabilities"},
                        {"method": "GET", "path": "/api/v1/introspect/<subsystem>"},
                        {"method": "GET", "path": "/api/v1/tickets"},
                        {"method": "GET", "path": "/api/v1/tickets/<id>"},
                        {"method": "GET", "path": "/api/v1/tickets/<id>/view"},
                        {"method": "GET", "path": "/api/v1/tickets/<id>/dep"},
                        {"method": "GET", "path": "/api/v1/tickets/swarm"},
                        {"method": "POST", "path": "/api/v1/tickets"},
                        {"method": "PATCH", "path": "/api/v1/tickets/<id>"},
                        {"method": "GET", "path": "/api/v1/teams"},
                        {"method": "GET", "path": "/api/v1/teams/<team>/status"},
                        {"method": "GET", "path": "/api/v1/teams/<team>/run"},
                        {"method": "GET", "path": "/api/v1/teams/<team>/events"},
                        {"method": "GET", "path": "/api/v1/teams/<team>/inbox"},
                        {"method": "GET", "path": "/api/v1/teams/<team>/captures"},
                        {"method": "GET", "path": "/api/v1/teams/<team>/captures/text"},
                        {"method": "GET", "path": "/api/v1/memory/recall"},
                        {"method": "GET", "path": "/api/v1/memory/notes/<id>"},
                        {"method": "GET", "path": "/api/v1/workspace/meta"},
                        {"method": "GET", "path": "/api/v1/workspace/worktrees"},
                        {"method": "GET", "path": "/api/v1/workspace/worktree/diff"},
                        {"method": "GET", "path": "/api/v1/workspace/services/index"},
                        {"method": "GET", "path": "/api/v1/compound/skills"},
                        {"method": "GET", "path": "/api/v1/compound/skills/<name>"},
                        {"method": "GET", "path": "/api/v1/compound/instincts"},
                    ],
                },
                meta={"subsystem_versions": _subsystem_versions()},
            )
        )

    @app.get("/api/v1/introspect/<subsystem>")
    def introspect(subsystem: str) -> Any:
        name = str(subsystem or "").strip().lower()
        mod_name = {
            "ticket": "agent_loom.ticket.core",
            "team": "agent_loom.team.core",
            "memory": "agent_loom.memory.core",
            "workspace": "agent_loom.workspace.core",
            "compound": "agent_loom.compound.sync",
        }.get(name)
        if not mod_name:
            return jsonify(err(code="ARG", message="Unknown subsystem")), 400
        mod = importlib.import_module(mod_name)
        payload = introspect_module(mod)
        return jsonify(ok(data=payload))

    # -----------------
    # Tickets
    # -----------------

    def _tickets_dir() -> Path:
        # Server is repo-root anchored; allow override for testing.
        return (cfg.repo_root / ".tickets").resolve()

    @app.get("/api/v1/tickets")
    def tickets_list() -> Any:
        from agent_loom.ticket.api import list_tickets

        q = request.args
        res = list_tickets(
            tickets_dir=_tickets_dir(),
            status=str(q.get("status", "")),
            type_=str(q.get("type", "")),
            assignee=str(q.get("assignee", "")),
            tag=str(q.get("tag", "")),
            prio_min=int(q["prio_min"]) if q.get("prio_min") else None,
            prio_max=int(q["prio_max"]) if q.get("prio_max") else None,
            include_closed=(str(q.get("include_closed", "1")) != "0"),
            limit=int(q["limit"]) if q.get("limit") else 0,
        )
        return jsonify(ok(data=res))

    @app.get("/api/v1/tickets/<ticket_id>")
    def tickets_show(ticket_id: str) -> Any:
        from agent_loom.ticket.api import show

        res = show(ticket_id=str(ticket_id), tickets_dir=_tickets_dir())
        return jsonify(ok(data=res))

    @app.get("/api/v1/tickets/<ticket_id>/view")
    def tickets_view(ticket_id: str) -> Any:
        from agent_loom.ticket.api import view

        res = view(ticket_id=str(ticket_id), tickets_dir=_tickets_dir())
        return jsonify(ok(data=res))

    @app.get("/api/v1/tickets/<ticket_id>/dep")
    def tickets_dep(ticket_id: str) -> Any:
        from agent_loom.ticket.api import dep

        res = dep(ticket_id=str(ticket_id), tickets_dir=_tickets_dir())
        return jsonify(ok(data=res))

    @app.get("/api/v1/tickets/swarm")
    def tickets_swarm() -> Any:
        from agent_loom.ticket.api import swarm

        q = request.args
        res = swarm(
            tickets_dir=_tickets_dir(),
            active_within=str(q.get("active_within") or "2h"),
        )
        return jsonify(ok(data=res))

    @app.post("/api/v1/tickets")
    def tickets_create() -> Any:
        allowed, payload = _ensure_writes_enabled(cfg)
        if not allowed:
            return jsonify(payload), 403
        allowed, payload = _require_auth(cfg, request)
        if not allowed:
            return jsonify(payload), 401

        from agent_loom.ticket.api import create

        body = request.get_json(silent=True) or {}
        try:
            res = create(
                tickets_dir=_tickets_dir(),
                title=str(body.get("title") or "").strip(),
                type=str(body.get("type") or "task").strip(),
                priority=int(body.get("priority") or 2),
                tags=str(body.get("tags") or ""),
                description=str(body.get("description") or ""),
                assignee=str(body.get("assignee") or "").strip(),
                external_ref=str(body.get("external_ref") or "").strip(),
                parent=str(body.get("parent") or "").strip(),
                design=str(body.get("design") or "").strip(),
                acceptance=str(body.get("acceptance") or "").strip(),
            )
        except Exception as e:
            return jsonify(err(code="CREATE_FAILED", message=str(e))), 400
        return jsonify(ok(data=res)), 201

    @app.patch("/api/v1/tickets/<ticket_id>")
    def tickets_update(ticket_id: str) -> Any:
        allowed, payload = _ensure_writes_enabled(cfg)
        if not allowed:
            return jsonify(payload), 403
        allowed, payload = _require_auth(cfg, request)
        if not allowed:
            return jsonify(payload), 401

        from agent_loom.ticket.api import update

        body = request.get_json(silent=True) or {}
        try:
            res = update(
                tickets_dir=_tickets_dir(),
                ticket_id=str(ticket_id),
                title=body.get("title"),
                status=str(body.get("status") or "").strip(),
                priority=(int(body["priority"]) if "priority" in body else None),
                type_=str(body.get("type") or "").strip(),
                assignee=str(body.get("assignee") or "").strip(),
                tags=(str(body.get("tags")) if "tags" in body else None),
                external_ref=(
                    str(body.get("external_ref") or "")
                    if "external_ref" in body
                    else None
                ),
                parent=(str(body.get("parent") or "") if "parent" in body else None),
                deps=(
                    (
                        ",".join([str(x) for x in (body.get("deps") or [])])
                        if isinstance(body.get("deps"), list)
                        else str(body.get("deps") or "")
                    )
                    if "deps" in body
                    else None
                ),
                links=(
                    (
                        ",".join([str(x) for x in (body.get("links") or [])])
                        if isinstance(body.get("links"), list)
                        else str(body.get("links") or "")
                    )
                    if "links" in body
                    else None
                ),
                body_text=(str(body.get("body")) if "body" in body else None),
                force=bool(body.get("force")),
            )
        except Exception as e:
            return jsonify(err(code="UPDATE_FAILED", message=str(e))), 400
        return jsonify(ok(data=res))

    # -----------------
    # Teams
    # -----------------

    @app.get("/api/v1/teams")
    def teams_list() -> Any:
        from agent_loom.team.constants import DEFAULT_RUNS_DIR

        runs_dir = cfg.repo_root / DEFAULT_RUNS_DIR
        teams: list[dict[str, Any]] = []
        if runs_dir.exists():
            for d in sorted(
                [p for p in runs_dir.iterdir() if p.is_dir()], key=lambda p: p.name
            ):
                run_json = d / "run.json"
                if not run_json.exists():
                    continue
                import json

                try:
                    run = json.loads(
                        run_json.read_text(encoding="utf-8", errors="replace")
                    )
                except Exception:
                    run = {}
                teams.append(
                    {
                        "team": d.name,
                        "created_at": run.get("created_at"),
                        "updated_at": run.get("updated_at"),
                        "objective": run.get("objective"),
                        "session": run.get("session"),
                    }
                )
        teams.sort(
            key=lambda x: str(x.get("updated_at") or x.get("created_at") or ""),
            reverse=True,
        )
        return jsonify(ok(data={"teams": teams, "count": len(teams)}))

    @app.get("/api/v1/teams/<team>/status")
    def team_status(team: str) -> Any:
        from agent_loom.team.core import status as team_status_fn

        try:
            res = team_status_fn(team=str(team), repo=cfg.repo_root)
        except Exception as e:
            return jsonify(err(code="TEAM_STATUS_FAILED", message=str(e))), 400
        return jsonify(ok(data=res))

    @app.get("/api/v1/teams/<team>/run")
    def team_run(team: str) -> Any:
        from agent_loom.team.constants import DEFAULT_RUNS_DIR

        run_json = cfg.repo_root / DEFAULT_RUNS_DIR / str(team) / "run.json"
        if not run_json.exists():
            return jsonify(err(code="NOT_FOUND", message="team not found")), 404
        import json

        try:
            run = json.loads(run_json.read_text(encoding="utf-8", errors="replace"))
        except Exception as e:
            return jsonify(err(code="READ_FAILED", message=str(e))), 400
        return jsonify(ok(data=run))

    @app.get("/api/v1/teams/<team>/events")
    def team_events(team: str) -> Any:
        from agent_loom.team.constants import DEFAULT_RUNS_DIR

        q = request.args
        limit = int(q.get("limit") or 100)
        since = str(q.get("since") or "").strip()
        events_dir = cfg.repo_root / DEFAULT_RUNS_DIR / str(team) / "events"
        if not events_dir.exists():
            return jsonify(ok(data={"events": [], "count": 0}))

        files = sorted(
            [p for p in events_dir.glob("*.json")], key=lambda p: p.name, reverse=True
        )
        out: list[dict[str, Any]] = []
        import json

        for p in files:
            if since and p.name < since:
                continue
            try:
                data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                continue
            if isinstance(data, dict):
                data["_cursor"] = p.name
                out.append(data)
            if len(out) >= limit:
                break
        return jsonify(ok(data={"events": out, "count": len(out)}))

    @app.get("/api/v1/teams/<team>/inbox")
    def team_inbox(team: str) -> Any:
        from agent_loom.team.constants import DEFAULT_RUNS_DIR

        base = cfg.repo_root / DEFAULT_RUNS_DIR / str(team) / "inbox"
        read_dir = base / "read"

        def _scan(d: Path, *, limit: int) -> list[dict[str, Any]]:
            if not d.exists():
                return []
            files = sorted(
                [p for p in d.glob("*.json")], key=lambda p: p.name, reverse=True
            )
            items: list[dict[str, Any]] = []
            import json

            for p in files:
                try:
                    data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
                except Exception:
                    continue
                if isinstance(data, dict):
                    items.append(data)
                if len(items) >= limit:
                    break
            return items

        limit = int(request.args.get("limit") or 50)
        payload = {
            "unread": _scan(base, limit=limit),
            "read": _scan(read_dir, limit=limit),
        }
        return jsonify(ok(data=payload))

    @app.get("/api/v1/teams/<team>/captures")
    def team_captures(team: str) -> Any:
        from agent_loom.team.constants import DEFAULT_RUNS_DIR

        captures_dir = cfg.repo_root / DEFAULT_RUNS_DIR / str(team) / "captures"
        if not captures_dir.exists():
            return jsonify(ok(data={"captures": [], "count": 0}))
        files = sorted(
            [p for p in captures_dir.glob("*.json")], key=lambda p: p.name, reverse=True
        )
        limit = int(request.args.get("limit") or 50)
        out: list[dict[str, Any]] = []
        import json

        for p in files:
            try:
                data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                continue
            if isinstance(data, dict):
                data.setdefault("_meta", p.name)
                out.append(data)
            if len(out) >= limit:
                break
        return jsonify(ok(data={"captures": out, "count": len(out)}))

    @app.get("/api/v1/teams/<team>/captures/text")
    def team_capture_text(team: str) -> Any:
        """Return capture text for a capture meta filename.

        This keeps captures usable in the dashboard without exposing arbitrary file reads.
        """

        from agent_loom.team.constants import DEFAULT_RUNS_DIR

        meta = str(request.args.get("meta") or "").strip()
        if not meta:
            return jsonify(err(code="ARG", message="missing meta")), 400

        mp = Path(meta)
        if mp.name != meta or mp.suffix != ".json":
            return jsonify(err(code="ARG", message="invalid meta")), 400

        captures_dir = cfg.repo_root / DEFAULT_RUNS_DIR / str(team) / "captures"
        meta_file = captures_dir / meta
        if not meta_file.exists():
            return jsonify(err(code="NOT_FOUND", message="capture meta not found")), 404

        txt_file = meta_file.with_suffix(".txt")
        if not txt_file.exists():
            return jsonify(err(code="NOT_FOUND", message="capture text not found")), 404

        # Guardrail: prevent gigantic reads in the UI.
        cap_bytes = 200_000
        raw = b""
        truncated = False
        try:
            with open(txt_file, "rb") as f:
                raw = f.read(cap_bytes + 1)
        except Exception as e:
            return jsonify(err(code="READ_FAILED", message=str(e))), 400

        if len(raw) > cap_bytes:
            truncated = True
            raw = raw[:cap_bytes]

        meta_payload: dict[str, Any] = {}
        try:
            import json

            meta_payload0 = json.loads(
                meta_file.read_text(encoding="utf-8", errors="replace")
            )
            if isinstance(meta_payload0, dict):
                meta_payload = meta_payload0
        except Exception:
            meta_payload = {}

        text = raw.decode("utf-8", errors="replace")
        payload = {
            "meta": meta,
            "captured_at": str(meta_payload.get("captured_at") or ""),
            "target": dict(meta_payload.get("target") or {}),
            "pane": dict(meta_payload.get("pane") or {}),
            "text": text,
            "bytes": len(raw),
            "truncated": truncated,
        }
        return jsonify(ok(data=payload))

    # -----------------
    # Memory
    # -----------------

    @app.get("/api/v1/memory/recall")
    def memory_recall() -> Any:
        from agent_loom.memory.core import recall

        q = request.args
        vault_raw = str(q.get("vault") or "").strip() or ".memory"
        vault_path = Path(vault_raw).expanduser()
        if not vault_path.is_absolute():
            vault_path = (cfg.repo_root / vault_path).resolve()
        vault = str(vault_path)
        res = recall(
            vault=vault,
            query=str(q.get("q") or ""),
            limit=int(q.get("limit") or 8),
            tag=(q.getlist("tag") if hasattr(q, "getlist") else None),
            not_tag=(q.getlist("not_tag") if hasattr(q, "getlist") else None),
            scope=(q.getlist("scope") if hasattr(q, "getlist") else None),
            not_scope=(q.getlist("not_scope") if hasattr(q, "getlist") else None),
            visibility=(q.getlist("visibility") if hasattr(q, "getlist") else None),
            include_deprecated=(str(q.get("include_deprecated") or "0") == "1"),
            expand=int(q.get("expand") or 0),
            context=(str(q.get("context") or "0") == "1"),
            deterministic=(str(q.get("deterministic") or "0") == "1"),
            format=str(q.get("format") or "json"),
            quiet=True,
        )
        return jsonify(ok(data=res))

    @app.get("/api/v1/memory/notes/<note_id>")
    def memory_note(note_id: str) -> Any:
        from agent_loom.memory.vault import (
            find_note_path,
            resolve_vault_root,
            try_read_note_from_path,
            vault_paths,
        )

        vault_raw = str(request.args.get("vault") or "").strip() or ".memory"
        vault_path = Path(vault_raw).expanduser()
        if not vault_path.is_absolute():
            vault_path = (cfg.repo_root / vault_path).resolve()
        vp_root = resolve_vault_root(str(vault_path), cwd=cfg.repo_root)
        vp = vault_paths(vp_root)
        try:
            p = find_note_path(vp, str(note_id))
        except Exception as e:
            return jsonify(err(code="NOT_FOUND", message=str(e))), 404
        note, warns = try_read_note_from_path(
            p, default_visibility="shared", repo_root=cfg.repo_root
        )
        if note is None:
            return jsonify(err(code="READ_FAILED", message="failed to read note")), 400
        return jsonify(ok(data={"note": note, "warnings": warns}))

    # -----------------
    # Workspace
    # -----------------

    @app.get("/api/v1/workspace/meta")
    def ws_meta() -> Any:
        q = request.args
        try:
            mode, root = detect_workspace_mode(
                cwd=cfg.repo_root,
                mode=str(q.get("mode") or cfg.workspace_mode),
                root_arg=str(
                    q.get("root")
                    or (str(cfg.workspace_root) if cfg.workspace_root else "")
                ),
            )
            payload = workspace_meta(mode=mode, root=root)
        except Exception as e:
            return jsonify(err(code="WS_ERROR", message=str(e))), 400
        return jsonify(ok(data=payload))

    @app.get("/api/v1/workspace/worktrees")
    def ws_worktrees() -> Any:
        q = request.args
        try:
            mode, root = detect_workspace_mode(
                cwd=cfg.repo_root,
                mode=str(q.get("mode") or cfg.workspace_mode),
                root_arg=str(
                    q.get("root")
                    or (str(cfg.workspace_root) if cfg.workspace_root else "")
                ),
            )
            if mode == "repo":
                payload = repo_worktrees(
                    root=root,
                    q=str(q.get("q") or ""),
                    dirty_only=(str(q.get("dirty") or "0") == "1"),
                )
            else:
                payload = poly_worktrees(
                    root=root,
                    group=str(q.get("group") or ""),
                    repo=str(q.get("repo") or ""),
                    q=str(q.get("q") or ""),
                    dirty_only=(str(q.get("dirty") or "0") == "1"),
                    missing_only=(str(q.get("missing") or "0") == "1"),
                )
        except WorkspaceReadError as e:
            return jsonify(err(code="WS_ERROR", message=str(e))), 400
        except Exception as e:
            return jsonify(err(code="WS_ERROR", message=str(e))), 400
        return jsonify(ok(data=payload))

    @app.get("/api/v1/workspace/services/index")
    def ws_services_index() -> Any:
        q = request.args
        try:
            mode, root = detect_workspace_mode(
                cwd=cfg.repo_root,
                mode=str(q.get("mode") or cfg.workspace_mode),
                root_arg=str(
                    q.get("root")
                    or (str(cfg.workspace_root) if cfg.workspace_root else "")
                ),
            )
            if mode != "poly":
                return jsonify(ok(data={"index": None}))
            idx = services_index(root=root)
            return jsonify(ok(data={"index": idx}))
        except Exception as e:
            return jsonify(err(code="WS_ERROR", message=str(e))), 400

    @app.get("/api/v1/workspace/worktree/diff")
    def ws_worktree_diff() -> Any:
        q = request.args
        try:
            mode, root = detect_workspace_mode(
                cwd=cfg.repo_root,
                mode=str(q.get("mode") or cfg.workspace_mode),
                root_arg=str(
                    q.get("root")
                    or (str(cfg.workspace_root) if cfg.workspace_root else "")
                ),
            )
            payload = worktree_diff(
                mode=mode,
                root=root,
                path=str(q.get("path") or ""),
                diff_mode=str(q.get("diff_mode") or "cumulative"),
                base=str(q.get("base") or ""),
                max_patch_bytes=(
                    int(q.get("max_bytes") or 2_000_000)
                    if str(q.get("max_bytes") or "").strip()
                    else 2_000_000
                ),
            )
        except WorkspaceReadError as e:
            return jsonify(err(code="WS_ERROR", message=str(e))), 400
        except Exception as e:
            return jsonify(err(code="WS_ERROR", message=str(e))), 400
        return jsonify(ok(data=payload))

    # -----------------
    # Compound
    # -----------------

    @app.get("/api/v1/compound/skills")
    def compound_skills() -> Any:
        return jsonify(ok(data={"skills": list_skills(cfg.repo_root)}))

    @app.get("/api/v1/compound/skills/<name>")
    def compound_skill(name: str) -> Any:
        try:
            return jsonify(ok(data=read_skill(cfg.repo_root, name=str(name))))
        except FileNotFoundError as e:
            return jsonify(err(code="NOT_FOUND", message=str(e))), 404

    @app.get("/api/v1/compound/instincts")
    def compound_instincts() -> Any:
        return jsonify(ok(data=read_instincts(cfg.repo_root)))

    # -----------------
    # Errors
    # -----------------

    @app.errorhandler(404)
    def _not_found(_e: Exception) -> Any:
        return jsonify(err(code="NOT_FOUND", message="not found")), 404

    @app.errorhandler(405)
    def _method_not_allowed(_e: Exception) -> Any:
        return jsonify(
            err(code="METHOD_NOT_ALLOWED", message="method not allowed")
        ), 405

    @app.errorhandler(Exception)
    def _unhandled(e: Exception) -> Any:
        return jsonify(err(code="SERVER_ERROR", message=str(e))), 500

    return app
