from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from agent_loom.workspace.constants import (
    DEFAULT_DEFAULT_BRANCH,
    REPO_INTERNAL_DIR,
    SHA_RE,
)
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.state import Repo, worktrees_base
from agent_loom.workspace.utils import ensure_dir, is_git_repo, run, short, which


def git_git_dir(repo_path: Path) -> Path:
    """Return the resolved .git dir for a repo/worktree."""

    out = run(["git", "rev-parse", "--git-dir"], cwd=repo_path).stdout.strip()
    if not out:
        raise WorkspaceError(f"Unable to resolve git dir for: {repo_path}")
    p = Path(out)
    if not p.is_absolute():
        p = (repo_path / p).resolve()
    return p


def ensure_repo_internal_ignored(repo_path: Path) -> None:
    """Best-effort: keep repo-local workspace state out of git status output."""

    try:
        git_dir = git_git_dir(repo_path)
        exclude = git_dir / "info" / "exclude"
        ensure_dir(exclude.parent)
        line = f"{REPO_INTERNAL_DIR}/"
        existing = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
        if line in (ln.strip() for ln in existing.splitlines()):
            return
        text = existing.rstrip("\n")
        if text:
            text += "\n"
        text += line + "\n"
        exclude.write_text(text, encoding="utf-8")
    except Exception:
        # Never fail core operations due to ignore bookkeeping.
        return


def require_git() -> None:
    if not which("git"):
        raise WorkspaceError("git not found on PATH")


def _normalize_fetch_target(ref: str) -> str:
    if ref.startswith("origin/"):
        return ref[len("origin/") :]
    return ref


def git_fetch_ref(root: Path, repo: Repo, ref: str) -> None:
    path = root / repo.path
    target = _normalize_fetch_target(ref)

    # If it's a raw SHA, there is nothing to "fetch by name" (unless using special syntax).
    # Caller should handle SHAs separately.
    if SHA_RE.match(target):
        return

    cmd = ["git", "fetch", "--prune", "origin", target]
    if repo.shallow:
        cmd += ["--depth", str(repo.depth)]
    run(cmd, cwd=path)


def git_clone_if_missing(root: Path, repo: Repo) -> None:
    path = root / repo.path
    if path.exists():
        if not is_git_repo(path):
            raise WorkspaceError(f"Path exists but is not a git repo: {path}")
        return

    ensure_dir(path.parent)

    depth = max(1, int(repo.depth))  # defensive
    cmd = ["git", "clone", "--branch", repo.default_branch]
    if repo.shallow:
        cmd += ["--depth", str(depth)]
    cmd += [repo.remote, str(path)]
    run(cmd, cwd=root)


def git_fetch(root: Path, repo: Repo) -> None:
    path = root / repo.path
    if repo.shallow:
        git_fetch_ref(root, repo, repo.default_branch)
    else:
        run(["git", "fetch", "--all", "--prune"], cwd=path)


def git_checkout_reset_branch(
    root: Path, repo: Repo, branch: str, base_ref: Optional[str]
) -> None:
    path = root / repo.path
    base = (base_ref or repo.default_branch).strip()

    # If base is a SHA, use it directly.
    if SHA_RE.match(base):
        base_obj = base
        run(["git", "checkout", "-B", branch, base_obj], cwd=path)
        return

    fetch_target = _normalize_fetch_target(base)

    # Fetch base ref in a shallow-safe way.
    git_fetch_ref(root, repo, fetch_target)

    preferred = f"origin/{fetch_target}"

    # Prefer origin/<branch> if it exists after fetch.
    try:
        run(["git", "rev-parse", "--verify", preferred], cwd=path, check=True)
        base_obj = preferred
    except WorkspaceError:
        # FETCH_HEAD should exist immediately after fetch of a specific target.
        try:
            run(["git", "rev-parse", "--verify", "FETCH_HEAD"], cwd=path, check=True)
            base_obj = "FETCH_HEAD"
        except WorkspaceError:
            # Last resort: fall back to HEAD (should be rare)
            base_obj = "HEAD"

    run(["git", "checkout", "-B", branch, base_obj], cwd=path)


def git_current_branch(path: Path) -> str:
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=path).stdout.strip()


def git_head_sha(path: Path) -> str:
    return run(["git", "rev-parse", "HEAD"], cwd=path).stdout.strip()


def git_is_dirty(path: Path) -> bool:
    return bool(run(["git", "status", "--porcelain"], cwd=path).stdout.strip())


def git_ref_exists(path: Path, ref: str) -> bool:
    try:
        run(["git", "rev-parse", "--verify", ref], cwd=path, check=True)
        return True
    except WorkspaceError:
        return False


def git_branch_upstream(path: Path, branch: str) -> Optional[str]:
    p = run(
        ["git", "rev-parse", "--abbrev-ref", f"{branch}@{{upstream}}"],
        cwd=path,
        check=False,
    )
    if p.returncode != 0:
        return None
    return p.stdout.strip()


def git_set_upstream(path: Path, branch: str, upstream: str) -> None:
    run(["git", "branch", "--set-upstream-to", upstream, branch], cwd=path)


