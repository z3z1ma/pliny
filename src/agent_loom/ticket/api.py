from __future__ import annotations

import re
from pathlib import Path
from typing import Any, List, Optional, Sequence

from agent_loom.core.git import git_checked, git_repo_root, git_scoped_commit
from agent_loom.ticket.frontmatter import decanonicalize_frontmatter
from agent_loom.ticket.graph import (
    blockers_for,
    build_index,
    closure_from,
    compute_health,
    predecessors,
)
from agent_loom.ticket.models import (
    GitStatusEntry,
    TicketListResult,
    TicketSummary,
    TicketDetails,
    TicketDepResult,
    TicketGraph,
    TicketGraphEdge,
    TicketHealth,
    TicketRelationships,
    TicketShowResult,
    TicketSyncResult,
    TicketUpdateResult,
    TicketViewResult,
    TicketSwarmAgent,
    TicketSwarmResult,
)
from agent_loom.ticket.core import create_in_dir
from agent_loom.ticket.models import TicketCreateResult
from agent_loom.ticket.store import (
    TicketStore,
    active_claimed_by,
    effective_lease,
    write_guard,
)
from agent_loom.ticket.errors import TicketArgError
from agent_loom.ticket.normalize import normalize_status
from agent_loom.ticket.constants import STATUS_ORDER, VALID_STATUSES
from agent_loom.ticket.core import default_agent_id


