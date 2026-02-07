from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import List, Optional, Sequence

from agent_loom.core.io import read_json
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.guards import workspace_root
from agent_loom.workspace.models import ImpactResult
from agent_loom.workspace.poly.services import service_index_path
from agent_loom.workspace.state import load_workspace
from agent_loom.workspace.poly.ops import snapshot_diff


def _neighbors(idx: dict, svc: str, key: str) -> List[str]:
    s = (idx.get("services", {}) or {}).get(svc) or {}
    raw = s.get(key, []) or []
    if not isinstance(raw, list):
        return []
    out = [str(x) for x in raw if str(x).strip()]
    return sorted(set(out))


def _bfs_multi(idx: dict, starts: Sequence[str], key: str) -> List[str]:
    q: deque[str] = deque(sorted({str(s) for s in starts if str(s).strip()}))
    seen = set(q)
    out: List[str] = []
    while q:
        cur = q.popleft()
        for nxt in _neighbors(idx, cur, key):
            if nxt in seen:
                continue
            seen.add(nxt)
            out.append(nxt)
            q.append(nxt)
    return out


def _load_services_index(*, ws_root: Path) -> dict:
    ws = load_workspace(ws_root)
    idx_path = service_index_path(ws_root, ws)
    if not idx_path.exists():
        raise WorkspaceError(
            "Missing services/index.json (run `loom workspace harness services refresh-index`)."
        )
    idx = read_json(idx_path)
    if not isinstance(idx, dict):
        raise WorkspaceError("Invalid services index (expected JSON object)")
    return idx


def poly_impact_repos(
    *,
    changed: Sequence[str],
    root: Optional[Path] = None,
    source: Optional[dict] = None,
) -> ImpactResult:
    ws_root = root.resolve() if root is not None else workspace_root()
    idx = _load_services_index(ws_root=ws_root)
    services = idx.get("services", {}) or {}

    changed_list = sorted({str(x).strip() for x in (changed or []) if str(x).strip()})
    unknown = sorted([x for x in changed_list if x not in services])
    known = [x for x in changed_list if x in services]
    impacted = sorted(_bfs_multi(idx, known, "used_by"))
    all_services = sorted({*changed_list, *impacted})

    return ImpactResult(
        source=source or {"kind": "repos"},
        changed=changed_list,
        unknown=unknown,
        impacted=impacted,
        all=all_services,
    )


def poly_impact_snapshot(
    *,
    name: str,
    include_missing: bool = True,
    root: Optional[Path] = None,
) -> ImpactResult:
    ws_root = root.resolve() if root is not None else workspace_root()
    diff = snapshot_diff(name=name, root=ws_root)
    changed: list[str] = []
    for row in diff.diffs:
        st = str((row or {}).get("status") or "")
        repo = str((row or {}).get("repo") or "").strip()
        if not repo:
            continue
        if st == "changed":
            changed.append(repo)
        elif st == "missing" and include_missing:
            changed.append(repo)
        elif st == "snapshot_error":
            changed.append(repo)

    src = {
        "kind": "snapshot",
        "name": str(name),
        "snapshot_path": str(diff.snapshot_path),
        "target": diff.target,
        "summary": diff.summary,
        "include_missing": bool(include_missing),
    }
    return poly_impact_repos(changed=changed, root=ws_root, source=src)
