from __future__ import annotations

import contextlib
import datetime as dt
import json
import os
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from agent_loom.memory.constants import RE_WORD, SCHEMA_VERSION, SCOPE_KIND_KEY
from agent_loom.memory.frontmatter import (
    canonicalize_rfc3339_utc,
    split_yaml_frontmatter,
)
from agent_loom.memory.errors import MemoryError
from agent_loom.memory.index import (
    connect_db,
    db_init,
    fetch_notes_by_ids,
    graph_expand_with_distances,
    graph_neighbors,
    sync_index,
)
from agent_loom.memory.models import VaultPaths
from agent_loom.memory.scopes import (
    _validate_tags,
    parse_scope_string,
    scope_matches_context,
    tag_filter_exclude,
    tag_filter_match,
    validate_file_scopes_exist,
)
from agent_loom.memory.utils import eprint, now_iso, sha256_text
from agent_loom.memory.vault import git_repo_root


def fts_sanitize_query(q: str) -> str:
    toks = RE_WORD.findall(q)
    if not toks:
        return ""
    return " AND ".join(toks)


def parse_multi_csvish(values: Optional[List[str]]) -> List[str]:
    if not values:
        return []
    out: List[str] = []
    for v in values:
        if v is None:
            continue
        for part in str(v).split(","):
            p = part.strip()
            if p:
                out.append(p)
    return out


def parse_since(since: Optional[str]) -> Optional[str]:
    if not since:
        return None
    s = since.strip()
    if not s:
        return None
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        s = s + "T00:00:00Z"
    return canonicalize_rfc3339_utc(s)


def parse_until(until: Optional[str]) -> Optional[str]:
    if not until:
        return None
    s = until.strip()
    if not s:
        return None
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        # End of day.
        s = s + "T23:59:59Z"
    return canonicalize_rfc3339_utc(s)


def default_visibility_from_env() -> List[str]:
    raw = str(os.environ.get("MEMORY_DEFAULT_VISIBILITY") or "").strip()
    if raw:
        parts = [p.strip().lower() for p in raw.split(",") if p.strip()]
        out = [p for p in parts if p in ("shared", "personal", "ephemeral")]
        return out or ["shared", "personal"]
    return ["shared", "personal"]


def build_safe_fts_query(q: str, *, or_mode: bool) -> str:
    toks = [t for t in RE_WORD.findall(q or "") if t]
    if not toks:
        return ""
    # Prefix matching makes recall tolerant to partial tokens.
    joined = (" OR " if or_mode else " AND ").join([f"{t}*" for t in toks])
    return joined


