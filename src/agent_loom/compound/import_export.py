from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from agent_loom.compound.instincts import Instinct, load_instincts, save_instincts
from agent_loom.core.time import now_iso_precise


@dataclass(frozen=True)
class InstinctExportResult:
    ok: bool
    out: str
    exported: int


@dataclass(frozen=True)
class InstinctImportResult:
    ok: bool
    source: str
    dry_run: bool
    imported: int
    updated: int
    skipped: int


def _slug(text: str) -> str:
    value = str(text or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "general"


def _instinct_to_dict(inst: Instinct) -> dict[str, Any]:
    return {
        "id": str(inst.id),
        "title": str(inst.title),
        "trigger": str(inst.trigger),
        "action": str(inst.action),
        "domain": str(inst.domain),
        "source": str(inst.source),
        "tags": [str(t) for t in list(inst.tags or [])],
        "confidence": float(inst.confidence or 0.0),
        "status": str(inst.status),
        "notes": str(inst.notes or ""),
        "created_at": str(inst.created_at or ""),
        "updated_at": str(inst.updated_at or ""),
        "evidence": list(inst.evidence or []),
    }


def export_instincts(
    *,
    instincts_file: Path,
    out_file: Path,
    min_confidence: float = 0.0,
    domain: str = "",
) -> InstinctExportResult:
    store = load_instincts(instincts_file)
    dom = _slug(domain) if str(domain or "").strip() else ""

    selected = [
        inst
        for inst in list(store.instincts or [])
        if float(inst.confidence or 0.0) >= float(min_confidence)
        and (not dom or _slug(inst.domain) == dom)
    ]
    selected.sort(key=lambda x: x.id)

    payload = {
        "version": 1,
        "generated_at": now_iso_precise(),
        "instincts": [_instinct_to_dict(i) for i in selected],
    }

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    return InstinctExportResult(ok=True, out=str(out_file), exported=len(selected))


def _load_source_text(source: str) -> str:
    src = str(source or "").strip()
    parsed = urlparse(src)
    if parsed.scheme in {"http", "https"}:
        req = Request(src, headers={"User-Agent": "loom-compound"})
        with urlopen(req, timeout=20) as resp:
            return resp.read().decode("utf-8", errors="replace")

    p = Path(src).expanduser().resolve()
    return p.read_text(encoding="utf-8", errors="replace")


def _parse_import_payload(source_text: str) -> list[dict[str, Any]]:
    parsed = json.loads(source_text)
    if isinstance(parsed, dict):
        instincts = parsed.get("instincts")
        if isinstance(instincts, list):
            return [x for x in instincts if isinstance(x, dict)]
        return []
    if isinstance(parsed, list):
        return [x for x in parsed if isinstance(x, dict)]
    return []


def instinct_import(
    *,
    instincts_file: Path,
    source: str,
    dry_run: bool = False,
    force: bool = False,
    min_confidence: float = 0.0,
) -> InstinctImportResult:
    source_text = _load_source_text(source)
    source_sha = hashlib.sha256(source_text.encode("utf-8")).hexdigest()[:16]
    source_id = f"import-{source_sha}"
    source_ts = now_iso_precise()

    incoming = _parse_import_payload(source_text)
    store = load_instincts(instincts_file)
    by_id = {i.id: i for i in store.instincts}

    imported = 0
    updated = 0
    skipped = 0

    for raw in incoming:
        instinct_id = _slug(str(raw.get("id") or ""))
        if not instinct_id:
            skipped += 1
            continue

        confidence = float(raw.get("confidence") or 0.0)
        if confidence < float(min_confidence):
            skipped += 1
            continue

        tags = [_slug(str(t)) for t in list(raw.get("tags") or []) if str(t).strip()]
        domain = (
            _slug(str(raw.get("domain") or ""))
            if str(raw.get("domain") or "").strip()
            else (tags[0] if tags else "general")
        )
        notes = str(raw.get("notes") or "").strip() or None

        existing = by_id.get(instinct_id)
        if existing is None:
            inst = Instinct(
                id=instinct_id,
                title=str(raw.get("title") or "").strip(),
                trigger=str(raw.get("trigger") or "").strip(),
                action=str(raw.get("action") or "").strip(),
                tags=tags,
                confidence=max(0.0, min(1.0, confidence)),
                status="active",
                domain=domain,
                source="inherited",
                notes=notes,
                created_at=str(raw.get("created_at") or source_ts),
                updated_at=source_ts,
                evidence=[
                    {
                        "ts": source_ts,
                        "source_id": source_id,
                        "source_hash": source_sha,
                    }
                ],
            )
            store.instincts.append(inst)
            by_id[inst.id] = inst
            imported += 1
            continue

        should_update = bool(force) or float(confidence) > float(
            existing.confidence or 0.0
        )
        if not should_update:
            skipped += 1
            continue

        existing.title = str(raw.get("title") or existing.title).strip()
        existing.trigger = str(raw.get("trigger") or existing.trigger).strip()
        existing.action = str(raw.get("action") or existing.action).strip()
        existing.tags = tags or list(existing.tags)
        existing.confidence = max(0.0, min(1.0, confidence))
        existing.domain = domain
        existing.source = "inherited"
        existing.notes = notes if notes is not None else existing.notes
        existing.updated_at = source_ts
        existing.evidence.append(
            {
                "ts": source_ts,
                "source_id": source_id,
                "source_hash": source_sha,
            }
        )
        updated += 1

    store.instincts.sort(key=lambda x: x.id)
    if not dry_run:
        save_instincts(instincts_file, store)

    return InstinctImportResult(
        ok=True,
        source=str(source),
        dry_run=bool(dry_run),
        imported=int(imported),
        updated=int(updated),
        skipped=int(skipped),
    )
