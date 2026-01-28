from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Sequence

from agent_loom.core.git import git_checked, git_repo_root, git_scoped_commit
from agent_loom.ticket.frontmatter import decanonicalize_frontmatter
from agent_loom.ticket.graph import blockers_for, build_index, predecessors
from agent_loom.ticket.models import (
    GitStatusEntry,
    TicketDetails,
    TicketRelationships,
    TicketShowResult,
    TicketSyncResult,
)
from agent_loom.ticket.core import create_in_dir
from agent_loom.ticket.models import TicketCreateResult
from agent_loom.ticket.store import (
    TicketStore,
    active_claimed_by,
    effective_lease,
)
from agent_loom.ticket.errors import TicketArgError


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
    "create",
    "show",
    "sync",
]
