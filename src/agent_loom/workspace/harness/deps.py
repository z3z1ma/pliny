from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.guards import harness_root
from agent_loom.workspace.harness.components import components_index_path
from agent_loom.workspace.state import load_workspace
from agent_loom.core.io import read_json


def _neighbors(idx: dict, name: str, key: str) -> List[str]:
    s = (idx.get("components", {}) or {}).get(name) or {}
    raw = s.get(key, []) or []
    if not isinstance(raw, list):
        return []
    out = [str(x) for x in raw if str(x).strip()]
    return sorted(set(out))


def _bfs(idx: dict, start: str, key: str) -> List[str]:
    seen = set([start])
    out: List[str] = []
    q: deque[str] = deque([start])
    while q:
        cur = q.popleft()
        for nxt in _neighbors(idx, cur, key):
            if nxt in seen:
                continue
            seen.add(nxt)
            out.append(nxt)
            q.append(nxt)
    return out


def deps_closure(*, component: str, root: Optional[Path] = None) -> Dict[str, Any]:
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)
    idx_path = components_index_path(ws_root, ws)
    if not idx_path.exists():
        raise WorkspaceError(
            "Missing components/index.json (run `loom workspace harness components refresh-index`)."
        )
    idx = read_json(idx_path)
    if component not in (idx.get("components", {}) or {}):
        raise WorkspaceError(f"Unknown component in index: {component}")

    depends_on = _bfs(idx, component, "depends_on")
    used_by = _bfs(idx, component, "used_by")
    return {
        "component": component,
        "depends_on_transitive": depends_on,
        "used_by_transitive": used_by,
    }


def deps_impacted(*, component: str, root: Optional[Path] = None) -> Dict[str, Any]:
    data = deps_closure(component=component, root=root)
    return {"component": component, "impacted": data.get("used_by_transitive", [])}
