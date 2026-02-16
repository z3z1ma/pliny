from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
from importlib import resources
from pathlib import Path
from typing import Optional, Sequence

from agent_loom.compound.evolve import evolve_instincts
from agent_loom.compound.hooks import run_claude_hook, run_omp_hook, run_opencode_hook
from agent_loom.compound.import_export import export_instincts, instinct_import
from agent_loom.compound.install import COMPOUND_PACK_ID, install_opencode
from agent_loom.compound.observer import (
    observer_status,
    run_observer_once,
    start_observer,
    stop_observer,
)
from agent_loom.compound.sync import sync as compound_sync
from agent_loom.core.cli_args import (
    ArgParseError,
    StrictArgumentParser,
    argv_requests_json,
)
from agent_loom.core.cli_output import emit_json
from agent_loom.core.git import resolve_repo_root
from agent_loom.pack.diff import any_pack_diffs, diff_pack_files


class CompoundArgumentParser(StrictArgumentParser):
    pass


def _resolve_repo_root(repo: Optional[str]) -> Path:
    cr = str(os.environ.get("COMPOUND_ROOT") or "").strip()
    if cr:
        p = Path(cr).expanduser().resolve()
        if p.exists() and p.is_dir():
            return p

    return resolve_repo_root(repo)


def _resolve_init_dest(dest: Optional[str]) -> Path:
    d = str(dest or ".").strip() or "."
    if d == ".":
        return resolve_repo_root(Path.cwd())
    return Path(d).expanduser().resolve()


def _infer_json(argv: Sequence[str]) -> bool:
    return argv_requests_json(argv)


def _echo_claude_payload(payload_raw: str, stdin_text: str) -> None:
    text = (
        str(payload_raw or "")
        if str(payload_raw or "").strip()
        else str(stdin_text or "")
    )
    text = text if str(text).strip() else "{}"
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")


