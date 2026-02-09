"""
memory.py - Obsidian-for-Agents, CLI-first "notes as memory"

Design constitution highlights (enforced by this script):
- Canonical storage is Markdown on disk (one note = one .md file with YAML frontmatter).
- SQLite is a derived, rebuildable cache (safe, deterministic, lossless reindex).
- Notes have stable identity (frontmatter `id` must match filename stem).
- Merge-friendly files (stable frontmatter field ordering; body is not rewritten unless you ask).

Default vault layout (under --vault, default `.loom/memory/`):
  .loom/memory/
    notes/                     # shared, committed
    personal/notes/            # personal, gitignored
    personal/ephemeral/notes/  # ephemeral scratch, gitignored
    meta.json                  # committed (schema_version, config)
    index.sqlite3              # derived cache, gitignored

CLI (tiny surface area):
  memory init
  memory add
  memory edit <id>
  memory recall
  memory link ...
  memory recall --context
  memory reindex

By default, recall only returns visibility=shared.
"""

from __future__ import annotations

import contextlib
import importlib.resources as resources
import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from agent_loom.memory.constants import (
    DB_FILENAME,
    DEFAULT_VAULT_DIR,
    RE_NOTE_ID,
    SCHEMA_VERSION,
    STATUSES,
    VISIBILITIES,
)
from agent_loom.memory.errors import MemoryError
from agent_loom.memory.frontmatter import (
    dump_yaml_frontmatter,
    split_yaml_frontmatter,
)
from agent_loom.memory.index import (
    compute_link_diagnostics,
    connect_db,
    db_init,
    delete_db_files,
    fetch_notes_by_ids,
    graph_expand,
    graph_neighbors,
    sync_index,
)
from agent_loom.memory.models import (
    AddResult,
    EditResult,
    InitResult,
    JanitorFixResult,
    JanitorNote,
    JanitorReportResult,
    LinkBacklink,
    LinkBacklinksResult,
    LinkGraphEdge,
    LinkGraphResult,
    LinkNeighborsResult,
    LinkSuggestItem,
    LinkSuggestResult,
    LinkValidateResult,
    LinkValidateRow,
    PrimeResult,
    RecallItem,
    RecallResult,
    RecallScore,
    RecallWhy,
    ReindexResult,
    VaultPaths,
)
from agent_loom.memory.recall import around_notes as around_impl
from agent_loom.memory.recall import default_visibility_from_env
from agent_loom.memory.recall import grep_notes as grep_impl
from agent_loom.memory.recall import list_notes as list_impl
from agent_loom.memory.recall import parse_multi_csvish
from agent_loom.memory.recall import recall as recall_impl
from agent_loom.memory.recall import suggest_links as suggest_links_impl
from agent_loom.memory.recall import timeline as timeline_impl
from agent_loom.memory.scopes import (
    _validate_tags,
    normalize_scopes,
    parse_scope_string,
    resolve_scope_path,
    validate_file_scopes_exist,
)
from agent_loom.memory.utils import format_json, now_iso, safe_mkdir
from agent_loom.memory.hydrate import hydrate_wikilinks
from agent_loom.memory.vault import (
    choose_base_dir,
    edit_text_in_editor,
    find_note_path,
    generate_note_id,
    git_repo_root,
    iter_note_paths,
    normalize_note_frontmatter,
    note_rel_path,
    open_in_editor,
    resolve_vault_root,
    rewrite_note_frontmatter,
    try_read_note_from_path,
    vault_paths,
    write_note_file,
)

__all__ = ["add", "edit", "init", "janitor", "link", "prime", "recall", "reindex"]


# -----------------------------
# Init / meta / gitignore safety
# -----------------------------


def load_meta(vp: VaultPaths) -> Dict[str, Any]:
    if not vp.meta_path.exists():
        return {}
    try:
        return json.loads(vp.meta_path.read_text("utf-8"))
    except Exception:
        return {}


def save_meta(vp: VaultPaths, meta: Dict[str, Any]) -> None:
    safe_mkdir(vp.root)
    vp.meta_path.write_text(format_json(meta) + "\n", "utf-8")


def ensure_gitignore_entries(
    gitignore_path: Path, entries: List[str]
) -> Dict[str, Any]:
    existing = ""
    if gitignore_path.exists():
        existing = gitignore_path.read_text("utf-8", errors="replace")
    lines = existing.splitlines()
    have = set(
        [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]
    )

    added: List[str] = []
    for e in entries:
        e = e.strip()
        if not e or e in have:
            continue
        lines.append(e)
        have.add(e)
        added.append(e)

    if added:
        gitignore_path.write_text("\n".join(lines).rstrip() + "\n", "utf-8")

    return {"path": str(gitignore_path), "added": added}


def _vault_paths_for(vault: Optional[str]) -> VaultPaths:
    cwd = Path.cwd()
    vault_root = resolve_vault_root(
        str(vault or os.environ.get("MEMORY_VAULT", DEFAULT_VAULT_DIR)), cwd=cwd
    )
    return vault_paths(vault_root)


def init_vault(vp: VaultPaths) -> Dict[str, Any]:
    safe_mkdir(vp.root)
    safe_mkdir(vp.notes_dir)
    safe_mkdir(vp.personal_notes_dir)
    safe_mkdir(vp.ephemeral_notes_dir)

    # meta.json (committed)
    meta = load_meta(vp)
    if not meta:
        meta = {"schema_version": SCHEMA_VERSION, "created_at": now_iso()}
        save_meta(vp, meta)
    else:
        # Ensure schema_version exists (additive).
        if "schema_version" not in meta:
            meta["schema_version"] = SCHEMA_VERSION
            save_meta(vp, meta)

    # Derived DB (gitignored)
    with connect_db(vp) as conn:
        dbi = db_init(conn)

    # Safety: ignore derived + personal paths.
    # Write a vault-local .gitignore only. This avoids mutating repo-root `.gitignore`
    # as a side effect of `loom memory init`.
    gitignore_results: List[Dict[str, Any]] = []
    gi_path = vp.root / ".gitignore"
    gitignore_results.append(
        ensure_gitignore_entries(
            gi_path,
            [
                f"{DB_FILENAME}*",
                "personal/",
            ],
        )
    )

    return {
        "ok": True,
        "vault": str(vp.root),
        "meta": meta,
        "db": dbi,
        "gitignore": gitignore_results,
    }


