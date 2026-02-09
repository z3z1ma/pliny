from __future__ import annotations

import contextlib
import hashlib
from pathlib import Path
from typing import Iterable


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def norm_rel_path(rel: str) -> str:
    # Normalize to posix-ish relative paths for lockfiles.
    return str(rel).replace("\\", "/").lstrip("/")


def ensure_parent_dir(dest: Path, *, dry_run: bool) -> None:
    if dry_run:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)


def safe_unlink(p: Path, *, dry_run: bool) -> None:
    if dry_run:
        return
    with contextlib.suppress(FileNotFoundError):
        p.unlink()


def prune_empty_dirs(root: Path, *, touched: Iterable[Path], dry_run: bool) -> None:
    if dry_run:
        return
    # Try to remove parent dirs up to root.
    for p in sorted(
        {t.parent for t in touched}, key=lambda x: len(x.as_posix()), reverse=True
    ):
        cur = p
        while True:
            if cur == root:
                break
            with contextlib.suppress(OSError):
                cur.rmdir()
            if cur.parent == cur:
                break
            cur = cur.parent
