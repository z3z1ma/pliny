from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, Mapping, MutableMapping

from agent_loom.team.errors import TeamError
from agent_loom.team.models import ObjectiveShowResult
from agent_loom.team.run_state import RunPaths
from agent_loom.team.strings import sanitize


def read_text_input(
    *,
    message: str,
    file_path: str,
    stdin_ok: bool,
) -> str:
    msg = str(message or "")
    fp = str(file_path or "").strip()
    if msg.strip():
        return msg
    if fp:
        p = Path(fp).expanduser().resolve()
        return p.read_text(encoding="utf-8")
    if stdin_ok and not sys.stdin.isatty():
        return sys.stdin.read()
    raise TeamError(
        "Missing objective text. Use --message, --file, or pipe via stdin.",
        code="ARG",
        exit_code=2,
    )


def objective_append_block(text: str, *, stamp: str) -> str:
    t = str(text or "").strip("\n")
    if not t:
        return ""
    return f"\n\n---\n\n## Update {stamp}\n\n{t}\n"


def objective_show(*, paths: RunPaths, run: Mapping[str, Any]) -> ObjectiveShowResult:
    return ObjectiveShowResult(
        team=str(run.get("team") or paths.team),
        objective=str(run.get("objective") or ""),
        objective_rev=int(run.get("objective_rev") or 0),
        objective_updated_at=str(run.get("objective_updated_at") or ""),
        charter=str(paths.charter_file.resolve()),
    )


def apply_objective_mutation(
    *,
    run: MutableMapping[str, Any],
    mode: str,
    text: str,
    now: str,
) -> Dict[str, Any]:
    cur = str(run.get("objective") or "")
    if mode == "set":
        new_obj = str(text or "").strip("\n") + "\n"
    elif mode == "append":
        new_obj = (cur or "").rstrip("\n") + objective_append_block(text, stamp=now)
    else:
        raise TeamError(f"Invalid objective mode: {mode}", code="BUG", exit_code=2)

    prev_rev = int(run.get("objective_rev") or 0)
    run["objective"] = new_obj
    run["objective_rev"] = prev_rev + 1
    run["objective_updated_at"] = now
    run["done_reminder"] = {}

    return {
        "objective_rev": int(run.get("objective_rev") or 0),
        "objective_updated_at": str(run.get("objective_updated_at") or ""),
    }


def sprint_state(run: Mapping[str, Any]) -> Dict[str, str]:
    sprint = run.get("sprint")
    if not isinstance(sprint, dict):
        return {"name": "", "tag": ""}
    return {
        "name": str(sprint.get("name") or "").strip(),
        "tag": str(sprint.get("tag") or "").strip(),
    }


def sprint_slug(name: str) -> str:
    return sanitize(str(name or ""), max_len=40)


def start_sprint_state(
    *,
    run: MutableMapping[str, Any],
    name: str,
    force: bool,
    now: str,
) -> Dict[str, Any]:
    sprint_name = str(name or "").strip()
    if not sprint_name:
        raise TeamError("Sprint name is required", code="ARG", exit_code=2)

    slug = sprint_slug(sprint_name)
    if not slug:
        raise TeamError("Invalid sprint name", code="ARG", exit_code=2)

    existing = run.get("sprint") if isinstance(run.get("sprint"), dict) else {}
    existing_name = str((existing or {}).get("name") or "").strip()
    if existing_name and not bool(force):
        raise TeamError(
            f"Sprint already set: {existing_name} (use --force to overwrite)",
            code="ARG",
            exit_code=2,
        )

    rev = int((existing or {}).get("rev") or 0) + 1
    sprint = {
        "name": sprint_name,
        "slug": slug,
        "tag": f"sprint:{slug}",
        "rev": rev,
        "started_at": now,
        "updated_at": now,
    }
    run["sprint"] = sprint
    return sprint


