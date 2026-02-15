from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

import yaml

from agent_loom.team.constants import (
    DEFAULT_HARNESS,
    ROLE_INTEGRATOR,
    ROLE_INVESTIGATOR,
    ROLE_MANAGER,
    ROLE_WORKER,
)
from agent_loom.team.errors import TeamError

SCHEMA_VERSION = 1

_MEMBER_ROLES = {
    ROLE_MANAGER,
    ROLE_WORKER,
    ROLE_INVESTIGATOR,
    ROLE_INTEGRATOR,
}
_MEMBER_LIFECYCLES = {"always_on", "ephemeral"}
_MEMBER_SOURCES = {"loom", "byo"}
_HARNESS_VALUES = {"opencode", "claude", "omp", "codex"}
_COMM_CHANNELS = {"inbox_only", "inbox_and_tmux"}
_ESCALATION_TARGETS = {ROLE_MANAGER, ROLE_INTEGRATOR}
_PATTERN_HINT = "Use exact names or a single trailing '*' prefix pattern (examples: 'al-aec3', 'al-*', '*')."


class TeamCompositionError(TeamError):
    def __init__(self, message: str, *, hint: str = "") -> None:
        super().__init__(message, code="ARG", exit_code=2, hint=hint)


@dataclass(frozen=True)
class CompositionMetadata:
    name: str
    purpose: str
    labels: Tuple[str, ...]

    def as_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"name": self.name}
        if self.purpose:
            out["purpose"] = self.purpose
        if self.labels:
            out["labels"] = list(self.labels)
        return out


@dataclass(frozen=True)
class BYOAgent:
    id: str
    command: str
    cwd: str
    env: Tuple[Tuple[str, str], ...]

    def as_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"command": self.command}
        if self.cwd:
            out["cwd"] = self.cwd
        if self.env:
            out["env"] = {k: v for k, v in self.env}
        return out


@dataclass(frozen=True)
class TeamMember:
    id: str
    role: str
    lifecycle: str
    source: str
    agent: str
    harness: str

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "lifecycle": self.lifecycle,
            "source": self.source,
            "agent": self.agent,
            "harness": self.harness,
        }


@dataclass(frozen=True)
class WorktreeMapping:
    pattern: str
    member: str

    def as_dict(self) -> Dict[str, str]:
        return {
            "pattern": self.pattern,
            "member": self.member,
        }


@dataclass(frozen=True)
class EscalationPolicy:
    target_role: str
    timeout_seconds: int
    max_retries: int

    def as_dict(self) -> Dict[str, Any]:
        return {
            "target_role": self.target_role,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
        }


@dataclass(frozen=True)
class CommunicationPolicy:
    channel: str
    require_ack: bool
    escalation: EscalationPolicy

    def as_dict(self) -> Dict[str, Any]:
        return {
            "channel": self.channel,
            "require_ack": self.require_ack,
            "escalation": self.escalation.as_dict(),
        }


@dataclass(frozen=True)
class TeamComposition:
    version: int
    metadata: CompositionMetadata
    members: Tuple[TeamMember, ...]
    worktree_mappings: Tuple[WorktreeMapping, ...]
    communication: CommunicationPolicy
    byo_agents: Tuple[BYOAgent, ...]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "metadata": self.metadata.as_dict(),
            "members": [m.as_dict() for m in self.members],
            "worktree_mappings": [m.as_dict() for m in self.worktree_mappings],
            "communication": self.communication.as_dict(),
            "byo_agents": {a.id: a.as_dict() for a in self.byo_agents},
        }


