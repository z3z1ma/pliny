from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from agent_loom.pack.models import InstalledPack, LockFile, LockFileEntry


def lock_path(repo_root: Path) -> Path:
    return repo_root / ".loom" / "pack" / "lock.json"


def load_lock(repo_root: Path) -> LockFile:
    p = lock_path(repo_root)
    if not p.exists():
        return LockFile(version=1, packs=[])
    raw = p.read_text(encoding="utf-8")
    doc = json.loads(raw)
    if not isinstance(doc, dict):
        raise ValueError("invalid lock.json: expected object")
    version = int(doc.get("version") or 1)
    packs_raw = doc.get("packs")
    if packs_raw is None:
        packs_raw = []
    if not isinstance(packs_raw, list):
        raise ValueError("invalid lock.json: packs must be a list")
    packs: list[InstalledPack] = []
    for pr in packs_raw:
        if not isinstance(pr, dict):
            continue
        files_raw = pr.get("files") or []
        files: list[LockFileEntry] = []
        if isinstance(files_raw, list):
            for fr in files_raw:
                if not isinstance(fr, dict):
                    continue
                path = str(fr.get("path") or "").strip()
                sha = str(fr.get("sha256") or "").strip()
                if path and sha:
                    files.append(LockFileEntry(path=path, sha256=sha))
        packs.append(
            InstalledPack(
                id=str(pr.get("id") or "").strip(),
                version=str(pr.get("version") or "").strip(),
                installed_at=str(pr.get("installed_at") or "").strip(),
                files=files,
            )
        )
    packs = [p for p in packs if p.id]
    return LockFile(version=version, packs=packs)


def save_lock(repo_root: Path, lock: LockFile, *, dry_run: bool) -> None:
    if dry_run:
        return
    p = lock_path(repo_root)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(asdict(lock), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def index_packs(lock: LockFile) -> Dict[str, InstalledPack]:
    return {p.id: p for p in lock.packs}
