from __future__ import annotations

import argparse
import difflib
import json
import os
import select
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Optional, Sequence

from agent_loom.memory.constants import (
    DEFAULT_VAULT_DIR,
    STATUSES,
    SUBSYSTEM_NAME,
    VISIBILITIES,
)
from agent_loom.memory.core import (
    add,
    around,
    edit,
    forget,
    grep,
    init,
    janitor,
    link,
    list_recent,
    open_note,
    prime,
    recall,
    reindex,
    show,
    timeline,
)
from agent_loom.memory.models import (
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
from agent_loom.memory.recall import print_index_warnings
from agent_loom.memory.errors import MemoryError
from agent_loom.memory.utils import emit_error, format_json, read_all_stdin_text
from agent_loom.memory.vault import resolve_vault_root, vault_paths


class ArgParseError(RuntimeError):
    pass


class MemoryArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ArgParseError(message)


_FLAG_ALIASES = {
    "--vault-dir": "--vault",
    "--vault_root": "--vault",
    "--stdout-format": "--format",
}


def _normalize_argv(argv: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(argv):
        tok = argv[i]

        if tok in _FLAG_ALIASES:
            out.append(_FLAG_ALIASES[tok])
            i += 1
            continue

        if tok.startswith(tuple(f + "=" for f in _FLAG_ALIASES)):
            for src, dst in _FLAG_ALIASES.items():
                if tok.startswith(src + "="):
                    out.append(dst + tok[len(src) :])
                    break
            else:
                out.append(tok)
            i += 1
            continue

        # Common format shorthands.
        if tok == "--json":
            out.extend(["--format", "json"])
            i += 1
            continue
        if tok == "--jsonl":
            out.extend(["--format", "jsonl"])
            i += 1
            continue
        if tok in {"--md", "--markdown"}:
            out.extend(["--format", "md"])
            i += 1
            continue
        if tok == "--prompt":
            out.extend(["--format", "prompt"])
            i += 1
            continue

        out.append(tok)
        i += 1

    # Positional fallbacks:
    # memory add <title>  ->  memory add --title <title>
    # memory add <title> <body>  ->  memory add --title <title> --body <body>
    for add_cmd in ("add", "note", "save"):
        if add_cmd not in out:
            continue
        idx = out.index(add_cmd)
        tail = out[idx:]

        # Gather positional tokens immediately after the subcommand (stop at first flag).
        pos: list[str] = []
        j = idx + 1
        while j < len(out):
            tok = out[j]
            if not tok or tok.startswith("-"):
                break
            pos.append(tok)
            j += 1

        has_title = "--title" in tail
        has_body = "--body" in tail

        # Only apply the two-positional shortcut when it is unambiguous.
        if not has_title and pos:
            # Rewrite first positional into --title.
            out = out[: idx + 1] + ["--title", pos[0]] + out[idx + 2 :]

            # If the user provided exactly two positional tokens, treat second as body.
            if not has_body and len(pos) == 2:
                # After inserting --title, the second positional shifts by +1.
                body_idx = idx + 3
                if body_idx < len(out) and out[body_idx] == pos[1]:
                    out = (
                        out[:body_idx] + ["--body", out[body_idx]] + out[body_idx + 1 :]
                    )
        break

    # memory link validate <id>  ->  memory link validate --id <id>
    if len(out) >= 3 and out[0] == "link" and out[1] == "validate":
        if "--id" not in out and out[2] and not out[2].startswith("-"):
            out = ["link", "validate", "--id", out[2]] + out[3:]

    return out


def _infer_error_format(argv: list[str]) -> str:
    # Default: memory defaults to JSON success output, so default errors to JSON too.
    fmt = "json"
    for i, tok in enumerate(argv):
        if tok == "--format" and i + 1 < len(argv):
            cand = str(argv[i + 1] or "").strip().lower()
            if cand in {"json", "jsonl", "text", "md", "prompt"}:
                return cand
        if tok.startswith("--format="):
            cand = tok.split("=", 1)[1].strip().lower()
            if cand in {"json", "jsonl", "text", "md", "prompt"}:
                return cand
    return fmt


def _did_you_mean(value: str, choices: Sequence[str]) -> list[str]:
    v = str(value or "").strip()
    if not v:
        return []
    return difflib.get_close_matches(v, list(choices), n=3, cutoff=0.6)


def _stdin_is_ready() -> bool:
    if sys.stdin.isatty():
        return False
    try:
        r, _w, _x = select.select([sys.stdin], [], [], 0)
        return bool(r)
    except Exception:
        # Likely an in-memory stream (e.g. tests). Assume it's safe to read.
        return True


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


def payload_for(obj: Any, *, fmt: str) -> Any:
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


def build_parser() -> argparse.ArgumentParser:
    p = MemoryArgumentParser(prog=SUBSYSTEM_NAME)

    # Global flags (accepted before the subcommand).
    p.add_argument(
        "--vault",
        default=os.environ.get("MEMORY_VAULT", DEFAULT_VAULT_DIR),
        help="Vault directory (absolute or repo-root-relative when in git). Default: .loom/memory",
    )
    p.add_argument(
        "--format",
        default=None,
        choices=["json", "jsonl", "text", "md", "prompt"],
        help="Output format. Default is json (recall --context defaults to text).",
    )
    p.add_argument(
        "--deterministic",
        action="store_true",
        help="Prefer stable outputs (no recency boost; context pack omits generated_at).",
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce stderr diagnostics (still returns structured output).",
    )

    # Same flags accepted after the subcommand too, without overriding when omitted.
    common_sub = MemoryArgumentParser(add_help=False)
    common_sub.add_argument("--vault", default=argparse.SUPPRESS)
    common_sub.add_argument(
        "--format",
        default=argparse.SUPPRESS,
        choices=["json", "jsonl", "text", "md", "prompt"],
    )
    common_sub.add_argument(
        "--deterministic", action="store_true", default=argparse.SUPPRESS
    )
    common_sub.add_argument("--quiet", action="store_true", default=argparse.SUPPRESS)

    sp = p.add_subparsers(dest="cmd", required=True, parser_class=MemoryArgumentParser)

    sp.add_parser(
        "prime",
        parents=[common_sub],
        help="Print memory cookbook",
    )

    sp.add_parser(
        "init",
        parents=[common_sub],
        help="Initialize vault layout, meta.json, gitignore safety, db cache",
    )

    add_p = sp.add_parser(
        "add",
        parents=[common_sub],
        help="Add a note",
        aliases=["note", "save"],
    )
    add_p.add_argument(
        "--title",
        default=None,
        help="Note title (if omitted, derived from first non-empty body line)",
    )
    add_p.add_argument(
        "--id", default=None, help="Explicit note id (advanced; must be link-safe)"
    )
    add_p.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Tag (repeatable; comma-separated ok)",
    )
    add_p.add_argument(
        "--alias",
        action="append",
        default=[],
        help="Alias (repeatable; comma-separated ok)",
    )
    add_p.add_argument(
        "--link",
        action="append",
        default=[],
        help="Add frontmatter links (repeatable; comma-separated ok)",
    )
    add_p.add_argument(
        "--related",
        action="append",
        default=[],
        help="Append a Related: line with [[wikilinks]] (repeatable; comma ok)",
    )
    add_p.add_argument(
        "--scope", action="append", default=[], help="Scope kind:value (repeatable)"
    )
    add_p.add_argument(
        "--command",
        default=None,
        help="Command context shorthand (adds scope command:...)",
    )
    add_p.add_argument(
        "--visibility",
        choices=VISIBILITIES,
        default="shared",
        help="shared|personal|ephemeral",
    )
    add_p.add_argument(
        "--status", choices=STATUSES, default="active", help="active|deprecated"
    )
    add_p.add_argument(
        "--folder",
        default="",
        help="Subfolder under the visibility root (keeps ids path-independent)",
    )
    add_p.add_argument(
        "--body",
        default=None,
        help="Note body text. If omitted: read stdin when piped.",
    )
    add_p.add_argument(
        "--interactive",
        action="store_true",
        help="Open editor to write body (human path; off the beaten path)",
    )
    add_p.add_argument(
        "--allow-missing-scopes",
        action="store_true",
        help="Allow file: scopes that do not exist on disk",
    )

    edit_p = sp.add_parser(
        "edit",
        parents=[common_sub],
        help="Edit a note by id",
        aliases=["update"],
    )
    edit_p.add_argument("id", help="Note id")
    edit_p.add_argument(
        "--body",
        default=None,
        help="Replace note body text (agent path)",
    )
    edit_p.add_argument(
        "--from-stdin",
        action="store_true",
        help="Replace note body from stdin (strict; prevents accidental overwrites)",
    )
    edit_p.add_argument(
        "--append",
        default=None,
        help="Append text to the note body (agent path)",
    )
    edit_p.add_argument(
        "--append-from-stdin",
        action="store_true",
        help="Append text to the note body from stdin (strict)",
    )
    edit_p.add_argument(
        "--interactive",
        action="store_true",
        help="Open editor to edit the note body (human path)",
    )
    edit_p.add_argument(
        "--allow-missing-scopes",
        action="store_true",
        help="Allow file: scopes that do not exist on disk",
    )
    edit_p.add_argument("--title", default=None, help="Set title")
    edit_p.add_argument("--tag", action="append", default=[], help="Add tag(s)")
    edit_p.add_argument(
        "--remove-tag", action="append", default=[], help="Remove tag(s)"
    )
    edit_p.add_argument("--clear-tags", action="store_true", help="Remove all tags")
    edit_p.add_argument("--alias", action="append", default=[], help="Add alias(es)")
    edit_p.add_argument(
        "--remove-alias", action="append", default=[], help="Remove alias(es)"
    )
    edit_p.add_argument(
        "--clear-aliases", action="store_true", help="Remove all aliases"
    )
    edit_p.add_argument(
        "--link",
        action="append",
        default=[],
        help="Add frontmatter links (repeatable; comma-separated ok)",
    )
    edit_p.add_argument(
        "--remove-link",
        action="append",
        default=[],
        help="Remove frontmatter links (repeatable; comma-separated ok)",
    )
    edit_p.add_argument(
        "--clear-links", action="store_true", help="Remove all frontmatter links"
    )
    edit_p.add_argument(
        "--related",
        action="append",
        default=[],
        help="Append a Related: line with [[wikilinks]] (repeatable; comma ok)",
    )
    edit_p.add_argument(
        "--scope", action="append", default=[], help="Add scope(s) kind:value"
    )
    edit_p.add_argument(
        "--command",
        default=None,
        help="Command context shorthand (adds scope command:...)",
    )
    edit_p.add_argument(
        "--remove-scope",
        action="append",
        default=[],
        help="Remove scope(s) kind:value (exact, normalized)",
    )
    edit_p.add_argument("--clear-scopes", action="store_true", help="Remove all scopes")
    edit_p.add_argument(
        "--visibility",
        choices=VISIBILITIES,
        default=None,
        help="Change visibility (also moves file)",
    )
    edit_p.add_argument(
        "--status", choices=STATUSES, default=None, help="Change status"
    )

    recall_p = sp.add_parser(
        "recall",
        parents=[common_sub],
        help="Recall notes (FTS + filters), default JSON output",
        aliases=["get", "remember"],
    )
    recall_p.add_argument(
        "query", nargs="?", default="", help="Full-text query (FTS5 if available)"
    )
    recall_p.add_argument(
        "--limit", type=int, default=8, help="Max results (default 8)"
    )
    recall_p.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Filter by note tag (repeatable; comma ok)",
    )
    recall_p.add_argument(
        "--not-tag",
        action="append",
        default=[],
        help="Exclude by note tag (repeatable)",
    )
    recall_p.add_argument(
        "--scope",
        action="append",
        default=[],
        help="Context scope kind:value (repeatable)",
    )
    recall_p.add_argument(
        "--not-scope",
        action="append",
        default=[],
        help="Exclude notes matching these context scopes",
    )
    recall_p.add_argument(
        "--command",
        default=None,
        help="Command context (shorthand for --scope command:...)",
    )
    recall_p.add_argument(
        "--visibility",
        action="append",
        choices=VISIBILITIES,
        default=None,
        help="Visibility filter (default: shared+personal)",
    )
    recall_p.add_argument(
        "--include-deprecated", action="store_true", help="Include status=deprecated"
    )
    recall_p.add_argument(
        "--until",
        default=None,
        help="Only notes updated_at <= until (RFC3339 or YYYY-MM-DD)",
    )
    recall_p.add_argument(
        "--or",
        dest="or_mode",
        action="store_true",
        help="Use OR semantics between query tokens (default: AND)",
    )
    recall_p.add_argument(
        "--fts-raw",
        action="store_true",
        help="Treat the query as a raw SQLite FTS expression (advanced)",
    )
    recall_p.add_argument(
        "--since",
        default=None,
        help="Only notes updated_at >= since (RFC3339 or YYYY-MM-DD)",
    )
    recall_p.add_argument(
        "--and",
        dest="and_mode",
        action="store_true",
        help="AND semantics for multiple --tag/--scope",
    )
    recall_p.add_argument(
        "--scoped-only",
        action="store_true",
        help="When context scopes are provided, drop unscoped notes",
    )
    recall_p.add_argument(
        "--full",
        action="store_true",
        help="Include note body (bounded by --max-body-chars)",
    )
    recall_p.add_argument(
        "--max-body-chars",
        type=int,
        default=None,
        help="Max chars of body when included (default 800; default 4000 for --context)",
    )
    recall_p.add_argument(
        "--context",
        action="store_true",
        help="Emit a bounded context pack (string output; requires query or context)",
    )
    recall_p.add_argument(
        "--max-chars",
        type=int,
        default=12000,
        help="Max output chars for --context (default 12000)",
    )
    recall_p.add_argument(
        "--expand",
        type=int,
        default=0,
        help="k-hop graph expansion around hits (adds role=neighbor notes)",
    )
    recall_p.add_argument(
        "--allow-missing-scopes",
        action="store_true",
        help="Allow file: context scopes that do not exist on disk",
    )

    grep_p = sp.add_parser(
        "grep",
        parents=[common_sub],
        help="Regex search notes (literal regex; no ranking)",
    )
    grep_p.add_argument("pattern", help="Python regex pattern")
    grep_p.add_argument("--limit", type=int, default=20, help="Max results")
    grep_p.add_argument(
        "--ignore-case",
        action="store_true",
        help="Case-insensitive regex matching",
    )
    grep_p.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Filter by note tag (repeatable; comma ok)",
    )
    grep_p.add_argument(
        "--not-tag",
        action="append",
        default=[],
        help="Exclude by note tag (repeatable)",
    )
    grep_p.add_argument(
        "--scope",
        action="append",
        default=[],
        help="Context scope kind:value (repeatable)",
    )
    grep_p.add_argument(
        "--not-scope",
        action="append",
        default=[],
        help="Exclude notes matching these context scopes",
    )
    grep_p.add_argument(
        "--command",
        default=None,
        help="Command context (shorthand for --scope command:...)",
    )
    grep_p.add_argument(
        "--visibility",
        action="append",
        choices=VISIBILITIES,
        default=None,
        help="Visibility filter (default: shared+personal)",
    )
    grep_p.add_argument(
        "--include-deprecated", action="store_true", help="Include status=deprecated"
    )
    grep_p.add_argument(
        "--since",
        default=None,
        help="Only notes updated_at >= since (RFC3339 or YYYY-MM-DD)",
    )
    grep_p.add_argument(
        "--until",
        default=None,
        help="Only notes updated_at <= until (RFC3339 or YYYY-MM-DD)",
    )
    grep_p.add_argument(
        "--and",
        dest="and_mode",
        action="store_true",
        help="AND semantics for multiple --tag/--scope",
    )
    grep_p.add_argument(
        "--scoped-only",
        action="store_true",
        help="When context scopes are provided, drop unscoped notes",
    )
    grep_p.add_argument(
        "--allow-missing-scopes",
        action="store_true",
        help="Allow file: context scopes that do not exist on disk",
    )

    list_p = sp.add_parser(
        "list",
        parents=[common_sub],
        help="List recent notes (no query required)",
        aliases=["ls", "recent"],
    )
    list_p.add_argument("--limit", type=int, default=20, help="Max results")
    list_p.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Filter by note tag (repeatable; comma ok)",
    )
    list_p.add_argument(
        "--not-tag",
        action="append",
        default=[],
        help="Exclude by note tag (repeatable)",
    )
    list_p.add_argument(
        "--scope",
        action="append",
        default=[],
        help="Context scope kind:value (repeatable)",
    )
    list_p.add_argument(
        "--not-scope",
        action="append",
        default=[],
        help="Exclude notes matching these context scopes",
    )
    list_p.add_argument(
        "--command",
        default=None,
        help="Command context (shorthand for --scope command:...)",
    )
    list_p.add_argument(
        "--visibility",
        action="append",
        choices=VISIBILITIES,
        default=None,
        help="Visibility filter (default: shared+personal)",
    )
    list_p.add_argument(
        "--include-deprecated", action="store_true", help="Include status=deprecated"
    )
    list_p.add_argument(
        "--since",
        default=None,
        help="Only notes updated_at >= since (RFC3339 or YYYY-MM-DD)",
    )
    list_p.add_argument(
        "--until",
        default=None,
        help="Only notes updated_at <= until (RFC3339 or YYYY-MM-DD)",
    )
    list_p.add_argument(
        "--sort",
        choices=["updated", "created"],
        default="updated",
        help="Sort key (default updated)",
    )
    list_p.add_argument(
        "--allow-missing-scopes",
        action="store_true",
        help="Allow file: context scopes that do not exist on disk",
    )

    show_p = sp.add_parser("show", parents=[common_sub], help="Show a note by id")
    show_p.add_argument("id", help="Note id")
    show_p.add_argument("--meta", action="store_true", help="Show frontmatter only")

    open_p = sp.add_parser("open", parents=[common_sub], help="Open a note in editor")
    open_p.add_argument("id", help="Note id")

    forget_p = sp.add_parser(
        "forget",
        parents=[common_sub],
        help="Forget notes (soft by default; hard delete with --hard)",
        aliases=["archive"],
    )
    forget_p.add_argument(
        "query",
        nargs="?",
        default="",
        help="Optional full-text query (FTS5 if available)",
    )
    forget_p.add_argument("--limit", type=int, default=50, help="Max candidates")
    forget_p.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Filter by note tag (repeatable; comma ok)",
    )
    forget_p.add_argument(
        "--not-tag",
        action="append",
        default=[],
        help="Exclude by note tag (repeatable)",
    )
    forget_p.add_argument(
        "--scope",
        action="append",
        default=[],
        help="Context scope kind:value (repeatable)",
    )
    forget_p.add_argument(
        "--not-scope",
        action="append",
        default=[],
        help="Exclude notes matching these context scopes",
    )
    forget_p.add_argument(
        "--command",
        default=None,
        help="Command context (shorthand for --scope command:...)",
    )
    forget_p.add_argument(
        "--visibility",
        action="append",
        choices=VISIBILITIES,
        default=None,
        help="Visibility filter (default: shared+personal)",
    )
    forget_p.add_argument(
        "--include-deprecated", action="store_true", help="Include status=deprecated"
    )
    forget_p.add_argument(
        "--since",
        default=None,
        help="Only notes updated_at >= since (RFC3339 or YYYY-MM-DD)",
    )
    forget_p.add_argument(
        "--until",
        default=None,
        help="Only notes updated_at <= until (RFC3339 or YYYY-MM-DD)",
    )
    forget_p.add_argument(
        "--or",
        dest="or_mode",
        action="store_true",
        help="Use OR semantics between query tokens (default: AND)",
    )
    forget_p.add_argument(
        "--fts-raw",
        action="store_true",
        help="Treat the query as a raw SQLite FTS expression (advanced)",
    )
    forget_p.add_argument(
        "--apply", action="store_true", help="Apply changes (default is dry-run)"
    )
    forget_p.add_argument(
        "--hard",
        action="store_true",
        help="Hard delete matching notes (requires --apply)",
    )
    forget_p.add_argument(
        "--allow-missing-scopes",
        action="store_true",
        help="Allow file: context scopes that do not exist on disk",
    )

    around_p = sp.add_parser(
        "around",
        parents=[common_sub],
        help="Show notes temporally near a note",
    )
    around_p.add_argument("id", help="Note id")
    around_p.add_argument("--k", type=int, default=12, help="Number of neighbors")
    around_p.add_argument(
        "--by",
        choices=["updated", "created"],
        default="updated",
        help="Which timestamp to use",
    )
    around_p.add_argument(
        "--window-days",
        type=int,
        default=14,
        help="Search window in days around the target timestamp",
    )
    around_p.add_argument(
        "--visibility",
        action="append",
        choices=VISIBILITIES,
        default=None,
        help="Visibility filter (default: shared+personal)",
    )
    around_p.add_argument(
        "--include-deprecated", action="store_true", help="Include status=deprecated"
    )

    timeline_p = sp.add_parser(
        "timeline",
        parents=[common_sub],
        help="Temporal browse of recent notes grouped by day",
    )
    timeline_p.add_argument(
        "--days", type=int, default=30, help="How many days back to include"
    )
    timeline_p.add_argument(
        "--by",
        choices=["updated", "created"],
        default="updated",
        help="Which timestamp to group by",
    )
    timeline_p.add_argument(
        "--visibility",
        action="append",
        choices=VISIBILITIES,
        default=None,
        help="Visibility filter (default: shared+personal)",
    )
    timeline_p.add_argument(
        "--include-deprecated", action="store_true", help="Include status=deprecated"
    )

    link_p = sp.add_parser(
        "link",
        parents=[common_sub],
        help="Link graph utilities (backlinks/neighbors/validate/graph)",
    )
    lsp = link_p.add_subparsers(
        dest="link_cmd", required=True, parser_class=MemoryArgumentParser
    )

    lb = lsp.add_parser(
        "backlinks",
        parents=[common_sub],
        help="Show backlinks (notes that link to <id>)",
    )
    lb.add_argument("id")
    lb.add_argument("--limit", type=int, default=50)

    ln = lsp.add_parser(
        "neighbors",
        parents=[common_sub],
        help="Show neighbors (inbound+outbound), optionally k-hop expansion",
    )
    ln.add_argument("id")
    ln.add_argument(
        "--k", type=int, default=0, help="k-hop expansion (0 => only 1-hop lists)"
    )

    lv = lsp.add_parser(
        "validate", parents=[common_sub], help="List broken links (missing/ambiguous)"
    )
    lv.add_argument(
        "--id", default=None, help="Only validate links originating from this id"
    )
    lv.add_argument("--limit", type=int, default=200)

    lg = lsp.add_parser("graph", parents=[common_sub], help="Export link edge list")
    lg.add_argument(
        "--include-unresolved",
        action="store_true",
        help="Include missing/ambiguous links too",
    )

    ls = lsp.add_parser(
        "suggest",
        parents=[common_sub],
        help="Suggest likely related notes for <id> (non-mutating)",
    )
    ls.add_argument("id")
    ls.add_argument("--limit", type=int, default=12)
    ls.add_argument(
        "--visibility",
        action="append",
        choices=VISIBILITIES,
        default=None,
        help="Visibility filter (default: shared+personal)",
    )
    ls.add_argument(
        "--include-deprecated", action="store_true", help="Include status=deprecated"
    )

    sp.add_parser(
        "reindex",
        parents=[common_sub],
        help="Rebuild derived sqlite index from scratch (safe, deterministic)",
    )

    janitor_p = sp.add_parser(
        "janitor",
        parents=[common_sub],
        help="Clean up stale scopes after files move/delete",
    )
    jsp = janitor_p.add_subparsers(
        dest="janitor_cmd", required=True, parser_class=MemoryArgumentParser
    )

    jr = jsp.add_parser(
        "report",
        parents=[common_sub],
        help="Report file: scopes whose files do not exist",
    )
    jr.add_argument(
        "--visibility",
        action="append",
        choices=VISIBILITIES,
        default=None,
        help="Visibility filter (default: shared)",
    )
    jr.add_argument("--limit", type=int, default=200)

    jf = jsp.add_parser(
        "fix",
        parents=[common_sub],
        help="Remove stale file: scopes (requires --apply)",
    )
    jf.add_argument(
        "--visibility",
        action="append",
        choices=VISIBILITIES,
        default=None,
        help="Visibility filter (default: shared)",
    )
    jf.add_argument("--limit", type=int, default=200)
    jf.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes (otherwise dry-run)",
    )

    return p


