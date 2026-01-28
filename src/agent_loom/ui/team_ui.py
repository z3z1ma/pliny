"""team_ui.py - readonly web UI for team runs.

Goals:
- Observability plane for team dynamics.
- Real-time updates via polling.
- Read-only (mostly) view of run state, events, and inbox.

Run:
  uv run team_ui.py
  uv run team_ui.py --team my-team
  uv run team_ui.py --host 0.0.0.0 --port 9876
"""

import argparse
import json
import re
import threading
import time
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional, cast
from urllib.parse import parse_qs, quote

from agent_loom.team.constants import DEFAULT_RUNS_DIR
from agent_loom.team.errors import TeamError
from agent_loom.team.run_state import canonical_repo_root, discover_repo_root_for_team

# -----------------------------
# Data Access
# -----------------------------


def _read_json(path: Path) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def list_teams(repo_root: Path) -> List[Dict[str, Any]]:
    runs_dir = repo_root / DEFAULT_RUNS_DIR
    if not runs_dir.exists():
        return []

    teams = []
    for d in runs_dir.iterdir():
        if d.is_dir() and (d / "run.json").exists():
            # Try to read basic info
            run = _read_json(d / "run.json") or {}
            teams.append(
                {
                    "team": d.name,
                    "created_at": run.get("created_at"),
                    "updated_at": run.get("updated_at"),
                    "objective": run.get("objective"),
                    "session": run.get("session"),
                }
            )

    # Sort by updated_at desc
    return sorted(
        teams,
        key=lambda x: str(x.get("updated_at") or x.get("created_at") or ""),
        reverse=True,
    )


def get_run_state(repo_root: Path, team: str) -> Dict[str, Any]:
    run_dir = repo_root / DEFAULT_RUNS_DIR / team
    if not run_dir.exists():
        return {"ok": False, "error": "Team not found"}

    run_data = _read_json(run_dir / "run.json") or {}
    status_data = _read_json(run_dir / "snapshots" / "status.json")

    # Basic merge queue stats
    merge_items = (run_data.get("merge") or {}).get("items") or []
    merge_stats = {
        "total": len(merge_items),
        "queued": sum(1 for i in merge_items if i.get("state") == "queued"),
        "claimed": sum(1 for i in merge_items if i.get("state") == "claimed"),
        "done": sum(1 for i in merge_items if i.get("state") == "done"),
    }

    return {
        "ok": True,
        "team": team,
        "run": run_data,
        "status": status_data,
        "merge_stats": merge_stats,
    }


def list_events(
    repo_root: Path, team: str, limit: int = 100, since: Optional[str] = None
) -> List[Dict[str, Any]]:
    events_dir = repo_root / DEFAULT_RUNS_DIR / team / "events"
    if not events_dir.exists():
        return []

    # Files are named <stamp>_<id>_<type>.json
    # We can sort by filename to get chronological order.
    files = sorted(events_dir.glob("*.json"), key=lambda p: p.name, reverse=True)

    events = []
    for p in files:
        if since and p.name < since:
            continue

        data = _read_json(p)
        if data:
            # Inject filename as a cursor for "since"
            data["_cursor"] = p.name
            events.append(data)
            if len(events) >= limit:
                break

    return events


def list_inbox(
    repo_root: Path, team: str, limit: int = 50
) -> Dict[str, List[Dict[str, Any]]]:
    base = repo_root / DEFAULT_RUNS_DIR / team / "inbox"
    read_dir = base / "read"

    def _scan(d: Path) -> List[Dict[str, Any]]:
        if not d.exists():
            return []
        files = sorted(d.glob("*.json"), key=lambda p: p.name, reverse=True)
        items = []
        for p in files:
            data = _read_json(p)
            if data:
                items.append(data)
            if len(items) >= limit:
                break
        return items

    return {
        "unread": _scan(base),
        "read": _scan(read_dir),
    }


def list_captures(repo_root: Path, team: str, limit: int = 50) -> List[Dict[str, Any]]:
    captures_dir = repo_root / DEFAULT_RUNS_DIR / team / "captures"
    if not captures_dir.exists():
        return []

    # Files are named <stamp>_<id>_<target>.json / .txt
    files = sorted(captures_dir.glob("*.json"), key=lambda p: p.name, reverse=True)
    items = []
    for p in files:
        data = _read_json(p)
        if data:
            data.setdefault("_meta", p.name)
            items.append(data)
        if len(items) >= limit:
            break
    return items


# -----------------------------
# Helpers
# -----------------------------


def _search_repo_root(cwd: Path) -> Optional[Path]:
    # Look for .team directory or .git
    cur = cwd.resolve()
    while True:
        if (cur / ".team").is_dir():
            return cur
        if (cur / ".git").exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def find_repo_root(cwd: Path, *, team: Optional[str] = None) -> Optional[Path]:
    if team:
        discovered = discover_repo_root_for_team(team, start=cwd)
        if discovered is not None:
            return discovered
    try:
        return canonical_repo_root(cwd)
    except TeamError:
        return _search_repo_root(cwd)


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

    t = threading.Thread(target=_work, name="team_ui_open", daemon=True)
    t.start()


# -----------------------------
# HTTP Server
# -----------------------------


