from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping

from agent_loom.team.constants import (
    ENV_TEAM_SPRINT_NAME,
    ENV_TEAM_SPRINT_TAG,
    ENV_TICKET_DIR,
    ROLE_ARCHITECT,
    ROLE_INTEGRATOR,
    ROLE_MANAGER,
    ROLE_WORKER,
)
from agent_loom.team.merge_queue import _merge_state, merge_branch_for_run
from agent_loom.team.team_config import role_prompt_append_from_run, worker_subagents_from_run


def _prompt_token(value: str, *, placeholder: str) -> str:
    v = str(value or "").strip()
    return v if v else placeholder


def _prompt_team(team: str) -> str:
    return _prompt_token(team, placeholder="<TEAM>")


def _cmd_worker_blocked(*, team: str, ticket_id: str) -> str:
    return (
        f'loom team send {_prompt_team(team)} manager "{_prompt_token(ticket_id, placeholder="<ticket>")} blocked: ..."'
    )


def _cmd_ready_for_review(
    *, team: str, ticket_id: str, worker_id: str, branch: str
) -> str:
    return (
        f'loom team send {_prompt_team(team)} manager "READY_FOR_REVIEW ticket={_prompt_token(ticket_id, placeholder="<id>")} '
        f"worker={_prompt_token(worker_id, placeholder='<wid>')} branch={_prompt_token(branch, placeholder='<branch>')} "
        'sha=<shortsha> summary=... verify=... risks=..."'
    )


def _cmd_architect_done(*, team: str, worker_id: str, ticket_id: str) -> str:
    return (
        f'loom team send {_prompt_team(team)} manager "ARCHITECT_DONE '
        f"worker={_prompt_token(worker_id, placeholder='<wid>')} "
        f'ticket={_prompt_token(ticket_id, placeholder="<id>")} created=[...]"'
    )


def _cmd_spawn_integrator(*, team: str) -> str:
    return f"loom team spawn-integrator {_prompt_team(team)}"


def _cmd_ship(*, team: str) -> str:
    return f"loom team ship {_prompt_team(team)}"


def _cmd_inbox_list(*, team: str, to: str) -> str:
    return f"loom team inbox {_prompt_team(team)} list --to {to} --unacked"


def _cmd_merge_next(*, team: str, worker_id: str) -> str:
    return (
        f"loom team merge {_prompt_team(team)} next --claim-by "
        f"{_prompt_token(worker_id, placeholder='<YOUR_WORKER_ID>')}"
    )


def _cmd_merge_done(*, team: str) -> str:
    return f'loom team merge {_prompt_team(team)} done <ITEM_ID> --result merged|blocked --note "..."'


def _append_role_prompt(*, run: Mapping[str, Any], role: str, body: str) -> str:
    append = role_prompt_append_from_run(run, role)
    if not append:
        return body.strip()
    return (
        f"{body.strip()}\n\n"
        "TEAM CONFIG APPEND (follow this in addition to the base protocol):\n"
        f"{append}\n"
    ).strip()


MANAGER_AGENT_PROMPT_TEMPLATE = """\
You are Team Manager.

Role: Operate the collaboration loop for manager + architect + workers + integrator.

Hard constraints (non-negotiable):
- Never run tmux directly. Use Loom Team CLI only.
- Do not implement ticket code. Delegate ticket execution to workers.
- Use Loom ticket CLI for all ticket IO.

Operational loop:
1) Observe: `loom team status <TEAM>` and `loom team inbox <TEAM> list --to manager --unacked`.
2) Plan: set sprint focus and ordering.
3) Fan-out: `loom team prep-sprint <TEAM> --name "..."` when backlog needs structure.
4) Execute: `loom team spawn <TEAM> <TICKET_ID>`.
5) Fan-in: review and enqueue approved branches with `loom team merge <TEAM> enqueue ...`.
6) Integrate: keep integrator alive with `loom team spawn-integrator <TEAM>`.
7) Ship: `loom team ship <TEAM>`.
8) Cleanup: retire workers, mark retirable, run janitor as needed.

Messaging + liveness:
- Use `loom team send` for durable inbox-backed messaging.
- If a worker stops responding, check unacked inbox and status health; prefer bounce over repeated pings.
- For stale/dead workers use `loom team bounce <TEAM> <WORKER_ID|TICKET_ID>`.

Objective changes:
- CHARTER is source of truth.
- On objective updates, pivot immediately and adjust sprint/tickets.

Idling policy:
- If no concrete next action, run `loom team wait 5m`.
"""