def _parse_args(
    argv_list: list[str], *, fmt_for_parse_errors: str
) -> argparse.Namespace | None:
    parser = build_parser()
    try:
        return parser.parse_args(argv_list)
    except ArgParseError as e:
        first = ""
        for tok in argv_list:
            if not tok.startswith("-"):
                first = tok
                break

        cmds: list[str] = []
        try:
            sub = next(
                a
                for a in parser._actions
                if isinstance(a, argparse._SubParsersAction)  # type: ignore[attr-defined]
            )
            cmds = sorted(list(sub.choices.keys()))
        except Exception:
            cmds = []

        suggestions = [f"loom memory {c} -h" for c in _did_you_mean(first, cmds)]
        emit_error(
            code="ARGPARSE",
            error=str(e),
            fmt=fmt_for_parse_errors,
            hint="Run `loom memory -h` or `loom memory <command> -h`.",
            suggestions=suggestions or ["loom memory -h"],
            details={"argv": argv_list},
        )
        return None


def _effective_format(args: argparse.Namespace) -> str:
    if (
        args.format is None
        and args.cmd in {"recall", "get", "remember"}
        and bool(getattr(args, "context", False))
    ):
        return "text"
    if args.format is None and args.cmd in {"list", "ls", "recent"}:
        return "text"
    if args.format is None and args.cmd in {"show", "open"}:
        return "text"
    return args.format or "json"