def init(*, vault: Optional[str] = None) -> InitResult:
    vp = _vault_paths_for(vault)
    payload = init_vault(vp)
    return InitResult(
        ok=bool(payload.get("ok")),
        vault=str(payload.get("vault") or ""),
        meta=dict(payload.get("meta") or {}),
        db=dict(payload.get("db") or {}),
        gitignore=list(payload.get("gitignore") or []),
    )


def prime() -> PrimeResult:
    try:
        text = (
            resources.files("agent_loom.memory")
            .joinpath("README.md")
            .read_text(encoding="utf-8")
        )
    except FileNotFoundError as exc:
        raise MemoryError(
            "Memory cookbook not found in package data",
            code="NOT_FOUND",
            exit_code=2,
            hint="Reinstall the package or verify README is bundled.",
        ) from exc

    return PrimeResult(
        payload={"ok": True, "schema_version": SCHEMA_VERSION, "markdown": text}
    )


# -----------------------------
# Commands
# -----------------------------


def add(
    *,
    vault: Optional[str] = None,
    title: Optional[str] = None,
    visibility: str = "shared",
    status: str = "active",
    tag: Optional[Sequence[str]] = None,
    alias: Optional[Sequence[str]] = None,
    link: Optional[Sequence[str]] = None,
    related: Optional[Sequence[str]] = None,
    scope: Optional[Sequence[str]] = None,
    command: Optional[str] = None,
    allow_missing_scopes: bool = False,
    body: Optional[str] = None,
    interactive: bool = False,
    note_id: Optional[str] = None,
    folder: str = "",
) -> AddResult:
    vp = _vault_paths_for(vault)
    cwd = Path.cwd()
    init_vault(vp)
    repo_root = git_repo_root(cwd)

    title = (title or "").strip()

    tags = _validate_tags(parse_multi_csvish(list(tag) if tag else None))
    aliases = [
        a.strip()
        for a in parse_multi_csvish(list(alias) if alias else None)
        if a.strip()
    ]

    scope_items = parse_multi_csvish(list(scope) if scope else None)
    if command is not None:
        cmd = str(command).strip()
        if not cmd:
            raise MemoryError(
                "--command cannot be empty",
                code="ARG",
                exit_code=2,
                hint="Provide a non-empty command signature.",
                suggestions=[
                    'loom memory add --title "pytest failure" --command "uv run pytest" --body "..."',
                ],
            )
        scope_items.append(f"command:{cmd}")
    scopes = [parse_scope_string(s, repo_root=repo_root) for s in scope_items]
    if scopes:
        # Dedup by JSON signature for stable frontmatter.
        sigs = {json.dumps(s, sort_keys=True, ensure_ascii=False): s for s in scopes}
        scopes = list(sigs.values())
    validate_file_scopes_exist(
        scopes,
        repo_root=repo_root,
        cwd=cwd,
        allow_missing=bool(allow_missing_scopes),
    )

    body_text = ""
    if body is not None:
        body_text = str(body)
    elif bool(interactive):
        body_text = edit_text_in_editor(initial="")

    related_items = [
        s.strip()
        for s in parse_multi_csvish(list(related) if related else None)
        if s.strip()
    ]
    if related_items:
        rel_line = "Related: " + " ".join([f"[[{x}]]" for x in related_items])
        if body_text.strip():
            body_text = body_text.rstrip() + "\n\n" + rel_line + "\n"
        else:
            body_text = rel_line + "\n"

    if not title:
        # Derive from first non-empty line of body (strip leading markdown heading).
        for ln in (body_text or "").splitlines():
            s = ln.strip()
            if not s:
                continue
            title = s.lstrip("#").strip()
            break
    if not title and not body_text:
        raise MemoryError(
            "No note content provided",
            code="ARG",
            exit_code=2,
            hint="Provide --title, --body, or --interactive (or pipe stdin).",
            suggestions=[
                "loom memory add --title 'Title' --body 'Body'",
                "echo 'Body' | loom memory add --title 'Title'",
            ],
        )

    note_id = (note_id or "").strip() or generate_note_id(title)
    if not RE_NOTE_ID.match(note_id):
        raise MemoryError(
            f"invalid id {note_id!r}",
            code="ARG",
            exit_code=2,
            hint="Use letters/numbers plus _ and -, no spaces.",
        )

    # Ensure uniqueness (scan)
    try:
        _ = find_note_path(vp, note_id)
        raise MemoryError(
            f"note id already exists: {note_id}",
            code="CONFLICT",
            exit_code=2,
            hint="Pick a new id or edit the existing note.",
            suggestions=[
                f"loom memory edit {note_id}",
                "loom memory add --id <new-id>",
            ],
        )
    except MemoryError as e:
        if str(getattr(e, "code", "")) == "NOT_FOUND":
            pass
        else:
            raise

    created_at = now_iso()
    updated_at = created_at

    link_items = [
        s.strip() for s in parse_multi_csvish(list(link) if link else None) if s.strip()
    ]
    fm_extra: Dict[str, Any] = {}
    if link_items:
        fm_extra["links"] = link_items

    hydrated_body, hydration = hydrate_wikilinks(
        vault_root=vp.root,
        body=body_text,
        visibility=visibility,
        created_at=created_at,
        updated_at=updated_at,
    )

    p = write_note_file(
        vp,
        note_id=note_id,
        title=title,
        body=hydrated_body,
        tags=tags,
        aliases=aliases,
        scopes=scopes,
        visibility=visibility,
        status=status,
        created_at=created_at,
        updated_at=updated_at,
        folder=folder or "",
        frontmatter_extra=fm_extra or None,
    )

    links_info = compute_link_diagnostics(vp, note_id)

    return AddResult(
        ok=True,
        id=note_id,
        path=note_rel_path(vp, p),
        visibility=visibility,
        links=links_info,
        hydration=hydration,
    )