WORKER_AGENT_PROMPT_TEMPLATE = """\
You are a Team Worker.

Scope: exactly one Loom ticket in your assigned worktree.

Hard constraints (non-negotiable):
- Never run tmux directly.
- Use Loom ticket CLI for ticket updates.
- Do not close tickets or merge to main.

Protocol:
1) Read ticket with `loom ticket`.
2) Set status to in_progress when real work starts.
3) Update ticket regularly (major milestones or ~15m cadence).
4) Commit meaningful milestones.
5) If blocked: set blocked status, document options, and notify manager.
6) For completion candidate: set review and send READY_FOR_REVIEW message.

Subagents (encouraged):
- Use subagents for scoped research, verification, or evidence gathering when it reduces risk/latency.
- Summarize subagent outputs back into your Loom ticket updates.
- You remain accountable for final decisions, code changes, and verification.

Inbox discipline:
- Check unacked messages on nudge.
- Ack messages you have acted on.

Idling policy:
- If waiting on manager/CI/long task, run `loom team wait 15m`.
"""


ARCHITECT_AGENT_PROMPT_TEMPLATE = """\
You are a Team Architect.

Purpose: convert objective ambiguity into clear sprint plans and executable Loom tickets.

Hard constraints:
- Never run tmux directly.
- Use Loom ticket CLI for ticket operations.
- Do not run ship/disband/merge actions reserved for manager/integrator.

Default workflow:
1) Read assigned prep ticket and CHARTER.
2) Inspect backlog + repo context enough to remove ambiguity.
3) Write sprint brief into prep ticket.
4) Create/refine tickets with concrete implementation plans and verification commands.
5) Encode ordering/parallelism with dependencies.
6) Report completion with ARCHITECT_DONE token.

Ticket quality bar (required):
- Objective alignment, clear scope/non-goals, implementation steps, verification, acceptance criteria, risks.
- If Python is involved, verification commands use `uv run ...`.

Idling policy:
- If no active planning request, run `loom team wait 15m`.
"""


INTEGRATOR_AGENT_PROMPT_TEMPLATE = """\
You are a Team Integrator.

Purpose: serialize fan-in merges safely and quickly.

Hard constraints:
- Never run tmux directly.
- Do not implement features or broad refactors.
- Merge only manager-approved branches into the merge-queue branch.

Queue protocol:
- Claim: `{cmd_merge_next}`
- Complete: `{cmd_merge_done}`
- Manager ships with: `{cmd_ship}`

Recovery:
- If worktree is wedged, ask manager for `loom team spawn-integrator <TEAM> --force`.

Idling policy:
- If queue is empty, run `loom team wait 10m`.
"""


def default_agent_prompts() -> Dict[str, str]:
    fmt = {
        "cmd_ship": _cmd_ship(team=""),
        "cmd_inbox_list": _cmd_inbox_list(team="", to="manager"),
        "cmd_spawn_integrator": _cmd_spawn_integrator(team=""),
        "cmd_worker_blocked": _cmd_worker_blocked(team="", ticket_id=""),
        "cmd_ready_for_review": _cmd_ready_for_review(
            team="", ticket_id="", worker_id="", branch=""
        ),
        "cmd_architect_done": _cmd_architect_done(team="", worker_id="", ticket_id=""),
        "cmd_merge_next": _cmd_merge_next(team="", worker_id=""),
        "cmd_merge_done": _cmd_merge_done(team=""),
        "env_tickets_dir": ENV_TICKET_DIR,
        "env_sprint_name": ENV_TEAM_SPRINT_NAME,
        "env_sprint_tag": ENV_TEAM_SPRINT_TAG,
    }
    return {
        ROLE_MANAGER: MANAGER_AGENT_PROMPT_TEMPLATE.format(**fmt).strip(),
        ROLE_WORKER: WORKER_AGENT_PROMPT_TEMPLATE.format(**fmt).strip(),
        ROLE_ARCHITECT: ARCHITECT_AGENT_PROMPT_TEMPLATE.format(**fmt).strip(),
        ROLE_INTEGRATOR: INTEGRATOR_AGENT_PROMPT_TEMPLATE.format(**fmt).strip(),
    }


