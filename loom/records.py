"""Record creation and mutation helpers."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from .primitives import (
    build_record_index,
    flatten_link_values,
    read_record,
    relative_to_workspace,
    render_record,
    render_with_frontmatter,
    slugify,
    utc_now,
)
from .scope import (
    default_repository_scope,
    discover_repositories,
    normalize_repository_scope,
)


# ---------------------------------------------------------------------------
# Ticket filename helpers
# ---------------------------------------------------------------------------


def _git_stdout(repo_root: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    output = result.stdout.strip()
    return output or None


def repository_root_for_scope(workspace: Path, repository_scope: dict | None) -> Path:
    normalized = normalize_repository_scope(workspace, repository_scope)
    if normalized["kind"] != "repository":
        return workspace.resolve()
    repository_id = normalized["repository_id"]
    if repository_id == "repo:root":
        return workspace.resolve()
    for repo in discover_repositories(workspace):
        if repo["repository_id"] != repository_id:
            continue
        return (
            workspace.resolve()
            if repo["path"] == "."
            else (workspace / repo["path"]).resolve()
        )
    return workspace.resolve()


def preferred_remote_url(repo_root: Path) -> str | None:
    origin_url = _git_stdout(repo_root, "remote", "get-url", "origin")
    if origin_url:
        return origin_url
    remotes = _git_stdout(repo_root, "remote")
    if not remotes:
        return None
    for remote_name in remotes.splitlines():
        remote_url = _git_stdout(repo_root, "remote", "get-url", remote_name.strip())
        if remote_url:
            return remote_url
    return None


def repository_name_from_remote(remote_url: str) -> str | None:
    cleaned = remote_url.strip().rstrip("/")
    if not cleaned:
        return None
    if cleaned.endswith(".git"):
        cleaned = cleaned[:-4]
    if "://" not in cleaned and ":" in cleaned:
        cleaned = cleaned.split(":", 1)[1]
    else:
        cleaned = urlparse(cleaned).path.strip("/")
    parts = [part for part in cleaned.split("/") if part and part != "."]
    if not parts:
        return None
    return parts[-1]


def short_repository_slug(value: str) -> str:
    tokens = [token for token in slugify(value).split("-") if token]
    if not tokens:
        return "repo"
    prefix = tokens[0][:3]
    for token in tokens[1:]:
        if len(prefix) >= 8:
            break
        remaining = 8 - len(prefix)
        prefix += token[: min(remaining, 2 if token.isdigit() else 1)]
    return prefix or tokens[0][:6] or "repo"


def ticket_filename_prefix(workspace: Path, repository_scope: dict | None) -> str:
    normalized = normalize_repository_scope(workspace, repository_scope)
    if normalized["kind"] == "workspace":
        return "wksp"
    if normalized["kind"] == "multi_repository":
        return "multi"
    repo_root = repository_root_for_scope(workspace, repository_scope)
    remote_url = preferred_remote_url(repo_root)
    repo_name = repository_name_from_remote(remote_url) if remote_url else None
    return short_repository_slug(repo_name or repo_root.name)


# ---------------------------------------------------------------------------
# ID allocation
# ---------------------------------------------------------------------------


def next_number(workspace: Path, prefix: str, index: dict[str, Path]) -> int:
    pattern = re.compile(rf"^{re.escape(prefix)}:(\d+)$")
    highest = 0
    for record_id in index:
        match = pattern.match(record_id)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def allocate_id(kind: str, slug: str, workspace: Path, index: dict[str, Path]) -> str:
    if kind == "ticket":
        return f"ticket:{next_number(workspace, 'ticket', index):04d}"
    if kind == "decision":
        return f"decision:{next_number(workspace, 'decision', index):04d}"
    return f"{kind}:{slug}"


# ---------------------------------------------------------------------------
# Link helpers
# ---------------------------------------------------------------------------


def normalize_links(links: dict[str, list[str]] | None) -> dict[str, list[str]]:
    if not links:
        return {}
    normalized: dict[str, list[str]] = {}
    for key, values in links.items():
        seen: set[str] = set()
        cleaned: list[str] = []
        for value in values:
            if not isinstance(value, str) or not value or value in seen:
                continue
            cleaned.append(value)
            seen.add(value)
        if cleaned:
            normalized[key] = cleaned
    return normalized


# ---------------------------------------------------------------------------
# Record creation
# ---------------------------------------------------------------------------


def create_record(
    kind: str,
    slug: str,
    workspace: Path,
    title: str | None = None,
    *,
    sections: list[str] | None = None,
    status: str = "active",
    initial_links: dict[str, list[str]] | None = None,
    repository_scope: dict | None = None,
    output_directory: str | None = None,
    record_id: str | None = None,
    file_slug: str | None = None,
) -> Path:
    if not output_directory:
        raise SystemExit(f"output_directory is required for kind: {kind}")
    index, index_issues = build_record_index(workspace)
    if index_issues:
        raise SystemExit(
            "Fix record parse issues before creating records: "
            + "; ".join(i["message"] for i in index_issues[:3])
        )
    final_record_id = record_id or allocate_id(kind, slug, workspace, index)
    timestamp = utc_now()
    final_file_slug = file_slug or slugify(title or slug)
    normalized_links = normalize_links(initial_links)
    link_refs = flatten_link_values(normalized_links)
    broken = [ref for ref in link_refs if ref not in index]
    if broken:
        raise SystemExit(f"Broken links in new record: {', '.join(broken)}")
    normalized_scope = normalize_repository_scope(
        workspace,
        repository_scope or default_repository_scope(workspace),
    )
    if kind == "ticket" and not re.match(
        r"^[a-z0-9][a-z0-9-]*-\d{4}-", final_file_slug
    ):
        number = final_record_id.split(":", 1)[1]
        final_file_slug = (
            f"{ticket_filename_prefix(workspace, normalized_scope)}"
            f"-{number}-{final_file_slug}"
        )
    if final_record_id == "constitution:main" and flatten_link_values(normalized_links):
        raise SystemExit(
            "constitution:main must not declare frontmatter links; it is implicitly authoritative"
        )
    path_root = workspace / output_directory
    path = path_root / f"{final_file_slug}.md"
    frontmatter = {
        "id": final_record_id,
        "kind": kind,
        "schema_version": 1,
        "status": status,
        "repository_scope": normalized_scope,
        "links": normalized_links,
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise SystemExit(
            f"Refusing to overwrite existing record: {relative_to_workspace(path, workspace)}"
        )
    path.write_text(render_record(frontmatter, sections or []))
    return path


# ---------------------------------------------------------------------------
# Record mutation
# ---------------------------------------------------------------------------


def resolve_record_path(
    workspace: Path, target: str, *, include_runs: bool = True
) -> Path:
    candidate = Path(target)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    workspace_candidate = (workspace / target).resolve()
    if workspace_candidate.exists():
        return workspace_candidate
    index, issues = build_record_index(workspace)
    if issues:
        raise SystemExit("Fix record parse issues before mutating records")
    if target not in index:
        area = "record graph including runs" if include_runs else "canonical records"
        raise SystemExit(f"Unknown target in {area}: {target}")
    return index[target]


def write_record(path: Path, frontmatter: dict, body: str) -> None:
    path.write_text(render_with_frontmatter(frontmatter, body))


def _parse_sections(body: str) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_heading: str | None = None
    current_lines: list[str] = []
    for line in body.splitlines():
        if line.startswith("# "):
            if current_heading is not None:
                sections.append((current_heading, current_lines))
            current_heading = line[2:].strip()
            current_lines = []
            continue
        if current_heading is not None:
            current_lines.append(line)
    if current_heading is not None:
        sections.append((current_heading, current_lines))
    return sections


def _render_sections(sections: list[tuple[str, list[str]]]) -> str:
    chunks: list[str] = []
    for heading, lines in sections:
        content = "\n".join(lines).strip()
        if content:
            chunks.append(f"# {heading}\n\n{content}\n")
        else:
            chunks.append(f"# {heading}\n")
    return "\n".join(chunks).rstrip()


def set_sections(workspace: Path, target: str, updates: dict[str, str]) -> Path:
    path = resolve_record_path(workspace, target)
    frontmatter, body = read_record(path)
    sections = _parse_sections(body)
    section_map = {heading: index for index, (heading, _lines) in enumerate(sections)}
    missing = [heading for heading in updates if heading not in section_map]
    if missing:
        raise SystemExit(
            f"Unknown section(s) in {relative_to_workspace(path, workspace)}: {', '.join(missing)}"
        )
    for heading, content in updates.items():
        sections[section_map[heading]] = (heading, content.rstrip().splitlines())
    frontmatter["updated_at"] = utc_now()
    write_record(path, frontmatter, _render_sections(sections))
    return path
