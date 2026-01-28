from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from agent_loom.workspace.constants import REPO_INTERNAL_DIR, SHA_RE
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.git_ops import (
    git_git_dir,
    ensure_repo_internal_ignored,
    git_current_branch,
    git_head_sha,
    git_is_dirty,
    git_ref_exists,
    git_worktree_list_porcelain,
    git_worktree_remove_from,
    repo_default_branch,
    require_git,
)
from agent_loom.workspace.models import (
    MergeAttemptResult,
    RepoInitResult,
    RepoStatusResult,
    RepoWorktreeAddResult,
    RepoWorktreeEnsureDetachedResult,
    RepoWorktreeListResult,
    RepoWorktreePruneResult,
    RepoWorktreeRemoveResult,
    WorktreeEnsureResult,
)
from agent_loom.workspace.state import fs_escape
from agent_loom.workspace.utils import (
    atomic_write_json,
    ensure_dir,
    is_git_repo,
    now_iso,
    read_json,
    run,
)


def repo_root() -> Path:
    require_git()
    p = run(["git", "rev-parse", "--show-toplevel"], cwd=Path.cwd(), check=False)
    if p.returncode != 0:
        raise WorkspaceError("Not inside a git repository")
    out = p.stdout.strip()
    if not out:
        raise WorkspaceError("Not inside a git repository")
    return Path(out).resolve()


def repo_ws_worktrees_dir(repo_path: Path) -> Path:
    return repo_path / REPO_INTERNAL_DIR / "worktrees"


def repo_worktree_default_path(repo_path: Path, branch: str) -> Path:
    return repo_ws_worktrees_dir(repo_path) / fs_escape(branch)


def repo_init(*, root: Optional[Path] = None) -> RepoInitResult:
    repo = root.resolve() if root is not None else repo_root()

    created: list[str] = []

    internal = repo / REPO_INTERNAL_DIR
    worktrees = repo_ws_worktrees_dir(repo)
    git_exclude = git_git_dir(repo) / "info" / "exclude"

    # Ignore bookkeeping
    ensure_repo_internal_ignored(repo)

    if not internal.exists():
        created.append(f"{REPO_INTERNAL_DIR}/")
    ensure_dir(internal)

    if not worktrees.exists():
        created.append(f"{REPO_INTERNAL_DIR}/worktrees/")
    ensure_dir(worktrees)

    return RepoInitResult(
        repo_root=str(repo.resolve()),
        internal_dir=str(internal.resolve()),
        worktrees_dir=str(worktrees.resolve()),
        git_exclude_path=str(git_exclude.resolve()),
        created=sorted({c for c in created if c}),
    )


def repo_fetch_ref(repo_path: Path, ref: str) -> None:
    """Best-effort fetch to resolve a ref-ish inside a repo."""

    target = str(ref or "").strip()
    if not target or SHA_RE.match(target):
        return
    run(["git", "fetch", "origin", target], cwd=repo_path, check=False)


def repo_status(*, root: Optional[Path] = None) -> RepoStatusResult:
    repo = root.resolve() if root is not None else repo_root()
    return RepoStatusResult(
        repo_root=str(repo),
        branch=git_current_branch(repo),
        commit=git_head_sha(repo),
        dirty=git_is_dirty(repo),
        default_branch=repo_default_branch(repo),
    )


