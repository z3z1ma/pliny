from __future__ import annotations

import unittest
from pathlib import Path

from agent_loom.team.composition import (
    SCHEMA_VERSION,
    TeamCompositionError,
    load_team_composition_yaml,
    parse_team_composition_yaml,
)


_FIXTURE_DIR = Path(__file__).parent / "fixtures" / "team_composition"


def _fixture_text(name: str) -> str:
    return (_FIXTURE_DIR / name).read_text(encoding="utf-8")


class TestTeamCompositionSchema(unittest.TestCase):
    def test_load_minimal_fixture(self) -> None:
        composition = load_team_composition_yaml(_FIXTURE_DIR / "valid_minimal.yaml")
        data = composition.as_dict()

        self.assertEqual(data["version"], SCHEMA_VERSION)
        self.assertEqual(data["metadata"]["name"], "YAML Sprint Foundations")
        self.assertEqual([m["id"] for m in data["members"]], ["manager", "worker-template"])
        self.assertEqual(data["members"][0]["harness"], "opencode")
        self.assertEqual(
            data["worktree_mappings"],
            [
                {"pattern": "al-aec3", "member": "worker-template"},
                {"pattern": "mgr/*", "member": "manager"},
            ],
        )

    def test_parse_unsorted_fixture_is_deterministically_normalized(self) -> None:
        composition = parse_team_composition_yaml(_fixture_text("valid_unsorted.yaml"), source="fixture")
        data = composition.as_dict()

        self.assertEqual(data["metadata"]["labels"], ["a", "b"])
        self.assertEqual([m["id"] for m in data["members"]], ["manager", "worker-template"])
        self.assertEqual(data["byo_agents"]["codex-worker"]["env"], {"A": "1", "B": "2"})
        self.assertEqual(
            data["worktree_mappings"],
            [
                {"pattern": "al-z*", "member": "worker-template"},
                {"pattern": "mgr/main", "member": "manager"},
            ],
        )

    def test_unknown_top_level_key_fails_fast_with_hint(self) -> None:
        with self.assertRaises(TeamCompositionError) as ctx:
            parse_team_composition_yaml(_fixture_text("invalid_unknown_key.yaml"), source="fixture")

        self.assertIn("unknown key(s): unexpected_section", str(ctx.exception))
        self.assertIn("Allowed keys", ctx.exception.hint)

    def test_invalid_enum_fails_fast(self) -> None:
        with self.assertRaises(TeamCompositionError) as ctx:
            parse_team_composition_yaml(_fixture_text("invalid_enum.yaml"), source="fixture")

        self.assertIn("members[0].lifecycle", str(ctx.exception))
        self.assertIn("expected one of", str(ctx.exception))

    def test_ambiguous_mapping_patterns_are_rejected(self) -> None:
        with self.assertRaises(TeamCompositionError) as ctx:
            parse_team_composition_yaml(
                _fixture_text("invalid_ambiguous_mapping.yaml"),
                source="fixture",
            )

        self.assertIn("ambiguous pattern overlap", str(ctx.exception))
        self.assertIn("Patterns must be disjoint", ctx.exception.hint)

    def test_unknown_byo_agent_reference_is_rejected(self) -> None:
        payload = """
version: 1
metadata:
  name: x
members:
  - id: worker-1
    role: worker
    lifecycle: ephemeral
    source: byo
    agent: missing-ref
worktree_mappings:
  - pattern: "*"
    member: worker-1
communication:
  channel: inbox_only
  require_ack: true
  escalation:
    target_role: manager
    timeout_seconds: 60
"""
        with self.assertRaises(TeamCompositionError) as ctx:
            parse_team_composition_yaml(payload, source="inline")

        self.assertIn("unknown BYO agent reference", str(ctx.exception))
        self.assertIn("Define it under byo_agents", ctx.exception.hint)


if __name__ == "__main__":
    unittest.main()
