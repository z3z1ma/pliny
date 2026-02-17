from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Sequence

from agent_loom.ticket.errors import TicketArgError, TicketNotFoundError
from agent_loom.ticket.graph import build_index, has_cycle
from agent_loom.ticket.models import Ticket
from agent_loom.ticket.store import TicketStore, write_guard


@dataclass(frozen=True)
class TicketUpdateSpec:
    title: Optional[str]
    status: str
    priority: Optional[int]
    type: str
    assignee: str
    tags: Optional[str]
    external_ref: Optional[str]
    parent: Optional[str]
    remove_parent: bool
    deps: Optional[str]
    add_deps: Sequence[str]
    remove_deps: Sequence[str]
    links: Optional[str]
    add_links: Sequence[str]
    remove_links: Sequence[str]
    body: Optional[str]
    force: bool


def _is_clear_token(value: str) -> bool:
    return value.strip().lower() in {"", "none", "null", "(none)", "-"}


def _parse_ref_list(store: TicketStore, raw: str) -> list[str]:
    parts = [p for p in re.split(r"[,\s]+", str(raw or "").strip()) if p.strip()]
    out: list[str] = []
    for part in parts:
        out.append(store.resolve_id(part))
    return sorted(set(out))


def _resolve_refs(store: TicketStore, patterns: Sequence[str]) -> list[str]:
    out: list[str] = []
    for pattern in patterns:
        ref = str(pattern or "").strip()
        if not ref:
            continue
        out.append(store.resolve_id(ref))
    return sorted(set(out))


def _validate_parent_chain(
    store: TicketStore, *, ticket_id: str, parent_id: str
) -> None:
    cur = parent_id
    seen: set[str] = set()
    while cur:
        if cur == ticket_id:
            raise TicketArgError(
                code="ARG",
                error="Parent would create a cycle",
                hint=f"Setting parent={parent_id} would make {ticket_id} its own ancestor.",
            )
        if cur in seen:
            return
        seen.add(cur)
        try:
            parent_ticket = store.load_ticket_by_id(cur)
        except TicketNotFoundError as exc:
            raise TicketArgError(
                code="ARG",
                error=f"Parent chain references missing ticket: {cur}",
                hint="Choose an existing parent ticket.",
                suggestions=["loom ticket list", "loom ticket show <id>"],
            ) from exc
        nxt = str(parent_ticket.fm.get("parent") or "").strip()
        if not nxt:
            return
        cur = nxt


def _validate_update_conflicts(spec: TicketUpdateSpec) -> None:
    if spec.remove_parent and spec.parent is not None:
        raise TicketArgError(
            code="ARG",
            error="--remove-parent cannot be combined with --parent",
            hint="Use either --remove-parent, or set --parent (use 'none' to clear).",
        )

    if spec.deps is not None and (spec.add_deps or spec.remove_deps):
        raise TicketArgError(
            code="ARG",
            error="--deps cannot be combined with --add-dep/--remove-dep",
            hint="Use --deps to replace the full list, or --add-dep/--remove-dep for incremental edits.",
        )
    if spec.links is not None and (spec.add_links or spec.remove_links):
        raise TicketArgError(
            code="ARG",
            error="--links cannot be combined with --add-link/--remove-link",
            hint="Use --links to replace the full list, or --add-link/--remove-link for incremental edits.",
        )


def _validate_dependency_graph_update(
    store: TicketStore, *, ticket_id: str, deps: Sequence[str]
) -> None:
    idx = build_index(store)
    deps_map = {k: list(v) for k, v in idx.deps.items()}
    deps_map.setdefault(ticket_id, [])
    deps_map[ticket_id] = list(deps)
    if has_cycle(deps_map):
        raise TicketArgError(
            code="ARG",
            error=f"Dependency update would create a cycle for {ticket_id}",
            hint="Inspect cycles with `loom ticket dep-cycle`.",
            suggestions=["loom ticket dep-cycle"],
        )


