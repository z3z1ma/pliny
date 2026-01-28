from __future__ import annotations

import contextlib
import json
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple

from agent_loom.memory.constants import (
    DB_SCHEMA_VERSION,
    MDLINK_RE,
    RE_NOTE_ID,
    WIKILINK_RE,
)
from agent_loom.memory.utils import safe_mkdir, strip_fenced_code_blocks
from agent_loom.memory.vault import (
    Note,
    VaultPaths,
    git_repo_root,
    iter_note_paths,
    normalize_preview,
    note_content_hash,
    note_rel_path,
    try_read_note_from_path,
)


def sqlite_has_fts5(conn: sqlite3.Connection) -> bool:
    try:
        conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS __fts5_test USING fts5(x);")
        conn.execute("DROP TABLE IF EXISTS __fts5_test;")
        return True
    except sqlite3.OperationalError:
        return False


@contextlib.contextmanager
def connect_db(vp: VaultPaths) -> Iterator[sqlite3.Connection]:
    safe_mkdir(vp.root)

    def _open() -> sqlite3.Connection:
        c = sqlite3.connect(str(vp.db_path))
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA journal_mode=WAL;")
        c.execute("PRAGMA foreign_keys=ON;")
        return c

    conn = _open()

    try:
        uv_row = conn.execute("PRAGMA user_version;").fetchone()
        uv = int((uv_row[0] if uv_row else 0) or 0)
    except Exception:
        uv = 0
    if uv not in (0, DB_SCHEMA_VERSION):
        conn.close()
        delete_db_files(vp)
        conn = _open()

    try:
        yield conn
    finally:
        with contextlib.suppress(Exception):
            conn.close()


def delete_db_files(vp: VaultPaths) -> None:
    for p in [
        vp.db_path,
        vp.db_path.with_name(vp.db_path.name + "-wal"),
        vp.db_path.with_name(vp.db_path.name + "-shm"),
    ]:
        if p.exists():
            with contextlib.suppress(Exception):
                p.unlink()