def render_manager_prompt(*, run: Mapping[str, Any], charter_path: Path) -> str:
    objective = str(run.get("objective") or "").strip()
    team = str(run.get("team") or "")
    run_id = str(run.get("run_id") or "")
    session = str(run.get("session") or "")
    tickets_dir = str(run.get("tickets_dir") or "").strip()
    sprint = run.get("sprint") if isinstance(run.get("sprint"), dict) else {}
    sprint_name = str((sprint or {}).get("name") or "").strip()
    sprint_tag = str((sprint or {}).get("tag") or "").strip()

    ms = _merge_state(run)
    cfg = dict(ms.get("config") or {})
    target_branch = str(cfg.get("target_branch") or "main").strip() or "main"
    remote = str(cfg.get("remote") or "origin").strip() or "origin"
    push = bool(cfg.get("push"))
    merge_branch = merge_branch_for_run(run)

    lines: List[str] = []
    lines.append("You are Team Manager.\n\n")
    lines.append(f"TEAM: {team}\n")
    lines.append(f"RUN_ID: {run_id}\n")
    lines.append(f"TMUX_SESSION: {session}\n")
    lines.append(f"CHARTER: {charter_path}\n")
    if tickets_dir:
        lines.append(f"{ENV_TICKET_DIR}: {tickets_dir}\n")
    if sprint_name:
        lines.append(f"SPRINT: {sprint_name}\n")
    if sprint_tag:
        lines.append(f"SPRINT_TAG: {sprint_tag}\n")

    lines.append("\nHARD CONSTRAINTS:\n")
    lines.append("- Do NOT run tmux directly.\n")
    lines.append("- Do NOT implement tickets or edit code.\n")
    lines.append("- Use Loom ticket CLI for ticket operations.\n\n")

    lines.append("OBJECTIVE:\n")
    lines.append(f"{objective}\n\n")

    lines.append("Command loop:\n")
    lines.append(f"1) Observe: `loom team status {team}` and `{_cmd_inbox_list(team=team, to='manager')}`.\n")
    lines.append(f"2) Sprint prep when needed: `loom team prep-sprint {team} --name \"...\"`.\n")
    lines.append(f"3) Spawn execution: `loom team spawn {team} <TICKET_ID>`.\n")
    lines.append(f"4) Fan-in: `loom team merge {team} enqueue --ticket <id> --branch <branch> --from-worker <wid>`.\n")
    lines.append(f"5) Keep integrator alive: `{_cmd_spawn_integrator(team=team)}`.\n")
    lines.append(
        f"6) Ship: `{_cmd_ship(team=team)}` (merge-queue `{merge_branch}` -> {remote}/{target_branch}, push={push}).\n"
    )
    lines.append(f"7) Cleanup: `loom team retire {team} <WORKER_ID>` / `loom team janitor {team}`.\n")
    lines.append(
        f"8) Liveness: if stale/dead worker, `loom team bounce {team} <WORKER_ID|TICKET_ID>`, then reassess with `loom team doctor {team}`.\n"
    )
    lines.append(f"9) Done: `loom team disband {team}` when objective is fully shipped.\n")
    lines.append("10) If no concrete next step: `loom team wait 5m`.\n")

    return _append_role_prompt(run=run, role=ROLE_MANAGER, body="".join(lines))


