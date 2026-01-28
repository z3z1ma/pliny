from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.guards import workspace_root
from agent_loom.workspace.services import service_index_path
from agent_loom.workspace.state import load_workspace
from agent_loom.workspace.utils import read_json


def _neighbors(idx: dict, svc: str, key: str) -> List[str]:
    s = (idx.get("services", {}) or {}).get(svc) or {}
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


def deps_closure(*, service: str, root: Optional[Path] = None) -> Dict[str, Any]:
    ws_root = root.resolve() if root is not None else workspace_root()
    ws = load_workspace(ws_root)
    idx_path = service_index_path(ws_root, ws)
    if not idx_path.exists():
        raise WorkspaceError(
            "Missing services/index.json (run `loom workspace poly services refresh-index`)."
        )
    idx = read_json(idx_path)
    if service not in (idx.get("services", {}) or {}):
        raise WorkspaceError(f"Unknown service in index: {service}")

    depends_on = _bfs(idx, service, "depends_on")
    used_by = _bfs(idx, service, "used_by")
    return {
        "service": service,
        "depends_on_transitive": depends_on,
        "used_by_transitive": used_by,
    }


def deps_impacted(*, service: str, root: Optional[Path] = None) -> Dict[str, Any]:
    data = deps_closure(service=service, root=root)
    return {"service": service, "impacted": data.get("used_by_transitive", [])}
