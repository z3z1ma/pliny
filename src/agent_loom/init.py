from __future__ import annotations

import argparse
import dataclasses
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from agent_loom.compound.install import install_opencode
from agent_loom.core.cli_output import emit_json
from agent_loom.core.git import git_repo_root
from agent_loom.core.time import now_iso_precise
from agent_loom.memory.core import init as memory_init
from agent_loom.team.core import init_agents
from agent_loom.ticket.core import init as ticket_init
from agent_loom.workspace.harness.core import harness_init
from agent_loom.workspace.repo.core import repo_init


def now_iso() -> str:
    return now_iso_precise()


def as_dict(obj: object) -> object:
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    return obj


@dataclass(frozen=True)
class LoomInitSelection:
    workspace: bool
    ticket: bool
    memory: bool
    compound: bool
    team: bool


@dataclass(frozen=True)
class LoomInitOptions:
    root: Path
    git_root: Optional[Path]
    workspace_mode: str  # repo|harness
    selection: LoomInitSelection
    memory_vault: str
    compound_force: bool


@dataclass(frozen=True)
class LoomInitResult:
    ok: bool
    root: str
    git: Dict[str, Any]
    selected: Dict[str, bool]
    results: Dict[str, Any]
    warnings: list[str]
    error: str
    meta: Dict[str, Any]


def detect_git_root(cwd: Path) -> Optional[Path]:
    return git_repo_root(cwd)


def resolve_root_for_init(cwd: Path) -> tuple[Path, Optional[Path]]:
    gr = detect_git_root(cwd)
    if gr is not None:
        return gr.resolve(), gr.resolve()
    return cwd.resolve(), None


def run_init(opts: LoomInitOptions) -> LoomInitResult:
    warnings: list[str] = []
    results: Dict[str, Any] = {}
    ok = True
    err = ""

    git_payload: Dict[str, Any] = {
        "ok": opts.git_root is not None,
        "repo_root": str(opts.git_root) if opts.git_root is not None else "",
    }

    ws_mode = str(opts.workspace_mode or "").strip().lower()
    if opts.selection.workspace and ws_mode not in {"repo", "harness"}:
        raise ValueError("workspace_mode must be 'repo' or 'harness'")

    # Execute in deterministic order.
    try:
        if opts.selection.workspace:
            if ws_mode == "repo":
                if opts.git_root is None:
                    raise ValueError("workspace repo init requires a git repository")
                results["workspace"] = as_dict(repo_init(root=opts.git_root))
            elif ws_mode == "harness":
                results["workspace"] = as_dict(harness_init(root=opts.root))
            else:
                raise ValueError("workspace_mode must be 'repo' or 'harness'")
        else:
            results["workspace"] = {"skipped": True}

        if opts.selection.ticket:
            results["ticket"] = as_dict(ticket_init())
        else:
            results["ticket"] = {"skipped": True}

        if opts.selection.memory:
            results["memory"] = as_dict(memory_init(vault=str(opts.memory_vault)))
        else:
            results["memory"] = {"skipped": True}

        if opts.selection.compound:
            res = install_opencode(
                dest=opts.root,
                dry_run=False,
                force=bool(opts.compound_force),
            )
            results["compound"] = {
                "dest": res.dest,
                "dry_run": res.dry_run,
                "wrote": sorted(list(res.wrote or [])),
                "skipped": sorted(list(res.skipped or [])),
                "warnings": sorted(list(res.warnings or [])),
                "force": bool(opts.compound_force),
            }
        else:
            results["compound"] = {"skipped": True}

        if opts.selection.team:
            if opts.git_root is None:
                results["team"] = {
                    "skipped": True,
                    "reason": "requires git repo",
                }
            else:
                results["team"] = as_dict(
                    init_agents(repo=opts.git_root, create_missing=True)
                )
        else:
            results["team"] = {"skipped": True}

    except Exception as e:
        ok = False
        err = str(e)

    selected = {
        "workspace": bool(opts.selection.workspace),
        "ticket": bool(opts.selection.ticket),
        "memory": bool(opts.selection.memory),
        "compound": bool(opts.selection.compound),
        "team": bool(opts.selection.team),
    }

    if isinstance(results.get("compound"), dict):
        cw = list((results.get("compound") or {}).get("warnings") or [])
        warnings.extend([str(w) for w in cw if str(w)])

    warnings = sorted({w for w in warnings if w})
    return LoomInitResult(
        ok=bool(ok),
        root=str(opts.root),
        git=git_payload,
        selected=selected,
        results=results,
        warnings=warnings,
        error=err,
        meta={"generated_at": now_iso(), "workspace_mode": ws_mode},
    )


