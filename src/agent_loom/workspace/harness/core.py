from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from agent_loom.core.concurrent import parallel_map
from agent_loom.core.fs import ensure_dir, fs_escape, fs_unescape
from agent_loom.core.git import is_git_repo
from agent_loom.core.io import atomic_write_json, atomic_write_text, read_json
from agent_loom.core.time import now_iso
from agent_loom.workspace.constants import (
    DEFAULT_DEFAULT_BRANCH,
    HARNESS_DIR,
    INTERNAL_DIR,
    SHA_RE,
    WORKSPACE_FILE,
)
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.git.core import (
    git_checkout_reset_branch,
    git_clone_if_missing,
    git_current_branch,
    git_ensure_branch,
    git_fetch,
    git_fetch_ref,
    git_head_sha,
    git_is_dirty,
    git_ref_exists,
    git_worktree_add,
    git_worktree_remove,
    git_worktree_remove_from,
    repo_default_branch,
    require_git,
)
from agent_loom.workspace.guards import harness_root
from agent_loom.workspace.models import (
    AddRepoResult,
    BranchResult,
    ContextResult,
    DeepenResult,
    DepsShowResult,
    DepsWhoUsesResult,
    ListReposResult,
    HarnessInitResult,
    RemoveRepoResult,
    ComponentsRefreshIndexResult,
    SnapshotResult,
    SnapshotDiffResult,
    SnapshotRestoreResult,
    StatusResult,
    SyncResult,
    WorktreeAddResult,
    WorktreeGroupRemoveResult,
    WorktreeGroupDiffResult,
    WorktreeListResult,
    WorktreePushResult,
    WorktreeRebaseResult,
)
from agent_loom.workspace.harness.selection import (
    harness_has_selection,
    harness_resolve_repo_names,
)
from agent_loom.workspace.harness.components import (
    components_index_path,
    ensure_component_files,
    refresh_components_index,
)
from agent_loom.workspace.state import (
    Repo,
    default_workspace_json,
    harness_manifest_path,
    iter_repos,
    load_workspace,
    save_workspace,
    snapshot_path,
    validate_workspace,
    validate_repo_name,
    worktrees_base,
    ws_repos_dir,
    ws_components_dir,
    ws_states_dir,
    ws_worktrees_dir,
)
from agent_loom.workspace.utils import run, short

from agent_loom.workspace.git.diff import worktree_diff_by_file


def _touch_group_meta(*, ws_root: Path, group: str) -> None:
    try:
        from agent_loom.workspace.worktree_meta import harness_group_touch

        harness_group_touch(ws_root=ws_root, group=group)
    except Exception:
        return


def _iter_group_bases(*, ws_root: Path, ws: dict) -> List[tuple[str, Path]]:
    groups: Dict[str, Path] = {}

    wt_dir = ws_root / ws_worktrees_dir(ws)
    if wt_dir.exists():
        for group_dir in sorted(p for p in wt_dir.iterdir() if p.is_dir()):
            group = fs_unescape(group_dir.name)
            groups[group] = group_dir.resolve()

    meta_dir = (ws_root / INTERNAL_DIR / HARNESS_DIR / "meta" / "groups").resolve()
    if meta_dir.exists():
        for p in sorted(meta_dir.glob("*.json")):
            try:
                meta = read_json(p)
            except Exception:
                continue
            if not isinstance(meta, dict):
                continue
            group = str(meta.get("group") or "").strip() or fs_unescape(p.stem)
            if not group:
                continue
            groups[group] = worktrees_base(ws_root, ws, group).resolve()

    return sorted(groups.items(), key=lambda x: x[0])


def harness_init(
    *, root: Optional[Path] = None, symlinks: bool = False
) -> HarnessInitResult:
    require_git()
    ws_root = root.resolve() if root is not None else Path.cwd().resolve()

    created: List[str] = []

    def _ensure_dir(p: Path, label: str) -> None:
        existed = p.exists()
        ensure_dir(p)
        if not existed:
            created.append(label)

    from agent_loom.workspace.state import harness_manifest_path

    wf = harness_manifest_path(ws_root)
    if wf.exists():
        ws = validate_workspace(ws_root, read_json(wf))
    else:
        ws = default_workspace_json()
        save_workspace(ws_root, ws)
        created.append(str(wf.relative_to(ws_root)))

    _ensure_dir(wf.parent, f"{wf.parent.relative_to(ws_root)}/")
    _ensure_dir(ws_root / ws_repos_dir(ws), f"{ws_repos_dir(ws)}/")
    _ensure_dir(ws_root / ws_worktrees_dir(ws), f"{ws_worktrees_dir(ws)}/")
    _ensure_dir(ws_root / ws_states_dir(ws), f"{ws_states_dir(ws)}/")
    _ensure_dir(ws_root / ws_components_dir(ws), f"{ws_components_dir(ws)}/")

    if symlinks:
        links: list[tuple[str, str]] = [
            ("repos", ws_repos_dir(ws)),
            ("worktrees", ws_worktrees_dir(ws)),
            ("states", ws_states_dir(ws)),
            ("components", ws_components_dir(ws)),
        ]
        for link_name, target_rel in links:
            lp = ws_root / link_name
            tp = Path(target_rel)
            if lp.exists() or lp.is_symlink():
                if not lp.is_symlink():
                    raise WorkspaceError(
                        f"Refusing to create symlink '{link_name}': path exists and is not a symlink: {lp}"
                    )
                try:
                    if Path(lp.readlink()) != tp:
                        raise WorkspaceError(
                            f"Refusing to change existing symlink '{link_name}': expected -> {tp}, got -> {lp.readlink()}"
                        )
                except OSError as e:
                    raise WorkspaceError(
                        f"Unable to read existing symlink '{link_name}': {e}"
                    ) from e
                continue
            try:
                lp.symlink_to(tp)
            except OSError as e:
                raise WorkspaceError(
                    f"Failed to create symlink '{link_name}': {e}"
                ) from e

    # Ensure baseline ignores exist. Preserve existing file content.
    gi = ws_root / ".gitignore"
    baseline = [
        f"{ws_repos_dir(ws)}/",
        f"{ws_worktrees_dir(ws)}/",
        f"{ws_states_dir(ws)}/",
        f"{ws_components_dir(ws)}/index.json",
        f"{INTERNAL_DIR}/ticket/",
        f"{INTERNAL_DIR}/memory/",
        f"{INTERNAL_DIR}/team/",
        f"{INTERNAL_DIR}/workspace/",
        f"{INTERNAL_DIR}/workspaces/meta/",
        f"{INTERNAL_DIR}/workspaces/leases/",
    ]
    if symlinks:
        baseline += ["repos/", "worktrees/", "states/", "components/index.json"]

    updated_gitignore = False
    if not gi.exists():
        atomic_write_text(gi, "\n".join(baseline + [""]) + "\n")
        created.append(".gitignore")
        updated_gitignore = True
    else:
        existing = gi.read_text(encoding="utf-8")
        existing_lines = [ln.rstrip("\n") for ln in existing.splitlines()]
        existing_set = {ln.strip() for ln in existing_lines if ln.strip()}
        missing = [
            ln for ln in baseline if ln.strip() and ln.strip() not in existing_set
        ]
        if missing:
            text = existing.rstrip("\n")
            if text:
                text += "\n"
            text += "\n".join(missing) + "\n"
            atomic_write_text(gi, text)
            updated_gitignore = True

    # Ensure empty components index exists.
    idx = components_index_path(ws_root, ws)
    if not idx.exists():
        atomic_write_json(idx, {"updated_at": now_iso(), "components": {}})
        created.append(f"{ws_components_dir(ws)}/index.json")

    return HarnessInitResult(
        workspace_file=str(wf.resolve()),
        repos_dir=str((ws_root / ws_repos_dir(ws)).resolve()),
        worktrees_dir=str((ws_root / ws_worktrees_dir(ws)).resolve()),
        states_dir=str((ws_root / ws_states_dir(ws)).resolve()),
        components_dir=str((ws_root / ws_components_dir(ws)).resolve()),
        gitignore_path=str(gi.resolve()),
        created=sorted({c for c in created if c}),
        updated_gitignore=bool(updated_gitignore),
    )