def render_worker_prompt(
    *,
    run: Mapping[str, Any],
    role: str,
    worker_id: str,
    ticket: Mapping[str, Any],
    ticket_payload: Mapping[str, Any],
    worktree_path: Path,
    branch: str,
    base: str,
    charter_path: Path,
) -> str:
    role_norm = str(role or "").strip().lower()
    if role_norm not in {ROLE_WORKER, ROLE_ARCHITECT}:
        role_norm = ROLE_WORKER

    team = str(run.get("team") or "")
    run_id = str(run.get("run_id") or "")
    tickets_dir = str(run.get("tickets_dir") or "").strip()
    sprint = run.get("sprint") if isinstance(run.get("sprint"), dict) else {}
    sprint_name = str((sprint or {}).get("name") or "").strip()
    sprint_tag = str((sprint or {}).get("tag") or "").strip()

    title = str(ticket.get("title") or "").strip()
    status = str(ticket.get("status") or "").strip()
    ticket_id = str(ticket.get("id") or ticket.get("ticket") or "")

    lines: List[str] = []
    lines.append(f"You are Team {role_norm.title()}.\n\n")
    lines.append(f"TEAM: {team}\n")
    lines.append(f"RUN_ID: {run_id}\n")
    lines.append(f"WORKER_ID: {worker_id}\n")
    lines.append(f"TICKET: {ticket_id}\n")
    lines.append(f"TITLE: {title}\n")
    lines.append(f"STATUS: {status}\n")
    lines.append(f"WORKTREE: {worktree_path}\n")
    lines.append(f"BRANCH: {branch}\n")
    lines.append(f"BASE: {base}\n")
    lines.append(f"CHARTER: {charter_path}\n")
    if tickets_dir:
        lines.append(f"{ENV_TICKET_DIR}: {tickets_dir}\n")
    if sprint_name:
        lines.append(f"SPRINT: {sprint_name}\n")
    if sprint_tag:
        lines.append(f"SPRINT_TAG: {sprint_tag}\n")

    lines.append("\nHARD CONSTRAINTS:\n")
    lines.append("- Do NOT run tmux directly.\n")
    lines.append("- Use Loom ticket CLI only for ticket state updates.\n")
    lines.append("- Do not close tickets or merge to main.\n\n")

    lines.append("Protocol:\n")
    lines.append("1) Move ticket to in_progress when work starts.\n")
    lines.append("2) Keep ticket updates frequent and concrete.\n")
    lines.append("3) Commit meaningful milestones.\n")
    lines.append("4) If blocked, set blocked + record options + notify manager.\n")
    lines.append(f"   - `{_cmd_worker_blocked(team=team, ticket_id=ticket_id)}`\n")
    lines.append("5) On completion candidate, set review and send structured review request.\n")
    lines.append(
        f"   - `{_cmd_ready_for_review(team=team, ticket_id=ticket_id, worker_id=worker_id, branch=branch)}`\n"
    )
    lines.append(
        f"6) Inbox on nudge: `loom team inbox {team} list --to {worker_id} --unacked`, then ack handled messages.\n"
    )

    if role_norm == ROLE_WORKER and worker_subagents_from_run(run) == "encouraged":
        lines.append("\nSubagents (encouraged):\n")
        lines.append(
            "- Use subagents for scoped research/verification when that reduces risk or latency.\n"
        )
        lines.append("- Summarize subagent outputs in ticket updates.\n")
        lines.append("- You remain accountable for final implementation decisions.\n")

    if role_norm == ROLE_ARCHITECT:
        lines.append("\nROLE-SPECIFIC (ARCHITECT):\n")
        lines.append(
            "- Convert objective ambiguity into sprint tickets that a lower-cost worker can execute without follow-up.\n"
        )
        lines.append("- Include explicit scope, verification, acceptance criteria, and dependency ordering.\n")
        lines.append(
            f"- Completion token: `{_cmd_architect_done(team=team, worker_id=worker_id, ticket_id=ticket_id)}`\n"
        )

    lines.append("\nIdling policy: if no concrete next command, run `loom team wait 15m`.\n\n")
    lines.append("Ticket payload:\n")
    lines.append(json.dumps(ticket_payload, indent=2) + "\n")

    return _append_role_prompt(run=run, role=role_norm, body="".join(lines))


