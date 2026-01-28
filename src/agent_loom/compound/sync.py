from pathlib import Path
from typing import List, Optional

from agent_loom.compound.models import CompoundSyncResult
from agent_loom.core.git import git_checked, git_repo_root, git_scoped_commit


def _git_status_paths(repo_root: Path, *, pathspecs: List[str]) -> List[str]:
    raw = git_checked(repo_root, ["status", "--porcelain=v1", "-z", "--", *pathspecs])
    if not raw:
        return []

    parts = raw.split("\0")
    i = 0
    changed: List[str] = []
    while i < len(parts):
        tok = parts[i]
        i += 1
        if not tok:
            continue
        if len(tok) < 4 or tok[2] != " ":
            continue
        xy = tok[:2]
        p1 = tok[3:]
        if p1:
            changed.append(p1)
        if "R" in xy or "C" in xy:
            if i < len(parts):
                p2 = parts[i]
                i += 1
                if p2:
                    changed.append(p2)
    return sorted(set([p for p in changed if p]))


def sync(
    *, repo: Optional[Path] = None, message: str = "chore: compound"
) -> CompoundSyncResult:
    repo_root = git_repo_root(repo or Path.cwd())
    if repo_root is None:
        raise ValueError("Not in a git repository")

    # Deliberately scoped to compound-owned/AI-managed artifacts.
    pathspecs = [
        "AGENTS.md",
        "LOOM_PROJECT.md",
        "LOOM_ROADMAP.md",
        "LOOM_CHANGELOG.md",
        ".opencode/agents",
        ".opencode/memory",
        ".opencode/skills",
        ".claude/agents",
        ".claude/skills",
    ]

    changed = _git_status_paths(repo_root, pathspecs=pathspecs)

    if not changed:
        return CompoundSyncResult(
            committed=False,
            count=0,
            files=[],
            sha="",
            message=str(message or "chore: compound"),
        )

    sha = git_scoped_commit(
        repo_root,
        pathspecs=pathspecs,
        message=str(message or "chore: compound"),
    )

    remaining = _git_status_paths(repo_root, pathspecs=pathspecs)
    if remaining:
        raise ValueError(
            "Compound sync incomplete: compound paths still have uncommitted changes"
        )

    return CompoundSyncResult(
        committed=bool(sha),
        count=len(changed),
        files=changed,
        sha=sha or "",
        message=str(message or "chore: compound"),
    )


__all__ = [
    "sync",
]