def add_repo(
    *,
    name: str,
    remote: str,
    default_branch: str = "",
    shallow: bool = False,
    depth: int = 1,
    clone: bool = False,
    force: bool = False,
    root: Optional[Path] = None,
) -> AddRepoResult:
    require_git()
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)

    validate_repo_name(name)
    default_branch_arg = str(default_branch or "").strip()
    infer_default_branch = not bool(default_branch_arg)
    default_branch = default_branch_arg or DEFAULT_DEFAULT_BRANCH

    if name in ws["repos"] and not force:
        raise WorkspaceError(
            f"Repo '{name}' already exists in {WORKSPACE_FILE} (use --force to overwrite)."
        )

    entry: Dict[str, Any] = {"remote": remote, "default_branch": default_branch}

    if shallow:
        entry["shallow"] = True
        entry["depth"] = max(1, int(depth))
    else:
        entry["shallow"] = False

    ws["repos"][name] = entry

    save_workspace(ws_root, ws)

    # Ensure components metadata file exists
    ensure_component_files(ws_root, ws, [name])
    refresh_components_index(ws_root, ws)

    if clone:
        repo_path = (ws_root / ws_repos_dir(ws) / name).resolve()

        # If the user didn't pass --default-branch, prefer cloning without specifying
        # a branch, then infer origin/HEAD via repo_default_branch().
        if infer_default_branch:
            if repo_path.exists():
                if not is_git_repo(repo_path):
                    raise WorkspaceError(
                        f"Path exists but is not a git repo: {repo_path}"
                    )
            else:
                ensure_dir(repo_path.parent)
                depth = max(1, int(entry.get("depth", 1)))
                cmd = ["git", "clone"]
                if bool(entry.get("shallow", False)):
                    cmd += ["--depth", str(depth)]
                cmd += [remote, str(repo_path)]
                run(cmd, cwd=ws_root)

            detected = repo_default_branch(repo_path)
            if detected and detected != entry.get("default_branch"):
                entry["default_branch"] = detected
                ws["repos"][name] = entry
                save_workspace(ws_root, ws)

        repo = Repo(
            name=name,
            remote=remote,
            default_branch=str(entry.get("default_branch") or DEFAULT_DEFAULT_BRANCH),
            shallow=bool(entry.get("shallow", False)),
            depth=int(entry.get("depth", 1)),
            repos_dir=ws_repos_dir(ws),
        )
        if not infer_default_branch:
            git_clone_if_missing(ws_root, repo)
        git_fetch(ws_root, repo)

    return AddRepoResult(repo=name, entry=ws["repos"][name], cloned=bool(clone))


def remove_repo(
    *,
    name: str,
    delete_clone: bool = False,
    delete_component_md: bool = False,
    confirm_delete: bool = False,
    root: Optional[Path] = None,
) -> RemoveRepoResult:
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)

    validate_repo_name(name)
    if name not in ws["repos"]:
        raise WorkspaceError(f"Repo '{name}' not present in {WORKSPACE_FILE}.")

    clone_base = (ws_root / ws_repos_dir(ws)).resolve()
    clone_path = (clone_base / name).resolve()
    svc_base = (ws_root / ws_components_dir(ws)).resolve()
    svc_path = (svc_base / f"{name}.md").resolve()

    if delete_clone and not confirm_delete:
        raise WorkspaceError("Refusing to delete clone without --yes-delete")

    if delete_clone and clone_path.exists():
        if clone_base not in clone_path.parents:
            raise WorkspaceError(
                f"Refusing to delete path outside repos_dir: {clone_path}"
            )
        shutil.rmtree(clone_path)

    if delete_component_md and svc_path.exists():
        if svc_base not in svc_path.parents:
            raise WorkspaceError(
                f"Refusing to delete path outside components_dir: {svc_path}"
            )
        svc_path.unlink()

    # Remove from manifest
    del ws["repos"][name]
    save_workspace(ws_root, ws)
    refresh_components_index(ws_root, ws)

    return RemoveRepoResult(
        repo=name,
        deleted_clone=bool(delete_clone),
        deleted_component_md=bool(delete_component_md),
    )