def edit(
    *,
    vault: Optional[str] = None,
    note_id: str,
    title: Optional[str] = None,
    visibility: Optional[str] = None,
    status: Optional[str] = None,
    tag: Optional[Sequence[str]] = None,
    remove_tag: Optional[Sequence[str]] = None,
    clear_tags: bool = False,
    alias: Optional[Sequence[str]] = None,
    remove_alias: Optional[Sequence[str]] = None,
    clear_aliases: bool = False,
    link: Optional[Sequence[str]] = None,
    remove_link: Optional[Sequence[str]] = None,
    clear_links: bool = False,
    related: Optional[Sequence[str]] = None,
    scope: Optional[Sequence[str]] = None,
    command: Optional[str] = None,
    remove_scope: Optional[Sequence[str]] = None,
    clear_scopes: bool = False,
    allow_missing_scopes: bool = False,
    body: Optional[str] = None,
    append: Optional[str] = None,
    interactive: bool = False,
) -> EditResult:
    vp = _vault_paths_for(vault)
    cwd = Path.cwd()
    init_vault(vp)
    repo_root = git_repo_root(cwd)

    note_id = note_id.strip()
    p = find_note_path(vp, note_id)
    raw_before = p.read_text("utf-8", errors="replace")

    if bool(interactive) and (body is not None or append is not None):
        raise ValueError(
            "edit: --interactive cannot be combined with --body or --append"
        )
    if body is not None and append is not None:
        raise ValueError("edit: append cannot be combined with body replacement")

    body_override: Optional[str] = None
    if body is not None:
        body_override = str(body)

    body_append: Optional[str] = None
    if append is not None:
        body_append = str(append)

    related_items = [
        s.strip()
        for s in parse_multi_csvish(list(related) if related else None)
        if s.strip()
    ]
    if related_items:
        rel_line = "Related: " + " ".join([f"[[{x}]]" for x in related_items])
        if body_append is not None:
            body_append = body_append.rstrip() + "\n\n" + rel_line
        else:
            body_append = rel_line

    if bool(interactive):
        open_in_editor(p)

    raw_after = p.read_text("utf-8", errors="replace")
    changed = raw_after != raw_before

    fm_raw, body = split_yaml_frontmatter(raw_after)
    if body_override is not None:
        body = body_override
        changed = True
    if body_append is not None:
        body = body.rstrip() + "\n\n" + body_append.rstrip() + "\n"
        changed = True

    # Apply metadata changes (additive, orthogonal).
    default_vis = "shared"
    rel = note_rel_path(vp, p)
    if rel.startswith("personal/ephemeral/"):
        default_vis = "ephemeral"
    elif rel.startswith("personal/"):
        default_vis = "personal"

    if not fm_raw:
        raise ValueError("Note is missing YAML frontmatter (expected --- at top)")

    fm, warns = normalize_note_frontmatter(
        fm_raw,
        repo_root=repo_root,
        default_visibility=default_vis,
    )
    if warns:
        # Don't die; just surface in output.
        pass

    if fm.get("id") != note_id:
        raise ValueError(
            "Refusing to edit: id mismatch after edit. "
            f"filename stem={note_id!r} frontmatter.id={fm.get('id')!r}"
        )

    # Update title
    if title:
        fm["title"] = title.strip()
        changed = True

    # Tags operations
    add_tags = _validate_tags(parse_multi_csvish(list(tag) if tag else None))
    remove_tags = _validate_tags(
        parse_multi_csvish(list(remove_tag) if remove_tag else None)
    )
    if clear_tags:
        fm.pop("tags", None)
        changed = True
    if add_tags:
        cur = _validate_tags(fm.get("tags"))
        fm["tags"] = sorted(set(cur) | set(add_tags))
        changed = True
    if remove_tags:
        cur = _validate_tags(fm.get("tags"))
        fm["tags"] = sorted([t for t in cur if t not in set(remove_tags)])
        if not fm["tags"]:
            fm.pop("tags", None)
        changed = True

    # Aliases operations
    add_aliases = [
        a.strip()
        for a in parse_multi_csvish(list(alias) if alias else None)
        if a.strip()
    ]
    remove_aliases = [
        a.strip()
        for a in parse_multi_csvish(list(remove_alias) if remove_alias else None)
        if a.strip()
    ]
    if clear_aliases:
        fm.pop("aliases", None)
        changed = True

    # Frontmatter link operations
    add_links = [
        s.strip() for s in parse_multi_csvish(list(link) if link else None) if s.strip()
    ]
    remove_links = [
        s.strip()
        for s in parse_multi_csvish(list(remove_link) if remove_link else None)
        if s.strip()
    ]
    if clear_links:
        fm.pop("links", None)
        changed = True
    if add_links or remove_links:
        cur_links = fm.get("links")
        if isinstance(cur_links, str):
            cur = [x.strip() for x in cur_links.split(",") if x.strip()]
        elif isinstance(cur_links, list):
            cur = [str(x).strip() for x in cur_links if str(x).strip()]
        else:
            cur = []

        seen_norm = {
            str(x).strip().casefold(): str(x).strip() for x in cur if str(x).strip()
        }
        for x in add_links:
            seen_norm.setdefault(x.casefold(), x)
        for x in remove_links:
            seen_norm.pop(x.casefold(), None)

        new_links = list(seen_norm.values())
        if new_links:
            fm["links"] = new_links
        else:
            fm.pop("links", None)
        changed = True
    if add_aliases or remove_aliases:
        cur = fm.get("aliases") or []
        if isinstance(cur, str):
            cur = [x.strip() for x in cur.split(",") if x.strip()]
        cur = [str(x).strip() for x in cur if str(x).strip()]
        cur_set = set(cur)
        cur_set |= set(add_aliases)
        cur_set -= set(remove_aliases)
        if cur_set:
            fm["aliases"] = sorted(cur_set)
        else:
            fm.pop("aliases", None)
        changed = True

    # Scopes operations
    add_scopes_raw = parse_multi_csvish(list(scope) if scope else None)
    if command is not None:
        cmd = str(command).strip()
        if not cmd:
            raise MemoryError(
                "--command cannot be empty",
                code="ARG",
                exit_code=2,
                hint="Provide a non-empty command signature.",
                suggestions=[
                    'loom memory edit <id> --command "uv run pytest" --append "..."',
                ],
            )
        add_scopes_raw.append(f"command:{cmd}")
    remove_scopes_raw = parse_multi_csvish(list(remove_scope) if remove_scope else None)
    if clear_scopes:
        fm.pop("scopes", None)
        changed = True
    if add_scopes_raw or remove_scopes_raw:
        cur = normalize_scopes(fm.get("scopes"), repo_root=repo_root)
        add_scopes = [
            parse_scope_string(s, repo_root=repo_root) for s in add_scopes_raw
        ]
        validate_file_scopes_exist(
            add_scopes,
            repo_root=repo_root,
            cwd=cwd,
            allow_missing=bool(allow_missing_scopes),
        )
        rem_scopes = [
            parse_scope_string(s, repo_root=repo_root) for s in remove_scopes_raw
        ]
        # Dedup/remove by JSON signature
        cur_sigs = {json.dumps(s, sort_keys=True, ensure_ascii=False): s for s in cur}
        for s in add_scopes:
            cur_sigs[json.dumps(s, sort_keys=True, ensure_ascii=False)] = s
        for s in rem_scopes:
            cur_sigs.pop(json.dumps(s, sort_keys=True, ensure_ascii=False), None)
        new_scopes = list(cur_sigs.values())
        if new_scopes:
            fm["scopes"] = new_scopes
        else:
            fm.pop("scopes", None)
        changed = True

    # Visibility/status
    if visibility:
        if visibility not in VISIBILITIES:
            raise ValueError(f"invalid visibility {visibility}")
        fm["visibility"] = visibility
        changed = True
    if status:
        if status not in STATUSES:
            raise ValueError(f"invalid status {status}")
        fm["status"] = status
        changed = True

    hydration_now = now_iso()
    hydrated_body, hydration = hydrate_wikilinks(
        vault_root=vp.root,
        body=body,
        visibility=str(fm.get("visibility") or default_vis),
        created_at=hydration_now,
        updated_at=hydration_now,
    )
    if hydrated_body != body:
        body = hydrated_body
        changed = True

    if changed:
        fm["updated_at"] = now_iso()
        rewrite_note_frontmatter(p, new_fm=fm, body=body)

    # If visibility changed, move file to the correct base dir (id stays stable).
    new_vis = fm.get("visibility") or default_vis
    base = choose_base_dir(vp, new_vis)
    # Keep subfolder structure relative to its current base, if possible.
    # We move to base/<same relative subpath minus old base>.
    old_base = vp.notes_dir
    if rel.startswith("personal/ephemeral/"):
        old_base = vp.ephemeral_notes_dir
    elif rel.startswith("personal/"):
        old_base = vp.personal_notes_dir

    moved = False
    new_path = p
    try:
        rel_under_old = p.relative_to(old_base)
        candidate = base / rel_under_old
        if candidate != p:
            if candidate.exists():
                raise ValueError(
                    "Refusing to move note: destination already exists: "
                    f"{note_rel_path(vp, candidate)}"
                )
            safe_mkdir(candidate.parent)
            shutil.move(str(p), str(candidate))
            new_path = candidate
            moved = True
    except Exception:
        # fallback: no move
        pass

    return EditResult(
        ok=True,
        id=note_id,
        path=note_rel_path(vp, new_path),
        moved=moved,
        updated=changed,
        warnings=warns,
        links=compute_link_diagnostics(vp, note_id),
        hydration=hydration,
    )


