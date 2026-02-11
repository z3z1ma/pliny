from __future__ import annotations

import fnmatch
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from agent_loom.memory.constants import (
    RE_TAG,
    SCOPE_KIND_KEY,
    SCOPE_KINDS,
    SCOPE_MATCH_SCORE,
)
from agent_loom.memory.errors import MemoryError
from agent_loom.memory.utils import normcase


def _validate_tags(tags: Any) -> List[str]:
    if tags is None:
        return []
    if isinstance(tags, str):
        tags = [t for t in tags.split(",") if t.strip()]
    if not isinstance(tags, list):
        raise ValueError("tags must be a list of strings")
    out: List[str] = []
    for t in tags:
        if not isinstance(t, str):
            raise ValueError("tags must be strings")
        ts = t.strip()
        if not ts:
            continue
        if ts.startswith("#"):
            ts = ts[1:]
        ts = ts.lower()
        if not RE_TAG.match(ts):
            raise ValueError(f"invalid tag: {t!r} (use letters/numbers/_/-, no spaces)")
        out.append(ts)
    return sorted(set(out))


def _normalize_posix_path(raw: str, *, repo_root: Optional[Path]) -> str:
    s = (raw or "").strip()
    if not s:
        return ""

    s = s.replace("\\", "/")

    if repo_root is not None:
        if re.match(r"^[A-Za-z]:/", s) or s.startswith("/"):
            try:
                p = Path(s).expanduser().resolve()
                rel = p.relative_to(repo_root)
                s = rel.as_posix()
            except Exception:
                pass
        else:
            s = (repo_root / s).resolve().relative_to(repo_root).as_posix()

    return s.lstrip("./")


def _normalize_glob(raw: str, *, repo_root: Optional[Path]) -> str:
    s = (raw or "").strip()
    if not s:
        return ""
    s = s.replace("\\", "/").lstrip("./")
    if repo_root is not None:
        rr = repo_root.as_posix().rstrip("/")
        if s.startswith(rr + "/"):
            s = s[len(rr) + 1 :]
    return s


def _normalize_filetype(raw: str) -> str:
    s = (raw or "").strip().lower()
    if s.startswith("."):
        s = s[1:]
    return s


def _normalize_command(raw: str) -> str:
    return (raw or "").strip()


def _looks_like_glob(raw: str) -> bool:
    s = raw or ""
    return any(ch in s for ch in ("*", "?", "["))


def _normalize_tag_scope(raw: str) -> str:
    s = (raw or "").strip()
    if s.startswith("#"):
        s = s[1:]
    return s.lower()


def _validate_repo_relative_scope_path(
    *, kind: str, raw_val: str, repo_root: Optional[Path]
) -> None:
    if repo_root is None:
        return
    rv = raw_val.replace("\\", "/").strip()
    if not rv.startswith("/"):
        return
    try:
        ap = Path(rv).expanduser().resolve()
    except Exception:
        return
    if repo_root not in ap.parents and ap != repo_root:
        raise ValueError(
            f"scope {kind}: path must be repo-relative (got absolute path outside repo root: {raw_val!r})"
        )


def parse_scope_string(
    item: str,
    *,
    repo_root: Optional[Path],
) -> Optional[Dict[str, Any]]:
    if ":" not in item:
        raise ValueError(
            f"Invalid scope {item!r}. Expected kind:value; valid kinds: {', '.join(SCOPE_KINDS)}"
        )
    kind, value = item.split(":", 1)
    kind = kind.strip()
    raw_val = value.strip()
    if kind not in SCOPE_KINDS:
        return None

    key = SCOPE_KIND_KEY[kind]
    out: Dict[str, Any] = {"kind": kind, "raw": raw_val}

    if kind in ("file", "folder"):
        is_glob_path = _looks_like_glob(raw_val)
        _validate_repo_relative_scope_path(
            kind=kind,
            raw_val=raw_val,
            repo_root=repo_root,
        )
        p = (
            _normalize_glob(raw_val, repo_root=repo_root)
            if is_glob_path
            else _normalize_posix_path(raw_val, repo_root=repo_root)
        )
        if not p:
            raise ValueError(f"scope {kind}: path is empty")
        if kind == "folder" and not is_glob_path and not p.endswith("/"):
            p = p.rstrip("/") + "/"
        out[key] = p
        return out

    if kind == "filetype":
        ext = _normalize_filetype(raw_val)
        if not ext:
            raise ValueError("scope filetype: ext is empty")
        out[key] = ext
        return out

    if kind == "command":
        pat = _normalize_command(raw_val)
        if not pat:
            raise ValueError("scope command: pattern is empty")
        out[key] = pat
        return out

    if kind == "tag":
        t = _normalize_tag_scope(raw_val)
        if not t or not RE_TAG.match(t):
            raise ValueError(
                "scope tag: value must be a valid tag (letters/numbers/_/-)"
            )
        out[key] = t
        return out

    raise ValueError(f"Unhandled scope kind: {kind!r}")