def list_repos(*, root: Optional[Path] = None) -> ListReposResult:
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repos = iter_repos(ws)
    rows = [
        {
            "name": name,
            "remote": repos[name].remote,
            "default_branch": repos[name].default_branch,
            "tags": repos[name].tags,
            "description": repos[name].description,
            "path": str((ws_root / repos[name].path).resolve()),
        }
        for name in sorted(repos.keys())
    ]

    return ListReposResult(repos=rows, repo_sets=ws.get("repo_sets", {}))


def context(
    *,
    root: Optional[Path] = None,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    jobs: int = 1,
) -> ContextResult:
    """Emit a compact, AI-friendly view of the entire workspace state."""

    require_git()
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)

    names = harness_resolve_repo_names(
        ws,
        repo_map,
        repo_names=repos,
        sets=sets,
        tags=tags,
    )

    def _context_one(name: str) -> dict:
        r = repo_map[name]
        p = ws_root / r.path
        rec: dict = {
            "name": name,
            "remote": r.remote,
            "default_branch": r.default_branch,
            "tags": r.tags,
            "description": r.description,
            "path": str(p.resolve()),
            "exists": p.exists(),
            "is_repo": is_git_repo(p) if p.exists() else False,
        }
        if rec["is_repo"]:
            rec.update(
                {
                    "branch": git_current_branch(p),
                    "commit": git_head_sha(p),
                    "dirty": git_is_dirty(p),
                }
            )
        return rec

    repo_status = parallel_map(_context_one, names, int(jobs or 1))

    idx_path = components_index_path(ws_root, ws)
    components_index = read_json(idx_path) if idx_path.exists() else None

    worktrees: List[dict] = []
    for group, group_dir in _iter_group_bases(ws_root=ws_root, ws=ws):
        if not group_dir.exists() or not group_dir.is_dir():
            continue
        for repo_dir in sorted(p for p in group_dir.iterdir() if p.is_dir()):
            repo = repo_dir.name
            entry: dict = {
                "group": group,
                "repo": repo,
                "path": str(repo_dir.resolve()),
                "is_repo": is_git_repo(repo_dir),
            }
            if entry["is_repo"]:
                entry.update(
                    {
                        "branch": git_current_branch(repo_dir),
                        "commit": git_head_sha(repo_dir),
                        "dirty": git_is_dirty(repo_dir),
                    }
                )
            worktrees.append(entry)

    return ContextResult(
        workspace={
            "version": ws.get("version"),
            "workspace_file": str(harness_manifest_path(ws_root).resolve()),
            "repos_dir": str((ws_root / ws_repos_dir(ws)).resolve()),
            "worktrees_dir": str((ws_root / ws_worktrees_dir(ws)).resolve()),
            "states_dir": str((ws_root / ws_states_dir(ws)).resolve()),
            "components_dir": str((ws_root / ws_components_dir(ws)).resolve()),
            "repo_sets": ws.get("repo_sets", {}),
        },
        repos=repo_status,
        worktrees=worktrees,
        components_index=components_index,
    )


def sync(
    *,
    root: Optional[Path] = None,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    clone: bool = False,
    jobs: int = 1,
    allow_all: bool = False,
) -> SyncResult:
    require_git()
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)

    if not repo_map:
        return SyncResult(results=[], components_index=None)

    names = harness_resolve_repo_names(
        ws,
        repo_map,
        repo_names=repos,
        sets=sets,
        tags=tags,
        require_intent_for_multi=True,
        allow_all=allow_all,
    )

    def _sync_one(name: str) -> dict:
        r = repo_map[name]
        rec: dict = {"repo": name, "actions": [], "warnings": []}
        try:
            if clone:
                git_clone_if_missing(ws_root, r)
                rec["actions"].append("cloned")

            if (ws_root / r.path).exists():
                repo_path = ws_root / r.path
                git_fetch(ws_root, r)
                rec["actions"].append("fetched")

                current_branch = git_current_branch(repo_path)
                if current_branch == r.default_branch:
                    try:
                        run(
                            ["git", "pull", "--ff-only", "origin", r.default_branch],
                            cwd=repo_path,
                        )
                        rec["actions"].append("pulled")
                    except WorkspaceError as e:
                        rec["warnings"].append(
                            f"pull failed (may need rebase or merge): {e}"
                        )
            else:
                rec["warnings"].append("missing clone")
        except WorkspaceError as e:
            rec["error"] = str(e)
        return rec

    results = parallel_map(_sync_one, names, int(jobs or 1))

    index = refresh_components_index(ws_root, ws)

    return SyncResult(results=results, components_index=index)


def status(
    *,
    root: Optional[Path] = None,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    jobs: int = 1,
    allow_all: bool = False,
) -> StatusResult:
    require_git()
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)
    if not repo_map:
        return StatusResult(repos=[])

    names = harness_resolve_repo_names(
        ws,
        repo_map,
        repo_names=repos,
        sets=sets,
        tags=tags,
        allow_all=allow_all,
    )

    def _status_one(name: str) -> Tuple[str, str, str, str]:
        r = repo_map.get(name)
        if not r:
            return (name, "UNKNOWN", "-", "-")
        p = ws_root / r.path
        if not p.exists():
            return (name, "MISSING", "-", "-")
        if not is_git_repo(p):
            return (name, "NOT_A_REPO", "-", "-")
        br = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=p).stdout.strip()
        sha = short(run(["git", "rev-parse", "HEAD"], cwd=p).stdout.strip())
        dirty = "DIRTY" if git_is_dirty(p) else "clean"
        return (name, br, sha, dirty)

    rows = parallel_map(_status_one, names, int(jobs or 1))

    return StatusResult(
        repos=[
            {"repo": n, "branch": br, "sha": sha, "status": st}
            for (n, br, sha, st) in rows
        ]
    )