def repo_worktree_add(
    *,
    branch: str,
    path: Optional[str] = None,
    base_ref: Optional[str] = None,
    root: Optional[Path] = None,
) -> RepoWorktreeAddResult:
    repo = root.resolve() if root is not None else repo_root()
    ensure_repo_internal_ignored(repo)

    ensure_dir(repo_ws_worktrees_dir(repo))

    if path:
        p = Path(path)
        wt_path = (p if p.is_absolute() else (repo / p)).resolve()
    else:
        wt_path = repo_worktree_default_path(repo, branch).resolve()

    if wt_path.exists():
        if not is_git_repo(wt_path):
            raise WorkspaceError(
                f"Worktree path exists but is not a git worktree: {wt_path}"
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
        try:
            from agent_loom.workspace.worktree_meta import repo_worktree_touch

            repo_worktree_touch(repo_root=repo, branch=branch)
        except Exception:
            pass
        return RepoWorktreeAddResult(branch=branch, path=str(wt_path), existed=True)

    if git_ref_exists(repo, branch):
        run(["git", "worktree", "add", str(wt_path), branch], cwd=repo)
    else:
        if base_ref:
            base = base_ref
        else:
            remote = run(["git", "remote", "get-url", "origin"], cwd=repo, check=False)
            if remote.returncode == 0 and remote.stdout.strip():
                base = f"origin/{repo_default_branch(repo)}"
            else:
                base = "HEAD"

        repo_fetch_ref(repo, base)
        run(["git", "worktree", "add", "-b", branch, str(wt_path), base], cwd=repo)

    try:
        from agent_loom.workspace.worktree_meta import repo_worktree_touch

        repo_worktree_touch(repo_root=repo, branch=branch)
    except Exception:
        pass

    return RepoWorktreeAddResult(branch=branch, path=str(wt_path), existed=False)


def repo_worktree_ensure(
    *,
    branch: str,
    path: Optional[str] = None,
    base_ref: Optional[str] = None,
    allow_dirty: bool = False,
    root: Optional[Path] = None,
) -> WorktreeEnsureResult:
    """Ensure a worktree exists for a branch at a specific path.

    Unlike `worktree add`, this command is resumable:
    - If the branch already has a worktree elsewhere, reuse that path.
    - If the path exists, validate it's the correct worktree and return it.
    - Otherwise create a new worktree at the requested path.
    """

    repo = root.resolve() if root is not None else repo_root()
    ensure_repo_internal_ignored(repo)

    def _touch_meta() -> None:
        try:
            from agent_loom.workspace.worktree_meta import repo_worktree_touch

            repo_worktree_touch(repo_root=repo, branch=branch)
        except Exception:
            return

    raw_path = str(path or "").strip()
    if raw_path:
        p = Path(raw_path)
        wt_path = (p if p.is_absolute() else (repo / p)).resolve()
    else:
        wt_path = repo_worktree_default_path(repo, branch).resolve()

    # Resolve base-ref for branch creation (only used if branch doesn't exist).
    if base_ref:
        base_ref = str(base_ref)
    else:
        remote = run(["git", "remote", "get-url", "origin"], cwd=repo, check=False)
        if remote.returncode == 0 and remote.stdout.strip():
            base_ref = f"origin/{repo_default_branch(repo)}"
        else:
            base_ref = "HEAD"

    base_branch = base_ref
    if base_branch.startswith("origin/"):
        base_branch = base_branch.split("/", 1)[1]

    rows = git_worktree_list_porcelain(repo)

    # 1) If branch already has a worktree elsewhere, reuse it.
    for wt in rows:
        if str(wt.get("branch") or "") != branch:
            continue
        existing = Path(str(wt.get("path") or "")).resolve()
        if not existing.exists():
            # Dangling worktree metadata; let callers prune/repair explicitly.
            continue
        if not allow_dirty and git_is_dirty(existing):
            raise WorkspaceError(
                f"Worktree exists for branch '{branch}' at {existing} but has uncommitted changes; refusing to proceed."
            )
        _touch_meta()
        return WorktreeEnsureResult(
            branch=branch,
            path=str(existing),
            existed=True,
            reused=True,
            base_ref=base_ref,
            base_branch=base_branch,
        )

    # 2) If the requested path already exists, validate it.
    if wt_path.exists():
        if not is_git_repo(wt_path):
            raise WorkspaceError(
                f"Worktree path exists but is not a git worktree: {wt_path}"
            )
        br = git_current_branch(wt_path)
        if br != branch:
            raise WorkspaceError(
                f"Worktree exists at {wt_path} but is on branch '{br}' (expected '{branch}')"
            )

        registered = {Path(str(w.get("path") or "")).resolve() for w in rows}
        if wt_path.resolve() not in registered:
            raise WorkspaceError(
                f"Worktree directory exists but is not registered with git: {wt_path} (try `git worktree prune`)"
            )

        if not allow_dirty and git_is_dirty(wt_path):
            raise WorkspaceError(
                f"Worktree exists at {wt_path} but has uncommitted changes; refusing to proceed."
            )
        _touch_meta()
        return WorktreeEnsureResult(
            branch=branch,
            path=str(wt_path),
            existed=True,
            reused=False,
            base_ref=base_ref,
            base_branch=base_branch,
        )

    # 3) Create the worktree at the requested path.
    if git_ref_exists(repo, branch):
        run(["git", "worktree", "add", str(wt_path), branch], cwd=repo)
        used_start = branch
    else:
        # Mirror team's behavior: allow base refs like 'main' or 'origin/main'.
        start = base_ref
        if (
            run(
                ["git", "rev-parse", "--verify", "--quiet", start],
                cwd=repo,
                check=False,
            ).returncode
            != 0
        ):
            if (
                not start.startswith("origin/")
                and not SHA_RE.match(start)
                and start != "HEAD"
            ):
                start = f"origin/{start}"
        repo_fetch_ref(repo, start)
        run(["git", "worktree", "add", "-b", branch, str(wt_path), start], cwd=repo)
        used_start = start

    _touch_meta()

    return WorktreeEnsureResult(
        branch=branch,
        path=str(wt_path),
        existed=False,
        reused=False,
        base_ref=used_start,
        base_branch=base_branch,
    )


def repo_worktree_rm_path(
    *,
    path: str,
    force: bool = False,
    confirm: bool = False,
    root: Optional[Path] = None,
) -> RepoWorktreeRemoveResult:
    repo = root.resolve() if root is not None else repo_root()
    if not confirm:
        raise WorkspaceError("Refusing to remove a worktree without --yes")

    raw = str(path or "").strip()
    if not raw:
        raise WorkspaceError("Missing path")

    p = Path(raw)
    wt_path = (p if p.is_absolute() else (repo / p)).resolve()
    git_worktree_remove_from(repo, wt_path, force=bool(force))

    return RepoWorktreeRemoveResult(removed=str(wt_path))


def repo_worktree_prune(*, root: Optional[Path] = None) -> RepoWorktreePruneResult:
    repo = root.resolve() if root is not None else repo_root()
    run(["git", "worktree", "prune"], cwd=repo, check=False)
    return RepoWorktreePruneResult(pruned=True)


def _repo_resolve_ref_to_commit(repo_path: Path, ref: str) -> str:
    """Resolve a ref-ish (branch, origin/branch, tag, SHA) to a commit SHA."""

    r = str(ref or "").strip()
    if not r:
        raise WorkspaceError("Missing ref")

    # Best-effort fetch when origin exists.
    repo_fetch_ref(repo_path, r)

    def _try(x: str) -> Optional[str]:
        p = run(
            ["git", "rev-parse", "--verify", "--quiet", x], cwd=repo_path, check=False
        )
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip()
        return None

    out = _try(r)
    if out:
        return out

    if not r.startswith("origin/") and not SHA_RE.match(r) and r != "HEAD":
        out = _try(f"origin/{r}")
        if out:
            return out

    raise WorkspaceError(f"Unable to resolve ref to commit: {r}")


def _repo_worktree_registered(repo_path: Path, wt_path: Path) -> bool:
    registered = {
        Path(str(w.get("path") or "")).resolve()
        for w in git_worktree_list_porcelain(repo_path)
    }
    return wt_path.resolve() in registered


def repo_worktree_ensure_detached(
    *,
    path: str,
    ref: str,
    root: Optional[Path] = None,
) -> RepoWorktreeEnsureDetachedResult:
    repo = root.resolve() if root is not None else repo_root()

    raw = str(path or "").strip()
    if not raw:
        raise WorkspaceError("Missing --path")
    p = Path(raw)
    wt_path = (p if p.is_absolute() else (repo / p)).resolve()

    if repo.resolve() not in wt_path.parents and wt_path != repo.resolve():
        raise WorkspaceError(
            f"Refusing to create worktree outside repo root: {wt_path}"
        )

    ref = str(ref or "").strip()
    commit = _repo_resolve_ref_to_commit(repo, ref)

    existed = wt_path.exists()
    if existed:
        if not is_git_repo(wt_path):
            raise WorkspaceError(
                f"Worktree path exists but is not a git worktree: {wt_path}"
            )
        if not _repo_worktree_registered(repo, wt_path):
            raise WorkspaceError(
                f"Worktree directory exists but is not registered with git: {wt_path} (try `loom workspace worktree prune`)"
            )
        return RepoWorktreeEnsureDetachedResult(
            path=str(wt_path), ref=ref, commit=commit, existed=True
        )

    ensure_dir(wt_path.parent)
    run(["git", "worktree", "add", "--detach", str(wt_path), commit], cwd=repo)
    return RepoWorktreeEnsureDetachedResult(
        path=str(wt_path), ref=ref, commit=commit, existed=False
    )


def repo_merge_attempt(
    *,
    worktree: str,
    base: str,
    topic: str,
    force_clean: bool = False,
    root: Optional[Path] = None,
) -> MergeAttemptResult:
    """Attempt a local merge in a dedicated worktree.

    This command is designed for automation and returns ok=true even for merge failures.
    Use `data.merged` to check success.
    """

    repo = root.resolve() if root is not None else repo_root()
    wt_raw = str(worktree or "").strip()
    if not wt_raw:
        raise WorkspaceError("Missing --worktree")
    p = Path(wt_raw)
    wt_path = (p if p.is_absolute() else (repo / p)).resolve()

    if repo.resolve() not in wt_path.parents and wt_path != repo.resolve():
        raise WorkspaceError(f"Refusing to operate outside repo root: {wt_path}")

    base_ref = str(base or "").strip()
    topic = str(topic or "").strip()
    if not topic:
        raise WorkspaceError("Missing --topic")

    base_commit = _repo_resolve_ref_to_commit(repo, base_ref)

    # Ensure merge worktree exists.
    created = False
    if not wt_path.exists():
        ensure_dir(wt_path.parent)
        run(["git", "worktree", "add", "--detach", str(wt_path), base_commit], cwd=repo)
        created = True
    else:
        if not is_git_repo(wt_path):
            raise WorkspaceError(
                f"Worktree path exists but is not a git worktree: {wt_path}"
            )
        if not _repo_worktree_registered(repo, wt_path):
            raise WorkspaceError(
                f"Worktree directory exists but is not registered with git: {wt_path} (try `loom workspace worktree prune`)"
            )

    def _dirty() -> bool:
        return bool(run(["git", "status", "--porcelain"], cwd=wt_path).stdout.strip())

    if _dirty():
        if force_clean:
            run(["git", "merge", "--abort"], cwd=wt_path, check=False)
            run(["git", "reset", "--hard"], cwd=wt_path, check=False)
            run(["git", "clean", "-fd"], cwd=wt_path, check=False)
        else:
            return MergeAttemptResult(
                merged=False,
                worktree=str(wt_path),
                base=base_ref,
                base_commit=base_commit,
                topic=topic,
                error="merge worktree has local changes",
                hint="Run with --force-clean to reset the merge worktree.",
            )

    # If base ref was supplied, ensure worktree is based on that commit.
    anc = run(
        ["git", "merge-base", "--is-ancestor", base_commit, "HEAD"],
        cwd=wt_path,
        check=False,
    )
    if anc.returncode != 0:
        if force_clean or created:
            run(["git", "reset", "--hard", base_commit], cwd=wt_path, check=False)
            run(["git", "clean", "-fd"], cwd=wt_path, check=False)
        else:
            return MergeAttemptResult(
                merged=False,
                worktree=str(wt_path),
                base=base_ref,
                base_commit=base_commit,
                topic=topic,
                error="merge worktree not based on requested base",
                hint="Run with --force-clean to reset the merge worktree to the requested base.",
            )

    # Merge
    pmerge = run(
        ["git", "merge", "--no-ff", "--no-edit", topic],
        cwd=wt_path,
        check=False,
    )
    if pmerge.returncode != 0:
        return MergeAttemptResult(
            merged=False,
            worktree=str(wt_path),
            base=base_ref,
            base_commit=base_commit,
            topic=topic,
            stdout=(pmerge.stdout or "").strip(),
            stderr=(pmerge.stderr or "").strip(),
            error="merge failed",
        )

    head = run(["git", "rev-parse", "HEAD"], cwd=wt_path).stdout.strip()
    return MergeAttemptResult(
        merged=True,
        worktree=str(wt_path),
        base=base_ref,
        base_commit=base_commit,
        topic=topic,
        merge_commit=head,
        stdout=(pmerge.stdout or "").strip(),
        stderr=(pmerge.stderr or "").strip(),
    )


def repo_worktree_rm(
    *,
    branch: str,
    force: bool = False,
    confirm: bool = False,
    root: Optional[Path] = None,
) -> RepoWorktreeRemoveResult:
    repo = root.resolve() if root is not None else repo_root()
    if not confirm:
        raise WorkspaceError("Refusing to remove a worktree without --yes")

    wt_path: Optional[Path] = None
    for wt in git_worktree_list_porcelain(repo):
        if wt.get("branch") == branch:
            wt_path = Path(wt["path"]).resolve()
            break
    if wt_path is None:
        guess = repo_worktree_default_path(repo, branch)
        if guess.exists():
            wt_path = guess.resolve()
        else:
            raise WorkspaceError(f"No worktree found for branch: {branch}")

    git_worktree_remove_from(repo, wt_path, force=bool(force))
    return RepoWorktreeRemoveResult(branch=branch, removed=str(wt_path))


def repo_worktree_ls(*, root: Optional[Path] = None) -> RepoWorktreeListResult:
    repo = root.resolve() if root is not None else repo_root()
    rows = git_worktree_list_porcelain(repo)
    return RepoWorktreeListResult(worktrees=rows)


def _repo_resolve_worktree(repo: Path, selector: str) -> Path:
    sel = str(selector or "").strip()
    if not sel:
        return repo

    p = Path(sel)
    if p.is_absolute() or (repo / p).exists():
        wt_path = (p if p.is_absolute() else (repo / p)).resolve()
        return wt_path

    # treat as branch
    for wt in git_worktree_list_porcelain(repo):
        if wt.get("branch") == sel:
            return Path(wt.get("path") or "").resolve()
    return repo_worktree_default_path(repo, sel).resolve()


def repo_worktree_status(*, worktree: str = "", root: Optional[Path] = None) -> dict:
    repo = root.resolve() if root is not None else repo_root()
    wt_path = _repo_resolve_worktree(repo, worktree)
    if not wt_path.exists() or not is_git_repo(wt_path):
        raise WorkspaceError(f"Not a git worktree: {wt_path}")

    return {
        "repo_root": str(repo.resolve()),
        "worktree": str(wt_path.resolve()),
        "branch": git_current_branch(wt_path),
        "commit": git_head_sha(wt_path),
        "dirty": git_is_dirty(wt_path),
    }


def repo_worktree_check_clean(
    *,
    worktree: str = "",
    allow_untracked: bool = False,
    root: Optional[Path] = None,
) -> dict:
    repo = root.resolve() if root is not None else repo_root()
    wt_path = _repo_resolve_worktree(repo, worktree)
    if not wt_path.exists() or not is_git_repo(wt_path):
        raise WorkspaceError(f"Not a git worktree: {wt_path}")

    out = run(["git", "status", "--porcelain"], cwd=wt_path).stdout
    lines = [ln for ln in out.splitlines() if ln.strip()]
    dirty = False
    if allow_untracked:
        dirty = any(not ln.startswith("??") for ln in lines)
    else:
        dirty = bool(lines)

    return {
        "repo_root": str(repo.resolve()),
        "worktree": str(wt_path.resolve()),
        "dirty": bool(dirty),
        "allow_untracked": bool(allow_untracked),
        "ok": not dirty,
    }


def repo_worktree_check_divergence(
    *,
    base: str,
    worktree: str = "",
    root: Optional[Path] = None,
) -> dict:
    repo = root.resolve() if root is not None else repo_root()
    wt_path = _repo_resolve_worktree(repo, worktree)
    if not wt_path.exists() or not is_git_repo(wt_path):
        raise WorkspaceError(f"Not a git worktree: {wt_path}")

    base_ref = str(base or "").strip()
    if not base_ref:
        raise WorkspaceError("Missing --base")

    # ahead/behind of HEAD vs base
    p = run(
        [
            "git",
            "rev-list",
            "--left-right",
            "--count",
            f"{base_ref}...HEAD",
        ],
        cwd=wt_path,
        check=False,
    )
    if p.returncode != 0:
        raise WorkspaceError(
            f"Unable to compute divergence vs {base_ref}:\nstdout:\n{p.stdout}\nstderr:\n{p.stderr}"
        )
    left, right = (p.stdout.strip().split() + ["0", "0"])[:2]
    behind = int(left)
    ahead = int(right)

    return {
        "repo_root": str(repo.resolve()),
        "worktree": str(wt_path.resolve()),
        "base": base_ref,
        "ahead": ahead,
        "behind": behind,
        "ok": behind == 0,
    }


def _repo_states_dir(repo: Path) -> Path:
    return (repo / REPO_INTERNAL_DIR / "states").resolve()


def repo_snapshot_capture(
    *,
    name: str,
    worktree: str = "",
    root: Optional[Path] = None,
) -> dict:
    repo = root.resolve() if root is not None else repo_root()
    wt_path = _repo_resolve_worktree(repo, worktree)
    if not wt_path.exists() or not is_git_repo(wt_path):
        raise WorkspaceError(f"Not a git worktree: {wt_path}")

    _repo_states_dir(repo).mkdir(parents=True, exist_ok=True)
    snap_path = _repo_states_dir(repo) / f"{fs_escape(name)}.json"

    snap = {
        "name": name,
        "captured_at": now_iso(),
        "target": {"worktree": str(wt_path.resolve())},
        "state": {
            "branch": run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=wt_path
            ).stdout.strip(),
            "commit": run(["git", "rev-parse", "HEAD"], cwd=wt_path).stdout.strip(),
            "dirty": git_is_dirty(wt_path),
        },
    }
    atomic_write_json(snap_path, snap)
    return {"snapshot_path": str(snap_path.resolve()), "snapshot": snap}