def resolve_scope_path(
    *, scope_path: str, repo_root: Optional[Path], cwd: Path
) -> Path:
    base = repo_root if repo_root is not None else cwd
    sp = (scope_path or "").replace("\\", "/").lstrip("/")
    return (base / Path(sp)).resolve()


def validate_file_scopes_exist(
    scopes: List[Dict[str, Any]],
    *,
    repo_root: Optional[Path],
    cwd: Path,
    allow_missing: bool,
) -> None:
    if allow_missing:
        return
    for s in scopes or []:
        if not isinstance(s, dict) or s.get("kind") != "file":
            continue
        p = s.get("path")
        if not isinstance(p, str) or not p.strip():
            continue
        if _looks_like_glob(p):
            continue
        resolved = resolve_scope_path(scope_path=p, repo_root=repo_root, cwd=cwd)
        if not resolved.exists():
            raise MemoryError(
                f"scope file:{p} does not exist",
                code="NOT_FOUND",
                exit_code=2,
                hint=f"Resolved to {str(resolved)}.",
                suggestions=[
                    "Use folder:<dir>/ if the file is generated or not checked out",
                    "Use file:<pattern> for multiple possible paths",
                    "Or pass --allow-missing-scopes",
                ],
                details={"scope": f"file:{p}", "resolved": str(resolved)},
            )
        if not resolved.is_file():
            raise MemoryError(
                f"scope file:{p} is not a file",
                code="ARG",
                exit_code=2,
                hint=f"Resolved to {str(resolved)}.",
                suggestions=[
                    "Use file:<path> for files",
                    "Use folder:<dir>/ for directories",
                ],
                details={"scope": f"file:{p}", "resolved": str(resolved)},
            )


def normalize_scopes(scopes: Any, *, repo_root: Optional[Path]) -> List[Dict[str, Any]]:
    if scopes is None:
        return []
    if isinstance(scopes, str):
        scopes = [x for x in scopes.split(",") if x.strip()]
    if not isinstance(scopes, list):
        raise ValueError("scopes must be a list")

    out: List[Dict[str, Any]] = []
    for s in scopes:
        if isinstance(s, str):
            parsed = parse_scope_string(s, repo_root=repo_root)
            if parsed is None:
                continue
            out.append(parsed)
            continue
        if not isinstance(s, dict):
            raise ValueError("scopes must contain objects or kind:value strings")

        kind = s.get("kind")
        if kind not in SCOPE_KINDS:
            continue

        raw_val = s.get("raw")
        if not isinstance(raw_val, str) or not raw_val.strip():
            raise ValueError("scope objects must include raw")

        normalized = parse_scope_string(f"{kind}:{raw_val}", repo_root=repo_root)
        if normalized is None:
            continue
        out.append(normalized)

    seen = set()
    deduped: List[Dict[str, Any]] = []
    for s in out:
        sig = json.dumps(s, sort_keys=True, ensure_ascii=False)
        if sig in seen:
            continue
        seen.add(sig)
        deduped.append(s)
    return deduped


