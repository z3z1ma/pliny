from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

from agent_loom.core.git import git_repo_root
from agent_loom.pack.core import (
    doctor,
    install_pack,
    list_packs,
    status,
    uninstall_pack,
    update_pack,
)


class ArgParseError(RuntimeError):
    pass


class PackArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:  # noqa: D401
        raise ArgParseError(message)


def _emit_json(obj: object) -> None:
    sys.stdout.write(json.dumps(obj, sort_keys=True) + "\n")


def _infer_json(argv: Sequence[str]) -> bool:
    return any(str(tok) == "--json" or str(tok).startswith("--json=") for tok in argv)


def _resolve_repo_root(repo: Optional[str]) -> Path:
    start = Path(repo).expanduser().resolve() if repo else Path.cwd().resolve()
    return (git_repo_root(start) or start).resolve()


def build_parser() -> argparse.ArgumentParser:
    p = PackArgumentParser(prog="pack", description="Packs (agents/skills/commands)")
    sub = p.add_subparsers(dest="cmd", required=True)

    lp = sub.add_parser("list", help="List available packs")
    lp.add_argument("--json", action="store_true", help="Emit machine-readable JSON")

    inst = sub.add_parser("install", help="Install a pack")
    inst.add_argument("pack_id")
    inst.add_argument(
        "--repo",
        default=None,
        help="Path inside repo (defaults to CWD; resolves git root)",
    )
    inst.add_argument("--dry-run", action="store_true")
    inst.add_argument("--force", action="store_true")
    inst.add_argument("--json", action="store_true")

    upd = sub.add_parser("update", help="Update a pack")
    upd.add_argument("pack_id")
    upd.add_argument(
        "--repo",
        default=None,
        help="Path inside repo (defaults to CWD; resolves git root)",
    )
    upd.add_argument("--dry-run", action="store_true")
    upd.add_argument("--force", action="store_true")
    upd.add_argument("--json", action="store_true")

    uninst = sub.add_parser("uninstall", help="Uninstall a pack")
    uninst.add_argument("pack_id")
    uninst.add_argument(
        "--repo",
        default=None,
        help="Path inside repo (defaults to CWD; resolves git root)",
    )
    uninst.add_argument("--dry-run", action="store_true")
    uninst.add_argument("--force", action="store_true")
    uninst.add_argument("--json", action="store_true")

    st = sub.add_parser("status", help="Show installed packs and drift summary")
    st.add_argument(
        "--repo",
        default=None,
        help="Path inside repo (defaults to CWD; resolves git root)",
    )
    st.add_argument("--json", action="store_true")

    doc = sub.add_parser("doctor", help="Verify installed pack checksums")
    doc.add_argument(
        "--repo",
        default=None,
        help="Path inside repo (defaults to CWD; resolves git root)",
    )
    doc.add_argument("--pack", default=None, help="Only check one pack")
    doc.add_argument("--json", action="store_true")

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
            "hint": "Run: loom pack -h",
        }
        if _infer_json(raw_argv):
            _emit_json(payload)
        else:
            sys.stderr.write(f"Error: {e}\n")
            sys.stderr.write("Run: loom pack -h\n")
        return 2

    if args.cmd == "list":
        packs = list_packs()
        payload = {"ok": True, "packs": [p.__dict__ for p in packs]}
        if bool(getattr(args, "json", False)):
            _emit_json(payload)
        else:
            if not packs:
                sys.stdout.write("(no packs)\n")
            for pck in packs:
                sys.stdout.write(f"{pck.id} {pck.version} - {pck.description}\n")
        return 0

    if args.cmd == "status":
        repo = _resolve_repo_root(getattr(args, "repo", None))
        payload = status(repo)
        if bool(getattr(args, "json", False)):
            _emit_json(payload)
        else:
            sys.stdout.write(json.dumps(payload, indent=2) + "\n")
        return 0

    if args.cmd == "doctor":
        repo = _resolve_repo_root(getattr(args, "repo", None))
        payload = doctor(repo, pack_id=getattr(args, "pack", None))
        if bool(getattr(args, "json", False)):
            _emit_json(payload)
        else:
            sys.stdout.write(json.dumps(payload, indent=2) + "\n")
        return 0

    if args.cmd == "install":
        repo = _resolve_repo_root(getattr(args, "repo", None))
        res = install_pack(
            repo_root=repo,
            pack_id=str(args.pack_id),
            dry_run=bool(getattr(args, "dry_run", False)),
            force=bool(getattr(args, "force", False)),
        )
        payload = res.__dict__
        if bool(getattr(args, "json", False)):
            _emit_json(payload)
        else:
            sys.stdout.write(json.dumps(payload, indent=2) + "\n")
        return 0

    if args.cmd == "update":
        repo = _resolve_repo_root(getattr(args, "repo", None))
        res = update_pack(
            repo_root=repo,
            pack_id=str(args.pack_id),
            dry_run=bool(getattr(args, "dry_run", False)),
            force=bool(getattr(args, "force", False)),
        )
        payload = res.__dict__
        if bool(getattr(args, "json", False)):
            _emit_json(payload)
        else:
            sys.stdout.write(json.dumps(payload, indent=2) + "\n")
        return 0

    if args.cmd == "uninstall":
        repo = _resolve_repo_root(getattr(args, "repo", None))
        res = uninstall_pack(
            repo_root=repo,
            pack_id=str(args.pack_id),
            dry_run=bool(getattr(args, "dry_run", False)),
            force=bool(getattr(args, "force", False)),
        )
        payload = res.__dict__
        if bool(getattr(args, "json", False)):
            _emit_json(payload)
        else:
            sys.stdout.write(json.dumps(payload, indent=2) + "\n")
        return 0

    return 2


__all__ = [
    "build_parser",
    "main",
]