def _apply_frontmatter_updates(
    ticket: Ticket,
    *,
    spec: TicketUpdateSpec,
    require_status: Callable[[str], str],
) -> None:
    if spec.status:
        ticket.fm["status"] = require_status(spec.status)
    if spec.priority is not None:
        ticket.fm["priority"] = int(spec.priority)
    if spec.type:
        ticket.fm["type"] = spec.type
    if spec.assignee:
        ticket.fm["assignee"] = spec.assignee
    if spec.tags is not None:
        ticket.fm["tags"] = [x.strip() for x in (spec.tags or "").split(",") if x.strip()]
    if spec.external_ref is not None:
        ticket.fm["external_ref"] = str(spec.external_ref or "").strip()


def _apply_parent_update(store: TicketStore, ticket: Ticket, *, spec: TicketUpdateSpec) -> None:
    if spec.remove_parent:
        ticket.fm["parent"] = ""

    if spec.parent is None:
        return
    parent_value = str(spec.parent or "").strip()
    if _is_clear_token(parent_value):
        ticket.fm["parent"] = ""
        return

    parent_id = store.resolve_id(parent_value)
    if parent_id == ticket.id:
        raise TicketArgError(
            code="ARG",
            error="A ticket cannot be its own parent",
            hint=f"Both references resolved to {ticket.id}.",
        )
    _validate_parent_chain(store, ticket_id=ticket.id, parent_id=parent_id)
    ticket.fm["parent"] = parent_id


def _apply_dependency_update(
    store: TicketStore, ticket: Ticket, *, spec: TicketUpdateSpec
) -> None:
    if spec.deps is not None:
        dep_ids = (
            []
            if _is_clear_token(str(spec.deps or ""))
            else _parse_ref_list(store, spec.deps)
        )
        if ticket.id in dep_ids:
            raise TicketArgError(
                code="ARG",
                error="A ticket cannot depend on itself",
                hint=f"Both references resolved to {ticket.id}.",
            )
        _validate_dependency_graph_update(store, ticket_id=ticket.id, deps=dep_ids)
        ticket.fm["deps"] = dep_ids
        return

    if not (spec.add_deps or spec.remove_deps):
        return

    current = [str(x) for x in (ticket.fm.get("deps") or [])]
    current_set = {dep for dep in current if dep}
    add_ids = _resolve_refs(store, spec.add_deps)
    remove_ids = _resolve_refs(store, spec.remove_deps)

    if ticket.id in add_ids:
        raise TicketArgError(
            code="ARG",
            error="A ticket cannot depend on itself",
            hint=f"Both references resolved to {ticket.id}.",
        )

    for dependency_id in remove_ids:
        if dependency_id not in current_set:
            raise TicketNotFoundError(
                code="NOT_FOUND",
                error="Dependency not found",
                hint=f"{ticket.id} does not depend on {dependency_id}.",
                details={"ticket": ticket.id, "dependency": dependency_id},
                suggestions=["loom ticket show <id>", "loom ticket --json show <id>"],
            )

    dep_ids = sorted((current_set | set(add_ids)) - set(remove_ids))
    _validate_dependency_graph_update(store, ticket_id=ticket.id, deps=dep_ids)
    ticket.fm["deps"] = dep_ids


def _apply_link_replace(store: TicketStore, ticket: Ticket, *, links: Optional[str]) -> None:
    if links is None:
        return
    link_ids = [] if _is_clear_token(str(links or "")) else _parse_ref_list(store, links)
    if ticket.id in link_ids:
        raise TicketArgError(
            code="ARG",
            error="A ticket cannot link to itself",
            hint=f"Both references resolved to {ticket.id}.",
        )
    ticket.fm["links"] = link_ids