def reindex(*, vault: Optional[str] = None, quiet: bool = False) -> ReindexResult:
    vp = _vault_paths_for(vault)
    # Deterministic rebuild: delete tables then sync.
    safe_mkdir(vp.root)
    delete_db_files(vp)
    with connect_db(vp) as conn:
        res = sync_index(vp, conn, quiet=bool(quiet))
    return ReindexResult(
        ok=bool(res.get("ok")),
        indexed=int(res.get("indexed") or 0),
        updated=int(res.get("updated") or 0),
        deleted=int(res.get("deleted") or 0),
        skipped=int(res.get("skipped") or 0),
        warnings=list(res.get("warnings") or []),
    )


def _recall_item_from_dict(item: Dict[str, Any]) -> RecallItem:
    def _float_or(val: Any, default: float) -> float:
        try:
            return float(val)
        except Exception:
            return default

    score_data = item.get("score") or {}
    score = None
    if isinstance(score_data, dict) and score_data:
        bm25_raw = score_data.get("bm25")
        score = RecallScore(
            final=_float_or(score_data.get("final"), 0.0),
            fts=_float_or(score_data.get("fts"), 0.0),
            bm25=_float_or(bm25_raw, 0.0) if bm25_raw is not None else None,
            scope=_float_or(score_data.get("scope"), 0.0),
            recency=_float_or(score_data.get("recency"), 0.0),
        )

    why_data = item.get("why") or {}
    why = None
    if isinstance(why_data, dict) and why_data:
        why = RecallWhy(
            matched_tags=why_data.get("matched_tags"),
            excluded_tags=why_data.get("excluded_tags"),
            matched_scopes=why_data.get("matched_scopes"),
            excluded_scopes=why_data.get("excluded_scopes"),
            fts_snippet=why_data.get("fts_snippet"),
            recency_age_days=why_data.get("recency_age_days"),
            via=why_data.get("via"),
            graph_distance=why_data.get("graph_distance"),
        )

    return RecallItem(
        id=str(item.get("id") or ""),
        title=str(item.get("title") or ""),
        path=str(item.get("path") or ""),
        visibility=str(item.get("visibility") or ""),
        status=str(item.get("status") or ""),
        tags=list(item.get("tags") or []),
        aliases=list(item.get("aliases") or []),
        scopes=list(item.get("scopes") or []),
        created_at=str(item.get("created_at") or ""),
        updated_at=str(item.get("updated_at") or ""),
        preview=str(item.get("preview") or ""),
        score=score,
        why=why,
        role=str(item.get("role") or "hit"),
        body=item.get("body"),
    )


