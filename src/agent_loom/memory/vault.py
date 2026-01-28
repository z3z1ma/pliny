from __future__ import annotations

import contextlib
import datetime as dt
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from agent_loom.core.git import git_repo_root as core_git_repo_root
from agent_loom.memory.constants import (
    DB_FILENAME,
    META_FILENAME,
    RE_NOTE_ID,
    STATUSES,
    VISIBILITIES,
)
from agent_loom.memory.frontmatter import (
    canonicalize_rfc3339_utc,
    dump_yaml_frontmatter,
    split_yaml_frontmatter,
)
from agent_loom.memory.models import Note, VaultPaths
from agent_loom.memory.scopes import _validate_tags, normalize_scopes
from agent_loom.memory.errors import MemoryError
from agent_loom.memory.utils import now_iso, safe_mkdir, sha256_text


def git_repo_root(start: Path) -> Optional[Path]:
    return core_git_repo_root(start)


def resolve_vault_root(vault: str, *, cwd: Path) -> Path:
    p = Path(vault or "").expanduser()
    if p.is_absolute():
        return p.resolve()

    repo_root = git_repo_root(cwd)
    if repo_root is not None:
        return (repo_root / p).resolve()
    return (cwd / p).resolve()


def vault_paths(root: Path) -> VaultPaths:
    root = root.expanduser().resolve()
    return VaultPaths(
        root=root,
        notes_dir=root / "notes",
        personal_notes_dir=root / "personal" / "notes",
        ephemeral_notes_dir=root / "personal" / "ephemeral" / "notes",
        db_path=root / DB_FILENAME,
        meta_path=root / META_FILENAME,
    )


def iter_note_paths(vp: VaultPaths) -> List[Tuple[Path, str]]:
    out: List[Tuple[Path, str]] = []
    for base, vis in [
        (vp.notes_dir, "shared"),
        (vp.personal_notes_dir, "personal"),
        (vp.ephemeral_notes_dir, "ephemeral"),
    ]:
        if base.exists():
            for p in base.rglob("*.md"):
                if p.is_file():
                    out.append((p, vis))
    out.sort(key=lambda t: str(t[0]).replace(os.sep, "/"))
    return out


def find_note_path(vp: VaultPaths, note_id: str) -> Path:
    if not note_id:
        raise MemoryError(
            "Note id is required",
            code="ARG",
            exit_code=2,
            hint="Provide a note id like `hello-world`.",
        )

    for base in [vp.notes_dir, vp.personal_notes_dir, vp.ephemeral_notes_dir]:
        p0 = base / f"{note_id}.md"
        if p0.exists():
            return p0

    matches: List[Path] = []
    for p, _ in iter_note_paths(vp):
        if p.stem == note_id:
            matches.append(p)

    if not matches:
        raise MemoryError(
            f"Note not found: {note_id}",
            code="NOT_FOUND",
            exit_code=2,
            hint="Search for a note by content or title.",
            suggestions=[
                f"loom memory recall {note_id!r}",
                "loom memory recall <query>",
            ],
            details={"id": note_id},
        )
    if len(matches) == 1:
        return matches[0]

    rels = [str(p.relative_to(vp.root)).replace(os.sep, "/") for p in matches]
    raise MemoryError(
        f"Ambiguous note id {note_id!r}",
        code="ARG",
        exit_code=2,
        hint="Multiple notes share the same id. Use one id per vault.",
        suggestions=[
            "Rename or move one of the duplicates so ids are unique",
            f"Matches: {', '.join(sorted(rels)[:10])}",
        ],
        details={"id": note_id, "matches": sorted(rels)},
    )


def note_rel_path(vp: VaultPaths, p: Path) -> str:
    try:
        return str(p.relative_to(vp.root)).replace(os.sep, "/")
    except Exception:
        return str(p).replace(os.sep, "/")


