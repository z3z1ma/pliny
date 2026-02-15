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
            fake_model_check = subprocess.CompletedProcess(
                args=["omp", "--list-models", "opus"],
                returncode=0,
                stdout="opus (provider)\n",
                stderr="",
            )
            old_env = os.environ.copy()
            os.environ.update(env)
            try:

                with (
                    mock.patch.object(team, "load_run", return_value=run),
                    mock.patch.object(team, "_require_bin"),
                    mock.patch.object(team, "safe_write_event"),
                    mock.patch.object(team, "tmux_signal"),
                    mock.patch.object(team, "_run", return_value=fake_model_check),
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

            env_backup = os.environ.copy()
            # Clear team role to simulate running from outside team pane
            os.environ.pop(team.ENV_TEAM_ROLE, None)
            try:
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

            finally:
                os.environ.clear()
                os.environ.update(env_backup)
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

    def test_omp_model_available_success(self) -> None:
        """Test that _omp_model_available returns True for available models."""
        fake_proc = subprocess.CompletedProcess(
            args=["omp", "--list-models", "valid-model"],
            returncode=0,
            stdout="valid-model (provider)\n",
            stderr="",
        )
        with mock.patch.object(team, "_run", return_value=fake_proc):
            available, error_msg = team._omp_model_available("omp", "valid-model")
            self.assertTrue(available)
            self.assertEqual(error_msg, "")

    def test_omp_model_available_not_found(self) -> None:
        """Test that _omp_model_available returns False for unavailable models."""
        fake_proc = subprocess.CompletedProcess(
            args=["omp", "--list-models", "invalid-model"],
            returncode=0,
            stdout="No models matching 'invalid-model'\n",
            stderr="",
        )
        with mock.patch.object(team, "_run", return_value=fake_proc):
            available, error_msg = team._omp_model_available("omp", "invalid-model")
            self.assertFalse(available)
            self.assertIn("not found", error_msg)

    def test_omp_model_available_empty_model(self) -> None:
        """Test that _omp_model_available returns False for empty model string."""
        available, error_msg = team._omp_model_available("omp", "")
        self.assertFalse(available)
        self.assertIn("empty", error_msg)

    def test_omp_model_available_command_failure(self) -> None:
        """Test that _omp_model_available handles provider failures gracefully."""
        fake_proc = subprocess.CompletedProcess(
            args=["omp", "--list-models", "some-model"],
            returncode=1,
            stdout="",
            stderr="Provider authentication failed\n",
        )
        with mock.patch.object(team, "_run", return_value=fake_proc):
            available, error_msg = team._omp_model_available("omp", "some-model")
            self.assertFalse(available)
            self.assertIn("failed", error_msg)

    def test_omp_model_available_exception_handling(self) -> None:
        """Test that _omp_model_available returns True on exception to avoid blocking valid setups."""
        def raise_exception(*_args: object, **_kwargs: object) -> None:
            raise RuntimeError("Network timeout")

        with mock.patch.object(team, "_run", side_effect=raise_exception):
            available, error_msg = team._omp_model_available("omp", "test-model")
            self.assertTrue(available)  # Should not block on exception
            self.assertIn("preflight check failed", error_msg)

    def test_tui_omp_invalid_model_fails_fast(self) -> None:
        """Test that tui() exits with model_invalid when OMP model is unavailable."""
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            run_dir = repo_root / ".loom" / "team" / "runs" / "test"
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "run.json").write_text('{"run_id": "test-123"}', encoding="utf-8")

            agent_dir = repo_root / ".opencode" / "agents"
            agent_dir.mkdir(parents=True, exist_ok=True)
            (agent_dir / f"{team.DEFAULT_WORKER_AGENT}.md").write_text(
                "\n".join(
                    [
                        "---",
                        "name: loom-team-worker",
                        "description: worker",
                        "---",
                        team.TEAM_AGENT_PROMPT_BEGIN,
                        "SYSTEM PROMPT",
                        team.TEAM_AGENT_PROMPT_END,
                    ]
                ),
                encoding="utf-8",
            )

            run = {"run_id": "test-123", "team": "test"}
            fake_model_check = subprocess.CompletedProcess(
                args=["omp", "--list-models", "invalid-model"],
                returncode=0,
                stdout="No models matching 'invalid-model'\n",
                stderr="",
            )

            env = {
                "TMUX_PANE": "%1",
                team.ENV_TEAM_NAME: "test",
                team.ENV_TEAM_RUN_DIR: str(run_dir),
                team.ENV_TEAM_ROLE: team.ROLE_WORKER,
                team.ENV_TEAM_WORKER_ID: "w1",
            }
            old_env = os.environ.copy()
            os.environ.update(env)
            try:
                with (
                    mock.patch.object(team, "load_run", return_value=run),
                    mock.patch.object(team, "_require_bin"),
                    mock.patch.object(team, "safe_write_event"),
                    mock.patch.object(team, "_run", return_value=fake_model_check),
                    mock.patch.object(team, "_inbox_write_and_maybe_nudge"),
                    mock.patch("agent_loom.team.core.threading.Thread", _NoopThread),
                ):
                    result = team.tui(
                        project_dir=repo_root,
                        harness="omp",
                        agent=team.DEFAULT_WORKER_AGENT,
                        model="invalid-model",
                        prompt="test",
                        respawn_cap=1,
                    )
            finally:
                os.environ.clear()
                os.environ.update(old_env)

            self.assertEqual(result.exit_reason, "model_invalid")

    def test_tui_omp_valid_model_spawns(self) -> None:
        """Test that tui() spawns normally when OMP model is valid."""
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            run_dir = repo_root / ".loom" / "team" / "runs" / "test"
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "run.json").write_text('{"run_id": "test-123"}', encoding="utf-8")

            agent_dir = repo_root / ".opencode" / "agents"
            agent_dir.mkdir(parents=True, exist_ok=True)
            (agent_dir / f"{team.DEFAULT_WORKER_AGENT}.md").write_text(
                "\n".join(
                    [
                        "---",
                        "name: loom-team-worker",
                        "description: worker",
                        "---",
                        team.TEAM_AGENT_PROMPT_BEGIN,
                        "SYSTEM PROMPT",
                        team.TEAM_AGENT_PROMPT_END,
                    ]
                ),
                encoding="utf-8",
            )

            run = {"run_id": "test-123", "team": "test"}
            fake_model_check = subprocess.CompletedProcess(
                args=["omp", "--list-models", "valid-model"],
                returncode=0,
                stdout="valid-model (provider)\n",
                stderr="",
            )
            popen_called = []

            def fake_popen(argv, **kwargs):
                _ = kwargs
                popen_called.append(list(argv))
                return _FakeProc(pid=1234)

            env = {
                "TMUX_PANE": "%1",
                team.ENV_TEAM_NAME: "test",
                team.ENV_TEAM_RUN_DIR: str(run_dir),
                team.ENV_TEAM_ROLE: team.ROLE_WORKER,
                team.ENV_TEAM_WORKER_ID: "w1",
            }
            old_env = os.environ.copy()
            os.environ.update(env)
            try:
                with (
                    mock.patch.object(team, "load_run", return_value=run),
                    mock.patch.object(team, "_require_bin"),
                    mock.patch.object(team, "safe_write_event"),
                    mock.patch.object(team, "tmux_signal"),
                    mock.patch.object(team, "_run", return_value=fake_model_check),
                    mock.patch("agent_loom.team.core.threading.Thread", _NoopThread),
                    mock.patch("agent_loom.team.core.subprocess.Popen", side_effect=fake_popen),
                ):
                    result = team.tui(
                        project_dir=repo_root,
                        harness="omp",
                        agent=team.DEFAULT_WORKER_AGENT,
                        model="valid-model",
                        prompt="test",
                        respawn_cap=1,
                    )
            finally:
                os.environ.clear()
                os.environ.update(old_env)

            # Should hit respawn cap (normal flow), not model_invalid
            self.assertEqual(result.exit_reason, "respawn_cap")
            # Popen should have been called
            self.assertTrue(popen_called)

    def test_start_rejects_invalid_omp_worker_model(self) -> None:
        """Test that start() fails fast when OMP worker model is invalid."""
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)

            def fake_tmux_cmd(argv, **kwargs):
                _ = kwargs
                return subprocess.CompletedProcess(list(argv), 0, stdout="", stderr="")

            fake_model_check = subprocess.CompletedProcess(
                args=["omp", "--list-models", "invalid-worker-model"],
                returncode=0,
                stdout="No models matching 'invalid-worker-model'\n",
                stderr="",
            )

            env_backup = os.environ.copy()
            os.environ.pop(team.ENV_TEAM_ROLE, None)
            try:
                with (
                    mock.patch.object(team, "canonical_repo_root", return_value=repo_root),
                    mock.patch.object(team, "_require_bin"),
                    mock.patch.object(team, "tmux_has_session", return_value=False),
                    mock.patch.object(team, "tmux_cmd", side_effect=fake_tmux_cmd),
                    mock.patch.object(team, "tmux_set_option"),
                    mock.patch.object(team, "tmux_window_exists", return_value=False),
                    mock.patch.object(team, "tmux_mark_pane"),
                    mock.patch.object(team, "tmux_format", return_value="%1"),
                    mock.patch.object(team, "_run", return_value=fake_model_check),
                ):
                    team.init_agents(repo=repo_root, create_missing=True)
                    with self.assertRaises(team.TeamError) as ctx:
                        team.start(
                            team="Cobra",
                            repo=repo_root,
                            harness="omp",
                            worker_model="invalid-worker-model",
                        )
                    self.assertIn("OMP model invalid", str(ctx.exception))
                    self.assertIn("worker", str(ctx.exception))
            finally:
                os.environ.clear()
                os.environ.update(env_backup)

    def test_start_accepts_valid_omp_model(self) -> None:
        """Test that start() succeeds when OMP model is valid."""
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)

            def fake_tmux_cmd(argv, **kwargs):
                _ = kwargs
                return subprocess.CompletedProcess(list(argv), 0, stdout="", stderr="")

            fake_model_check = subprocess.CompletedProcess(
                args=["omp", "--list-models", "valid-model"],
                returncode=0,
                stdout="valid-model (provider)\n",
                stderr="",
            )

            env_backup = os.environ.copy()
            os.environ.pop(team.ENV_TEAM_ROLE, None)
            try:
                with (
                    mock.patch.object(team, "canonical_repo_root", return_value=repo_root),
                    mock.patch.object(team, "_require_bin"),
                    mock.patch.object(team, "tmux_has_session", return_value=False),
                    mock.patch.object(team, "tmux_cmd", side_effect=fake_tmux_cmd),
                    mock.patch.object(team, "tmux_set_option"),
                    mock.patch.object(team, "tmux_window_exists", return_value=False),
                    mock.patch.object(team, "tmux_mark_pane"),
                    mock.patch.object(team, "tmux_format", return_value="%1"),
                    mock.patch.object(team, "_run", return_value=fake_model_check),
                ):
                    team.init_agents(repo=repo_root, create_missing=True)
                    res = team.start(
                        team="Cobra",
                        repo=repo_root,
                        harness="omp",
                        worker_model="valid-model",
                    )
                    # Should succeed without raising
                    run_path = Path(res.run_dir) / "run.json"
                    run = json.loads(run_path.read_text(encoding="utf-8"))
                    self.assertEqual(str(run.get("harness") or ""), "omp")
                    omp_cfg = dict(run.get("omp") or {})
                    models = dict(omp_cfg.get("models") or {})
                    self.assertEqual(models.get("worker"), "valid-model")
            finally:
                os.environ.clear()
                os.environ.update(env_backup)

    def test_start_ignores_invalid_model_for_non_omp_harness(self) -> None:
        """Test that start() does not validate models for non-OMP harnesses."""
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)

            def fake_tmux_cmd(argv, **kwargs):
                _ = kwargs
                return subprocess.CompletedProcess(list(argv), 0, stdout="", stderr="")

            env_backup = os.environ.copy()
            os.environ.pop(team.ENV_TEAM_ROLE, None)
            try:
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
                    # Should not attempt validation for opencode harness
                    res = team.start(
                        team="Cobra",
                        repo=repo_root,
                        harness="opencode",
                        worker_model="any-model-string",
                    )
                    # Should succeed without raising
                    self.assertTrue(res.run_dir)
            finally:
                os.environ.clear()
                os.environ.update(env_backup)



if __name__ == "__main__":
    unittest.main()