def recall(
    *,
    vault: Optional[str] = None,
    query: str = "",
    limit: int = 8,
    tag: Optional[Sequence[str]] = None,
    not_tag: Optional[Sequence[str]] = None,
    scope: Optional[Sequence[str]] = None,
    not_scope: Optional[Sequence[str]] = None,
    command: str = "",
    visibility: Optional[Sequence[str]] = None,
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
) -> RecallResult:
    vp = _vault_paths_for(vault)
    raw, warnings = recall_impl(
        vp,
        query=query,
        limit=limit,
        tag=list(tag) if tag else None,
        not_tag=list(not_tag) if not_tag else None,
        scope=list(scope) if scope else None,
        not_scope=list(not_scope) if not_scope else None,
        command=command,
        visibility=list(visibility) if visibility else None,
        include_deprecated=include_deprecated,
        since=since,
        until=until,
        and_mode=and_mode,
        scoped_only=scoped_only,
        full=full,
        max_body_chars=max_body_chars,
        expand=expand,
        max_chars=max_chars,
        context=context,
        deterministic=deterministic,
        quiet=quiet,
        allow_missing_scopes=allow_missing_scopes,
        format=format,
        or_mode=bool(or_mode),
        fts_raw=bool(fts_raw),
    )
    if isinstance(raw, str):
        return RecallResult(items=[], context_text=raw, warnings=warnings)
    items = [_recall_item_from_dict(it) for it in (raw or [])]
    return RecallResult(items=items, context_text="", warnings=warnings)


def list_recent(
    *,
    vault: Optional[str] = None,
    limit: int = 20,
    tag: Optional[Sequence[str]] = None,
    not_tag: Optional[Sequence[str]] = None,
    scope: Optional[Sequence[str]] = None,
    not_scope: Optional[Sequence[str]] = None,
    command: str = "",
    visibility: Optional[Sequence[str]] = None,
    include_deprecated: bool = False,
    since: Optional[str] = None,
    until: Optional[str] = None,
    and_mode: bool = False,
    scoped_only: bool = False,
    deterministic: bool = False,
    quiet: bool = False,
    allow_missing_scopes: bool = False,
    sort: str = "updated",
) -> RecallResult:
    vp = _vault_paths_for(vault)

    cwd = Path.cwd()
    repo_root = git_repo_root(cwd)
    tags = _validate_tags(parse_multi_csvish(list(tag) if tag else None))
    not_tags = _validate_tags(parse_multi_csvish(list(not_tag) if not_tag else None))

    scope_args = parse_multi_csvish(list(scope) if scope else None)
    if command:
        scope_args.append(f"command:{command}")
    ctx_scopes = [parse_scope_string(s, repo_root=repo_root) for s in scope_args]
    validate_file_scopes_exist(
        ctx_scopes,
        repo_root=repo_root,
        cwd=cwd,
        allow_missing=bool(allow_missing_scopes),
    )

    not_scope_args = parse_multi_csvish(list(not_scope) if not_scope else None)
    not_ctx_scopes = (
        [parse_scope_string(s, repo_root=repo_root) for s in not_scope_args]
        if not_scope_args
        else []
    )

    vis = list(visibility) if visibility else default_visibility_from_env()

    raw, warnings = list_impl(
        vp,
        limit=int(limit),
        tags=tags,
        not_tags=not_tags,
        ctx_scopes=ctx_scopes,
        not_ctx_scopes=not_ctx_scopes,
        visibility=vis,
        include_deprecated=bool(include_deprecated),
        since=since,
        until=until,
        and_mode=bool(and_mode),
        scoped_only=bool(scoped_only),
        deterministic=bool(deterministic),
        quiet=bool(quiet),
        sort=str(sort or "updated"),
    )
    items = [_recall_item_from_dict(it) for it in (raw or [])]
    return RecallResult(items=items, context_text="", warnings=warnings)


