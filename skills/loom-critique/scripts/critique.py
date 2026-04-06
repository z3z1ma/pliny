#!/usr/bin/env python3
# vi: set ft=python :
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

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
    frontmatter = json.loads("\n".join(lines[1:closing]).strip())
    if not isinstance(frontmatter, dict):
        raise ValueError("Frontmatter must be a JSON object")
    body = "\n".join(lines[closing + 1 :]).lstrip("\n")
    return frontmatter, body


def render_markdown(frontmatter: dict, body: str) -> str:
    return f"---\n{json.dumps(frontmatter, indent=2, sort_keys=True)}\n---\n\n{body.rstrip()}\n"


def render_blank_body(sections: list[str]) -> str:
    return "\n".join(f"# {section}\n\nTBD\n" for section in sections)


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


def resolve_scope(args: argparse.Namespace, workspace: Path) -> dict:
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


def parse_links(values: list[str]) -> dict[str, list[str]]:
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


def critique_directory(workspace: Path) -> Path:
    return workspace / ".loom/critique"


def resolve_critique_target(workspace: Path, target: str) -> Path:
    candidate = Path(target)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    workspace_candidate = (workspace / target).resolve()
    if workspace_candidate.exists():
        return workspace_candidate
    expected_id = target if target.startswith("critique:") else f"critique:{target}"
    for path in critique_directory(workspace).glob("*.md"):
        try:
            frontmatter, _body = parse_frontmatter(path.read_text())
        except Exception:
            continue
        if frontmatter.get("id") == expected_id:
            return path
    raise SystemExit(f"Unknown critique target: {target}")


