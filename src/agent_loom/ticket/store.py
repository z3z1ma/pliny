from __future__ import annotations

import contextlib
import datetime as dt
import hashlib
import json
import os
import socket
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Mapping, NoReturn, Optional, Sequence, Tuple

import yaml

from agent_loom.core.paths import safe_relpath
from agent_loom.core.time import isoformat_z, parse_iso, utcnow
from agent_loom.ticket.constants import (
    AUDIT_DIRNAME,
    CACHE_DIRNAME,
    CONFIG_FILENAME,
    LOCKS_DIRNAME,
    VALID_STATUSES,
)
from agent_loom.ticket.frontmatter import (
    dump_frontmatter,
    normalize_list_value,
    split_frontmatter,
)
from agent_loom.ticket.models import Ticket, TicketConfig
from agent_loom.ticket.normalize import (
    normalize_priority,
    normalize_status,
    normalize_ticket_ref,
    normalize_type,
)
from agent_loom.ticket.errors import TicketArgError, TicketNotFoundError


def sha256_hex(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8", errors="replace")).hexdigest()


class LockError(RuntimeError):
    pass


class FileLeaseLock:
    def __init__(
        self,
        lock_path: Path,
        *,
        owner: str,
        stale_after: dt.timedelta = dt.timedelta(minutes=15),
    ):
        self.lock_path = lock_path
        self.owner = owner
        self.stale_after = stale_after
        self._acquired = False

    def acquire(
        self, *, wait: bool = False, timeout: dt.timedelta = dt.timedelta(seconds=10)
    ) -> None:
        deadline = utcnow() + timeout
        while True:
            try:
                self.lock_path.parent.mkdir(parents=True, exist_ok=True)
                fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                try:
                    payload = {
                        "owner": self.owner,
                        "created": isoformat_z(utcnow()),
                        "pid": os.getpid(),
                        "host": socket.gethostname(),
                        "nonce": uuid.uuid4().hex,
                    }
                    os.write(fd, json.dumps(payload, sort_keys=True).encode("utf-8"))
                finally:
                    os.close(fd)
                self._acquired = True
                return
            except FileExistsError:
                if self._is_stale():
                    try:
                        self.lock_path.unlink()
                        continue
                    except Exception:
                        pass
                if not wait or utcnow() >= deadline:
                    raise LockError(f"Lock busy: {self.lock_path}")
                time.sleep(0.1)

    def _is_stale(self) -> bool:
        try:
            s = self.lock_path.read_text(encoding="utf-8")
            data = json.loads(s)
            created = parse_iso(str(data.get("created", "")))
            if not created:
                return True
            return (utcnow() - created) > self.stale_after
        except Exception:
            return True

    def release(self) -> None:
        if not self._acquired:
            return
        try:
            self.lock_path.unlink()
        finally:
            self._acquired = False

    def __enter__(self) -> "FileLeaseLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()


class AuditLogger:
    def __init__(
        self,
        *,
        tickets_dir: Path,
        run_id: str,
        agent_id: str,
        cwd: Path,
        repo_root: Optional[Path],
        argv: Sequence[str],
        audit_mode: str = "all",
        json_mode: bool = False,
    ):
        self.tickets_dir = tickets_dir
        self.audit_dir = tickets_dir / AUDIT_DIRNAME
        self.lock_path = (tickets_dir / LOCKS_DIRNAME) / "audit.lock"
        self.run_id = run_id
        self.agent_id = agent_id
        self.cwd = cwd
        self.repo_root = repo_root
        self.argv = list(argv)
        self.audit_mode = audit_mode
        self.json_mode = json_mode

    def _events_path(self) -> Path:
        day = utcnow().strftime("%Y-%m-%d")
        return self.audit_dir / f"audit-{day}.jsonl"

    def log(self, event: Mapping[str, Any]) -> None:
        if self.audit_mode == "off":
            return
        if os.getenv("TK_AUDIT", "1") == "0":
            return

        payload: Dict[str, Any] = {
            "v": 1,
            "ts": isoformat_z(utcnow()),
            "run_id": self.run_id,
            "agent": self.agent_id,
            "pid": os.getpid(),
            "host": socket.gethostname(),
            "cwd": str(self.cwd),
            "repo_root": str(self.repo_root) if self.repo_root else "",
            "tickets_dir": str(self.tickets_dir),
            "json": bool(self.json_mode),
            "argv_flags": [a for a in self.argv if a.startswith("-")],
            "argv_sha256": sha256_hex("\n".join(self.argv)),
        }
        payload.update(dict(event))

        try:
            self.audit_dir.mkdir(parents=True, exist_ok=True)
            # Best-effort: keep audit logs private by default.
            with contextlib.suppress(Exception):
                os.chmod(str(self.audit_dir), 0o700)

            with FileLeaseLock(self.lock_path, owner=f"audit:{self.agent_id}"):
                line = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
                with open(self._events_path(), "a", encoding="utf-8") as f:
                    f.write(line)
        except Exception:
            # Logging must never break ticket operations.
            return


def normalize_ticket_frontmatter(raw: Mapping[str, Any]) -> Dict[str, Any]:
    fm = dict(raw or {})

    tid = str(fm.get("id") or "").strip()
    if not tid:
        raise TicketArgError(
            code="ARG",
            error="Ticket frontmatter missing required key: 'id'",
            hint="Add `id: <filename-stem>` to the YAML frontmatter.",
        )
    fm["id"] = tid

    status_raw = fm.get("status") or "open"
    status = normalize_status(status_raw)
    if status not in VALID_STATUSES:
        raise TicketArgError(
            code="ARG",
            error=f"Invalid status {str(status_raw).strip()!r}. Must be one of: {', '.join(VALID_STATUSES)}",
            hint="Fix the ticket YAML frontmatter status (or run `loom ticket status <id> <status>`).",
        )
    fm["status"] = status

    prio_raw = fm.get("priority")
    fm["priority"] = normalize_priority(prio_raw if prio_raw is not None else 2)

    type_raw = fm.get("type")
    fm["type"] = normalize_type(type_raw) or "task"
    fm.setdefault("created", "")
    fm.setdefault("assignee", "")
    fm.setdefault("external_ref", "")
    fm.setdefault("parent", "")

    for k in ("deps", "links", "tags"):
        fm[k] = normalize_list_value(fm.get(k))

    for k in (
        "claimed_by",
        "claimed_at",
        "claim_expires",
        "claim_ttl",
        "heartbeat",
        "last_sync",
    ):
        v = fm.get(k)
        fm[k] = "" if v is None else str(v)

    ext = fm.get("external")
    if ext is None:
        fm["external"] = {}
    elif isinstance(ext, dict):
        fm["external"] = ext
    else:
        fm["external"] = {"value": ext}

    return fm


class TicketStore:
    def __init__(self, tickets_dir: Path, *, audit: Optional[AuditLogger] = None):
        self.tickets_dir = tickets_dir
        self.locks_dir = tickets_dir / LOCKS_DIRNAME
        self.cache_dir = tickets_dir / CACHE_DIRNAME
        self.leases_dir = self.locks_dir / "leases"
        self.config_path = tickets_dir / CONFIG_FILENAME
        self.audit = audit

    def ensure(self) -> None:
        self.tickets_dir.mkdir(parents=True, exist_ok=True)
        self.locks_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.leases_dir.mkdir(parents=True, exist_ok=True)
        (self.tickets_dir / AUDIT_DIRNAME).mkdir(parents=True, exist_ok=True)

    def lease_path(self, ticket_id: str) -> Path:
        return self.leases_dir / f"{ticket_id}.json"

    def read_lease(self, ticket_id: str) -> Dict[str, Any]:
        p = self.lease_path(ticket_id)
        if not p.exists():
            return {}
        try:
            data = json.loads(p.read_text(encoding="utf-8") or "{}")
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def write_lease(self, ticket_id: str, data: Mapping[str, Any]) -> None:
        before = self.read_lease(ticket_id)
        p = self.lease_path(ticket_id)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(dict(data), sort_keys=True) + "\n", encoding="utf-8")
        tmp.replace(p)

        if self.audit is not None and self.audit.audit_mode != "off":
            changed = sorted(
                {
                    k
                    for k in set(before.keys()) | set(dict(data).keys())
                    if before.get(k) != dict(data).get(k)
                }
            )
            self.audit.log(
                {
                    "event": "lease_write",
                    "ticket_id": ticket_id,
                    "changed": changed,
                    "claimed_by": str(dict(data).get("claimed_by") or ""),
                    "claim_expires": str(dict(data).get("claim_expires") or ""),
                    "heartbeat": str(dict(data).get("heartbeat") or ""),
                }
            )

    def remove_lease(self, ticket_id: str) -> None:
        p = self.lease_path(ticket_id)
        try:
            p.unlink()
        except FileNotFoundError:
            return

        if self.audit is not None and self.audit.audit_mode != "off":
            self.audit.log({"event": "lease_remove", "ticket_id": ticket_id})

    def load_config(self) -> TicketConfig:
        if not self.config_path.exists():
            return TicketConfig()
        try:
            raw = yaml.safe_load(self.config_path.read_text(encoding="utf-8")) or {}
        except Exception:
            raw = {}

        github = (
            raw.get("github", {}) if isinstance(raw.get("github", {}), dict) else {}
        )
        jira = raw.get("jira", {}) if isinstance(raw.get("jira", {}), dict) else {}

        return TicketConfig(
            prefix=str(raw.get("prefix") or ""),
            github_default_repo=str(
                raw.get("github_default_repo") or github.get("default_repo") or ""
            ),
            jira_base_url=str(raw.get("jira_base_url") or jira.get("base_url") or ""),
            extra={
                k: v
                for k, v in (raw or {}).items()
                if k
                not in {
                    "prefix",
                    "github",
                    "jira",
                    "github_default_repo",
                    "jira_base_url",
                }
            },
        )

    def ticket_path(self, ticket_id: str) -> Path:
        return self.tickets_dir / f"{ticket_id}.md"

    def resolve_id(self, pattern: str) -> str:
        raw = (pattern or "").strip()
        if not raw:
            raise TicketArgError(
                code="ARG",
                error="Ticket id is required",
                hint="Example: `loom ticket show <id>` or `loom ticket list`.",
            )

        norm = normalize_ticket_ref(raw, tickets_dir=self.tickets_dir)
        if not norm:
            raise TicketArgError(
                code="ARG",
                error=f"Invalid ticket reference {raw!r}",
                hint="Use an id like `ab-1234`, `#ab-1234`, or a path like `.tickets/ab-1234.md`.",
            )
        exact = self.ticket_path(norm)
        if exact.exists():
            return norm

        if not self.tickets_dir.exists() or not self.tickets_dir.is_dir():
            raise TicketNotFoundError(
                code="NOT_FOUND",
                error=f"Tickets directory not found: {self.tickets_dir}",
                hint="Run `loom ticket init` (or `loom ticket create`) to create `.tickets/`, or set TICKET_DIR.",
                suggestions=["loom ticket init", "loom ticket create 'Title'"],
                details={"tickets_dir": str(self.tickets_dir)},
            )

        paths = list(self.tickets_dir.glob("*.md"))

        prefix_matches = [p for p in paths if p.stem.startswith(norm)]
        if len(prefix_matches) == 1:
            return prefix_matches[0].stem
        if len(prefix_matches) > 1:
            ids = sorted([p.stem for p in prefix_matches])
            show = ids[:10]
            more = max(0, len(ids) - len(show))
            self._raise_ambiguous(norm, show, more)

        contains_matches = [p for p in paths if norm in p.stem]
        if len(contains_matches) == 1:
            return contains_matches[0].stem
        if len(contains_matches) > 1:
            ids = sorted([p.stem for p in contains_matches])
            show = ids[:10]
            more = max(0, len(ids) - len(show))
            self._raise_ambiguous(norm, show, more)

        raise TicketNotFoundError(
            code="NOT_FOUND",
            error=f"Ticket {norm!r} not found",
            hint="Run `loom ticket list` to see ids. Refs like `#id`, `id.md`, and `.tickets/id.md` are accepted.",
        )

    def _raise_ambiguous(self, norm: str, matches: list[str], more: int) -> NoReturn:
        tail = f" (+{more} more)" if more else ""
        raise TicketArgError(
            code="ARG",
            error=f"Ambiguous id {norm!r} matches multiple tickets",
            hint=f"Use a full id. Matches: {', '.join(matches)}{tail}",
            details={"matches": matches, "more": more, "pattern": norm},
            suggestions=["loom ticket list", "loom ticket show <full-id>"],
        )

    def iter_paths(self):
        if not self.tickets_dir.exists():
            return iter(())
        return iter(sorted(self.tickets_dir.glob("*.md")))

    def load_ticket_by_id(self, ticket_id: str) -> Ticket:
        p = self.ticket_path(ticket_id)
        if not p.exists():
            raise TicketNotFoundError(
                code="NOT_FOUND",
                error=f"Ticket {ticket_id!r} not found",
                hint="Run `loom ticket list` to see ids.",
            )
        text = p.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        if not fm.get("id"):
            fm["id"] = ticket_id
        fm = normalize_ticket_frontmatter(fm)
        return Ticket(path=p, fm=fm, body=body)

    def load_ticket(self, pattern: str) -> Ticket:
        tid = self.resolve_id(pattern)
        return self.load_ticket_by_id(tid)

    def save_ticket(self, t: Ticket) -> None:
        before_text = ""
        before_fm: Dict[str, Any] = {}
        before_body = ""
        if t.path.exists():
            try:
                before_text = t.path.read_text(encoding="utf-8")
                before_fm, before_body = split_frontmatter(before_text)
                with contextlib.suppress(Exception):
                    before_fm = normalize_ticket_frontmatter(before_fm)
            except Exception:
                before_text = ""
                before_fm = {}
                before_body = ""

        t.fm = normalize_ticket_frontmatter(t.fm)
        out = dump_frontmatter(t.fm) + t.body.lstrip("\n")

        audit_event: Optional[Dict[str, Any]] = None
        if self.audit is not None and self.audit.audit_mode != "off":
            changed_keys = sorted(
                {
                    k
                    for k in set(before_fm.keys()) | set(t.fm.keys())
                    if before_fm.get(k) != t.fm.get(k)
                }
            )
            audit_event = {
                "event": "ticket_write",
                "ticket_id": t.id,
                "path": safe_relpath(t.path, self.tickets_dir),
                "before_sha256": sha256_hex(before_text),
                "after_sha256": sha256_hex(out),
                "changed_keys": changed_keys,
                "status": str(t.fm.get("status") or ""),
                "priority": int(t.fm.get("priority") or 0),
                "type": str(t.fm.get("type") or ""),
                "assignee": str(t.fm.get("assignee") or ""),
                "tags": [str(x) for x in (t.fm.get("tags") or [])],
                "deps": [str(x) for x in (t.fm.get("deps") or [])],
                "links": [str(x) for x in (t.fm.get("links") or [])],
                "parent": str(t.fm.get("parent") or ""),
                "external_ref": str(t.fm.get("external_ref") or ""),
                "body_sha256_before": sha256_hex(before_body),
                "body_sha256_after": sha256_hex(t.body),
                "body_bytes_before": len(before_body.encode("utf-8", errors="replace")),
                "body_bytes_after": len(t.body.encode("utf-8", errors="replace")),
            }

        tmp = t.path.with_suffix(".md.tmp")
        tmp.write_text(out, encoding="utf-8")
        tmp.replace(t.path)

        if (
            audit_event is not None
            and self.audit is not None
            and self.audit.audit_mode != "off"
        ):
            self.audit.log(audit_event)

    def lock_for_ticket(self, ticket_id: str, owner: str) -> FileLeaseLock:
        return FileLeaseLock(self.locks_dir / f"{ticket_id}.lock", owner=owner)


