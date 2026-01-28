from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, cast

from agent_loom.workspace.constants import DEFAULT_DEFAULT_BRANCH
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.guards import workspace_root
from agent_loom.workspace.state import load_workspace, save_workspace


def poly_repo_edit(
    *,
    name: str,
    remote: Optional[str] = None,
    default_branch: Optional[str] = None,
    add_tags: Optional[Sequence[str]] = None,
    rm_tags: Optional[Sequence[str]] = None,
    description: Optional[str] = None,
    shallow: Optional[bool] = None,
    depth: Optional[int] = None,
    root: Optional[Path] = None,
) -> Dict[str, Any]:
    ws_root = root.resolve() if root is not None else workspace_root()
    ws = cast(dict[str, Any], load_workspace(ws_root))

    repos_map = ws.get("repos")
    if not isinstance(repos_map, dict) or name not in repos_map:
        raise WorkspaceError(f"Unknown repo: {name}")

    raw_spec = repos_map.get(name)
    spec: dict[str, Any]
    if isinstance(raw_spec, str):
        spec = {"remote": raw_spec, "default_branch": DEFAULT_DEFAULT_BRANCH}
    elif isinstance(raw_spec, dict):
        spec = cast(dict[str, Any], raw_spec)
    else:
        raise WorkspaceError(f"workspace.json: repo '{name}' must be string or object")

    changed: List[str] = []

    if remote is not None:
        spec["remote"] = str(remote)
        changed.append("remote")
    if default_branch is not None:
        spec["default_branch"] = str(default_branch)
        changed.append("default_branch")
    if description is not None:
        spec["description"] = str(description)
        changed.append("description")

    if shallow is not None:
        spec["shallow"] = bool(shallow)
        changed.append("shallow")
        if not shallow:
            spec.pop("depth", None)
        else:
            spec.setdefault("depth", 1)

    if depth is not None:
        spec["depth"] = max(1, int(depth))
        spec["shallow"] = True
        changed.append("depth")

    tags: List[str] = []
    raw_tags = spec.get("tags")
    if isinstance(raw_tags, list):
        tags = [str(t).strip() for t in raw_tags if str(t).strip()]

    if add_tags:
        for tok in add_tags:
            for t in str(tok).split(","):
                tt = t.strip()
                if tt and tt not in tags:
                    tags.append(tt)
        changed.append("tags")

    if rm_tags:
        remove = set()
        for tok in rm_tags:
            for t in str(tok).split(","):
                tt = t.strip()
                if tt:
                    remove.add(tt)
        tags = [t for t in tags if t not in remove]
        changed.append("tags")

    if tags:
        spec["tags"] = tags
    else:
        spec.pop("tags", None)

    repos_map[name] = spec
    ws["repos"] = repos_map
    save_workspace(ws_root, ws)

    return {"repo": name, "changed": sorted(set(changed)), "entry": spec}


def poly_set_upsert(
    *,
    name: str,
    items: Sequence[str],
    root: Optional[Path] = None,
) -> Dict[str, Any]:
    ws_root = root.resolve() if root is not None else workspace_root()
    ws = load_workspace(ws_root)

    set_name = str(name or "").strip()
    if not set_name:
        raise WorkspaceError("Missing set name")

    clean: List[str] = []
    for tok in items:
        t = str(tok).strip()
        if not t:
            continue
        clean.append(t)

    ws.setdefault("repo_sets", {})
    ws["repo_sets"][set_name] = clean
    save_workspace(ws_root, ws)
    return {"set": set_name, "items": clean}


def poly_set_rm(*, name: str, root: Optional[Path] = None) -> Dict[str, Any]:
    ws_root = root.resolve() if root is not None else workspace_root()
    ws = load_workspace(ws_root)
    sets = ws.get("repo_sets", {})
    if not isinstance(sets, dict) or name not in sets:
        raise WorkspaceError(f"Unknown repo set: {name}")
    sets.pop(name, None)
    ws["repo_sets"] = sets
    save_workspace(ws_root, ws)
    return {"set": name, "removed": True}


def poly_set_show(*, name: str, root: Optional[Path] = None) -> Dict[str, Any]:
    ws_root = root.resolve() if root is not None else workspace_root()
    ws = load_workspace(ws_root)
    sets = ws.get("repo_sets", {})
    if not isinstance(sets, dict) or name not in sets:
        raise WorkspaceError(f"Unknown repo set: {name}")
    return {"set": name, "items": sets.get(name)}


def poly_set_ls(*, root: Optional[Path] = None) -> Dict[str, Any]:
    ws_root = root.resolve() if root is not None else workspace_root()
    ws = load_workspace(ws_root)
    sets = ws.get("repo_sets", {})
    if not isinstance(sets, dict):
        sets = {}
    return {"repo_sets": {k: sets[k] for k in sorted(sets.keys())}}
