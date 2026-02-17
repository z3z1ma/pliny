from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from agent_loom.team.constants import ENV_TICKET_DIR
from agent_loom.team.io import _atomic_write_text
from agent_loom.team.merge_queue import _merge_state
from agent_loom.team.run_state import RunPaths
from agent_loom.team.team_config import team_config_summary_from_run


def write_charter(paths: RunPaths, run: Mapping[str, Any]) -> Path:
    objective = str(run.get("objective") or "").strip()
    objective_rev = int(run.get("objective_rev") or 0)
    objective_updated_at = str(run.get("objective_updated_at") or "").strip()
    tickets_dir = str(run.get("tickets_dir") or "").strip()
    sprint = run.get("sprint") if isinstance(run.get("sprint"), dict) else {}
    sprint_name = str((sprint or {}).get("name") or "").strip()
    sprint_tag = str((sprint or {}).get("tag") or "").strip()
    sprint_started_at = str((sprint or {}).get("started_at") or "").strip()

    lines = []
    lines.append(f"# Team Charter — {paths.team}\n")
    lines.append(f"Run ID: {run.get('run_id', '')}\n")
    lines.append(f"Repo: {run.get('repo_root', '')}\n")
    if tickets_dir:
        lines.append(f"{ENV_TICKET_DIR}: {tickets_dir}\n")
    lines.append("\n")
    lines.append("## Objective (current)\n\n")
    if objective_rev:
        lines.append(f"Objective rev: {objective_rev}\n")
    if objective_updated_at:
        lines.append(f"Objective updated_at: {objective_updated_at}\n")
    lines.append("\n")
    lines.append(objective + "\n\n")

    lines.append("## Sprint (current)\n\n")
    if sprint_name:
        lines.append(f"Name: {sprint_name}\n")
    if sprint_started_at:
        lines.append(f"Started: {sprint_started_at}\n")
    if sprint_tag:
        lines.append(f"Tag: {sprint_tag}\n")
        lines.append(f"Ticket rule: include tag `{sprint_tag}` on sprint tickets.\n")
    if not sprint_name:
        lines.append("(none)\n")
    lines.append("\n")

    team_config = team_config_summary_from_run(run)
    lines.append("## Team Config (current)\n\n")
    if team_config.get("source"):
        lines.append(f"Source: {team_config.get('source')}\n")
    if team_config.get("loaded_at"):
        lines.append(f"Loaded at: {team_config.get('loaded_at')}\n")
    if team_config.get("harness"):
        lines.append(f"Harness override: {team_config.get('harness')}\n")
    if team_config.get("model"):
        lines.append(f"Model override: {team_config.get('model')}\n")
    lines.append(f"Worker subagents: {team_config.get('worker_subagents')}\n")
    liveness = dict(team_config.get("liveness") or {})
    lines.append(
        "Liveness: "
        f"heartbeat={liveness.get('heartbeat_interval_s', '')}s "
        f"stale={liveness.get('stale_after_s', '')}s "
        f"dead={liveness.get('dead_after_s', '')}s "
        f"cooldown={liveness.get('recovery_cooldown_s', '')}s "
        f"max_recoveries_per_hour={liveness.get('max_recoveries_per_hour', '')}\n"
    )
    lines.append("\n")

    lines.append("## Manager quickstart\n\n")
    lines.append("Sprint loop:\n")
    lines.append(f'- Start sprint: `loom team prep-sprint {paths.team} --name "..."`\n')
    lines.append(
        "- Fan-out (preferred): spawn an Architect; architect creates tickets directly.\n"
    )
    lines.append("- Plan: decide concurrency + ordering.\n")
    lines.append("- Execute: spawn workers.\n")
    lines.append("- Fan-in: integrate via merge queue; ship.\n")
    lines.append("- Cleanup: retire workers; mark worktrees retirable when safe.\n")
    lines.append("\n")

    lines.append("Core:\n")
    lines.append(f"- Observe run health: `loom team status {paths.team}`\n")
    lines.append(
        f"- Capture output: `loom team capture {paths.team} <manager|worker:<id>|ticket:<id>>`\n"
    )
    lines.append(
        f'- Send message: `loom team send {paths.team} <manager|architect|integrator|workers|worker:<id>|ticket:<id>> "..."`\n'
    )
    lines.append(f"- Spawn worker: `loom team spawn {paths.team} <TICKET_ID>`\n")
    lines.append(
        f"- Resume worker: `loom team resume-worker {paths.team} <WORKER_ID>` (reuse existing worktree)\n"
    )
    lines.append(f"- Retire worker: `loom team retire {paths.team} <WORKER_ID>`\n")
    lines.append(
        f"- Mark worktree retirable: `loom team mark-retirable {paths.team} <WORKER_ID>` (manager-only)\n"
    )
    lines.append(
        f"- Bounce worker: `loom team bounce {paths.team} <WORKER_ID|TICKET_ID>`\n"
    )
    lines.append("\n")

    lines.append("Durability + waiting:\n")
    lines.append(
        f"- Inbox list: `loom team inbox {paths.team} list --to manager --unacked`\n"
    )
    lines.append(f"- Ack message: `loom team inbox {paths.team} ack <MSG_ID>`\n")
    lines.append(
        f"- Wait (blocks; wakes early on inbox): `loom team wait {paths.team} 5m` (or `loom team wait 5m` inside tmux; `snooze` is an alias)\n"
    )
    lines.append(
        f"- Clock out (pause team): `loom team clock-out {paths.team}` (keeps state; stops tmux session)\n"
    )
    lines.append(
        f"- Clock in (resume team): `loom team clock-in {paths.team}` (restores manager + active workers)\n"
    )
    lines.append(
        f'- Update objective: `loom team objective {paths.team} set|append --message "..."`\n'
    )
    lines.append(
        f"- Team hygiene: `loom team janitor {paths.team}` (deletes only marked-retirable worktrees)\n"
    )
    lines.append(
        f"- When 100% done: `loom team disband {paths.team}` (preserves worktrees by default)\n"
    )
    lines.append("\n")

    lines.append("Merge queue (ship code):\n")
    ms = _merge_state(run)
    cfg = dict(ms.get("config") or {})
    target_branch = str(cfg.get("target_branch") or "main").strip() or "main"
    remote = str(cfg.get("remote") or "origin").strip() or "origin"
    push = bool(cfg.get("push"))
    lines.append(
        f"- Ensure integrator exists: `loom team spawn-integrator {paths.team}`\n"
    )
    lines.append(
        f"- Enqueue approved branch: `loom team merge {paths.team} enqueue --ticket <TICKET_ID> --branch <BRANCH> --from-worker <WORKER_ID>`\n"
    )
    lines.append(f"- Queue status: `loom team merge {paths.team} list`\n")
    lines.append(
        f"- Ship (merge-queue -> {remote}/{target_branch}, push={push}): `loom team ship {paths.team}` (nothing is shipped until you do this)\n"
    )
    lines.append("\n")
    lines.append("## Worker protocol\n\n")
    lines.append("Workers must:\n")
    lines.append("- Work exactly one ticket in their assigned worktree.\n")
    lines.append(
        "- Update the ticket via loom ticket at least every ~15 minutes or after major steps.\n"
    )
    lines.append("- Escalate when blocked (structured) and notify manager.\n")
    lines.append("- Request review before considering a ticket complete.\n")

    paths.charter_file.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(paths.charter_file, "".join(lines), encoding="utf-8")
    return paths.charter_file


__all__ = ["write_charter"]
