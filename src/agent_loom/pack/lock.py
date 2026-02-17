from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path, PurePosixPath
from typing import Dict

from agent_loom.core.time import now_iso_precise
from agent_loom.pack.models import InstalledPack, LockFile, LockFileEntry
from agent_loom.pack.util import norm_rel_path


class LockFileError(ValueError):
    """Lockfile parse/validation error."""


def _err(msg: str) -> LockFileError:
    return LockFileError(f"invalid lock.json: {msg}")


def lock_path(repo_root: Path) -> Path:
    return repo_root / ".loom" / "pack" / "lock.json"


def _validate_entry_path(path: object) -> str:
    raw = str(path or "").strip()
    if not raw:
        raise _err("file entry path must be a non-empty string")
    normalized = norm_rel_path(raw)
    if not normalized:
        raise _err("file entry path must not resolve to empty")
    posix = PurePosixPath(normalized)
    if posix.is_absolute():
        raise _err(f"file entry path must be relative: {raw!r}")
    if any(part in {"", ".", ".."} for part in posix.parts):
        raise _err(f"file entry path is not normalized/safe: {raw!r}")
    return normalized


def _validate_entry_sha256(sha: object) -> str:
    value = str(sha or "").strip().lower()
    if len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
        raise _err("file entry sha256 must be a 64-char lowercase hex string")
    return value


def load_lock_detail(
    repo_root: Path, *, repair: bool = False, dry_run: bool = False
) -> tuple[LockFile, list[str]]:
    p = lock_path(repo_root)
    if not p.exists():
        return LockFile(version=1, packs=[]), []

    raw = p.read_text(encoding="utf-8")
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise _err(f"malformed JSON at line {exc.lineno} column {exc.colno}") from exc

    if not isinstance(doc, dict):
        raise _err("expected object")

    version_raw = doc.get("version", 1)
    if not isinstance(version_raw, int):
        raise _err("version must be an integer")
    if version_raw < 1:
        raise _err("version must be >= 1")
    version = int(version_raw)

    packs_raw = doc.get("packs")
    if packs_raw is None:
        packs_raw = []
    if not isinstance(packs_raw, list):
        raise _err("packs must be a list")

    packs: list[InstalledPack] = []
    pack_by_id: dict[str, InstalledPack] = {}
    warnings: list[str] = []

    for idx, pr in enumerate(packs_raw):
        if not isinstance(pr, dict):
            raise _err(f"pack entry at index {idx} must be an object")

        pack_id = str(pr.get("id") or "").strip()
        if not pack_id:
            raise _err(f"pack entry at index {idx} is missing non-empty id")

        pack_version = str(pr.get("version") or "").strip()
        if not pack_version:
            raise _err(f"pack {pack_id!r} is missing non-empty version")

        installed_at = str(pr.get("installed_at") or "").strip()
        if not installed_at:
            raise _err(f"pack {pack_id!r} is missing non-empty installed_at")

        files_raw = pr.get("files")
        if files_raw is None:
            files_raw = []
        if not isinstance(files_raw, list):
            raise _err(f"pack {pack_id!r} files must be a list")

        files: list[LockFileEntry] = []
        files_by_path: dict[str, str] = {}
        for file_idx, fr in enumerate(files_raw):
            if not isinstance(fr, dict):
                raise _err(
                    f"pack {pack_id!r} file entry at index {file_idx} must be an object"
                )
            path = _validate_entry_path(fr.get("path"))
            sha = _validate_entry_sha256(fr.get("sha256"))
            existing_sha = files_by_path.get(path)
            if existing_sha is not None:
                if existing_sha != sha:
                    raise _err(
                        f"pack {pack_id!r} has conflicting hashes for file path {path!r}"
                    )
                warnings.append(
                    f"deduplicated duplicate file entry in lock.json: pack={pack_id} path={path}"
                )
                continue
            files_by_path[path] = sha
            files.append(LockFileEntry(path=path, sha256=sha))

        pack = InstalledPack(
            id=pack_id,
            version=pack_version,
            installed_at=installed_at,
            files=sorted(files, key=lambda x: x.path),
        )

        existing_pack = pack_by_id.get(pack_id)
        if existing_pack is not None:
            if existing_pack != pack:
                raise _err(f"duplicate pack id {pack_id!r} has conflicting definitions")
            warnings.append(
                f"deduplicated duplicate pack entry in lock.json: pack={pack_id}"
            )
            continue

        pack_by_id[pack_id] = pack
        packs.append(pack)

    lock = LockFile(version=version, packs=sorted(packs, key=lambda x: x.id))
    deduped_warnings = sorted(set(warnings))
    if deduped_warnings and repair:
        save_lock(repo_root, lock, dry_run=dry_run)
    return lock, deduped_warnings


def load_lock(repo_root: Path) -> LockFile:
    lock, _ = load_lock_detail(repo_root)
    return lock


def save_lock(repo_root: Path, lock: LockFile, *, dry_run: bool) -> None:
    if dry_run:
        return
    p = lock_path(repo_root)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(asdict(lock), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def now_iso() -> str:
    return now_iso_precise()


def index_packs(lock: LockFile) -> Dict[str, InstalledPack]:
    return {p.id: p for p in lock.packs}


__all__ = [
    "LockFileError",
    "index_packs",
    "load_lock",
    "load_lock_detail",
    "lock_path",
    "now_iso",
    "save_lock",
]