def _apply_incremental_link_update(
    store: TicketStore,
    ticket: Ticket,
    *,
    spec: TicketUpdateSpec,
    agent: str,
    tickets_to_save: Dict[str, Ticket],
) -> None:
    if not (spec.add_links or spec.remove_links):
        return

    add_ids = _resolve_refs(store, spec.add_links)
    remove_ids = _resolve_refs(store, spec.remove_links)

    if ticket.id in add_ids or ticket.id in remove_ids:
        raise TicketArgError(
            code="ARG",
            error="A ticket cannot link to itself",
            hint=f"Both references resolved to {ticket.id}.",
        )

    targets: Dict[str, Ticket] = {}
    for target_id in sorted(set(add_ids + remove_ids)):
        target = store.load_ticket_by_id(target_id)
        write_guard(store, target, agent, force=bool(spec.force))
        targets[target_id] = target
        tickets_to_save[target_id] = target

    current_links = {
        str(link_id) for link_id in (ticket.fm.get("links") or []) if str(link_id)
    }
    changed_any = False

    for target_id in add_ids:
        other = targets[target_id]
        other_links = {
            str(link_id) for link_id in (other.fm.get("links") or []) if str(link_id)
        }
        if target_id not in current_links:
            current_links.add(target_id)
            changed_any = True
        if ticket.id not in other_links:
            other_links.add(ticket.id)
            other.fm["links"] = sorted(other_links)
            changed_any = True

    for target_id in remove_ids:
        other = targets[target_id]
        other_links = {
            str(link_id) for link_id in (other.fm.get("links") or []) if str(link_id)
        }
        ticket_had_link = target_id in current_links
        other_had_link = ticket.id in other_links
        current_links.discard(target_id)
        other_links.discard(ticket.id)
        other.fm["links"] = sorted(other_links)
        if ticket_had_link or other_had_link:
            changed_any = True

    if remove_ids and not changed_any:
        raise TicketNotFoundError(
            code="NOT_FOUND",
            error="Link not found",
            hint=f"No link existed between {ticket.id} and the requested target(s).",
            suggestions=["loom ticket show <id>", "loom ticket --json show <id>"],
        )

    ticket.fm["links"] = sorted(current_links)


def _apply_body_title_updates(ticket: Ticket, *, body: Optional[str], title: Optional[str]) -> None:
    if body is not None:
        ticket.body = body if body.endswith("\n") else (body + "\n")
    if title:
        if re.search(r"(?m)^#\s+.*$", ticket.body):
            ticket.body = re.sub(r"(?m)^#\s+.*$", f"# {title}", ticket.body, count=1)
        else:
            ticket.body = f"# {title}\n\n" + ticket.body.lstrip("\n")
        ticket.body = ticket.body.rstrip() + "\n"


def _persist_ticket_updates(
    store: TicketStore, *, tickets_to_save: Dict[str, Ticket], agent: str
) -> None:
    for ticket_id in sorted(tickets_to_save.keys()):
        ticket = tickets_to_save[ticket_id]
        with store.lock_for_ticket(ticket.id, agent):
            store.save_ticket(ticket)


def apply_ticket_update_workflow(
    *,
    store: TicketStore,
    ticket: Ticket,
    agent: str,
    spec: TicketUpdateSpec,
    require_status: Callable[[str], str],
) -> None:
    write_guard(store, ticket, agent, force=bool(spec.force))
    _validate_update_conflicts(spec)
    _apply_frontmatter_updates(ticket, spec=spec, require_status=require_status)
    _apply_parent_update(store, ticket, spec=spec)
    _apply_dependency_update(store, ticket, spec=spec)

    tickets_to_save: Dict[str, Ticket] = {ticket.id: ticket}
    _apply_link_replace(store, ticket, links=spec.links)
    if spec.links is None:
        _apply_incremental_link_update(
            store,
            ticket,
            spec=spec,
            agent=agent,
            tickets_to_save=tickets_to_save,
        )
    _apply_body_title_updates(ticket, body=spec.body, title=spec.title)
    _persist_ticket_updates(store, tickets_to_save=tickets_to_save, agent=agent)

