from __future__ import annotations

from pathlib import Path
from typing import Any

from flask import Blueprint, jsonify, request

from agent_loom.dashboard.config import ServerConfig
from agent_loom.dashboard.http import err, ok


def create_team_blueprint(cfg: ServerConfig, *, api_error: Any) -> Blueprint:
    bp = Blueprint("dashboard_team", __name__, url_prefix="/api/v1/teams")

    @bp.get("")
    def teams_list() -> Any:
        from agent_loom.team.constants import DEFAULT_RUNS_DIR
        import json

        runs_dir = cfg.repo_root / DEFAULT_RUNS_DIR
        teams: list[dict[str, Any]] = []
        if runs_dir.exists():
            for d in sorted(
                [p for p in runs_dir.iterdir() if p.is_dir()], key=lambda p: p.name
            ):
                run_json = d / "run.json"
                if not run_json.exists():
                    continue
                try:
                    run = json.loads(run_json.read_text(encoding="utf-8", errors="replace"))
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

    @bp.get("/<team>/status")
    def team_status(team: str) -> Any:
        from agent_loom.team.core import status as team_status_fn

        try:
            res = team_status_fn(team=str(team), repo=cfg.repo_root)
        except Exception as e:
            payload, status = api_error(
                e,
                default_code="TEAM_STATUS_FAILED",
                default_message="team status failed",
            )
            return jsonify(payload), status
        return jsonify(ok(data=res))

    @bp.get("/<team>/run")
    def team_run(team: str) -> Any:
        from agent_loom.team.constants import DEFAULT_RUNS_DIR
        import json

        run_json = cfg.repo_root / DEFAULT_RUNS_DIR / str(team) / "run.json"
        if not run_json.exists():
            return jsonify(err(code="NOT_FOUND", message="team not found")), 404
        try:
            run = json.loads(run_json.read_text(encoding="utf-8", errors="replace"))
        except Exception as e:
            payload, status = api_error(
                e,
                default_code="READ_FAILED",
                default_message="failed to read team run state",
            )
            return jsonify(payload), status
        return jsonify(ok(data=run))

    @bp.get("/<team>/events")
    def team_events(team: str) -> Any:
        from agent_loom.team.constants import DEFAULT_RUNS_DIR
        import json

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

    @bp.get("/<team>/inbox")
    def team_inbox(team: str) -> Any:
        from agent_loom.team.constants import DEFAULT_RUNS_DIR
        import json

        base = cfg.repo_root / DEFAULT_RUNS_DIR / str(team) / "inbox"
        read_dir = base / "read"

        def _scan(d: Path, *, limit: int) -> list[dict[str, Any]]:
            if not d.exists():
                return []
            files = sorted(
                [p for p in d.glob("*.json")], key=lambda p: p.name, reverse=True
            )
            items: list[dict[str, Any]] = []
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

    @bp.get("/<team>/captures")
    def team_captures(team: str) -> Any:
        from agent_loom.team.constants import DEFAULT_RUNS_DIR
        import json

        captures_dir = cfg.repo_root / DEFAULT_RUNS_DIR / str(team) / "captures"
        if not captures_dir.exists():
            return jsonify(ok(data={"captures": [], "count": 0}))
        files = sorted(
            [p for p in captures_dir.glob("*.json")], key=lambda p: p.name, reverse=True
        )
        limit = int(request.args.get("limit") or 50)
        out: list[dict[str, Any]] = []
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

    @bp.get("/<team>/captures/text")
    def team_capture_text(team: str) -> Any:
        from agent_loom.team.constants import DEFAULT_RUNS_DIR
        import json

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

        cap_bytes = 200_000
        raw = b""
        truncated = False
        try:
            with open(txt_file, "rb") as f:
                raw = f.read(cap_bytes + 1)
        except Exception as e:
            payload, status = api_error(
                e,
                default_code="READ_FAILED",
                default_message="failed to read capture text",
            )
            return jsonify(payload), status

        if len(raw) > cap_bytes:
            truncated = True
            raw = raw[:cap_bytes]

        meta_payload: dict[str, Any] = {}
        try:
            meta_payload0 = json.loads(meta_file.read_text(encoding="utf-8", errors="replace"))
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

    return bp
