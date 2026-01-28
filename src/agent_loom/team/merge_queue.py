from __future__ import annotations

import uuid
from typing import Any, Dict, List, Mapping, Optional

from agent_loom.team.errors import TeamError
from agent_loom.team.strings import sanitize
from agent_loom.team.time import _iso_z


def _merge_state(run: Mapping[str, Any]) -> Dict[str, Any]:
    ms = run.get("merge")
    if not isinstance(ms, dict):
        ms = {}
    if not isinstance(ms.get("items"), list):
        ms["items"] = []
    if not isinstance(ms.get("config"), dict):
        ms["config"] = {"target_branch": "main", "remote": "origin", "push": True}
    return ms


def merge_branch_for_run(run: Mapping[str, Any]) -> str:
    """Return the per-run merge-queue branch.

    Rules:
    - If run.merge.branch exists and is in the `team/` namespace, use it.
    - Else derive a stable per-run branch using 4 random bytes from run_id.
    - Fallback to the legacy default if run_id is unavailable.
    """

    ms = _merge_state(run)
    existing = str(ms.get("branch") or "").strip()
    if existing:
        b = sanitize(existing, allow=r"a-zA-Z0-9._/-", max_len=120)
        if b and b.startswith("team/"):
            return b

    run_id = str(run.get("run_id") or "").strip()
    if run_id:
        suffix = sanitize(run_id, allow=r"a-zA-Z0-9", max_len=64)[:8]
        if suffix:
            return f"team/merge-queue-{suffix}"

    return "team/merge-queue"


def merge_enqueue_item(
    run: Dict[str, Any],
    *,
    branch: str,
    ticket_id: str = "",
    from_worker: str = "",
    note: str = "",
) -> Dict[str, Any]:
    ms = _merge_state(run)
    item = {
        "id": uuid.uuid4().hex[:10],
        "enqueued_at": _iso_z(),
        "state": "queued",
        "branch": str(branch or "").strip(),
        "ticket_id": str(ticket_id or "").strip(),
        "from_worker": str(from_worker or "").strip(),
        "note": str(note or "").strip(),
        "claimed_by": "",
        "claimed_at": "",
        "done_at": "",
        "result": "",
        "result_note": "",
    }
    ms["items"] = list(ms.get("items") or []) + [item]
    run["merge"] = ms
    return item


def merge_list_items(
    run: Dict[str, Any], *, include_done: bool = False
) -> List[Dict[str, Any]]:
    ms = _merge_state(run)
    items = [i for i in (ms.get("items") or []) if isinstance(i, dict)]
    if include_done:
        return items
    return [i for i in items if str(i.get("state") or "") in ("queued", "claimed")]


def merge_claim_next(
    run: Dict[str, Any], *, claimed_by: str = ""
) -> Optional[Dict[str, Any]]:
    ms = _merge_state(run)
    items = [i for i in (ms.get("items") or []) if isinstance(i, dict)]
    for item in items:
        if str(item.get("state") or "") == "queued":
            item["state"] = "claimed"
            item["claimed_by"] = str(claimed_by or "").strip()
            item["claimed_at"] = _iso_z()
            run["merge"] = ms
            return item
    return None


def merge_mark_done(
    run: Dict[str, Any],
    *,
    item_id: str,
    result: str,
    note: str = "",
) -> Dict[str, Any]:
    ms = _merge_state(run)
    items = [i for i in (ms.get("items") or []) if isinstance(i, dict)]
    for item in items:
        if str(item.get("id") or "") == str(item_id or ""):
            item["state"] = "done"
            item["done_at"] = _iso_z()
            item["result"] = str(result or "").strip()
            item["result_note"] = str(note or "").strip()
            run["merge"] = ms
            return item
    raise TeamError(f"merge item not found: {item_id}", code="ARG", exit_code=2)


__all__ = [
    "_merge_state",
    "merge_branch_for_run",
    "merge_claim_next",
    "merge_enqueue_item",
    "merge_list_items",
    "merge_mark_done",
]
