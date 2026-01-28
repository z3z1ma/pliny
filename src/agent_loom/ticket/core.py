"""ticket - a minimal, file-backed ticket system for human+agent workflows.

Design goals
 - Ticket library + CLI (loom)
- State stored as Markdown with YAML frontmatter in `.tickets/`
- Agent-friendly graph primitives: deps, links, parent/child
- Safe-ish concurrency: per-ticket lease locks + optional claim enforcement
- Optional external sync (GitHub built-in)

Canonical usage
  ticket init
  ticket create "Implement orchestration layer" -p 1 -t epic --tags ai,infra
  ticket list
  ticket ready
  ticket show <id>
  ticket update <id> --status in_progress
  ticket dep <id>
  ticket dep-add <id> <dep-id>
  ticket claim <id> --ttl 45m

Machine usage
  ticket --json list
  ticket --json show <id>

Environment
  TICKET_DIR            Explicit tickets directory (overrides search)
  TICKET_AGENT          Agent identifier for claims (defaults to user@host:pid)
  GITHUB_TOKEN          Optional GitHub token for sync
  TK_GITHUB_REPO        Default repo (owner/repo) for gh-123 shorthand
  TK_REQUIRE_CLAIM=1    Require tickets to be claimed by current agent for writes
"""

from __future__ import annotations

import datetime as dt
import hashlib
import os
import re
import socket
import time
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
)

import jmespath
import yaml

from agent_loom.core.git import git_checked, git_quiet, git_repo_root, git_scoped_commit
from agent_loom.core.paths import safe_relpath
from agent_loom.core.time import isoformat_z, parse_duration, utcnow
from agent_loom.ticket.adapters import (
    ExternalAdapter,
    GitHubIssueAdapter,
    JiraIssueAdapter,
)
from agent_loom.ticket.constants import (
    AUDIT_DIRNAME,
    AUDIT_LOGGER,
    AUDIT_MODE,
    CACHE_DIRNAME,
    CONFIG_FILENAME,
    LOCKS_DIRNAME,
    SUBSYSTEM_NAME,
    SUBSYSTEM_VERSION,
    TICKET_DIR_OVERRIDE,
    TICKET_DIRNAME,
    VALID_STATUSES,
)
from agent_loom.ticket.frontmatter import decanonicalize_frontmatter
from agent_loom.ticket.graph import (
    blockers_for,
    build_index,
    closure_from,
    compute_health,
    has_cycle,
    is_ready,
    predecessors,
    simple_cycles,
)
from agent_loom.ticket.models import (
    GitStatusEntry,
    Ticket,
    TicketAddNoteResult,
    TicketClaimResult,
    TicketCreateResult,
    TicketCyclesResult,
    TicketDependencyResult,
    TicketDepResult,
    TicketDetails,
    TicketGraph,
    TicketGraphEdge,
    TicketHealth,
    TicketHeartbeatResult,
    TicketInitResult,
    TicketLinkManyResult,
    TicketLinkResult,
    TicketListResult,
    TicketPrimeResult,
    TicketQueryResult,
    TicketRelationships,
    TicketReleaseResult,
    TicketShowResult,
    TicketStatusResult,
    TicketSummary,
    TicketSwarmAgent,
    TicketSwarmResult,
    TicketSyncExternalItem,
    TicketSyncExternalResult,
    TicketSyncResult,
    TicketUpdateResult,
    TicketVersionResult,
    TicketViewResult,
)
from agent_loom.ticket.store import (
    TicketStore,
    active_claimed_by,
    claim_state,
    effective_lease,
    write_guard,
)
from agent_loom.ticket.normalize import normalize_status
from agent_loom.ticket.errors import TicketArgError, TicketNotFoundError

JSON_MODE = False

# External adapter singleton instances
_ADAPTERS: List[ExternalAdapter] = [GitHubIssueAdapter(), JiraIssueAdapter()]

__all__ = [
    "add_note",
    "blocked",
    "claim",
    "close",
    "closed",
    "create",
    "create_in_dir",
    "dep",
    "dep_add",
    "dep_cycle",
    "dep_rm",
    "heartbeat",
    "init",
    "link",
    "list_tickets",
    "prime",
    "query",
    "ready",
    "release",
    "reopen",
    "show",
    "start",
    "status",
    "swarm",
    "sync",
    "sync_external",
    "unlink",
    "update",
    "version",
    "view",
]


def short_hash(text: str, n: int = 4) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:n]