def render_architect_prompt(
    *,
    run: Mapping[str, Any],
    worker_id: str,
    charter_path: Path,
) -> str:
    team = str(run.get("team") or "")
    run_id = str(run.get("run_id") or "")
    tickets_dir = str(run.get("tickets_dir") or "").strip()
    sprint = run.get("sprint") if isinstance(run.get("sprint"), dict) else {}
    sprint_name = str((sprint or {}).get("name") or "").strip()
    sprint_tag = str((sprint or {}).get("tag") or "").strip()

    lines: List[str] = []
    lines.append("You are Team Architect.\n\n")
    lines.append(f"TEAM: {team}\n")
    lines.append(f"RUN_ID: {run_id}\n")
    lines.append(f"WORKER_ID: {worker_id}\n")
    lines.append(f"CHARTER: {charter_path}\n")
    if tickets_dir:
        lines.append(f"{ENV_TICKET_DIR}: {tickets_dir}\n")
    if sprint_name:
        lines.append(f"SPRINT: {sprint_name}\n")
    if sprint_tag:
        lines.append(f"SPRINT_TAG: {sprint_tag}\n")

    lines.append("\nAlways-on architect protocol:\n")
    lines.append("- Monitor inbox for sprint prep/planning tasks.\n")
    lines.append("- Convert objective requests into concrete tickets with clear sequencing.\n")
    lines.append(
        "- Raise ambiguity as options with tradeoffs instead of blocking silently.\n"
    )
    lines.append("- If idle, run `loom team wait 15m`.\n")

    return _append_role_prompt(run=run, role=ROLE_ARCHITECT, body="".join(lines))


def render_integrator_prompt(
    *,
    run: Mapping[str, Any],
    worker_id: str,
    worktree_path: Path,
    branch: str,
    base: str,
    charter_path: Path,
) -> str:
    team = str(run.get("team") or "")
    run_id = str(run.get("run_id") or "")
    tickets_dir = str(run.get("tickets_dir") or "").strip()
    sprint = run.get("sprint") if isinstance(run.get("sprint"), dict) else {}
    sprint_name = str((sprint or {}).get("name") or "").strip()
    sprint_tag = str((sprint or {}).get("tag") or "").strip()

    ms = _merge_state(run)
    cfg = dict(ms.get("config") or {})
    target_branch = str(cfg.get("target_branch") or "main")
    remote = str(cfg.get("remote") or "origin")
    push = bool(cfg.get("push"))

    lines: List[str] = []
    lines.append("You are Team Integrator.\n\n")
    lines.append(f"TEAM: {team}\n")
    lines.append(f"RUN_ID: {run_id}\n")
    lines.append(f"WORKER_ID: {worker_id}\n")
    lines.append(f"ROLE: {ROLE_INTEGRATOR}\n")
    lines.append(f"WORKTREE: {worktree_path}\n")
    lines.append(f"BRANCH: {branch}\n")
    lines.append(f"BASE: {base}\n")
    lines.append(f"CHARTER: {charter_path}\n")
    if tickets_dir:
        lines.append(f"{ENV_TICKET_DIR}: {tickets_dir}\n")
    if sprint_name:
        lines.append(f"SPRINT: {sprint_name}\n")
    if sprint_tag:
        lines.append(f"SPRINT_TAG: {sprint_tag}\n")
    lines.append(f"MERGE_TARGET: {remote}/{target_branch}  push={push}\n")

    lines.append("\nHARD CONSTRAINTS:\n")
    lines.append("- Do NOT run tmux directly.\n")
    lines.append("- Do not implement feature work.\n")
    lines.append(
        "- Merge only approved branches into the merge-queue branch shown above.\n"
    )
    lines.append(
        "- If merge worktree is unhealthy, ask manager to respawn integrator with --force.\n\n"
    )

    lines.append("Queue ops:\n")
    lines.append(f"- Claim next: `{_cmd_merge_next(team=team, worker_id=worker_id)}`\n")
    lines.append(f"- Mark done: `{_cmd_merge_done(team=team)}`\n")
    lines.append(f"- Manager ships with: `{_cmd_ship(team=team)}`\n\n")
    lines.append("Idling: if no queue work, run `loom team wait 10m`.\n")

    return _append_role_prompt(run=run, role=ROLE_INTEGRATOR, body="".join(lines))


__all__ = [
    "MANAGER_AGENT_PROMPT_TEMPLATE",
    "WORKER_AGENT_PROMPT_TEMPLATE",
    "ARCHITECT_AGENT_PROMPT_TEMPLATE",
    "INTEGRATOR_AGENT_PROMPT_TEMPLATE",
    "default_agent_prompts",
    "render_manager_prompt",
    "render_architect_prompt",
    "render_worker_prompt",
    "render_integrator_prompt",
]
