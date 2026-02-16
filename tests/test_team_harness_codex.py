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


class TestTeamHarnessCodex(unittest.TestCase):
    def test_normalize_harness_accepts_codex(self) -> None:
        self.assertEqual(team._normalize_harness("codex"), "codex")

    def test_start_persists_codex_harness_config(self) -> None:
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
                res = team.start(team="Cobra", repo=repo_root, harness="codex")

            run_path = Path(res.run_dir) / "run.json"
            run = json.loads(run_path.read_text(encoding="utf-8"))
            self.assertEqual(str(run.get("harness") or ""), "codex")
            self.assertIn("codex", run)
            codex_cfg = dict(run.get("codex") or {})
            self.assertIn("model", codex_cfg)
            self.assertIn("models", codex_cfg)
            self.assertEqual(
                str(codex_cfg.get("manager_agent") or ""), team.DEFAULT_MANAGER_AGENT
            )

    def test_tui_codex_spawns_with_instructions_sandbox_codex_home_and_resume(self) -> None:
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
            shared_codex_home = repo_root / "shared-codex-home"
            shared_codex_home.mkdir(parents=True, exist_ok=True)
            shared_auth = shared_codex_home / "auth.json"
            shared_auth.write_text('{"access_token":"token"}\n', encoding="utf-8")
            shared_config = shared_codex_home / "config.toml"
            shared_config.write_text('model = "gpt-5.3-codex"\n', encoding="utf-8")
            popen_calls: list[tuple[list[str], dict[str, str]]] = []

            def fake_popen(argv, **kwargs):
                env = dict(kwargs.get("env") or {})
                popen_calls.append((list(argv), env))
                return _FakeProc(pid=4321)

            env = {
                "TMUX_PANE": "%1",
                team.ENV_TEAM_NAME: "cobra",
                team.ENV_TEAM_RUN_DIR: str(run_dir),
                team.ENV_TEAM_ROLE: team.ROLE_MANAGER,
                team.ENV_TEAM_WORKER_ID: "",
                "CODEX_HOME": str(shared_codex_home),
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
                        harness="codex",
                        agent=team.DEFAULT_MANAGER_AGENT,
                        model="gpt-5.3-codex",
                        prompt="initial prompt",
                        respawn_cap=2,
                    )
            finally:
                os.environ.clear()
                os.environ.update(old_env)

            self.assertEqual(result.exit_reason, "respawn_cap")
            self.assertGreaterEqual(len(popen_calls), 2)

            first_argv, first_env = popen_calls[0]
            self.assertEqual(first_argv[0], "codex")
            self.assertIn("--model", first_argv)
            self.assertIn("gpt-5.3-codex", first_argv)
            self.assertIn("--dangerously-bypass-approvals-and-sandbox", first_argv)
            self.assertNotIn("--sandbox", first_argv)
            self.assertNotIn("--ask-for-approval", first_argv)
            self.assertIn("--config", first_argv)
            config_value = first_argv[first_argv.index("--config") + 1]
            self.assertIn("model_instructions_file=", config_value)
            self.assertIn("initial prompt", first_argv)

            codex_home = first_env.get("CODEX_HOME")
            self.assertEqual(
                str(Path(str(codex_home or "")).resolve()),
                str((run_dir / "sessions" / "codex" / "manager").resolve()),
            )
            pane_codex_home = Path(str(codex_home or ""))
            pane_auth = pane_codex_home / "auth.json"
            pane_config = pane_codex_home / "config.toml"
            self.assertTrue(pane_auth.exists())
            self.assertTrue(pane_config.exists())
            self.assertEqual(
                pane_auth.read_text(encoding="utf-8"),
                shared_auth.read_text(encoding="utf-8"),
            )
            self.assertEqual(
                pane_config.read_text(encoding="utf-8"),
                shared_config.read_text(encoding="utf-8"),
            )

            second_argv, _ = popen_calls[1]
            self.assertIn("resume", second_argv)
            self.assertIn("--last", second_argv)
            self.assertNotIn("initial prompt", second_argv)

            instructions_path = run_dir / "agents" / "codex" / "manager.md"
            self.assertTrue(instructions_path.exists())
            instructions_text = instructions_path.read_text(encoding="utf-8")
            self.assertIn("SYSTEM PROMPT BODY", instructions_text)
            self.assertIn("LOCAL NOTE", instructions_text)


if __name__ == "__main__":
    unittest.main()
