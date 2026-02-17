from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

from agent_loom.core.cli_args import (
    ArgParseError,
    StrictArgumentParser,
    argv_requests_json,
)
from agent_loom.core.cli_output import emit_json
from agent_loom.core.git import resolve_repo_root
from agent_loom.pack.core import (
    doctor,
    install_pack,
    list_packs,
    status,
    uninstall_pack,
    update_pack,
)
from agent_loom.pack.diff import diff_pack_file, diff_pack_files
from agent_loom.pack.lock import LockFileError


class PackArgumentParser(StrictArgumentParser):
    pass


def _infer_json(argv: Sequence[str]) -> bool:
    return argv_requests_json(argv)


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
    inst.add_argument(
        "--diff",
        action="store_true",
        help="Show unified diffs for drifted files skipped during install/update",
    )

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
    upd.add_argument(
        "--diff",
        action="store_true",
        help="Show unified diffs for drifted files skipped during update",
    )

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
    uninst.add_argument(
        "--diff",
        action="store_true",
        help="Show unified diffs for drifted files before forced uninstall",
    )

    st = sub.add_parser("status", help="Show installed packs and drift summary")
    st.add_argument(
        "--repo",
        default=None,
        help="Path inside repo (defaults to CWD; resolves git root)",
    )
    st.add_argument(
        "--diff",
        action="store_true",
        help="Show unified diffs for drifted managed files",
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


def _status_diff_items(
    *, repo_root: Path, max_lines: int = 400
) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    doc = doctor(repo_root)
    results = doc.get("results") if isinstance(doc, dict) else None
    if not isinstance(results, list):
        return items
    for r in results:
        if not isinstance(r, dict):
            continue
        pid = str(r.get("id") or "").strip()
        if not pid:
            continue
        drifted = r.get("drifted")
        if not isinstance(drifted, list):
            continue
        for rel in drifted:
            rp = str(rel or "").strip()
            if not rp:
                continue
            d = diff_pack_file(
                repo_root=repo_root,
                pack_id=pid,
                relpath=rp,
                max_lines=max_lines,
            )
            items.append(
                {
                    "pack_id": pid,
                    "relpath": rp,
                    "ok": bool(d is not None and bool(getattr(d, "diff", "").strip())),
                    "diff": ("" if d is None else d.diff),
                }
            )
    return items


def _result_diffs(
    *, repo_root: Path, pack_id: str, relpaths: list[str], max_lines: int = 400
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for d in diff_pack_files(
        repo_root=repo_root,
        pack_id=pack_id,
        relpaths=relpaths,
        max_lines=max_lines,
    ):
        out.append(
            {
                "pack_id": pack_id,
                "relpath": d.relpath,
                "ok": bool(str(d.diff or "").strip()),
                "diff": d.diff,
            }
        )
    return out


def _print_drift_guidance(*, cmd: str, pack_id: str, drifted_count: int) -> None:
    if drifted_count <= 0:
        return
    sys.stdout.write("\n")
    sys.stdout.write(
        "IMPORTANT: pack has proposed updates to existing files that were NOT applied.\n"
    )
    sys.stdout.write(f"drifted files: {int(drifted_count)}\n")
    sys.stdout.write(f"review intended changes: loom pack {cmd} {pack_id} --diff\n")
    sys.stdout.write(f"apply overwrites: loom pack {cmd} {pack_id} --force\n")


def _emit_runtime_error(
    *, json_output: bool, code: str, error: str, hint: str = ""
) -> int:
    payload = {"ok": False, "code": code, "error": error}
    if hint:
        payload["hint"] = hint
    if json_output:
        emit_json(payload)
    else:
        sys.stderr.write(f"Error: {error}\n")
        if hint:
            sys.stderr.write(f"{hint}\n")
    return 2


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
            emit_json(payload)
        else:
            sys.stderr.write(f"Error: {e}\n")
            sys.stderr.write("Run: loom pack -h\n")
        return 2

    try:
        if args.cmd == "list":
            packs = list_packs()
            payload = {"ok": True, "packs": [p.__dict__ for p in packs]}
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                if not packs:
                    sys.stdout.write("(no packs)\n")
                for pck in packs:
                    sys.stdout.write(f"{pck.id} {pck.version} - {pck.description}\n")
            return 0

        if args.cmd == "status":
            repo = resolve_repo_root(getattr(args, "repo", None))
            payload = status(repo)
            want_diff = bool(getattr(args, "diff", False))
            if bool(getattr(args, "json", False)):
                if want_diff:
                    payload = {**payload, "diffs": _status_diff_items(repo_root=repo)}
                emit_json(payload)
            else:
                sys.stdout.write(json.dumps(payload, indent=2) + "\n")
                drifted_val = payload.get("drifted")
                drifted = int(drifted_val) if isinstance(drifted_val, int) else 0
                if drifted and not want_diff:
                    sys.stdout.write(
                        "note: some pack files drifted; rerun with --diff to view diffs\n"
                    )
                if want_diff and drifted:
                    sys.stdout.write("\n")
                    for it in _status_diff_items(repo_root=repo):
                        sys.stdout.write(
                            f"diff (drifted): {it.get('pack_id')}/{it.get('relpath')}\n"
                        )
                        if bool(it.get("ok")) and str(it.get("diff") or "").strip():
                            sys.stdout.write(str(it.get("diff") or ""))
                        else:
                            sys.stdout.write("(diff unavailable)\n")
            return 0

        if args.cmd == "doctor":
            repo = resolve_repo_root(getattr(args, "repo", None))
            payload = doctor(repo, pack_id=getattr(args, "pack", None))
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stdout.write(json.dumps(payload, indent=2) + "\n")
            return 0

        if args.cmd == "install":
            repo = resolve_repo_root(getattr(args, "repo", None))
            res = install_pack(
                repo_root=repo,
                pack_id=str(args.pack_id),
                dry_run=bool(getattr(args, "dry_run", False)),
                force=bool(getattr(args, "force", False)),
            )
            want_diff = bool(getattr(args, "diff", False))
            diffs = (
                _result_diffs(
                    repo_root=repo,
                    pack_id=str(args.pack_id),
                    relpaths=list(res.drifted or []),
                )
                if want_diff
                else []
            )
            payload = {**res.__dict__, **({"diffs": diffs} if want_diff else {})}
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stdout.write(json.dumps(payload, indent=2) + "\n")
                sys.stdout.write("note: commit .loom/pack/lock.json\n")
                drifted = len(list(res.drifted or []))
                if drifted and not want_diff:
                    _print_drift_guidance(
                        cmd="install", pack_id=str(args.pack_id), drifted_count=drifted
                    )
                if want_diff and drifted:
                    sys.stdout.write("\n")
                    for it in diffs:
                        sys.stdout.write(
                            f"diff (drifted): {it.get('pack_id')}/{it.get('relpath')}\n"
                        )
                        if bool(it.get("ok")) and str(it.get("diff") or "").strip():
                            sys.stdout.write(str(it.get("diff") or ""))
                        else:
                            sys.stdout.write("(diff unavailable)\n")
            return 0

        if args.cmd == "update":
            repo = resolve_repo_root(getattr(args, "repo", None))
            res = update_pack(
                repo_root=repo,
                pack_id=str(args.pack_id),
                dry_run=bool(getattr(args, "dry_run", False)),
                force=bool(getattr(args, "force", False)),
            )
            want_diff = bool(getattr(args, "diff", False))
            diffs = (
                _result_diffs(
                    repo_root=repo,
                    pack_id=str(args.pack_id),
                    relpaths=list(res.drifted or []),
                )
                if want_diff
                else []
            )
            payload = {**res.__dict__, **({"diffs": diffs} if want_diff else {})}
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stdout.write(json.dumps(payload, indent=2) + "\n")
                sys.stdout.write("note: commit .loom/pack/lock.json\n")
                drifted = len(list(res.drifted or []))
                if drifted and not want_diff:
                    _print_drift_guidance(
                        cmd="update", pack_id=str(args.pack_id), drifted_count=drifted
                    )
                if want_diff and drifted:
                    sys.stdout.write("\n")
                    for it in diffs:
                        sys.stdout.write(
                            f"diff (drifted): {it.get('pack_id')}/{it.get('relpath')}\n"
                        )
                        if bool(it.get("ok")) and str(it.get("diff") or "").strip():
                            sys.stdout.write(str(it.get("diff") or ""))
                        else:
                            sys.stdout.write("(diff unavailable)\n")
            return 0

        if args.cmd == "uninstall":
            repo = resolve_repo_root(getattr(args, "repo", None))
            res = uninstall_pack(
                repo_root=repo,
                pack_id=str(args.pack_id),
                dry_run=bool(getattr(args, "dry_run", False)),
                force=bool(getattr(args, "force", False)),
            )
            want_diff = bool(getattr(args, "diff", False))
            diffs = (
                _result_diffs(
                    repo_root=repo,
                    pack_id=str(args.pack_id),
                    relpaths=list(res.drifted or []),
                )
                if want_diff
                else []
            )
            payload = {**res.__dict__, **({"diffs": diffs} if want_diff else {})}
            if bool(getattr(args, "json", False)):
                emit_json(payload)
            else:
                sys.stdout.write(json.dumps(payload, indent=2) + "\n")
                sys.stdout.write("note: commit .loom/pack/lock.json\n")
                drifted = len(list(res.drifted or []))
                if drifted and not want_diff:
                    _print_drift_guidance(
                        cmd="uninstall",
                        pack_id=str(args.pack_id),
                        drifted_count=drifted,
                    )
                if want_diff and drifted:
                    sys.stdout.write("\n")
                    for it in diffs:
                        sys.stdout.write(
                            f"diff (drifted): {it.get('pack_id')}/{it.get('relpath')}\n"
                        )
                        if bool(it.get("ok")) and str(it.get("diff") or "").strip():
                            sys.stdout.write(str(it.get("diff") or ""))
                        else:
                            sys.stdout.write("(diff unavailable)\n")
            return 0
    except LockFileError as e:
        return _emit_runtime_error(
            json_output=bool(getattr(args, "json", False)),
            code="LOCK_INVALID",
            error=str(e),
            hint="Fix .loom/pack/lock.json, then rerun. `loom pack doctor` can auto-repair safe duplicate entries.",
        )
    except FileNotFoundError as e:
        return _emit_runtime_error(
            json_output=bool(getattr(args, "json", False)),
            code="NOT_FOUND",
            error=str(e),
        )
    except ValueError as e:
        return _emit_runtime_error(
            json_output=bool(getattr(args, "json", False)),
            code="ARG",
            error=str(e),
            hint="Run: loom pack -h",
        )
    return 2


__all__ = [
    "build_parser",
    "main",
]