def editor_cmd() -> List[str]:
    raw = (
        os.environ.get("MEMORY_EDITOR")
        or os.environ.get("VISUAL")
        or os.environ.get("EDITOR")
        or "nvim"
    ).strip()
    cmd = shlex.split(raw) if raw else ["nvim"]
    if not cmd:
        cmd = ["nvim"]
    if shutil.which(cmd[0]) is None:
        raise MemoryError(
            f"Editor not found: {cmd[0]!r}",
            code="NOT_FOUND",
            exit_code=2,
            hint="Install the editor binary or set $MEMORY_EDITOR / $EDITOR.",
            suggestions=["export MEMORY_EDITOR=nvim", "export EDITOR=vim"],
            details={"editor": cmd[0], "raw": raw},
        )
    return cmd


def open_in_editor(path: Path) -> None:
    subprocess.run([*editor_cmd(), str(path)], check=False)


def edit_text_in_editor(*, initial: str = "", suffix: str = ".md") -> str:
    tmp_path: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix="memory-", suffix=suffix, delete=False
        ) as tf:
            tmp_path = Path(tf.name)
            tf.write((initial or "").encode("utf-8", errors="replace"))
            tf.flush()
        open_in_editor(tmp_path)
        return tmp_path.read_text("utf-8", errors="replace")
    finally:
        if tmp_path is not None:
            with contextlib.suppress(Exception):
                tmp_path.unlink()


def _canonicalize_rfc3339_utc(s: str) -> str:
    return canonicalize_rfc3339_utc(s)


def normalize_frontmatter_links(links: Any) -> List[str]:
    if links is None:
        return []
    if isinstance(links, str):
        links = [x for x in links.split(",") if x.strip()]
    if not isinstance(links, list):
        raise ValueError("links must be a list of strings")
    out: List[str] = []
    for x in links:
        if not isinstance(x, str):
            raise ValueError("links must be strings")
        xs = x.strip()
        if xs:
            out.append(xs)
    return out


def normalize_note_frontmatter(
    raw: Dict[str, Any],
    *,
    repo_root: Optional[Path],
    default_visibility: str,
) -> Tuple[Dict[str, Any], List[str]]:
    fm = dict(raw or {})
    warnings: List[str] = []

    note_id = fm.get("id")
    title = fm.get("title")

    if not isinstance(note_id, str) or not note_id.strip():
        raise ValueError("frontmatter: id is required")
    note_id = note_id.strip()
    if not RE_NOTE_ID.match(note_id):
        raise ValueError(
            f"frontmatter: invalid id {note_id!r} (use [A-Za-z0-9][A-Za-z0-9_-]...)"
        )

    if not isinstance(title, str) or not title.strip():
        raise ValueError("frontmatter: title is required")
    title = title.strip()

    created_at = fm.get("created_at")
    updated_at = fm.get("updated_at")

    if not isinstance(created_at, str) or not created_at.strip():
        raise ValueError("frontmatter: created_at is required (RFC3339 UTC)")
    if not isinstance(updated_at, str) or not updated_at.strip():
        raise ValueError("frontmatter: updated_at is required (RFC3339 UTC)")

    created_at_s = _canonicalize_rfc3339_utc(str(created_at))
    updated_at_s = _canonicalize_rfc3339_utc(str(updated_at))

    tags = _validate_tags(fm.get("tags"))
    aliases_val = fm.get("aliases")
    if aliases_val is None:
        aliases: List[str] = []
    elif isinstance(aliases_val, str):
        aliases = [x.strip() for x in aliases_val.split(",") if x.strip()]
    elif isinstance(aliases_val, list) and all(isinstance(x, str) for x in aliases_val):
        aliases = [x.strip() for x in aliases_val if x.strip()]
    else:
        raise ValueError("frontmatter: aliases must be a list of strings")

    visibility = fm.get("visibility")
    if visibility is None or visibility == "":
        visibility = default_visibility
    if not isinstance(visibility, str) or visibility not in VISIBILITIES:
        raise ValueError(f"frontmatter: visibility must be one of {list(VISIBILITIES)}")

    status = fm.get("status")
    if status is None or status == "":
        status = "active"
    if not isinstance(status, str) or status not in STATUSES:
        raise ValueError(f"frontmatter: status must be one of {list(STATUSES)}")

    scopes = normalize_scopes(fm.get("scopes"), repo_root=repo_root)

    links_fm = normalize_frontmatter_links(fm.get("links"))

    fm_vis = str(fm.get("visibility") or default_visibility)
    if fm_vis != default_visibility:
        prefix = (
            "SAFETY: "
            if (default_visibility == "shared" and fm_vis in {"personal", "ephemeral"})
            else ""
        )
        warnings.append(
            prefix
            + f"visibility/path mismatch: frontmatter.visibility={fm_vis!r} but file location implies {default_visibility!r}"
        )

    fm["id"] = note_id
    fm["title"] = title
    fm["created_at"] = created_at_s
    fm["updated_at"] = updated_at_s
    if tags:
        fm["tags"] = tags
    else:
        fm.pop("tags", None)
    if aliases:
        fm["aliases"] = aliases
    else:
        fm.pop("aliases", None)
    if scopes:
        fm["scopes"] = scopes
    else:
        fm.pop("scopes", None)
    if links_fm:
        fm["links"] = links_fm
    else:
        fm.pop("links", None)
    fm["visibility"] = visibility
    fm["status"] = status

    return fm, warnings