class TeamUIHandler(BaseHTTPRequestHandler):
    def _server(self) -> "TeamUIServer":
        return cast(TeamUIServer, self.server)

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send_json(self, status: int, obj: Any) -> None:
        body = json.dumps(obj, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, body: bytes) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, status: int, body: str) -> None:
        raw = body.encode("utf-8", errors="replace")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        path, _, qs = self.path.partition("?")
        server = self._server()

        if path == "/":
            if qs:
                self._send_html(server.html_content)
                return
            if server.default_team:
                target = f"/?team={quote(server.default_team)}"
                self.send_response(HTTPStatus.FOUND)
                self.send_header("Location", target)
                self.send_header("Cache-Control", "no-store")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.end_headers()
                return
            self._send_html(server.html_content)
            return

        # API
        repo_root = server.repo_root

        if path == "/api/teams":
            self._send_json(200, {"teams": list_teams(repo_root)})
            return

        # Parse query params (decode %-escapes)
        q: Dict[str, str] = {}
        if qs:
            parsed = parse_qs(qs, keep_blank_values=True)
            q = {k: (v[0] if v else "") for k, v in parsed.items()}

        team = q.get("team")

        if path == "/api/state":
            if not team:
                self._send_json(400, {"error": "Missing team param"})
                return
            self._send_json(200, get_run_state(repo_root, team))
            return

        if path == "/api/events":
            if not team:
                self._send_json(400, {"error": "Missing team param"})
                return
            limit = int(q.get("limit", 100))
            since = q.get("since")
            self._send_json(200, {"events": list_events(repo_root, team, limit, since)})
            return

        if path == "/api/inbox":
            if not team:
                self._send_json(400, {"error": "Missing team param"})
                return
            self._send_json(200, list_inbox(repo_root, team))
            return

        if path == "/api/captures":
            if not team:
                self._send_json(400, {"error": "Missing team param"})
                return
            self._send_json(200, {"captures": list_captures(repo_root, team)})
            return

        if path == "/api/capture":
            if not team:
                self._send_json(400, {"error": "Missing team param"})
                return

            meta = str(q.get("meta") or "").strip()
            if not meta:
                self._send_json(400, {"error": "Missing meta param"})
                return

            # Safety: meta must be a basename like "...json" (no path traversal).
            meta_name = Path(meta).name
            if meta_name != meta or not re.fullmatch(
                r"[A-Za-z0-9._-]+\.json", meta_name
            ):
                self._send_json(400, {"error": "Invalid meta param"})
                return

            captures_dir = repo_root / DEFAULT_RUNS_DIR / team / "captures"
            cap_json = captures_dir / meta_name
            if not cap_json.exists():
                self._send_json(404, {"error": "Capture not found"})
                return

            cap_txt = cap_json.with_suffix(".txt")
            if not cap_txt.exists():
                self._send_json(404, {"error": "Capture text not found"})
                return

            try:
                text = cap_txt.read_text(encoding="utf-8", errors="replace")
            except Exception:
                self._send_json(500, {"error": "Failed to read capture"})
                return

            self._send_text(200, text)
            return

        self.send_error(404)


class TeamUIServer(ThreadingHTTPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        handler_cls: type[BaseHTTPRequestHandler],
        *,
        repo_root: Path,
        html_content: bytes,
        default_team: Optional[str],
    ) -> None:
        super().__init__(server_address, handler_cls)
        self.repo_root = repo_root
        self.html_content = html_content
        self.default_team = default_team


def run_server(
    host: str,
    port: Optional[int],
    repo_root: Path,
    open_browser: bool,
    default_team: Optional[str],
) -> None:
    html_path = Path(__file__).with_name("team_ui.html")
    if not html_path.exists():
        print(f"Error: {html_path} not found")
        return

    # Bind
    server: Optional[TeamUIServer] = None
    port_requested = port
    try_ports = [int(port_requested)] if port_requested is not None else [9876, 0]
    last_err: Optional[OSError] = None

    for p in try_ports:
        try:
            server = TeamUIServer(
                (host, p),
                TeamUIHandler,
                repo_root=repo_root,
                html_content=html_path.read_bytes(),
                default_team=default_team,
            )
            break
        except OSError as e:
            last_err = e
            continue

    if not server:
        if last_err:
            print(f"Could not bind to any port: {last_err}")
        else:
            print("Could not bind to any port")
        return

    host_name, port_num = server.socket.getsockname()[:2]
    url = f"http://{_browser_host_for(host_name)}:{port_num}/"
    if default_team:
        url = f"{url}?team={quote(default_team)}"

    print(f"Team UI running at {url}")
    print(f"Repo root: {repo_root}")

    if open_browser:
        _open_browser_later(url, delay_s=0.5)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def main(argv: Optional[List[str]] = None) -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=None)
    p.add_argument("--team", default="", help="Default team to open")
    p.add_argument("--repo", help="Path to repo root (optional)")
    p.add_argument("--no-open", action="store_true")
    args = p.parse_args(argv)

    team = str(getattr(args, "team", "") or "").strip() or None
    repo = (
        Path(args.repo).resolve()
        if args.repo
        else find_repo_root(Path.cwd(), team=team)
    )
    if not repo:
        print("Error: Could not find repo root (no .team or .git found in parents)")
        print("Try running from the repo root or use --repo")
        return

    run_server(args.host, args.port, repo, not args.no_open, team)


if __name__ == "__main__":
    main()
