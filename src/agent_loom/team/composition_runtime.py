from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping

from agent_loom.team.constants import ROLE_INTEGRATOR, ROLE_INVESTIGATOR, ROLE_MANAGER, ROLE_WORKER
from agent_loom.team.errors import TeamError


@dataclass(frozen=True)
class ResolvedMemberProfile:
    member_id: str
    role: str
    lifecycle: str
    source: str
    agent: str
    harness: str
    byo_agent: Dict[str, Any]


def resolve_member_profile(
    run: Mapping[str, Any],
    *,
    role: str,
    ticket_id: str = "",
    worktree_key: str = "",
) -> ResolvedMemberProfile | None:
    spec = _composition_spec(run)
    if spec is None:
        return None

    members_value = spec.get("members")
    members_raw: list[Any] = list(members_value) if isinstance(members_value, list) else []
    members: Dict[str, Dict[str, Any]] = {}
    for item in members_raw:
        if not isinstance(item, dict):
            continue
        member_id = str(item.get("id") or "").strip()
        if not member_id:
            continue
        members[member_id] = item

    role_norm = str(role or "").strip().lower()
    role_members = [m for m in members.values() if str(m.get("role") or "").strip().lower() == role_norm]
    if not role_members:
        return None

    selected_member: Dict[str, Any] | None = None
    selected_member_id = ""
    mapped_member_ids = _mapped_member_ids(spec, ticket_id=ticket_id, worktree_key=worktree_key)
    if mapped_member_ids:
        if len(mapped_member_ids) > 1:
            keys = ", ".join(_nonempty_unique([ticket_id, worktree_key])) or "<none>"
            raise TeamError(
                (
                    f"Composition mapping is ambiguous for role={role_norm}: "
                    f"matched members={', '.join(mapped_member_ids)} keys={keys}"
                ),
                code="ARG",
                exit_code=2,
                hint="Fix worktree_mappings so a ticket/worktree resolves to exactly one member.",
            )
        selected_member_id = mapped_member_ids[0]
        selected_member = members.get(selected_member_id)
        if not isinstance(selected_member, dict):
            raise TeamError(
                f"Composition mapping references unknown member: {selected_member_id}",
                code="ARG",
                exit_code=2,
            )
        selected_role = str(selected_member.get("role") or "").strip().lower()
        if selected_role != role_norm:
            raise TeamError(
                (
                    f"Composition mapping selected member '{selected_member_id}' with role={selected_role}, "
                    f"but role={role_norm} was requested"
                ),
                code="ARG",
                exit_code=2,
                hint="Update worktree_mappings so each role resolves to a matching member role.",
            )
    else:
        if len(role_members) > 1:
            raise TeamError(
                (
                    f"Multiple composition members exist for role={role_norm} but no mapping matched "
                    f"ticket={ticket_id!r} worktree={worktree_key!r}"
                ),
                code="ARG",
                exit_code=2,
                hint="Add a disambiguating worktree_mappings entry for this ticket/worktree.",
            )
        selected_member = role_members[0]
        selected_member_id = str(selected_member.get("id") or "").strip()

    if selected_member is None:
        raise TeamError("Composition member resolution failed", code="BAD_STATE", exit_code=2)

    lifecycle = str(selected_member.get("lifecycle") or "").strip()
    source = str(selected_member.get("source") or "").strip()
    agent = str(selected_member.get("agent") or "").strip()
    harness = str(selected_member.get("harness") or "").strip()

    byo_agent: Dict[str, Any] = {}
    if source == "byo":
        byo_raw_value = spec.get("byo_agents")
        byo_raw: Dict[str, Any] = dict(byo_raw_value) if isinstance(byo_raw_value, dict) else {}
        byo_entry = byo_raw.get(agent)
        if not isinstance(byo_entry, dict):
            available = ", ".join(sorted(str(k) for k in byo_raw.keys())) if byo_raw else "<none>"
            raise TeamError(
                f"Composition member '{selected_member_id}' references missing BYO agent '{agent}'",
                code="ARG",
                exit_code=2,
                hint=f"Define it under composition.spec.byo_agents. Available refs: {available}",
            )
        byo_agent = dict(byo_entry)

    return ResolvedMemberProfile(
        member_id=selected_member_id,
        role=role_norm,
        lifecycle=lifecycle,
        source=source,
        agent=agent,
        harness=harness,
        byo_agent=byo_agent,
    )


def enforce_member_lifecycle(*, profile: ResolvedMemberProfile | None, role: str) -> None:
    if profile is None:
        return

    role_norm = str(role or "").strip().lower()
    lifecycle = str(profile.lifecycle or "").strip().lower()

    if role_norm in (ROLE_WORKER, ROLE_INVESTIGATOR) and lifecycle != "ephemeral":
        raise TeamError(
            (
                f"Role '{role_norm}' must use ephemeral composition members; "
                f"resolved member='{profile.member_id}' lifecycle='{profile.lifecycle}'"
            ),
            code="ARG",
            exit_code=2,
            hint="Use lifecycle: ephemeral for worker/investigator members mapped to tickets/worktrees.",
        )

    if role_norm in (ROLE_MANAGER, ROLE_INTEGRATOR) and lifecycle != "always_on":
        raise TeamError(
            (
                f"Role '{role_norm}' must use always_on composition members; "
                f"resolved member='{profile.member_id}' lifecycle='{profile.lifecycle}'"
            ),
            code="ARG",
            exit_code=2,
            hint="Use lifecycle: always_on for manager/integrator members.",
        )


def _composition_spec(run: Mapping[str, Any]) -> Dict[str, Any] | None:
    composition = run.get("composition") if isinstance(run.get("composition"), dict) else None
    if composition is None:
        return None
    spec = composition.get("spec") if isinstance(composition.get("spec"), dict) else None
    if spec is None:
        return None
    return dict(spec)


def _mapped_member_ids(spec: Mapping[str, Any], *, ticket_id: str, worktree_key: str) -> list[str]:
    mappings_value = spec.get("worktree_mappings")
    mappings: list[Any] = list(mappings_value) if isinstance(mappings_value, list) else []
    keys = _nonempty_unique([ticket_id, worktree_key])
    if not keys:
        return []

    matched: set[str] = set()
    for mapping in mappings:
        if not isinstance(mapping, dict):
            continue
        pattern = str(mapping.get("pattern") or "").strip()
        member_id = str(mapping.get("member") or "").strip()
        if not pattern or not member_id:
            continue
        for key in keys:
            if _pattern_matches(key, pattern):
                matched.add(member_id)
                break
    return sorted(matched)


def _pattern_matches(value: str, pattern: str) -> bool:
    if pattern == "*":
        return True
    if pattern.endswith("*"):
        return value.startswith(pattern[:-1])
    return value == pattern


def _nonempty_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in values:
        val = str(raw or "").strip()
        if not val or val in seen:
            continue
        out.append(val)
        seen.add(val)
    return out


__all__ = [
    "ResolvedMemberProfile",
    "enforce_member_lifecycle",
    "resolve_member_profile",
]