def set_sprint_state(
    *,
    run: MutableMapping[str, Any],
    name: str,
    tag: str,
    now: str,
) -> Dict[str, Any]:
    sprint_name = str(name or "").strip()
    if not sprint_name:
        raise TeamError("Sprint name is required", code="ARG", exit_code=2)

    slug = sprint_slug(sprint_name)
    if not slug:
        raise TeamError("Invalid sprint name", code="ARG", exit_code=2)

    sprint_tag = str(tag or "").strip() or f"sprint:{slug}"
    existing = run.get("sprint") if isinstance(run.get("sprint"), dict) else {}
    rev = int((existing or {}).get("rev") or 0) + 1
    sprint = {
        "name": sprint_name,
        "slug": slug,
        "tag": sprint_tag,
        "rev": rev,
        "started_at": (existing or {}).get("started_at") or now,
        "updated_at": now,
    }
    run["sprint"] = sprint
    return sprint


def clear_sprint_state(*, run: MutableMapping[str, Any]) -> int:
    existing = run.get("sprint") if isinstance(run.get("sprint"), dict) else {}
    rev = int((existing or {}).get("rev") or 0) + 1
    run["sprint"] = {}
    return rev


def build_prep_sprint_ticket_description(*, objective: str, sprint_name: str, tag: str) -> str:
    desc_lines = []
    if objective:
        desc_lines.append("Objective:")
        desc_lines.append(objective)
        desc_lines.append("")
    desc_lines.append("Sprint prep deliverable (fill this ticket in, then create tickets):")
    desc_lines.append("")
    desc_lines.append("## Sprint Brief")
    desc_lines.append("")
    desc_lines.append("Write a short sprint brief that a cheaper worker model can follow.")
    desc_lines.append("")
    desc_lines.append("Required sections:")
    desc_lines.append("- Objective restatement: ...")
    desc_lines.append("- Sprint focus (2-5 words): ...")
    desc_lines.append("- Why this sprint focus is the best next step: ...")
    desc_lines.append("- Current state:")
    desc_lines.append("  - Existing tickets that matter: ...")
    desc_lines.append("  - Codebase state that matters (git status/log, key modules): ...")
    desc_lines.append("- Risks + unknowns (and how we'll resolve them): ...")
    desc_lines.append("")
    desc_lines.append("## Ticket Set")
    desc_lines.append("")
    desc_lines.append(
        "Create the sprint tickets directly. This sprint prep ticket should be the parent."
    )
    desc_lines.append(f"- Tag rule: include `{tag}` on sprint tickets.")
    desc_lines.append(
        '- Prefer: `loom ticket create ... --parent <THIS_TICKET_ID> --acceptance "..."`'
    )
    desc_lines.append("")
    desc_lines.append("Ticket quality rubric (non-negotiable):")
    desc_lines.append("- Scope + explicit non-goals")
    desc_lines.append("- Step-by-step implementation plan (include file paths when possible)")
    desc_lines.append("- Acceptance criteria (observable outcomes)")
    desc_lines.append("- Verification commands (use `uv run ...` for Python)")
    desc_lines.append("- Risks/edge cases")
    desc_lines.append(
        "- Dependencies + suggested ordering (use `loom ticket dep-add`)\n"
    )
    desc_lines.append("## Output")
    desc_lines.append("")
    desc_lines.append("When done, update THIS ticket with:")
    desc_lines.append("- Created/updated ticket IDs: [ ... ]")
    desc_lines.append("- Suggested ordering + what can run in parallel")
    desc_lines.append("")
    desc_lines.append(f"Sprint name: {sprint_name}")
    desc_lines.append(f"Sprint tag: {tag}")
    return "\n".join(desc_lines).strip()


__all__ = [
    "apply_objective_mutation",
    "build_prep_sprint_ticket_description",
    "clear_sprint_state",
    "objective_show",
    "read_text_input",
    "set_sprint_state",
    "sprint_slug",
    "sprint_state",
    "start_sprint_state",
]
