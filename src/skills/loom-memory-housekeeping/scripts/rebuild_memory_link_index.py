#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent))

from _loom.core import find_workspace_root, parse_frontmatter  # noqa: E402

MEMORY_ROOT = Path(".loom/memories")
MANIFEST_PATH = MEMORY_ROOT / "manifest.json"
EXPECTED_DOMAINS = ("system", "user")
DOMAIN_REQUIRED_FILES = {
    "system": [
        "hot-memory.md",
        "patterns.md",
        "self-observations.md",
        "improvements.md",
    ],
    "user": ["hot-memory.md", "observations.md", "entities.md", "action-items.md"],
}
L0_PATTERN = re.compile(r"^<!-- L0: .+ -->$")
WIKI_LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")


def memory_root(workspace: Path) -> Path:
    return workspace / MEMORY_ROOT


def load_memory_manifest(workspace: Path) -> dict:
    manifest_path = workspace / MANIFEST_PATH
    if not manifest_path.exists():
        raise SystemExit(f"Missing memory manifest: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid memory manifest JSON: {exc}") from exc
    if not isinstance(manifest, dict):
        raise SystemExit("Memory manifest must be a JSON object")
    return manifest


def list_memory_markdown_files(workspace: Path) -> list[Path]:
    root = memory_root(workspace)
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def read_l0_summary(path: Path) -> str | None:
    try:
        first_line = path.read_text().splitlines()[0].strip()
    except IndexError:
        return None
    if not L0_PATTERN.match(first_line):
        return None
    return first_line.removeprefix("<!-- L0: ").removesuffix(" -->")


def collect_archive_rows(workspace: Path) -> list[dict[str, str | int]]:
    glacier_root = memory_root(workspace) / "glacier"
    if not glacier_root.exists():
        return []
    rows: list[dict[str, str | int]] = []
    for path in sorted(glacier_root.rglob("*.md")):
        if path.name == "index.md":
            continue
        frontmatter, _ = parse_frontmatter(path.read_text())
        rows.append(
            {
                "path": str(path.relative_to(memory_root(workspace))),
                "domain": str(frontmatter.get("domain", "")),
                "type": str(frontmatter.get("type", "")),
                "tags": ", ".join(frontmatter.get("tags", [])),
                "date_range": str(frontmatter.get("date_range", "")),
                "entries": int(frontmatter.get("entries", 0)),
                "summary": str(frontmatter.get("summary", "")),
            }
        )
    return rows


def validate_memory_structure(workspace: Path) -> dict:
    manifest = load_memory_manifest(workspace)
    if manifest.get("schema_version") != 1:
        raise SystemExit("Memory manifest schema_version must be 1")
    domains = manifest.get("domains")
    if not isinstance(domains, dict):
        raise SystemExit("Memory manifest domains must be a JSON object")
    actual_domains = tuple(sorted(domains))
    if actual_domains != EXPECTED_DOMAINS:
        expected = ", ".join(EXPECTED_DOMAINS)
        actual = ", ".join(actual_domains) or "<none>"
        raise SystemExit(
            f"Memory manifest domains must be exactly {expected}; got {actual}"
        )
    root = memory_root(workspace)
    if not root.exists():
        raise SystemExit(f"Missing memory root: {root}")
    required_paths = [
        root / "hot-memory.md",
        root / "link-index.md",
        root / "glacier/index.md",
    ]
    for domain_name, expected_files in DOMAIN_REQUIRED_FILES.items():
        domain = domains.get(domain_name)
        if not isinstance(domain, dict):
            raise SystemExit(f"Memory domain {domain_name} must be a JSON object")
        if domain.get("path") != domain_name:
            raise SystemExit(
                f"Memory domain {domain_name} must use path '{domain_name}'"
            )
        files = domain.get("files")
        if files != expected_files:
            raise SystemExit(
                f"Memory domain {domain_name} files must be {expected_files}; got {files}"
            )
        required_paths.extend(
            root / domain_name / file_name for file_name in expected_files
        )
    missing = [
        str(path.relative_to(workspace)) for path in required_paths if not path.exists()
    ]
    if missing:
        raise SystemExit(f"Missing required memory files: {', '.join(missing)}")
    regular_files = []
    for path in list_memory_markdown_files(workspace):
        relative_path = path.relative_to(root)
        if relative_path.parts[:1] == ("glacier",) and relative_path.name != "index.md":
            continue
        regular_files.append(path)
    missing_l0 = [
        str(path.relative_to(workspace))
        for path in regular_files
        if read_l0_summary(path) is None
    ]
    if missing_l0:
        raise SystemExit(f"Missing L0 headers in memory files: {', '.join(missing_l0)}")
    return {
        "memory_root": str(root.relative_to(workspace)),
        "domain_count": len(domains),
        "domains": list(EXPECTED_DOMAINS),
        "markdown_file_count": len(list_memory_markdown_files(workspace)),
        "archive_file_count": len(collect_archive_rows(workspace)),
    }


def source_ref_from_path(root: Path, path: Path) -> str:
    relative = path.relative_to(root).as_posix()
    if relative.endswith(".md"):
        relative = relative[:-3]
    return relative


def collect_link_index_rows(workspace: Path) -> list[dict[str, str]]:
    root = memory_root(workspace)
    inbound: dict[str, set[str]] = {}
    for path in list_memory_markdown_files(workspace):
        relative = path.relative_to(root).as_posix()
        if relative.startswith("glacier/"):
            continue
        if relative == "link-index.md":
            continue
        text = path.read_text()
        source = source_ref_from_path(root, path)
        for target in WIKI_LINK_PATTERN.findall(text):
            inbound.setdefault(target, set()).add(source)
    rows = []
    for target in sorted(inbound):
        rows.append(
            {"target": target, "linked_from": ", ".join(sorted(inbound[target]))}
        )
    return rows


def utc_today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def render_index(rows: list[dict[str, str]]) -> str:
    lines = [
        "<!-- L0: Backlink map showing which memory files point to which topics -->",
        "# Memory Link Index",
        "",
        "<!-- Auto-generated by rebuild_memory_link_index.py. Do not edit manually. -->",
        f"<!-- Last updated: {utc_today()} -->",
        "",
        "| Target | Linked from |",
        "|--------|-------------|",
    ]
    if rows:
        for row in rows:
            lines.append(f"| `{row['target']}` | `{row['linked_from']}` |")
    else:
        lines.append("| - | No inbound wiki-links yet. |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    workspace = find_workspace_root()
    validate_memory_structure(workspace)
    output = memory_root(workspace) / "link-index.md"
    rows = collect_link_index_rows(workspace)
    output.write_text(render_index(rows))
    print(output.relative_to(workspace))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