def _run_with_args(args: argparse.Namespace, *, fmt: str) -> int:
    quiet = bool(getattr(args, "quiet", False))
    vp = vault_paths(resolve_vault_root(str(args.vault), cwd=Path.cwd()))

    if args.cmd == "prime":
        res = prime()
        emit(payload_for(res, fmt=fmt), fmt)
        return 0

    if args.cmd == "init":
        res = init(vault=str(args.vault))
        emit(payload_for(res, fmt=fmt), fmt)
        return 0

    if not vp.root.exists():
        raise MemoryError(
            f"Vault not found at {vp.root}",
            code="NOT_FOUND",
            exit_code=2,
            hint="Initialize a vault or point --vault to an existing one.",
            suggestions=[
                f"loom memory init --vault {vp.root}",
                "export MEMORY_VAULT=.loom/memory",
            ],
            details={"vault": str(vp.root)},
        )

    if not vp.meta_path.exists():
        init(vault=str(args.vault))

    if args.cmd in {"add", "note", "save"}:
        body = args.body
        if body == "-":
            if not _stdin_is_ready():
                raise MemoryError(
                    "--body - requires piped stdin",
                    code="ARG",
                    exit_code=2,
                    hint="Pipe body text into stdin.",
                    suggestions=[
                        "cat file.md | loom memory add --title 'Title' --body -",
                    ],
                )
            body = read_all_stdin_text()
        if body is None and not sys.stdin.isatty():
            body = read_all_stdin_text()

        res = add(
            vault=str(args.vault),
            title=args.title,
            visibility=str(args.visibility or "shared").strip().lower(),
            status=str(args.status or "active").strip().lower(),
            tag=args.tag,
            alias=args.alias,
            link=getattr(args, "link", None),
            related=getattr(args, "related", None),
            scope=args.scope,
            command=args.command,
            allow_missing_scopes=bool(getattr(args, "allow_missing_scopes", False)),
            body=body,
            interactive=bool(args.interactive),
            note_id=args.id,
            folder=args.folder or "",
        )
        emit(payload_for(res, fmt=fmt), fmt)
        return 0

    if args.cmd in {"edit", "update"}:
        if bool(args.from_stdin) and bool(args.append_from_stdin):
            raise MemoryError(
                "edit: cannot combine --from-stdin and --append-from-stdin",
                code="ARG",
                exit_code=2,
                hint="Pick exactly one stdin mode.",
                suggestions=[
                    "cat file.md | loom memory edit <id> --from-stdin",
                    "cat file.md | loom memory edit <id> --append-from-stdin",
                ],
            )

        body_override = args.body
        if body_override == "-":
            if not _stdin_is_ready():
                raise MemoryError(
                    "--body - requires piped stdin",
                    code="ARG",
                    exit_code=2,
                    hint="Pipe body text into stdin.",
                )
            body_override = read_all_stdin_text()
        if bool(args.from_stdin):
            if sys.stdin.isatty():
                raise MemoryError(
                    "edit --from-stdin requires piped stdin",
                    code="ARG",
                    exit_code=2,
                    hint="Pipe content: cat file.md | loom memory edit <id> --from-stdin",
                )
            body_override = read_all_stdin_text()

        body_append = args.append
        if body_append == "-":
            if not _stdin_is_ready():
                raise MemoryError(
                    "--append - requires piped stdin",
                    code="ARG",
                    exit_code=2,
                    hint="Pipe append text into stdin.",
                )
            body_append = read_all_stdin_text()
        if bool(args.append_from_stdin):
            if sys.stdin.isatty():
                raise MemoryError(
                    "edit --append-from-stdin requires piped stdin",
                    code="ARG",
                    exit_code=2,
                    hint="Pipe content: cat file.md | loom memory edit <id> --append-from-stdin",
                )
            body_append = read_all_stdin_text()

        res = edit(
            vault=str(args.vault),
            note_id=args.id,
            title=args.title,
            visibility=(
                str(args.visibility).strip().lower()
                if args.visibility is not None
                else None
            ),
            status=(
                str(args.status).strip().lower() if args.status is not None else None
            ),
            tag=args.tag,
            remove_tag=args.remove_tag,
            clear_tags=bool(args.clear_tags),
            alias=args.alias,
            remove_alias=args.remove_alias,
            clear_aliases=bool(args.clear_aliases),
            link=getattr(args, "link", None),
            remove_link=getattr(args, "remove_link", None),
            clear_links=bool(getattr(args, "clear_links", False)),
            related=getattr(args, "related", None),
            scope=args.scope,
            command=args.command,
            remove_scope=args.remove_scope,
            clear_scopes=bool(args.clear_scopes),
            allow_missing_scopes=bool(getattr(args, "allow_missing_scopes", False)),
            body=body_override,
            append=body_append,
            interactive=bool(args.interactive),
        )
        emit(payload_for(res, fmt=fmt), fmt)
        return 0

    if args.cmd in {"recall", "get", "remember"}:
        res = recall(
            vault=str(args.vault),
            query=args.query or "",
            limit=int(args.limit),
            tag=args.tag,
            not_tag=args.not_tag,
            scope=args.scope,
            not_scope=args.not_scope,
            command=args.command or "",
            visibility=args.visibility,
            include_deprecated=bool(args.include_deprecated),
            since=args.since,
            until=getattr(args, "until", None),
            and_mode=bool(args.and_mode),
            scoped_only=bool(args.scoped_only),
            full=bool(args.full),
            max_body_chars=args.max_body_chars,
            expand=int(args.expand or 0),
            max_chars=int(args.max_chars),
            context=bool(args.context),
            deterministic=bool(getattr(args, "deterministic", False)),
            quiet=quiet,
            allow_missing_scopes=bool(getattr(args, "allow_missing_scopes", False)),
            format=fmt,
            or_mode=bool(getattr(args, "or_mode", False)),
            fts_raw=bool(getattr(args, "fts_raw", False)),
        )
        if not quiet and res.warnings:
            print_index_warnings(list(res.warnings))
        emit(payload_for(res, fmt=fmt), fmt)
        return 0

    if args.cmd in {"list", "ls", "recent"}:
        res = list_recent(
            vault=str(args.vault),
            limit=int(args.limit),
            tag=args.tag,
            not_tag=args.not_tag,
            scope=args.scope,
            not_scope=args.not_scope,
            command=args.command or "",
            visibility=args.visibility,
            include_deprecated=bool(args.include_deprecated),
            since=args.since,
            until=getattr(args, "until", None),
            and_mode=False,
            scoped_only=False,
            deterministic=bool(getattr(args, "deterministic", False)),
            quiet=quiet,
            allow_missing_scopes=bool(getattr(args, "allow_missing_scopes", False)),
            sort=str(getattr(args, "sort", "updated") or "updated"),
        )
        if not quiet and res.warnings:
            print_index_warnings(list(res.warnings))
        emit(payload_for(res, fmt=fmt), fmt)
        return 0

    if args.cmd == "grep":
        payload = grep(
            vault=str(args.vault),
            pattern=str(args.pattern),
            limit=int(args.limit),
            tag=args.tag,
            not_tag=args.not_tag,
            scope=args.scope,
            not_scope=args.not_scope,
            command=args.command or "",
            visibility=args.visibility,
            include_deprecated=bool(args.include_deprecated),
            since=args.since,
            until=getattr(args, "until", None),
            and_mode=bool(getattr(args, "and_mode", False)),
            scoped_only=bool(getattr(args, "scoped_only", False)),
            quiet=quiet,
            allow_missing_scopes=bool(getattr(args, "allow_missing_scopes", False)),
            ignore_case=bool(getattr(args, "ignore_case", False)),
        )
        emit(payload, fmt)
        return 0

    if args.cmd == "show":
        text = show(
            vault=str(args.vault), note_id=str(args.id), meta_only=bool(args.meta)
        )
        emit(text, fmt)
        return 0

    if args.cmd == "open":
        rel = open_note(vault=str(args.vault), note_id=str(args.id))
        emit(rel, fmt)
        return 0

    if args.cmd in {"forget", "archive"}:
        payload = forget(
            vault=str(args.vault),
            query=args.query or "",
            limit=int(args.limit),
            tag=args.tag,
            not_tag=args.not_tag,
            scope=args.scope,
            not_scope=args.not_scope,
            command=args.command or "",
            visibility=args.visibility,
            include_deprecated=bool(args.include_deprecated),
            since=args.since,
            until=getattr(args, "until", None),
            and_mode=False,
            scoped_only=False,
            deterministic=bool(getattr(args, "deterministic", False)),
            quiet=quiet,
            allow_missing_scopes=bool(getattr(args, "allow_missing_scopes", False)),
            or_mode=bool(getattr(args, "or_mode", False)),
            fts_raw=bool(getattr(args, "fts_raw", False)),
            apply=bool(getattr(args, "apply", False)),
            hard=bool(getattr(args, "hard", False)),
        )
        emit(payload, fmt)
        return 0

    if args.cmd == "around":
        payload = around(
            vault=str(args.vault),
            note_id=str(args.id),
            k=int(getattr(args, "k", 12) or 12),
            by=str(getattr(args, "by", "updated") or "updated"),
            window_days=int(getattr(args, "window_days", 14) or 14),
            visibility=args.visibility,
            include_deprecated=bool(getattr(args, "include_deprecated", False)),
            quiet=quiet,
        )
        emit(payload, fmt)
        return 0

    if args.cmd == "timeline":
        payload = timeline(
            vault=str(args.vault),
            days=int(getattr(args, "days", 30) or 30),
            by=str(getattr(args, "by", "updated") or "updated"),
            visibility=args.visibility,
            include_deprecated=bool(getattr(args, "include_deprecated", False)),
            quiet=quiet,
        )
        emit(payload, fmt)
        return 0

    if args.cmd == "reindex":
        res = reindex(vault=str(args.vault), quiet=quiet)
        emit(payload_for(res, fmt=fmt), fmt)
        return 0

    if args.cmd == "janitor":
        res = janitor(
            vault=str(args.vault),
            cmd=args.janitor_cmd,
            visibility=args.visibility,
            limit=int(args.limit),
            apply=bool(getattr(args, "apply", False)),
            quiet=quiet,
        )
        emit(payload_for(res, fmt=fmt), fmt)
        return 0

    if args.cmd == "link":
        res = link(
            vault=str(args.vault),
            cmd=args.link_cmd,
            note_id=getattr(args, "id", ""),
            limit=int(getattr(args, "limit", 200) or 200),
            k=int(getattr(args, "k", 1) or 1),
            include_unresolved=bool(getattr(args, "include_unresolved", False)),
            visibility=getattr(args, "visibility", None),
            include_deprecated=bool(getattr(args, "include_deprecated", False)),
            quiet=quiet,
        )
        if not quiet and res.warnings:
            print_index_warnings(list(res.warnings))
        emit(payload_for(res, fmt=fmt), fmt)
        return 0

    raise MemoryError(
        f"Unknown command: {args.cmd}",
        code="ARG",
        exit_code=2,
        hint="Run `loom memory -h` to see commands.",
        suggestions=["loom memory -h"],
        details={"cmd": str(args.cmd)},
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv_list = list(argv) if argv is not None else sys.argv[1:]
    argv_list = _normalize_argv(argv_list)
    fmt_for_parse_errors = _infer_error_format(argv_list)

    args = _parse_args(argv_list, fmt_for_parse_errors=fmt_for_parse_errors)
    if args is None:
        return 2

    fmt = _effective_format(args)
    if args.format is None:
        args.format = fmt

    try:
        return _run_with_args(args, fmt=fmt)
    except MemoryError as e:
        hint = str(getattr(e, "hint", "") or "")
        if not hint and str(getattr(e, "code", "")) in {"ARG", "ARGPARSE"}:
            hint = "Run `loom memory -h` or `loom memory <command> -h`."
        emit_error(
            code=str(getattr(e, "code", "ERROR")),
            error=str(e),
            fmt=fmt,
            hint=hint,
            suggestions=list(getattr(e, "suggestions", []) or []),
            details=getattr(e, "details", None),
        )
        return int(getattr(e, "exit_code", 1) or 1)
    except FileExistsError as e:
        emit_error(
            code="CONFLICT",
            error=str(e),
            fmt=fmt,
            hint="Choose a different id/folder or remove the existing file.",
        )
        return 2
    except FileNotFoundError as e:
        emit_error(
            code="NOT_FOUND",
            error=str(e),
            fmt=fmt,
            hint="Confirm the id/path, or search with `loom memory recall <query>`.",
        )
        return 2
    except ValueError as e:
        emit_error(
            code="ARG",
            error=str(e),
            fmt=fmt,
            hint="Run `loom memory -h` or `loom memory <command> -h`.",
        )
        return 2
    except Exception as e:
        emit_error(code="ERROR", error=str(e), fmt=fmt)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
