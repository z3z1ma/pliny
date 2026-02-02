import hashlib
import tempfile
import textwrap
import unittest
from unittest import mock
from typing import Callable, cast
from pathlib import Path

from agent_loom.team import core as team

init_agents = cast(Callable[..., object], getattr(team, "init_agents"))


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class TestYamlLines(unittest.TestCase):
    def test_emits_yaml_mapping_lines(self) -> None:
        obj = {
            "a": "b",
            "nested": {"x": True, "y": None, "z": 123},
        }

        self.assertEqual(
            team._yaml_lines(obj),
            [
                '"a": "b"',
                '"nested":',
                '  "x": true',
                '  "y": null',
                '  "z": 123',
            ],
        )

    def test_rejects_non_mapping(self) -> None:
        with self.assertRaises(TypeError):
            team._yaml_lines(["nope"])  # type: ignore[arg-type]


class TestAgentFileContent(unittest.TestCase):
    def test_renders_managed_frontmatter_and_marker(self) -> None:
        out = team._agent_file_content(
            name="team-worker",
            description="Team worker agent.",
            prompt="You are a worker.\n",
            permission={
                "*": "allow",
                "bash": {"*": "deny", "team *": "allow"},
            },
        )

        self.assertEqual(
            out,
            textwrap.dedent(
                """\
                ---
                description: "Team worker agent."
                mode: primary
                permission:
                  "*": "allow"
                  "bash":
                    "*": "deny"
                    "team *": "allow"
                ---
                <!-- managed-by: agent-loom-team 1.3.0 | agent: team-worker -->

                <!-- BEGIN:agent-loom-team:prompt -->
                You are a worker.
                <!-- END:agent-loom-team:prompt -->

                ## Manual notes

                _Everything below the managed prompt block is preserved on sync. Put human-only instructions, caveats, and repo-specific policy here._
                """
            ),
        )


class TestRenderManagerPrompt(unittest.TestCase):
    def test_snapshot(self) -> None:
        run = {
            "objective": "Ship fast, stay correct.",
            "team": "CobraKai",
            "run_id": "b2ede2554eec",
            "session": "team-cobrakai",
            "tickets_dir": "/repo/.tickets",
        }

        out = team.render_manager_prompt(run=run, charter_path=Path("CHARTER.md"))

        self.assertEqual(
            out,
            textwrap.dedent(
                """\
You are Team Manager.

TEAM: CobraKai
RUN_ID: b2ede2554eec
TMUX_SESSION: team-cobrakai
CHARTER: CHARTER.md
TICKET_DIR: /repo/.tickets

HARD CONSTRAINTS (non-negotiable):
- Do NOT run tmux directly. Use Loom CLI only.
- Do NOT implement tickets or edit code. Delegate tickets to workers.
- Do NOT move tickets to in_progress (workers do that when they start).
- Use Loom ticket CLI for all ticket IO; do not browse `.ticket`/`.tickets` directories.

OBJECTIVE:
Ship fast, stay correct.

Immediate sprint loop:
1) Fan-out: if backlog is unclear, start a sprint + spawn investigator: `loom team prep-sprint CobraKai --name "..."`.
   - You may create a one-off ticket yourself if it is truly small and obvious.
2) Plan: decide what runs in parallel and what must sequence.
3) Execute: spawn workers: `loom team spawn CobraKai <TICKET_ID>`.
   - Resume a retired worker in-place: `loom team resume-worker CobraKai <WORKER_ID>`.
4) Monitor: `loom team status CobraKai` / `loom team capture CobraKai <target>`.
5) Fan-in: ensure integrator: `loom team spawn-integrator CobraKai`; approve+enqueue: `loom team merge CobraKai enqueue --ticket <id> --branch <branch>`.
   - Integrator merges into merge-queue only (merge branch: team/merge-queue-b2ede255).
6) Ship: run `loom team ship CobraKai` to merge merge-queue -> origin/main (push=True). Nothing is shipped until this happens.
7) Cleanup: retire workers: `loom team retire CobraKai <WORKER_ID>`.
   - When safe to delete: `loom team mark-retirable CobraKai <WORKER_ID>` then later `loom team janitor CobraKai`.
   - Recovery: bounce a wedged worker: `loom team bounce CobraKai <WORKER_ID|TICKET_ID>`.
8) Objective updates: treat CHARTER as source of truth; pivot immediately.
   - Update objective yourself: `loom team objective CobraKai set|append --message "..."` (updates CHARTER + inbox).
9) When 100% done: `loom team disband CobraKai`.
10) Waiting: if you have no concrete next command, run `loom team wait 5m` and stop output.
   - Clock out/in: `loom team clock-out CobraKai` (pause) and later `loom team clock-in CobraKai` (resume).
   - If you wake and inbox is empty: run `loom team status CobraKai`, then check in with 1-2 active workers, then wait again.
11) Inbox: `loom team inbox CobraKai list --to manager --unacked` when nudged.
   - Per-worker backlog: `loom team inbox CobraKai list --to <WORKER_ID> --unacked`.
   - If you have pinged a worker multiple times and unacked keeps growing (e.g., 3+): bounce them: `loom team bounce CobraKai <WORKER_ID|TICKET_ID>`.

Memory (optional but useful):
- Loom memory is an Obsidian-like vault with links and backlinks.
- Use `loom memory` to leave notes for yourself or other workers.
- Notes can be associated with files, directories, file types, or commands.

Compound learning (repo-root only):
- Skills/docs/instincts are written in the canonical repo root (not worker worktrees).
- Workers may trigger compounding, but must not commit compound artifacts.
- Manager commits compound artifacts during ship (ship auto-syncs).
"""
            ).strip(),
        )


