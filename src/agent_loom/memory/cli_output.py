from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any

from agent_loom.memory.models import (
    AddResult,
    EditResult,
    JanitorFixResult,
    JanitorReportResult,
    LinkBacklinksResult,
    LinkGraphResult,
    LinkNeighborsResult,
    LinkSuggestResult,
    LinkValidateResult,
    PrimeResult,
    RecallResult,
)
from agent_loom.memory.utils import format_json

def emit(payload: Any, fmt: str) -> None:
    if fmt == "json":
        print(format_json(payload))
        return
    if fmt == "jsonl":
        if isinstance(payload, list):
            for it in payload:
                print(json.dumps(it, ensure_ascii=False, sort_keys=True))
        else:
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return
    if isinstance(payload, str):
        print(payload)
        return
    print(format_json(payload))


def render_link_validate(rows: list[dict[str, Any]], *, fmt: str) -> str:
    if fmt == "md":
        lines = []
        for r in rows:
            lines.append(
                f"- {r.get('src_id')} -> {r.get('dst_raw')} ({r.get('resolution')}, {r.get('style')})"
            )
        return "\n".join(lines).rstrip() + "\n"
    if fmt == "prompt":
        lines = ["Broken/ambiguous memo links:", ""]
        for r in rows:
            lines.append(
                f"- {r.get('src_id')} -> {r.get('dst_raw')} ({r.get('resolution')}, {r.get('style')})"
            )
        return "\n".join(lines).rstrip() + "\n"

    lines2: list[str] = []
    for r in rows:
        lines2.append(
            f"{r.get('src_id')}\t{r.get('dst_raw')}\t{r.get('resolution')}\t{r.get('style')}"
        )
    return "\n".join(lines2).rstrip() + "\n"


def render_recall_results(results: list[dict[str, Any]], *, fmt: str) -> str:
    if fmt == "md":
        lines: list[str] = []
        for r in results:
            nid = r.get("id")
            title = (r.get("title") or "").strip()
            preview = (r.get("preview") or "").strip()
            lines.append(f"- [[{nid}]] {title} - {preview}")
        return "\n".join(lines).rstrip() + "\n"
    if fmt == "prompt":
        lines = ["Relevant memory notes:", ""]
        for r in results:
            title = (r.get("title") or "").strip()
            snippet = None
            why = r.get("why")
            if isinstance(why, dict):
                snippet = (why.get("fts_snippet") or "").strip() or None
            preview = (r.get("preview") or "").strip()
            lines.append(f"- {title} (`{r.get('id')}`)")
            lines.append(f"  {snippet or preview}")
        return "\n".join(lines).rstrip() + "\n"

    lines2: list[str] = []
    for r in results:
        nid = r.get("id")
        title = (r.get("title") or "").strip()
        updated_at = (r.get("updated_at") or "").strip()
        preview = (r.get("preview") or "").strip()
        lines2.append(f"{nid}\t{updated_at}\t{title}\t{preview}")
    return "\n".join(lines2).rstrip() + "\n"


def render_mutation_result(result: dict[str, Any], *, fmt: str) -> str:
    rid = str(result.get("id") or "")
    path = str(result.get("path") or "")
    action = "updated" if bool(result.get("updated")) else "created"
    lines = [f"Memory note {action}: {rid}"]
    if path:
        lines.append(f"path: {path}")

    hs = result.get("hydration_summary") or {}
    if isinstance(hs, dict):
        rewrites = int(hs.get("rewrites") or 0)
        created = int(hs.get("created_notes") or 0)
        seeded = int(hs.get("seeded_notes") or 0)
        ambiguous = int(hs.get("ambiguous") or 0)
        lines.append(
            "hydration: "
            f"rewrites={rewrites} created={created} seeded={seeded} ambiguous={ambiguous}"
        )

    actions = result.get("next_actions") or []
    if isinstance(actions, list) and actions:
        lines.append("next:")
        for item in actions[:5]:
            s = str(item or "").strip()
            if s:
                lines.append(f"- {s}")

    if fmt == "md":
        if len(lines) > 1 and lines[1].startswith("path: "):
            lines[1] = f"- {lines[1]}"
        out: list[str] = [f"- {lines[0]}"]
        for ln in lines[1:]:
            out.append(ln if ln.startswith("-") else f"- {ln}")
        return "\n".join(out).rstrip() + "\n"

    if fmt == "prompt":
        return "\n".join(lines).rstrip() + "\n"

    return "\n".join(lines).rstrip() + "\n"


def payload_for(obj: Any, *, fmt: str) -> Any:
    if isinstance(obj, (AddResult, EditResult)):
        payload = asdict(obj)
        if fmt in ("text", "md", "prompt"):
            return render_mutation_result(payload, fmt=fmt)
        return payload
    if isinstance(obj, PrimeResult):
        if fmt in ("json", "jsonl"):
            return obj.payload
        text = str(obj.payload.get("markdown") or "")
        if text:
            return text.rstrip() + "\n"
        return ""
    if isinstance(obj, RecallResult):
        if obj.context_text:
            return obj.context_text
        items = [asdict(it) for it in obj.items]
        if fmt in ("text", "md", "prompt"):
            return render_recall_results(items, fmt=fmt)
        return items
    if isinstance(obj, LinkValidateResult):
        rows = [asdict(r) for r in obj.rows]
        if fmt in ("text", "md", "prompt"):
            return render_link_validate(rows, fmt=fmt)
        return rows
    if isinstance(obj, LinkBacklinksResult):
        return [asdict(b) for b in obj.backlinks]
    if isinstance(obj, LinkGraphResult):
        return [asdict(e) for e in obj.edges]
    if isinstance(obj, LinkNeighborsResult):
        if obj.nodes is not None:
            return {"id": obj.id, "k": obj.k, "nodes": obj.nodes}
        if obj.neighbors is not None:
            return obj.neighbors
        return {}
    if isinstance(obj, LinkSuggestResult):
        items = [asdict(it) for it in obj.suggestions]
        if fmt == "md":
            lines = [
                f"- [[{it['id']}]] ({it.get('score')}) {it.get('title')}"
                for it in items
            ]
            return "\n".join(lines).rstrip() + "\n" if lines else ""
        if fmt == "prompt":
            lines = ["Suggested related notes:", ""]
            for it in items:
                lines.append(f"- [[{it['id']}]] ({it.get('score')}) {it.get('title')}")
            return "\n".join(lines).rstrip() + "\n" if items else ""
        if fmt == "text":
            lines2: list[str] = []
            for it in items:
                lines2.append(
                    f"{it.get('id')}\t{it.get('score')}\t{it.get('updated_at')}\t{(it.get('title') or '').strip()}"
                )
            return "\n".join(lines2).rstrip() + "\n" if items else ""
        return items
    if isinstance(obj, (JanitorReportResult, JanitorFixResult)):
        return asdict(obj)
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    return obj
