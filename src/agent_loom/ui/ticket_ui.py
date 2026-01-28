"""ticket_ui.py - readonly web UI for loom tickets.

Goals
 - Read-only: imports Loom ticket library and serves JSON.
- Web: serve ticket_ui.html + JSON API.
- Readonly: never writes tickets.

Run
  uv run ticket_ui.py
  uv run ticket_ui.py --tickets-dir /path/to/.tickets
  uv run ticket_ui.py --host 0.0.0.0 --port 8765

Notes
- By default, the server tries port 8765; if it's busy, it falls back to a random free
  port.
- By default, a browser tab is opened automatically (use --no-open to disable).

Env
  TICKET_DIR: passed through to loom ticket
"""

import argparse
import contextlib
import hashlib
import io
import json
import os
import threading
import time
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, cast
from urllib.parse import parse_qs, unquote

from agent_loom.core.env import patched_environ
from agent_loom.ticket import cli as ticket_cli


def find_tickets_dir(cwd: Path) -> Optional[Path]:
    d = cwd.resolve()
    while True:
        cand = d / ".tickets"
        if cand.is_dir():
            return cand
        if d.parent == d:
            return None
        d = d.parent


# -----------------------------
# loom ticket in-process adapter
# -----------------------------


class TicketError(RuntimeError):
    pass


