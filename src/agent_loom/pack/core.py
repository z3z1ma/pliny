from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from agent_loom.pack.lock import index_packs, load_lock, now_iso, save_lock
from agent_loom.pack.models import (
    InstalledPack,
    LockFile,
    LockFileEntry,
    PackApplyResult,
    PackManifest,
)
from agent_loom.pack.packs import iter_pack_files, list_pack_ids, load_manifest
from agent_loom.pack.util import (
    ensure_parent_dir,
    norm_rel_path,
    prune_empty_dirs,
    safe_unlink,
    sha256_file,
)


def _match_any(path: str, globs: List[str]) -> bool:
    for g in globs:
        if fnmatch.fnmatch(path, g):
            return True
    return False


def _managed_paths_for_pack(
    manifest: PackManifest, pack_files: Iterable[str]
) -> List[str]:
    # Primary behavior: managed_globs select which pack files are tracked.
    # (We treat these globs as repo-relative.)
    out: List[str] = []
    for rel in pack_files:
        rp = norm_rel_path(rel)
        if _match_any(rp, manifest.managed_globs):
            out.append(rp)
    return sorted(set(out))


def _build_file_index(files: Iterable[Tuple[str, Path]]) -> Dict[str, Path]:
    idx: Dict[str, Path] = {}
    for rel, p in files:
        idx[norm_rel_path(rel)] = p
    return idx


def list_packs() -> List[PackManifest]:
    return [load_manifest(pid) for pid in list_pack_ids()]


def status(repo_root: Path) -> Dict[str, object]:
    lock = load_lock(repo_root)
    packs = index_packs(lock)
    drift_total = 0
    missing_total = 0
    by_pack: List[Dict[str, object]] = []
    for ip in sorted(packs.values(), key=lambda p: p.id):
        drifted, missing = _scan_drift_missing(repo_root, ip)
        drift_total += len(drifted)
        missing_total += len(missing)
        by_pack.append(
            {
                "id": ip.id,
                "version": ip.version,
                "installed_at": ip.installed_at,
                "files": len(ip.files),
                "drifted": len(drifted),
                "missing": len(missing),
            }
        )
    return {
        "ok": True,
        "packs": by_pack,
        "drifted": drift_total,
        "missing": missing_total,
    }


def doctor(repo_root: Path, *, pack_id: Optional[str] = None) -> Dict[str, object]:
    lock = load_lock(repo_root)
    packs = index_packs(lock)
    want = [pack_id] if pack_id else sorted(packs.keys())
    results: List[Dict[str, object]] = []
    ok = True
    for pid in want:
        ip = packs.get(pid)
        if ip is None:
            ok = False
            results.append({"id": pid, "ok": False, "error": "not installed"})
            continue
        drifted, missing = _scan_drift_missing(repo_root, ip)
        if drifted or missing:
            ok = False
        results.append(
            {
                "id": pid,
                "ok": not (drifted or missing),
                "drifted": drifted,
                "missing": missing,
            }
        )
    return {"ok": ok, "results": results}


def _scan_drift_missing(
    repo_root: Path, ip: InstalledPack
) -> tuple[List[str], List[str]]:
    drifted: List[str] = []
    missing: List[str] = []
    for e in ip.files:
        p = repo_root / e.path
        if not p.exists():
            missing.append(e.path)
            continue
        if sha256_file(p) != e.sha256:
            drifted.append(e.path)
    return drifted, missing


def install_pack(
    *,
    repo_root: Path,
    pack_id: str,
    dry_run: bool,
    force: bool = False,
) -> PackApplyResult:
    manifest = load_manifest(pack_id)
    lock = load_lock(repo_root)
    packs_by_id = index_packs(lock)
    existing = packs_by_id.get(pack_id)

    pack_files = list(iter_pack_files(pack_id))
    file_index = _build_file_index(pack_files)
    managed = _managed_paths_for_pack(manifest, file_index.keys())

    wrote: List[str] = []
    skipped: List[str] = []
    drifted: List[str] = []
    missing: List[str] = []
    removed: List[str] = []
    warnings: List[str] = []

    # If already installed, treat install as update.
    if existing is not None:
        warnings.append("pack already installed; treating as update")
        return update_pack(
            repo_root=repo_root, pack_id=pack_id, dry_run=dry_run, force=force
        )

    installed_files: List[LockFileEntry] = []
    for rel in managed:
        src = file_index.get(rel)
        if src is None:
            continue
        dst = repo_root / rel

        if dst.exists() and not force:
            # Existing file that we don't own yet: don't clobber.
            skipped.append(rel)
            drifted.append(rel)
            continue

        ensure_parent_dir(dst, dry_run=dry_run)
        if not dry_run:
            dst.write_bytes(src.read_bytes())
        wrote.append(rel)
        # Record intended hash based on source.
        installed_files.append(LockFileEntry(path=rel, sha256=sha256_file(src)))

    new_pack = InstalledPack(
        id=manifest.id,
        version=manifest.version,
        installed_at=now_iso(),
        files=sorted(installed_files, key=lambda x: x.path),
    )
    lock = LockFile(
        version=lock.version, packs=sorted(lock.packs + [new_pack], key=lambda p: p.id)
    )
    save_lock(repo_root, lock, dry_run=dry_run)

    return PackApplyResult(
        ok=True,
        action="install",
        pack_id=manifest.id,
        pack_version=manifest.version,
        dest=str(repo_root),
        dry_run=bool(dry_run),
        wrote=sorted(set(wrote)),
        removed=removed,
        skipped=sorted(set(skipped)),
        drifted=sorted(set(drifted)),
        missing=missing,
        warnings=sorted(set(warnings)),
    )


