"""workspace_ui.py - read-only web UI for workspace worktrees + services graph.

Run:
  uv run src/agent_loom/ui/workspace_ui.py
  uv run src/agent_loom/ui/workspace_ui.py --mode auto
  uv run src/agent_loom/ui/workspace_ui.py --mode poly --root /path/to/workspace
  uv run src/agent_loom/ui/workspace_ui.py --mode repo --root /path/to/repo

Also available via:
  loom ui workspace

Notes
- Read-only: never mutates repos/workspaces.
- Serves a single HTML page + JSON APIs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import threading
import time
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple, cast
from urllib.parse import parse_qs, unquote

from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.guards import poly_context
from agent_loom.workspace.repo_ops import repo_root
from agent_loom.workspace.state import (
    fs_unescape,
    iter_repos,
    load_workspace,
    worktrees_base,
    ws_services_dir,
    ws_worktrees_dir,
)
from agent_loom.workspace.utils import is_git_repo, read_json, run, short, which
from agent_loom.workspace.git_ops import git_is_dirty, git_worktree_list_porcelain


class WorkspaceUIError(RuntimeError):
    pass


def _read_static_html() -> bytes:
    p = Path(__file__).with_name("workspace_ui.html")
    return p.read_bytes()


def _json_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, sort_keys=True) + "\n").encode("utf-8")


def _parse_qs(qs: str) -> Dict[str, str]:
    if not qs:
        return {}
    parsed = parse_qs(qs, keep_blank_values=True)
    return {k: (v[0] if v else "") for k, v in parsed.items()}


def _match_etag(header: str, etag: str) -> bool:
    if not header:
        return False
    for token in header.split(","):
        candidate = token.strip()
        if not candidate:
            continue
        if candidate.startswith("W/"):
            candidate = candidate[2:].strip()
        if candidate.strip('"') == etag:
            return True
    return False


def compute_etag(payload: Any) -> str:
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]


def _browser_host_for(host: str) -> str:
    if host.strip() in {"0.0.0.0", "::", "[::]", ""}:
        return "127.0.0.1"
    return host


def _open_browser_later(url: str, *, delay_s: float) -> None:
    def _work() -> None:
        try:
            if delay_s > 0:
                time.sleep(delay_s)
            webbrowser.open_new_tab(url)
        except Exception:
            return

    t = threading.Thread(target=_work, name="workspace_ui_open", daemon=True)
    t.start()


def _require_git() -> None:
    if not which("git"):
        raise WorkspaceUIError("git not found on PATH")


def _find_poly_root(start: Path) -> Optional[Path]:
    ctx = poly_context(start)
    if ctx.root and ctx.ws:
        return ctx.root
    return None


def _detect_mode(*, cwd: Path, mode: str, root_arg: str) -> Tuple[str, Path]:
    m = (mode or "auto").strip().lower()
    root_s = (root_arg or "").strip()

    if m not in {"auto", "poly", "repo"}:
        raise WorkspaceUIError("Invalid --mode (expected auto|poly|repo)")

    if m == "poly":
        root = Path(root_s).expanduser().resolve() if root_s else _find_poly_root(cwd)
        if not root:
            raise WorkspaceUIError(
                "Unable to find workspace root (expected workspace.json + .loom/). Use --root."
            )
        # Validate workspace config.
        _ = load_workspace(root)
        return "poly", root

    if m == "repo":
        _require_git()
        if root_s:
            root = Path(root_s).expanduser().resolve()
            if not is_git_repo(root):
                raise WorkspaceUIError(f"Not a git repo: {root}")
            return "repo", root
        return "repo", repo_root()

    # auto
    poly_root = _find_poly_root(cwd)
    if poly_root is not None:
        return "poly", poly_root
    _require_git()
    return "repo", repo_root()


def _safe_int(s: str, *, default: int, min_: int, max_: int) -> int:
    try:
        n = int(str(s).strip())
    except Exception:
        return default
    return max(min_, min(max_, n))


def _sha256_id(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def _porcelain_counts(lines: Iterable[str]) -> Dict[str, int]:
    # Very small heuristic; works for `git status --porcelain`.
    modified = 0
    added = 0
    deleted = 0
    untracked = 0
    for ln in lines:
        if not ln:
            continue
        if ln.startswith("??"):
            untracked += 1
            continue
        x = ln[0:1]
        y = ln[1:2]
        code = (x + y).strip()
        if "D" in code:
            deleted += 1
        elif "A" in code:
            added += 1
        else:
            modified += 1
    return {
        "modified": modified,
        "added": added,
        "deleted": deleted,
        "untracked": untracked,
    }


def _git_upstream(path: Path) -> Optional[str]:
    p = run(
        ["git", "rev-parse", "--abbrev-ref", "@{upstream}"],
        cwd=path,
        check=False,
    )
    if p.returncode != 0:
        return None
    out = (p.stdout or "").strip()
    return out or None


def _git_ahead_behind(path: Path, upstream: str) -> Optional[Dict[str, int]]:
    p = run(
        ["git", "rev-list", "--left-right", "--count", f"HEAD...{upstream}"],
        cwd=path,
        check=False,
    )
    if p.returncode != 0:
        return None
    raw = (p.stdout or "").strip().split()
    if len(raw) != 2:
        return None
    try:
        ahead = int(raw[0])
        behind = int(raw[1])
    except Exception:
        return None
    return {"ahead": ahead, "behind": behind}


def _git_last_commit(path: Path) -> Dict[str, str]:
    # subject\nunix_ts\nfullsha
    p = run(
        ["git", "log", "-1", "--pretty=%s%n%ct%n%H"],
        cwd=path,
        check=False,
    )
    if p.returncode != 0:
        return {"subject": "", "ts": "", "sha": ""}
    lines = (p.stdout or "").splitlines()
    subject = lines[0].strip() if len(lines) >= 1 else ""
    ts = lines[1].strip() if len(lines) >= 2 else ""
    sha = lines[2].strip() if len(lines) >= 3 else ""
    return {"subject": subject, "ts": ts, "sha": sha}


def _worktree_details(path: Path, *, default_branch: str = "") -> Dict[str, Any]:
    if not path.exists() or not is_git_repo(path):
        return {
            "ok": False,
            "path": str(path),
            "error": "not a git worktree",
        }

    br = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=path, check=False)
    branch = (br.stdout or "").strip() if br.returncode == 0 else ""
    sha_full = run(["git", "rev-parse", "HEAD"], cwd=path, check=False)
    head = (sha_full.stdout or "").strip() if sha_full.returncode == 0 else ""

    status = run(["git", "status", "--porcelain"], cwd=path, check=False)
    st_lines = (status.stdout or "").splitlines()
    dirty = bool("\n".join(st_lines).strip())
    counts = _porcelain_counts(st_lines)

    upstream = _git_upstream(path)
    ahead_behind = _git_ahead_behind(path, upstream) if upstream else None
    last = _git_last_commit(path)

    base = (default_branch or "").strip()
    base_cmp: Optional[Dict[str, int]] = None
    if base and base != "HEAD":
        # Compare HEAD vs origin/<base> if it exists, else the local base.
        preferred = f"origin/{base}" if not base.startswith("origin/") else base
        target = preferred
        pcmp = run(
            ["git", "rev-list", "--left-right", "--count", f"HEAD...{target}"],
            cwd=path,
            check=False,
        )
        if pcmp.returncode == 0:
            raw = (pcmp.stdout or "").strip().split()
            if len(raw) == 2:
                try:
                    base_cmp = {"ahead": int(raw[0]), "behind": int(raw[1])}
                except Exception:
                    base_cmp = None

    return {
        "ok": True,
        "path": str(path.resolve()),
        "branch": branch,
        "head": head,
        "head_short": short(head) if head else "",
        "dirty": dirty,
        "counts": counts,
        "upstream": upstream or "",
        "ahead_behind": ahead_behind,
        "last_commit": last,
        "default_branch": base,
        "default_branch_cmp": base_cmp,
        "commands": [
            f"cd {str(path.resolve())}",
            "git status",
            "git log -n 20 --graph --oneline",
        ],
    }


def _service_excerpt(md_path: Path) -> str:
    if not md_path.exists():
        return ""
    try:
        text = md_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

    lines = text.splitlines()
    out: List[str] = []
    in_summary = False
    for ln in lines:
        if ln.strip().lower().startswith("## "):
            in_summary = ln.strip().lower().startswith("## summary")
            continue
        if in_summary:
            if ln.strip().startswith("## "):
                break
            out.append(ln)
            if len(out) >= 24:
                break
    excerpt = "\n".join(out).strip()
    return excerpt


def _services_index(root: Path) -> Optional[dict]:
    ws = load_workspace(root)
    idx = root / ws_services_dir(ws) / "index.json"
    if not idx.exists():
        return None
    try:
        data = read_json(idx)
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    return data


def _services_graph(index: dict) -> Dict[str, Any]:
    services = index.get("services") if isinstance(index, dict) else None
    if not isinstance(services, dict):
        return {"nodes": [], "edges": []}

    nodes: Dict[str, Dict[str, Any]] = {}
    edges: List[Dict[str, str]] = []

    def _ensure_node(n: str, kind: str) -> None:
        if n in nodes:
            return
        nodes[n] = {"id": n, "name": n, "kind": kind}

    for name, entry in services.items():
        if not isinstance(name, str):
            continue
        if not isinstance(entry, dict):
            entry = {}
        _ensure_node(name, "internal")
        nodes[name]["repo_path"] = str(entry.get("repo_path") or "")
        nodes[name]["depends_on"] = list(entry.get("depends_on") or [])
        nodes[name]["depends_on_external"] = list(
            entry.get("depends_on_external") or []
        )
        nodes[name]["used_by"] = list(entry.get("used_by") or [])

    for name, entry in services.items():
        if not isinstance(name, str) or not isinstance(entry, dict):
            continue
        for dep in entry.get("depends_on") or []:
            if not isinstance(dep, str) or not dep:
                continue
            _ensure_node(dep, "internal" if dep in services else "external")
            edges.append({"from": name, "to": dep, "kind": "internal"})
        for dep in entry.get("depends_on_external") or []:
            if not isinstance(dep, str) or not dep:
                continue
            _ensure_node(dep, "external")
            edges.append({"from": name, "to": dep, "kind": "external"})

    node_list = sorted(
        nodes.values(), key=lambda x: (x.get("kind") != "internal", x["id"])
    )
    edge_list = sorted(edges, key=lambda e: (e["from"], e["to"], e["kind"]))
    return {"nodes": node_list, "edges": edge_list}


def _poly_meta(root: Path) -> Dict[str, Any]:
    ws = load_workspace(root)
    wt_dir = root / ws_worktrees_dir(ws)
    groups: List[str] = []
    if wt_dir.exists():
        for p in sorted(wt_dir.iterdir()):
            if p.is_dir():
                groups.append(fs_unescape(p.name))
    repos = sorted(iter_repos(ws).keys())
    return {
        "mode": "poly",
        "root": str(root.resolve()),
        "groups": groups,
        "repos": repos,
        "paths": {
            "worktrees_dir": str((root / ws_worktrees_dir(ws)).resolve()),
            "services_dir": str((root / ws_services_dir(ws)).resolve()),
        },
    }


def _repo_meta(root: Path) -> Dict[str, Any]:
    return {
        "mode": "repo",
        "root": str(root.resolve()),
    }


def _poly_worktrees(
    *, root: Path, group: str, repo: str, q: str, dirty_only: bool, missing_only: bool
) -> Dict[str, Any]:
    ws = load_workspace(root)
    repo_map = iter_repos(ws)

    # Build list from filesystem; do not call mutating ops.
    wt_dir = root / ws_worktrees_dir(ws)
    items: List[Dict[str, Any]] = []
    if wt_dir.exists():
        for group_dir in sorted(wt_dir.iterdir()):
            if not group_dir.is_dir():
                continue
            g = fs_unescape(group_dir.name)
            if group and g != group:
                continue
            for repo_dir in sorted(group_dir.iterdir()):
                if not repo_dir.is_dir():
                    continue
                rname = repo_dir.name
                if repo and rname != repo:
                    continue
                entry: Dict[str, Any] = {
                    "mode": "poly",
                    "id": f"{g}:{rname}",
                    "group": g,
                    "repo": rname,
                    "path": str(repo_dir.resolve()),
                    "missing": False,
                    "is_repo": is_git_repo(repo_dir),
                }
                if entry["is_repo"]:
                    entry.update(
                        {
                            "branch": run(
                                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                cwd=repo_dir,
                                check=False,
                            ).stdout.strip(),
                            "commit": run(
                                ["git", "rev-parse", "HEAD"], cwd=repo_dir, check=False
                            ).stdout.strip(),
                            "dirty": git_is_dirty(repo_dir),
                        }
                    )
                items.append(entry)

    # Add missing items (only meaningful when group is set).
    if group:
        base = worktrees_base(root, ws, group)
        present = {x.get("repo") for x in items if x.get("group") == group}
        for rname in sorted(repo_map.keys()):
            if repo and rname != repo:
                continue
            if rname in present:
                continue
            expected = base / rname
            items.append(
                {
                    "mode": "poly",
                    "id": f"{group}:{rname}",
                    "group": group,
                    "repo": rname,
                    "path": str(expected.resolve()),
                    "missing": True,
                    "is_repo": False,
                }
            )

    # Client-style filtering.
    query = (q or "").strip().lower()

    def _matches(it: Mapping[str, Any]) -> bool:
        if dirty_only and not bool(it.get("dirty")):
            return False
        if missing_only and not bool(it.get("missing")):
            return False
        if query:
            blob = " ".join(
                [
                    str(it.get("group") or ""),
                    str(it.get("repo") or ""),
                    str(it.get("branch") or ""),
                    str(it.get("path") or ""),
                ]
            ).lower()
            if query not in blob:
                return False
        return True

    items = [it for it in items if _matches(it)]
    return {"ok": True, "worktrees": items, "count": len(items)}


def _repo_worktrees(
    *, root: Path, q: str, dirty_only: bool, detached_only: bool
) -> Dict[str, Any]:
    rows = git_worktree_list_porcelain(root)
    items: List[Dict[str, Any]] = []
    query = (q or "").strip().lower()
    for row in rows:
        path = str(row.get("path") or "")
        if not path:
            continue
        p = Path(path).resolve()
        wid = _sha256_id(str(p))
        branch = str(row.get("branch") or "")
        detached = bool(row.get("detached"))

        if detached_only and not detached:
            continue

        entry: Dict[str, Any] = {
            "mode": "repo",
            "id": wid,
            "path": str(p),
            "head": str(row.get("head") or ""),
            "head_short": short(str(row.get("head") or "")) if row.get("head") else "",
            "branch": branch,
            "ref": str(row.get("ref") or ""),
            "detached": detached,
            "locked": bool(row.get("locked")),
            "is_repo": is_git_repo(p),
            "dirty": git_is_dirty(p) if is_git_repo(p) else False,
        }
        if dirty_only and not bool(entry.get("dirty")):
            continue
        if query:
            blob = " ".join(
                [str(entry.get("branch") or ""), str(entry.get("path") or "")]
            ).lower()
            if query not in blob:
                continue
        items.append(entry)
    return {"ok": True, "worktrees": items, "count": len(items)}


def _repo_worktree_by_id(root: Path, worktree_id: str) -> Optional[Path]:
    want = (worktree_id or "").strip()
    if not want:
        return None
    for row in git_worktree_list_porcelain(root):
        p = str(row.get("path") or "").strip()
        if not p:
            continue
        rp = Path(p).resolve()
        if _sha256_id(str(rp)) == want:
            return rp
    return None


def _poly_worktree_path(root: Path, group: str, repo: str) -> Path:
    ws = load_workspace(root)
    base = worktrees_base(root, ws, group)
    return (base / repo).resolve()


class WorkspaceUIServer(ThreadingHTTPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        handler_cls: type[BaseHTTPRequestHandler],
        *,
        html_content: bytes,
        mode: str,
        root: Path,
    ) -> None:
        super().__init__(server_address, handler_cls)
        self.html_content = html_content
        self.mode = mode
        self.root = root


class WorkspaceUIHandler(BaseHTTPRequestHandler):
    server_version = "workspace-ui/0"

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    def _server(self) -> WorkspaceUIServer:
        return cast(WorkspaceUIServer, self.server)

    def _send(
        self, *, status: int, body: bytes, content_type: str, etag: str = ""
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if etag:
            self.send_header("ETag", etag)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, obj: Any, *, etag: str = "") -> None:
        self._send(
            status=status,
            body=_json_bytes(obj),
            content_type="application/json",
            etag=etag,
        )

    def do_GET(self) -> None:  # noqa: N802
        try:
            self._do_GET()
        except (WorkspaceError, WorkspaceUIError) as e:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {"ok": False, "error": str(e), "code": "UI_ERROR"},
            )
        except Exception as e:
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"ok": False, "error": str(e), "code": "SERVER_ERROR"},
            )

    def _do_GET(self) -> None:
        path, _, qs = self.path.partition("?")
        server = self._server()

        if path in {"/", "/index.html"}:
            self._send(
                status=HTTPStatus.OK,
                body=server.html_content,
                content_type="text/html; charset=utf-8",
            )
            return

        q = _parse_qs(qs)
        mode = (q.get("mode") or server.mode).strip().lower()
        if mode not in {"poly", "repo"}:
            mode = server.mode

        if path == "/api/meta":
            if mode == "poly":
                payload = _poly_meta(server.root)
            else:
                payload = _repo_meta(server.root)
            payload["ok"] = True
            self._send_json(HTTPStatus.OK, payload)
            return

        if path == "/api/worktrees":
            q_group = (q.get("group") or "").strip()
            q_repo = (q.get("repo") or "").strip()
            q_search = (q.get("q") or "").strip()
            dirty_only = (q.get("dirty") or "") == "1"
            detached_only = (q.get("detached") or "") == "1"
            missing_only = (q.get("missing") or "") == "1"

            if mode == "poly":
                payload = _poly_worktrees(
                    root=server.root,
                    group=q_group,
                    repo=q_repo,
                    q=q_search,
                    dirty_only=dirty_only,
                    missing_only=missing_only,
                )
            else:
                payload = _repo_worktrees(
                    root=server.root,
                    q=q_search,
                    dirty_only=dirty_only,
                    detached_only=detached_only,
                )

            etag = compute_etag(payload)
            if _match_etag(self.headers.get("If-None-Match") or "", etag):
                self.send_response(HTTPStatus.NOT_MODIFIED)
                self.send_header("Cache-Control", "no-store")
                self.send_header("ETag", etag)
                self.send_header("X-Content-Type-Options", "nosniff")
                self.end_headers()
                return

            self._send_json(HTTPStatus.OK, payload, etag=etag)
            return

        if path == "/api/worktrees/detail":
            if mode == "poly":
                group = (q.get("group") or "").strip()
                repo = (q.get("repo") or "").strip()
                if not group or not repo:
                    raise WorkspaceUIError("Missing group/repo")
                wt_path = _poly_worktree_path(server.root, group, repo)
                ws = load_workspace(server.root)
                repo_map = iter_repos(ws)
                r = repo_map.get(repo)
                default_branch = r.default_branch if r else ""
                detail = _worktree_details(wt_path, default_branch=default_branch)
                detail.update({"mode": "poly", "group": group, "repo": repo})
                self._send_json(HTTPStatus.OK, detail)
                return

            wid = (q.get("id") or "").strip()
            if not wid:
                raise WorkspaceUIError("Missing id")
            wt_path = _repo_worktree_by_id(server.root, wid)
            if wt_path is None:
                raise WorkspaceUIError("Unknown worktree")
            default_branch = ""
            try:
                default_branch = run(
                    ["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"],
                    cwd=server.root,
                    check=False,
                ).stdout.strip()
                if default_branch.startswith("origin/"):
                    default_branch = default_branch[len("origin/") :]
            except Exception:
                default_branch = ""
            detail = _worktree_details(wt_path, default_branch=default_branch)
            detail.update({"mode": "repo", "id": wid})
            self._send_json(HTTPStatus.OK, detail)
            return

        if path == "/api/services/index":
            if mode != "poly":
                self._send_json(HTTPStatus.OK, {"ok": True, "index": None})
                return
            idx = _services_index(server.root)
            self._send_json(HTTPStatus.OK, {"ok": True, "index": idx})
            return

        if path == "/api/services/graph":
            if mode != "poly":
                self._send_json(HTTPStatus.OK, {"ok": True, "nodes": [], "edges": []})
                return
            idx = _services_index(server.root)
            graph = _services_graph(idx or {})
            payload = {"ok": True, **graph}

            etag = compute_etag(payload)
            if _match_etag(self.headers.get("If-None-Match") or "", etag):
                self.send_response(HTTPStatus.NOT_MODIFIED)
                self.send_header("Cache-Control", "no-store")
                self.send_header("ETag", etag)
                self.send_header("X-Content-Type-Options", "nosniff")
                self.end_headers()
                return

            self._send_json(HTTPStatus.OK, payload, etag=etag)
            return

        if path == "/api/services/detail":
            if mode != "poly":
                self._send_json(
                    HTTPStatus.OK,
                    {
                        "ok": False,
                        "error": "services graph only available in poly mode",
                    },
                )
                return
            name = unquote((q.get("name") or "").strip())
            if not name:
                raise WorkspaceUIError("Missing name")
            idx = _services_index(server.root) or {}
            services = idx.get("services") if isinstance(idx, dict) else None
            if not isinstance(services, dict) or name not in services:
                raise WorkspaceUIError("Unknown service")
            entry_obj = services.get(name)
            entry: dict = entry_obj if isinstance(entry_obj, dict) else {}

            ws = load_workspace(server.root)
            md_path = server.root / ws_services_dir(ws) / f"{name}.md"
            excerpt = _service_excerpt(md_path)

            payload = {
                "ok": True,
                "name": name,
                "repo_path": str(entry.get("repo_path") or ""),
                "depends_on": list(entry.get("depends_on") or []),
                "depends_on_external": list(entry.get("depends_on_external") or []),
                "used_by": list(entry.get("used_by") or []),
                "service_md": str(md_path.resolve()),
                "summary_excerpt": excerpt,
            }
            self._send_json(HTTPStatus.OK, payload)
            return

        self._send(
            status=HTTPStatus.NOT_FOUND,
            body=b"not found\n",
            content_type="text/plain; charset=utf-8",
        )


def parse_args(argv: Optional[List[str]]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="workspace_ui",
        description="Start the workspace web UI and open a browser tab.",
    )
    p.add_argument("--host", default="127.0.0.1", help="Listen address")
    p.add_argument(
        "--port",
        type=int,
        default=None,
        help="Listen port (default: try 8766, then random free port)",
    )
    p.add_argument(
        "--mode",
        default="auto",
        help="auto|poly|repo (default: auto)",
    )
    p.add_argument(
        "--root",
        default="",
        help="Root path (workspace root for poly, repo root for repo)",
    )
    p.add_argument("--no-open", action="store_true", help="Do not auto-open a tab")
    return p.parse_args(argv)


def run_web(
    *, host: str, port: Optional[int], mode: str, root: Path, open_browser: bool
) -> None:
    html_content = _read_static_html()
    port_requested = port
    try_ports = [int(port_requested)] if port_requested is not None else [8766, 0]

    last_err: Optional[BaseException] = None
    srv: Optional[WorkspaceUIServer] = None
    for p in try_ports:
        try:
            srv = WorkspaceUIServer(
                (host, p),
                WorkspaceUIHandler,
                html_content=html_content,
                mode=mode,
                root=root,
            )
            break
        except OSError as e:
            last_err = e

    if srv is None:
        assert last_err is not None
        raise last_err

    bound_host, bound_port = srv.socket.getsockname()[:2]
    url = f"http://{_browser_host_for(host)}:{bound_port}/"
    print(f"Workspace UI running at {url} (listening on {bound_host}:{bound_port})")
    print(f"Mode: {mode} Root: {root}")

    if open_browser:
        _open_browser_later(url, delay_s=0.25)

    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    mode, root = _detect_mode(
        cwd=Path.cwd(), mode=str(args.mode), root_arg=str(args.root)
    )
    run_web(
        host=str(args.host),
        port=(int(args.port) if args.port is not None else None),
        mode=mode,
        root=root,
        open_browser=(not bool(args.no_open)),
    )


if __name__ == "__main__":
    main()