class TestRenderWorkerPrompt(unittest.TestCase):
    def test_snapshot_worker_role(self) -> None:
        run = {
            "objective": "Freeze prompt UX.",
            "team": "CobraKai",
            "run_id": "b2ede2554eec",
            "tickets_dir": "/repo/.tickets",
        }
        ticket = {"id": "mem-127d", "title": "Lock prompts", "status": "open"}
        ticket_payload = {
            "ok": True,
            "ticket": {"id": "mem-127d", "status": "open"},
            "body": "Unit tests only.",
        }

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

        self.assertEqual(
            out,
            textwrap.dedent(
                """\
                You are Team Worker.

                TEAM: CobraKai
                RUN_ID: b2ede2554eec
                WORKER_ID: w5
                TICKET: mem-127d
                TITLE: Lock prompts
                STATUS: open
                WORKTREE: worktrees/mem-127d
                BRANCH: team/mem-127d
                BASE: main
                CHARTER: CHARTER.md
                TICKET_DIR: /repo/.tickets

                HARD CONSTRAINTS:
                - Do NOT run tmux directly.
                - Do NOT browse `.ticket`/`.tickets` directories; use Loom ticket CLI only.
                - Transition ticket to in_progress when you begin real work (worker-owned).
                - Keep a steady cadence of Loom ticket updates.
                - Do not close tickets; do not merge to main (manager-owned).

                Instructions:
                - Work only on the assigned ticket.
                - Use Loom ticket to update progress after each major step or every ~15 minutes.
                - Commit after each meaningful milestone (do not sit on uncommitted work).
                - If blocked: write a structured escalation in Loom ticket (what was tried, what is needed, 2 options)
                  - Set status: `loom ticket status mem-127d blocked`
                  and notify the manager via `loom team send CobraKai manager "mem-127d blocked: ..."`.
                - Inbox discipline: when nudged, run `loom team inbox CobraKai list --to w5 --unacked` and ack messages you read with `loom team inbox CobraKai ack <MSG_ID>`.
                - Then respond with a brief status update and/or a Loom ticket update.
                - If completion candidate: set status to review and provide verification steps + commands run + risks.
                  - Set status: `loom ticket status mem-127d review`

                Idling policy: if you have no concrete next command right now, run `loom team wait 15m` and stop output.

                Follow-up tickets (encouraged): if you find important out-of-scope work, create a follow-up ticket with `loom ticket create`, link it, and mention it in your next update.

                Memory (optional but useful):
                - Loom memory is an Obsidian-like vault with links and backlinks.
                - Use `loom memory` to leave notes for yourself or other workers.
                - Notes can be associated with files, directories, file types, or commands.

                ROLE-SPECIFIC (WORKER):
                - When you believe work is complete, request manager review.
                - Preconditions: working tree clean; at least one commit for this ticket.
                - Required: `loom team send CobraKai manager "READY_FOR_REVIEW ticket=mem-127d worker=w5 branch=team/mem-127d sha=<shortsha> summary=... verify=... risks=..."`.

                Ticket payload (from Loom ticket) is available; follow acceptance criteria and dependencies.
                {
                  "ok": true,
                  "ticket": {
                    "id": "mem-127d",
                    "status": "open"
                  },
                  "body": "Unit tests only."
                }
                """
            ).strip(),
        )


