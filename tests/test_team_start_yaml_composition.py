import json
import subprocess
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team
from agent_loom.team.team_config import TeamConfigError


def _fake_tmux_cmd(argv, **kwargs):
    _ = kwargs
    return subprocess.CompletedProcess(list(argv), 0, stdout="", stderr="")


@contextmanager
def _patched_team_start(repo_root: Path):
    with (
        mock.patch.object(team, "canonical_repo_root", return_value=repo_root),
        mock.patch.object(team, "_require_bin"),
        mock.patch.object(team, "_deny_if_role_set"),
        mock.patch.object(team, "tmux_has_session", return_value=False),
        mock.patch.object(team, "tmux_cmd", side_effect=_fake_tmux_cmd),
        mock.patch.object(team, "tmux_set_option"),
        mock.patch.object(team, "tmux_window_exists", return_value=False),
        mock.patch.object(team, "tmux_mark_pane"),
        mock.patch.object(team, "tmux_format", return_value="%1"),
    ):
        yield


class TestTeamStartYamlConfig(unittest.TestCase):
    def test_missing_config_file_fails_fast(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            missing_path = repo_root / "missing-config.yaml"
            with _patched_team_start(repo_root):
                team.init_agents(repo=repo_root, create_missing=True)
                with self.assertRaises(TeamConfigError) as ctx:
                    team.start(team="MiyagiDo", repo=repo_root, config=str(missing_path))

            self.assertIn("Unable to read team config file", str(ctx.exception))

    def test_invalid_yaml_fails_fast(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            config_path = repo_root / "team-config.yaml"
            config_path.write_text("harness: [1", encoding="utf-8")

            with _patched_team_start(repo_root):
                team.init_agents(repo=repo_root, create_missing=True)
                with self.assertRaises(TeamConfigError) as ctx:
                    team.start(team="MiyagiDo", repo=repo_root, config=str(config_path))

            self.assertIn("invalid YAML", str(ctx.exception))

    def test_valid_config_persists_and_survives_resume_without_override(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            config_path = repo_root / "team-config.yaml"
            config_path.write_text(
                """
harness: codex
model: gpt-5-codex
worker:
  subagents: encouraged
""".strip()
                + "\n",
                encoding="utf-8",
            )

            with _patched_team_start(repo_root):
                team.init_agents(repo=repo_root, create_missing=True)
                start_res = team.start(
                    team="MiyagiDo",
                    repo=repo_root,
                    config=str(config_path),
                )

                run_path = Path(start_res.run_dir) / "run.json"
                first_run = json.loads(run_path.read_text(encoding="utf-8"))
                self.assertEqual(str(first_run.get("harness") or ""), "codex")
                self.assertIn("team_config", first_run)
                self.assertEqual(
                    str(
                        (((first_run.get("team_config") or {}).get("spec") or {}).get("model") or "")
                    ),
                    "gpt-5-codex",
                )

                config_path.write_text(
                    """
harness: opencode
model: stale-should-not-apply
""".strip()
                    + "\n",
                    encoding="utf-8",
                )

                team.start(team="MiyagiDo", repo=repo_root)
                second_run = json.loads(run_path.read_text(encoding="utf-8"))
                self.assertEqual(
                    str(
                        (((second_run.get("team_config") or {}).get("spec") or {}).get("model") or "")
                    ),
                    "gpt-5-codex",
                )

                with mock.patch.object(
                    team,
                    "_paths_for",
                    return_value=team.RunPaths(repo_root=repo_root, team="MiyagiDo"),
                ):
                    status_res = team.status(team="MiyagiDo", repo=repo_root)
                self.assertEqual(
                    str(status_res.team_config.get("model") or ""),
                    "gpt-5-codex",
                )


if __name__ == "__main__":
    unittest.main()
