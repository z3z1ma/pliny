from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.utils import is_git_repo, run


@dataclass(frozen=True)
class DiffFile:
    path: str
    patch: str
    adds: int
    dels: int


def git_has_head(path: Path) -> bool:
    p = run(["git", "rev-parse", "--verify", "HEAD"], cwd=path, check=False)
    return p.returncode == 0


def git_ref_exists(path: Path, ref: str) -> bool:
    r = str(ref or "").strip()
    if not r:
        return False
    p = run(["git", "rev-parse", "--verify", r], cwd=path, check=False)
    return p.returncode == 0


def git_merge_base(path: Path, a: str, b: str = "HEAD") -> str:
    aa = str(a or "").strip()
    bb = str(b or "").strip() or "HEAD"
    if not aa:
        raise WorkspaceError("Missing base ref")
    p = run(["git", "merge-base", aa, bb], cwd=path, check=False)
    if p.returncode != 0:
        raise WorkspaceError(
            f"git merge-base failed ({aa} {bb}):\n{(p.stderr or p.stdout or '').strip()}"
        )
    return p.stdout.strip()


def git_untracked_files(path: Path) -> list[str]:
    p = run(["git", "status", "--porcelain"], cwd=path, check=False)
    if p.returncode != 0:
        raise WorkspaceError(
            (p.stderr or p.stdout or "").strip() or "git status failed"
        )
    out: list[str] = []
    for ln in p.stdout.splitlines():
        if not ln.startswith("?? "):
            continue
        out.append(ln[3:].strip())
    return sorted({x for x in out if x})


def _git_diff_text(path: Path, *, base: str) -> str:
    cmd = ["git", "diff", "--no-color"]
    b = str(base or "").strip()
    if b:
        cmd.append(b)
    p = run(cmd, cwd=path, check=False)
    if p.returncode != 0:
        raise WorkspaceError(
            f"git diff failed (base={b or 'DEFAULT'}):\n{(p.stderr or p.stdout or '').strip()}"
        )
    return p.stdout


def _git_diff_text_best_effort_unborn(path: Path) -> str:
    # In an unborn repo, `git diff` can still show unstaged changes.
    # `git diff --cached` may fail depending on git version and state.
    parts: list[str] = []
    p = run(["git", "diff", "--no-color"], cwd=path, check=False)
    if p.returncode == 0 and p.stdout:
        parts.append(p.stdout)
    p2 = run(["git", "diff", "--no-color", "--cached"], cwd=path, check=False)
    if p2.returncode == 0 and p2.stdout:
        parts.append(p2.stdout)
    return "".join(parts)


def _split_patch_blocks(patch: str) -> list[tuple[str, str]]:
    """Split a unified patch into (file_path, patch_block) tuples.

    Uses `diff --git a/... b/...` boundaries.
    """

    blocks: list[tuple[str, str]] = []
    cur_path = ""
    cur_lines: list[str] = []

    def _flush() -> None:
        nonlocal cur_path, cur_lines
        if not cur_lines:
            return
        blocks.append((cur_path, "".join(cur_lines)))
        cur_path = ""
        cur_lines = []

    for ln in patch.splitlines(keepends=True):
        if ln.startswith("diff --git "):
            _flush()
            parts = ln.strip().split()
            # diff --git a/<path> b/<path>
            b = parts[3] if len(parts) >= 4 else ""
            if b.startswith("b/"):
                cur_path = b[2:]
            else:
                cur_path = b
        cur_lines.append(ln)

    _flush()
    return blocks


def _count_patch_changes(patch: str) -> tuple[int, int]:
    adds = 0
    dels = 0
    for ln in patch.splitlines():
        if not ln:
            continue
        if ln.startswith("+++") or ln.startswith("---"):
            continue
        if ln.startswith("+"):
            adds += 1
        elif ln.startswith("-"):
            dels += 1
    return adds, dels


def _stable_unique(seq: Iterable[str]) -> list[str]:
    return sorted({str(x) for x in seq if str(x)})


def resolve_base_ref(
    *,
    worktree: Path,
    default_branch: str = "main",
) -> str:
    """Resolve a reasonable base ref for cumulative diffs.

    Preference order:
    - origin/<default_branch> (if present)
    - <default_branch> (if present)
    - HEAD (if present)
    - "" (unborn)
    """

    wt = worktree.resolve()
    branch = str(default_branch or "").strip() or "main"
    if git_ref_exists(wt, f"origin/{branch}"):
        return f"origin/{branch}"
    if git_ref_exists(wt, branch):
        return branch
    if git_has_head(wt):
        return "HEAD"
    return ""


def worktree_diff_by_file(
    *,
    worktree: Path,
    diff_mode: str,
    base_ref: Optional[str] = None,
    default_branch: str = "main",
    max_patch_bytes: int = 2_000_000,
) -> tuple[list[DiffFile], list[str], bool, str, str]:
    """Return per-file diffs for a git worktree.

    diff_mode:
    - dirty: uncommitted changes in the worktree
    - cumulative: worktree vs merge-base with base_ref

    Returns: (files, untracked, truncated, base_used, merge_base)
    """

    wt = worktree.resolve()
    if not wt.exists() or not is_git_repo(wt):
        raise WorkspaceError(f"Not a git worktree: {wt}")

    mode = str(diff_mode or "").strip().lower()
    if mode not in {"dirty", "cumulative"}:
        raise WorkspaceError("Invalid diff_mode (expected dirty|cumulative)")

    base_used = str(base_ref or "").strip()
    merge_base = ""

    if mode == "dirty":
        if not base_used:
            base_used = "HEAD" if git_has_head(wt) else ""
        if base_used and not git_ref_exists(wt, base_used) and base_used != "HEAD":
            # Let git diff surface the error message if a caller passes junk.
            pass
        patch = (
            _git_diff_text(wt, base=base_used)
            if base_used
            else _git_diff_text_best_effort_unborn(wt)
        )
    else:
        if not base_used:
            base_used = resolve_base_ref(worktree=wt, default_branch=default_branch)
        if not git_has_head(wt) or base_used in {"", "HEAD"}:
            # If we can't compute merge-base meaningfully, fall back to dirty semantics.
            patch = (
                _git_diff_text(wt, base="HEAD")
                if git_has_head(wt)
                else _git_diff_text_best_effort_unborn(wt)
            )
        else:
            merge_base = git_merge_base(wt, base_used, "HEAD")
            patch = _git_diff_text(wt, base=merge_base)

    untracked = git_untracked_files(wt)

    blocks = _split_patch_blocks(patch)

    grouped: dict[str, list[str]] = {}
    for path, blk in blocks:
        key = str(path or "")
        if not key:
            continue
        grouped.setdefault(key, []).append(blk)

    paths = _stable_unique(grouped.keys())

    out: list[DiffFile] = []
    used = 0
    truncated = False
    for p in paths:
        patch = "".join(grouped.get(p) or [])
        patch_bytes = len(patch.encode("utf-8", errors="replace"))
        if out and (used + patch_bytes) > max_patch_bytes:
            truncated = True
            break
        adds, dels = _count_patch_changes(patch)
        out.append(DiffFile(path=p, patch=patch, adds=adds, dels=dels))
        used += patch_bytes

    if len(out) < len(paths):
        truncated = True

    return out, untracked, truncated, base_used, merge_base