def _isatty() -> bool:
    try:
        return bool(sys.stdin.isatty())
    except Exception:
        return False


def _ask_yes_no(prompt: str, *, default: bool) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        sys.stdout.write(f"{prompt} {suffix} ")
        sys.stdout.flush()
        s = sys.stdin.readline()
        if not s:
            return bool(default)
        s = s.strip().lower()
        if not s:
            return bool(default)
        if s in {"y", "yes"}:
            return True
        if s in {"n", "no"}:
            return False
        sys.stdout.write("Please answer y or n.\n")


def _ask_text(prompt: str, *, default: str) -> str:
    sys.stdout.write(f"{prompt} (default: {default}): ")
    sys.stdout.flush()
    s = sys.stdin.readline()
    if not s:
        return str(default)
    s = s.strip()
    return s or str(default)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="loom init",
        description="Initialize all Loom subsystems in one pass",
    )
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    p.add_argument(
        "--yes",
        action="store_true",
        help="Answer yes to all prompts (uses defaults; explicit --no-* wins)",
    )
    p.add_argument(
        "--no-input",
        action="store_true",
        help="Do not prompt (uses defaults unless overridden by flags)",
    )
    p.add_argument(
        "--workspace-mode",
        default=None,
        choices=["repo", "harness"],
        help="Workspace init mode (repo or harness). Required for non-interactive runs.",
    )

    def add_toggle(name: str, dest: str) -> None:
        g = p.add_mutually_exclusive_group()
        g.add_argument(f"--{name}", dest=dest, action="store_true", default=None)
        g.add_argument(f"--no-{name}", dest=dest, action="store_false", default=None)

    add_toggle("workspace", "do_workspace")
    add_toggle("ticket", "do_ticket")
    add_toggle("memory", "do_memory")
    add_toggle("compound", "do_compound")
    add_toggle("team", "do_team")

    p.add_argument(
        "--memory-vault",
        default="",
        help="Memory vault path (default: .loom/memory)",
    )
    p.add_argument(
        "--compound-force",
        action="store_true",
        help="Overwrite compound scaffold files (.opencode plugins/commands/agents/prompts)",
    )
    return p


