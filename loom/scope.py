"""Scope and repository discovery for Loom workspaces."""

from __future__ import annotations

import os
from pathlib import Path

from .primitives import relative_to_workspace

WORKSPACE_SCOPE_ID = "workspace:main"


# ---------------------------------------------------------------------------
# Repository discovery
# ---------------------------------------------------------------------------


def discover_repositories(workspace: Path) -> list[dict]:
    repositories = []
    seen: set[str] = set()
    for current, dirs, _files in os.walk(workspace):
        current_path = Path(current)
        if ".git" in dirs or (current_path / ".git").is_file():
            rel = current_path.relative_to(workspace)
            repo_id = (
                "repo:root"
                if str(rel) == "."
                else f"repo:{str(rel).replace(os.sep, '-')}"
            )
            if repo_id not in seen:
                repositories.append(
                    {
                        "repository_id": repo_id,
                        "path": "." if str(rel) == "." else str(rel),
                        "worktree_id": f"worktree:{repo_id.split(':', 1)[1]}:default",
                    }
                )
                seen.add(repo_id)
            dirs[:] = [directory for directory in dirs if directory != ".git"]
    repositories.sort(key=lambda item: item["repository_id"])
    return repositories


def repository_ids_by_path(workspace: Path) -> dict[str, dict]:
    return {repo["repository_id"]: repo for repo in discover_repositories(workspace)}


# ---------------------------------------------------------------------------
# Scope normalization
# ---------------------------------------------------------------------------


def normalize_repository_scope(workspace: Path, repository_scope: dict | None) -> dict:
    repos = repository_ids_by_path(workspace)
    if not repository_scope:
        return {"kind": "repository", "repository_id": "repo:root"}
    if not isinstance(repository_scope, dict):
        raise SystemExit("repository_scope must be an object")
    kind = repository_scope.get("kind")
    if kind == "repository":
        repository_id = repository_scope.get("repository_id")
        if not isinstance(repository_id, str) or not repository_id:
            raise SystemExit("repository scope requires repository_id")
        if repository_id not in repos:
            raise SystemExit(
                f"unknown repository_id in repository_scope: {repository_id}"
            )
        return {"kind": "repository", "repository_id": repository_id}
    if kind == "workspace":
        workspace_id = repository_scope.get("workspace_id") or WORKSPACE_SCOPE_ID
        if not isinstance(workspace_id, str) or not workspace_id:
            raise SystemExit("workspace scope requires workspace_id")
        return {"kind": "workspace", "workspace_id": workspace_id}
    if kind == "multi_repository":
        repository_ids = repository_scope.get("repository_ids")
        if not isinstance(repository_ids, list):
            raise SystemExit("multi_repository scope requires repository_ids")
        cleaned = sorted(
            {
                repository_id
                for repository_id in repository_ids
                if isinstance(repository_id, str) and repository_id
            }
        )
        if len(cleaned) < 2:
            raise SystemExit(
                "multi_repository scope requires at least two repository_ids"
            )
        unknown = [
            repository_id for repository_id in cleaned if repository_id not in repos
        ]
        if unknown:
            raise SystemExit(
                "unknown repository_ids in repository_scope: " + ", ".join(unknown)
            )
        return {"kind": "multi_repository", "repository_ids": cleaned}
    raise SystemExit(f"unsupported repository_scope kind: {kind!r}")


def repository_ids_for_scope(
    workspace: Path, repository_scope: dict | None
) -> list[str]:
    normalized = normalize_repository_scope(workspace, repository_scope)
    if normalized["kind"] == "repository":
        return [normalized["repository_id"]]
    if normalized["kind"] == "multi_repository":
        return list(normalized["repository_ids"])
    return [repo["repository_id"] for repo in discover_repositories(workspace)]


def merge_repository_scopes(workspace: Path, scopes: list[dict | None]) -> dict | None:
    normalized_scopes = [
        normalize_repository_scope(workspace, scope)
        for scope in scopes
        if scope is not None
    ]
    if not normalized_scopes:
        return None
    if any(scope["kind"] == "workspace" for scope in normalized_scopes):
        return {"kind": "workspace", "workspace_id": WORKSPACE_SCOPE_ID}
    repository_ids = sorted(
        {
            repository_id
            for scope in normalized_scopes
            for repository_id in repository_ids_for_scope(workspace, scope)
        }
    )
    if not repository_ids:
        return None
    all_repository_ids = [
        repo["repository_id"] for repo in discover_repositories(workspace)
    ]
    if repository_ids == all_repository_ids:
        return {"kind": "workspace", "workspace_id": WORKSPACE_SCOPE_ID}
    if len(repository_ids) == 1:
        return {"kind": "repository", "repository_id": repository_ids[0]}
    return {"kind": "multi_repository", "repository_ids": repository_ids}


def default_repository_scope(workspace: Path, start: Path | None = None) -> dict:
    owner = resolve_repository_for_path(workspace, start or Path.cwd())
    return {"kind": "repository", "repository_id": owner["repository_id"]}


def resolve_repository_for_path(workspace: Path, target: Path) -> dict:
    target_path = target if target.is_absolute() else (workspace / target)
    target_path = target_path.resolve()
    candidates = []
    for repo in discover_repositories(workspace):
        repo_path = (
            workspace.resolve()
            if repo["path"] == "."
            else (workspace / repo["path"]).resolve()
        )
        if target_path == repo_path or repo_path in target_path.parents:
            candidates.append((len(repo_path.parts), repo))
    if not candidates:
        raise SystemExit(
            f"No repository owns path: {relative_to_workspace(target_path, workspace)}"
        )
    candidates.sort(key=lambda item: item[0], reverse=True)
    if len(candidates) > 1 and candidates[0][0] == candidates[1][0]:
        raise SystemExit(
            f"Ambiguous repository ownership for path: {relative_to_workspace(target_path, workspace)}"
        )
    return candidates[0][1]
