from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANONICAL_PATHS = ("SKILL.md", "autoresearch/program.md")


class CanonicalGuardError(ValueError):
    pass


@dataclass(frozen=True)
class CanonicalFile:
    path: str
    sha256: str
    byte_length: int


def snapshot(
    repo_root: str | Path = REPO_ROOT,
    paths: tuple[str, ...] = DEFAULT_CANONICAL_PATHS,
) -> dict[str, CanonicalFile]:
    root = Path(repo_root)
    result = {}
    for relative in paths:
        path = root / relative
        try:
            data = path.read_bytes()
        except FileNotFoundError as exc:
            raise CanonicalGuardError(f"canonical file missing: {relative}") from exc
        result[relative] = CanonicalFile(
            path=relative,
            sha256=hashlib.sha256(data).hexdigest(),
            byte_length=len(data),
        )
    return result


def diff_snapshots(
    before: dict[str, CanonicalFile],
    after: dict[str, CanonicalFile],
) -> list[str]:
    changed = []
    for path, before_file in before.items():
        after_file = after.get(path)
        if after_file is None:
            changed.append(path)
        elif before_file.sha256 != after_file.sha256:
            changed.append(path)
    for path in after:
        if path not in before:
            changed.append(path)
    return sorted(changed)


def require_clean_git(
    repo_root: str | Path = REPO_ROOT,
    paths: tuple[str, ...] = DEFAULT_CANONICAL_PATHS,
) -> None:
    root = Path(repo_root)
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--", *paths],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise CanonicalGuardError(completed.stderr.strip() or "git status failed")
    dirty = [line for line in completed.stdout.splitlines() if line.strip()]
    if dirty:
        raise CanonicalGuardError(
            "canonical files are not clean in git: " + "; ".join(dirty)
        )


def write_guard_report(
    out_path: str | Path,
    *,
    before: dict[str, CanonicalFile],
    after: dict[str, CanonicalFile],
    require_clean: bool,
) -> Path:
    changed = diff_snapshots(before, after)
    data = {
        "schema_version": 1,
        "canonical_paths": sorted(before),
        "require_clean_canonical": require_clean,
        "unchanged_during_run": not changed,
        "changed_paths": changed,
        "before": _snapshot_json(before),
        "after": _snapshot_json(after),
        "limits": [
            "This guard proves the checked canonical files did not change during this one command.",
            "Use --require-clean-canonical after committing setup to fail if canonical files are dirty before a run.",
        ],
    }
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check canonical autoresearch files before a run."
    )
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--require-clean", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.require_clean:
            require_clean_git(args.root)
        current = snapshot(args.root)
        payload: dict[str, Any] = {
            "schema_version": 1,
            "canonical_paths": sorted(current),
            "snapshot": _snapshot_json(current),
        }
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(payload, indent=2))
    except (OSError, CanonicalGuardError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


def _snapshot_json(snapshot_data: dict[str, CanonicalFile]) -> dict[str, dict[str, Any]]:
    return {
        path: {
            "sha256": item.sha256,
            "byte_length": item.byte_length,
        }
        for path, item in sorted(snapshot_data.items())
    }


if __name__ == "__main__":
    raise SystemExit(main())
