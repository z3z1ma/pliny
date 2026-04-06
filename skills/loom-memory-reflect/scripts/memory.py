#!/usr/bin/env python3
# vi: set ft=python :
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

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


def find_workspace_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists() and (candidate / ".loom").exists():
            return candidate
    return current


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


def validate_memory_structure(workspace: Path) -> dict:
    manifest = load_memory_manifest(workspace)
    if manifest.get("schema_version") != 1:
        raise SystemExit("Memory manifest schema_version must be 1")
    domains = manifest.get("domains")
    if not isinstance(domains, dict):
        raise SystemExit("Memory manifest domains must be a JSON object")
    actual_domains = tuple(sorted(domains))
    if actual_domains != EXPECTED_DOMAINS:
        raise SystemExit(
            "Memory manifest domains must be exactly system, user; got "
            + (", ".join(actual_domains) or "<none>")
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
        if domain.get("files") != expected_files:
            raise SystemExit(
                f"Memory domain {domain_name} files must be {expected_files}; got {domain.get('files')}"
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
    }


def collect_l0_rows(workspace: Path, domain: str | None = None) -> list[dict[str, str]]:
    root = memory_root(workspace)
    rows = []
    for path in list_memory_markdown_files(workspace):
        relative_path = path.relative_to(root)
        if relative_path.parts[:1] == ("glacier",) and relative_path.name != "index.md":
            continue
        if domain and domain != "all":
            if (
                relative_path.parts[:1] != (domain,)
                and relative_path.as_posix() != "hot-memory.md"
            ):
                continue
        summary = read_l0_summary(path)
        if summary is None:
            continue
        rows.append({"path": str(relative_path), "summary": summary})
    return rows


def run_scan(args: argparse.Namespace) -> int:
    workspace = find_workspace_root()
    rows = collect_l0_rows(workspace, domain=args.domain)
    if args.json:
        print(json.dumps(rows, indent=2, sort_keys=True))
    else:
        for row in rows:
            print(f"{row['path']}: {row['summary']}")
    return 0


def run_validate(args: argparse.Namespace) -> int:
    workspace = find_workspace_root()
    summary = validate_memory_structure(workspace)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        for key, value in summary.items():
            print(f"{key}: {value}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="memory.py", description="Memory reflection CLI"
    )
    subparsers = parser.add_subparsers(dest="command")
    memory_parser = subparsers.add_parser("memory", help="Memory module operations")
    memory_sub = memory_parser.add_subparsers(dest="memory_command")

    scan = memory_sub.add_parser("scan", help="List L0 summaries from memory files")
    scan.add_argument("--domain", choices=["all", *EXPECTED_DOMAINS], default="all")
    scan.add_argument("--json", action="store_true")
    scan.set_defaults(func=run_scan)

    validate = memory_sub.add_parser(
        "validate", help="Validate memory module structure"
    )
    validate.add_argument("--json", action="store_true")
    validate.set_defaults(func=run_validate)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