def _run_ticket_json(
    args: List[str],
    *,
    tickets_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    env = os.environ.copy()

    if tickets_dir is not None:
        env["TICKET_DIR"] = str(tickets_dir)
    elif not env.get("TICKET_DIR"):
        auto = find_tickets_dir(Path.cwd())
        if auto is not None:
            env["TICKET_DIR"] = str(auto)

    out_buf = io.StringIO()
    err_buf = io.StringIO()
    code = 0
    with patched_environ(env):
        with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
            try:
                ticket_cli(["--json", *args])
            except SystemExit as e:
                code = int(getattr(e, "code", 0) or 0)

    out = (out_buf.getvalue() or "").strip()
    err = (err_buf.getvalue() or "").strip()
    if code != 0:
        raise TicketError(f"loom ticket failed ({code}): {err or out}")

    try:
        data = json.loads(out or "{}")
    except Exception as e:
        raise TicketError(f"Invalid JSON from loom ticket: {out[:200]!r}") from e

    if not isinstance(data, dict) or data.get("ok") is False:
        raise TicketError(str(data.get("error") or "loom ticket error"))

    return data


def ticket_list(
    *,
    status: str = "",
    type_: str = "",
    assignee: str = "",
    tag: str = "",
    prio_min: Optional[int] = None,
    prio_max: Optional[int] = None,
    include_closed: bool = True,
    tickets_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    args: List[str] = ["list"]
    if status:
        args += ["--status", status]
    if type_:
        args += ["--type", type_]
    if assignee:
        args += ["-a", assignee]
    if tag:
        args += ["-T", tag]
    if prio_min is not None:
        args += ["--prio-min", str(int(prio_min))]
    if prio_max is not None:
        args += ["--prio-max", str(int(prio_max))]
    if include_closed:
        args += ["--all"]
    return _run_ticket_json(args, tickets_dir=tickets_dir)


def ticket_show(
    ticket_id: str, *, tickets_dir: Optional[Path] = None
) -> Dict[str, Any]:
    return _run_ticket_json(["show", ticket_id], tickets_dir=tickets_dir)


# -----------------------------
# Change detection
# -----------------------------


def compute_etag_from_list(list_payload: Mapping[str, Any]) -> str:
    tickets = list_payload.get("tickets") or []
    blob = json.dumps(tickets, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]


# -----------------------------
# Web server (static HTML + JSON API)
# -----------------------------


def _read_static_html() -> bytes:
    p = Path(__file__).with_name("ticket_ui.html")
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


class TicketUIServer(ThreadingHTTPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        handler_cls: type[BaseHTTPRequestHandler],
        *,
        tickets_dir: Optional[Path],
        html_content: bytes,
    ) -> None:
        super().__init__(server_address, handler_cls)
        self.tickets_dir = tickets_dir
        self.html_content = html_content


class TicketUIHandler(BaseHTTPRequestHandler):
    server_version = "ticket-ui/0"

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        # Keep output quiet; only print an explicit startup line.
        return

    def _server(self) -> TicketUIServer:
        return cast(TicketUIServer, self.server)

    def _send(self, *, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, obj: Any) -> None:
        self._send(
            status=status, body=_json_bytes(obj), content_type="application/json"
        )

    def do_GET(self) -> None:  # noqa: N802
        try:
            self._do_GET()
        except TicketError as e:
            self._send_json(
                HTTPStatus.BAD_GATEWAY,
                {"ok": False, "error": str(e), "code": "TK_ERROR"},
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

        if path == "/api/meta":
            self._send_json(
                HTTPStatus.OK,
                {
                    "ok": True,
                    "statuses": ["open", "in_progress", "closed"],
                    "types": ["task", "bug", "feature", "epic", "chore"],
                },
            )
            return

        if path == "/api/tickets":
            q = _parse_qs(qs)
            payload = ticket_list(
                status=q.get("status", ""),
                type_=q.get("type", ""),
                assignee=q.get("assignee", ""),
                tag=q.get("tag", ""),
                prio_min=int(q["prio_min"]) if q.get("prio_min") else None,
                prio_max=int(q["prio_max"]) if q.get("prio_max") else None,
                include_closed=(q.get("all", "1") != "0"),
                tickets_dir=server.tickets_dir,
            )

            query = (q.get("q") or "").strip().lower()
            if query:
                tickets = payload.get("tickets") or []
                filtered = [
                    t
                    for t in tickets
                    if query in str(t.get("id", "")).lower()
                    or query in str(t.get("title", "")).lower()
                    or query in str(t.get("assignee", "")).lower()
                    or any(query in str(x).lower() for x in (t.get("tags") or []))
                ]
                payload = dict(payload)
                payload["tickets"] = filtered
                payload["count"] = len(filtered)

            etag = compute_etag_from_list(payload)
            if _match_etag(self.headers.get("If-None-Match") or "", etag):
                self.send_response(HTTPStatus.NOT_MODIFIED)
                self.send_header("Cache-Control", "no-store")
                self.send_header("ETag", etag)
                self.send_header("X-Content-Type-Options", "nosniff")
                self.end_headers()
                return

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("ETag", etag)
            self.send_header("X-Content-Type-Options", "nosniff")
            body = _json_bytes(payload)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path.startswith("/api/tickets/"):
            tid = unquote(path.split("/", 3)[-1])
            payload = ticket_show(tid, tickets_dir=server.tickets_dir)
            self._send_json(HTTPStatus.OK, payload)
            return

        self._send(
            status=HTTPStatus.NOT_FOUND,
            body=b"not found\n",
            content_type="text/plain; charset=utf-8",
        )


def _format_tickets_dir_for_log(tickets_dir: Optional[Path]) -> str:
    if tickets_dir is None:
        return "auto"
    try:
        return str(tickets_dir)
    except Exception:
        return repr(tickets_dir)


def _browser_host_for(host: str) -> str:
    # Browsers won't navigate to 0.0.0.0 / ::, and localhost can be configured
    # weirdly. Prefer a stable loopback.
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
            # Best-effort only; server still runs.
            return

    t = threading.Thread(target=_work, name="ticket_ui_open_browser", daemon=True)
    t.start()


def run_web(
    *,
    host: str,
    port: Optional[int],
    tickets_dir: Optional[Path],
    open_browser: bool,
) -> None:
    html_content = _read_static_html()
    port_requested = port
    if port_requested is None:
        # Try a memorable port first, then fall back to an ephemeral port.
        try_ports = [8765, 0]
    else:
        try_ports = [int(port_requested)]

    last_err: Optional[BaseException] = None
    srv: Optional[TicketUIServer] = None
    for p in try_ports:
        try:
            srv = TicketUIServer(
                (host, p),
                TicketUIHandler,
                tickets_dir=tickets_dir,
                html_content=html_content,
            )
            break
        except OSError as e:
            last_err = e

    if srv is None:
        assert last_err is not None
        raise last_err

    bound_host, bound_port = srv.socket.getsockname()[:2]

    url = f"http://{_browser_host_for(host)}:{bound_port}/"
    print(
        " ".join(
            [
                f"Serving ticket UI at {url}",
                f"(listening on {bound_host}:{bound_port})",
                f"tickets_dir={_format_tickets_dir_for_log(tickets_dir)}",
            ]
        )
    )

    if open_browser:
        _open_browser_later(url, delay_s=0.25)

    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


# -----------------------------
# CLI
# -----------------------------


def parse_args(argv: Optional[List[str]]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="ticket_ui",
        description="Start the readonly tickets web UI and open a browser tab.",
    )
    p.add_argument("--host", default="127.0.0.1", help="Listen address")
    p.add_argument(
        "--port",
        type=int,
        default=None,
        help="Listen port (default: try 8765, then random free port)",
    )
    p.add_argument(
        "--tickets-dir",
        default="",
        help="Path to .tickets directory (default: $TICKET_DIR or auto-detect)",
    )
    p.add_argument(
        "--no-open",
        action="store_true",
        help="Do not auto-open a browser tab",
    )
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    tickets_dir: Optional[Path]
    if getattr(args, "tickets_dir", ""):
        tickets_dir = Path(args.tickets_dir).expanduser().resolve()
    elif os.environ.get("TICKET_DIR"):
        tickets_dir = Path(os.environ["TICKET_DIR"]).expanduser().resolve()
    else:
        tickets_dir = find_tickets_dir(Path.cwd())

    run_web(
        host=str(args.host),
        port=(int(args.port) if args.port is not None else None),
        tickets_dir=tickets_dir,
        open_browser=(not bool(args.no_open)),
    )


if __name__ == "__main__":
    main()