def build_parser() -> argparse.ArgumentParser:
    p = CompoundArgumentParser(prog="compound", description="Loom compound integration")
    sub = p.add_subparsers(dest="cmd", required=True)

    init = sub.add_parser(
        "init",
        help="Install/upgrade the compound adapter scaffolds (.claude, .opencode, .omp) into a repo",
    )
    init.add_argument(
        "--dest",
        default=".",
        help="Destination project directory (default: repo root if in git, else .)",
    )
    init.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files",
    )
    init.add_argument(
        "--force",
        action="store_true",
        help="Overwrite scaffold files (adapters, commands, and docs). Never overwrites skills or memory.",
    )
    init.add_argument(
        "--diff", action="store_true", help="Show diffs for skipped pack files"
    )
    init.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON",
    )

    sync = sub.add_parser(
        "sync",
        help="Stage+commit compound-owned changes (LOOM.md and .loom/compound)",
    )
    sync.add_argument(
        "-m",
        "--message",
        default="chore: compound",
        help="Commit message (default: chore: compound)",
    )
    sync.add_argument(
        "--repo",
        default=None,
        help="Path inside repo (defaults to CWD; resolves git root)",
    )
    sync.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON",
    )

    instincts = sub.add_parser(
        "instincts-update",
        help="Ingest observations and use headless LLM derivation to upsert instincts",
    )
    instincts.add_argument(
        "--repo",
        default=None,
        help="Path inside repo (defaults to CWD; resolves git root)",
    )
    instincts.add_argument(
        "--auto",
        action="store_true",
        help="Apply auto threshold gating for background execution",
    )
    instincts.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without writing files",
    )
    instincts.add_argument(
        "--min-new-observations",
        type=int,
        default=None,
        help="Minimum new observations required in --auto mode (default: COMPOUND_INSTINCTS_MIN_NEW_OBSERVATIONS or 12)",
    )
    instincts.add_argument(
        "--min-occurrences",
        type=int,
        default=3,
        help="Minimum repeated pattern count hint passed to the LLM (default: 3)",
    )
    instincts.add_argument(
        "--max-candidates",
        type=int,
        default=12,
        help="Maximum instinct candidates processed per run (default: 12)",
    )
    instincts.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON",
    )

    instinct_status = sub.add_parser(
        "instinct-status",
        help="Show current instincts and observer status",
    )
    instinct_status.add_argument(
        "--repo",
        default=None,
        help="Path inside repo (defaults to CWD; resolves git root)",
    )
    instinct_status.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON"
    )

    instinct_export = sub.add_parser(
        "instinct-export",
        help="Export instincts to a JSON bundle",
    )
    instinct_export.add_argument("--repo", default=None, help="Path inside repo")
    instinct_export.add_argument("--out", required=True, help="Output file path")
    instinct_export.add_argument("--min-confidence", type=float, default=0.0)
    instinct_export.add_argument("--domain", default="")
    instinct_export.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON"
    )

    instinct_import_cmd = sub.add_parser(
        "instinct-import",
        help="Import instincts from a file path or URL",
    )
    instinct_import_cmd.add_argument("source", help="Source file path or URL")
    instinct_import_cmd.add_argument("--repo", default=None, help="Path inside repo")
    instinct_import_cmd.add_argument("--dry-run", action="store_true")
    instinct_import_cmd.add_argument("--force", action="store_true")
    instinct_import_cmd.add_argument("--min-confidence", type=float, default=0.0)
    instinct_import_cmd.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON"
    )

    evolve = sub.add_parser(
        "evolve",
        help="Cluster instincts and emit evolved skills/commands/agents",
    )
    evolve.add_argument("--repo", default=None, help="Path inside repo")
    evolve.add_argument("--threshold", type=float, default=0.75)
    evolve.add_argument("--generate", action="store_true")
    evolve.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON"
    )

    observer = sub.add_parser(
        "observer", help="Manage the background instincts observer"
    )
    observer_sub = observer.add_subparsers(dest="observer_cmd", required=True)
    for name in ["start", "stop", "status", "run-once"]:
        op = observer_sub.add_parser(name)
        op.add_argument("--repo", default=None, help="Path inside repo")
        op.add_argument(
            "--json", action="store_true", help="Emit machine-readable JSON"
        )

    prime = sub.add_parser(
        "prime",
        help="Print the Compound cookbook (module README)",
    )
    prime.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON",
    )

    claude_hook = sub.add_parser(
        "claude-hook",
        help="Process a Claude Code hook event (logs observation)",
    )
    claude_hook.add_argument(
        "--repo",
        default=None,
        help="Path inside repo (defaults to CWD; resolves git root)",
    )
    claude_hook.add_argument(
        "--event",
        default="",
        help="Hook event override (defaults to payload.hook_event_name)",
    )
    claude_hook.add_argument(
        "--payload",
        default="",
        help="Optional JSON payload override (otherwise reads stdin)",
    )
    claude_hook.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON (non-Claude hooks only)",
    )

    opencode_hook = sub.add_parser(
        "opencode-hook",
        help="Process an OpenCode adapter event (logs observation)",
    )
    opencode_hook.add_argument(
        "--repo",
        default=None,
        help="Path inside repo (defaults to CWD; resolves git root)",
    )
    opencode_hook.add_argument(
        "--event",
        default="",
        help="Event override (defaults to payload.type)",
    )
    opencode_hook.add_argument(
        "--payload",
        default="",
        help="Optional JSON payload override (otherwise reads stdin)",
    )
    opencode_hook.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON",
    )

    omp_hook = sub.add_parser(
        "omp-hook",
        help="Process an OMP adapter event (logs observation)",
    )
    omp_hook.add_argument(
        "--repo",
        default=None,
        help="Path inside repo (defaults to CWD; resolves git root)",
    )
    omp_hook.add_argument(
        "--event",
        default="",
        help="Event override (defaults to payload.event_name)",
    )
    omp_hook.add_argument(
        "--payload",
        default="",
        help="Optional JSON payload override (otherwise reads stdin)",
    )
    omp_hook.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON",
    )

    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    raw_argv = list(argv) if argv is not None else sys.argv[1:]
    try:
        args = build_parser().parse_args(
            list(raw_argv) if raw_argv is not None else None
        )
    except SystemExit as e:
        return int(e.code or 0)
    except ArgParseError as e:
        payload = {
            "ok": False,
            "code": "ARGPARSE",
            "error": str(e),
            "hint": "Run: loom compound -h",
        }
        if _infer_json(raw_argv):
            emit_json(payload)
        else:
            sys.stderr.write(f"Error: {e}\n")
            sys.stderr.write("Run: loom compound -h\n")
        return 2

    if args.cmd == "init":
        try:
            res = install_opencode(
                dest=_resolve_init_dest(getattr(args, "dest", None)),
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
                emit_json(payload)
            else:
                sys.stdout.write(f"installed into: {res.dest}\n")
                sys.stdout.write(f"pack: {COMPOUND_PACK_ID}\n")
                sys.stdout.write("note: commit .loom/pack/lock.json\n")
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

                repo_root = Path(res.dest).resolve()
                diff_targets = sorted(set(list(res.skipped or [])))
                if (
                    diff_targets
                    and not bool(getattr(args, "diff", False))
                    and any_pack_diffs(
                        repo_root=repo_root,
                        pack_id=COMPOUND_PACK_ID,
                        relpaths=diff_targets,
                    )
                ):
                    sys.stdout.write(
                        "note: some skipped pack files differ from Loom scaffold; rerun with --diff to view\n"
                    )
                if bool(getattr(args, "diff", False)) and not bool(res.dry_run):
                    diffs = diff_pack_files(
                        repo_root=repo_root,
                        pack_id=COMPOUND_PACK_ID,
                        relpaths=diff_targets,
                        max_lines=400,
                    )
                    for d in diffs:
                        sys.stdout.write(f"diff (skipped): {d.relpath}\n")
                        sys.stdout.write(d.diff)
            return 0
        except Exception as e:
            payload = {"ok": False, "error": str(e)}
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stderr.write(f"Error: {e}\n")
            return 1

    if args.cmd == "sync":
        try:
            res = compound_sync(
                repo=_resolve_repo_root(getattr(args, "repo", None)),
                message=str(args.message or ""),
            )
            payload = {"ok": True, **dataclasses.asdict(res)}
            if bool(getattr(args, "json", False)):
                emit_json(payload)
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
                emit_json(payload)
            else:
                sys.stderr.write(f"Error: {e}\n")
            return 1

    if args.cmd == "instincts-update":
        repo = _resolve_repo_root(getattr(args, "repo", None))
        try:
            from agent_loom.compound.engine import run_instincts_update

            min_new_observations = getattr(args, "min_new_observations", None)
            if min_new_observations is None:
                min_new_observations = int(
                    os.environ.get("COMPOUND_INSTINCTS_MIN_NEW_OBSERVATIONS", "12")
                )

            res = run_instincts_update(
                root=repo,
                auto=bool(getattr(args, "auto", False)),
                dry_run=bool(getattr(args, "dry_run", False)),
                min_new_observations=int(min_new_observations),
                min_occurrences=int(getattr(args, "min_occurrences", 3) or 3),
                max_candidates=int(getattr(args, "max_candidates", 12) or 12),
            )
            payload = dataclasses.asdict(res)
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stdout.write(json.dumps(payload, indent=2) + "\n")
            return 0
        except Exception as e:
            payload = {"ok": False, "error": str(e)}
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stderr.write(f"Error: {e}\n")
            return 1

    if args.cmd == "instinct-status":
        repo = _resolve_repo_root(getattr(args, "repo", None))
        try:
            from agent_loom.compound.instincts import load_instincts
            from agent_loom.compound.paths import compound_paths

            paths = compound_paths(repo)
            store = load_instincts(paths.instincts_file)
            status = observer_status(repo=repo)
            active = [i for i in store.instincts if i.status == "active"]
            payload = {
                "ok": True,
                "repo": str(repo),
                "instincts_total": len(store.instincts),
                "instincts_active": len(active),
                "observer": dataclasses.asdict(status),
            }
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stdout.write(json.dumps(payload, indent=2) + "\n")
            return 0
        except Exception as e:
            payload = {"ok": False, "error": str(e)}
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stderr.write(f"Error: {e}\n")
            return 1

    if args.cmd == "instinct-export":
        repo = _resolve_repo_root(getattr(args, "repo", None))
        try:
            from agent_loom.compound.paths import compound_paths

            paths = compound_paths(repo)
            res = export_instincts(
                instincts_file=paths.instincts_file,
                out_file=Path(str(args.out)).expanduser().resolve(),
                min_confidence=float(getattr(args, "min_confidence", 0.0) or 0.0),
                domain=str(getattr(args, "domain", "") or ""),
            )
            payload = dataclasses.asdict(res)
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stdout.write(json.dumps(payload, indent=2) + "\n")
            return 0
        except Exception as e:
            payload = {"ok": False, "error": str(e)}
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stderr.write(f"Error: {e}\n")
            return 1

    if args.cmd == "instinct-import":
        repo = _resolve_repo_root(getattr(args, "repo", None))
        try:
            from agent_loom.compound.paths import compound_paths

            paths = compound_paths(repo)
            res = instinct_import(
                instincts_file=paths.instincts_file,
                source=str(args.source),
                dry_run=bool(getattr(args, "dry_run", False)),
                force=bool(getattr(args, "force", False)),
                min_confidence=float(getattr(args, "min_confidence", 0.0) or 0.0),
            )
            payload = dataclasses.asdict(res)
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stdout.write(json.dumps(payload, indent=2) + "\n")
            return 0
        except Exception as e:
            payload = {"ok": False, "error": str(e)}
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stderr.write(f"Error: {e}\n")
            return 1

    if args.cmd == "evolve":
        repo = _resolve_repo_root(getattr(args, "repo", None))
        try:
            res = evolve_instincts(
                root=repo,
                threshold=float(getattr(args, "threshold", 0.75) or 0.75),
                generate=bool(getattr(args, "generate", False)),
            )
            payload = dataclasses.asdict(res)
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stdout.write(json.dumps(payload, indent=2) + "\n")
            return 0
        except Exception as e:
            payload = {"ok": False, "error": str(e)}
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stderr.write(f"Error: {e}\n")
            return 1

    if args.cmd == "observer":
        repo = _resolve_repo_root(getattr(args, "repo", None))
        try:
            if args.observer_cmd == "start":
                res = start_observer(repo=repo)
            elif args.observer_cmd == "stop":
                res = stop_observer(repo=repo)
            elif args.observer_cmd == "status":
                res = observer_status(repo=repo)
            else:
                res = run_observer_once(repo=repo)
            payload = dataclasses.asdict(res)
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stdout.write(json.dumps(payload, indent=2) + "\n")
            return 0
        except Exception as e:
            payload = {"ok": False, "error": str(e)}
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stderr.write(f"Error: {e}\n")
            return 1

    if args.cmd == "prime":
        traversable = resources.files("agent_loom.compound").joinpath("README.md")
        with resources.as_file(traversable) as p:
            md = p.read_text(encoding="utf-8", errors="replace")
        payload = {"ok": True, "markdown": md}
        if bool(getattr(args, "json", False)):
            emit_json(payload)
        else:
            sys.stdout.write(str(md).rstrip() + "\n")
        return 0

    if args.cmd in {"claude-hook", "opencode-hook", "omp-hook"}:
        repo = _resolve_repo_root(getattr(args, "repo", None))
        try:
            payload_raw = str(getattr(args, "payload", "") or "")
            event_raw = str(getattr(args, "event", "") or "")
            stdin_text = (
                ""
                if payload_raw
                else (
                    sys.stdin.read()
                    if sys.stdin is not None and not sys.stdin.isatty()
                    else ""
                )
            )
            if args.cmd == "claude-hook":
                res = run_claude_hook(
                    repo=repo,
                    stdin_text=stdin_text,
                    payload_json=payload_raw,
                    event=event_raw,
                )
                _echo_claude_payload(payload_raw, stdin_text)
            elif args.cmd == "opencode-hook":
                res = run_opencode_hook(
                    repo=repo,
                    stdin_text=stdin_text,
                    payload_json=payload_raw,
                    event=event_raw,
                )
                if bool(getattr(args, "json", False)):
                    emit_json(dataclasses.asdict(res))
            else:
                res = run_omp_hook(
                    repo=repo,
                    stdin_text=stdin_text,
                    payload_json=payload_raw,
                    event=event_raw,
                )
                if bool(getattr(args, "json", False)):
                    emit_json(dataclasses.asdict(res))
            return 0 if bool(res.ok) else 1
        except Exception as e:
            payload = {"ok": False, "error": str(e)}
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stderr.write(f"Error: {e}\n")
            return 1
    return 2


__all__ = [
    "build_parser",
    "main",
]