def repo_snapshot_diff(*, name: str, root: Optional[Path] = None) -> dict:
    repo = root.resolve() if root is not None else repo_root()
    snap_path = _repo_states_dir(repo) / f"{fs_escape(name)}.json"
    if not snap_path.exists():
        raise WorkspaceError(f"Missing snapshot: {snap_path}")
    snap = read_json(snap_path)
    if not isinstance(snap, dict):
        raise WorkspaceError(f"Invalid snapshot file: {snap_path}")

    target = (snap.get("target") or {}).get("worktree")
    wt_path = Path(str(target or repo)).resolve()
    if not wt_path.exists() or not is_git_repo(wt_path):
        return {
            "snapshot_path": str(snap_path.resolve()),
            "name": name,
            "status": "missing",
            "target": str(wt_path),
        }

    cur = {
        "branch": run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=wt_path
        ).stdout.strip(),
        "commit": run(["git", "rev-parse", "HEAD"], cwd=wt_path).stdout.strip(),
        "dirty": git_is_dirty(wt_path),
    }
    prev = snap.get("state") or {}
    mismatches: Dict[str, Any] = {}
    for key in ("branch", "commit", "dirty"):
        if cur.get(key) != prev.get(key):
            mismatches[key] = {"current": cur.get(key), "snapshot": prev.get(key)}

    return {
        "snapshot_path": str(snap_path.resolve()),
        "name": name,
        "target": str(wt_path.resolve()),
        "mismatches": mismatches,
        "ok": not bool(mismatches),
    }


