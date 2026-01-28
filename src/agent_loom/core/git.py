from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Sequence

from agent_loom.core.paths import realpath_from


def run_quiet(cmd: Sequence[str]) -> str:
    try:
        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            text=True,
        )
        return (p.stdout or "").strip()
    except Exception:
        return ""


def git_quiet(cwd: Path, args: Sequence[str]) -> str:
    return run_quiet(["git", "-C", str(cwd), *list(args)])


def git_checked(cwd: Path, args: Sequence[str]) -> str:
    p = subprocess.run(
        ["git", "-C", str(cwd), *list(args)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if p.returncode != 0:
        msg = (p.stderr or p.stdout or "").strip() or "git command failed"
        raise ValueError(msg)
    return (p.stdout or "").rstrip()


def git_checked_env(cwd: Path, args: Sequence[str], *, env: dict[str, str]) -> str:
    p = subprocess.run(
        ["git", "-C", str(cwd), *list(args)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        env=env,
    )
    if p.returncode != 0:
        msg = (p.stderr or p.stdout or "").strip() or "git command failed"
        raise ValueError(msg)
    return (p.stdout or "").rstrip()


def git_scoped_commit(
    cwd: Path, *, pathspecs: Sequence[str], message: str
) -> Optional[str]:
    if not pathspecs:
        raise ValueError("pathspecs required")

    env = os.environ.copy()
    fd, idx = tempfile.mkstemp(prefix="loom-index-")
    os.close(fd)
    env["GIT_INDEX_FILE"] = idx

    try:
        head = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--verify", "HEAD"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            check=False,
        )
        if head.returncode == 0:
            git_checked_env(cwd, ["read-tree", "HEAD"], env=env)
        else:
            git_checked_env(cwd, ["read-tree", "--empty"], env=env)

        git_checked_env(cwd, ["add", "-A", "--", *list(pathspecs)], env=env)

        staged = git_checked_env(
            cwd,
            ["diff", "--cached", "--name-only", "-z", "--", *list(pathspecs)],
            env=env,
        )
        if not staged.strip("\0").strip():
            return None

        git_checked_env(cwd, ["commit", "-m", str(message or "chore")], env=env)
    finally:
        try:
            os.unlink(idx)
        except Exception:
            pass

    # Keep the real index consistent with the working tree for these paths.
    git_checked(cwd, ["add", "-A", "--", *list(pathspecs)])
    return git_quiet(cwd, ["rev-parse", "HEAD"]).strip() or None


def git_toplevel(cwd: Path) -> Optional[Path]:
    s = git_quiet(cwd, ["rev-parse", "--show-toplevel"])
    if not s:
        return None
    return realpath_from(cwd, s)


def git_common_dir(toplevel: Path) -> Optional[Path]:
    s = git_quiet(toplevel, ["rev-parse", "--git-common-dir"])
    if not s:
        return None
    return realpath_from(toplevel, s)


def git_abs_git_dir(toplevel: Path) -> Optional[Path]:
    s = git_quiet(toplevel, ["rev-parse", "--absolute-git-dir"])
    if not s:
        s = git_quiet(toplevel, ["rev-parse", "--git-dir"])
    if not s:
        return None
    return realpath_from(toplevel, s)


def git_worktree_paths(toplevel: Path) -> List[Path]:
    s = git_quiet(toplevel, ["worktree", "list", "--porcelain"])
    if not s:
        return []

    paths: List[Path] = []
    cur_path: Optional[Path] = None
    cur_bare = False
    cur_prunable = False

    def flush() -> None:
        nonlocal cur_path, cur_bare, cur_prunable
        if cur_path is not None and (not cur_bare) and (not cur_prunable):
            paths.append(cur_path)
        cur_path = None
        cur_bare = False
        cur_prunable = False

    for line in s.splitlines():
        line = line.strip()
        if line.startswith("worktree "):
            flush()
            cur_path = realpath_from(toplevel, line.split(" ", 1)[1])
            continue
        if line == "bare":
            cur_bare = True
            continue
        if line.startswith("prunable"):
            cur_prunable = True
            continue

    flush()
    return [p for p in paths if p is not None]


def git_repo_root(cwd: Path) -> Optional[Path]:
    toplevel = git_toplevel(cwd)
    if toplevel is None:
        return None

    common_dir = git_common_dir(toplevel)
    if common_dir is None:
        return toplevel

    if common_dir.name == ".git":
        return common_dir.parent

    for wt in git_worktree_paths(toplevel):
        if not wt.exists():
            continue
        wt_git_dir = git_abs_git_dir(wt)
        if wt_git_dir is not None and wt_git_dir == common_dir:
            return wt

    return toplevel