def try_read_note_from_path(
    p: Path, *, default_visibility: str, repo_root: Optional[Path]
) -> Tuple[Optional[Note], List[str]]:
    warnings: List[str] = []
    try:
        raw = p.read_text("utf-8", errors="replace")
    except Exception as e:
        return None, [f"unreadable: {e}"]

    try:
        fm_raw, body = split_yaml_frontmatter(raw)
    except Exception as e:
        return None, [f"invalid frontmatter: {e}"]

    if not fm_raw:
        return None, ["missing YAML frontmatter (expected --- at top)"]

    note_id = p.stem
    if "id" in fm_raw and str(fm_raw.get("id") or "").strip() != note_id:
        return None, [
            f"id mismatch: filename stem={note_id!r} frontmatter.id={fm_raw.get('id')!r}"
        ]

    file_mtime = dt.datetime.fromtimestamp(
        p.stat().st_mtime, tz=dt.timezone.utc
    ).replace(microsecond=0)
    file_mtime_iso = file_mtime.isoformat().replace("+00:00", "Z")

    try:
        fm, w = normalize_note_frontmatter(
            fm_raw
            if fm_raw
            else {
                "id": note_id,
                "title": note_id,
                "created_at": file_mtime_iso,
                "updated_at": file_mtime_iso,
            },
            repo_root=repo_root,
            default_visibility=default_visibility,
        )
        warnings.extend(w)
    except Exception as e:
        return None, [f"frontmatter validation failed: {e}"]

    if fm.get("id") != note_id:
        return None, [
            f"id mismatch after normalization: filename stem={note_id!r} frontmatter.id={fm.get('id')!r}"
        ]

    tags = _validate_tags(fm.get("tags"))
    aliases_val = fm.get("aliases") or []
    aliases = (
        [str(x).strip() for x in aliases_val] if isinstance(aliases_val, list) else []
    )
    scopes = fm.get("scopes") or []
    links_fm = normalize_frontmatter_links(fm.get("links"))

    fm_vis = str(fm.get("visibility") or default_visibility)
    effective_visibility = default_visibility
    if fm_vis != default_visibility:
        prefix = (
            "SAFETY: "
            if (default_visibility == "shared" and fm_vis in {"personal", "ephemeral"})
            else ""
        )
        warnings.append(
            prefix
            + f"visibility/path mismatch: frontmatter.visibility={fm_vis!r} but file location implies {default_visibility!r}"
        )

    return (
        Note(
            id=note_id,
            title=str(fm.get("title") or "").strip(),
            body=body,
            tags=tags,
            aliases=aliases,
            scopes=scopes if isinstance(scopes, list) else [],
            links_frontmatter=links_fm,
            visibility=effective_visibility,
            status=str(fm.get("status") or "active"),
            created_at=str(fm.get("created_at") or file_mtime_iso),
            updated_at=str(fm.get("updated_at") or file_mtime_iso),
            frontmatter=fm,
        ),
        warnings,
    )


def read_note(vp: VaultPaths, note_id: str) -> Note:
    repo_root = git_repo_root(Path.cwd())
    p = find_note_path(vp, note_id)
    default_vis = (
        "personal" if str(p).startswith(str(vp.personal_notes_dir)) else "shared"
    )
    if str(p).startswith(str(vp.ephemeral_notes_dir)):
        default_vis = "ephemeral"
    n, warns = try_read_note_from_path(
        p, default_visibility=default_vis, repo_root=repo_root
    )
    if n is None:
        raise ValueError("; ".join(warns) if warns else "failed to read note")
    return n