def scope_matches_context(
    note_scopes: List[Dict[str, Any]],
    *,
    ctx_scopes: List[Dict[str, Any]],
    and_mode: bool,
) -> Tuple[int, List[Dict[str, Any]]]:
    if not note_scopes:
        return (0, [])

    ctx_paths: List[str] = []
    ctx_cmds: List[str] = []
    ctx_tags: List[str] = []
    ctx_filetypes: List[str] = []

    for c in ctx_scopes:
        if not isinstance(c, dict):
            continue
        k = c.get("kind")
        if k in ("file", "folder"):
            ctx_paths.append(str(c.get("path") or ""))
        elif k == "command":
            ctx_cmds.append(str(c.get("pattern") or ""))
        elif k == "tag":
            ctx_tags.append(str(c.get("tag") or ""))
        elif k == "filetype":
            ctx_filetypes.append(str(c.get("ext") or ""))

    for p in ctx_paths:
        suf = Path(p).suffix.lower().lstrip(".")
        if suf:
            ctx_filetypes.append(suf)

    ctx_paths = [p for p in ctx_paths if p]
    ctx_cmds = [c for c in ctx_cmds if c]
    ctx_tags = [t.lower() for t in ctx_tags if t]
    ctx_filetypes = [e.lower().lstrip(".") for e in ctx_filetypes if e]

    matched: List[Dict[str, Any]] = []
    best = 0

    satisfied_ctx = [False] * len(ctx_scopes) if and_mode else []

    def _mark_ctx_satisfied(idx: int) -> None:
        if and_mode and 0 <= idx < len(satisfied_ctx):
            satisfied_ctx[idx] = True

    def _glob_match(path: str, pattern: str) -> bool:
        p = normcase(path)
        pat = normcase(pattern)
        return fnmatch.fnmatchcase(p, pat)

    def _glob_root(pattern: str) -> str:
        p = (pattern or "").replace("\\", "/")
        wildcards = [i for i, ch in enumerate(p) if ch in ("*", "?", "[")]
        if not wildcards:
            return p
        prefix = p[: min(wildcards)]
        slash = prefix.rfind("/")
        if slash < 0:
            return ""
        return prefix[: slash + 1]

    for s in note_scopes:
        kind = s.get("kind")
        if kind not in SCOPE_KINDS:
            continue

        if kind == "file":
            sp = s.get("path")
            if isinstance(sp, str) and sp:
                sp_is_glob = _looks_like_glob(sp)
                for idx, c in enumerate(ctx_scopes):
                    if c.get("kind") in ("file", "folder"):
                        cp = str(c.get("path") or "")
                        if not cp:
                            continue
                        cp_is_glob = _looks_like_glob(cp)
                        if normcase(sp) == normcase(cp):
                            matched.append(
                                {"note_scope": s, "context": c, "reason": "file exact"}
                            )
                            best = max(best, SCOPE_MATCH_SCORE["file"])
                            _mark_ctx_satisfied(idx)
                        elif cp_is_glob and _glob_match(sp, cp):
                            matched.append(
                                {
                                    "note_scope": s,
                                    "context": c,
                                    "reason": "file matches ctx pattern",
                                }
                            )
                            best = max(best, SCOPE_MATCH_SCORE["file"])
                            _mark_ctx_satisfied(idx)
                        elif sp_is_glob and _glob_match(cp, sp):
                            matched.append(
                                {
                                    "note_scope": s,
                                    "context": c,
                                    "reason": "ctx path matches note file pattern",
                                }
                            )
                            best = max(best, SCOPE_MATCH_SCORE["file"])
                            _mark_ctx_satisfied(idx)
            continue

        if kind == "folder":
            folder = s.get("path")
            if isinstance(folder, str) and folder:
                folder_is_glob = _looks_like_glob(folder)
                folder_norm = folder.rstrip("/") + "/"
                for idx, c in enumerate(ctx_scopes):
                    if c.get("kind") in ("file", "folder"):
                        cp = str(c.get("path") or "")
                        if not cp:
                            continue
                        cp_is_glob = _looks_like_glob(cp)
                        if not folder_is_glob and not cp_is_glob:
                            if normcase(cp) == normcase(folder) or normcase(
                                cp
                            ).startswith(normcase(folder_norm)):
                                matched.append(
                                    {
                                        "note_scope": s,
                                        "context": c,
                                        "reason": "folder prefix",
                                    }
                                )
                                best = max(best, SCOPE_MATCH_SCORE["folder"])
                                _mark_ctx_satisfied(idx)
                        elif folder_is_glob and not cp_is_glob:
                            if _glob_match(cp, folder):
                                matched.append(
                                    {
                                        "note_scope": s,
                                        "context": c,
                                        "reason": "ctx path matches note folder pattern",
                                    }
                                )
                                best = max(best, SCOPE_MATCH_SCORE["folder"])
                                _mark_ctx_satisfied(idx)
                        elif (not folder_is_glob) and cp_is_glob:
                            cp_root = _glob_root(cp)
                            if cp_root and normcase(cp_root).startswith(
                                normcase(folder_norm)
                            ):
                                matched.append(
                                    {
                                        "note_scope": s,
                                        "context": c,
                                        "reason": "folder contains ctx pattern",
                                    }
                                )
                                best = max(best, SCOPE_MATCH_SCORE["folder"])
                                _mark_ctx_satisfied(idx)
                        elif folder_is_glob and cp_is_glob:
                            if normcase(folder) == normcase(cp):
                                matched.append(
                                    {
                                        "note_scope": s,
                                        "context": c,
                                        "reason": "folder pattern eq",
                                    }
                                )
                                best = max(best, SCOPE_MATCH_SCORE["folder"])
                                _mark_ctx_satisfied(idx)
            continue

        if kind == "filetype":
            ext = s.get("ext")
            if isinstance(ext, str) and ext:
                ext_l = ext.lower().lstrip(".")
                for idx, c in enumerate(ctx_scopes):
                    if c.get("kind") == "filetype":
                        if str(c.get("ext") or "").lower().lstrip(".") == ext_l:
                            matched.append(
                                {"note_scope": s, "context": c, "reason": "filetype eq"}
                            )
                            best = max(best, SCOPE_MATCH_SCORE["filetype"])
                            _mark_ctx_satisfied(idx)
                    elif c.get("kind") in ("file", "folder"):
                        cp = str(c.get("path") or "")
                        cp_ext = Path(cp).suffix.lower().lstrip(".")
                        if cp_ext and cp_ext == ext_l:
                            matched.append(
                                {
                                    "note_scope": s,
                                    "context": c,
                                    "reason": "filetype from path",
                                }
                            )
                            best = max(best, SCOPE_MATCH_SCORE["filetype"])
                            _mark_ctx_satisfied(idx)
            continue

        if kind == "command":
            pat = s.get("pattern")
            if isinstance(pat, str) and pat:
                pat_l = pat.casefold()
                for idx, c in enumerate(ctx_scopes):
                    if c.get("kind") == "command":
                        cmd = str(c.get("pattern") or "")
                        if cmd and pat_l in cmd.casefold():
                            matched.append(
                                {
                                    "note_scope": s,
                                    "context": c,
                                    "reason": "command substring",
                                }
                            )
                            best = max(best, SCOPE_MATCH_SCORE["command"])
                            _mark_ctx_satisfied(idx)
            continue

        if kind == "tag":
            tt = s.get("tag")
            if isinstance(tt, str) and tt:
                tt_l = tt.lower()
                for idx, c in enumerate(ctx_scopes):
                    if c.get("kind") == "tag":
                        if str(c.get("tag") or "").lower() == tt_l:
                            matched.append(
                                {"note_scope": s, "context": c, "reason": "tag eq"}
                            )
                            best = max(best, SCOPE_MATCH_SCORE["tag"])
                            _mark_ctx_satisfied(idx)
            continue

    if and_mode and ctx_scopes:
        if not all(satisfied_ctx):
            return (0, matched)

    return (best, matched)


def tag_filter_match(
    note_tags: List[str], *, want: List[str], and_mode: bool
) -> Tuple[bool, List[str]]:
    if not want:
        return True, []
    s = {t.lower() for t in (note_tags or [])}
    want_l = [t.lower() for t in want]
    matched = [t for t in want_l if t in s]
    if and_mode:
        return (len(matched) == len(want_l)), matched
    return (len(matched) > 0), matched


def tag_filter_exclude(
    note_tags: List[str], *, not_tags: List[str]
) -> Tuple[bool, List[str]]:
    if not not_tags:
        return False, []
    s = {t.lower() for t in (note_tags or [])}
    nt = [t.lower() for t in not_tags]
    hit = [t for t in nt if t in s]
    return (len(hit) > 0), hit


__all__ = [
    "_validate_tags",
    "normalize_scopes",
    "parse_scope_string",
    "resolve_scope_path",
    "scope_matches_context",
    "tag_filter_exclude",
    "tag_filter_match",
    "validate_file_scopes_exist",
]