def branch(
    *,
    branch: str,
    reset: bool = False,
    allow_dirty: bool = False,
    clone: bool = False,
    base_ref: Optional[str] = None,
    refresh_index: bool = False,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    confirm_reset: bool = False,
    root: Optional[Path] = None,
) -> BranchResult:
    require_git()
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)

    if reset and not confirm_reset:
        raise WorkspaceError("Refusing to reset branches without --yes")
    names = harness_resolve_repo_names(
        ws,
        repo_map,
        repo_names=repos,
        sets=sets,
        tags=tags,
        require_intent_for_multi=True,
        allow_all=allow_all,
    )

    results: List[dict] = []
    for name in names:
        r = repo_map[name]
        if clone:
            git_clone_if_missing(ws_root, r)
        p = ws_root / r.path
        if not p.exists():
            raise WorkspaceError(
                f"Repo not cloned: {name} (use --clone or run `loom workspace harness sync --clone --all`)"
            )

        if git_is_dirty(p) and not allow_dirty:
            raise WorkspaceError(
                f"Repo has uncommitted changes: {p} (use --allow-dirty to override)"
            )

        git_fetch(ws_root, r)

        if reset:
            git_checkout_reset_branch(ws_root, r, branch, base_ref=base_ref)
        else:
            git_ensure_branch(ws_root, r, branch, base_ref=base_ref)
            run(["git", "checkout", branch], cwd=p)

        results.append({"repo": name, "branch": branch})

    index = None
    if refresh_index:
        index = refresh_components_index(ws_root, ws)

    return BranchResult(branch=branch, repos=results, components_index=index)


def worktree_add(
    *,
    group: str,
    base_ref: Optional[str] = None,
    path: Optional[str] = None,
    clone: bool = False,
    allow_dirty: bool = False,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    root: Optional[Path] = None,
) -> WorktreeAddResult:
    require_git()
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)

    names = harness_resolve_repo_names(
        ws,
        repo_map,
        repo_names=repos,
        sets=sets,
        tags=tags,
        require_intent_for_multi=True,
        allow_all=allow_all,
    )

    raw_path = str(path or "").strip()
    if raw_path:
        # The harness needs to be able to control where group worktrees live.
        # This is stored in group metadata so subsequent group operations remain coherent.
        desired = Path(raw_path).expanduser()
        desired = (desired if desired.is_absolute() else (ws_root / desired)).resolve()

        default_base = (ws_root / ws_worktrees_dir(ws) / fs_escape(group)).resolve()
        if default_base.exists() and any(p.is_dir() for p in default_base.iterdir()):
            raise WorkspaceError(
                "Refusing to change group worktree base when default group dir already exists. "
                "Pick a new group name or remove existing worktrees first."
            )

        try:
            from agent_loom.workspace.worktree_meta import harness_group_meta_path

            mp = harness_group_meta_path(ws_root, group)
            if mp.exists():
                try:
                    meta = read_json(mp)
                except Exception:
                    meta = {}
                if isinstance(meta, dict):
                    existing_raw = str(meta.get("worktrees_base_path") or "").strip()
                    if existing_raw:
                        existing_p = Path(existing_raw).expanduser()
                        existing_p = (
                            existing_p
                            if existing_p.is_absolute()
                            else (ws_root / existing_p)
                        ).resolve()
                        if existing_p != desired:
                            raise WorkspaceError(
                                "Group already has a configured worktrees base path; refusing to change it. "
                                f"group={group} existing={existing_p} requested={desired}"
                            )
        except WorkspaceError:
            raise
        except Exception:
            pass

        from agent_loom.workspace.worktree_meta import harness_group_set_worktrees_base

        harness_group_set_worktrees_base(
            ws_root=ws_root, group=group, base_path=str(desired)
        )

    created: List[dict] = []
    for name in names:
        r = repo_map[name]
        if clone:
            git_clone_if_missing(ws_root, r)
        p = ws_root / r.path
        if not p.exists():
            raise WorkspaceError(f"Repo not cloned: {name} (use --clone)")

        git_fetch(ws_root, r)

        existing_wt = worktrees_base(ws_root, ws, group) / r.name
        if existing_wt.exists():
            wt = git_worktree_add(ws_root, ws, r, group)
            created.append({"repo": name, "path": str(wt.resolve()), "existed": True})
            continue

        repo_path = ws_root / r.path
        if git_is_dirty(repo_path) and not allow_dirty:
            raise WorkspaceError(
                f"Repo has uncommitted changes: {repo_path} (use --allow-dirty to override)"
            )
        orig_branch = git_current_branch(repo_path)
        safe_branch = (
            r.default_branch if orig_branch in ("HEAD", group) else orig_branch
        )

        try:
            run(["git", "checkout", safe_branch], cwd=repo_path)
        except WorkspaceError:
            safe_branch = r.default_branch
            run(["git", "checkout", safe_branch], cwd=repo_path)

        git_ensure_branch(ws_root, r, group, base_ref=base_ref)

        wt = git_worktree_add(ws_root, ws, r, group)
        created.append({"repo": name, "path": str(wt.resolve()), "existed": False})

    _touch_group_meta(ws_root=ws_root, group=group)

    return WorktreeAddResult(group=group, worktrees=created)


def worktree_rm(
    *,
    group: str,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    force: bool = False,
    confirm: bool = False,
    root: Optional[Path] = None,
) -> WorktreeGroupRemoveResult:
    require_git()
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)

    if not confirm:
        raise WorkspaceError("Refusing to remove worktrees without --yes")

    base = worktrees_base(ws_root, ws, group)
    if not base.exists():
        return WorktreeGroupRemoveResult(group=group, removed=[])

    targets: List[Path]
    if repos or sets or tags:
        names = harness_resolve_repo_names(
            ws,
            repo_map,
            repo_names=repos,
            sets=sets,
            tags=tags,
            require_intent_for_multi=True,
            allow_all=allow_all,
        )
        targets = [base / n for n in names]
    else:
        targets = [p for p in base.iterdir() if p.is_dir()]

    if len(targets) > 1 and not harness_has_selection(
        repos=repos, sets=sets, tags=tags, allow_all=allow_all
    ):
        raise WorkspaceError(
            "Refusing to remove worktrees for multiple repos without explicit intent. "
            "Pass --all, or select repos via --repos/--set/--tag."
        )

    removed: List[str] = []

    for t in targets:
        repo_name = t.name
        repo_path = ws_root / ws_repos_dir(ws) / repo_name
        if repo_path.exists() and is_git_repo(repo_path):
            git_worktree_remove_from(repo_path, t, force=force)
        else:
            git_worktree_remove(t, force=force)
        removed.append(str(t.resolve()))

    # If the group is now empty, remove group-level metadata + stale leases.
    try:
        if base.exists() and not any(p.is_dir() for p in base.iterdir()):
            base.rmdir()
    except Exception:
        pass

    try:
        is_empty = (not base.exists()) or (not any(p.is_dir() for p in base.iterdir()))
    except Exception:
        is_empty = False
    if is_empty:
        try:
            from agent_loom.workspace.worktree_meta import harness_group_meta_path

            harness_group_meta_path(ws_root, group).unlink(missing_ok=True)
        except Exception:
            pass
        try:
            from agent_loom.workspace.harness.leases import lease_path

            lease_path(root=ws_root, key=f"group:{group}").unlink(missing_ok=True)
        except Exception:
            pass

    return WorktreeGroupRemoveResult(group=group, removed=removed)


