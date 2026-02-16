from __future__ import annotations

import os
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


class TestTeamByoAgentWrapping(unittest.TestCase):
    def test_wrap_composes_protocol_and_user_prompt(self) -> None:
        wrapped = team._compose_wrapped_agent_prompt(
            protocol_preamble="TEAM PROTOCOL BLOCK",
            user_agent_prompt="USER AGENT BLOCK",
        )
        self.assertIn("TEAM PROTOCOL BLOCK", wrapped)
        self.assertIn("USER AGENT BLOCK", wrapped)
        self.assertIn("---", wrapped)

    def _run_tui_once(self, *, harness: str, prompt: str, user_prompt: str) -> tuple[team.TuiResult, list[list[str]], str]:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            run_dir = repo_root / ".loom" / "team" / "runs" / "cobra"
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "run.json").write_text("{}", encoding="utf-8")

            run = {"run_id": "run-123", "team": "cobra"}
            popen_argv: list[list[str]] = []

            def fake_popen(argv, **kwargs):
                _ = kwargs
                popen_argv.append(list(argv))
                return _FakeProc(pid=1234)

            env = {
                "TMUX_PANE": "%1",
                team.ENV_TEAM_NAME: "cobra",
                team.ENV_TEAM_RUN_DIR: str(run_dir),
                team.ENV_TEAM_ROLE: team.ROLE_WORKER,
                team.ENV_TEAM_WORKER_ID: "w1",
                team.ENV_TEAM_TICKET_ID: "al-1",
            }
            old_env = os.environ.copy()
            os.environ.update(env)
            try:
                with (
                    mock.patch.object(team, "load_run", return_value=run),
                    mock.patch.object(team, "_require_bin"),
                    mock.patch.object(team, "safe_write_event"),
                    mock.patch.object(team, "tmux_signal"),
                    mock.patch.object(team, "_agent_prompt_text", return_value=user_prompt),
                    mock.patch("agent_loom.team.core.threading.Thread", _NoopThread),
                    mock.patch("agent_loom.team.core.subprocess.Popen", side_effect=fake_popen),
                ):
                    result = team.tui(
                        project_dir=repo_root,
                        harness=harness,
                        agent="custom-agent",
                        model="m1",
                        prompt=prompt,
                        respawn_cap=1,
                    )
            finally:
                os.environ.clear()
                os.environ.update(old_env)

            codex_instructions = ""
            instructions_path = run_dir / "agents" / "codex" / "w1.md"
            if instructions_path.exists():
                codex_instructions = instructions_path.read_text(encoding="utf-8")
            return result, popen_argv, codex_instructions

    def test_tui_wrap_applies_to_opencode(self) -> None:
        result, popen_argv, _ = self._run_tui_once(
            harness="opencode",
            prompt="TEAM PROTOCOL",
            user_prompt="USER AGENT",
        )
        self.assertEqual(result.exit_reason, "respawn_cap")
        self.assertTrue(popen_argv)
        argv = popen_argv[0]
        self.assertIn("--prompt", argv)
        wrapped = argv[argv.index("--prompt") + 1]
        self.assertIn("TEAM PROTOCOL", wrapped)
        self.assertIn("USER AGENT", wrapped)

    def test_tui_wrap_applies_to_claude(self) -> None:
        result, popen_argv, _ = self._run_tui_once(
            harness="claude",
            prompt="TEAM PROTOCOL",
            user_prompt="USER AGENT",
        )
        self.assertEqual(result.exit_reason, "respawn_cap")
        self.assertTrue(popen_argv)
        argv = popen_argv[0]
        wrapped = argv[-1]
        self.assertIn("TEAM PROTOCOL", wrapped)
        self.assertIn("USER AGENT", wrapped)

    def test_tui_wrap_applies_to_omp_append_prompt(self) -> None:
        result, popen_argv, _ = self._run_tui_once(
            harness="omp",
            prompt="TEAM PROTOCOL",
            user_prompt="USER AGENT",
        )
        self.assertEqual(result.exit_reason, "respawn_cap")
        self.assertTrue(popen_argv)
        argv = popen_argv[0]
        self.assertIn("--append-system-prompt", argv)
        wrapped = argv[argv.index("--append-system-prompt") + 1]
        self.assertIn("TEAM PROTOCOL", wrapped)
        self.assertIn("USER AGENT", wrapped)

    def test_tui_wrap_applies_to_codex_instructions_file(self) -> None:
        result, popen_argv, codex_instructions = self._run_tui_once(
            harness="codex",
            prompt="TEAM PROTOCOL",
            user_prompt="USER AGENT",
        )
        self.assertEqual(result.exit_reason, "respawn_cap")
        self.assertTrue(popen_argv)
        self.assertTrue(codex_instructions)
        self.assertIn("TEAM PROTOCOL", codex_instructions)
        self.assertIn("USER AGENT", codex_instructions)


if __name__ == "__main__":
    unittest.main()
