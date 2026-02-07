from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from agent_loom.compound.episodes import load_episode
from agent_loom.compound.paths import compound_paths
from agent_loom.compound.scaffold import require_scaffold_installed


@dataclass(frozen=True)
class CompoundDoctorResult:
    ok: bool
    errors: List[str]
    warnings: List[str]


def doctor(*, root: Path) -> CompoundDoctorResult:
    repo = root.resolve()
    require_scaffold_installed(repo)
    paths = compound_paths(repo)

    errors: List[str] = []
    warnings: List[str] = []

    if paths.episodes_dir.exists():
        for p in sorted(paths.episodes_dir.rglob("*.json")):
            if not p.is_file():
                continue
            try:
                ep = load_episode(p)
            except Exception as e:
                errors.append(f"episode load failed: {p.as_posix()}: {e}")
                continue

            if ep.git.patch_omitted:
                if not str(ep.git.patch_blob_sha256 or "").strip():
                    errors.append(f"episode missing patch blob sha256: {p.as_posix()}")
                    continue
                blob = paths.blobs_dir / f"{ep.git.patch_blob_sha256}.diff"
                if not blob.exists():
                    warnings.append(
                        f"episode references missing patch blob: {blob.as_posix()}"
                    )

    ok = not errors
    return CompoundDoctorResult(ok=ok, errors=errors, warnings=warnings)


__all__ = [
    "CompoundDoctorResult",
    "doctor",
]
