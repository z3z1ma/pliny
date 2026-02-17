from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_loom.team.team_config import (
    TeamConfigError,
    default_liveness_spec,
    default_team_config_spec,
    load_team_config_yaml,
    normalize_team_config_spec,
)


class TestTeamConfigSchema(unittest.TestCase):
    def test_defaults_are_stable(self) -> None:
        spec = default_team_config_spec()
        self.assertEqual(str(spec.get("worker", {}).get("subagents") or ""), "encouraged")
        self.assertEqual(
            int(spec.get("liveness", {}).get("heartbeat_interval_s") or 0),
            int(default_liveness_spec()["heartbeat_interval_s"]),
        )

    def test_normalize_valid_full_config(self) -> None:
        spec = normalize_team_config_spec(
            {
                "harness": "CoDeX",
                "model": "gpt-5-codex",
                "role_prompts": {
                    "append": {
                        "manager": "Do concise check-ins.",
                        "worker": "Use subagents for research.",
                    }
                },
                "worker": {"subagents": "encouraged"},
                "liveness": {
                    "heartbeat_interval_s": 15,
                    "stale_after_s": 90,
                    "dead_after_s": 240,
                    "recovery_cooldown_s": 180,
                    "max_recoveries_per_hour": 4,
                },
            }
        )
        self.assertEqual(str(spec.get("harness") or ""), "codex")
        self.assertEqual(str(spec.get("model") or ""), "gpt-5-codex")
        self.assertEqual(
            str(spec.get("role_prompts", {}).get("append", {}).get("manager") or ""),
            "Do concise check-ins.",
        )
        self.assertEqual(
            str(spec.get("role_prompts", {}).get("append", {}).get("worker") or ""),
            "Use subagents for research.",
        )

    def test_unknown_top_level_key_is_rejected(self) -> None:
        with self.assertRaises(TeamConfigError) as ctx:
            normalize_team_config_spec({"unknown": 1})
        self.assertIn("unknown key(s): unknown", str(ctx.exception))

    def test_invalid_harness_value_is_rejected(self) -> None:
        with self.assertRaises(TeamConfigError) as ctx:
            normalize_team_config_spec({"harness": "bad-harness"})
        self.assertIn("team_config.harness", str(ctx.exception))

    def test_invalid_worker_subagents_value_is_rejected(self) -> None:
        with self.assertRaises(TeamConfigError) as ctx:
            normalize_team_config_spec({"worker": {"subagents": "disabled"}})
        self.assertIn("worker.subagents", str(ctx.exception))

    def test_liveness_requires_stale_less_than_dead(self) -> None:
        with self.assertRaises(TeamConfigError) as ctx:
            normalize_team_config_spec(
                {"liveness": {"stale_after_s": 300, "dead_after_s": 200}}
            )
        self.assertIn("stale_after_s must be < dead_after_s", str(ctx.exception))

    def test_load_yaml_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "team-config.yaml"
            p.write_text(
                """
model: gpt-5-codex
worker:
  subagents: encouraged
liveness:
  heartbeat_interval_s: 12
""".strip()
                + "\n",
                encoding="utf-8",
            )
            data = load_team_config_yaml(p)

        self.assertTrue(str(data.get("source") or "").endswith("team-config.yaml"))
        spec = dict(data.get("spec") or {})
        self.assertEqual(str(spec.get("model") or ""), "gpt-5-codex")
        self.assertEqual(
            int(spec.get("liveness", {}).get("heartbeat_interval_s") or 0), 12
        )


if __name__ == "__main__":
    unittest.main()