def claim_state(
    fm: Mapping[str, Any],
    *,
    lease: Optional[Mapping[str, Any]] = None,
) -> Tuple[str, Optional[dt.datetime], Optional[dt.datetime]]:
    src: Mapping[str, Any] = lease if lease is not None and len(lease) > 0 else fm
    who = str(src.get("claimed_by") or src.get("claimed-by") or "")
    exp = parse_iso(str(src.get("claim_expires") or src.get("claim-expires") or ""))
    hb = parse_iso(str(src.get("heartbeat") or ""))
    return who, exp, hb


def effective_lease(
    store: TicketStore, ticket_id: str, fm: Mapping[str, Any]
) -> Dict[str, Any]:
    """Return runtime lease if present; else fall back to frontmatter claim fields."""

    lease = store.read_lease(ticket_id)
    if lease:
        return lease

    who, exp, hb = claim_state(fm)
    if not who and exp is None and hb is None:
        return {}
    out: Dict[str, Any] = {}
    if who:
        out["claimed_by"] = who
    if exp is not None:
        out["claim_expires"] = isoformat_z(exp)
    if hb is not None:
        out["heartbeat"] = isoformat_z(hb)
    ttl = str(fm.get("claim_ttl") or fm.get("claim-ttl") or "")
    if ttl:
        out["claim_ttl"] = ttl
    claimed_at = str(fm.get("claimed_at") or fm.get("claimed-at") or "")
    if claimed_at:
        out["claimed_at"] = claimed_at
    return out