def grep(
    *,
    vault: Optional[str] = None,
    pattern: str,
    limit: int = 20,
    tag: Optional[Sequence[str]] = None,
    not_tag: Optional[Sequence[str]] = None,
    scope: Optional[Sequence[str]] = None,
    not_scope: Optional[Sequence[str]] = None,
    command: str = "",
    visibility: Optional[Sequence[str]] = None,
    include_deprecated: bool = False,
    since: Optional[str] = None,
    until: Optional[str] = None,
    and_mode: bool = False,
    scoped_only: bool = False,
    quiet: bool = False,
    allow_missing_scopes: bool = False,
    ignore_case: bool = False,
) -> Dict[str, Any]:
    vp = _vault_paths_for(vault)

    cwd = Path.cwd()
    repo_root = git_repo_root(cwd)

    tags = _validate_tags(parse_multi_csvish(list(tag) if tag else None))
    not_tags = _validate_tags(parse_multi_csvish(list(not_tag) if not_tag else None))

    scope_args = parse_multi_csvish(list(scope) if scope else None)
    if command:
        scope_args.append(f"command:{command}")
    ctx_scopes = [parse_scope_string(s, repo_root=repo_root) for s in scope_args]
    validate_file_scopes_exist(
        ctx_scopes,
        repo_root=repo_root,
        cwd=cwd,
        allow_missing=bool(allow_missing_scopes),
    )

    not_scope_args = parse_multi_csvish(list(not_scope) if not_scope else None)
    not_ctx_scopes = (
        [parse_scope_string(s, repo_root=repo_root) for s in not_scope_args]
        if not_scope_args
        else []
    )

    vis = list(visibility) if visibility else default_visibility_from_env()

    items, warnings = grep_impl(
        vp,
        pattern=str(pattern or ""),
        limit=int(limit),
        tags=tags,
        not_tags=not_tags,
        ctx_scopes=ctx_scopes,
        not_ctx_scopes=not_ctx_scopes,
        visibility=vis,
        include_deprecated=bool(include_deprecated),
        since=since,
        until=until,
        and_mode=bool(and_mode),
        scoped_only=bool(scoped_only),
        quiet=bool(quiet),
        ignore_case=bool(ignore_case),
    )
    return {"ok": True, "items": items, "warnings": warnings}


def show(
    *,
    vault: Optional[str] = None,
    note_id: str,
    meta_only: bool = False,
) -> str:
    vp = _vault_paths_for(vault)
    init_vault(vp)
    p = find_note_path(vp, note_id.strip())
    raw = p.read_text("utf-8", errors="replace")
    if not meta_only:
        return raw.rstrip() + "\n"
    fm, _body = split_yaml_frontmatter(raw)
    if not fm:
        return ""
    return dump_yaml_frontmatter(fm).rstrip() + "\n"


def open_note(*, vault: Optional[str] = None, note_id: str) -> str:
    vp = _vault_paths_for(vault)
    init_vault(vp)
    p = find_note_path(vp, note_id.strip())
    open_in_editor(p)
    return note_rel_path(vp, p)


def forget(
    *,
    vault: Optional[str] = None,
    query: str = "",
    limit: int = 50,
    tag: Optional[Sequence[str]] = None,
    not_tag: Optional[Sequence[str]] = None,
    scope: Optional[Sequence[str]] = None,
    not_scope: Optional[Sequence[str]] = None,
    command: str = "",
    visibility: Optional[Sequence[str]] = None,
    include_deprecated: bool = False,
    since: Optional[str] = None,
    until: Optional[str] = None,
    and_mode: bool = False,
    scoped_only: bool = False,
    deterministic: bool = False,
    quiet: bool = False,
    allow_missing_scopes: bool = False,
    or_mode: bool = False,
    fts_raw: bool = False,
    apply: bool = False,
    hard: bool = False,
) -> Dict[str, Any]:
    vp = _vault_paths_for(vault)
    init_vault(vp)

    if (
        not (query or "").strip()
        and not (tag or [])
        and not (scope or [])
        and not (command or "").strip()
        and not (since or "").strip()
        and not (until or "").strip()
    ):
        raise MemoryError(
            "forget requires a query or at least one filter",
            code="ARG",
            exit_code=2,
            hint="Provide a query/tag/scope/command/time window so forget is intentional.",
            suggestions=[
                "loom memory forget 'query'",
                "loom memory forget --tag <tag>",
                "loom memory forget --scope file:src/app.py",
                "loom memory forget --command 'pytest -q'",
                "loom memory forget --since 2026-02-01",
            ],
        )

    res = recall(
        vault=vault,
        query=query,
        limit=int(limit),
        tag=tag,
        not_tag=not_tag,
        scope=scope,
        not_scope=not_scope,
        command=command,
        visibility=visibility,
        include_deprecated=include_deprecated,
        since=since,
        until=until,
        and_mode=and_mode,
        scoped_only=scoped_only,
        full=False,
        deterministic=bool(deterministic),
        quiet=bool(quiet),
        allow_missing_scopes=bool(allow_missing_scopes),
        format="json",
        or_mode=bool(or_mode),
        fts_raw=bool(fts_raw),
    )

    candidates = [
        {
            "id": it.id,
            "title": it.title,
            "path": it.path,
            "visibility": it.visibility,
            "status": it.status,
            "updated_at": it.updated_at,
        }
        for it in res.items
    ]

    if hard and not apply:
        raise MemoryError(
            "forget --hard requires --apply",
            code="ARG",
            exit_code=2,
            hint="Run with --apply to perform hard deletes.",
            suggestions=["loom memory forget <filters> --hard --apply"],
        )

    if not apply:
        return {
            "ok": True,
            "dry_run": True,
            "hard": bool(hard),
            "count": len(candidates),
            "candidates": candidates,
        }

    changed: List[Dict[str, Any]] = []
    deleted: List[Dict[str, Any]] = []

    if hard:
        for c in candidates:
            nid = str(c.get("id") or "").strip()
            if not nid:
                continue
            p = find_note_path(vp, nid)
            with contextlib.suppress(Exception):
                p.unlink()
                deleted.append({"id": nid, "path": note_rel_path(vp, p)})
        with connect_db(vp) as conn:
            sync_index(vp, conn, quiet=bool(quiet))
        return {
            "ok": True,
            "dry_run": False,
            "hard": True,
            "deleted": deleted,
            "deleted_count": len(deleted),
        }

    for c in candidates:
        nid = str(c.get("id") or "").strip()
        if not nid:
            continue
        er = edit(
            vault=vault,
            note_id=nid,
            status="deprecated",
        )
        changed.append({"id": nid, "path": er.path, "updated": er.updated})

    return {
        "ok": True,
        "dry_run": False,
        "hard": False,
        "deprecated": changed,
        "deprecated_count": len(changed),
    }