def generate_note_id(title: str) -> str:
    base = re.sub(r"[^A-Za-z0-9]+", "-", (title or "").strip()).strip("-").lower()
    if not base:
        base = "note"
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d%H%M%S")
    raw = f"{ts}-{base}"[:90].strip("-")
    if not RE_NOTE_ID.match(raw):
        raw = f"{ts}-note"
    h = hashlib.sha1(f"{raw}\n{now_iso()}".encode("utf-8")).hexdigest()[:8]
    out = f"{raw}-{h}"[:128].strip("-")
    if not RE_NOTE_ID.match(out):
        out = f"{ts}-note-{h}"[:128].strip("-")
    return out


def choose_base_dir(vp: VaultPaths, visibility: str) -> Path:
    if visibility == "shared":
        return vp.notes_dir
    if visibility == "personal":
        return vp.personal_notes_dir
    return vp.ephemeral_notes_dir


def write_note_file(
    vp: VaultPaths,
    *,
    note_id: str,
    title: str,
    body: str,
    tags: List[str],
    aliases: List[str],
    scopes: List[Dict[str, Any]],
    visibility: str,
    status: str,
    created_at: str,
    updated_at: str,
    folder: str = "",
    frontmatter_extra: Optional[Dict[str, Any]] = None,
) -> Path:
    if visibility not in VISIBILITIES:
        raise ValueError(f"invalid visibility {visibility!r}")
    if status not in STATUSES:
        raise ValueError(f"invalid status {status!r}")

    base = choose_base_dir(vp, visibility)
    folder = (folder or "").strip().replace("\\", "/").strip("/")
    target_dir = base / folder if folder else base
    safe_mkdir(target_dir)

    p = target_dir / f"{note_id}.md"
    if p.exists():
        raise FileExistsError(str(p))

    fm: Dict[str, Any] = {}
    fm["id"] = note_id
    fm["title"] = title.strip()
    fm["created_at"] = _canonicalize_rfc3339_utc(created_at)
    fm["updated_at"] = _canonicalize_rfc3339_utc(updated_at)
    fm["visibility"] = visibility
    fm["status"] = status
    if tags:
        fm["tags"] = _validate_tags(tags)
    if aliases:
        fm["aliases"] = [a.strip() for a in aliases if a.strip()]
    if scopes:
        fm["scopes"] = scopes
    if frontmatter_extra:
        for k, v in frontmatter_extra.items():
            if v is None:
                continue
            fm[k] = v

    txt = dump_yaml_frontmatter(fm) + (body or "")
    if not txt.endswith("\n"):
        txt += "\n"
    p.write_text(txt, "utf-8")
    return p


def rewrite_note_frontmatter(path: Path, *, new_fm: Dict[str, Any], body: str) -> None:
    txt = dump_yaml_frontmatter(new_fm) + (body or "")
    if not txt.endswith("\n"):
        txt += "\n"
    path.write_text(txt, "utf-8")


def note_content_hash(fm: Dict[str, Any], body: str) -> str:
    return sha256_text(
        json.dumps(fm, sort_keys=True, ensure_ascii=False) + "\n" + (body or "")
    )


def normalize_preview(body: str, max_len: int = 360) -> str:
    b = re.sub(r"\s+", " ", (body or "").strip())
    return (b[: max_len - 3] + "...") if len(b) > max_len else b


__all__ = [
    "Note",
    "VaultPaths",
    "choose_base_dir",
    "edit_text_in_editor",
    "editor_cmd",
    "find_note_path",
    "generate_note_id",
    "git_repo_root",
    "iter_note_paths",
    "normalize_frontmatter_links",
    "normalize_note_frontmatter",
    "normalize_preview",
    "note_content_hash",
    "note_rel_path",
    "open_in_editor",
    "read_note",
    "resolve_vault_root",
    "rewrite_note_frontmatter",
    "try_read_note_from_path",
    "vault_paths",
    "write_note_file",
]