def show(*, ticket_id: str, tickets_dir: Path) -> TicketShowResult:
    store = TicketStore(tickets_dir)
    idx = build_index(store)
    t = store.load_ticket(ticket_id)

    lease = effective_lease(store, t.id, t.fm)
    claimed_by = active_claimed_by(t.fm, lease=lease)

    blockers = blockers_for(t.id, idx)
    pred = predecessors(idx.deps)
    blocking = [
        x
        for x in pred.get(t.id, [])
        if (tx := idx.ticket(x)) is not None and tx.status != "closed"
    ]
    children = list(idx.parent.get(t.id, []))
    linked = list(idx.links.get(t.id, []))

    ticket = TicketDetails(
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

    relationships = TicketRelationships(
        blockers=blockers,
        blocking=sorted(set(blocking)),
        children=sorted(set(children)),
        linked=sorted(set(linked)),
    )

    return TicketShowResult(
        ticket=ticket,
        relationships=relationships,
        body=t.body,
        frontmatter=decanonicalize_frontmatter(t.fm),
        lease=dict(lease),
    )


def _graph_edges(edges: list[tuple[str, str, str]]) -> list[TicketGraphEdge]:
    return [TicketGraphEdge(src=a, dst=b, kind=k) for a, b, k in edges]


def _health_from_mapping(health: dict[str, Any]) -> TicketHealth:
    return TicketHealth(
        counts=dict(health.get("counts") or {}),
        ready=int(health.get("ready") or 0),
        blocked=int(health.get("blocked") or 0),
        bottlenecks=list(health.get("bottlenecks") or []),
    )


def view(*, ticket_id: str, tickets_dir: Path) -> TicketViewResult:
    store = TicketStore(tickets_dir)
    idx = build_index(store)
    t = store.load_ticket(ticket_id)

    nodes, edges = closure_from(t.id, idx, include_children=True)
    health = compute_health(nodes, idx)
    graph = TicketGraph(
        nodes=sorted(list(nodes)), edges=_graph_edges(sorted(list(edges)))
    )
    return TicketViewResult(
        ticket=show(ticket_id=t.id, tickets_dir=tickets_dir).ticket,
        graph=graph,
        health=_health_from_mapping(health),
    )


def dep(*, ticket_id: str, tickets_dir: Path) -> TicketDepResult:
    store = TicketStore(tickets_dir)
    idx = build_index(store)
    root = store.resolve_id(ticket_id)
    nodes, edges = closure_from(root, idx, include_children=False)
    health = compute_health(nodes, idx)
    dep_edges = [e for e in sorted(list(edges)) if e[2] == "dep"]
    return TicketDepResult(
        root=root,
        nodes=sorted(list(nodes)),
        edges=_graph_edges(dep_edges),
        health=_health_from_mapping(health),
    )


def swarm(*, tickets_dir: Path, active_within: str = "2h") -> TicketSwarmResult:
    from agent_loom.core.time import parse_duration, utcnow, isoformat_z
    from agent_loom.ticket.store import claim_state

    store = TicketStore(tickets_dir)
    idx = build_index(store)
    window = parse_duration(active_within)
    now = utcnow()

    agents: dict[str, dict[str, Any]] = {}
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

    agents_out: list[TicketSwarmAgent] = []
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


def create(
    *,
    tickets_dir: Path,
    title: str,
    type: str,
    priority: int,
    tags: str = "",
    description: str = "",
    assignee: str = "",
    external_ref: str = "",
    parent: str = "",
    design: str = "",
    acceptance: str = "",
) -> TicketCreateResult:
    return create_in_dir(
        tickets_dir=tickets_dir,
        title=str(title or "").strip(),
        type=str(type or "").strip(),
        priority=int(priority),
        tags=str(tags or "").strip() or None,
        description=str(description or "").strip() or None,
        assignee=str(assignee or "").strip() or None,
        external_ref=str(external_ref or "").strip() or None,
        parent=str(parent or "").strip() or None,
        design=str(design or "").strip() or None,
        acceptance=str(acceptance or "").strip() or None,
    )


def _require_status(s: str) -> str:
    s0 = normalize_status(s)
    if s0 not in VALID_STATUSES:
        raise TicketArgError(
            code="ARG",
            error=f"Invalid status {str(s).strip()!r}. Must be one of: {', '.join(VALID_STATUSES)}",
            hint=(
                "Aliases: todo/new/backlog->open, queued/next->ready, "
                "wip/doing/started->in_progress, stuck/waiting->blocked, "
                "pr/ready_for_review->review, done/completed->closed."
            ),
        )
    return s0


def _status_rank(status: str) -> int:
    try:
        return STATUS_ORDER.index(str(status or ""))
    except ValueError:
        return len(STATUS_ORDER)


def list_tickets(
    *,
    tickets_dir: Path,
    status: str = "",
    type_: str = "",
    assignee: str = "",
    tag: str = "",
    prio_min: Optional[int] = None,
    prio_max: Optional[int] = None,
    include_closed: bool = True,
    limit: int = 0,
) -> TicketListResult:
    store = TicketStore(tickets_dir)
    idx = build_index(store)

    limit = int(limit or 0)
    if limit < 0:
        raise TicketArgError(
            code="ARG",
            error="limit must be >= 0",
            hint="Use 0 for unlimited.",
            details={"limit": limit},
        )

    status_filter = _require_status(status) if status else ""
    type_filter = (type_ or "").strip()
    assignee_filter = (assignee or "").strip()
    tag_filter = (tag or "").strip()

    def match(t: Any) -> bool:
        if not include_closed and getattr(t, "status", "") == "closed":
            return False
        if status_filter and getattr(t, "status", "") != status_filter:
            return False
        if (
            type_filter
            and str((getattr(t, "fm", {}) or {}).get("type") or "") != type_filter
        ):
            return False
        if (
            assignee_filter
            and str((getattr(t, "fm", {}) or {}).get("assignee") or "")
            != assignee_filter
        ):
            return False
        if tag_filter:
            tags = [
                str(x) for x in (((getattr(t, "fm", {}) or {}).get("tags") or []) or [])
            ]
            if tag_filter not in tags:
                return False
        # Priority filter
        try:
            p = int(
                (getattr(t, "fm", {}) or {}).get("priority")
                or getattr(t, "priority", 2)
            )
        except Exception:
            p = int(getattr(t, "priority", 2) or 2)
        if prio_min is not None and p < int(prio_min):
            return False
        if prio_max is not None and p > int(prio_max):
            return False
        return True

    tickets = [t for t in idx.tickets.values() if match(t)]
    tickets.sort(
        key=lambda t: (
            _status_rank(getattr(t, "status", "")),
            getattr(t, "priority", 2),
            getattr(t, "id", ""),
        )
    )
    if limit:
        tickets = tickets[:limit]

    rows: list[TicketSummary] = []
    for t in tickets:
        lease = effective_lease(store, t.id, t.fm)
        claimed_by = active_claimed_by(t.fm, lease=lease)
        rows.append(
            TicketSummary(
                id=t.id,
                title=t.title,
                status=t.status,
                priority=t.priority,
                assignee=str(t.fm.get("assignee") or ""),
                tags=[str(x) for x in (t.fm.get("tags") or [])],
                claimed_by=claimed_by,
                deps=[str(x) for x in (t.fm.get("deps") or [])],
                blockers=[],
                mtime="",
            )
        )

    return TicketListResult(count=len(rows), tickets=rows)


def update(
    *,
    tickets_dir: Path,
    ticket_id: str,
    title: Optional[str] = None,
    status: str = "",
    priority: Optional[int] = None,
    type_: str = "",
    assignee: str = "",
    tags: Optional[str] = None,
    external_ref: Optional[str] = None,
    body_text: Optional[str] = None,
    force: bool = False,
) -> TicketUpdateResult:
    store = TicketStore(tickets_dir)
    agent = default_agent_id()

    t = store.load_ticket(ticket_id)
    write_guard(store, t, agent, force=bool(force))

    if status:
        t.fm["status"] = _require_status(status)
    if priority is not None:
        t.fm["priority"] = int(priority)
    if type_:
        t.fm["type"] = str(type_)
    if assignee:
        t.fm["assignee"] = str(assignee)
    if tags is not None:
        t.fm["tags"] = [x.strip() for x in (tags or "").split(",") if x.strip()]
    if external_ref is not None:
        t.fm["external_ref"] = str(external_ref or "").strip()

    with store.lock_for_ticket(t.id, agent):
        if body_text is not None:
            t.body = str(body_text)
            if not t.body.endswith("\n"):
                t.body += "\n"

        if title:
            if re.search(r"(?m)^#\s+.*$", t.body):
                t.body = re.sub(r"(?m)^#\s+.*$", f"# {title}", t.body, count=1)
            else:
                t.body = f"# {title}\n\n" + t.body.lstrip("\n")
            t.body = t.body.rstrip() + "\n"

        store.save_ticket(t)

    return TicketUpdateResult(id=t.id)


def sync(*, tickets_dir: Path, message: str = "chore: tickets") -> TicketSyncResult:
    store = TicketStore(tickets_dir)
    repo_root = git_repo_root(store.tickets_dir) or git_repo_root(Path.cwd())
    if repo_root is None:
        raise TicketArgError(
            code="ARG",
            error="Not in a git repository",
            hint="Run from inside a git repository.",
        )

    try:
        tickets_rel = store.tickets_dir.relative_to(repo_root)
    except Exception:
        raise TicketArgError(
            code="ARG",
            error="Ticket dir must be within repo root",
            hint=f"Repo root: {repo_root}. Tickets dir: {store.tickets_dir}.",
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
        )

    return TicketSyncResult(
        committed=bool(sha),
        count=len(changed),
        files=changed,
        sha=sha or "",
        message=str(message or "chore: tickets"),
    )


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


__all__ = [
    "TicketDetails",
    "TicketCreateResult",
    "TicketRelationships",
    "TicketShowResult",
    "TicketSyncResult",
    "TicketListResult",
    "TicketSummary",
    "TicketUpdateResult",
    "TicketDepResult",
    "TicketViewResult",
    "TicketSwarmResult",
    "create",
    "list_tickets",
    "show",
    "dep",
    "sync",
    "swarm",
    "update",
    "view",
]