def _resolve_bool(flag_value: Optional[bool], *, default: bool, yes: bool) -> bool:
    if flag_value is not None:
        return bool(flag_value)
    if yes:
        return True
    return bool(default)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)

    cwd = Path.cwd()
    root, git_root = resolve_root_for_init(cwd)

    interactive = bool(_isatty()) and not bool(args.no_input) and not bool(args.yes)
    if bool(args.json):
        interactive = False

    # Defaults: initialize everything we can.
    do_workspace = _resolve_bool(
        getattr(args, "do_workspace", None), default=True, yes=bool(args.yes)
    )
    do_ticket = _resolve_bool(
        getattr(args, "do_ticket", None), default=True, yes=bool(args.yes)
    )
    do_memory = _resolve_bool(
        getattr(args, "do_memory", None), default=True, yes=bool(args.yes)
    )
    do_compound = _resolve_bool(
        getattr(args, "do_compound", None), default=True, yes=bool(args.yes)
    )
    do_team_default = bool(git_root is not None)
    do_team_flag = getattr(args, "do_team", None)
    do_team = _resolve_bool(do_team_flag, default=do_team_default, yes=bool(args.yes))
    if git_root is None and do_team_flag is None:
        # If we're not in git, don't pretend team init was selected.
        do_team = False

    memory_vault = str(getattr(args, "memory_vault", "") or "").strip()
    if not memory_vault:
        memory_vault = ".loom/memory"

    compound_force = bool(getattr(args, "compound_force", False))

    workspace_mode = str(getattr(args, "workspace_mode", "") or "").strip().lower()

    if interactive:
        sys.stdout.write("loom init\n")
        sys.stdout.write(f"- cwd: {cwd.resolve()}\n")
        sys.stdout.write(f"- root: {root}\n")
        sys.stdout.write(f"- git: {'yes' if git_root is not None else 'no'}\n")

        do_workspace = (
            do_workspace
            if getattr(args, "do_workspace", None) is not None
            else _ask_yes_no("Initialize workspace?", default=True)
        )
        if do_workspace:
            default_mode = "repo" if git_root is not None else "harness"
            while True:
                choice = (
                    _ask_text(
                        "Workspace mode (repo|harness)",
                        default=default_mode,
                    )
                    .strip()
                    .lower()
                )
                if choice in {"repo", "harness"}:
                    workspace_mode = choice
                    break
                sys.stdout.write("Please enter 'repo' or 'harness'.\n")
        do_ticket = (
            do_ticket
            if getattr(args, "do_ticket", None) is not None
            else _ask_yes_no("Initialize tickets?", default=True)
        )
        do_memory = (
            do_memory
            if getattr(args, "do_memory", None) is not None
            else _ask_yes_no("Initialize memory?", default=True)
        )
        if do_memory and not (str(getattr(args, "memory_vault", "") or "").strip()):
            memory_vault = _ask_text("Memory vault path", default=memory_vault)

        do_compound = (
            do_compound
            if getattr(args, "do_compound", None) is not None
            else _ask_yes_no("Initialize compound integration?", default=True)
        )
        if do_compound and not compound_force:
            compound_force = _ask_yes_no(
                "Refresh compound scaffold files (safe; never overwrites skills/memory)?",
                default=False,
            )

        if git_root is None:
            sys.stdout.write("- note: team init requires git; will be skipped\n")
            do_team = False
        else:
            do_team = (
                do_team
                if getattr(args, "do_team", None) is not None
                else _ask_yes_no("Initialize team agent definitions?", default=True)
            )

        sys.stdout.write("\n")

    if not interactive and do_workspace and workspace_mode not in {"repo", "harness"}:
        hint = "Pass --workspace-mode repo or --workspace-mode harness (required for non-interactive loom init)."
        if bool(args.json):
            emit_json(
                {
                    "ok": False,
                    "cmd": "init",
                    "error": "workspace_mode is required",
                    "hint": hint,
                }
            )
        else:
            sys.stderr.write(f"Error: workspace_mode is required. {hint}\n")
        return 2

    sel = LoomInitSelection(
        workspace=bool(do_workspace),
        ticket=bool(do_ticket),
        memory=bool(do_memory),
        compound=bool(do_compound),
        team=bool(do_team),
    )
    opts = LoomInitOptions(
        root=root,
        git_root=git_root,
        workspace_mode=str(workspace_mode),
        selection=sel,
        memory_vault=str(memory_vault),
        compound_force=bool(compound_force),
    )

    res = run_init(opts)
    payload = {
        "ok": bool(res.ok),
        "cmd": "init",
        "root": res.root,
        "git": res.git,
        "selected": res.selected,
        "results": res.results,
        "warnings": res.warnings,
        "error": res.error,
        "meta": res.meta,
    }

    if bool(args.json):
        emit_json(payload)
        return 0 if res.ok else 2

    if not res.ok:
        sys.stderr.write(f"loom init failed: {res.error}\n")
        return 2

    sys.stdout.write("loom init complete\n")
    for name in ["workspace", "ticket", "memory", "compound", "team"]:
        r = res.results.get(name)
        if isinstance(r, dict) and r.get("skipped"):
            sys.stdout.write(f"- {name}: skipped\n")
        else:
            sys.stdout.write(f"- {name}: ok\n")

    if res.warnings:
        sys.stdout.write("warnings:\n")
        for w in res.warnings:
            sys.stdout.write(f"- {w}\n")
    return 0


__all__ = [
    "LoomInitOptions",
    "LoomInitResult",
    "LoomInitSelection",
    "build_parser",
    "main",
    "resolve_root_for_init",
    "run_init",
]