def repo_snapshot_restore(
    *,
    name: str,
    confirm: bool,
    force_clean: bool = False,
    root: Optional[Path] = None,
) -> dict:
    if not confirm:
        raise WorkspaceError("Refusing to restore snapshot without --yes")

    repo = root.resolve() if root is not None else repo_root()
    snap_path = _repo_states_dir(repo) / f"{fs_escape(name)}.json"
    if not snap_path.exists():
        raise WorkspaceError(f"Missing snapshot: {snap_path}")
    snap = read_json(snap_path)
    if not isinstance(snap, dict):
        raise WorkspaceError(f"Invalid snapshot file: {snap_path}")

    target = (snap.get("target") or {}).get("worktree")
    wt_path = Path(str(target or repo)).resolve()
    if not wt_path.exists() or not is_git_repo(wt_path):
        raise WorkspaceError(f"Not a git worktree: {wt_path}")

    state = snap.get("state") or {}
    commit0 = str(state.get("commit") or "").strip()
    branch0 = str(state.get("branch") or "").strip()
    if not commit0:
        raise WorkspaceError("Invalid snapshot: missing commit")

    if git_is_dirty(wt_path) and not force_clean:
        raise WorkspaceError(
            "Refusing to restore onto a dirty worktree (use --force-clean)"
        )

    if force_clean:
        run(["git", "merge", "--abort"], cwd=wt_path, check=False)
        run(["git", "reset", "--hard"], cwd=wt_path, check=False)
        run(["git", "clean", "-fd"], cwd=wt_path, check=False)

    if branch0 == "HEAD":
        run(["git", "checkout", "--detach", commit0], cwd=wt_path)
    else:
        run(["git", "checkout", "-B", branch0, commit0], cwd=wt_path)

    return {
        "snapshot_path": str(snap_path.resolve()),
        "name": name,
        "target": str(wt_path.resolve()),
        "restored": True,
        "force_clean": bool(force_clean),
    }
