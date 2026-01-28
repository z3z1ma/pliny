from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

from agent_loom.init.core import (
    LoomInitOptions,
    LoomInitSelection,
    resolve_root_for_init,
    run_init,
)


def _emit_json(obj: object) -> None:
    sys.stdout.write(json.dumps(obj, sort_keys=True) + "\n")


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
        choices=["repo", "poly"],
        help="Workspace init mode (repo or poly). Required for non-interactive runs.",
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
        help="Memory vault path (default: .memory)",
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
        memory_vault = ".memory"

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
            default_mode = "repo" if git_root is not None else "poly"
            while True:
                choice = (
                    _ask_text(
                        "Workspace mode (repo|poly)",
                        default=default_mode,
                    )
                    .strip()
                    .lower()
                )
                if choice in {"repo", "poly"}:
                    workspace_mode = choice
                    break
                sys.stdout.write("Please enter 'repo' or 'poly'.\n")
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

    if not interactive and do_workspace and workspace_mode not in {"repo", "poly"}:
        hint = "Pass --workspace-mode repo or --workspace-mode poly (required for non-interactive loom init)."
        if bool(args.json):
            _emit_json(
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
        _emit_json(payload)
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


__all__ = ["build_parser", "main"]
