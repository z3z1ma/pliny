from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from agent_loom.workspace.guards import poly_context
from agent_loom.workspace.repo_ops import repo_root as repo_root_fn
from agent_loom.workspace.state import (
    fs_unescape,
    iter_repos,
    load_workspace,
    worktrees_base,
    ws_services_dir,
    ws_worktrees_dir,
)
from agent_loom.workspace.utils import is_git_repo, parallel_map, read_json
from agent_loom.workspace.git_ops import git_is_dirty, git_worktree_list_porcelain

from agent_loom.workspace.diff_ops import worktree_diff_by_file


class WorkspaceReadError(RuntimeError):
    pass


def _find_poly_root(start: Path) -> Optional[Path]:
    ctx = poly_context(start)
    if ctx.root and ctx.ws:
        return ctx.root
    return None


def detect_workspace_mode(*, cwd: Path, mode: str, root_arg: str) -> tuple[str, Path]:
    m = (mode or "auto").strip().lower()
    root_s = (root_arg or "").strip()
    if m not in {"auto", "poly", "repo"}:
        raise WorkspaceReadError("Invalid mode (expected auto|poly|repo)")

    if m == "poly":
        root = Path(root_s).expanduser().resolve() if root_s else _find_poly_root(cwd)
        if not root:
            raise WorkspaceReadError(
                "Unable to find workspace root (expected workspace.json + .loom/). Use --workspace-root."
            )
        _ = load_workspace(root)
        return "poly", root

    if m == "repo":
        if root_s:
            root = Path(root_s).expanduser().resolve()
            if not is_git_repo(root):
                raise WorkspaceReadError(f"Not a git repo: {root}")
            return "repo", root
        # In server mode, `cwd` is already anchored to the repo root.
        if is_git_repo(cwd):
            return "repo", cwd.resolve()
        return "repo", repo_root_fn()

    # auto
    poly_root = _find_poly_root(cwd)
    if poly_root is not None:
        return "poly", poly_root
    if is_git_repo(cwd):
        return "repo", cwd.resolve()
    return "repo", repo_root_fn()


def workspace_meta(*, mode: str, root: Path) -> dict[str, Any]:
    if mode == "repo":
        return {"mode": "repo", "root": str(root.resolve())}

    ws = load_workspace(root)
    wt_dir = root / ws_worktrees_dir(ws)
    groups: list[str] = []
    if wt_dir.exists():
        for p in sorted(
            [x for x in wt_dir.iterdir() if x.is_dir()], key=lambda x: x.name
        ):
            groups.append(fs_unescape(p.name))
    repos = sorted(iter_repos(ws).keys())
    return {
        "mode": "poly",
        "root": str(root.resolve()),
        "groups": groups,
        "repos": repos,
        "paths": {
            "worktrees_dir": str((root / ws_worktrees_dir(ws)).resolve()),
            "services_dir": str((root / ws_services_dir(ws)).resolve()),
        },
    }


def repo_worktrees(
    *, root: Path, q: str = "", dirty_only: bool = False
) -> dict[str, Any]:
    rows = git_worktree_list_porcelain(root)
    query = (q or "").strip().lower()
    items: list[dict[str, Any]] = []
    dirty_paths: list[Path] = []
    for row in rows:
        path = str(row.get("path") or "").strip()
        if not path:
            continue
        p = Path(path).resolve()
        entry: dict[str, Any] = {
            "mode": "repo",
            "path": str(p),
            "head": str(row.get("head") or ""),
            "branch": str(row.get("branch") or ""),
            "ref": str(row.get("ref") or ""),
            "detached": bool(row.get("detached")),
            "locked": bool(row.get("locked")),
            "is_repo": is_git_repo(p),
            "dirty": False,
        }
        if entry["is_repo"]:
            dirty_paths.append(p)
        items.append(entry)

    # Compute dirty in parallel (git status is slow for many worktrees)
    if dirty_paths:
        jobs = min(8, len(dirty_paths))
        dirties = parallel_map(lambda pp: git_is_dirty(pp), dirty_paths, jobs=jobs)
        dirty_map = {str(p.resolve()): bool(d) for p, d in zip(dirty_paths, dirties)}
        for it in items:
            if it.get("is_repo"):
                it["dirty"] = bool(
                    dirty_map.get(str(Path(str(it["path"])).resolve()), False)
                )

    # Apply filters after dirtiness is known.
    items2: list[dict[str, Any]] = []
    for entry in items:
        if dirty_only and not bool(entry.get("dirty")):
            continue
        if query:
            blob = " ".join(
                [entry.get("branch") or "", entry.get("path") or ""]
            ).lower()
            if query not in blob:
                continue
        items2.append(entry)
    items2.sort(
        key=lambda x: (
            x.get("detached") is True,
            x.get("branch") or "",
            x.get("path") or "",
        )
    )
    return {"worktrees": items2, "count": len(items2)}


