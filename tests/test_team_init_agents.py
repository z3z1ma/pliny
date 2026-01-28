import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team


class TestTeamInitAgents(unittest.TestCase):
    def test_init_creates_committed_agent_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)

            with mock.patch.object(team, "canonical_repo_root", return_value=repo_root):
                res = team.init_agents(repo=repo_root, create_missing=True)
            self.assertEqual(
                str(Path(res.repo_root).resolve()), str(repo_root.resolve())
            )
            self.assertFalse(res.missing)

            required = [
                repo_root / ".opencode" / "agents" / f"{team.DEFAULT_MANAGER_AGENT}.md",
                repo_root / ".opencode" / "agents" / f"{team.DEFAULT_WORKER_AGENT}.md",
                repo_root
                / ".opencode"
                / "agents"
                / f"{team.DEFAULT_INVESTIGATOR_AGENT}.md",
                repo_root
                / ".opencode"
                / "agents"
                / f"{team.DEFAULT_INTEGRATOR_AGENT}.md",
                repo_root / ".claude" / "agents" / f"{team.DEFAULT_MANAGER_AGENT}.md",
                repo_root / ".claude" / "agents" / f"{team.DEFAULT_WORKER_AGENT}.md",
                repo_root
                / ".claude"
                / "agents"
                / f"{team.DEFAULT_INVESTIGATOR_AGENT}.md",
                repo_root
                / ".claude"
                / "agents"
                / f"{team.DEFAULT_INTEGRATOR_AGENT}.md",
            ]
            for p in required:
                self.assertTrue(p.exists(), str(p))
                txt = p.read_text(encoding="utf-8")
                self.assertIn("<!-- managed-by: agent-loom-team", txt)
                self.assertIn(team.TEAM_AGENT_PROMPT_BEGIN, txt)
                self.assertIn(team.TEAM_AGENT_PROMPT_END, txt)

    def test_sync_preserves_manual_notes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            with mock.patch.object(team, "canonical_repo_root", return_value=repo_root):
                team.init_agents(repo=repo_root, create_missing=True)

            agent_path = (
                repo_root / ".opencode" / "agents" / f"{team.DEFAULT_MANAGER_AGENT}.md"
            )
            original = agent_path.read_text(encoding="utf-8")
            self.assertIn(team.TEAM_AGENT_PROMPT_END, original)

            # Add user customization after the managed block.
            agent_path.write_text(original + "\nUSER_NOTE: keep me\n", encoding="utf-8")
            with mock.patch.object(team, "canonical_repo_root", return_value=repo_root):
                team.init_agents(repo=repo_root, create_missing=True)

            updated = agent_path.read_text(encoding="utf-8")
            self.assertIn("USER_NOTE: keep me", updated)

    def test_sync_does_not_touch_non_managed_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            with mock.patch.object(team, "canonical_repo_root", return_value=repo_root):
                team.init_agents(repo=repo_root, create_missing=True)

            agent_path = (
                repo_root / ".opencode" / "agents" / f"{team.DEFAULT_MANAGER_AGENT}.md"
            )
            raw = agent_path.read_text(encoding="utf-8")

            # Remove managed-by marker to opt out.
            raw2 = raw.replace("<!-- managed-by:", "<!-- user-managed:", 1)
            agent_path.write_text(raw2, encoding="utf-8")

            with mock.patch.object(team, "canonical_repo_root", return_value=repo_root):
                team.init_agents(repo=repo_root, create_missing=True)
            again = agent_path.read_text(encoding="utf-8")
            self.assertIn("<!-- user-managed:", again)


if __name__ == "__main__":
    unittest.main()
