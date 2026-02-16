from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Sequence

from agent_loom.core.exec import ExecError
from agent_loom.core.exec import run as exec_run
from agent_loom.core.paths import realpath_from


def _git_exec(
    cwd: Path,
    args: Sequence[str],
    *,
    check: bool,
    env: Optional[dict[str, str]] = None,
) -> subprocess.CompletedProcess[str]:
    cmd = ["git", *list(args)]
    try:
        return exec_run(cmd, cwd=cwd, check=check, env=env)
    except OSError as e:
        raise ExecError(
            cmd=cmd, cwd=cwd, returncode=127, stdout="", stderr=str(e)
        ) from e


def is_git_repo(path: Path) -> bool:
    # normal repo has .git dir; worktree has .git file
    gitp = path / ".git"
    return gitp.is_dir() or gitp.is_file()


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
    try:
        rows = git_worktree_list_porcelain(toplevel)
    except ExecError:
        return []

    paths: List[Path] = []
    for row in rows:
        if bool(row.get("bare")) or bool(row.get("prunable")):
            continue
        p = realpath_from(toplevel, str(row.get("path") or ""))
        if p is not None:
            paths.append(p)
    return paths


def git_worktree_list_porcelain(cwd: Path) -> list[dict[str, object]]:
    p = _git_exec(cwd, ["worktree", "list", "--porcelain"], check=True)
    out = p.stdout or ""

    rows: list[dict[str, object]] = []
    cur: Optional[dict[str, object]] = None

    for line in out.splitlines():
        if not line.strip():
            continue
        if line.startswith("worktree "):
            if cur:
                rows.append(cur)
            cur = {"path": line.split(" ", 1)[1].strip()}
            continue
        if cur is None:
            continue

        if line.startswith("HEAD "):
            cur["head"] = line.split(" ", 1)[1].strip()
        elif line.startswith("branch "):
            ref = line.split(" ", 1)[1].strip()
            cur["ref"] = ref
            if ref.startswith("refs/heads/"):
                cur["branch"] = ref[len("refs/heads/") :]
            else:
                cur["branch"] = ref
        elif line == "detached":
            cur["detached"] = True
        elif line == "bare":
            cur["bare"] = True
        elif line.startswith("prunable"):
            cur["prunable"] = True
        elif line.startswith("locked"):
            cur["locked"] = True

    if cur:
        rows.append(cur)
    return rows


def git_ref_exists(cwd: Path, ref: str) -> bool:
    r = str(ref or "").strip()
    if not r:
        return False
    p = _git_exec(cwd, ["rev-parse", "--verify", r], check=False)
    return p.returncode == 0


def git_has_head(cwd: Path) -> bool:
    return git_ref_exists(cwd, "HEAD")


def git_merge_base(cwd: Path, a: str, b: str = "HEAD") -> str:
    aa = str(a or "").strip()
    bb = str(b or "").strip() or "HEAD"
    if not aa:
        raise ValueError("missing base ref")
    p = _git_exec(cwd, ["merge-base", aa, bb], check=True)
    return (p.stdout or "").strip()


def git_is_ancestor(cwd: Path, older: str, newer: str) -> bool:
    p = _git_exec(
        cwd,
        ["merge-base", "--is-ancestor", str(older), str(newer)],
        check=False,
    )
    return p.returncode == 0


def git_current_branch(cwd: Path) -> str:
    p = _git_exec(cwd, ["rev-parse", "--abbrev-ref", "HEAD"], check=True)
    return (p.stdout or "").strip()


def git_head_sha(cwd: Path) -> str:
    p = _git_exec(cwd, ["rev-parse", "HEAD"], check=True)
    return (p.stdout or "").strip()


def git_is_dirty(cwd: Path) -> bool:
    p = _git_exec(cwd, ["status", "--porcelain"], check=True)
    return bool((p.stdout or "").strip())


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


def resolve_repo_root(path: Path | str | None = None) -> Path:
    if path is None:
        start = Path.cwd().resolve()
    else:
        raw = str(path).strip()
        start = Path(raw if raw else ".").expanduser().resolve()
    return (git_repo_root(start) or start).resolve()