def poly_worktrees(
    *,
    root: Path,
    group: str = "",
    repo: str = "",
    q: str = "",
    dirty_only: bool = False,
    missing_only: bool = False,
) -> dict[str, Any]:
    ws = load_workspace(root)
    repo_map = iter_repos(ws)

    wt_dir = root / ws_worktrees_dir(ws)
    items: list[dict[str, Any]] = []
    dirty_paths2: list[Path] = []
    if wt_dir.exists():
        for group_dir in sorted(
            [x for x in wt_dir.iterdir() if x.is_dir()], key=lambda x: x.name
        ):
            g = fs_unescape(group_dir.name)
            if group and g != group:
                continue
            for repo_dir in sorted(
                [x for x in group_dir.iterdir() if x.is_dir()], key=lambda x: x.name
            ):
                rname = repo_dir.name
                if repo and rname != repo:
                    continue
                entry: dict[str, Any] = {
                    "mode": "poly",
                    "group": g,
                    "repo": rname,
                    "path": str(repo_dir.resolve()),
                    "missing": False,
                    "is_repo": is_git_repo(repo_dir),
                }
                if entry["is_repo"]:
                    dirty_paths2.append(repo_dir)
                items.append(entry)

    if dirty_paths2:
        jobs = min(8, len(dirty_paths2))
        dirties = parallel_map(lambda pp: git_is_dirty(pp), dirty_paths2, jobs=jobs)
        dirty_map = {str(p.resolve()): bool(d) for p, d in zip(dirty_paths2, dirties)}
        for it in items:
            if it.get("is_repo"):
                it["dirty"] = bool(
                    dirty_map.get(str(Path(str(it["path"])).resolve()), False)
                )

    if group:
        base = worktrees_base(root, ws, group)
        present = {x.get("repo") for x in items if x.get("group") == group}
        for rname in sorted(repo_map.keys()):
            if repo and rname != repo:
                continue
            if rname in present:
                continue
            expected = base / rname
            items.append(
                {
                    "mode": "poly",
                    "group": group,
                    "repo": rname,
                    "path": str(expected.resolve()),
                    "missing": True,
                    "is_repo": False,
                    "dirty": False,
                }
            )

    query = (q or "").strip().lower()

    def _matches(it: dict[str, Any]) -> bool:
        if dirty_only and not bool(it.get("dirty")):
            return False
        if missing_only and not bool(it.get("missing")):
            return False
        if query:
            blob = " ".join(
                [
                    str(it.get("group") or ""),
                    str(it.get("repo") or ""),
                    str(it.get("path") or ""),
                ]
            ).lower()
            if query not in blob:
                return False
        return True

    items = [it for it in items if _matches(it)]
    items.sort(
        key=lambda x: (
            x.get("missing") is True,
            x.get("group") or "",
            x.get("repo") or "",
        )
    )
    return {"worktrees": items, "count": len(items)}


def services_index(*, root: Path) -> dict[str, Any] | None:
    ws = load_workspace(root)
    idx = root / ws_services_dir(ws) / "index.json"
    if not idx.exists():
        return None
    try:
        data = read_json(idx)
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def worktree_diff(
    *,
    mode: str,
    root: Path,
    path: str,
    diff_mode: str = "cumulative",
    base: str = "",
    max_patch_bytes: int = 2_000_000,
) -> dict[str, Any]:
    """Return a worktree diff (split by file) for a known worktree.

    Security posture: `path` must match a worktree returned by the corresponding
    `repo_worktrees` / `poly_worktrees` listing for the same mode/root.
    """

    requested = Path(str(path or "").strip()).expanduser().resolve()
    if not str(path or "").strip():
        raise WorkspaceReadError("Missing path")

    if mode == "repo":
        listing = repo_worktrees(root=root, q="", dirty_only=False)
    else:
        # In poly mode, allow diffing any present worktree under the root.
        listing = poly_worktrees(
            root=root,
            group="",
            repo="",
            q="",
            dirty_only=False,
            missing_only=False,
        )

    known: dict[str, dict[str, Any]] = {}
    for it in listing.get("worktrees", []) if isinstance(listing, dict) else []:
        p = Path(str((it or {}).get("path") or "")).expanduser().resolve()
        if str(p):
            known[str(p)] = it

    if str(requested) not in known:
        raise WorkspaceReadError("Unknown worktree path")

    meta = known[str(requested)]
    if bool(meta.get("missing")):
        raise WorkspaceReadError("Worktree is missing")
    if not is_git_repo(requested):
        raise WorkspaceReadError("Not a git worktree")

    dm = str(diff_mode or "cumulative").strip().lower()
    if dm not in {"dirty", "cumulative"}:
        raise WorkspaceReadError("Invalid diff_mode (expected dirty|cumulative)")

    # Determine default branch for cumulative resolution.
    default_branch = "main"
    if mode == "poly":
        try:
            ws = load_workspace(root)
            repo_name = str(meta.get("repo") or "").strip()
            if repo_name:
                r = iter_repos(ws).get(repo_name)
                if r:
                    default_branch = str(
                        getattr(r, "default_branch", "") or default_branch
                    )
        except Exception:
            pass
    else:
        # Best-effort: infer from origin/HEAD when present.
        try:
            from agent_loom.workspace.git_ops import repo_default_branch

            default_branch = repo_default_branch(requested)
        except Exception:
            pass

    files, untracked, truncated, base_used, merge_base = worktree_diff_by_file(
        worktree=requested,
        diff_mode=dm,
        base_ref=str(base or "").strip() or None,
        default_branch=default_branch,
        max_patch_bytes=int(max_patch_bytes),
    )
    payload_files = [
        {"path": f.path, "adds": f.adds, "dels": f.dels, "patch": f.patch}
        for f in files
    ]
    return {
        "mode": mode,
        "worktree": str(requested),
        "diff_mode": dm,
        "base": str(base_used or ""),
        "merge_base": str(merge_base or ""),
        "files": payload_files,
        "untracked": untracked,
        "truncated": bool(truncated),
    }