class TestRenderInvestigatorPrompt(unittest.TestCase):
    def test_snapshot_investigator_role(self) -> None:
        run = {
            "objective": "Freeze prompt UX.",
            "team": "CobraKai",
            "run_id": "b2ede2554eec",
            "tickets_dir": "/repo/.tickets",
            "sprint": {"name": "Alpha", "tag": "sprint:alpha"},
        }
        ticket = {"id": "t-1", "title": "Sprint prep: Alpha", "status": "open"}
        ticket_payload = {
            "ok": True,
            "ticket": {"id": "t-1", "status": "open"},
            "body": "Write sprint brief, then create tickets.",
        }

        out = team.render_worker_prompt(
            run=run,
            role=team.ROLE_INVESTIGATOR,
            worker_id="w9",
            ticket=ticket,
            ticket_payload=ticket_payload,
            worktree_path=Path("worktrees/t-1"),
            branch="team/t-1",
            base="main",
            charter_path=Path("CHARTER.md"),
        )

        self.assertEqual(
            out,
            textwrap.dedent(
                """\
                You are Team Investigator.

                TEAM: CobraKai
                RUN_ID: b2ede2554eec
                WORKER_ID: w9
                TICKET: t-1
                TITLE: Sprint prep: Alpha
                STATUS: open
                WORKTREE: worktrees/t-1
                BRANCH: team/t-1
                BASE: main
                CHARTER: CHARTER.md
                TICKET_DIR: /repo/.tickets
                SPRINT: Alpha
                SPRINT_TAG: sprint:alpha

                HARD CONSTRAINTS:
                - Do NOT run tmux directly.
                - Do NOT browse `.ticket`/`.tickets` directories; use Loom ticket CLI only.
                - Transition ticket to in_progress when you begin real work (worker-owned).
                - Keep a steady cadence of Loom ticket updates.
                - Do not close tickets; do not merge to main (manager-owned).

                Instructions:
                - Work only on the assigned ticket.
                - Use Loom ticket to update progress after each major step or every ~15 minutes.
                - Commit after each meaningful milestone (do not sit on uncommitted work).
                - If blocked: write a structured escalation in Loom ticket (what was tried, what is needed, 2 options)
                  - Set status: `loom ticket status t-1 blocked`
                  and notify the manager via `loom team send CobraKai manager "t-1 blocked: ..."`.
                - Inbox discipline: when nudged, run `loom team inbox CobraKai list --to w9 --unacked` and ack messages you read with `loom team inbox CobraKai ack <MSG_ID>`.
                - Then respond with a brief status update and/or a Loom ticket update.
                - If completion candidate: set status to review and provide verification steps + commands run + risks.
                  - Set status: `loom ticket status t-1 review`

                Idling policy: if you have no concrete next command right now, run `loom team wait 15m` and stop output.

                Follow-up tickets (encouraged): if you find important out-of-scope work, create a follow-up ticket with `loom ticket create`, link it, and mention it in your next update.

                Memory (optional but useful):
                - Loom memory is an Obsidian-like vault with links and backlinks.
                - Use `loom memory` to leave notes for yourself or other workers.
                - Notes can be associated with files, directories, file types, or commands.

                ROLE-SPECIFIC (INVESTIGATOR):
                - You are the sprint PM. Your job is to turn the objective + current state into a coherent sprint and a crisp backlog.
                - First, read the run CHARTER to understand objective + historical direction.
                - Then inspect current backlog + repo state enough to remove ambiguity (tickets + git status/log).
                - Write a sprint brief INTO THIS assigned ticket (objective restatement, sprint focus, current state, plan, risks/unknowns).
                - Create/refine sprint tickets directly (prefer `loom ticket create --parent <THIS_TICKET>`).
                - Every ticket must include: scope/non-goals, step-by-step plan, acceptance criteria, verification commands (use `uv run ...` for Python), risks/edge cases, deps/ordering.
                - Before you stop: update THIS assigned ticket with (1) the list of created/updated ticket IDs and (2) suggested ordering + parallelization.
                - Then notify manager: `loom team send CobraKai manager "INVESTIGATOR_DONE worker=w9 ticket=t-1 created=[...]"`.
                - Then stop. The manager will retire your pane.

                Ticket payload (from Loom ticket) is available; follow acceptance criteria and dependencies.
                {
                  "ok": true,
                  "ticket": {
                    "id": "t-1",
                    "status": "open"
                  },
                  "body": "Write sprint brief, then create tickets."
                }
                """
            ).strip(),
        )


