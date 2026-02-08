from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CompoundPaths:
    root: Path

    # Cognitive state
    skills_dir: Path
    memory_dir: Path
    observations_file: Path
    instincts_file: Path
    instincts_md: Path

    # Scaffold
    compound_dir: Path

    # Evidence (committed)
    loom_dir: Path
    loom_compound_dir: Path
    episodes_dir: Path
    blobs_dir: Path
    decisions_dir: Path

    # Docs
    agents_md: Path
    loom_md: Path
    roadmap_md: Path


def compound_paths(root: Path) -> CompoundPaths:
    root = root.resolve()
    skills_dir = root / ".opencode" / "skills"
    memory_dir = root / ".opencode" / "memory"
    observations_file = memory_dir / "observations.jsonl"

    compound_dir = root / ".opencode" / "compound"

    loom_dir = root / ".loom"
    loom_compound_dir = loom_dir / "compound"
    episodes_dir = loom_compound_dir / "episodes"
    blobs_dir = loom_compound_dir / "blobs"
    decisions_dir = loom_compound_dir / "decisions"

    instincts_file = loom_compound_dir / "instincts.json"
    instincts_md = loom_compound_dir / "INSTINCTS.md"

    agents_md = root / "AGENTS.md"
    loom_md = root / "LOOM.md"
    roadmap_md = loom_compound_dir / "ROADMAP.md"

    return CompoundPaths(
        root=root,
        skills_dir=skills_dir,
        memory_dir=memory_dir,
        observations_file=observations_file,
        instincts_file=instincts_file,
        instincts_md=instincts_md,
        compound_dir=compound_dir,
        loom_dir=loom_dir,
        loom_compound_dir=loom_compound_dir,
        episodes_dir=episodes_dir,
        blobs_dir=blobs_dir,
        decisions_dir=decisions_dir,
        agents_md=agents_md,
        loom_md=loom_md,
        roadmap_md=roadmap_md,
    )


def required_scaffold_paths() -> list[str]:
    # These should be installed via `loom compound init`.
    return [
        "AGENTS.md",
        "LOOM.md",
        ".loom/compound/ROADMAP.md",
        ".loom/compound/README.md",
        ".opencode/commands/workflow-plan.md",
        ".opencode/commands/workflow-work.md",
        ".opencode/commands/workflow-review.md",
        ".opencode/commands/workflow-compound.md",
        ".opencode/memory/.gitignore",
        ".opencode/compound/.gitignore",
    ]
