from __future__ import annotations

import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

from agent_loom.core.exec import ExecError
from agent_loom.core.exec import run as exec_run
from agent_loom.core.paths import realpath_from


@dataclass(frozen=True)
class GitCommandResult:
    ok: bool
    returncode: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class GitStdoutResult:
    value: Optional[str]
    command: GitCommandResult


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


def git_result(
    cwd: Path,
    args: Sequence[str],
    *,
    env: Optional[dict[str, str]] = None,
) -> GitCommandResult:
    try:
        p = _git_exec(cwd, args, check=False, env=env)
        return GitCommandResult(
            ok=bool(p.returncode == 0),
            returncode=int(p.returncode),
            stdout=str(p.stdout or ""),
            stderr=str(p.stderr or ""),
        )
    except ExecError as e:
        return GitCommandResult(
            ok=False,
            returncode=int(e.returncode),
            stdout=str(e.stdout or ""),
            stderr=str(e.stderr or ""),
        )


def is_git_repo(path: Path) -> bool:
    # normal repo has .git dir; worktree has .git file
    gitp = path / ".git"
    return gitp.is_dir() or gitp.is_file()


def git_stdout_result(
    cwd: Path,
    args: Sequence[str],
    *,
    env: Optional[dict[str, str]] = None,
    strip: bool = True,
) -> GitStdoutResult:
    command = git_result(cwd, args, env=env)
    if not command.ok:
        return GitStdoutResult(value=None, command=command)
    stdout = command.stdout.strip() if strip else command.stdout
    return GitStdoutResult(value=(stdout or None), command=command)


def _stdout_or_raise(result: GitCommandResult) -> str:
    if not result.ok:
        msg = (result.stderr or result.stdout).strip() or "git command failed"
        raise ValueError(msg)
    return result.stdout.rstrip()


def git_checked(cwd: Path, args: Sequence[str]) -> str:
    return _stdout_or_raise(git_result(cwd, args))


def git_checked_env(cwd: Path, args: Sequence[str], *, env: dict[str, str]) -> str:
    return _stdout_or_raise(git_result(cwd, args, env=env))


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
        head = git_result(cwd, ["rev-parse", "--verify", "HEAD"])
        if head.ok:
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
    return git_checked(cwd, ["rev-parse", "HEAD"]).strip() or None


def git_toplevel(cwd: Path) -> Optional[Path]:
    out = git_stdout_result(cwd, ["rev-parse", "--show-toplevel"])
    if out.value is None:
        return None
    return realpath_from(cwd, out.value)


def git_common_dir(toplevel: Path) -> Optional[Path]:
    out = git_stdout_result(toplevel, ["rev-parse", "--git-common-dir"])
    if out.value is None:
        return None
    return realpath_from(toplevel, out.value)


def git_abs_git_dir(toplevel: Path) -> Optional[Path]:
    out = git_stdout_result(toplevel, ["rev-parse", "--absolute-git-dir"])
    if out.value is None:
        out = git_stdout_result(toplevel, ["rev-parse", "--git-dir"])
    if out.value is None:
        return None
    return realpath_from(toplevel, out.value)


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