class TestRenderMergeWorkerPrompt(unittest.TestCase):
    def test_snapshot(self) -> None:
        run = {
            "objective": "Merge safely.",
            "team": "CobraKai",
            "run_id": "b2ede2554eec",
            "tickets_dir": "/repo/.tickets",
            "merge": {
                "config": {"target_branch": "main", "remote": "origin", "push": True}
            },
        }

        out = team.render_integrator_prompt(
            run=run,
            worker_id="merge-1",
            worktree_path=Path("worktrees/merge"),
            branch="team/merge-queue",
            base="main",
            charter_path=Path("CHARTER.md"),
        )

        self.assertEqual(
            out,
            textwrap.dedent(
                """\
                You are Team Integrator.

                TEAM: CobraKai
                RUN_ID: b2ede2554eec
                WORKER_ID: merge-1
                ROLE: integrator
                WORKTREE: worktrees/merge
                BRANCH: team/merge-queue
                BASE: main
                CHARTER: CHARTER.md
                TICKET_DIR: /repo/.tickets
                MERGE_TARGET: origin/main  push=True

                HARD CONSTRAINTS:
                - Do NOT run tmux directly.
                - Do not implement features; ship only manager-approved branches.
                - You do NOT merge into the target branch. You only merge into the merge-queue branch shown above.
                - If your merge worktree is wedged, ask the manager to run: `loom team spawn-integrator <TEAM> --force`.
                - Use `loom team merge` commands for deterministic queue operations.

                Queue ops:
                - Claim next: `loom team merge CobraKai next --claim-by merge-1`
                - Mark done: `loom team merge CobraKai done <ITEM_ID> --result merged|blocked --note "..."`
                - Manager ships merge-queue -> target with: `loom team ship CobraKai`

                Idling: If no work, run `loom team wait 10m` and stop output.
                """
            ).strip(),
        )


class TestEnsureOpenCodeAgents(unittest.TestCase):
    def test_default_agent_markdown_snapshot_sha256(self) -> None:
        expected = {
            "team-integrator.md": "21a1e7d976e9a9f3a3020224efc58f451b8ad9b7839cbf800ab87468baca153e",
            "team-investigator.md": "d57403b3acfa0d557c7ac331f800a333640289fa34127837566c4b8f42eeab5d",
            "team-manager.md": "f47deba920a92ee1e57dcb63e488f1d657ea56ac5468c8ec4ce5a8060213feff",
            "team-worker.md": "a7c3f05d0208b24ad7874295f218d6210facba5c7c49f5f6cc18cdb318f933c6",
        }

        with tempfile.TemporaryDirectory() as d:
            workdir = Path(d)
            with mock.patch.object(team, "canonical_repo_root", return_value=workdir):
                init_agents(repo=workdir, create_missing=True)
            agents_dir = workdir / ".opencode" / "agents"

            got = {}
            for p in sorted(agents_dir.glob("*.md")):
                got[p.name] = _sha256_text(p.read_text(encoding="utf-8"))

        self.assertEqual(got, expected)


if __name__ == "__main__":
    unittest.main()