def worktree_ls(*, root: Optional[Path] = None) -> WorktreeListResult:
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)

    rows: List[Tuple[str, str, str, str, str]] = []
    for group, group_dir in _iter_group_bases(ws_root=ws_root, ws=ws):
        if not group_dir.exists() or not group_dir.is_dir():
            continue
        for repo_dir in sorted(p for p in group_dir.iterdir() if p.is_dir()):
            repo = repo_dir.name
            if not is_git_repo(repo_dir):
                rows.append((group, repo, "NOT_A_REPO", "-", "-"))
                continue
            br = git_current_branch(repo_dir)
            sha = short(git_head_sha(repo_dir))
            dirty = "DIRTY" if git_is_dirty(repo_dir) else "clean"
            rows.append((group, repo, br, sha, dirty))

    return WorktreeListResult(
        worktrees=[
            {"group": g, "repo": repo, "branch": br, "sha": sha, "status": st}
            for (g, repo, br, sha, st) in rows
        ]
    )


def worktree_prune(
    *,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    root: Optional[Path] = None,
) -> dict:
    require_git()
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)

    names = harness_resolve_repo_names(
        ws,
        repo_map,
        repo_names=repos,
        sets=sets,
        tags=tags,
        require_intent_for_multi=True,
        allow_all=allow_all,
    )

    results: List[dict] = []
    for name in names:
        r = repo_map[name]
        repo_path = (ws_root / r.path).resolve()
        if not repo_path.exists() or not is_git_repo(repo_path):
            results.append({"repo": name, "status": "skip", "reason": "not_a_repo"})
            continue
        p = run(["git", "worktree", "prune"], cwd=repo_path, check=False)
        results.append(
            {
                "repo": name,
                "status": "success" if p.returncode == 0 else "fail",
                "exit_code": int(p.returncode),
            }
        )

    return {"results": results}


def worktree_group_status(
    *,
    group: str,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    root: Optional[Path] = None,
) -> dict:
    require_git()
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)

    base = worktrees_base(ws_root, ws, group)
    if not base.exists():
        raise WorkspaceError(f"No worktrees found for: {group}")

    _touch_group_meta(ws_root=ws_root, group=group)

    if repos or sets or tags:
        names = harness_resolve_repo_names(
            ws,
            repo_map,
            repo_names=repos,
            sets=sets,
            tags=tags,
            require_intent_for_multi=True,
            allow_all=allow_all,
        )
        targets = [(n, base / n) for n in names]
    else:
        targets = [(p.name, p) for p in base.iterdir() if p.is_dir()]

    rows: List[dict] = []
    for repo_name, wt_path in targets:
        rec: dict = {"repo": repo_name, "path": str(wt_path.resolve())}
        if not wt_path.exists() or not is_git_repo(wt_path):
            rec.update({"is_repo": False})
        else:
            rec.update(
                {
                    "is_repo": True,
                    "branch": git_current_branch(wt_path),
                    "commit": git_head_sha(wt_path),
                    "dirty": git_is_dirty(wt_path),
                }
            )
        rows.append(rec)

    return {"group": group, "worktrees": rows}


def worktree_group_check_clean(
    *,
    group: str,
    allow_untracked: bool = False,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    root: Optional[Path] = None,
) -> dict:
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)

    base = worktrees_base(ws_root, ws, group)
    if not base.exists():
        raise WorkspaceError(f"No worktrees found for: {group}")

    if repos or sets or tags:
        names = harness_resolve_repo_names(
            ws,
            repo_map,
            repo_names=repos,
            sets=sets,
            tags=tags,
            require_intent_for_multi=True,
            allow_all=allow_all,
        )
        targets = [base / n for n in names]
    else:
        targets = [p for p in base.iterdir() if p.is_dir()]

    results: List[dict] = []
    for wt_path in targets:
        repo_name = wt_path.name
        if not wt_path.exists() or not is_git_repo(wt_path):
            results.append(
                {"repo": repo_name, "status": "skip", "reason": "not_a_repo"}
            )
            continue
        out = run(["git", "status", "--porcelain"], cwd=wt_path).stdout
        lines = [ln for ln in out.splitlines() if ln.strip()]
        if allow_untracked:
            dirty = any(not ln.startswith("??") for ln in lines)
        else:
            dirty = bool(lines)
        results.append(
            {
                "repo": repo_name,
                "dirty": bool(dirty),
                "ok": not dirty,
            }
        )

    return {
        "group": group,
        "allow_untracked": bool(allow_untracked),
        "results": results,
    }


def worktree_group_check_divergence(
    *,
    group: str,
    base: str,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    root: Optional[Path] = None,
) -> dict:
    base_ref = str(base or "").strip()
    if not base_ref:
        raise WorkspaceError("Missing --base")

    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)
    base_dir = worktrees_base(ws_root, ws, group)
    if not base_dir.exists():
        raise WorkspaceError(f"No worktrees found for: {group}")

    _touch_group_meta(ws_root=ws_root, group=group)

    if repos or sets or tags:
        names = harness_resolve_repo_names(
            ws,
            repo_map,
            repo_names=repos,
            sets=sets,
            tags=tags,
            require_intent_for_multi=True,
            allow_all=allow_all,
        )
        targets = [base_dir / n for n in names]
    else:
        targets = [p for p in base_dir.iterdir() if p.is_dir()]

    results: List[dict] = []
    for wt_path in targets:
        repo_name = wt_path.name
        if not wt_path.exists() or not is_git_repo(wt_path):
            results.append(
                {"repo": repo_name, "status": "skip", "reason": "not_a_repo"}
            )
            continue
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
            results.append(
                {
                    "repo": repo_name,
                    "status": "fail",
                    "error": (p.stderr or p.stdout or "").strip(),
                }
            )
            continue
        left, right = (p.stdout.strip().split() + ["0", "0"])[:2]
        results.append(
            {
                "repo": repo_name,
                "ahead": int(right),
                "behind": int(left),
                "ok": int(left) == 0,
            }
        )

    return {"group": group, "base": base_ref, "results": results}