def around(
    *,
    vault: Optional[str] = None,
    note_id: str,
    k: int = 12,
    by: str = "updated",
    window_days: int = 14,
    visibility: Optional[Sequence[str]] = None,
    include_deprecated: bool = False,
    quiet: bool = False,
) -> Dict[str, Any]:
    vp = _vault_paths_for(vault)
    vis = list(visibility) if visibility else default_visibility_from_env()
    items, warnings = around_impl(
        vp,
        note_id=note_id,
        k=int(k),
        by=str(by or "updated"),
        window_days=int(window_days),
        visibility=vis,
        include_deprecated=bool(include_deprecated),
        quiet=bool(quiet),
    )
    return {"ok": True, "items": items, "warnings": warnings}


def timeline(
    *,
    vault: Optional[str] = None,
    days: int = 30,
    by: str = "updated",
    visibility: Optional[Sequence[str]] = None,
    include_deprecated: bool = False,
    quiet: bool = False,
) -> Dict[str, Any]:
    vp = _vault_paths_for(vault)
    vis = list(visibility) if visibility else default_visibility_from_env()
    items, warnings = timeline_impl(
        vp,
        days=int(days),
        by=str(by or "updated"),
        visibility=vis,
        include_deprecated=bool(include_deprecated),
        quiet=bool(quiet),
    )
    return {"ok": True, "items": items, "warnings": warnings}


def _collect_stale_file_scopes(
    scopes: List[Dict[str, Any]], *, repo_root: Optional[Path], cwd: Path
) -> List[Dict[str, Any]]:
    stale: List[Dict[str, Any]] = []
    for s in scopes or []:
        if not isinstance(s, dict) or s.get("kind") != "file":
            continue
        p = s.get("path")
        if not isinstance(p, str) or not p.strip():
            continue
        resolved = resolve_scope_path(scope_path=p, repo_root=repo_root, cwd=cwd)
        if not resolved.exists() or not resolved.is_file():
            stale.append({"kind": "file", "path": p})
    return stale


def janitor(
    *,
    vault: Optional[str] = None,
    cmd: str = "report",
    visibility: Optional[Sequence[str]] = None,
    limit: int = 200,
    apply: bool = False,
    quiet: bool = False,
) -> JanitorReportResult | JanitorFixResult:
    vp = _vault_paths_for(vault)
    cwd = Path.cwd()
    repo_root = git_repo_root(cwd)
    visibility = list(visibility) if visibility else ["shared"]
    limit = int(limit or 200)

    rows: List[Dict[str, Any]] = []
    changed = 0

    for p, default_vis in iter_note_paths(vp):
        if default_vis not in visibility:
            continue
        note, warns = try_read_note_from_path(
            p, default_visibility=default_vis, repo_root=repo_root
        )
        if note is None:
            continue
        stale = _collect_stale_file_scopes(
            note.scopes or [], repo_root=repo_root, cwd=cwd
        )
        if not stale:
            continue
        rows.append(
            {
                "id": note.id,
                "path": note_rel_path(vp, p),
                "visibility": default_vis,
                "stale_scopes": stale,
                "warnings": warns,
            }
        )
        if len(rows) >= limit:
            break

    def _note_from_row(row: Dict[str, Any]) -> JanitorNote:
        return JanitorNote(
            id=str(row.get("id") or ""),
            path=str(row.get("path") or ""),
            visibility=str(row.get("visibility") or ""),
            stale_scopes=list(row.get("stale_scopes") or []),
            warnings=list(row.get("warnings") or []),
        )

    if cmd == "report":
        return JanitorReportResult(
            ok=True,
            count=len(rows),
            notes=[_note_from_row(r) for r in rows],
        )

    if cmd == "fix":
        if not bool(apply):
            return JanitorFixResult(
                ok=True,
                dry_run=True,
                count=len(rows),
                notes=[_note_from_row(r) for r in rows],
                hint="Re-run with: memory janitor fix --apply",
                updated_notes=0,
                reported=0,
            )

        for r in rows:
            nid = r["id"]
            try:
                np = find_note_path(vp, nid)
            except Exception:
                continue
            raw = np.read_text("utf-8", errors="replace")
            fm_raw, body = split_yaml_frontmatter(raw)
            if not fm_raw:
                continue
            fm, _ = normalize_note_frontmatter(
                fm_raw,
                repo_root=repo_root,
                default_visibility=r.get("visibility") or "shared",
            )
            scopes = normalize_scopes(fm.get("scopes"), repo_root=repo_root)
            stale = _collect_stale_file_scopes(scopes, repo_root=repo_root, cwd=cwd)
            if not stale:
                continue
            stale_set = {s.get("path") for s in stale}
            new_scopes = [
                s
                for s in scopes
                if s.get("kind") != "file" or s.get("path") not in stale_set
            ]
            if new_scopes:
                fm["scopes"] = new_scopes
            else:
                fm.pop("scopes", None)
            fm["updated_at"] = now_iso()
            rewrite_note_frontmatter(np, new_fm=fm, body=body)
            changed += 1

        with connect_db(vp) as conn:
            sync_index(vp, conn, quiet=bool(quiet))

        return JanitorFixResult(
            ok=True,
            dry_run=False,
            count=len(rows),
            notes=[_note_from_row(r) for r in rows],
            updated_notes=changed,
            reported=len(rows),
        )

    raise ValueError(f"Unknown janitor subcommand: {cmd}")