def parse_team_composition_yaml(text: str, *, source: str = "<string>") -> TeamComposition:
    try:
        raw_doc = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise TeamCompositionError(f"{source}: invalid YAML: {e}") from e

    if raw_doc is None:
        raise TeamCompositionError(f"{source}: expected a YAML mapping/object at top level")
    if not isinstance(raw_doc, dict):
        raise TeamCompositionError(f"{source}: expected a YAML mapping/object at top level")

    root = _expect_mapping(f"{source}", raw_doc)
    _require_keys(f"{source}", root, {"version", "metadata", "members", "worktree_mappings", "communication"})
    _reject_unknown_keys(
        f"{source}",
        root,
        {"version", "metadata", "members", "worktree_mappings", "communication", "byo_agents"},
    )

    version = _expect_int(f"{source}.version", root.get("version"), min_value=1)
    if version != SCHEMA_VERSION:
        raise TeamCompositionError(
            f"{source}.version: unsupported schema version {version}",
            hint=f"Use version: {SCHEMA_VERSION}",
        )

    metadata = _parse_metadata(root.get("metadata"), source=source)
    byo_agents = _parse_byo_agents(root.get("byo_agents"), source=source)
    members = _parse_members(root.get("members"), source=source, byo_agent_ids={x.id for x in byo_agents})
    mappings = _parse_worktree_mappings(
        root.get("worktree_mappings"), source=source, member_ids={x.id for x in members}
    )
    communication = _parse_communication(root.get("communication"), source=source)

    return TeamComposition(
        version=version,
        metadata=metadata,
        members=tuple(sorted(members, key=lambda x: x.id)),
        worktree_mappings=tuple(sorted(mappings, key=lambda x: (x.pattern, x.member))),
        communication=communication,
        byo_agents=tuple(sorted(byo_agents, key=lambda x: x.id)),
    )


def load_team_composition_yaml(path: Path | str) -> TeamComposition:
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
    except OSError as e:
        raise TeamCompositionError(f"Unable to read composition file {p}: {e}") from e
    return parse_team_composition_yaml(text, source=str(p))


def _parse_metadata(raw: Any, *, source: str) -> CompositionMetadata:
    obj = _expect_mapping(f"{source}.metadata", raw)
    _require_keys(f"{source}.metadata", obj, {"name"})
    _reject_unknown_keys(f"{source}.metadata", obj, {"name", "purpose", "labels"})

    name = _expect_nonempty_str(f"{source}.metadata.name", obj.get("name"))
    purpose = _expect_optional_str(f"{source}.metadata.purpose", obj.get("purpose"))
    labels = _expect_str_list(f"{source}.metadata.labels", obj.get("labels"), default=())
    return CompositionMetadata(name=name, purpose=purpose, labels=tuple(sorted(set(labels))))


def _parse_byo_agents(raw: Any, *, source: str) -> Tuple[BYOAgent, ...]:
    if raw is None:
        return ()
    obj = _expect_mapping(f"{source}.byo_agents", raw)
    agents: list[BYOAgent] = []
    for agent_id in sorted(obj.keys(), key=str):
        aid = _expect_nonempty_str(f"{source}.byo_agents.<key>", agent_id)
        spec = _expect_mapping(f"{source}.byo_agents.{aid}", obj.get(agent_id))
        _require_keys(f"{source}.byo_agents.{aid}", spec, {"command"})
        _reject_unknown_keys(f"{source}.byo_agents.{aid}", spec, {"command", "cwd", "env"})

        command = _expect_nonempty_str(f"{source}.byo_agents.{aid}.command", spec.get("command"))
        cwd = _expect_optional_str(f"{source}.byo_agents.{aid}.cwd", spec.get("cwd"))

        env_raw = spec.get("env")
        env_items: Tuple[Tuple[str, str], ...] = ()
        if env_raw is not None:
            env_obj = _expect_mapping(f"{source}.byo_agents.{aid}.env", env_raw)
            env_pairs: list[Tuple[str, str]] = []
            for k, v in env_obj.items():
                ek = _expect_nonempty_str(f"{source}.byo_agents.{aid}.env.<key>", k)
                ev = _expect_nonempty_str(f"{source}.byo_agents.{aid}.env.{ek}", v)
                env_pairs.append((ek, ev))
            env_items = tuple(sorted(env_pairs, key=lambda x: x[0]))

        agents.append(BYOAgent(id=aid, command=command, cwd=cwd, env=env_items))

    return tuple(agents)