def worktree_group_diff(
    *,
    group: str,
    diff_mode: str = "dirty",
    base: str = "",
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    max_patch_bytes_per_repo: int = 2_000_000,
    root: Optional[Path] = None,
) -> WorktreeGroupDiffResult:
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)
    base_dir = worktrees_base(ws_root, ws, group)
    if not base_dir.exists():
        raise WorkspaceError(f"No worktrees found for: {group}")

    # Diff output can be large; require explicit intent when targeting multiple repos.
    if (repos is None or len(repos) == 0) and not harness_has_selection(
        repos=repos, sets=sets, tags=tags, allow_all=allow_all
    ):
        # If the group contains exactly one worktree repo directory, allow it.
        dirs = [p for p in base_dir.iterdir() if p.is_dir()]
        if len(dirs) != 1:
            raise WorkspaceError(
                "Refusing to diff worktrees for multiple repos without explicit intent. "
                "Pass --all, or select repos via --repos/--set/--tag."
            )

    if repos or sets or tags:
        names = harness_resolve_repo_names(
            ws,
            repo_map,
            repo_names=repos,
            sets=sets,
            tags=tags,
            require_intent_for_multi=True,
            allow_all=allow_all,
        )
        targets = [(n, base_dir / n) for n in names]
    else:
        targets = [(p.name, p) for p in base_dir.iterdir() if p.is_dir()]

    base_ref = str(base or "").strip()
    mode = str(diff_mode or "dirty").strip().lower()

    results: list[dict[str, Any]] = []
    for repo_name, wt_path in sorted(targets, key=lambda x: x[0]):
        if not wt_path.exists():
            results.append({"repo": repo_name, "status": "skip", "reason": "not_found"})
            continue
        if not is_git_repo(wt_path):
            results.append(
                {"repo": repo_name, "status": "skip", "reason": "not_a_repo"}
            )
            continue

        r = repo_map.get(repo_name)
        default_branch = str(getattr(r, "default_branch", "") or "main")
        try:
            files, untracked, truncated, base_used, merge_base = worktree_diff_by_file(
                worktree=wt_path,
                diff_mode=mode,
                base_ref=base_ref or None,
                default_branch=default_branch,
                max_patch_bytes=int(max_patch_bytes_per_repo),
            )
        except Exception as e:
            results.append(
                {
                    "repo": repo_name,
                    "status": "fail",
                    "error": str(e),
                    "worktree": str(wt_path.resolve()),
                }
            )
            continue

        payload_files = [
            {"path": f.path, "adds": f.adds, "dels": f.dels, "patch": f.patch}
            for f in files
        ]
        results.append(
            {
                "repo": repo_name,
                "status": "ok",
                "worktree": str(wt_path.resolve()),
                "diff_mode": mode,
                "base": str(base_used or ""),
                "merge_base": str(merge_base or ""),
                "files": payload_files,
                "untracked": untracked,
                "truncated": bool(truncated),
            }
        )

    return WorktreeGroupDiffResult(group=str(group), base=base_ref, results=results)


def worktree_rebase(
    *,
    group: str,
    base_ref: Optional[str] = None,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    root: Optional[Path] = None,
) -> WorktreeRebaseResult:
    require_git()
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)

    base = worktrees_base(ws_root, ws, group)
    if not base.exists():
        raise WorkspaceError(f"No worktrees found for: {group}")

    if repos or sets or tags:
        names = harness_resolve_repo_names(
            ws,
            repo_map,
            repo_names=repos,
            sets=sets,
            tags=tags,
            require_intent_for_multi=True,
            allow_all=allow_all,
        )
        targets = [(n, base / n) for n in names]
    else:
        targets = [(p.name, p) for p in base.iterdir() if p.is_dir()]

    if len(targets) > 1 and not harness_has_selection(
        repos=repos, sets=sets, tags=tags, allow_all=allow_all
    ):
        raise WorkspaceError(
            "Refusing to rebase worktrees for multiple repos without explicit intent. "
            "Pass --all, or select repos via --repos/--set/--tag."
        )

    results: List[dict] = []
    for repo_name, wt_path in targets:
        if not wt_path.exists():
            results.append({"repo": repo_name, "status": "skip", "reason": "not_found"})
            continue

        if not is_git_repo(wt_path):
            results.append(
                {"repo": repo_name, "status": "skip", "reason": "not_a_repo"}
            )
            continue

        if git_is_dirty(wt_path):
            raise WorkspaceError(
                f"Worktree {wt_path} has uncommitted changes; commit or stash first."
            )

        r = repo_map.get(repo_name)
        if not r:
            results.append(
                {"repo": repo_name, "status": "skip", "reason": "not_in_workspace"}
            )
            continue

        effective_base = base_ref or r.default_branch

        if SHA_RE.match(effective_base):
            base_obj = effective_base
        else:
            fetch_target = effective_base
            repo_path = ws_root / r.path
            git_fetch_ref(ws_root, r, fetch_target)

            preferred = f"origin/{fetch_target}"
            if git_ref_exists(repo_path, preferred):
                base_obj = preferred
            elif git_ref_exists(repo_path, "FETCH_HEAD"):
                base_obj = "FETCH_HEAD"
            else:
                base_obj = "HEAD"

        run(["git", "rebase", base_obj], cwd=wt_path)
        results.append({"repo": repo_name, "status": "success", "onto": base_obj})

    return WorktreeRebaseResult(group=group, results=results)


