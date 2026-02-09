from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from agent_loom.memory.constants import RE_NOTE_ID, WIKILINK_RE
from agent_loom.memory.vault import (
    generate_note_id,
    iter_note_paths,
    note_rel_path,
    try_read_note_from_path,
    vault_paths,
    write_note_file,
)


def slugify_name(s: str) -> str:
    base = re.sub(r"[^A-Za-z0-9]+", "-", (s or "").strip()).strip("-").lower()
    return base or "note"


def normalize_name_key(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip()).casefold()


def _split_fenced_blocks(md: str) -> List[Tuple[bool, str]]:
    """Split markdown into (is_fenced_code, text) chunks.

    This is a conservative, line-oriented splitter that avoids rewriting content inside
    fenced code blocks (``` or ~~~). It doesn't try to parse markdown; it just tracks
    fence open/close lines.
    """

    lines = (
        (md or "").replace("\r\n", "\n").replace("\r", "\n").splitlines(keepends=True)
    )
    out: List[Tuple[bool, str]] = []
    buf: List[str] = []
    in_fence = False
    fence_tok: Optional[str] = None

    def flush() -> None:
        nonlocal buf
        if not buf:
            return
        out.append((in_fence, "".join(buf)))
        buf = []

    for ln in lines:
        stripped = ln.lstrip()
        if not in_fence:
            if stripped.startswith("```"):
                flush()
                in_fence = True
                fence_tok = "```"
            elif stripped.startswith("~~~"):
                flush()
                in_fence = True
                fence_tok = "~~~"
        else:
            if fence_tok is not None and stripped.startswith(fence_tok):
                buf.append(ln)
                flush()
                in_fence = False
                fence_tok = None
                continue

        buf.append(ln)

    flush()
    return out


def _split_inline_code_spans(md: str) -> List[Tuple[bool, str]]:
    """Split markdown into (is_inline_code, text) chunks using backtick fences."""

    t = md or ""
    out: List[Tuple[bool, str]] = []
    i = 0
    last = 0
    n = len(t)
    while i < n:
        if t[i] != "`":
            i += 1
            continue

        # Count backtick run length.
        j = i
        while j < n and t[j] == "`":
            j += 1
        tick_len = j - i

        # Find matching close run.
        close = t.find("`" * tick_len, j)
        if close == -1:
            i = j
            continue

        if last < i:
            out.append((False, t[last:i]))
        out.append((True, t[i : close + tick_len]))
        i = close + tick_len
        last = i

    if last < n:
        out.append((False, t[last:]))
    return out


@dataclass(frozen=True)
class HydrationCreatedNote:
    id: str
    title: str
    visibility: str
    path: str
    slug: str


@dataclass(frozen=True)
class HydrationRewrite:
    raw: str
    to: str
    target: str
    resolved_id: str
    created: bool


def _parse_wikilink_inner(inner: str) -> Tuple[str, Optional[str], Optional[str]]:
    raw = (inner or "").strip()
    if not raw:
        return "", None, None

    target, alias = raw, None
    if "|" in raw:
        target, alias = raw.split("|", 1)
        target = target.strip()
        alias = (alias or "").strip() or None

    anchor = None
    if "#" in target:
        target, anchor = target.split("#", 1)
        target = target.strip()
        anchor = (anchor or "").strip() or None

    return target, alias, anchor


def _compose_wikilink(*, note_id: str, anchor: Optional[str], display: str) -> str:
    dst = note_id
    if anchor:
        dst = f"{dst}#{anchor}"
    disp = (display or "").strip() or note_id
    return f"[[{dst}|{disp}]]"