def _parse_members(raw: Any, *, source: str, byo_agent_ids: set[str]) -> Tuple[TeamMember, ...]:
    items = _expect_list(f"{source}.members", raw)
    if not items:
        raise TeamCompositionError(f"{source}.members: must include at least one member")

    members: list[TeamMember] = []
    seen_ids: set[str] = set()
    for idx, item in enumerate(items):
        path = f"{source}.members[{idx}]"
        obj = _expect_mapping(path, item)
        _require_keys(path, obj, {"id", "role", "lifecycle", "source", "agent"})
        _reject_unknown_keys(path, obj, {"id", "role", "lifecycle", "source", "agent", "harness"})

        member_id = _expect_nonempty_str(f"{path}.id", obj.get("id"))
        if member_id in seen_ids:
            raise TeamCompositionError(f"{path}.id: duplicate member id {member_id!r}")
        seen_ids.add(member_id)

        role = _expect_enum(f"{path}.role", obj.get("role"), _MEMBER_ROLES)
        lifecycle = _expect_enum(f"{path}.lifecycle", obj.get("lifecycle"), _MEMBER_LIFECYCLES)
        source_kind = _expect_enum(f"{path}.source", obj.get("source"), _MEMBER_SOURCES)
        agent = _expect_nonempty_str(f"{path}.agent", obj.get("agent"))
        harness = _expect_optional_enum(
            f"{path}.harness", obj.get("harness"), _HARNESS_VALUES, default=DEFAULT_HARNESS
        )

        if source_kind == "byo" and agent not in byo_agent_ids:
            available = ", ".join(sorted(byo_agent_ids)) if byo_agent_ids else "<none>"
            raise TeamCompositionError(
                f"{path}.agent: unknown BYO agent reference {agent!r}",
                hint=f"Define it under byo_agents. Available refs: {available}",
            )

        members.append(
            TeamMember(
                id=member_id,
                role=role,
                lifecycle=lifecycle,
                source=source_kind,
                agent=agent,
                harness=harness,
            )
        )

    return tuple(members)


def _parse_worktree_mappings(raw: Any, *, source: str, member_ids: set[str]) -> Tuple[WorktreeMapping, ...]:
    items = _expect_list(f"{source}.worktree_mappings", raw)
    if not items:
        raise TeamCompositionError(f"{source}.worktree_mappings: must include at least one mapping")

    mappings: list[WorktreeMapping] = []
    for idx, item in enumerate(items):
        path = f"{source}.worktree_mappings[{idx}]"
        obj = _expect_mapping(path, item)
        _require_keys(path, obj, {"pattern", "member"})
        _reject_unknown_keys(path, obj, {"pattern", "member"})

        pattern = _expect_nonempty_str(f"{path}.pattern", obj.get("pattern"))
        _validate_pattern(pattern, path=f"{path}.pattern")

        member = _expect_nonempty_str(f"{path}.member", obj.get("member"))
        if member not in member_ids:
            known = ", ".join(sorted(member_ids))
            raise TeamCompositionError(
                f"{path}.member: unknown member {member!r}",
                hint=f"Use one of: {known}",
            )

        mappings.append(WorktreeMapping(pattern=pattern, member=member))

    _reject_ambiguous_pattern_overlap(source=source, mappings=mappings)
    return tuple(mappings)


def _parse_communication(raw: Any, *, source: str) -> CommunicationPolicy:
    obj = _expect_mapping(f"{source}.communication", raw)
    _require_keys(f"{source}.communication", obj, {"channel", "require_ack", "escalation"})
    _reject_unknown_keys(f"{source}.communication", obj, {"channel", "require_ack", "escalation"})

    channel = _expect_enum(f"{source}.communication.channel", obj.get("channel"), _COMM_CHANNELS)
    require_ack = _expect_bool(f"{source}.communication.require_ack", obj.get("require_ack"))

    esc_obj = _expect_mapping(f"{source}.communication.escalation", obj.get("escalation"))
    _require_keys(
        f"{source}.communication.escalation",
        esc_obj,
        {"target_role", "timeout_seconds"},
    )
    _reject_unknown_keys(
        f"{source}.communication.escalation",
        esc_obj,
        {"target_role", "timeout_seconds", "max_retries"},
    )

    target_role = _expect_enum(
        f"{source}.communication.escalation.target_role",
        esc_obj.get("target_role"),
        _ESCALATION_TARGETS,
    )
    timeout_seconds = _expect_int(
        f"{source}.communication.escalation.timeout_seconds",
        esc_obj.get("timeout_seconds"),
        min_value=1,
    )
    max_retries = _expect_int(
        f"{source}.communication.escalation.max_retries",
        esc_obj.get("max_retries", 1),
        min_value=0,
    )

    return CommunicationPolicy(
        channel=channel,
        require_ack=require_ack,
        escalation=EscalationPolicy(
            target_role=target_role,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
        ),
    )


def _validate_pattern(pattern: str, *, path: str) -> None:
    wildcard_count = pattern.count("*")
    if wildcard_count == 0:
        return
    if wildcard_count > 1 or not pattern.endswith("*"):
        raise TeamCompositionError(
            f"{path}: invalid pattern {pattern!r}",
            hint=_PATTERN_HINT,
        )