def worktree_push(
    *,
    group: str,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    force: bool = False,
    force_with_lease: bool = False,
    set_upstream: bool = False,
    confirm_force: bool = False,
    root: Optional[Path] = None,
) -> WorktreePushResult:
    require_git()
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)

    base = worktrees_base(ws_root, ws, group)
    if not base.exists():
        raise WorkspaceError(f"No worktrees found for: {group}")

    if repos or sets or tags:
        names = harness_resolve_repo_names(
            ws,
            repo_map,
            repo_names=repos,
            sets=sets,
            tags=tags,
            require_intent_for_multi=True,
            allow_all=allow_all,
        )
        targets = [(n, base / n) for n in names]
    else:
        targets = [(p.name, p) for p in base.iterdir() if p.is_dir()]

    if len(targets) > 1 and not harness_has_selection(
        repos=repos, sets=sets, tags=tags, allow_all=allow_all
    ):
        raise WorkspaceError(
            "Refusing to push worktrees for multiple repos without explicit intent. "
            "Pass --all, or select repos via --repos/--set/--tag."
        )

    results: List[dict] = []
    for repo_name, wt_path in targets:
        if not wt_path.exists():
            results.append({"repo": repo_name, "status": "skip", "reason": "not_found"})
            continue

        if not is_git_repo(wt_path):
            results.append(
                {"repo": repo_name, "status": "skip", "reason": "not_a_repo"}
            )
            continue

        current_branch = git_current_branch(wt_path)
        if current_branch != group:
            results.append(
                {
                    "repo": repo_name,
                    "status": "skip",
                    "reason": "wrong_branch",
                    "branch": current_branch,
                    "expected": group,
                }
            )
            continue

        if git_is_dirty(wt_path):
            results.append({"repo": repo_name, "status": "skip", "reason": "dirty"})
            continue

        if (force or force_with_lease) and not confirm_force:
            raise WorkspaceError("Refusing to force push without --yes")

        push_cmd = ["git", "push"]
        if set_upstream:
            push_cmd += ["-u", "origin", group]
        elif force_with_lease:
            push_cmd += ["--force-with-lease", "origin", group]
        elif force:
            push_cmd += ["--force", "origin", group]
        else:
            push_cmd += ["origin", group]

        run(push_cmd, cwd=wt_path)
        results.append({"repo": repo_name, "status": "success"})

    return WorktreePushResult(group=group, results=results)


def _snapshot_load(ws_root: Path, ws: dict, name: str) -> tuple[Path, dict]:
    p = snapshot_path(ws_root, ws, name)
    if not p.exists():
        raise WorkspaceError(f"Missing snapshot: {p}")
    data = read_json(p)
    if not isinstance(data, dict):
        raise WorkspaceError(f"Invalid snapshot file (expected JSON object): {p}")
    return p, data


def _snapshot_target_base(
    *, ws_root: Path, ws: dict, target: dict
) -> tuple[str, Optional[str], Path]:
    kind = str((target or {}).get("kind") or "repos").strip() or "repos"
    if kind not in {"repos", "worktrees"}:
        raise WorkspaceError(f"Unknown snapshot target kind: {kind}")

    group = str((target or {}).get("group") or "").strip() or None
    if kind == "repos":
        return kind, group, (ws_root / ws_repos_dir(ws)).resolve()
    if not group:
        raise WorkspaceError("Snapshot target kind 'worktrees' requires target.group")
    return kind, group, (worktrees_base(ws_root, ws, group)).resolve()


def snapshot(
    *,
    name: str,
    group: Optional[str] = None,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    root: Optional[Path] = None,
) -> SnapshotResult:
    require_git()
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)

    repo_names = harness_resolve_repo_names(
        ws,
        repo_map,
        repo_names=repos,
        sets=sets,
        tags=tags,
        require_intent_for_multi=True,
        allow_all=allow_all,
    )

    target: dict = {"kind": "repos"}
    if group:
        target = {"kind": "worktrees", "group": str(group)}

    kind, group_name, base = _snapshot_target_base(
        ws_root=ws_root, ws=ws, target=target
    )

    snap = {
        "name": name,
        "captured_at": now_iso(),
        "target": {"kind": kind, **({"group": group_name} if group_name else {})},
        "repos": {},
    }

    for repo_name in repo_names:
        r = repo_map.get(repo_name)
        if not r:
            snap["repos"][repo_name] = {"error": "unknown_repo"}
            continue
        p = base / r.name
        if not p.exists() or not is_git_repo(p):
            snap["repos"][repo_name] = {
                "error": "missing_or_not_a_repo",
                "path": str(p),
            }
            continue
        snap["repos"][repo_name] = {
            "path": str(p.resolve()),
            "branch": run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=p
            ).stdout.strip(),
            "commit": run(["git", "rev-parse", "HEAD"], cwd=p).stdout.strip(),
            "dirty": git_is_dirty(p),
        }

    out = snapshot_path(ws_root, ws, name)
    atomic_write_json(out, snap)
    return SnapshotResult(snapshot_path=str(out.resolve()), snapshot=snap)


def snapshot_diff(*, name: str, root: Optional[Path] = None) -> SnapshotDiffResult:
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)

    snap_path, snap = _snapshot_load(ws_root, ws, name)
    target = snap.get("target") or {"kind": "repos"}
    kind, group, base = _snapshot_target_base(ws_root=ws_root, ws=ws, target=target)

    repos_obj = snap.get("repos")
    if not isinstance(repos_obj, dict):
        raise WorkspaceError("Invalid snapshot: missing or invalid 'repos'")

    diffs: List[Dict[str, Any]] = []
    changed = 0
    missing = 0
    match = 0

    for repo_name in sorted(repos_obj.keys()):
        rec0 = repos_obj.get(repo_name) or {}
        if not isinstance(rec0, dict):
            rec0 = {}

        if rec0.get("error"):
            diffs.append(
                {
                    "repo": repo_name,
                    "status": "snapshot_error",
                    "snapshot": rec0,
                }
            )
            missing += 1
            continue

        p = base / repo_name
        if not p.exists() or not is_git_repo(p):
            diffs.append(
                {
                    "repo": repo_name,
                    "status": "missing",
                    "path": str(p),
                    "snapshot": rec0,
                }
            )
            missing += 1
            continue

        cur = {
            "path": str(p.resolve()),
            "branch": git_current_branch(p),
            "commit": run(["git", "rev-parse", "HEAD"], cwd=p).stdout.strip(),
            "dirty": git_is_dirty(p),
        }

        mismatches: Dict[str, Any] = {}
        for key in ("branch", "commit", "dirty"):
            if cur.get(key) != rec0.get(key):
                mismatches[key] = {"current": cur.get(key), "snapshot": rec0.get(key)}

        if mismatches:
            diffs.append(
                {
                    "repo": repo_name,
                    "status": "changed",
                    "mismatches": mismatches,
                    "current": cur,
                }
            )
            changed += 1
        else:
            diffs.append({"repo": repo_name, "status": "match", "current": cur})
            match += 1

    summary = {
        "repos": len(diffs),
        "match": match,
        "changed": changed,
        "missing": missing,
    }
    return SnapshotDiffResult(
        snapshot_path=str(snap_path.resolve()),
        name=name,
        target={"kind": kind, **({"group": group} if group else {})},
        diffs=diffs,
        summary=summary,
    )