def active_claimed_by(
    fm: Mapping[str, Any], *, lease: Optional[Mapping[str, Any]] = None
) -> str:
    who, exp, _hb = claim_state(fm, lease=lease)
    if not who:
        return ""
    if exp is None:
        return who
    return who if utcnow() < exp else ""


def write_guard(
    store: TicketStore, t: Ticket, agent_id: str, force: bool = False
) -> None:
    lease = effective_lease(store, t.id, t.fm)
    who, exp, hb = claim_state(t.fm, lease=lease)
    active = bool(who) and (exp is None or utcnow() < exp)

    require = os.getenv("TK_REQUIRE_CLAIM", "0") == "1"

    if active and who and who != agent_id and not force:
        exp_s = isoformat_z(exp) if exp else "(no expiry)"
        hb_s = isoformat_z(hb) if hb else "(no heartbeat)"
        if store.audit is not None and store.audit.audit_mode != "off":
            store.audit.log(
                {
                    "event": "policy_denied",
                    "ticket_id": t.id,
                    "reason": "claimed_by_other",
                    "claimed_by": who,
                    "claim_expires": exp_s,
                    "heartbeat": hb_s,
                    "force": bool(force),
                }
            )
        raise PermissionError(
            f"Ticket is claimed by {who} (expires {exp_s}, heartbeat {hb_s}). Use --force to override."
        )

    if require and (not who or who != agent_id) and not force:
        if store.audit is not None and store.audit.audit_mode != "off":
            store.audit.log(
                {
                    "event": "policy_denied",
                    "ticket_id": t.id,
                    "reason": "require_claim",
                    "claimed_by": who,
                    "force": bool(force),
                }
            )
        raise PermissionError(
            "Writes require an active claim by this agent (TK_REQUIRE_CLAIM=1). "
            "Run 'loom ticket claim <id>' or use --force."
        )


__all__ = [
    "AUDIT_DIRNAME",
    "CACHE_DIRNAME",
    "CONFIG_FILENAME",
    "LOCKS_DIRNAME",
    "VALID_STATUSES",
    "AuditLogger",
    "FileLeaseLock",
    "LockError",
    "TicketStore",
    "active_claimed_by",
    "claim_state",
    "effective_lease",
    "normalize_ticket_frontmatter",
    "write_guard",
]