def parse_context_scopes(
    scope_args: List[str], *, repo_root: Optional[Path]
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for it in scope_args:
        it = it.strip()
        if not it:
            continue
        parsed = parse_scope_string(it, repo_root=repo_root)
        if parsed is not None:
            out.append(parsed)
    return out


def compute_recency_boost(updated_at: str) -> Tuple[float, Optional[float]]:
    try:
        t = canonicalize_rfc3339_utc(updated_at)
        txt = t.replace("Z", "+00:00") if t.endswith("Z") else t
        d = dt.datetime.fromisoformat(txt)
        if d.tzinfo is None:
            d = d.replace(tzinfo=dt.timezone.utc)
        age = dt.datetime.now(dt.timezone.utc) - d.astimezone(dt.timezone.utc)
        age_days = age.total_seconds() / 86400.0
        boost = max(0.0, 30.0 - age_days) / 30.0 * 5.0
        return boost, age_days
    except Exception:
        return 0.0, None


def print_index_warnings(warnings: List[Dict[str, Any]], *, limit: int = 6) -> None:
    if not warnings:
        return
    eprint(f"[memory] index warnings: {len(warnings)}")
    for w in warnings[:limit]:
        t = w.get("type")
        if t == "invalid_note":
            eprint(f"[memory] - invalid_note: {w.get('path')}")
        elif t == "duplicate_id":
            eprint(
                f"[memory] - duplicate_id: {w.get('id')} kept={w.get('kept')} skipped={w.get('skipped')}"
            )
        elif t == "note_warning":
            ws = w.get("warnings") or []
            eprint(
                f"[memory] - note_warning: {w.get('id')} {w.get('path')} ({len(ws)} warning(s))"
            )
            for msg in ws[:2]:
                eprint(f"[memory]   - {msg}")
        else:
            eprint(
                f"[memory] - {t}: {json.dumps(w, ensure_ascii=False, sort_keys=True)}"
            )


def recall_notes(
    vp: VaultPaths,
    *,
    query: str,
    limit: int,
    tags: List[str],
    not_tags: List[str],
    ctx_scopes: List[Dict[str, Any]],
    not_ctx_scopes: List[Dict[str, Any]],
    visibility: List[str],
    include_deprecated: bool,
    since: Optional[str],
    until: Optional[str],
    and_mode: bool,
    scoped_only: bool,
    include_body: bool,
    max_body_chars: int,
    expand: int,
    deterministic: bool,
    quiet: bool,
    or_mode: bool,
    fts_raw: bool,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    q = (query or "").strip()
    if limit <= 0:
        return ([], [])

    if not q and not tags and not ctx_scopes:
        return ([], [])

    since_s = parse_since(since)
    until_s = parse_until(until)

    with connect_db(vp) as conn:
        sync_res = sync_index(vp, conn, quiet=quiet)
        warnings = list(sync_res.get("warnings") or [])

        where = ["1=1"]
        params: List[Any] = []

        if visibility:
            where.append("n.visibility IN (" + ",".join(["?"] * len(visibility)) + ")")
            params.extend(visibility)

        if not include_deprecated:
            where.append("n.status != 'deprecated'")

        if since_s:
            where.append("n.updated_at >= ?")
            params.append(since_s)

        if until_s:
            where.append("n.updated_at <= ?")
            params.append(until_s)

        rows: List[sqlite3.Row] = []
        used_fts = False

        if q:
            cand_limit = max(200, limit * 50)
            safe_q = q if fts_raw else build_safe_fts_query(q, or_mode=bool(or_mode))
            if not safe_q:
                safe_q = fts_sanitize_query(q)
            sql = (
                "SELECT n.*, bm25(notes_fts) AS bm25, "
                "snippet(notes_fts, 2, '[', ']', '…', 12) AS snippet "
                "FROM notes_fts JOIN notes n ON n.id = notes_fts.id "
                "WHERE notes_fts MATCH ? AND "
                + " AND ".join(where)
                + " ORDER BY bm25 ASC, n.updated_at DESC, n.id ASC LIMIT ?;"
            )
            try:
                rows = conn.execute(sql, [safe_q, *params, cand_limit]).fetchall()
                used_fts = True
            except sqlite3.OperationalError:
                # Fallback: drop to a sanitized AND-join.
                sq2 = fts_sanitize_query(q)
                if sq2:
                    with contextlib.suppress(sqlite3.OperationalError):
                        rows = conn.execute(sql, [sq2, *params, cand_limit]).fetchall()
                        used_fts = True

        if not q or not used_fts:
            sql = (
                "SELECT n.*, NULL AS bm25, NULL AS snippet FROM notes n WHERE "
                + " AND ".join(where)
            )
            sql += " ORDER BY n.updated_at DESC, n.id ASC LIMIT ?;"
            rows = conn.execute(sql, [*params, max(500, limit * 50)]).fetchall()

        out: List[Dict[str, Any]] = []

        for r in rows:
            note_tags = json.loads(r["tags_json"] or "[]")
            note_scopes = json.loads(r["scopes_json"] or "[]")
            note_aliases = json.loads(r["aliases_json"] or "[]")

            ok_tags, matched_tags = tag_filter_match(
                note_tags, want=tags, and_mode=and_mode
            )
            if not ok_tags:
                continue
            ex, excluded_tags = tag_filter_exclude(note_tags, not_tags=not_tags)
            if ex:
                continue

            scope_score, matched_scopes = scope_matches_context(
                note_scopes,
                ctx_scopes=ctx_scopes,
                and_mode=and_mode,
            )

            if ctx_scopes:
                if scoped_only and scope_score <= 0:
                    continue
            if not_ctx_scopes:
                neg_score, neg_matches = scope_matches_context(
                    note_scopes, ctx_scopes=not_ctx_scopes, and_mode=False
                )
                if neg_score > 0:
                    continue
            else:
                neg_matches = []

            bm25 = r["bm25"]
            snippet = r["snippet"]
            fts_score = 0.0
            if bm25 is not None:
                try:
                    fts_score = -float(bm25)
                except Exception:
                    fts_score = 0.0
            elif q:
                toks = [t.lower() for t in RE_WORD.findall(q.lower())]
                title_l = (r["title"] or "").lower()
                preview_l = (r["preview"] or "").lower()
                lex = 0.0
                for t in toks:
                    lex += 10.0 * title_l.count(t)
                    lex += 1.0 * preview_l.count(t)
                fts_score = lex

            scope_boost = float(scope_score)

            if deterministic:
                rec_boost, age_days = 0.0, None
            else:
                rec_boost, age_days = compute_recency_boost(r["updated_at"] or "")

            final = fts_score + scope_boost + rec_boost

            item: Dict[str, Any] = {
                "id": r["id"],
                "title": r["title"],
                "path": r["md_path"],
                "visibility": r["visibility"],
                "status": r["status"],
                "tags": note_tags,
                "aliases": note_aliases,
                "scopes": note_scopes,
                "created_at": r["created_at"],
                "updated_at": r["updated_at"],
                "preview": r["preview"],
                "score": {
                    "final": final,
                    "fts": fts_score,
                    "bm25": float(bm25) if bm25 is not None else None,
                    "scope": scope_score,
                    "recency": rec_boost,
                },
                "why": {
                    "matched_tags": matched_tags,
                    "excluded_tags": excluded_tags,
                    "matched_scopes": matched_scopes[:20],
                    "excluded_scopes": neg_matches[:20],
                    "fts_snippet": snippet,
                    "recency_age_days": age_days,
                },
                "role": "hit",
            }

            if include_body:
                p = vp.root / r["md_path"]
                body = ""
                if p.exists():
                    with contextlib.suppress(Exception):
                        _, body = split_yaml_frontmatter(
                            p.read_text("utf-8", errors="replace")
                        )
                if max_body_chars and len(body) > max_body_chars:
                    body = body[: max(0, max_body_chars - 3)] + "..."
                item["body"] = body

            out.append(item)

        out.sort(key=lambda x: str(x.get("id") or ""))
        out.sort(key=lambda x: str(x.get("updated_at") or ""), reverse=True)
        out.sort(key=lambda x: float(x["score"]["final"]), reverse=True)

        hits = out[:limit]

        if expand and expand > 0 and hits:
            hit_ids = [h["id"] for h in hits]
            dist = graph_expand_with_distances(conn, hit_ids, k=expand)
            neighbor_ids = [i for i, d in dist.items() if d and i not in set(hit_ids)]
            neighbor_ids.sort()
            if neighbor_ids:
                neighbors = fetch_notes_by_ids(conn, neighbor_ids)
                for n in neighbors:
                    n["role"] = "neighbor"
                    n["why"] = {
                        "via": hit_ids,
                        "graph_distance": int(dist.get(n["id"], 0) or 0),
                    }
                neighbors.sort(key=lambda x: str(x.get("id") or ""))
                neighbors.sort(
                    key=lambda x: str(x.get("updated_at") or ""), reverse=True
                )
                hits = hits + neighbors

        if include_body and expand and hits:
            want_ids = [x["id"] for x in hits if "body" not in x]
            if want_ids:
                by_id = {x["id"]: x for x in hits}
                rows2 = conn.execute(
                    "SELECT id, md_path FROM notes WHERE id IN ("
                    + ",".join(["?"] * len(want_ids))
                    + ");",
                    want_ids,
                ).fetchall()
                for rr in rows2:
                    nid = rr["id"]
                    p = vp.root / rr["md_path"]
                    body = ""
                    if p.exists():
                        with contextlib.suppress(Exception):
                            _, body = split_yaml_frontmatter(
                                p.read_text("utf-8", errors="replace")
                            )
                    if max_body_chars and len(body) > max_body_chars:
                        body = body[: max(0, max_body_chars - 3)] + "..."
                    by_id[nid]["body"] = body

    return (hits, warnings)


def list_notes(
    vp: VaultPaths,
    *,
    limit: int,
    tags: List[str],
    not_tags: List[str],
    ctx_scopes: List[Dict[str, Any]],
    not_ctx_scopes: List[Dict[str, Any]],
    visibility: List[str],
    include_deprecated: bool,
    since: Optional[str],
    until: Optional[str],
    and_mode: bool,
    scoped_only: bool,
    deterministic: bool,
    quiet: bool,
    sort: str,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    if limit <= 0:
        return ([], [])

    since_s = parse_since(since)
    until_s = parse_until(until)
    sort_key = (sort or "updated").strip().lower()
    if sort_key not in ("updated", "created"):
        sort_key = "updated"
    order_col = "n.updated_at" if sort_key == "updated" else "n.created_at"

    with connect_db(vp) as conn:
        sync_res = sync_index(vp, conn, quiet=quiet)
        warnings = list(sync_res.get("warnings") or [])

        where = ["1=1"]
        params: List[Any] = []

        if visibility:
            where.append("n.visibility IN (" + ",".join(["?"] * len(visibility)) + ")")
            params.extend(visibility)

        if not include_deprecated:
            where.append("n.status != 'deprecated'")

        if since_s:
            where.append("n.updated_at >= ?")
            params.append(since_s)
        if until_s:
            where.append("n.updated_at <= ?")
            params.append(until_s)

        # Pull a wider candidate set because tag/scope filters happen in Python.
        cand_limit = max(500, limit * 50)
        sql = (
            "SELECT n.*, NULL AS bm25, NULL AS snippet FROM notes n WHERE "
            + " AND ".join(where)
            + f" ORDER BY {order_col} DESC, n.id ASC LIMIT ?;"
        )
        rows = conn.execute(sql, [*params, cand_limit]).fetchall()

        out: List[Dict[str, Any]] = []
        for r in rows:
            note_tags = json.loads(r["tags_json"] or "[]")
            note_scopes = json.loads(r["scopes_json"] or "[]")
            note_aliases = json.loads(r["aliases_json"] or "[]")

            ok_tags, matched_tags = tag_filter_match(
                note_tags, want=tags, and_mode=and_mode
            )
            if not ok_tags:
                continue
            ex, excluded_tags = tag_filter_exclude(note_tags, not_tags=not_tags)
            if ex:
                continue

            scope_score, matched_scopes = scope_matches_context(
                note_scopes,
                ctx_scopes=ctx_scopes,
                and_mode=and_mode,
            )
            if ctx_scopes:
                if scoped_only and scope_score <= 0:
                    continue
            if not_ctx_scopes:
                neg_score, neg_matches = scope_matches_context(
                    note_scopes, ctx_scopes=not_ctx_scopes, and_mode=False
                )
                if neg_score > 0:
                    continue
            else:
                neg_matches = []

            if deterministic:
                rec_boost, age_days = 0.0, None
            else:
                rec_boost, age_days = compute_recency_boost(r["updated_at"] or "")

            final = float(scope_score) + float(rec_boost)

            out.append(
                {
                    "id": r["id"],
                    "title": r["title"],
                    "path": r["md_path"],
                    "visibility": r["visibility"],
                    "status": r["status"],
                    "tags": note_tags,
                    "aliases": note_aliases,
                    "scopes": note_scopes,
                    "created_at": r["created_at"],
                    "updated_at": r["updated_at"],
                    "preview": r["preview"],
                    "score": {
                        "final": final,
                        "fts": 0.0,
                        "bm25": None,
                        "scope": scope_score,
                        "recency": rec_boost,
                    },
                    "why": {
                        "matched_tags": matched_tags,
                        "excluded_tags": excluded_tags,
                        "matched_scopes": matched_scopes[:20],
                        "excluded_scopes": neg_matches[:20],
                        "fts_snippet": None,
                        "recency_age_days": age_days,
                    },
                    "role": "hit",
                }
            )

        return (out[:limit], warnings)


def _parse_rfc3339_utc(s: str) -> Optional[dt.datetime]:
    try:
        t = canonicalize_rfc3339_utc(s)
        txt = t.replace("Z", "+00:00") if t.endswith("Z") else t
        d = dt.datetime.fromisoformat(txt)
        if d.tzinfo is None:
            d = d.replace(tzinfo=dt.timezone.utc)
        return d.astimezone(dt.timezone.utc)
    except Exception:
        return None


def around_notes(
    vp: VaultPaths,
    *,
    note_id: str,
    k: int,
    by: str,
    window_days: int,
    visibility: List[str],
    include_deprecated: bool,
    quiet: bool,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    if k <= 0:
        return ([], [])
    by_key = (by or "updated").strip().lower()
    if by_key not in ("updated", "created"):
        by_key = "updated"
    col = "updated_at" if by_key == "updated" else "created_at"

    with connect_db(vp) as conn:
        sync_res = sync_index(vp, conn, quiet=quiet)
        warnings = list(sync_res.get("warnings") or [])

        row = conn.execute(
            f"SELECT id, title, {col} AS ts FROM notes WHERE id=?;", (note_id,)
        ).fetchone()
        if not row:
            raise MemoryError(
                f"Note not found: {note_id}",
                code="NOT_FOUND",
                exit_code=2,
                hint="Pick an existing note id.",
                suggestions=[f"loom memory recall {note_id!r}"],
            )

        base_ts = _parse_rfc3339_utc(str(row["ts"] or ""))
        if base_ts is None:
            return ([], warnings)

        wd = int(window_days)
        if wd <= 0:
            wd = 1
        start = (base_ts - dt.timedelta(days=wd)).isoformat().replace("+00:00", "Z")
        end = (base_ts + dt.timedelta(days=wd)).isoformat().replace("+00:00", "Z")

        where = ["1=1"]
        params: List[Any] = []
        if visibility:
            where.append("visibility IN (" + ",".join(["?"] * len(visibility)) + ")")
            params.extend(visibility)
        if not include_deprecated:
            where.append("status != 'deprecated'")
        where.append(f"{col} >= ?")
        where.append(f"{col} <= ?")
        params.extend([start, end])

        cand = conn.execute(
            f"SELECT id, title, md_path, visibility, status, tags_json, aliases_json, scopes_json, created_at, updated_at, preview, {col} AS ts FROM notes WHERE "
            + " AND ".join(where)
            + " ORDER BY "
            + col
            + " DESC, id ASC LIMIT ?;",
            (*params, max(400, k * 80)),
        ).fetchall()

        items: List[Tuple[float, Dict[str, Any]]] = []
        for r in cand:
            if str(r["id"] or "") == note_id:
                continue
            ts = _parse_rfc3339_utc(str(r["ts"] or ""))
            if ts is None:
                continue
            delta_days = abs((ts - base_ts).total_seconds()) / 86400.0
            items.append(
                (
                    delta_days,
                    {
                        "id": r["id"],
                        "title": r["title"],
                        "path": r["md_path"],
                        "visibility": r["visibility"],
                        "status": r["status"],
                        "tags": json.loads(r["tags_json"] or "[]"),
                        "aliases": json.loads(r["aliases_json"] or "[]"),
                        "scopes": json.loads(r["scopes_json"] or "[]"),
                        "created_at": r["created_at"],
                        "updated_at": r["updated_at"],
                        "preview": r["preview"],
                        "why": {"temporal_delta_days": delta_days, "by": by_key},
                        "role": "temporal",
                    },
                )
            )

        items.sort(key=lambda x: x[0])
        return ([d for _delta, d in items[:k]], warnings)


def timeline(
    vp: VaultPaths,
    *,
    days: int,
    by: str,
    visibility: List[str],
    include_deprecated: bool,
    quiet: bool,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    by_key = (by or "updated").strip().lower()
    if by_key not in ("updated", "created"):
        by_key = "updated"
    col = "updated_at" if by_key == "updated" else "created_at"
    d = int(days)
    if d <= 0:
        d = 1
    since_ts = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=d)).replace(
        microsecond=0
    )
    since_s = since_ts.isoformat().replace("+00:00", "Z")

    with connect_db(vp) as conn:
        sync_res = sync_index(vp, conn, quiet=quiet)
        warnings = list(sync_res.get("warnings") or [])

        where = ["1=1"]
        params: List[Any] = []
        if visibility:
            where.append("visibility IN (" + ",".join(["?"] * len(visibility)) + ")")
            params.extend(visibility)
        if not include_deprecated:
            where.append("status != 'deprecated'")
        where.append(f"{col} >= ?")
        params.append(since_s)

        rows = conn.execute(
            f"SELECT id, title, {col} AS ts FROM notes WHERE "
            + " AND ".join(where)
            + f" ORDER BY {col} DESC, id ASC LIMIT 5000;",
            params,
        ).fetchall()

        buckets: Dict[str, Dict[str, Any]] = {}
        for r in rows:
            ts = str(r["ts"] or "")
            day = ts[:10] if len(ts) >= 10 else ""
            if not day:
                continue
            b = buckets.get(day)
            if b is None:
                b = {"day": day, "count": 0, "sample": []}
                buckets[day] = b
            b["count"] = int(b["count"]) + 1
            if len(b["sample"]) < 5:
                b["sample"].append({"id": r["id"], "title": r["title"]})

        days_sorted = sorted(buckets.keys(), reverse=True)
        out = [buckets[d] for d in days_sorted]
        return (out, warnings)


def grep_notes(
    vp: VaultPaths,
    *,
    pattern: str,
    limit: int,
    tags: List[str],
    not_tags: List[str],
    ctx_scopes: List[Dict[str, Any]],
    not_ctx_scopes: List[Dict[str, Any]],
    visibility: List[str],
    include_deprecated: bool,
    since: Optional[str],
    until: Optional[str],
    and_mode: bool,
    scoped_only: bool,
    quiet: bool,
    ignore_case: bool,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    pat = str(pattern or "").strip()
    if not pat:
        raise MemoryError(
            "grep pattern is required",
            code="ARG",
            exit_code=2,
            hint="Provide a Python regex pattern.",
            suggestions=["loom memory grep <regex>"],
        )
    if limit <= 0:
        return ([], [])

    flags = re.MULTILINE
    if ignore_case:
        flags |= re.IGNORECASE
    try:
        rx = re.compile(pat, flags=flags)
    except re.error as e:
        raise MemoryError(
            f"invalid regex: {e}",
            code="ARG",
            exit_code=2,
            hint="Fix the regex or escape special characters.",
        ) from e

    since_s = parse_since(since)
    until_s = parse_until(until)

    with connect_db(vp) as conn:
        sync_res = sync_index(vp, conn, quiet=quiet)
        warnings = list(sync_res.get("warnings") or [])

        where = ["1=1"]
        params: List[Any] = []

        if visibility:
            where.append("visibility IN (" + ",".join(["?"] * len(visibility)) + ")")
            params.extend(visibility)

        if not include_deprecated:
            where.append("status != 'deprecated'")

        if since_s:
            where.append("updated_at >= ?")
            params.append(since_s)
        if until_s:
            where.append("updated_at <= ?")
            params.append(until_s)

        cand_limit = 5000
        rows = conn.execute(
            "SELECT id, title, md_path, visibility, status, tags_json, aliases_json, scopes_json, created_at, updated_at "
            "FROM notes WHERE "
            + " AND ".join(where)
            + " ORDER BY updated_at DESC, id ASC LIMIT ?;",
            (*params, cand_limit),
        ).fetchall()

        hits: List[Dict[str, Any]] = []
        for r in rows:
            note_tags = json.loads(r["tags_json"] or "[]")
            note_scopes = json.loads(r["scopes_json"] or "[]")

            ok_tags, matched_tags = tag_filter_match(
                note_tags, want=tags, and_mode=and_mode
            )
            if not ok_tags:
                continue
            ex, excluded_tags = tag_filter_exclude(note_tags, not_tags=not_tags)
            if ex:
                continue

            scope_score, matched_scopes = scope_matches_context(
                note_scopes,
                ctx_scopes=ctx_scopes,
                and_mode=and_mode,
            )
            if ctx_scopes:
                if scoped_only and scope_score <= 0:
                    continue
            if not_ctx_scopes:
                neg_score, neg_matches = scope_matches_context(
                    note_scopes, ctx_scopes=not_ctx_scopes, and_mode=False
                )
                if neg_score > 0:
                    continue
            else:
                neg_matches = []

            p = vp.root / str(r["md_path"] or "")
            if not p.exists():
                continue

            raw = p.read_text("utf-8", errors="replace")
            _fm, body = split_yaml_frontmatter(raw)

            title = str(r["title"] or "")
            text = title + "\n" + (body or "")
            m = rx.search(text)
            if not m:
                continue

            # Find a stable snippet and (approx) line number.
            loc = "title" if rx.search(title or "") else "body"
            line_no = None
            line = ""
            if loc == "title":
                line_no = 1
                line = title.strip()
            else:
                # The match might be in the title segment; guard.
                if m.start() <= len(title):
                    line_no = 1
                    line = title.strip()
                else:
                    idx_in_body = max(0, m.start() - (len(title) + 1))
                    pre = (body or "")[:idx_in_body]
                    line_no = pre.count("\n") + 1
                    body_lines = (body or "").splitlines()
                    if 1 <= line_no <= len(body_lines):
                        line = body_lines[line_no - 1].strip()
            if len(line) > 240:
                line = line[:237] + "..."

            match_count = 0
            with contextlib.suppress(Exception):
                match_count = sum(1 for _ in rx.finditer(text))

            hits.append(
                {
                    "id": r["id"],
                    "title": title,
                    "path": r["md_path"],
                    "visibility": r["visibility"],
                    "status": r["status"],
                    "created_at": r["created_at"],
                    "updated_at": r["updated_at"],
                    "match_count": int(match_count),
                    "match": {
                        "pattern": pat,
                        "ignore_case": bool(ignore_case),
                        "location": loc,
                        "line_no": int(line_no) if line_no is not None else None,
                        "line": line,
                    },
                    "why": {
                        "matched_tags": matched_tags,
                        "excluded_tags": excluded_tags,
                        "matched_scopes": matched_scopes[:20],
                        "excluded_scopes": neg_matches[:20],
                    },
                }
            )

            if len(hits) >= int(limit):
                break

        return (hits, warnings)


def suggest_links(
    vp: VaultPaths,
    *,
    note_id: str,
    limit: int,
    visibility: List[str],
    include_deprecated: bool,
    quiet: bool,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    nid = str(note_id or "").strip()
    if not nid:
        raise MemoryError(
            "note id is required",
            code="ARG",
            exit_code=2,
            hint="Provide a note id.",
            suggestions=["loom memory link suggest <id>"],
        )
    if limit <= 0:
        return ([], [])

    with connect_db(vp) as conn:
        sync_res = sync_index(vp, conn, quiet=quiet)
        warnings = list(sync_res.get("warnings") or [])

        row = conn.execute(
            "SELECT id, title, md_path, tags_json, scopes_json, preview, updated_at, visibility, status FROM notes WHERE id=?;",
            (nid,),
        ).fetchone()
        if not row:
            raise MemoryError(
                f"Note not found: {nid}",
                code="NOT_FOUND",
                exit_code=2,
                hint="Pick an existing note id.",
                suggestions=[f"loom memory recall {nid!r}"],
            )

        src_tags = [str(x).strip() for x in json.loads(row["tags_json"] or "[]")]
        src_scopes = json.loads(row["scopes_json"] or "[]")
        src_title = str(row["title"] or "")
        src_preview = str(row["preview"] or "")

        src_tag_set = {t.casefold(): t for t in src_tags if t}

        def scope_sig(s: Any) -> str:
            try:
                if not isinstance(s, dict):
                    return ""
                k = str(s.get("kind") or "").strip()
                if not k:
                    return ""
                key = SCOPE_KIND_KEY.get(k)
                if not key:
                    return ""
                v = s.get(key)
                if not isinstance(v, str) or not v.strip():
                    return ""
                return json.dumps(
                    {"kind": k, key: v.strip()}, sort_keys=True, ensure_ascii=False
                )
            except Exception:
                return ""

        src_scope_sigs = {scope_sig(s) for s in src_scopes}
        src_scope_sigs.discard("")

        src_cmds = []
        for s in src_scopes:
            if isinstance(s, dict) and s.get("kind") == "command":
                c = s.get("command")
                if isinstance(c, str) and c.strip():
                    src_cmds.append(c.strip().casefold())

        src_tokens = {
            t.casefold()
            for t in RE_WORD.findall((src_title + " " + src_preview).strip())
            if len(t) >= 3 and not t.isdigit()
        }

        where = ["id != ?"]
        params: List[Any] = [nid]
        if visibility:
            where.append("visibility IN (" + ",".join(["?"] * len(visibility)) + ")")
            params.extend(visibility)
        if not include_deprecated:
            where.append("status != 'deprecated'")

        cand = conn.execute(
            "SELECT id, title, md_path, tags_json, scopes_json, preview, updated_at "
            "FROM notes WHERE "
            + " AND ".join(where)
            + " ORDER BY updated_at DESC, id ASC LIMIT 4000;",
            params,
        ).fetchall()

        scored: List[Tuple[float, Dict[str, Any]]] = []
        for r in cand:
            cid = str(r["id"] or "")
            ctitle = str(r["title"] or "")
            ctags = [str(x).strip() for x in json.loads(r["tags_json"] or "[]")]
            cscopes = json.loads(r["scopes_json"] or "[]")
            cpreview = str(r["preview"] or "")

            matched_tags: List[str] = []
            ctag_norm = {t.casefold(): t for t in ctags if t}
            for tn, orig in src_tag_set.items():
                if tn in ctag_norm:
                    matched_tags.append(orig)

            c_scope_sigs = {scope_sig(s) for s in cscopes}
            c_scope_sigs.discard("")
            matched_scopes = list(sorted(src_scope_sigs & c_scope_sigs))

            cmd_bonus = 0.0
            if src_cmds:
                for s in cscopes:
                    if isinstance(s, dict) and s.get("kind") == "command":
                        c = s.get("command")
                        if (
                            isinstance(c, str)
                            and c.strip()
                            and c.strip().casefold() in set(src_cmds)
                        ):
                            cmd_bonus = 25.0
                            break

            ctokens = {
                t.casefold()
                for t in RE_WORD.findall((ctitle + " " + cpreview).strip())
                if len(t) >= 3 and not t.isdigit()
            }
            token_overlap = len(src_tokens & ctokens)

            rec_boost, _age_days = compute_recency_boost(str(r["updated_at"] or ""))

            score = (
                10.0 * float(len(matched_tags))
                + 5.0 * float(len(matched_scopes))
                + 2.0 * float(token_overlap)
                + cmd_bonus
                + 0.5 * float(rec_boost)
            )
            if score <= 0.0:
                continue

            scored.append(
                (
                    score,
                    {
                        "id": cid,
                        "title": ctitle,
                        "path": str(r["md_path"] or ""),
                        "updated_at": str(r["updated_at"] or ""),
                        "score": score,
                        "why": {
                            "matched_tags": sorted(set(matched_tags)),
                            "matched_scopes": matched_scopes[:20],
                            "token_overlap": int(token_overlap),
                            "command_overlap": bool(cmd_bonus > 0),
                        },
                    },
                )
            )

        scored.sort(key=lambda x: str(x[1].get("id") or ""))
        scored.sort(key=lambda x: str(x[1].get("updated_at") or ""), reverse=True)
        scored.sort(key=lambda x: float(x[0]), reverse=True)
        return ([d for _s, d in scored[: int(limit)]], warnings)


def format_scope_short(scopes: Any) -> str:
    if not isinstance(scopes, list):
        return ""
    parts: List[str] = []
    for s in scopes:
        if not isinstance(s, dict):
            continue
        kind = s.get("kind")
        if not isinstance(kind, str) or kind not in SCOPE_KIND_KEY:
            continue
        key = SCOPE_KIND_KEY[kind]
        val = s.get(key)
        if isinstance(kind, str) and isinstance(val, str) and val.strip():
            parts.append(f"{kind}:{val.strip()}")
    return ", ".join(parts)


def render_context_pack(
    vp: VaultPaths,
    *,
    query: str,
    limit: int,
    tags: List[str],
    not_tags: List[str],
    ctx_scopes: List[Dict[str, Any]],
    not_ctx_scopes: List[Dict[str, Any]],
    visibility: List[str],
    include_deprecated: bool,
    since: Optional[str],
    until: Optional[str],
    and_mode: bool,
    scoped_only: bool,
    expand: int,
    max_chars: int,
    max_body_chars: int,
    deterministic: bool,
    quiet: bool,
    or_mode: bool,
    fts_raw: bool,
) -> Tuple[str, List[Dict[str, Any]]]:
    hits, warnings = recall_notes(
        vp,
        query=query,
        limit=limit,
        tags=tags,
        not_tags=not_tags,
        ctx_scopes=ctx_scopes,
        not_ctx_scopes=not_ctx_scopes,
        visibility=visibility,
        include_deprecated=include_deprecated,
        since=since,
        until=until,
        and_mode=and_mode,
        scoped_only=scoped_only,
        include_body=True,
        max_body_chars=max_body_chars,
        expand=int(expand or 0),
        deterministic=deterministic,
        quiet=quiet,
        or_mode=bool(or_mode),
        fts_raw=bool(fts_raw),
    )

    if not hits:
        return ("", warnings)

    with connect_db(vp) as conn:
        db_init(conn)

        ordered = list(hits)

        seen_hashes: Dict[str, str] = {}

        lines: List[str] = []

        vault_str = str(vp.root)
        rr = git_repo_root(Path.cwd())
        if rr is not None:
            with contextlib.suppress(Exception):
                vault_str = vp.root.relative_to(rr).as_posix()
        header = {
            "schema_version": SCHEMA_VERSION,
            "vault": vault_str,
            "query": query,
            "limit": limit,
            "expand": expand,
            "filters": {
                "tags": tags,
                "not_tags": not_tags,
                "scopes": ctx_scopes,
                "not_scopes": not_ctx_scopes,
                "visibility": visibility,
                "include_deprecated": include_deprecated,
                "since": parse_since(since),
                "and_mode": and_mode,
                "scoped_only": scoped_only,
            },
        }
        if not deterministic:
            header["generated_at"] = now_iso()
        lines.append(
            "<!-- memory: "
            + json.dumps(header, ensure_ascii=False, sort_keys=True)
            + " -->"
        )
        lines.append("# Memory Context Pack")
        if query:
            lines.append(f"Query: {query}")
        if tags:
            lines.append(f"Tags: {', '.join(tags)}")
        if ctx_scopes:
            scope_parts: List[str] = []
            for s in ctx_scopes:
                if not isinstance(s, dict):
                    continue
                kind = s.get("kind")
                if not isinstance(kind, str) or kind not in SCOPE_KIND_KEY:
                    continue
                key = SCOPE_KIND_KEY[kind]
                val = s.get(key)
                if isinstance(val, str) and val.strip():
                    scope_parts.append(f"{kind}:{val.strip()}")
            if scope_parts:
                lines.append("Scopes: " + ", ".join(scope_parts))
        lines.append("")

        for n in ordered:
            nid = n["id"]
            title = (n.get("title") or "").strip()
            vis = n.get("visibility") or ""
            status = n.get("status") or ""
            updated_at = n.get("updated_at") or ""
            tags_s = ", ".join(n.get("tags") or [])
            scopes_s = format_scope_short(n.get("scopes") or [])
            body = n.get("body") or ""

            ch = sha256_text(body)
            if body and ch in seen_hashes:
                body = f"(deduped: same content as {seen_hashes[ch]})\n"
            elif body:
                seen_hashes[ch] = nid

            nb = graph_neighbors(conn, nid)
            out_links = " ".join([f"[[{x}]]" for x in nb["outbound"][:20]])
            in_links = " ".join([f"[[{x}]]" for x in nb["inbound"][:20]])

            section: List[str] = []
            section.append(f"## {title}  (`{nid}`)")
            section.append(f"- updated_at: {updated_at}")
            section.append(f"- visibility: {vis} | status: {status}")
            gd = None
            if isinstance(n.get("why"), dict):
                gd = n["why"].get("graph_distance")
            if isinstance(gd, int) and gd > 0:
                section.append(f"- graph_distance: {gd}")
            if tags_s:
                section.append(f"- tags: {tags_s}")
            if scopes_s:
                section.append(f"- scopes: {scopes_s}")
            if out_links:
                section.append(f"- outbound: {out_links}")
            if in_links:
                section.append(f"- inbound: {in_links}")
            section.append("")
            if body:
                section.append(body.rstrip())
                section.append("")
            section.append("---")
            section.append("")

            candidate = "\n".join(lines + section)
            if max_chars and len(candidate) > max_chars:
                break
            lines.extend(section)

        return ("\n".join(lines).rstrip() + "\n", warnings)


def recall(
    vp: VaultPaths,
    *,
    query: str = "",
    limit: int = 8,
    tag: Optional[List[str]] = None,
    not_tag: Optional[List[str]] = None,
    scope: Optional[List[str]] = None,
    not_scope: Optional[List[str]] = None,
    command: str = "",
    visibility: Optional[List[str]] = None,
    include_deprecated: bool = False,
    since: Optional[str] = None,
    until: Optional[str] = None,
    and_mode: bool = False,
    scoped_only: bool = False,
    full: bool = False,
    max_body_chars: Optional[int] = None,
    expand: int = 0,
    max_chars: int = 12000,
    context: bool = False,
    deterministic: bool = False,
    quiet: bool = False,
    allow_missing_scopes: bool = False,
    format: str = "json",
    or_mode: bool = False,
    fts_raw: bool = False,
) -> Tuple[Any, List[Dict[str, Any]]]:
    cwd = Path.cwd()
    repo_root = git_repo_root(cwd)

    tags = _validate_tags(parse_multi_csvish(tag))
    not_tags = _validate_tags(parse_multi_csvish(not_tag))

    scope_args = parse_multi_csvish(scope)
    if command:
        scope_args.append(f"command:{command}")
    ctx_scopes = parse_context_scopes(scope_args, repo_root=repo_root)
    validate_file_scopes_exist(
        ctx_scopes,
        repo_root=repo_root,
        cwd=cwd,
        allow_missing=bool(allow_missing_scopes),
    )

    not_scope_args = parse_multi_csvish(not_scope)
    not_ctx_scopes = (
        parse_context_scopes(not_scope_args, repo_root=repo_root)
        if not_scope_args
        else []
    )

    visibility = visibility or default_visibility_from_env()

    if context:
        if format in ("json", "jsonl"):
            raise MemoryError(
                "recall --context requires --format text|md|prompt",
                code="ARG",
                exit_code=2,
                hint="Context packs are rendered as text-like output, not JSON.",
                suggestions=[
                    "loom memory recall <query> --context --format text",
                    "loom memory recall <query> --context --format md",
                    "loom memory recall <query> --context --format prompt",
                ],
            )
        if not (query or "").strip() and not (tags or ctx_scopes):
            raise MemoryError(
                "recall --context requires a query or context (--tag/--scope/--command)",
                code="ARG",
                exit_code=2,
                hint="Provide a query string or at least one tag/scope/command context.",
                suggestions=[
                    "loom memory recall 'query' --context",
                    "loom memory recall --tag foo --context",
                    "loom memory recall --scope file:src/app.py --context",
                    "loom memory recall --command 'pytest' --context",
                ],
            )

        max_body_chars_ctx = int(max_body_chars) if max_body_chars is not None else 4000
        return render_context_pack(
            vp,
            query=query or "",
            limit=int(limit),
            tags=tags,
            not_tags=not_tags,
            ctx_scopes=ctx_scopes,
            not_ctx_scopes=not_ctx_scopes,
            visibility=visibility,
            include_deprecated=bool(include_deprecated),
            since=since,
            until=until,
            and_mode=bool(and_mode),
            scoped_only=bool(scoped_only),
            expand=int(expand or 0),
            max_chars=int(max_chars),
            max_body_chars=max_body_chars_ctx,
            deterministic=bool(deterministic),
            quiet=bool(quiet),
            or_mode=bool(or_mode),
            fts_raw=bool(fts_raw),
        )

    if not (query or "").strip() and not (tags or ctx_scopes):
        return list_notes(
            vp,
            limit=int(limit),
            tags=tags,
            not_tags=not_tags,
            ctx_scopes=ctx_scopes,
            not_ctx_scopes=not_ctx_scopes,
            visibility=visibility,
            include_deprecated=bool(include_deprecated),
            since=since,
            until=until,
            and_mode=bool(and_mode),
            scoped_only=bool(scoped_only),
            deterministic=bool(deterministic),
            quiet=bool(quiet),
            sort="updated",
        )

    max_body_chars_items = int(max_body_chars) if max_body_chars is not None else 800
    return recall_notes(
        vp,
        query=query or "",
        limit=int(limit),
        tags=tags,
        not_tags=not_tags,
        ctx_scopes=ctx_scopes,
        not_ctx_scopes=not_ctx_scopes,
        visibility=visibility,
        include_deprecated=bool(include_deprecated),
        since=since,
        until=until,
        and_mode=bool(and_mode),
        scoped_only=bool(scoped_only),
        include_body=bool(full),
        max_body_chars=max_body_chars_items,
        expand=int(expand or 0),
        deterministic=bool(deterministic),
        quiet=bool(quiet),
        or_mode=bool(or_mode),
        fts_raw=bool(fts_raw),
    )


__all__ = [
    "recall",
    "list_notes",
    "around_notes",
    "timeline",
    "grep_notes",
    "suggest_links",
    "compute_recency_boost",
    "default_visibility_from_env",
    "build_safe_fts_query",
    "fts_sanitize_query",
    "parse_context_scopes",
    "parse_multi_csvish",
    "parse_since",
    "parse_until",
    "print_index_warnings",
    "recall_notes",
    "render_context_pack",
]