def _scan_vault_indexes(vault_root: Path) -> Dict[str, Any]:
    vp = vault_paths(vault_root)
    repo_root = None
    slug_to_ids: Dict[str, List[str]] = {}
    name_to_ids: Dict[str, List[str]] = {}
    title_exact_to_ids: Dict[str, List[str]] = {}
    id_set: set[str] = set()

    for p, default_vis in iter_note_paths(vp):
        note_id = p.stem
        if not RE_NOTE_ID.match(note_id):
            continue
        n, _warns = try_read_note_from_path(
            p, default_visibility=default_vis, repo_root=repo_root
        )
        if n is None:
            continue
        id_set.add(n.id)

        def add(map0: Dict[str, List[str]], k: str, v: str) -> None:
            kk = (k or "").strip()
            if not kk:
                return
            map0.setdefault(kk, []).append(v)

        title_norm = normalize_name_key(n.title)
        add(name_to_ids, title_norm, n.id)
        add(title_exact_to_ids, (n.title or "").strip().casefold(), n.id)
        add(slug_to_ids, slugify_name(n.title), n.id)
        for a in n.aliases or []:
            add(name_to_ids, normalize_name_key(a), n.id)
            add(slug_to_ids, slugify_name(a), n.id)

    # Dedup/sort for deterministic picks.
    def norm_map(m: Dict[str, List[str]]) -> Dict[str, List[str]]:
        out: Dict[str, List[str]] = {}
        for k, ids in m.items():
            out[k] = sorted(set([i for i in ids if i]))
        return out

    return {
        "vp": vp,
        "slug_to_ids": norm_map(slug_to_ids),
        "name_to_ids": norm_map(name_to_ids),
        "title_exact_to_ids": norm_map(title_exact_to_ids),
        "id_set": sorted(id_set),
    }


def _pick_candidate(
    *, target: str, target_slug: str, idx: Dict[str, Any]
) -> Tuple[Optional[str], List[str]]:
    # Prefer:
    # 1) exact note id match
    # 2) exact title match (case-insensitive)
    # 3) slug match (unique)
    # 4) normalized name match (unique)
    # else ambiguous/missing
    target = (target or "").strip()
    if not target:
        return None, []

    id_set = set(idx.get("id_set") or [])
    if RE_NOTE_ID.match(target) and target in id_set:
        return target, []

    title_exact = (target or "").strip().casefold()
    tmap = idx.get("title_exact_to_ids") or {}
    if isinstance(tmap, dict):
        cands = list(tmap.get(title_exact) or [])
        if len(cands) == 1:
            return cands[0], []
        if len(cands) > 1:
            return None, cands

    smap = idx.get("slug_to_ids") or {}
    if isinstance(smap, dict):
        cands = list(smap.get(target_slug) or [])
        if len(cands) == 1:
            return cands[0], []
        if len(cands) > 1:
            # Prefer a short, non-timestamp id if it's present (human-created canonical id).
            if target_slug in cands:
                return target_slug, []
            return None, cands

    nmap = idx.get("name_to_ids") or {}
    if isinstance(nmap, dict):
        cands = list(nmap.get(normalize_name_key(target)) or [])
        if len(cands) == 1:
            return cands[0], []
        if len(cands) > 1:
            return None, cands

    return None, []


def _ensure_stub_note(
    *,
    vp,
    title: str,
    visibility: str,
    created_at: str,
    updated_at: str,
) -> HydrationCreatedNote:
    # Create a brand new id; retry a few times to avoid pathological collisions.
    for _ in range(5):
        nid = generate_note_id(title)
        p = vp.notes_dir / f"{nid}.md"
        if visibility == "personal":
            p = vp.personal_notes_dir / f"{nid}.md"
        if visibility == "ephemeral":
            p = vp.ephemeral_notes_dir / f"{nid}.md"
        if p.exists():
            continue

        wp = write_note_file(
            vp,
            note_id=nid,
            title=title,
            body="",
            tags=[],
            aliases=[],
            scopes=[],
            visibility=visibility,
            status="active",
            created_at=created_at,
            updated_at=updated_at,
            folder="",
            frontmatter_extra=None,
        )
        return HydrationCreatedNote(
            id=nid,
            title=title,
            visibility=visibility,
            path=note_rel_path(vp, wp),
            slug=slugify_name(title),
        )

    raise RuntimeError("failed to create stub note id after retries")


