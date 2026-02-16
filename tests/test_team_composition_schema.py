from __future__ import annotations

import unittest
from pathlib import Path

from agent_loom.team.composition import (
    SCHEMA_VERSION,
    TeamCompositionError,
    load_team_roster_yaml,
    parse_team_roster_yaml,
)

_FIXTURE_DIR = Path(__file__).parent / "fixtures" / "team_composition"


def _fixture_text(name: str) -> str:
    return (_FIXTURE_DIR / name).read_text(encoding="utf-8")


class TestTeamRosterSchema(unittest.TestCase):
    def test_load_minimal_fixture(self) -> None:
        roster = load_team_roster_yaml(_FIXTURE_DIR / "valid_minimal.yaml")
        data = roster.as_dict()

        self.assertEqual(data["version"], SCHEMA_VERSION)
        self.assertEqual(data["metadata"]["name"], "YAML Sprint Foundations")
        self.assertEqual(
            list(data["builtins"].keys()),
            ["manager", "architect", "worker", "integrator"],
        )
        self.assertEqual(data["builtins"]["worker"]["harness"], "codex")
        self.assertNotIn("members", data)
        self.assertNotIn("communication", data)

    def test_parse_unsorted_fixture_is_deterministically_normalized(self) -> None:
        roster = parse_team_roster_yaml(_fixture_text("valid_unsorted.yaml"), source="fixture")
        data = roster.as_dict()

        self.assertEqual(data["metadata"]["labels"], ["a", "b"])
        self.assertEqual(data["mounts"], [".venv"])
        self.assertEqual([m["id"] for m in data["members"]], ["designer", "ux"])
        self.assertEqual(data["builtins"]["worker"]["model"], "gpt-5-codex")
        self.assertEqual(
            data["communication"]["routes"],
            [{"from_role": "reviewer", "to": ["manager", "role:architect"]}],
        )

    def test_unknown_top_level_key_fails_fast_with_hint(self) -> None:
        with self.assertRaises(TeamCompositionError) as ctx:
            parse_team_roster_yaml(_fixture_text("invalid_unknown_key.yaml"), source="fixture")

        self.assertIn("unknown key(s): unexpected_section", str(ctx.exception))
        self.assertIn("Allowed keys", ctx.exception.hint)

    def test_invalid_enum_fails_fast(self) -> None:
        with self.assertRaises(TeamCompositionError) as ctx:
            parse_team_roster_yaml(_fixture_text("invalid_enum.yaml"), source="fixture")

        self.assertIn("members[0].always_on", str(ctx.exception))
        self.assertIn("expected boolean", str(ctx.exception))

    def test_builtin_extra_keys_are_rejected(self) -> None:
        with self.assertRaises(TeamCompositionError) as ctx:
            parse_team_roster_yaml(
                _fixture_text("invalid_ambiguous_mapping.yaml"),
                source="fixture",
            )

        self.assertIn("builtins.manager", str(ctx.exception))
        self.assertIn("unknown key(s): lifecycle", str(ctx.exception))

    def test_malformed_yaml_reports_source_context(self) -> None:
        payload = "version: [1"
        with self.assertRaises(TeamCompositionError) as ctx:
            parse_team_roster_yaml(payload, source="fixture")

        self.assertIn("fixture: invalid YAML", str(ctx.exception))

    def test_member_worktree_key_is_rejected(self) -> None:
        payload = """
version: 3
builtins:
  manager:
    harness: opencode
    agent: loom-team-manager
  architect:
    harness: opencode
    agent: loom-team-architect
  worker:
    harness: codex
    agent: loom-team-worker
  integrator:
    harness: claude
    agent: loom-team-integrator
members:
  - id: designer
    role: designer
    harness: codex
    agent: loom-team-worker
    always_on: true
    workspace: worktree
    worktree_key: design-hub
"""
        with self.assertRaises(TeamCompositionError) as ctx:
            parse_team_roster_yaml(payload, source="inline")

        self.assertIn("members[0]", str(ctx.exception))
        self.assertIn("unknown key(s): worktree_key", str(ctx.exception))

    def test_builtin_route_override_is_rejected(self) -> None:
        payload = """
version: 3
builtins:
  manager:
    harness: opencode
    agent: loom-team-manager
  architect:
    harness: opencode
    agent: loom-team-architect
  worker:
    harness: codex
    agent: loom-team-worker
  integrator:
    harness: claude
    agent: loom-team-integrator
communication:
  routes:
    - from_role: manager
      to:
        - all
"""
        with self.assertRaises(TeamCompositionError) as ctx:
            parse_team_roster_yaml(payload, source="inline")

        self.assertIn("built-in route overrides are not allowed", str(ctx.exception))

    def test_v2_schema_is_rejected(self) -> None:
        payload = """
version: 2
builtins: {}
"""
        with self.assertRaises(TeamCompositionError) as ctx:
            parse_team_roster_yaml(payload, source="inline")

        self.assertIn("unsupported schema version 2", str(ctx.exception))
        self.assertIn("Use version: 3", ctx.exception.hint)


if __name__ == "__main__":
    unittest.main()