def _reject_ambiguous_pattern_overlap(*, source: str, mappings: list[WorktreeMapping]) -> None:
    normalized: list[Tuple[WorktreeMapping, str, bool]] = []
    for item in mappings:
        wildcard = item.pattern.endswith("*")
        prefix = item.pattern[:-1] if wildcard else item.pattern
        normalized.append((item, prefix, wildcard))

    for idx, (left_item, left_prefix, left_wildcard) in enumerate(normalized):
        for right_item, right_prefix, right_wildcard in normalized[idx + 1 :]:
            if _patterns_overlap(left_prefix, left_wildcard, right_prefix, right_wildcard):
                raise TeamCompositionError(
                    (
                        f"{source}.worktree_mappings: ambiguous pattern overlap between "
                        f"{left_item.pattern!r} (member={left_item.member}) and "
                        f"{right_item.pattern!r} (member={right_item.member})"
                    ),
                    hint="Patterns must be disjoint. Prefer exact matches or non-overlapping prefixes.",
                )


def _patterns_overlap(left_prefix: str, left_wildcard: bool, right_prefix: str, right_wildcard: bool) -> bool:
    if left_wildcard and right_wildcard:
        return left_prefix.startswith(right_prefix) or right_prefix.startswith(left_prefix)
    if left_wildcard and not right_wildcard:
        return right_prefix.startswith(left_prefix)
    if not left_wildcard and right_wildcard:
        return left_prefix.startswith(right_prefix)
    return left_prefix == right_prefix


def _expect_mapping(path: str, raw: Any) -> Mapping[str, Any]:
    if not isinstance(raw, dict):
        raise TeamCompositionError(f"{path}: expected mapping/object")
    return raw


def _expect_list(path: str, raw: Any) -> list[Any]:
    if not isinstance(raw, list):
        raise TeamCompositionError(f"{path}: expected list")
    return raw


def _expect_nonempty_str(path: str, raw: Any) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise TeamCompositionError(f"{path}: expected non-empty string")
    return raw.strip()


def _expect_optional_str(path: str, raw: Any) -> str:
    if raw is None:
        return ""
    return _expect_nonempty_str(path, raw)


def _expect_bool(path: str, raw: Any) -> bool:
    if not isinstance(raw, bool):
        raise TeamCompositionError(f"{path}: expected boolean")
    return raw


def _expect_int(path: str, raw: Any, *, min_value: int | None = None) -> int:
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise TeamCompositionError(f"{path}: expected integer")
    if min_value is not None and raw < min_value:
        raise TeamCompositionError(f"{path}: expected integer >= {min_value}")
    return raw


def _expect_enum(path: str, raw: Any, allowed: set[str]) -> str:
    value = _expect_nonempty_str(path, raw)
    if value not in allowed:
        opts = ", ".join(sorted(allowed))
        raise TeamCompositionError(f"{path}: invalid value {value!r}; expected one of: {opts}")
    return value


def _expect_optional_enum(path: str, raw: Any, allowed: set[str], *, default: str) -> str:
    if raw is None:
        return default
    return _expect_enum(path, raw, allowed)


def _expect_str_list(path: str, raw: Any, *, default: Tuple[str, ...]) -> list[str]:
    if raw is None:
        return list(default)
    items = _expect_list(path, raw)
    out: list[str] = []
    for idx, item in enumerate(items):
        out.append(_expect_nonempty_str(f"{path}[{idx}]", item))
    return out


def _require_keys(path: str, obj: Mapping[str, Any], required: set[str]) -> None:
    missing = sorted(k for k in required if k not in obj)
    if missing:
        raise TeamCompositionError(f"{path}: missing required key(s): {', '.join(missing)}")


def _reject_unknown_keys(path: str, obj: Mapping[str, Any], allowed: set[str]) -> None:
    unknown = sorted(str(k) for k in obj.keys() if str(k) not in allowed)
    if unknown:
        allowed_s = ", ".join(sorted(allowed))
        raise TeamCompositionError(
            f"{path}: unknown key(s): {', '.join(unknown)}",
            hint=f"Allowed keys: {allowed_s}",
        )


__all__ = [
    "BYOAgent",
    "CommunicationPolicy",
    "CompositionMetadata",
    "EscalationPolicy",
    "SCHEMA_VERSION",
    "TeamComposition",
    "TeamCompositionError",
    "TeamMember",
    "WorktreeMapping",
    "load_team_composition_yaml",
    "parse_team_composition_yaml",
]
