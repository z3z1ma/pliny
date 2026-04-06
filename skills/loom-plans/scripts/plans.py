#!/usr/bin/env python3
# vi: set ft=python :
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

RECORD_KIND = "plan"
RECORD_DIRECTORY = Path(".loom/plans")
DEFAULT_STATUS = "draft"
REQUIRED_SECTIONS = [
    "Purpose / Big Picture",
    "Progress",
    "Surprises & Discoveries",
    "Decision Log",
    "Outcomes & Retrospective",
    "Context and Orientation",
    "Milestones",
    "Plan of Work",
    "Concrete Steps",
    "Validation and Acceptance",
    "Idempotence and Recovery",
    "Artifacts and Notes",
    "Interfaces and Dependencies",
    "Linked Tickets",
    "Risks and Open Questions",
    "Revision Notes",
]
WORKSPACE_SCOPE_ID = "workspace:main"


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def find_workspace_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists() and (candidate / ".loom").exists():
            return candidate
    return current


def relative_to_workspace(path: Path, workspace: Path) -> str:
    try:
        return str(path.relative_to(workspace))
    except ValueError:
        return str(path)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "record"


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
    try:
        frontmatter = json.loads("\n".join(lines[1:closing]).strip())
    except json.JSONDecodeError as exc:
        raise ValueError(f"Frontmatter must be JSON-compatible: {exc}") from exc
    if not isinstance(frontmatter, dict):
        raise ValueError("Frontmatter must be a JSON object")
    body = "\n".join(lines[closing + 1 :]).lstrip("\n")
    return frontmatter, body


def render_record(frontmatter: dict, body: str) -> str:
    return f"---\n{json.dumps(frontmatter, indent=2, sort_keys=True)}\n---\n\n{body.rstrip()}\n"


def render_blank_body() -> str:
    return "\n".join(f"# {section}\n\nTBD\n" for section in REQUIRED_SECTIONS)


def plan_records(workspace: Path) -> list[Path]:
    root = workspace / RECORD_DIRECTORY
    if not root.exists():
        return []
    return sorted(root.glob("*.md"))


def read_plan(path: Path) -> tuple[dict, str]:
    return parse_frontmatter(path.read_text())


def discover_repositories(workspace: Path) -> list[tuple[Path, str]]:
    repositories: list[tuple[Path, str]] = []
    for current, dirs, _files in os.walk(workspace):
        current_path = Path(current)
        if ".git" in dirs or (current_path / ".git").is_file():
            rel = current_path.relative_to(workspace)
            repo_id = (
                "repo:root"
                if str(rel) == "."
                else f"repo:{str(rel).replace(os.sep, '-')}"
            )
            repositories.append((current_path.resolve(), repo_id))
            dirs[:] = [directory for directory in dirs if directory != ".git"]
    repositories.sort(key=lambda item: len(item[0].parts), reverse=True)
    return repositories


def resolve_repository_id_for_path(workspace: Path, target: str) -> str:
    target_path = Path(target)
    if not target_path.is_absolute():
        target_path = (workspace / target_path).resolve()
    for repo_path, repo_id in discover_repositories(workspace):
        if target_path == repo_path or repo_path in target_path.parents:
            return repo_id
    raise SystemExit(
        f"No repository owns path: {relative_to_workspace(target_path, workspace)}"
    )


def resolve_repository_scope(args: argparse.Namespace, workspace: Path) -> dict:
    if args.workspace_scope:
        if args.repository or args.path:
            raise SystemExit(
                "Use either --workspace-scope or --repository/--path, not both"
            )
        return {"kind": "workspace", "workspace_id": WORKSPACE_SCOPE_ID}
    repository_ids = set(args.repository)
    for path in args.path:
        repository_ids.add(resolve_repository_id_for_path(workspace, path))
    if not repository_ids:
        return {"kind": "repository", "repository_id": "repo:root"}
    if len(repository_ids) == 1:
        return {"kind": "repository", "repository_id": next(iter(repository_ids))}
    return {"kind": "multi_repository", "repository_ids": sorted(repository_ids)}


