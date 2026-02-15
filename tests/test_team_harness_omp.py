import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team


class _FakeProc:
    def __init__(self, pid: int = 999) -> None:
        self.pid = pid
        self._done = False

    def poll(self):
        return 0 if self._done else None

    def wait(self):
        self._done = True
        return 0

    def send_signal(self, _sig):
        self._done = True

    def terminate(self):
        self._done = True

    def kill(self):
        self._done = True


class _NoopThread:
    def __init__(self, target=None, daemon=None):
        self.target = target
        self.daemon = daemon

    def start(self) -> None:
        return


class TestTeamHarnessOmp(unittest.TestCase):
    def test_normalize_harness_accepts_omp(self) -> None:
        self.assertEqual(team._normalize_harness("omp"), "omp")

    def test_extract_prompt_from_agent_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "agent.md"
            p.write_text(
                "\n".join(
                    [
                        "---",
                        "name: test-agent",
                        "description: sample",
                        "---",
                        "# Agent",
                        team.TEAM_AGENT_PROMPT_BEGIN,
                        "SYSTEM SECTION",
                        team.TEAM_AGENT_PROMPT_END,
                        "MANUAL NOTE",
                    ]
                ),
                encoding="utf-8",
            )
            prompt = team._extract_prompt_from_agent_file(p)
            self.assertTrue(prompt)
            self.assertIn("SYSTEM SECTION", prompt)
            self.assertIn("MANUAL NOTE", prompt)
            self.assertNotIn(team.TEAM_AGENT_PROMPT_BEGIN, prompt)
            self.assertNotIn(team.TEAM_AGENT_PROMPT_END, prompt)

    def test_tui_omp_spawns_with_append_prompt_resume_and_tools(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            run_dir = repo_root / ".loom" / "team" / "runs" / "cobra"
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "run.json").write_text("{}", encoding="utf-8")

            agent_dir = repo_root / ".opencode" / "agents"
            agent_dir.mkdir(parents=True, exist_ok=True)
            (agent_dir / f"{team.DEFAULT_MANAGER_AGENT}.md").write_text(
                "\n".join(
                    [
                        "---",
                        "name: loom-team-manager",
                        "description: manager",
                        "---",
                        team.TEAM_AGENT_PROMPT_BEGIN,
                        "SYSTEM PROMPT BODY",
                        team.TEAM_AGENT_PROMPT_END,
                        "LOCAL NOTE",
                    ]
                ),
                encoding="utf-8",
            )

            run = {"run_id": "run-123", "team": "cobra"}
            popen_argv: list[list[str]] = []

            def fake_popen(argv, **kwargs):
                _ = kwargs
                popen_argv.append(list(argv))
                return _FakeProc(pid=4321)

            env = {
                "TMUX_PANE": "%1",
                team.ENV_TEAM_NAME: "cobra",
                team.ENV_TEAM_RUN_DIR: str(run_dir),
                team.ENV_TEAM_ROLE: team.ROLE_MANAGER,
                team.ENV_TEAM_WORKER_ID: "",
            }
            old_env = os.environ.copy()
            os.environ.update(env)
            try:
                with (
                    mock.patch.object(team, "load_run", return_value=run),
                    mock.patch.object(team, "_require_bin"),
                    mock.patch.object(team, "safe_write_event"),
                    mock.patch.object(team, "tmux_signal"),
                    mock.patch("agent_loom.team.core.threading.Thread", _NoopThread),
                    mock.patch("agent_loom.team.core.subprocess.Popen", side_effect=fake_popen),
                ):
                    result = team.tui(
                        project_dir=repo_root,
                        harness="omp",
                        agent=team.DEFAULT_MANAGER_AGENT,
                        model="opus",
                        prompt="initial prompt",
                        respawn_cap=1,
                    )
            finally:
                os.environ.clear()
                os.environ.update(old_env)

            self.assertEqual(result.exit_reason, "respawn_cap")
            self.assertTrue(popen_argv)
            argv = popen_argv[0]
            self.assertEqual(argv[0], "omp")
            self.assertIn("--append-system-prompt", argv)
            self.assertIn("--resume", argv)
            self.assertIn("--tools", argv)
            self.assertIn("initial prompt", argv)
            resume_arg = argv[argv.index("--resume") + 1]
            self.assertEqual(
                str(Path(resume_arg).resolve()),
                str((run_dir / "sessions" / "omp" / "manager.jsonl").resolve()),
            )
            tools_arg = argv[argv.index("--tools") + 1]
            tools = tools_arg.split(",")
            self.assertIn("read", tools)
            self.assertNotIn("write", tools)

    def test_start_persists_omp_harness_config(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)

            def fake_tmux_cmd(argv, **kwargs):
                _ = kwargs
                return subprocess.CompletedProcess(list(argv), 0, stdout="", stderr="")

            with (
                mock.patch.object(team, "canonical_repo_root", return_value=repo_root),
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "tmux_has_session", return_value=False),
                mock.patch.object(team, "tmux_cmd", side_effect=fake_tmux_cmd),
                mock.patch.object(team, "tmux_set_option"),
                mock.patch.object(team, "tmux_window_exists", return_value=False),
                mock.patch.object(team, "tmux_mark_pane"),
                mock.patch.object(team, "tmux_format", return_value="%1"),
            ):
                team.init_agents(repo=repo_root, create_missing=True)
                res = team.start(team="Cobra", repo=repo_root, harness="omp")

            run_path = Path(res.run_dir) / "run.json"
            run = json.loads(run_path.read_text(encoding="utf-8"))
            self.assertEqual(str(run.get("harness") or ""), "omp")
            self.assertIn("omp", run)
            omp_cfg = dict(run.get("omp") or {})
            self.assertIn("model", omp_cfg)
            self.assertIn("models", omp_cfg)
            self.assertEqual(str(omp_cfg.get("manager_agent") or ""), team.DEFAULT_MANAGER_AGENT)

    def test_model_for_role_worker_with_omp_harness(self) -> None:
        """Test that _model_for_role correctly resolves worker model for OMP harness.

        This regression test captures the expected behavior:
        - When harness="omp" and role="worker"
        - With run.omp.models.worker set to a specific model
        - _model_for_role should return run.omp.models.worker (not run.omp.model)
        """
        run = {
            "harness": "omp",
            "omp": {
                "model": "github-copilot/claude-sonnet-4.5",
                "models": {
                    "worker": "github-copilot/claude-sonnet-4.5",
                    "investigator": "openai-codex/gpt-5.3-codex",
                    "manager": "github-copilot/gemini-3-flash-preview",
                    "integrator": "github-copilot/claude-sonnet-4.5",
                },
            },
        }
        model = team._model_for_role(run, "worker", harness="omp")
        self.assertEqual(model, "github-copilot/claude-sonnet-4.5")

    def test_model_for_role_fallback_to_harness_model(self) -> None:
        """Test that _model_for_role falls back to harness.model when role model is empty."""
        run = {
            "harness": "omp",
            "omp": {
                "model": "github-copilot/claude-sonnet-4.5",
                "models": {
                    "worker": "",  # Empty worker model
                    "manager": "github-copilot/gemini-3-flash-preview",
                },
            },
        }
        model = team._model_for_role(run, "worker", harness="omp")
        # Should fall back to run.omp.model
        self.assertEqual(model, "github-copilot/claude-sonnet-4.5")

    def test_model_for_role_precedence_role_over_harness(self) -> None:
        """Test that role-specific model takes precedence over harness-level model."""
        run = {
            "harness": "omp",
            "omp": {
                "model": "github-copilot/claude-sonnet-4.5",
                "models": {
                    "worker": "openai-codex/gpt-5.3-codex",  # Different from harness model
                },
            },
        }
        model = team._model_for_role(run, "worker", harness="omp")
        # Should use role-specific model, not harness-level
        self.assertEqual(model, "openai-codex/gpt-5.3-codex")


if __name__ == "__main__":
    unittest.main()