def sha256_hex(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8", errors="replace")).hexdigest()


def dirname_prefix(path: Path) -> str:
    name = path.name
    parts = re.split(r"[-_]+", name)
    prefix = "".join(p[:1] for p in parts if p)
    if len(prefix) < 2:
        prefix = name[:3] if len(name) >= 3 else (name + "xxx")[:3]
    return prefix


def generate_ticket_id(*, prefix: str) -> str:
    entropy = f"{os.getpid()}:{time.time_ns()}:{os.urandom(8).hex()}"
    return f"{prefix}-{short_hash(entropy, 4)}"


def _git_status_entries(
    repo_root: Path, *, pathspecs: Optional[Sequence[str]] = None
) -> List[GitStatusEntry]:
    argv = ["status", "--porcelain=v1", "-z"]
    if pathspecs:
        argv += ["--", *list(pathspecs)]
    raw = git_checked(repo_root, argv)
    if not raw:
        return []

    parts = raw.split("\0")
    i = 0
    out: List[GitStatusEntry] = []
    while i < len(parts):
        tok = parts[i]
        i += 1
        if not tok:
            continue
        if len(tok) < 4 or tok[2] != " ":
            continue
        xy = tok[:2]
        path = tok[3:]
        path2 = ""
        if "R" in xy or "C" in xy:
            if i < len(parts):
                path2 = parts[i]
                i += 1
        out.append(GitStatusEntry(xy=xy, path=path, path2=path2))
    return out


def default_assignee() -> str:
    base = git_repo_root(Path.cwd()) or Path.cwd()
    return git_quiet(base, ["config", "user.name"])


def default_agent_id() -> str:
    v = os.getenv("TICKET_AGENT")
    if v:
        return v
    user = os.getenv("USER") or os.getenv("USERNAME") or "unknown"
    host = socket.gethostname() or "host"
    return f"{user}@{host}:{os.getpid()}"


def find_tickets_dir(cmd: str, cwd: Path) -> Path:
    env = TICKET_DIR_OVERRIDE or os.getenv("TICKET_DIR")
    if env:
        p = Path(env).expanduser()
        if p.is_absolute():
            return p.resolve()
        base = git_repo_root(cwd) or cwd
        return (base / p).resolve()

    repo_root = git_repo_root(cwd)
    if repo_root is not None:
        cand = (repo_root / TICKET_DIRNAME).resolve()
        if cand.is_dir():
            return cand
        if cmd in {"init", "create"}:
            return cand
        raise FileNotFoundError(
            f"No {TICKET_DIRNAME} directory found at git root {repo_root}. "
            "Run 'loom ticket init' or 'loom ticket create' to initialize, or set TICKET_DIR."
        )

    d = cwd.resolve()
    while True:
        cand = d / TICKET_DIRNAME
        if cand.is_dir():
            return cand
        if d.parent == d:
            break
        d = d.parent

    if cmd in {"init", "create"}:
        return (cwd / TICKET_DIRNAME).resolve()

    raise FileNotFoundError(
        "No .tickets directory found (searched parent directories). "
        "Run 'loom ticket init' or 'loom ticket create' to initialize, or set TICKET_DIR."
    )


def store_for_cmd(cmd: str) -> TicketStore:
    tickets_dir = find_tickets_dir(cmd, Path.cwd())
    audit = (
        AUDIT_LOGGER
        if AUDIT_LOGGER is not None and AUDIT_LOGGER.tickets_dir == tickets_dir
        else None
    )
    return TicketStore(tickets_dir, audit=audit)


def require_status(s: str) -> str:
    s0 = normalize_status(s)
    if s0 not in VALID_STATUSES:
        raise TicketArgError(
            code="ARG",
            error=f"Invalid status {str(s).strip()!r}. Must be one of: {', '.join(VALID_STATUSES)}",
            hint="Aliases: todo/new->open, wip/doing/started->in_progress, done/completed->closed.",
            suggestions=[
                "loom ticket status <id> open",
                "loom ticket status <id> in_progress",
                "loom ticket status <id> closed",
            ],
        )
    return s0


def _summary_for_ticket(
    store: TicketStore,
    t: Ticket,
    *,
    deps: Optional[List[str]] = None,
    blockers: Optional[List[str]] = None,
    mtime: str = "",
) -> TicketSummary:
    lease = effective_lease(store, t.id, t.fm)
    claimed_by = active_claimed_by(t.fm, lease=lease)
    return TicketSummary(
        id=t.id,
        title=t.title,
        status=t.status,
        priority=t.priority,
        assignee=str(t.fm.get("assignee") or ""),
        tags=[str(x) for x in (t.fm.get("tags") or [])],
        claimed_by=claimed_by,
        deps=deps or [],
        blockers=blockers or [],
        mtime=mtime,
    )


def _details_for_ticket(store: TicketStore, t: Ticket) -> TicketDetails:
    lease = effective_lease(store, t.id, t.fm)
    claimed_by = active_claimed_by(t.fm, lease=lease)
    return TicketDetails(
        id=t.id,
        title=t.title,
        status=t.status,
        priority=t.priority,
        type=str(t.fm.get("type") or ""),
        assignee=str(t.fm.get("assignee") or ""),
        tags=[str(x) for x in (t.fm.get("tags") or [])],
        deps=[str(x) for x in (t.fm.get("deps") or [])],
        links=[str(x) for x in (t.fm.get("links") or [])],
        external_ref=str(t.fm.get("external_ref") or ""),
        parent=str(t.fm.get("parent") or ""),
        claimed_by=claimed_by,
    )


def _health_from_mapping(health: Mapping[str, Any]) -> TicketHealth:
    return TicketHealth(
        counts=dict(health.get("counts") or {}),
        ready=int(health.get("ready") or 0),
        blocked=int(health.get("blocked") or 0),
        bottlenecks=list(health.get("bottlenecks") or []),
    )


def _graph_edges(edges: List[Tuple[str, str, str]]) -> List[TicketGraphEdge]:
    return [TicketGraphEdge(src=a, dst=b, kind=k) for a, b, k in edges]


def pick_adapter(external_ref: str) -> Optional[ExternalAdapter]:
    for a in _ADAPTERS:
        try:
            if a.can_handle(external_ref):
                return a
        except Exception:
            continue
    return None


# -----------------------------
# Commands
# -----------------------------


def version() -> TicketVersionResult:
    return TicketVersionResult(name=SUBSYSTEM_NAME, version=SUBSYSTEM_VERSION)


def init() -> TicketInitResult:
    store = store_for_cmd("init")
    store.ensure()
    return TicketInitResult(initialized=str(store.tickets_dir))


def _ensure_prefix(store: TicketStore, *, cwd: Path) -> str:
    store.ensure()
    cfg = store.load_config()
    if cfg.prefix:
        return cfg.prefix

    prefix = dirname_prefix(cwd)

    raw: Dict[str, Any] = {}
    if store.config_path.exists():
        try:
            raw = yaml.safe_load(store.config_path.read_text(encoding="utf-8")) or {}
        except Exception:
            raw = {}

    raw = dict(raw) if isinstance(raw, dict) else {}
    raw["prefix"] = prefix
    store.config_path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")

    return prefix


def create(
    *,
    title: str,
    type: str,
    priority: int,
    tags: Optional[str] = None,
    include_sprint_tag: bool = True,
    assignee: Optional[str] = None,
    external_ref: Optional[str] = None,
    parent: Optional[str] = None,
    description: Optional[str] = None,
    design: Optional[str] = None,
    acceptance: Optional[str] = None,
) -> TicketCreateResult:
    store = store_for_cmd("create")
    return create_in_dir(
        tickets_dir=store.tickets_dir,
        title=title,
        type=type,
        priority=priority,
        tags=tags,
        include_sprint_tag=include_sprint_tag,
        assignee=assignee,
        external_ref=external_ref,
        parent=parent,
        description=description,
        design=design,
        acceptance=acceptance,
    )


def create_in_dir(
    *,
    tickets_dir: Path,
    title: str,
    type: str,
    priority: int,
    tags: Optional[str] = None,
    include_sprint_tag: bool = True,
    assignee: Optional[str] = None,
    external_ref: Optional[str] = None,
    parent: Optional[str] = None,
    description: Optional[str] = None,
    design: Optional[str] = None,
    acceptance: Optional[str] = None,
) -> TicketCreateResult:
    store = TicketStore(Path(tickets_dir).resolve())
    prefix = _ensure_prefix(store, cwd=store.tickets_dir.parent)

    assignee = assignee or default_assignee()

    parent_id = ""
    if parent:
        parent_id = store.resolve_id(parent)

    tid = generate_ticket_id(prefix=prefix)
    now = isoformat_z(utcnow())

    fm: Dict[str, Any] = {
        "id": tid,
        "status": "open",
        "deps": [],
        "links": [],
        "created": now,
        "type": type,
        "priority": int(priority),
    }
    if assignee:
        fm["assignee"] = assignee
    if external_ref:
        fm["external_ref"] = external_ref
    if parent_id:
        fm["parent"] = parent_id

    sprint_tag = str(os.getenv("TEAM_SPRINT_TAG") or "").strip()
    tags_list = [t.strip() for t in (tags or "").split(",") if t.strip()]
    if include_sprint_tag and sprint_tag and sprint_tag not in tags_list:
        tags_list = [sprint_tag, *tags_list]
    if tags_list:
        # Keep order stable (sprint tag first when present).
        seen: set[str] = set()
        deduped: list[str] = []
        for t in tags_list:
            if t not in seen:
                seen.add(t)
                deduped.append(t)
        fm["tags"] = deduped

    body_lines = [f"# {title}", ""]
    if description:
        body_lines += [description, ""]
    if design:
        body_lines += ["## Design", "", design, ""]
    if acceptance:
        body_lines += ["## Acceptance Criteria", "", acceptance, ""]

    path = store.ticket_path(tid)
    t = Ticket(path=path, fm=fm, body="\n".join(body_lines).rstrip() + "\n")
    store.save_ticket(t)

    return TicketCreateResult(id=tid, path=safe_relpath(path, store.tickets_dir))


def status(*, ticket: str, new_status: str, force: bool = False) -> TicketStatusResult:
    store = store_for_cmd("status")
    agent = default_agent_id()

    t = store.load_ticket(ticket)
    write_guard(store, t, agent, force=bool(force))

    new_status = require_status(new_status)
    with store.lock_for_ticket(t.id, agent):
        t.fm["status"] = new_status
        store.save_ticket(t)

    return TicketStatusResult(id=t.id, status=new_status)


def start(*, ticket: str, force: bool = False) -> TicketStatusResult:
    return status(ticket=ticket, new_status="in_progress", force=force)


def close(*, ticket: str, force: bool = False) -> TicketStatusResult:
    return status(ticket=ticket, new_status="closed", force=force)


def reopen(*, ticket: str, force: bool = False) -> TicketStatusResult:
    return status(ticket=ticket, new_status="open", force=force)


def list_tickets(
    *,
    status: str = "",
    type: str = "",
    priority: Optional[int] = None,
    prio_min: Optional[int] = None,
    prio_max: Optional[int] = None,
    assignee: str = "",
    tag: str = "",
    include_closed: bool = False,
    limit: int = 0,
) -> TicketListResult:
    store = store_for_cmd("list")
    idx = build_index(store)

    limit = int(limit)
    if limit < 0:
        raise TicketArgError(
            code="ARG",
            error="--limit must be >= 0",
            hint="Use --limit 0 for unlimited, or a positive integer.",
            suggestions=["loom ticket list --limit 50"],
            details={"limit": limit},
        )

    status_filter = require_status(status) if status else ""

    if priority is not None:
        prio_min = priority
        prio_max = priority

    type_filter = (type or "").strip()

    def match(t: Ticket) -> bool:
        if not include_closed and t.status == "closed":
            return False
        if status_filter and t.status != status_filter:
            return False

        try:
            p = int(t.fm.get("priority") or t.priority)
        except Exception:
            p = t.priority

        if prio_min is not None and p < prio_min:
            return False
        if prio_max is not None and p > prio_max:
            return False

        if type_filter and str(t.fm.get("type") or "") != type_filter:
            return False

        if assignee and str(t.fm.get("assignee") or "") != assignee:
            return False
        if tag:
            tags = [str(x) for x in (t.fm.get("tags") or [])]
            if tag not in tags:
                return False
        return True

    tickets = [t for t in idx.tickets.values() if match(t)]
    tickets.sort(key=lambda t: (t.status == "closed", t.priority, t.id))

    if limit:
        tickets = tickets[:limit]

    rows = [
        _summary_for_ticket(
            store,
            t,
            deps=[str(x) for x in (t.fm.get("deps") or [])],
        )
        for t in tickets
    ]
    return TicketListResult(count=len(rows), tickets=rows)


def ready(
    *,
    type: str = "",
    priority: Optional[int] = None,
    prio_min: Optional[int] = None,
    prio_max: Optional[int] = None,
    assignee: str = "",
    tag: str = "",
) -> TicketListResult:
    store = store_for_cmd("ready")
    idx = build_index(store)

    if priority is not None:
        prio_min = priority
        prio_max = priority

    type_filter = (type or "").strip()

    out: List[Ticket] = []
    for tid, t in idx.tickets.items():
        if t.status not in {"open", "in_progress"}:
            continue

        try:
            p = int(t.fm.get("priority") or t.priority)
        except Exception:
            p = t.priority

        if prio_min is not None and p < prio_min:
            continue
        if prio_max is not None and p > prio_max:
            continue

        if type_filter and str(t.fm.get("type") or "") != type_filter:
            continue

        if assignee and str(t.fm.get("assignee") or "") != assignee:
            continue
        if tag:
            tags = [str(x) for x in (t.fm.get("tags") or [])]
            if tag not in tags:
                continue
        if is_ready(tid, idx):
            out.append(t)

    out.sort(key=lambda t: (t.priority, t.id))

    rows = [
        _summary_for_ticket(
            store,
            t,
            deps=[str(x) for x in (t.fm.get("deps") or [])],
        )
        for t in out
    ]
    return TicketListResult(count=len(rows), tickets=rows)


def blocked(*, assignee: str = "", tag: str = "") -> TicketListResult:
    store = store_for_cmd("blocked")
    idx = build_index(store)

    rows: List[Tuple[Ticket, List[str]]] = []
    for tid, t in idx.tickets.items():
        if t.status not in {"open", "in_progress"}:
            continue
        if assignee and str(t.fm.get("assignee") or "") != assignee:
            continue
        if tag:
            tags = [str(x) for x in (t.fm.get("tags") or [])]
            if tag not in tags:
                continue
        bl = blockers_for(tid, idx)
        if bl:
            rows.append((t, bl))

    rows.sort(key=lambda x: (x[0].priority, x[0].id))

    out_rows = [
        _summary_for_ticket(
            store,
            t,
            deps=[str(x) for x in (t.fm.get("deps") or [])],
            blockers=list(bl),
        )
        for t, bl in rows
    ]
    return TicketListResult(count=len(out_rows), tickets=out_rows)


def closed(*, limit: int = 20, assignee: str = "", tag: str = "") -> TicketListResult:
    store = store_for_cmd("closed")
    idx = build_index(store)

    def match(t: Ticket) -> bool:
        if t.status != "closed":
            return False
        if assignee and str(t.fm.get("assignee") or "") != assignee:
            return False
        if tag:
            tags = [str(x) for x in (t.fm.get("tags") or [])]
            if tag not in tags:
                return False
        return True

    tickets = [t for t in idx.tickets.values() if match(t)]
    tickets.sort(
        key=lambda t: t.path.stat().st_mtime if t.path.exists() else 0, reverse=True
    )
    tickets = tickets[: max(0, int(limit))]
    rows = []
    for t in tickets:
        mtime = dt.datetime.fromtimestamp(t.path.stat().st_mtime, tz=dt.timezone.utc)
        rows.append(
            _summary_for_ticket(
                store,
                t,
                deps=[str(x) for x in (t.fm.get("deps") or [])],
                mtime=isoformat_z(mtime),
            )
        )
    return TicketListResult(count=len(rows), tickets=rows)


def show(*, ticket: str) -> TicketShowResult:
    store = store_for_cmd("show")
    idx = build_index(store)
    t = store.load_ticket(ticket)

    lease = effective_lease(store, t.id, t.fm)

    blockers = blockers_for(t.id, idx)
    pred = predecessors(idx.deps)
    blocking = [
        x
        for x in pred.get(t.id, [])
        if (tx := idx.ticket(x)) is not None and tx.status != "closed"
    ]
    children = list(idx.parent.get(t.id, []))
    linked = list(idx.links.get(t.id, []))
    relationships = TicketRelationships(
        blockers=blockers,
        blocking=sorted(set(blocking)),
        children=sorted(set(children)),
        linked=sorted(set(linked)),
    )
    return TicketShowResult(
        ticket=_details_for_ticket(store, t),
        relationships=relationships,
        body=t.body,
        frontmatter=decanonicalize_frontmatter(t.fm),
        lease=dict(lease),
    )


def update(
    *,
    ticket: str,
    title: Optional[str] = None,
    status: str = "",
    priority: Optional[int] = None,
    type: str = "",
    assignee: str = "",
    tags: Optional[str] = None,
    external_ref: Optional[str] = None,
    body: Optional[str] = None,
    force: bool = False,
) -> TicketUpdateResult:
    store = store_for_cmd("update")
    agent = default_agent_id()

    t = store.load_ticket(ticket)
    write_guard(store, t, agent, force=bool(force))

    if status:
        t.fm["status"] = require_status(status)
    if priority is not None:
        t.fm["priority"] = int(priority)
    if type:
        t.fm["type"] = type
    if assignee:
        t.fm["assignee"] = assignee
    if tags is not None:
        t.fm["tags"] = [x.strip() for x in (tags or "").split(",") if x.strip()]
    if external_ref is not None:
        t.fm["external_ref"] = str(external_ref or "").strip()

    new_body = body

    with store.lock_for_ticket(t.id, agent):
        if new_body is not None:
            t.body = new_body if new_body.endswith("\n") else (new_body + "\n")
        if title:
            if re.search(r"(?m)^#\s+.*$", t.body):
                t.body = re.sub(r"(?m)^#\s+.*$", f"# {title}", t.body, count=1)
            else:
                t.body = f"# {title}\n\n" + t.body.lstrip("\n")
            t.body = t.body.rstrip() + "\n"

        store.save_ticket(t)

    return TicketUpdateResult(id=t.id)


def add_note(*, ticket: str, note: str, force: bool = False) -> TicketAddNoteResult:
    store = store_for_cmd("add-note")
    agent = default_agent_id()
    t = store.load_ticket(ticket)

    write_guard(store, t, agent, force=bool(force))

    if not note:
        raise TicketArgError(
            code="ARG",
            error="No note provided",
            hint="Pass a note arg or pipe stdin.",
            suggestions=[
                "loom ticket add-note <id> 'your note'",
                "echo 'your note' | loom ticket add-note <id>",
            ],
        )

    stamp = isoformat_z(utcnow())

    with store.lock_for_ticket(t.id, agent):
        body = t.body
        if "\n## Notes\n" not in body and not body.strip().endswith("## Notes"):
            body = body.rstrip() + "\n\n## Notes\n"
        t.body = body.rstrip() + f"\n\n**{stamp}**\n\n{note.strip()}\n"
        store.save_ticket(t)

    return TicketAddNoteResult(id=t.id, timestamp=stamp)


def dep(*, ticket: str) -> TicketDepResult:
    store = store_for_cmd("dep")
    idx = build_index(store)
    root = store.resolve_id(ticket)

    nodes, edges = closure_from(root, idx, include_children=False)
    health = compute_health(nodes, idx)
    dep_edges = [e for e in sorted(list(edges)) if e[2] == "dep"]
    return TicketDepResult(
        root=root,
        nodes=sorted(list(nodes)),
        edges=_graph_edges(dep_edges),
        health=_health_from_mapping(health),
    )


def dep_add(
    *, ticket: str, dependency: str, force: bool = False
) -> TicketDependencyResult:
    store = store_for_cmd("dep-add")
    agent = default_agent_id()

    t = store.load_ticket(ticket)
    write_guard(store, t, agent, force=bool(force))
    dep_id = store.resolve_id(dependency)

    if dep_id == t.id:
        raise TicketArgError(
            code="ARG",
            error="A ticket cannot depend on itself",
            hint=f"Both references resolved to {t.id}.",
        )

    idx = build_index(store)
    deps_map = {k: list(v) for k, v in idx.deps.items()}
    deps_map.setdefault(t.id, [])
    deps_map[t.id] = list(sorted(set(deps_map[t.id] + [dep_id])))
    if has_cycle(deps_map):
        raise TicketArgError(
            code="ARG",
            error=f"Dependency would create a cycle: {t.id} -> {dep_id}",
            hint="Inspect cycles with `loom ticket dep-cycle`.",
            suggestions=["loom ticket dep-cycle"],
        )

    deps = [str(x) for x in (t.fm.get("deps") or [])]
    if dep_id in deps:
        return TicketDependencyResult(id=t.id, dependency=dep_id, changed=False)

    deps.append(dep_id)
    t.fm["deps"] = sorted(set(deps))

    with store.lock_for_ticket(t.id, agent):
        store.save_ticket(t)

    return TicketDependencyResult(id=t.id, dependency=dep_id, changed=True)


def dep_rm(
    *, ticket: str, dependency: str, force: bool = False
) -> TicketDependencyResult:
    store = store_for_cmd("dep-rm")
    agent = default_agent_id()

    t = store.load_ticket(ticket)
    write_guard(store, t, agent, force=bool(force))
    dep_id = store.resolve_id(dependency)

    deps = [str(x) for x in (t.fm.get("deps") or [])]
    if dep_id not in deps:
        raise TicketNotFoundError(
            code="NOT_FOUND",
            error="Dependency not found",
            hint=f"{t.id} does not depend on {dep_id}.",
            details={"ticket": t.id, "dependency": dep_id},
            suggestions=["loom ticket show <id>", "loom ticket --json show <id>"],
        )

    t.fm["deps"] = [d for d in deps if d != dep_id]

    with store.lock_for_ticket(t.id, agent):
        store.save_ticket(t)

    return TicketDependencyResult(id=t.id, dependency=dep_id, changed=True)


def dep_cycle() -> TicketCyclesResult:
    store = store_for_cmd("dep-cycle")
    idx = build_index(store)

    deps_map: Dict[str, List[str]] = {}
    for a, ds in idx.deps.items():
        if (ta := idx.ticket(a)) is None or ta.status == "closed":
            continue
        deps_map[a] = [
            d for d in ds if (td := idx.ticket(d)) is None or td.status != "closed"
        ]

    cycles = simple_cycles(deps_map)

    return TicketCyclesResult(cycles=cycles)


def link(*, tickets: List[str], force: bool = False) -> TicketLinkManyResult:
    if len(tickets) < 2:
        raise TicketArgError(
            code="ARG",
            error="`loom ticket link` needs at least 2 ids",
            hint="Usage: loom ticket link <id> <id> [id...]",
            suggestions=[
                "loom ticket link <id> <id>",
                "loom ticket link <id> <id> <id>",
            ],
        )

    store = store_for_cmd("link")
    agent = default_agent_id()

    ids = [store.resolve_id(t) for t in tickets]
    loaded = [store.load_ticket_by_id(tid) for tid in ids]

    for t in loaded:
        write_guard(store, t, agent, force=bool(force))

    changed = 0
    for t in loaded:
        with store.lock_for_ticket(t.id, agent):
            links = [str(x) for x in (t.fm.get("links") or [])]
            before = set(links)
            for other in ids:
                if other != t.id:
                    before.add(other)
            t.fm["links"] = sorted(before)
            store.save_ticket(t)
            changed += max(0, len(before) - len(links))

    return TicketLinkManyResult(ids=ids, changed=int(changed))


def unlink(*, ticket: str, target: str, force: bool = False) -> TicketLinkResult:
    store = store_for_cmd("unlink")
    agent = default_agent_id()

    a = store.load_ticket(ticket)
    b = store.load_ticket(target)

    write_guard(store, a, agent, force=bool(force))
    write_guard(store, b, agent, force=bool(force))

    def _rm(t: Ticket, other_id: str) -> bool:
        links = [str(x) for x in (t.fm.get("links") or [])]
        if other_id not in links:
            return False
        t.fm["links"] = [x for x in links if x != other_id]
        return True

    changed = False
    with store.lock_for_ticket(a.id, agent):
        changed |= _rm(a, b.id)
        store.save_ticket(a)
    with store.lock_for_ticket(b.id, agent):
        changed |= _rm(b, a.id)
        store.save_ticket(b)

    if not changed:
        raise TicketNotFoundError(
            code="NOT_FOUND",
            error="Link not found",
            hint=f"No link existed between {a.id} and {b.id}.",
            details={"ticket": a.id, "target": b.id},
            suggestions=["loom ticket show <id>", "loom ticket --json show <id>"],
        )

    return TicketLinkResult(id=a.id, target=b.id)


def view(*, ticket: str) -> TicketViewResult:
    store = store_for_cmd("view")
    idx = build_index(store)

    t = store.load_ticket(ticket)
    tid = t.id

    nodes, edges = closure_from(tid, idx, include_children=True)
    health = compute_health(nodes, idx)
    graph = TicketGraph(
        nodes=sorted(list(nodes)),
        edges=_graph_edges(sorted(list(edges))),
    )
    return TicketViewResult(
        ticket=_details_for_ticket(store, t),
        graph=graph,
        health=_health_from_mapping(health),
    )


def claim(*, ticket: str, ttl: str = "30m", force: bool = False) -> TicketClaimResult:
    store = store_for_cmd("claim")
    agent = default_agent_id()

    t = store.load_ticket(ticket)
    now = utcnow()
    ttl_td = parse_duration(ttl)

    lease0 = effective_lease(store, t.id, t.fm)
    who, exp, hb = claim_state(t.fm, lease=lease0)
    active = bool(who) and (exp is None or now < exp)

    if active and who != agent and not force:
        exp_s = isoformat_z(exp) if exp else "(no expiry)"
        hb_s = isoformat_z(hb) if hb else "(no heartbeat)"
        raise PermissionError(
            f"Ticket is claimed by {who} (expires {exp_s}, heartbeat {hb_s}). Use --force to override."
        )

    with store.lock_for_ticket(t.id, agent):
        lease = {
            "claimed_by": agent,
            "claimed_at": isoformat_z(now),
            "claim_ttl": ttl,
            "claim_expires": isoformat_z(now + ttl_td),
            "heartbeat": isoformat_z(now),
        }
        store.write_lease(t.id, lease)

    return TicketClaimResult(
        id=t.id,
        claimed_by=agent,
        claim_expires=str(lease.get("claim_expires") or ""),
        heartbeat=str(lease.get("heartbeat") or ""),
    )


def heartbeat(*, ticket: str, extend: bool = True) -> TicketHeartbeatResult:
    store = store_for_cmd("heartbeat")
    agent = default_agent_id()

    t = store.load_ticket(ticket)
    lease0 = effective_lease(store, t.id, t.fm)
    who, _, _ = claim_state(t.fm, lease=lease0)
    if who != agent:
        raise PermissionError(
            f"Ticket is claimed by {who or '(nobody)'}; current agent is {agent}"
        )

    now = utcnow()
    with store.lock_for_ticket(t.id, agent):
        lease = dict(lease0) if lease0 else {}
        lease["claimed_by"] = agent
        lease["heartbeat"] = isoformat_z(now)
        if extend:
            ttl = str(lease.get("claim_ttl") or t.fm.get("claim_ttl") or "30m")
            try:
                ttl_td = parse_duration(ttl)
                lease["claim_expires"] = isoformat_z(now + ttl_td)
                lease["claim_ttl"] = ttl
            except Exception:
                pass
        store.write_lease(t.id, lease)

    return TicketHeartbeatResult(
        id=t.id,
        heartbeat=str(lease.get("heartbeat") or ""),
        claim_expires=str(lease.get("claim_expires") or ""),
    )


def release(*, ticket: str, force: bool = False) -> TicketReleaseResult:
    store = store_for_cmd("release")
    agent = default_agent_id()

    t = store.load_ticket(ticket)
    lease0 = effective_lease(store, t.id, t.fm)
    who, _, _ = claim_state(t.fm, lease=lease0)
    if who and who != agent and not force:
        raise PermissionError(f"Ticket is claimed by {who}; use --force to release")

    with store.lock_for_ticket(t.id, agent):
        store.remove_lease(t.id)

    return TicketReleaseResult(id=t.id)


def swarm(*, active_within: str = "2h") -> TicketSwarmResult:
    store = store_for_cmd("swarm")
    idx = build_index(store)

    window = parse_duration(active_within)
    now = utcnow()

    agents: Dict[str, Dict[str, Any]] = {}
    for t in idx.tickets.values():
        lease = effective_lease(store, t.id, t.fm)
        who, exp, hb = claim_state(t.fm, lease=lease)
        if not who:
            continue
        active = exp is None or now < exp
        hb_ok = hb is not None and (now - hb) <= window
        agents.setdefault(who, {"tickets": [], "active": False, "last_hb": None})
        agents[who]["tickets"].append(t)
        agents[who]["active"] = agents[who]["active"] or (active and hb_ok)
        if hb and (agents[who]["last_hb"] is None or hb > agents[who]["last_hb"]):
            agents[who]["last_hb"] = hb

    agents_out = []
    for agent, info in sorted(agents.items()):
        hb = info.get("last_hb")
        agents_out.append(
            TicketSwarmAgent(
                agent=agent,
                active=bool(info["active"]),
                last_heartbeat=(isoformat_z(hb) if hb else ""),
                claims=sorted([t.id for t in info["tickets"]]),
            )
        )
    return TicketSwarmResult(agents=agents_out)


def sync(*, message: str = "chore: tickets") -> TicketSyncResult:
    store = store_for_cmd("sync")
    repo_root = git_repo_root(store.tickets_dir) or git_repo_root(Path.cwd())
    if repo_root is None:
        raise TicketArgError(
            code="ARG",
            error="Not in a git repository",
            hint="Run from inside a git repository.",
            suggestions=["git rev-parse --show-toplevel"],
        )

    try:
        tickets_rel = store.tickets_dir.relative_to(repo_root)
    except Exception:
        raise TicketArgError(
            code="ARG",
            error="Ticket dir must be within repo root",
            hint=f"Repo root: {repo_root}. Tickets dir: {store.tickets_dir}.",
            suggestions=[
                "Move `.tickets/` into the repo root",
                "Or set TICKET_DIR to a repo-local path",
            ],
            details={
                "repo_root": str(repo_root),
                "tickets_dir": str(store.tickets_dir),
            },
        )

    entries = _git_status_entries(repo_root, pathspecs=[str(tickets_rel)])
    changed: List[str] = []
    for e in entries:
        if e.path:
            changed.append(e.path)
        if e.path2:
            changed.append(e.path2)
    changed = sorted(set([p for p in changed if p]))

    if not changed:
        return TicketSyncResult(committed=False, count=0, files=[])

    sha = git_scoped_commit(
        repo_root,
        pathspecs=[str(tickets_rel)],
        message=str(message or "chore: tickets"),
    )

    remaining = _git_status_entries(repo_root, pathspecs=[str(tickets_rel)])
    if remaining:
        raise TicketArgError(
            code="ARG",
            error="Ticket sync incomplete: .tickets still has uncommitted changes",
            hint="Inspect remaining changes under `.tickets/` and retry.",
            suggestions=["git status --porcelain .tickets"],
        )

    return TicketSyncResult(
        committed=bool(sha),
        count=len(changed),
        files=changed,
        sha=sha or "",
        message=str(message or "chore: tickets"),
    )


def sync_external(
    *,
    ticket: str = "",
    dry_run: bool = False,
    force: bool = False,
) -> TicketSyncExternalResult:
    store = store_for_cmd("sync-external")
    agent = default_agent_id()
    idx = build_index(store)

    targets: List[Ticket]
    if ticket:
        targets = [store.load_ticket(ticket)]
    else:
        targets = [
            t
            for t in idx.tickets.values()
            if str(t.fm.get("external_ref") or "").strip()
        ]

    results = []
    for t in targets:
        ext_ref = str(t.fm.get("external_ref") or "").strip()
        if not ext_ref:
            continue
        adapter = pick_adapter(ext_ref)
        if not adapter:
            results.append(
                {
                    "id": t.id,
                    "external_ref": ext_ref,
                    "ok": False,
                    "error": "No adapter for external_ref. Supported: gh:owner/repo#123, gh-123 (requires TK_GITHUB_REPO), jira:KEY-1, or a Jira browse URL.",
                }
            )
            continue

        if not dry_run:
            write_guard(store, t, agent, force=bool(force))

        try:
            if not dry_run:
                with store.lock_for_ticket(t.id, agent):
                    t2 = store.load_ticket_by_id(t.id)
                    res = adapter.sync(
                        store=store,
                        ticket=t2,
                        external_ref=ext_ref,
                        dry_run=dry_run,
                        force=bool(force),
                    )
            else:
                res = adapter.sync(
                    store=store,
                    ticket=t,
                    external_ref=ext_ref,
                    dry_run=True,
                    force=bool(force),
                )

            if store.audit is not None and AUDIT_MODE != "off":
                store.audit.log(
                    {
                        "event": "external_sync",
                        "ticket_id": t.id,
                        "adapter": str(getattr(adapter, "name", "")),
                        "dry_run": bool(dry_run),
                        "force": bool(force),
                        "changed": bool(res.get("changed")),
                        "note": str(res.get("note") or ""),
                    }
                )
            results.append({"id": t.id, "external_ref": ext_ref, "ok": True, **res})
        except Exception as e:
            if store.audit is not None and AUDIT_MODE != "off":
                store.audit.log(
                    {
                        "event": "external_sync",
                        "ticket_id": t.id,
                        "adapter": str(getattr(adapter, "name", "")),
                        "dry_run": bool(dry_run),
                        "force": bool(force),
                        "ok": False,
                        "error": str(e),
                    }
                )
            results.append(
                {"id": t.id, "external_ref": ext_ref, "ok": False, "error": str(e)}
            )

    items = [
        TicketSyncExternalItem(
            id=str(r.get("id") or ""),
            external_ref=str(r.get("external_ref") or ""),
            ok=bool(r.get("ok")),
            changed=bool(r.get("changed")),
            note=str(r.get("note") or ""),
            error=str(r.get("error") or ""),
        )
        for r in results
    ]
    return TicketSyncExternalResult(results=items)


def query(*, jmes: str = "") -> TicketQueryResult:
    store = store_for_cmd("query")
    idx = build_index(store)

    docs: List[Dict[str, Any]] = []
    for t in idx.tickets.values():
        fm = dict(t.fm)
        fm["title"] = t.title
        fm["path"] = safe_relpath(t.path, store.tickets_dir)
        docs.append(fm)

    docs.sort(
        key=lambda d: (
            d.get("status") == "closed",
            int(d.get("priority") or 2),
            d.get("id") or "",
        )
    )

    obj: Any = docs
    if jmes:
        obj = jmespath.search(jmes, docs)

    return TicketQueryResult(result=obj)


def prime() -> TicketPrimeResult:
    payload = {
        "tool": {"name": SUBSYSTEM_NAME, "version": SUBSYSTEM_VERSION},
        "purpose": "File-backed tickets for human+agent workflows (Markdown + YAML frontmatter)",
        "zen": [
            "One file. One storage format.",
            "One global --json contract.",
            "Prefer atomic updates (loom ticket update) over editing files by hand.",
        ],
        "storage": {
            "tickets_dir": f"{TICKET_DIRNAME}/ (repo-local)",
            "ticket_files": f"{TICKET_DIRNAME}/<id>.md",
            "locks": f"{TICKET_DIRNAME}/{LOCKS_DIRNAME}/ (leases for claims)",
            "audit": f"{TICKET_DIRNAME}/{AUDIT_DIRNAME}/ (append-only run logs)",
            "cache": f"{TICKET_DIRNAME}/{CACHE_DIRNAME}/ (derived caches)",
            "config": f"{TICKET_DIRNAME}/{CONFIG_FILENAME} (optional)",
        },
        "output": {
            "default": "human-readable text",
            "json": "--json emits machine-readable JSON with ok/error keys",
            "errors": {"ok": False, "error": "string", "code": "string"},
        },
        "concurrency": {
            "claims": "loom ticket claim creates/refreshes a lease; loom ticket heartbeat extends it; loom ticket release removes it",
            "enforcement": "Set TK_REQUIRE_CLAIM=1 to require the current agent to hold the claim for writes",
        },
        "env": {
            "TICKET_DIR": "Override tickets directory (absolute or repo-root-relative)",
            "TICKET_AGENT": "Agent identifier for claims (default: user@host:pid)",
            "TK_REQUIRE_CLAIM": "If set to 1, require current agent claim for write commands",
            "TK_AUDIT_MODE": "Audit mode: all|writes|off (default all)",
            "TEAM_SPRINT_TAG": "If set, loom ticket create auto-adds this tag (override with --no-sprint-tag)",
            "GITHUB_TOKEN": "Optional GitHub token for external sync",
            "TK_GITHUB_REPO": "Default repo (owner/repo) for gh-123 shorthand",
        },
        "schema": {
            "frontmatter": {
                "id": "string (filename stem)",
                "status": list(VALID_STATUSES),
                "priority": "int 0..4 (0 highest)",
                "type": "task|bug|feature|epic|chore",
                "deps": "list[id] (this ticket depends on these)",
                "links": "list[id] (symmetric loose relationships)",
                "parent": "id (parent/child work hierarchy)",
                "tags": "list[str]",
                "assignee": "string",
                "external-ref": "string (e.g., gh:owner/repo#123, url)",
                "claimed-by": "string (agent id)",
                "claim-expires": "RFC3339 / ISO8601",
                "heartbeat": "RFC3339 / ISO8601",
                "external": "dict (sync cache)",
            }
        },
        "examples": {
            "copy_paste_for_agents_md": [
                "# Tickets",
                "- Run: loom ticket prime",
                "- Prefer JSON: loom ticket --json list | loom ticket --json show <id>",
                "- Help: loom ticket -h and loom ticket <command> -h",
            ],
            "happy_path": [
                "loom ticket init",
                "loom ticket create 'Title' -t task -p 2 --tags infra",
                "loom ticket ready",
                "loom ticket claim <id> --ttl 45m",
                "loom ticket update <id> --status in_progress",
                "loom ticket add-note <id> 'Progress update...'",
                "loom ticket close <id>",
                "loom ticket release <id>",
                "loom ticket sync -m 'chore: tickets'",
            ],
            "bootstrap": [
                "loom ticket -h",
                "loom ticket init",
                'loom ticket create "Implement orchestration layer" -p 1 -t epic --tags ai,infra',
                'loom ticket create "Investigate flaky CI" -t bug -p 1 --tags ci,infra -d "Observed intermittent failures in unit tests when run in parallel. Collect failing logs, identify race, and propose minimal fix."',
            ],
            "work": [
                "loom ticket list --status open",
                "loom ticket ready",
                "loom ticket blocked",
                "loom ticket show <id>",
                "loom ticket view <id>",
            ],
            "deps": [
                "loom ticket dep <id>",
                "loom ticket dep-add <id> <dep-id>",
                "loom ticket dep-rm <id> <dep-id>",
                "loom ticket dep-cycle",
            ],
            "mutation": [
                "loom ticket claim <id> --ttl 45m",
                "loom ticket heartbeat <id>",
                "loom ticket update <id> --status in_progress",
                'loom ticket update <id> --title "New title"',
                'loom ticket add-note <id> "Started investigation. Next: reproduce locally and capture stacktrace."',
                "cat new_body.md | loom ticket update <id>",
                "loom ticket release <id>",
            ],
            "machine": [
                "loom ticket --json list",
                "loom ticket --json show <id>",
                "loom ticket --json view <id>",
                "loom ticket --json query --format json",
            ],
            "help": [
                "loom ticket -h",
                "loom ticket <command> -h",
                "loom ticket prime --json",
            ],
        },
    }

    return TicketPrimeResult(payload=payload)