def hydrate_wikilinks(
    *,
    vault_root: Path,
    body: str,
    visibility: str,
    created_at: str,
    updated_at: str,
) -> Tuple[str, Dict[str, Any]]:
    idx = _scan_vault_indexes(vault_root)
    vp = idx["vp"]

    created_by_slug: Dict[str, HydrationCreatedNote] = {}
    rewrites: List[HydrationRewrite] = []
    ambiguous: List[Dict[str, Any]] = []

    def resolve_target(target: str) -> Tuple[Optional[str], bool, List[str]]:
        slug = slugify_name(target)
        if slug in created_by_slug:
            return created_by_slug[slug].id, True, []

        resolved, amb = _pick_candidate(target=target, target_slug=slug, idx=idx)
        if resolved is not None:
            return resolved, False, []
        if amb:
            return None, False, amb

        cn = _ensure_stub_note(
            vp=vp,
            title=target,
            visibility=visibility,
            created_at=created_at,
            updated_at=updated_at,
        )
        created_by_slug[slug] = cn
        # Update indexes in-memory so subsequent resolutions in the same call reuse.
        (idx["slug_to_ids"]).setdefault(slug, []).append(cn.id)
        (idx["name_to_ids"]).setdefault(normalize_name_key(target), []).append(cn.id)
        (idx["title_exact_to_ids"]).setdefault(target.strip().casefold(), []).append(
            cn.id
        )
        (idx["id_set"]).append(cn.id)
        return cn.id, True, []

    def rewrite_plain_text(t: str) -> str:
        if not t:
            return t

        def rewrite_segment(seg: str) -> str:
            out0: List[str] = []
            last0 = 0
            for m in WIKILINK_RE.finditer(seg):
                inner = (m.group(1) or "").strip()
                if not inner:
                    continue
                target, alias, anchor = _parse_wikilink_inner(inner)
                if not target:
                    continue
                display = alias or target
                # Resolve path-ish targets by basename as well.
                raw_target = target
                if "/" in raw_target or raw_target.lower().endswith(".md"):
                    base = raw_target.replace("\\", "/").rstrip("/").split("/")[-1]
                    if base.lower().endswith(".md"):
                        base = base[:-3]
                    target = base.strip() or raw_target

                resolved_id, created, amb = resolve_target(target)
                if amb:
                    ambiguous.append(
                        {
                            "raw": raw_target,
                            "slug": slugify_name(target),
                            "candidates": sorted(set([x for x in amb if x])),
                        }
                    )
                    continue
                if resolved_id is None:
                    continue

                replacement = _compose_wikilink(
                    note_id=resolved_id,
                    anchor=anchor,
                    display=display,
                )

                raw_link = f"[[{inner}]]"
                if replacement == raw_link:
                    continue

                out0.append(seg[last0 : m.start()])
                out0.append(replacement)
                last0 = m.end()
                rewrites.append(
                    HydrationRewrite(
                        raw=raw_link,
                        to=replacement,
                        target=raw_target,
                        resolved_id=resolved_id,
                        created=created,
                    )
                )
            out0.append(seg[last0:])
            return "".join(out0)

        seg_out: List[str] = []
        for is_code, seg in _split_inline_code_spans(t):
            seg_out.append(seg if is_code else rewrite_segment(seg))
        return "".join(seg_out)

    chunks = _split_fenced_blocks(body)
    rewritten_chunks: List[str] = []
    for is_code, text in chunks:
        rewritten_chunks.append(text if is_code else rewrite_plain_text(text))
    new_body = "".join(rewritten_chunks)

    created_notes = list(created_by_slug.values())
    created_notes.sort(key=lambda x: x.id)
    rewrites.sort(key=lambda x: (x.resolved_id, x.raw, x.to))
    ambiguous.sort(key=lambda x: str(x.get("raw") or ""))

    hydration: Dict[str, Any] = {
        "rewrites": [
            {
                "raw": r.raw,
                "to": r.to,
                "target": r.target,
                "resolved_id": r.resolved_id,
                "created": r.created,
            }
            for r in rewrites
        ],
        "created_notes": [
            {
                "id": n.id,
                "title": n.title,
                "visibility": n.visibility,
                "path": n.path,
                "slug": n.slug,
            }
            for n in created_notes
        ],
        "ambiguous": ambiguous,
    }
    return new_body, hydration


__all__ = [
    "hydrate_wikilinks",
    "normalize_name_key",
    "slugify_name",
]