def create_critique(args: argparse.Namespace) -> int:
    workspace = find_workspace_root()
    slug = slugify(args.slug)
    path = critique_directory(workspace) / f"{slug}.md"
    if path.exists():
        raise SystemExit(
            f"Refusing to overwrite existing record: {relative_to_workspace(path, workspace)}"
        )
    frontmatter = {
        "id": f"critique:{slug}",
        "kind": "critique",
        "schema_version": 1,
        "status": args.status or "active",
        "repository_scope": resolve_scope(args, workspace),
        "links": parse_links(args.link),
        "created_at": utc_now(),
        "updated_at": utc_now(),
    }
    body = render_blank_body(
        [
            "Target Under Review",
            "Review Question",
            "Focus Areas",
            "Relevant Context",
            "Evidence Reviewed",
            "Verdict",
            "Residual Risks",
            "Follow-up Tickets",
            "Findings Summary",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(frontmatter, body))
    print(relative_to_workspace(path, workspace))
    return 0


def link_critique(args: argparse.Namespace) -> int:
    if not args.add and not args.remove:
        raise SystemExit("Provide at least one --add or --remove argument")
    workspace = find_workspace_root()
    path = resolve_critique_target(workspace, args.target)
    frontmatter, body = parse_frontmatter(path.read_text())
    links = frontmatter.get("links", {})
    if not isinstance(links, dict):
        links = {}
    normalized: dict[str, list[str]] = {}
    for key, value in links.items():
        if isinstance(value, str):
            normalized[key] = [value]
        elif isinstance(value, list):
            normalized[key] = [item for item in value if isinstance(item, str)]
    for key, values in parse_links(args.add).items():
        normalized.setdefault(key, [])
        for value in values:
            if value not in normalized[key]:
                normalized[key].append(value)
    for key, values in parse_links(args.remove).items():
        if key not in normalized:
            continue
        normalized[key] = [value for value in normalized[key] if value not in values]
        if not normalized[key]:
            normalized.pop(key)
    frontmatter["links"] = normalized
    frontmatter["updated_at"] = utc_now()
    path.write_text(render_markdown(frontmatter, body))
    print(relative_to_workspace(path, workspace))
    return 0


def create_critique_verification(args: argparse.Namespace) -> int:
    workspace = find_workspace_root()
    path = workspace / ".loom/verification" / f"{slugify(args.slug)}.md"
    if path.exists():
        raise SystemExit(
            f"Refusing to overwrite existing record: {relative_to_workspace(path, workspace)}"
        )
    frontmatter = {
        "id": f"verification:{slugify(args.slug)}",
        "kind": "verification",
        "schema_version": 1,
        "status": "recorded",
        "repository_scope": resolve_scope(args, workspace),
        "links": parse_links(args.link),
        "created_at": utc_now(),
        "updated_at": utc_now(),
    }
    body = render_blank_body(
        [
            "Summary",
            "Command",
            "Evidence",
            "Outcome",
            "Related Artifacts",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(frontmatter, body))
    print(relative_to_workspace(path, workspace))
    return 0


def create_critique_packet(args: argparse.Namespace) -> int:
    workspace = find_workspace_root()
    target_id = args.target_ref
    packet_id = f"packet:critique-{slugify(target_id)}-{utc_now().replace(':', '').replace('-', '')}"
    path = (
        Path(args.output)
        if args.output
        else workspace / ".loom/runs/critique" / f"{packet_id.replace(':', '_')}.md"
    )
    if not path.is_absolute():
        path = (workspace / path).resolve()
    frontmatter = {
        "id": packet_id,
        "kind": "packet",
        "schema_version": 1,
        "status": "compiled",
        "mode": {args.mode: True, args.style: True},
        "target": {"kind": "unknown", "ref": target_id},
        "scope": {"kind": "repository", "repository_id": "repo:root"},
        "allowed_write_refs": args.allow_write_ref or [target_id],
        "generated_at": utc_now(),
        "generated_by": "skill:loom-critique",
        "source_refs": ["constitution:main", target_id],
    }
    body = "\n".join(
        [
            "# Objective",
            f"Execute bounded critique work against `{target_id}`.",
            "",
            "# Source Refs",
            "- `constitution:main`",
            f"- `{target_id}`",
            "",
            "# Output Contract",
            "Return outcome status, verification summary, and continue/stop/escalate recommendation.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(frontmatter, body))
    print(relative_to_workspace(path, workspace))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="critique.py", description="Critique CLI")
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create a critique record")
    create_parser.add_argument("slug")
    create_parser.add_argument("--status")
    create_parser.add_argument("--link", action="append", default=[])
    create_parser.add_argument("--path", action="append", default=[])
    create_parser.add_argument("--repository", action="append", default=[])
    create_parser.add_argument("--workspace-scope", action="store_true")
    create_parser.set_defaults(func=create_critique)

    packet_parser = subparsers.add_parser(
        "packet", help="Create a critique packet scaffold"
    )
    packet_parser.add_argument("target_ref")
    packet_parser.add_argument("subsystem", choices=["critique"])
    packet_parser.add_argument(
        "--mode",
        choices=["execution", "review-only", "diagnostic", "reconciliation"],
        default="review-only",
    )
    packet_parser.add_argument(
        "--style", choices=["reference-first", "hermetic"], default="reference-first"
    )
    packet_parser.add_argument("--allow-write-ref", action="append", default=[])
    packet_parser.add_argument("--output")
    packet_parser.set_defaults(func=create_critique_packet)

    link_parser = subparsers.add_parser("link", help="Add or remove critique links")
    link_parser.add_argument("target")
    link_parser.add_argument("--add", action="append", default=[])
    link_parser.add_argument("--remove", action="append", default=[])
    link_parser.set_defaults(func=link_critique)

    verify_parser = subparsers.add_parser(
        "verify", help="Create critique verification evidence"
    )
    verify_parser.add_argument("slug")
    verify_parser.add_argument("--link", action="append", default=[])
    verify_parser.add_argument("--path", action="append", default=[])
    verify_parser.add_argument("--repository", action="append", default=[])
    verify_parser.add_argument("--workspace-scope", action="store_true")
    verify_parser.set_defaults(func=create_critique_verification)

    args = parser.parse_args()
    if args.command == "packet" and args.subsystem != "critique":
        raise SystemExit("This CLI only supports the critique subsystem")
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