def update_pack(
    *,
    repo_root: Path,
    pack_id: str,
    dry_run: bool,
    force: bool = False,
) -> PackApplyResult:
    manifest = load_manifest(pack_id)
    lock = load_lock(repo_root)
    packs_by_id = index_packs(lock)
    existing = packs_by_id.get(pack_id)
    if existing is None:
        raise FileNotFoundError(f"pack not installed: {pack_id}")

    pack_files = list(iter_pack_files(pack_id))
    file_index = _build_file_index(pack_files)
    managed = _managed_paths_for_pack(manifest, file_index.keys())

    # Compute drift per lock.
    existing_files = {e.path: e.sha256 for e in existing.files}
    drifted: List[str] = []
    missing: List[str] = []
    wrote: List[str] = []
    skipped: List[str] = []
    removed: List[str] = []
    warnings: List[str] = []

    for pth, sha in existing_files.items():
        fp = repo_root / pth
        if not fp.exists():
            missing.append(pth)
        else:
            if sha256_file(fp) != sha:
                drifted.append(pth)

    installed_files: List[LockFileEntry] = []
    for rel in managed:
        if _match_any(rel, manifest.protected_globs):
            skipped.append(rel)
            continue
        src = file_index.get(rel)
        if src is None:
            continue
        dst = repo_root / rel
        is_drift = rel in drifted
        if is_drift and not force:
            skipped.append(rel)
            continue
        ensure_parent_dir(dst, dry_run=dry_run)
        if not dry_run:
            dst.write_bytes(src.read_bytes())
        wrote.append(rel)
        installed_files.append(LockFileEntry(path=rel, sha256=sha256_file(src)))

    # Also preserve tracked files that are still on disk but not in the new pack manifest.
    # We don't remove them on update; uninstall handles removal.
    for pth, sha in existing_files.items():
        if pth in {e.path for e in installed_files}:
            continue
        installed_files.append(LockFileEntry(path=pth, sha256=sha))

    updated_pack = InstalledPack(
        id=manifest.id,
        version=manifest.version,
        installed_at=existing.installed_at or now_iso(),
        files=sorted(installed_files, key=lambda x: x.path),
    )
    new_packs = [p for p in lock.packs if p.id != manifest.id] + [updated_pack]
    lock = LockFile(version=lock.version, packs=sorted(new_packs, key=lambda p: p.id))
    save_lock(repo_root, lock, dry_run=dry_run)

    if drifted and not force:
        warnings.append("some files drifted; rerun with --force to overwrite")

    return PackApplyResult(
        ok=True,
        action="update",
        pack_id=manifest.id,
        pack_version=manifest.version,
        dest=str(repo_root),
        dry_run=bool(dry_run),
        wrote=sorted(set(wrote)),
        removed=removed,
        skipped=sorted(set(skipped)),
        drifted=sorted(set(drifted)),
        missing=sorted(set(missing)),
        warnings=sorted(set(warnings)),
    )


def uninstall_pack(
    *,
    repo_root: Path,
    pack_id: str,
    dry_run: bool,
    force: bool = False,
) -> PackApplyResult:
    manifest = load_manifest(pack_id)
    lock = load_lock(repo_root)
    packs_by_id = index_packs(lock)
    existing = packs_by_id.get(pack_id)
    if existing is None:
        raise FileNotFoundError(f"pack not installed: {pack_id}")

    drifted, missing = _scan_drift_missing(repo_root, existing)
    removed: List[str] = []
    skipped: List[str] = []
    wrote: List[str] = []
    warnings: List[str] = []
    touched: List[Path] = []

    for e in existing.files:
        p = repo_root / e.path
        if not p.exists():
            skipped.append(e.path)
            continue
        is_drift = e.path in drifted
        if is_drift and not force:
            skipped.append(e.path)
            continue
        if _match_any(e.path, manifest.protected_globs):
            skipped.append(e.path)
            continue
        safe_unlink(p, dry_run=dry_run)
        removed.append(e.path)
        touched.append(p)

    prune_empty_dirs(repo_root, touched=touched, dry_run=dry_run)

    # Remove from lock
    lock = LockFile(
        version=lock.version, packs=[p for p in lock.packs if p.id != pack_id]
    )
    save_lock(repo_root, lock, dry_run=dry_run)

    if drifted and not force:
        warnings.append("some files drifted; rerun with --force to remove")

    return PackApplyResult(
        ok=True,
        action="uninstall",
        pack_id=manifest.id,
        pack_version=manifest.version,
        dest=str(repo_root),
        dry_run=bool(dry_run),
        wrote=wrote,
        removed=sorted(set(removed)),
        skipped=sorted(set(skipped)),
        drifted=sorted(set(drifted)),
        missing=sorted(set(missing)),
        warnings=sorted(set(warnings)),
    )