def parse_link_arguments(values: list[str]) -> dict[str, list[str]]:
    links: dict[str, list[str]] = {}
    for value in values:
        if "=" in value:
            key, ref = value.split("=", 1)
        else:
            key = value.split(":", 1)[0]
            ref = value
        key = key.strip()
        ref = ref.strip()
        if not key or not ref:
            raise SystemExit(f"Invalid link argument: {value!r}")
        links.setdefault(key, [])
        if ref not in links[key]:
            links[key].append(ref)
    return links


def resolve_plan_target(workspace: Path, target: str) -> Path:
    candidate = Path(target)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    workspace_candidate = (workspace / target).resolve()
    if workspace_candidate.exists():
        return workspace_candidate
    expected_id = (
        target if target.startswith(f"{RECORD_KIND}:") else f"{RECORD_KIND}:{target}"
    )
    for path in plan_records(workspace):
        frontmatter, _body = read_plan(path)
        if frontmatter.get("id") == expected_id:
            return path
    raise SystemExit(f"Unknown plan target: {target}")


def create_plan(args: argparse.Namespace) -> int:
    workspace = find_workspace_root()
    slug = slugify(args.slug)
    record_path = workspace / RECORD_DIRECTORY / f"{slug}.md"
    if record_path.exists():
        raise SystemExit(
            f"Refusing to overwrite existing record: {relative_to_workspace(record_path, workspace)}"
        )
    frontmatter = {
        "id": f"{RECORD_KIND}:{slug}",
        "kind": RECORD_KIND,
        "schema_version": 1,
        "status": args.status or DEFAULT_STATUS,
        "repository_scope": resolve_repository_scope(args, workspace),
        "links": parse_link_arguments(args.link),
        "created_at": utc_now(),
        "updated_at": utc_now(),
    }
    body = render_blank_body()
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(render_record(frontmatter, body))
    print(relative_to_workspace(record_path, workspace))
    return 0


def link_plan(args: argparse.Namespace) -> int:
    if not args.add and not args.remove:
        raise SystemExit("Provide at least one --add or --remove argument")
    workspace = find_workspace_root()
    record_path = resolve_plan_target(workspace, args.target)
    frontmatter, body = read_plan(record_path)
    links = frontmatter.get("links", {})
    if not isinstance(links, dict):
        links = {}
    normalized: dict[str, list[str]] = {}
    for key, value in links.items():
        if isinstance(value, str):
            normalized[key] = [value]
        elif isinstance(value, list):
            normalized[key] = [item for item in value if isinstance(item, str)]
    for key, values in parse_link_arguments(args.add).items():
        normalized.setdefault(key, [])
        for value in values:
            if value not in normalized[key]:
                normalized[key].append(value)
    for key, values in parse_link_arguments(args.remove).items():
        if key not in normalized:
            continue
        normalized[key] = [value for value in normalized[key] if value not in values]
        if not normalized[key]:
            normalized.pop(key)
    frontmatter["links"] = normalized
    frontmatter["updated_at"] = utc_now()
    record_path.write_text(render_record(frontmatter, body))
    print(relative_to_workspace(record_path, workspace))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="plans.py", description="Plan CLI")
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create a plan record")
    create_parser.add_argument("slug")
    create_parser.add_argument("--status")
    create_parser.add_argument("--link", action="append", default=[])
    create_parser.add_argument("--path", action="append", default=[])
    create_parser.add_argument("--repository", action="append", default=[])
    create_parser.add_argument("--workspace-scope", action="store_true")
    create_parser.set_defaults(func=create_plan)

    link_parser = subparsers.add_parser("link", help="Add or remove plan links")
    link_parser.add_argument("target")
    link_parser.add_argument("--add", action="append", default=[])
    link_parser.add_argument("--remove", action="append", default=[])
    link_parser.set_defaults(func=link_plan)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
