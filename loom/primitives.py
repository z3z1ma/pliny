"""Primitives: timestamps, frontmatter, workspace root, scanning, indexing."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

CANONICAL_SUBTREES = [
    ".loom/constitution",
    ".loom/research",
    ".loom/initiatives",
    ".loom/specs",
    ".loom/plans",
    ".loom/tickets",
    ".loom/critique",
    ".loom/docs",
]

SUPPORTING_SUBTREES = [
    ".loom/runs",
    ".loom/verification",
]


# ---------------------------------------------------------------------------
# Timestamps and workspace
# ---------------------------------------------------------------------------


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def is_workspace_root(candidate: Path) -> bool:
    return (candidate / ".git").exists() and (candidate / ".loom").exists()


def find_workspace_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if is_workspace_root(candidate):
            return candidate
    if not (current / ".git").exists():
        for ancestor in current.parents:
            if (ancestor / ".git").exists():
                raise SystemExit(
                    "Could not locate Loom workspace root: the current "
                    "working directory is inside a git repository but is "
                    "not itself a repository root"
                )
    return current


def relative_to_workspace(path: Path, workspace: Path) -> str:
    try:
        return str(path.relative_to(workspace))
    except ValueError:
        return str(path)


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------


def parse_frontmatter(text: str) -> tuple[dict, str]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError("Missing opening frontmatter fence")
    closing = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        raise ValueError("Missing closing frontmatter fence")
    frontmatter_text = "\n".join(lines[1:closing]).strip()
    if not frontmatter_text:
        raise ValueError("Empty frontmatter")
    try:
        frontmatter = json.loads(frontmatter_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Frontmatter must be JSON-compatible: {exc}") from exc
    body = "\n".join(lines[closing + 1 :]).lstrip("\n")
    return frontmatter, body


def dump_frontmatter(frontmatter: dict) -> str:
    return json.dumps(frontmatter, indent=2, sort_keys=True)


def render_with_frontmatter(frontmatter: dict, body: str) -> str:
    rendered_body = body.rstrip()
    return f"---\n{dump_frontmatter(frontmatter)}\n---\n\n{rendered_body}\n"


def render_record(frontmatter: dict, sections: list[str]) -> str:
    body = []
    for section in sections:
        body.append(f"# {section}\n\nTBD\n")
    return render_with_frontmatter(frontmatter, "\n".join(body))


def read_record(path: Path) -> tuple[dict, str]:
    return parse_frontmatter(path.read_text())


def extract_headings(body: str) -> set[str]:
    return {
        match.group(1).strip()
        for match in re.finditer(r"^#\s+(.+)$", body, re.MULTILINE)
    }


def parse_timestamp(value: str) -> None:
    datetime.fromisoformat(value.replace("Z", "+00:00"))


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------


def markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if ".git" not in path.parts)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "record"


# ---------------------------------------------------------------------------
# Record scanning and indexing
# ---------------------------------------------------------------------------


def scan_records(workspace: Path, include_runs: bool = False) -> list[Path]:
    roots = [workspace / subtree for subtree in CANONICAL_SUBTREES]
    if include_runs:
        roots.extend([workspace / ".loom/runs", workspace / ".loom/verification"])
    results = []
    for root in roots:
        if root.exists():
            results.extend(markdown_files(root))
    return sorted(set(results))


def flatten_link_values(links: object) -> list[str]:
    refs: list[str] = []
    if not isinstance(links, dict):
        return refs
    for value in links.values():
        if isinstance(value, str):
            refs.append(value)
        elif isinstance(value, list):
            refs.extend(item for item in value if isinstance(item, str))
    return refs


def issue(path: Path | None, workspace: Path, message: str) -> dict:
    return {
        "path": None if path is None else relative_to_workspace(path, workspace),
        "level": "error",
        "message": message,
    }


def build_record_index(workspace: Path) -> tuple[dict[str, Path], list[dict]]:
    index: dict[str, Path] = {}
    issues: list[dict] = []
    for path in scan_records(workspace, include_runs=True):
        try:
            frontmatter, _ = read_record(path)
        except Exception as exc:
            issues.append(issue(path, workspace, f"parse error: {exc}"))
            continue
        record_id = frontmatter.get("id")
        if not isinstance(record_id, str):
            continue
        if record_id in index:
            issues.append(
                issue(
                    path,
                    workspace,
                    f"duplicate id also used by {relative_to_workspace(index[record_id], workspace)}",
                )
            )
        else:
            index[record_id] = path
    return index, issues
