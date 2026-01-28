from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

from agent_loom.compound.install import install_opencode
from agent_loom.compound.sync import sync as compound_sync


def _emit_json(obj: object) -> None:
    sys.stdout.write(json.dumps(obj, sort_keys=True) + "\n")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="compound", description="Loom compound integration"
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    init = sub.add_parser(
        "init",
        help="Install/upgrade the .opencode compound plugin template into a repo",
    )
    init.add_argument(
        "--dest",
        default=".",
        help="Destination project directory (default: .)",
    )
    init.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files",
    )
    init.add_argument(
        "--force",
        action="store_true",
        help="Overwrite scaffold files (.opencode plugin/commands/agents/prompts). Never overwrites skills or memory.",
    )
    init.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON",
    )

    sync = sub.add_parser(
        "sync",
        help="Stage+commit compound learning changes (skills, memory, agents, LOOM docs)",
    )
    sync.add_argument(
        "-m",
        "--message",
        default="chore: compound",
        help="Commit message (default: chore: compound)",
    )
    sync.add_argument(
        "--repo",
        default=".",
        help="Repo root (default: .)",
    )
    sync.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON",
    )

    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)

    if args.cmd == "init":
        res = install_opencode(
            dest=Path(args.dest),
            dry_run=bool(args.dry_run),
            force=bool(getattr(args, "force", False)),
        )
        payload = {
            "ok": True,
            "dest": res.dest,
            "dry_run": res.dry_run,
            "wrote": res.wrote,
            "skipped": res.skipped,
            "warnings": res.warnings,
        }
        if bool(getattr(args, "json", False)):
            _emit_json(payload)
        else:
            sys.stdout.write(f"installed into: {res.dest}\n")
            if res.dry_run:
                sys.stdout.write("(dry-run)\n")
            if res.wrote:
                sys.stdout.write("wrote:\n")
                for p in res.wrote:
                    sys.stdout.write(f"- {p}\n")
            if res.skipped:
                sys.stdout.write("skipped:\n")
                for p in res.skipped:
                    sys.stdout.write(f"- {p}\n")
            if res.warnings:
                sys.stdout.write("warnings:\n")
                for w in res.warnings:
                    sys.stdout.write(f"- {w}\n")
        return 0

    if args.cmd == "sync":
        try:
            res = compound_sync(
                repo=Path(args.repo).resolve(), message=str(args.message or "")
            )
            payload = {"ok": True, **dataclasses.asdict(res)}
            if bool(getattr(args, "json", False)):
                _emit_json(payload)
            else:
                if not res.committed:
                    sys.stdout.write("compound sync: noop\n")
                else:
                    sys.stdout.write(
                        f"compound sync: committed {res.count} file(s) sha={res.sha[:8]}\n"
                    )
            return 0
        except Exception as e:
            payload = {"ok": False, "error": str(e)}
            if bool(getattr(args, "json", False)):
                _emit_json(payload)
            else:
                sys.stderr.write(f"Error: {e}\n")
            return 1

    raise SystemExit(2)


__all__ = [
    "build_parser",
    "main",
]