def git_is_ancestor(path: Path, older: str, newer: str) -> bool:
    p = run(["git", "merge-base", "--is-ancestor", older, newer], cwd=path, check=False)
    return p.returncode == 0


def git_ensure_branch(
    root: Path, repo: Repo, branch: str, base_ref: Optional[str]
) -> None:
    repo_path = root / repo.path

    cmd = ["git", "fetch", "--prune", "origin", branch]
    if repo.shallow:
        cmd += ["--depth", str(repo.depth)]
    run(cmd, cwd=repo_path, check=False)

    remote_branch = f"origin/{branch}"
    if git_ref_exists(repo_path, remote_branch):
        if git_ref_exists(repo_path, branch):
            if git_is_ancestor(repo_path, branch, remote_branch):
                run(["git", "branch", "-f", branch, remote_branch], cwd=repo_path)
            else:
                raise WorkspaceError(
                    f"Local branch '{branch}' has commits not on {remote_branch}; refusing to move it."
                )
        else:
            run(["git", "branch", "--track", branch, remote_branch], cwd=repo_path)

        upstream = git_branch_upstream(repo_path, branch)
        if upstream != remote_branch:
            git_set_upstream(repo_path, branch, remote_branch)
        return

    if git_ref_exists(repo_path, branch):
        return

    base = (base_ref or repo.default_branch).strip()

    if SHA_RE.match(base):
        run(["git", "branch", branch, base], cwd=repo_path)
        return

    fetch_target = _normalize_fetch_target(base)
    git_fetch_ref(root, repo, fetch_target)

    preferred = f"origin/{fetch_target}"
    if git_ref_exists(repo_path, preferred):
        base_obj = preferred
    elif git_ref_exists(repo_path, "FETCH_HEAD"):
        base_obj = "FETCH_HEAD"
    else:
        base_obj = "HEAD"

    run(["git", "branch", branch, base_obj], cwd=repo_path)


def git_worktree_add(root: Path, ws: dict, repo: Repo, branch: str) -> Path:
    repo_path = root / repo.path
    wt_path = worktrees_base(root, ws, branch) / repo.name
    ensure_dir(wt_path.parent)

    if wt_path.exists():
        if not is_git_repo(wt_path):
            raise WorkspaceError(
                f"Worktree path exists but isn't a git worktree: {wt_path}"
            )

        br = git_current_branch(wt_path)
        if br != branch:
            raise WorkspaceError(
                f"Worktree exists at {wt_path} but is on branch '{br}' (expected '{branch}')"
            )

        if git_is_dirty(wt_path):
            raise WorkspaceError(
                f"Worktree exists at {wt_path} but has uncommitted changes; refusing to proceed."
            )

        # Keep remote refs reasonably fresh before comparing.
        try:
            git_fetch_ref(root, repo, branch)
        except WorkspaceError:
            pass

        remote_branch = f"origin/{branch}"
        if git_ref_exists(wt_path, remote_branch):
            wt_head = git_head_sha(wt_path)
            remote_head = run(
                ["git", "rev-parse", remote_branch], cwd=wt_path
            ).stdout.strip()
            if wt_head != remote_head:
                raise WorkspaceError(
                    f"Worktree exists at {wt_path} but is not at {remote_branch} "
                    f"(local={short(wt_head)} remote={short(remote_head)})."
                )

        return wt_path

    run(["git", "worktree", "add", str(wt_path), branch], cwd=repo_path)
    return wt_path


def git_worktree_remove(wt_path: Path, force: bool = False) -> None:
    if not wt_path.exists():
        return

    git_file = wt_path / ".git"
    if not git_file.exists():
        raise WorkspaceError(f"Not a git worktree (missing .git): {wt_path}")

    cmd = ["git", "worktree", "remove", str(wt_path)]
    if force:
        cmd.append("--force")
    run(cmd, cwd=wt_path)


def git_worktree_remove_from(
    repo_path: Path, wt_path: Path, force: bool = False
) -> None:
    """Remove a worktree using the primary repo as the command CWD."""

    if not wt_path.exists():
        return

    if not is_git_repo(repo_path):
        raise WorkspaceError(f"Not a git repo: {repo_path}")

    cmd = ["git", "worktree", "remove", str(wt_path)]
    if force:
        cmd.append("--force")
    run(cmd, cwd=repo_path)


def git_worktree_list_porcelain(repo_path: Path) -> List[dict]:
    out = run(["git", "worktree", "list", "--porcelain"], cwd=repo_path).stdout
    rows: List[dict] = []
    cur: Optional[dict] = None
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
        elif line.startswith("locked"):
            cur["locked"] = True
    if cur:
        rows.append(cur)
    return rows


def repo_default_branch(repo_path: Path) -> str:
    p = run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        check=False,
    )
    if p.returncode == 0:
        ref = p.stdout.strip()
        if ref.startswith("refs/remotes/origin/"):
            return ref.split("/")[-1]
    return DEFAULT_DEFAULT_BRANCH
