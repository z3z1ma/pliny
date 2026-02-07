from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from agent_loom.compound.compiler_instincts import apply_instinct_candidates
from agent_loom.compound.compiler_skills import apply_skill_candidates
from agent_loom.compound.decisions import load_decision, list_decisions
from agent_loom.compound.episodes import find_episode_by_id, load_episode
from agent_loom.compound.instincts import InstinctStore, save_instincts
from agent_loom.compound.ops import parse_ops
from agent_loom.compound.paths import compound_paths
from agent_loom.compound.scaffold import require_scaffold_installed


@dataclass(frozen=True)
class CompoundRebuildResult:
    ok: bool
    dest: str
    wrote_instincts: bool
    wrote_skills: int
    decisions_applied: int
    warnings: List[str]


def rebuild_products(
    *,
    root: Path,
    dest: Optional[Path] = None,
    clean_dest: bool = True,
    mirror_claude: bool = False,
) -> CompoundRebuildResult:
    repo = root.resolve()
    require_scaffold_installed(repo)
    paths = compound_paths(repo)

    dest_root = dest.resolve() if dest is not None else repo
    dest_paths = compound_paths(dest_root)

    warnings: List[str] = []
    if clean_dest and dest_root != repo:
        if dest_root.exists():
            shutil.rmtree(dest_root)
        dest_root.mkdir(parents=True, exist_ok=True)

    store = InstinctStore(version=1, instincts=[])
    wrote_skills = 0
    decisions_applied = 0

    for dp in list_decisions(paths.decisions_dir):
        dec = load_decision(dp)
        ep_path = find_episode_by_id(
            episodes_dir=paths.episodes_dir, episode_id=dec.episode_id
        )
        if ep_path is None:
            warnings.append(f"decision references missing episode: {dp.as_posix()}")
            continue
        ep = load_episode(ep_path)

        parsed = parse_ops(dec.ops)
        if parsed.instincts:
            apply_instinct_candidates(
                store=store,
                candidates=parsed.instincts,
                episode_id=ep.episode_id,
                episode_ts=ep.created_at,
                head_sha=ep.git.head_sha,
                patch_sha256=ep.git.patch_sha256,
            )
        if parsed.skills:
            c, u = apply_skill_candidates(
                skills_dir=dest_paths.skills_dir,
                candidates=parsed.skills,
                episode_id=ep.episode_id,
                episode_ts=ep.created_at,
                mirror_claude_dir=(dest_root / ".claude" / "skills")
                if mirror_claude
                else None,
            )
            wrote_skills += int(c + u)

        decisions_applied += 1

    if decisions_applied:
        save_instincts(dest_paths.instincts_file, store)
        wrote_instincts = True
    else:
        wrote_instincts = False

    return CompoundRebuildResult(
        ok=True,
        dest=str(dest_root),
        wrote_instincts=bool(wrote_instincts),
        wrote_skills=int(wrote_skills),
        decisions_applied=int(decisions_applied),
        warnings=warnings,
    )


__all__ = [
    "CompoundRebuildResult",
    "rebuild_products",
]