def snapshot_restore(
    *,
    name: str,
    confirm: bool,
    force_clean: bool = False,
    root: Optional[Path] = None,
) -> SnapshotRestoreResult:
    if not confirm:
        raise WorkspaceError("Refusing to restore snapshot without --yes")

    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)

    snap_path, snap = _snapshot_load(ws_root, ws, name)
    target = snap.get("target") or {"kind": "repos"}
    kind, group, base = _snapshot_target_base(ws_root=ws_root, ws=ws, target=target)

    repos_obj = snap.get("repos")
    if not isinstance(repos_obj, dict):
        raise WorkspaceError("Invalid snapshot: missing or invalid 'repos'")

    results: List[Dict[str, Any]] = []
    ok = 0
    skipped = 0
    failed = 0

    def _clean(path: Path) -> None:
        run(["git", "merge", "--abort"], cwd=path, check=False)
        run(["git", "reset", "--hard"], cwd=path, check=False)
        run(["git", "clean", "-fd"], cwd=path, check=False)

    for repo_name in sorted(repos_obj.keys()):
        rec0 = repos_obj.get(repo_name) or {}
        if not isinstance(rec0, dict):
            rec0 = {}

        if rec0.get("error"):
            results.append(
                {"repo": repo_name, "status": "skip", "reason": "snapshot_error"}
            )
            skipped += 1
            continue

        commit0 = str(rec0.get("commit") or "").strip()
        branch0 = str(rec0.get("branch") or "").strip()
        if not commit0:
            results.append(
                {"repo": repo_name, "status": "skip", "reason": "missing_commit"}
            )
            skipped += 1
            continue

        p = base / repo_name
        if not p.exists() or not is_git_repo(p):
            results.append({"repo": repo_name, "status": "fail", "reason": "missing"})
            failed += 1
            continue

        try:
            if git_is_dirty(p) and not force_clean:
                results.append({"repo": repo_name, "status": "fail", "reason": "dirty"})
                failed += 1
                continue

            if force_clean:
                _clean(p)

            actions: List[str] = []
            if branch0 == "HEAD":
                run(["git", "checkout", "--detach", commit0], cwd=p)
                actions.append("checkout_detached")
            else:
                run(["git", "checkout", "-B", branch0, commit0], cwd=p)
                actions.append("checkout_branch_reset")

            results.append({"repo": repo_name, "status": "success", "actions": actions})
            ok += 1
        except WorkspaceError as e:
            results.append({"repo": repo_name, "status": "fail", "reason": str(e)})
            failed += 1

    summary = {
        "repos": len(results),
        "success": ok,
        "skipped": skipped,
        "failed": failed,
        "force_clean": bool(force_clean),
    }
    return SnapshotRestoreResult(
        snapshot_path=str(snap_path.resolve()),
        name=name,
        target={"kind": kind, **({"group": group} if group else {})},
        results=results,
        summary=summary,
    )


def components_refresh_index(
    *,
    root: Optional[Path] = None,
) -> ComponentsRefreshIndexResult:
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    index = refresh_components_index(ws_root, ws)
    return ComponentsRefreshIndexResult(
        components_index_path=str(components_index_path(ws_root, ws).resolve()),
        index=index,
    )


def services_refresh_index(
    *, root: Optional[Path] = None
) -> ComponentsRefreshIndexResult:
    """Alias for components_refresh_index (microservice-friendly naming)."""

    return components_refresh_index(root=root)


def deps_show(*, component: str, root: Optional[Path] = None) -> DepsShowResult:
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    idx_path = components_index_path(ws_root, ws)
    if not idx_path.exists():
        raise WorkspaceError(
            "Missing components/index.json (run `loom workspace harness components refresh-index`)."
        )
    idx = read_json(idx_path)

    name = component
    s = idx.get("components", {}).get(name)
    if not s:
        raise WorkspaceError(f"Unknown component in index: {name}")

    return DepsShowResult(component=name, data=s)


def deps_who_uses(*, component: str, root: Optional[Path] = None) -> DepsWhoUsesResult:
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    idx_path = components_index_path(ws_root, ws)
    if not idx_path.exists():
        raise WorkspaceError(
            "Missing components/index.json (run `loom workspace harness components refresh-index`)."
        )
    idx = read_json(idx_path)

    target = component
    s = idx.get("components", {}).get(target)
    if not s:
        raise WorkspaceError(f"Unknown component in index: {target}")

    users = s.get("used_by", [])
    return DepsWhoUsesResult(component=target, used_by=users)


def deepen(
    *,
    repo: str,
    depth: int,
    root: Optional[Path] = None,
) -> DeepenResult:
    require_git()
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)

    name = repo
    if name not in repo_map:
        raise WorkspaceError(f"Unknown repo: {name}")

    r = repo_map[name]
    if not r.shallow:
        return DeepenResult(repo=name, skipped=True, reason="not_shallow")

    path = ws_root / r.path
    if not path.exists():
        raise WorkspaceError(f"Repo not cloned: {name}")

    run(["git", "fetch", "--deepen", str(depth), "origin"], cwd=path)

    return DeepenResult(repo=name, depth=int(depth))