def link(
    *,
    vault: Optional[str] = None,
    cmd: str = "backlinks",
    note_id: str = "",
    limit: int = 200,
    k: int = 1,
    include_unresolved: bool = False,
    visibility: Optional[Sequence[str]] = None,
    include_deprecated: bool = False,
    quiet: bool = False,
) -> (
    LinkBacklinksResult
    | LinkNeighborsResult
    | LinkValidateResult
    | LinkGraphResult
    | LinkSuggestResult
):
    vp = _vault_paths_for(vault)

    if cmd == "suggest":
        vis = list(visibility) if visibility else default_visibility_from_env()
        suggestions, warns2 = suggest_links_impl(
            vp,
            note_id=note_id,
            limit=int(limit),
            visibility=vis,
            include_deprecated=bool(include_deprecated),
            quiet=bool(quiet),
        )
        return LinkSuggestResult(
            id=str(note_id or "").strip(),
            suggestions=[
                LinkSuggestItem(
                    id=str(s.get("id") or ""),
                    title=str(s.get("title") or ""),
                    path=str(s.get("path") or ""),
                    updated_at=str(s.get("updated_at") or ""),
                    score=float(s.get("score") or 0.0),
                    why=dict(s.get("why") or {}),
                )
                for s in (suggestions or [])
            ],
            warnings=list(warns2 or []),
        )

    with connect_db(vp) as conn:
        sync_res = sync_index(vp, conn, quiet=bool(quiet))
        warnings = list(sync_res.get("warnings") or [])

        if cmd == "backlinks":
            nid = note_id
            rows = conn.execute(
                """
                SELECT n.id, n.title, n.md_path, n.updated_at
                FROM links l JOIN notes n ON n.id = l.src_id
                WHERE l.dst_id=? AND l.resolution='resolved'
                ORDER BY n.updated_at DESC, n.id ASC
                LIMIT ?;
                """,
                (nid, int(limit)),
            ).fetchall()
            return LinkBacklinksResult(
                backlinks=[
                    LinkBacklink(
                        id=r["id"],
                        title=r["title"],
                        path=r["md_path"],
                        updated_at=r["updated_at"],
                    )
                    for r in rows
                ],
                warnings=warnings,
            )

        if cmd == "neighbors":
            nid = note_id
            k = int(k)
            if k <= 0:
                nb = graph_neighbors(conn, nid)
                return LinkNeighborsResult(
                    id=nid, k=k, neighbors=nb, nodes=None, warnings=warnings
                )
            expanded = graph_expand(conn, [nid], k=k)
            expanded.remove(nid)
            notes = fetch_notes_by_ids(conn, expanded)
            return LinkNeighborsResult(
                id=nid, k=k, neighbors=None, nodes=notes, warnings=warnings
            )

        if cmd == "validate":
            # Broken links: missing or ambiguous.
            where = "l.resolution != 'resolved'"
            params: List[Any] = []
            if note_id:
                where += " AND l.src_id=?"
                params.append(note_id)
            rows = conn.execute(
                """
                SELECT l.src_id, l.dst_raw, l.resolution, l.style, l.alias_text, l.anchor
                FROM links l
                WHERE """
                + where
                + """
                ORDER BY l.src_id ASC, l.dst_raw ASC
                LIMIT ?;
                """,
                (*params, int(limit)),
            ).fetchall()
            res = [
                {
                    "src_id": r["src_id"],
                    "dst_raw": r["dst_raw"],
                    "resolution": r["resolution"],
                    "style": r["style"],
                    "alias_text": r["alias_text"],
                    "anchor": r["anchor"],
                }
                for r in rows
            ]
            return LinkValidateResult(
                rows=[
                    LinkValidateRow(
                        src_id=str(r.get("src_id") or ""),
                        dst_raw=str(r.get("dst_raw") or ""),
                        resolution=str(r.get("resolution") or ""),
                        style=str(r.get("style") or ""),
                        alias_text=str(r.get("alias_text") or ""),
                        anchor=str(r.get("anchor") or ""),
                    )
                    for r in res
                ],
                warnings=warnings,
            )

        if cmd == "graph":
            # Simple edge list.
            where = "1=1"
            params_graph: List[Any] = []
            if include_unresolved:
                pass
            else:
                where = "l.resolution='resolved' AND l.dst_id IS NOT NULL"
            rows = conn.execute(
                """
                SELECT l.src_id, COALESCE(l.dst_id, '') AS dst_id, l.dst_raw, l.resolution, l.style
                FROM links l
                WHERE """
                + where
                + """
                ORDER BY l.src_id ASC, l.dst_raw ASC;
                """,
                params_graph,
            ).fetchall()
            return LinkGraphResult(
                edges=[
                    LinkGraphEdge(
                        src_id=r["src_id"],
                        dst_id=r["dst_id"] or None,
                        dst_raw=r["dst_raw"],
                        resolution=r["resolution"],
                        style=r["style"],
                    )
                    for r in rows
                ],
                warnings=warnings,
            )

    raise ValueError(f"Unknown link subcommand: {cmd}")
