from __future__ import annotations

import dataclasses
import tempfile
import unittest
from pathlib import Path
from typing import Callable, cast
from unittest import mock

from agent_loom.team import core as team

init_agents = cast(Callable[..., team.InitAgentsResult], getattr(team, "init_agents"))


@dataclasses.dataclass
class _PackResult:
    wrote: list[str]
    skipped: list[str]
    warnings: list[str]


def _extract_prompt_block(text: str) -> str:
    begin = team.TEAM_AGENT_PROMPT_BEGIN
    end = team.TEAM_AGENT_PROMPT_END
    i = text.find(begin)
    j = text.find(end)
    if i < 0 or j < 0 or j <= i:
        return ""
    return text[i + len(begin) : j].strip()


class TestRenderPrompts(unittest.TestCase):
    def test_manager_prompt_has_core_loop_and_no_legacy_terms(self) -> None:
        run = {
            "objective": "Ship fast, stay correct.",
            "team": "CobraKai",
            "run_id": "b2ede2554eec",
            "session": "team-cobrakai",
            "tickets_dir": "/repo/.loom/ticket",
            "team_config": {"source": "", "loaded_at": "", "spec": team.default_team_config_spec()},
            "merge": {"config": {"target_branch": "main", "remote": "origin", "push": True}},
        }

        out = team.render_manager_prompt(run=run, charter_path=Path("CHARTER.md"))

        self.assertIn("loom team prep-sprint CobraKai", out)
        self.assertIn("loom team spawn CobraKai <TICKET_ID>", out)
        self.assertIn("loom team spawn-integrator CobraKai", out)
        self.assertNotIn("spawn-persona", out)
        self.assertNotIn("Investigator", out)
        self.assertNotIn("INVESTIGATOR_DONE", out)

    def test_worker_prompt_includes_subagent_guidance_and_role_append(self) -> None:
        run = {
            "team": "CobraKai",
            "run_id": "b2ede2554eec",
            "tickets_dir": "/repo/.loom/ticket",
            "team_config": {
                "source": "",
                "loaded_at": "",
                "spec": {
                    **team.default_team_config_spec(),
                    "role_prompts": {
                        "append": {
                            "manager": "",
                            "architect": "",
                            "worker": "Always include a rollback note.",
                            "integrator": "",
                        }
                    },
                },
            },
        }
        ticket = {"id": "mem-127d", "title": "Lock prompts", "status": "open"}
        ticket_payload = {"ok": True, "ticket": {"id": "mem-127d", "status": "open"}}

        out = team.render_worker_prompt(
            run=run,
            role=team.ROLE_WORKER,
            worker_id="w5",
            ticket=ticket,
            ticket_payload=ticket_payload,
            worktree_path=Path("worktrees/mem-127d"),
            branch="team/mem-127d",
            base="main",
            charter_path=Path("CHARTER.md"),
        )

        self.assertIn("Subagents (encouraged)", out)
        self.assertIn("TEAM CONFIG APPEND", out)
        self.assertIn("Always include a rollback note.", out)

    def test_architect_ticket_prompt_uses_architect_done_token(self) -> None:
        run = {
            "team": "CobraKai",
            "run_id": "b2ede2554eec",
            "tickets_dir": "/repo/.loom/ticket",
            "team_config": {"source": "", "loaded_at": "", "spec": team.default_team_config_spec()},
        }
        ticket = {"id": "t-1", "title": "Sprint prep", "status": "open"}
        ticket_payload = {"ok": True, "ticket": {"id": "t-1", "status": "open"}}

        out = team.render_worker_prompt(
            run=run,
            role=team.ROLE_ARCHITECT,
            worker_id="architect",
            ticket=ticket,
            ticket_payload=ticket_payload,
            worktree_path=Path("worktrees/t-1"),
            branch="team/t-1",
            base="main",
            charter_path=Path("CHARTER.md"),
        )

        self.assertIn("ARCHITECT_DONE", out)
        self.assertNotIn("INVESTIGATOR_DONE", out)
        self.assertNotIn("Investigator", out)

    def test_default_agent_prompts_use_core_roles_only(self) -> None:
        prompts = team.default_agent_prompts()
        self.assertEqual(set(prompts.keys()), {"manager", "worker", "architect", "integrator"})
        joined = "\n".join(prompts.values())
        self.assertNotIn("Investigator", joined)
        self.assertNotIn("spawn-persona", joined)


class TestInitAgentsPromptSync(unittest.TestCase):
    def test_init_agents_syncs_managed_prompt_blocks_from_canonical_templates(self) -> None:
        prompt_map = team.default_agent_prompts()

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            rels = [
                f".opencode/agents/{team.DEFAULT_MANAGER_AGENT}.md",
                f".opencode/agents/{team.DEFAULT_WORKER_AGENT}.md",
                f".opencode/agents/{team.DEFAULT_ARCHITECT_AGENT}.md",
                f".opencode/agents/{team.DEFAULT_INTEGRATOR_AGENT}.md",
                f".claude/agents/{team.DEFAULT_MANAGER_AGENT}.md",
                f".claude/agents/{team.DEFAULT_WORKER_AGENT}.md",
                f".claude/agents/{team.DEFAULT_ARCHITECT_AGENT}.md",
                f".claude/agents/{team.DEFAULT_INTEGRATOR_AGENT}.md",
            ]
            for rel in rels:
                p = repo_root / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(
                    "\n".join(
                        [
                            "---",
                            "name: test-agent",
                            "---",
                            team.TEAM_AGENT_PROMPT_BEGIN,
                            "STALE PROMPT",
                            team.TEAM_AGENT_PROMPT_END,
                            "",
                        ]
                    ),
                    encoding="utf-8",
                )

            with (
                mock.patch.object(team, "canonical_repo_root", return_value=repo_root),
                mock.patch.object(team, "_pack_installed", return_value=True),
                mock.patch.object(
                    team,
                    "pack_update",
                    return_value=_PackResult(wrote=[], skipped=[], warnings=[]),
                ),
            ):
                res = init_agents(repo=repo_root, create_missing=True)

            self.assertFalse(res.missing)
            self.assertEqual(len(res.updated), 8)

            for rel in rels:
                text = (repo_root / rel).read_text(encoding="utf-8")
                block = _extract_prompt_block(text)
                name = Path(rel).stem
                if name == team.DEFAULT_MANAGER_AGENT:
                    expected_role = "manager"
                elif name == team.DEFAULT_WORKER_AGENT:
                    expected_role = "worker"
                elif name == team.DEFAULT_ARCHITECT_AGENT:
                    expected_role = "architect"
                else:
                    expected_role = "integrator"
                self.assertEqual(block, str(prompt_map[expected_role]).strip())


if __name__ == "__main__":
    unittest.main()