def db_init(conn: sqlite3.Connection) -> Dict[str, Any]:
    with contextlib.suppress(Exception):
        conn.execute(f"PRAGMA user_version={DB_SCHEMA_VERSION};")

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
          id TEXT PRIMARY KEY,
          title TEXT NOT NULL,
          aliases_json TEXT NOT NULL DEFAULT '[]',
          tags_json TEXT NOT NULL DEFAULT '[]',
          scopes_json TEXT NOT NULL DEFAULT '[]',
          visibility TEXT NOT NULL DEFAULT 'shared',
          status TEXT NOT NULL DEFAULT 'active',
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          content_hash TEXT NOT NULL,
          preview TEXT NOT NULL,
          md_path TEXT NOT NULL,
          frontmatter_json TEXT NOT NULL DEFAULT '{}'
        );
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS note_names (
          name TEXT NOT NULL,
          name_norm TEXT NOT NULL,
          id TEXT NOT NULL,
          kind TEXT NOT NULL,
          PRIMARY KEY (name_norm, id, kind)
        );
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_note_names_norm ON note_names(name_norm);"
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS links (
          src_id TEXT NOT NULL,
          dst_raw TEXT NOT NULL,
          dst_norm TEXT NOT NULL,
          dst_id TEXT,
          resolution TEXT NOT NULL DEFAULT 'missing',
          style TEXT NOT NULL,
          alias_text TEXT NOT NULL DEFAULT '',
          anchor TEXT NOT NULL DEFAULT '',
          PRIMARY KEY (src_id, dst_norm, style, alias_text, anchor)
        );
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_links_src ON links(src_id);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_links_dst ON links(dst_id);")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_links_resolution ON links(resolution);"
    )

    fts_ok = sqlite_has_fts5(conn)
    if fts_ok:
        conn.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
              id UNINDEXED,
              title,
              body,
              tags,
              tokenize='unicode61 remove_diacritics 2 tokenchars _'
            );
            """
        )

    conn.commit()
    return {"fts5": fts_ok}


def db_upsert_note_fts(
    conn: sqlite3.Connection, note_id: str, title: str, body: str, tags: List[str]
) -> None:
    try:
        conn.execute("DELETE FROM notes_fts WHERE id=?;", (note_id,))
        conn.execute(
            "INSERT INTO notes_fts (id, title, body, tags) VALUES (?, ?, ?, ?);",
            (note_id, title or "", body or "", ",".join(tags or [])),
        )
    except sqlite3.OperationalError:
        return


def db_delete_note_fts(conn: sqlite3.Connection, note_id: str) -> None:
    try:
        conn.execute("DELETE FROM notes_fts WHERE id=?;", (note_id,))
    except sqlite3.OperationalError:
        return


def normalize_name_key(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip()).casefold()


def rebuild_note_names(conn: sqlite3.Connection, note: Note) -> None:
    conn.execute("DELETE FROM note_names WHERE id=?;", (note.id,))
    rows: List[Tuple[str, str, str, str]] = []

    def add(kind: str, name: str) -> None:
        nm = (name or "").strip()
        if not nm:
            return
        rows.append((nm, normalize_name_key(nm), note.id, kind))

    add("id", note.id)
    add("title", note.title)
    for a in note.aliases or []:
        add("alias", a)

    conn.executemany(
        "INSERT OR IGNORE INTO note_names(name, name_norm, id, kind) VALUES (?, ?, ?, ?);",
        rows,
    )


def parse_wikilinks(body: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for m in WIKILINK_RE.finditer(body or ""):
        inner = (m.group(1) or "").strip()
        if not inner:
            continue
        target, alias = inner, None
        if "|" in inner:
            target, alias = inner.split("|", 1)
            target = target.strip()
            alias = (alias or "").strip() or None
        anchor = None
        if "#" in target:
            target, anchor = target.split("#", 1)
            target = target.strip()
            anchor = (anchor or "").strip() or None
        if not target:
            continue
        out.append(
            {
                "style": "wikilink",
                "target_raw": target,
                "target_norm": normalize_name_key(target),
                "alias_text": alias,
                "anchor": anchor,
            }
        )
    return out


def _extract_target_from_md_url(url: str) -> Optional[str]:
    u = (url or "").strip().strip("<>").strip()
    if not u:
        return None
    if (u.startswith('"') and u.endswith('"')) or (
        u.startswith("'") and u.endswith("'")
    ):
        u = u[1:-1].strip()

    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", u):
        return None

    u = u.split("#", 1)[0].split("?", 1)[0]

    m = re.match(r"^(memory|note|id):(.+)$", u, flags=re.IGNORECASE)
    if m:
        return (m.group(2) or "").strip() or None

    if u.lower().endswith(".md"):
        base = u.replace("\\", "/").rstrip("/")
        name = base.split("/")[-1]
        stem = name[:-3]
        return stem.strip() or None

    return u.strip() or None


def parse_mdlinks(body: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for m in MDLINK_RE.finditer(body or ""):
        url = m.group(1) or ""
        t = _extract_target_from_md_url(url)
        if not t:
            continue
        out.append(
            {
                "style": "mdlink",
                "target_raw": t,
                "target_norm": normalize_name_key(t),
                "alias_text": None,
                "anchor": None,
            }
        )
    return out


def parse_outbound_links(note: Note) -> List[Dict[str, Any]]:
    edges: List[Dict[str, Any]] = []
    body_for_links = strip_fenced_code_blocks(note.body)
    for e in parse_wikilinks(body_for_links):
        edges.append(e)
    for e in parse_mdlinks(body_for_links):
        edges.append(e)
    for t in note.links_frontmatter or []:
        edges.append(
            {
                "style": "frontmatter",
                "target_raw": t,
                "target_norm": normalize_name_key(t),
                "alias_text": None,
                "anchor": None,
            }
        )
    seen = set()
    out: List[Dict[str, Any]] = []
    for e in edges:
        sig = (
            e.get("style"),
            e.get("target_norm"),
            e.get("alias_text") or "",
            e.get("anchor") or "",
        )
        if sig in seen:
            continue
        seen.add(sig)
        out.append(e)
    return out


def _candidate_id_from_link_raw(dst_raw: str) -> Optional[str]:
    dr = (dst_raw or "").strip()
    if not dr:
        return None
    if "/" in dr or dr.lower().endswith(".md"):
        base = dr.replace("\\", "/").rstrip("/").split("/")[-1]
        if base.lower().endswith(".md"):
            base = base[:-3]
        if base and RE_NOTE_ID.match(base):
            return base
    if RE_NOTE_ID.match(dr):
        return dr
    return None


def compute_link_diagnostics(vp: VaultPaths, src_id: str) -> Dict[str, Any]:
    with connect_db(vp) as conn:
        sync_index(vp, conn, quiet=True)

        rows = conn.execute(
            """
            SELECT dst_raw, dst_id, resolution, style, alias_text, anchor
            FROM links
            WHERE src_id=?
            ORDER BY dst_raw ASC, style ASC, alias_text ASC, anchor ASC;
            """,
            (src_id,),
        ).fetchall()

        edges: List[Dict[str, Any]] = []
        counts = {"resolved": 0, "missing": 0, "ambiguous": 0, "total": 0}
        missing_candidate_ids: List[str] = []

        for r in rows:
            counts["total"] += 1
            res = r["resolution"]
            if res in counts:
                counts[res] += 1

            dst_id = r["dst_id"]
            inbound_count = None
            outbound_count = None
            if isinstance(dst_id, str) and dst_id:
                inbound_count = conn.execute(
                    "SELECT COUNT(DISTINCT src_id) AS c FROM links WHERE dst_id=? AND resolution='resolved';",
                    (dst_id,),
                ).fetchone()[0]
                outbound_count = conn.execute(
                    "SELECT COUNT(DISTINCT dst_id) AS c FROM links WHERE src_id=? AND resolution='resolved' AND dst_id IS NOT NULL;",
                    (dst_id,),
                ).fetchone()[0]

            candidate_id = None
            if res != "resolved":
                candidate_id = _candidate_id_from_link_raw(str(r["dst_raw"] or ""))
                if candidate_id:
                    missing_candidate_ids.append(candidate_id)

            edges.append(
                {
                    "src_id": src_id,
                    "dst_raw": r["dst_raw"],
                    "dst_id": dst_id,
                    "resolution": res,
                    "style": r["style"],
                    "alias_text": r["alias_text"],
                    "anchor": r["anchor"],
                    "candidate_id": candidate_id,
                    "inbound_count": inbound_count,
                    "outbound_count": outbound_count,
                }
            )

        missing_candidate_ids = sorted(set([x for x in missing_candidate_ids if x]))

        return {
            "summary": {
                "outbound_total": counts["total"],
                "resolved": counts["resolved"],
                "missing": counts["missing"],
                "ambiguous": counts["ambiguous"],
                "missing_candidate_ids": missing_candidate_ids,
            },
            "edges": edges,
        }


def resolve_links(conn: sqlite3.Connection) -> None:
    id_rows = conn.execute("SELECT id FROM notes;").fetchall()
    id_exact = {r["id"] for r in id_rows}

    name_rows = conn.execute("SELECT name_norm, id FROM note_names;").fetchall()
    mapping: Dict[str, List[str]] = {}
    for r in name_rows:
        nn = r["name_norm"]
        i = r["id"]
        mapping.setdefault(nn, []).append(i)
    for k in list(mapping.keys()):
        mapping[k] = sorted(set(mapping[k]))

    link_rows = conn.execute(
        "SELECT src_id, dst_raw, dst_norm, style, alias_text, anchor FROM links;"
    ).fetchall()
    updates: List[Tuple[Optional[str], str, str, str, str, str, str]] = []
    for r in link_rows:
        dst_raw = r["dst_raw"]
        dst_norm = r["dst_norm"]
        resolved_id: Optional[str] = None
        resolution = "missing"

        candidate_id = None
        try:
            dr = (dst_raw or "").strip()
            if "/" in dr or dr.lower().endswith(".md"):
                base = dr.replace("\\", "/").rstrip("/").split("/")[-1]
                if base.lower().endswith(".md"):
                    base = base[:-3]
                if base and RE_NOTE_ID.match(base):
                    candidate_id = base
        except Exception:
            candidate_id = None

        if dst_raw in id_exact:
            resolved_id = dst_raw
            resolution = "resolved"
        elif candidate_id is not None and candidate_id in id_exact:
            resolved_id = candidate_id
            resolution = "resolved"
        else:
            ids = mapping.get(dst_norm) or []
            if len(ids) == 1:
                resolved_id = ids[0]
                resolution = "resolved"
            elif len(ids) > 1:
                resolved_id = None
                resolution = "ambiguous"
            else:
                resolved_id = None
                resolution = "missing"

        updates.append(
            (
                resolved_id,
                resolution,
                r["src_id"],
                dst_norm,
                r["style"],
                r["alias_text"] or "",
                r["anchor"] or "",
            )
        )

    conn.executemany(
        """
        UPDATE links
        SET dst_id=?, resolution=?
        WHERE src_id=? AND dst_norm=? AND style=? AND alias_text=? AND anchor=?;
        """,
        updates,
    )


def sync_index(
    vp: VaultPaths, conn: sqlite3.Connection, *, quiet: bool = False
) -> Dict[str, Any]:
    db_init(conn)

    repo_root = git_repo_root(Path.cwd())

    existing_rows = conn.execute(
        "SELECT id, content_hash, md_path FROM notes;"
    ).fetchall()
    existing: Dict[str, Tuple[str, str]] = {
        r["id"]: (r["content_hash"], r["md_path"]) for r in existing_rows
    }

    note_paths = iter_note_paths(vp)
    seen: set[str] = set()
    updated = 0
    skipped = 0
    warnings_out: List[Dict[str, Any]] = []

    id_to_path: Dict[str, str] = {}

    for p, default_vis in note_paths:
        note_id = p.stem
        if note_id in id_to_path:
            skipped += 1
            if not quiet:
                warnings_out.append(
                    {
                        "type": "duplicate_id",
                        "id": note_id,
                        "kept": id_to_path[note_id],
                        "skipped": note_rel_path(vp, p),
                    }
                )
            continue
        id_to_path[note_id] = note_rel_path(vp, p)

        note, warns = try_read_note_from_path(
            p, default_visibility=default_vis, repo_root=repo_root
        )
        if note is None:
            skipped += 1
            if not quiet:
                warnings_out.append(
                    {
                        "type": "invalid_note",
                        "path": note_rel_path(vp, p),
                        "warnings": warns,
                    }
                )
            continue

        if warns and not quiet:
            warnings_out.append(
                {
                    "type": "note_warning",
                    "id": note.id,
                    "path": note_rel_path(vp, p),
                    "warnings": warns,
                }
            )

        seen.add(note.id)

        fm = note.frontmatter
        ch = note_content_hash(fm, note.body)
        md_path = note_rel_path(vp, p)

        prev = existing.get(note.id)
        if prev and prev[0] == ch and prev[1] == md_path:
            continue

        conn.execute(
            """
            INSERT INTO notes (
              id, title, aliases_json, tags_json, scopes_json,
              visibility, status, created_at, updated_at,
              content_hash, preview, md_path, frontmatter_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              title=excluded.title,
              aliases_json=excluded.aliases_json,
              tags_json=excluded.tags_json,
              scopes_json=excluded.scopes_json,
              visibility=excluded.visibility,
              status=excluded.status,
              created_at=excluded.created_at,
              updated_at=excluded.updated_at,
              content_hash=excluded.content_hash,
              preview=excluded.preview,
              md_path=excluded.md_path,
              frontmatter_json=excluded.frontmatter_json
            ;
            """,
            (
                note.id,
                note.title,
                json.dumps(note.aliases or [], ensure_ascii=False),
                json.dumps(note.tags or [], ensure_ascii=False),
                json.dumps(note.scopes or [], ensure_ascii=False),
                note.visibility,
                note.status,
                note.created_at,
                note.updated_at,
                ch,
                normalize_preview(note.body),
                md_path,
                json.dumps(fm, ensure_ascii=False),
            ),
        )

        rebuild_note_names(conn, note)

        conn.execute("DELETE FROM links WHERE src_id=?;", (note.id,))
        edges = parse_outbound_links(note)
        conn.executemany(
            """
            INSERT OR REPLACE INTO links (src_id, dst_raw, dst_norm, dst_id, resolution, style, alias_text, anchor)
            VALUES (?, ?, ?, NULL, 'missing', ?, ?, ?);
            """,
            [
                (
                    note.id,
                    e["target_raw"],
                    e["target_norm"],
                    e["style"],
                    e.get("alias_text") or "",
                    e.get("anchor") or "",
                )
                for e in edges
            ],
        )

        db_upsert_note_fts(conn, note.id, note.title, note.body, note.tags)
        updated += 1

    deleted = 0
    for note_id in existing.keys():
        if note_id in seen:
            continue
        conn.execute("DELETE FROM notes WHERE id=?;", (note_id,))
        conn.execute("DELETE FROM note_names WHERE id=?;", (note_id,))
        conn.execute("DELETE FROM links WHERE src_id=?;", (note_id,))
        db_delete_note_fts(conn, note_id)
        deleted += 1

    resolve_links(conn)
    conn.commit()

    return {
        "ok": True,
        "indexed": len(seen),
        "updated": updated,
        "deleted": deleted,
        "skipped": skipped,
        "warnings": warnings_out,
    }


def graph_neighbors(conn: sqlite3.Connection, note_id: str) -> Dict[str, List[str]]:
    out_rows = conn.execute(
        "SELECT dst_id FROM links WHERE src_id=? AND resolution='resolved' AND dst_id IS NOT NULL;",
        (note_id,),
    ).fetchall()
    inbound_rows = conn.execute(
        "SELECT src_id FROM links WHERE dst_id=? AND resolution='resolved';",
        (note_id,),
    ).fetchall()
    out_ids = sorted({r["dst_id"] for r in out_rows if r["dst_id"]})
    in_ids = sorted({r["src_id"] for r in inbound_rows if r["src_id"]})
    return {"outbound": out_ids, "inbound": in_ids}


def graph_expand(conn: sqlite3.Connection, seeds: List[str], *, k: int) -> List[str]:
    seen: set[str] = set(seeds)
    frontier: List[str] = list(seeds)
    for _ in range(k):
        nxt: List[str] = []
        for nid in sorted(frontier):
            nb = graph_neighbors(conn, nid)
            for cand in sorted(set(nb["outbound"] + nb["inbound"])):
                if cand in seen:
                    continue
                seen.add(cand)
                nxt.append(cand)
        frontier = nxt
        if not frontier:
            break
    return sorted(seen)


def graph_expand_with_distances(
    conn: sqlite3.Connection, seeds: List[str], *, k: int
) -> Dict[str, int]:
    dist: Dict[str, int] = {s: 0 for s in seeds}
    frontier: List[str] = sorted(set(seeds))
    for depth in range(1, k + 1):
        nxt: List[str] = []
        for nid in sorted(frontier):
            nb = graph_neighbors(conn, nid)
            for cand in sorted(set(nb["outbound"] + nb["inbound"])):
                if cand in dist:
                    continue
                dist[cand] = depth
                nxt.append(cand)
        frontier = nxt
        if not frontier:
            break
    return dist


def fetch_notes_by_ids(
    conn: sqlite3.Connection, ids: List[str]
) -> List[Dict[str, Any]]:
    if not ids:
        return []
    rows = conn.execute(
        "SELECT id, title, aliases_json, tags_json, scopes_json, visibility, status, created_at, updated_at, preview, md_path FROM notes WHERE id IN ("
        + ",".join(["?"] * len(ids))
        + ");",
        ids,
    ).fetchall()
    out: List[Dict[str, Any]] = []
    for r in rows:
        out.append(
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
            }
        )
    return out


__all__ = [
    "connect_db",
    "compute_link_diagnostics",
    "db_delete_note_fts",
    "db_init",
    "db_upsert_note_fts",
    "delete_db_files",
    "fetch_notes_by_ids",
    "graph_expand",
    "graph_expand_with_distances",
    "graph_neighbors",
    "normalize_name_key",
    "parse_mdlinks",
    "parse_outbound_links",
    "parse_wikilinks",
    "resolve_links",
    "sqlite_has_fts5",
    "sync_index",
]
