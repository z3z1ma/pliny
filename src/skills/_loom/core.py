from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

COMMON_FIELDS = [
    "id",
    "kind",
    "schema_version",
    "status",
    "repository_scope",
    "links",
    "created_at",
    "updated_at",
]

WORKSPACE_SCOPE_ID = "workspace:main"

STATUS_BY_KIND = {
    "constitution": {"active", "revised", "superseded"},
    "decision": {"active", "revised", "superseded"},
    "roadmap": {"active", "revised", "superseded"},
    "research": {"active", "revised", "superseded"},
    "initiative": {"active", "revised", "superseded"},
    "spec": {"active", "revised", "superseded"},
    "plan": {"draft", "active", "revised", "retired"},
    "ticket": {
        "proposed",
        "ready",
        "active",
        "blocked",
        "review_required",
        "complete_pending_acceptance",
        "closed",
        "cancelled",
    },
    "critique": {"active", "revised", "superseded"},
    "doc": {"draft", "accepted", "stale", "superseded"},
    "verification": {"recorded", "superseded"},
    "packet": {"compiled", "launched", "superseded", "accepted", "stale", "failed"},
}

SECTIONS_BY_KIND = {
    "constitution": [
        "Vision",
        "Principles",
        "Constraints",
        "Strategic Direction",
        "Current Focus",
        "Open Constitutional Questions",
        "Change History",
    ],
    "decision": [
        "Decision",
        "Why This Decision Exists",
        "Alternatives Considered",
        "Consequences",
        "Supersession",
    ],
    "roadmap": [
        "Strategic Theme",
        "Why Now",
        "Focus Areas",
        "Milestones",
        "Sequencing Assumptions",
        "Downstream Work",
        "Status Summary",
    ],
    "research": [
        "Question",
        "Objective",
        "Scope",
        "Non-goals",
        "Methodology",
        "Hypotheses",
        "Evidence",
        "Experiments",
        "Rejected Paths",
        "Conclusions",
        "Recommendations",
        "Open Questions",
        "Linked Downstream Artifacts",
    ],
    "initiative": [
        "Objective",
        "Why Now",
        "In Scope",
        "Out of Scope",
        "Success Metrics",
        "Milestones",
        "Dependencies",
        "Risks",
        "Linked Specs, Plans, and Tickets",
        "Status Summary",
    ],
    "spec": [
        "Summary",
        "Problem Framing",
        "Desired Behavior",
        "Constraints",
        "Capabilities",
        "Requirements",
        "Scenarios",
        "Acceptance",
        "Design Notes",
        "Open Questions",
    ],
    "plan": [
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
    ],
    "ticket": [
        "Summary",
        "Context",
        "Why This Work Matters Now",
        "Scope",
        "Non-goals",
        "Acceptance Criteria",
        "Implementation Plan",
        "Dependencies",
        "Risks / Edge Cases",
        "Verification",
        "Documentation Disposition",
        "Journal",
    ],
    "critique": [
        "Target Under Review",
        "Review Question",
        "Focus Areas",
        "Relevant Context",
        "Evidence Reviewed",
        "Verdict",
        "Residual Risks",
        "Follow-up Tickets",
        "Findings Summary",
    ],
    "doc": [
        "Overview",
        "Audience",
        "Problem Framing",
        "Accepted System Shape",
        "Workflow / Operations Details",
        "Rationale",
        "Examples",
        "Verification Source",
        "Related Artifacts",
        "Supersession / History",
    ],
    "verification": [
        "Summary",
        "Command",
        "Evidence",
        "Outcome",
        "Related Artifacts",
    ],
    "packet": [
        "Objective",
        "Completion Contract",
        "Constraints and Non-goals",
        "Trust Boundary",
        "Scope and Environment Notes",
        "Source Refs",
        "Embedded Source Material",
        "Current Execution State",
        "Verification Expectations",
        "Stop Rules and Escalation Guidance",
    ],
}

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

KIND_TO_PATH = {
    "constitution": ".loom/constitution",
    "decision": ".loom/constitution/decisions",
    "roadmap": ".loom/constitution/roadmap",
    "research": ".loom/research",
    "initiative": ".loom/initiatives",
    "spec": ".loom/specs",
    "plan": ".loom/plans",
    "ticket": ".loom/tickets",
    "critique": ".loom/critique",
    "doc": ".loom/docs",
    "verification": ".loom/verification",
}


# ---------------------------------------------------------------------------
# Primitives
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


def render_record(frontmatter: dict, kind: str) -> str:
    sections = SECTIONS_BY_KIND.get(kind, [])
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


# ---------------------------------------------------------------------------
# Scope and repository
# ---------------------------------------------------------------------------


def discover_repositories(workspace: Path) -> list[dict]:
    repositories = []
    seen = set()
    for current, dirs, _files in os.walk(workspace):
        current_path = Path(current)
        if ".git" in dirs or (current_path / ".git").is_file():
            rel = current_path.relative_to(workspace)
            repo_id = (
                "repo:root"
                if str(rel) == "."
                else f"repo:{str(rel).replace(os.sep, '-')}"
            )
            if repo_id not in seen:
                repositories.append(
                    {
                        "repository_id": repo_id,
                        "path": "." if str(rel) == "." else str(rel),
                        "worktree_id": f"worktree:{repo_id.split(':', 1)[1]}:default",
                    }
                )
                seen.add(repo_id)
            dirs[:] = [directory for directory in dirs if directory != ".git"]
    repositories.sort(key=lambda item: item["repository_id"])
    return repositories


def repository_ids_by_path(workspace: Path) -> dict[str, dict]:
    return {repo["repository_id"]: repo for repo in discover_repositories(workspace)}


def normalize_repository_scope(workspace: Path, repository_scope: dict | None) -> dict:
    repos = repository_ids_by_path(workspace)
    if not repository_scope:
        return {"kind": "repository", "repository_id": "repo:root"}
    if not isinstance(repository_scope, dict):
        raise SystemExit("repository_scope must be an object")
    kind = repository_scope.get("kind")
    if kind == "repository":
        repository_id = repository_scope.get("repository_id")
        if not isinstance(repository_id, str) or not repository_id:
            raise SystemExit("repository scope requires repository_id")
        if repository_id not in repos:
            raise SystemExit(
                f"unknown repository_id in repository_scope: {repository_id}"
            )
        return {"kind": "repository", "repository_id": repository_id}
    if kind == "workspace":
        workspace_id = repository_scope.get("workspace_id") or WORKSPACE_SCOPE_ID
        if not isinstance(workspace_id, str) or not workspace_id:
            raise SystemExit("workspace scope requires workspace_id")
        return {"kind": "workspace", "workspace_id": workspace_id}
    if kind == "multi_repository":
        repository_ids = repository_scope.get("repository_ids")
        if not isinstance(repository_ids, list):
            raise SystemExit("multi_repository scope requires repository_ids")
        cleaned = sorted(
            {
                repository_id
                for repository_id in repository_ids
                if isinstance(repository_id, str) and repository_id
            }
        )
        if len(cleaned) < 2:
            raise SystemExit(
                "multi_repository scope requires at least two repository_ids"
            )
        unknown = [
            repository_id for repository_id in cleaned if repository_id not in repos
        ]
        if unknown:
            raise SystemExit(
                "unknown repository_ids in repository_scope: " + ", ".join(unknown)
            )
        return {"kind": "multi_repository", "repository_ids": cleaned}
    raise SystemExit(f"unsupported repository_scope kind: {kind!r}")


def repository_ids_for_scope(
    workspace: Path, repository_scope: dict | None
) -> list[str]:
    normalized = normalize_repository_scope(workspace, repository_scope)
    if normalized["kind"] == "repository":
        return [normalized["repository_id"]]
    if normalized["kind"] == "multi_repository":
        return list(normalized["repository_ids"])
    return [repo["repository_id"] for repo in discover_repositories(workspace)]


def merge_repository_scopes(workspace: Path, scopes: list[dict | None]) -> dict | None:
    normalized_scopes = [
        normalize_repository_scope(workspace, scope)
        for scope in scopes
        if scope is not None
    ]
    if not normalized_scopes:
        return None
    if any(scope["kind"] == "workspace" for scope in normalized_scopes):
        return {"kind": "workspace", "workspace_id": WORKSPACE_SCOPE_ID}
    repository_ids = sorted(
        {
            repository_id
            for scope in normalized_scopes
            for repository_id in repository_ids_for_scope(workspace, scope)
        }
    )
    if not repository_ids:
        return None
    all_repository_ids = [
        repo["repository_id"] for repo in discover_repositories(workspace)
    ]
    if repository_ids == all_repository_ids:
        return {"kind": "workspace", "workspace_id": WORKSPACE_SCOPE_ID}
    if len(repository_ids) == 1:
        return {"kind": "repository", "repository_id": repository_ids[0]}
    return {"kind": "multi_repository", "repository_ids": repository_ids}


def default_repository_scope(workspace: Path, start: Path | None = None) -> dict:
    owner = resolve_repository_for_path(workspace, start or Path.cwd())
    return {"kind": "repository", "repository_id": owner["repository_id"]}


def resolve_repository_for_path(workspace: Path, target: Path) -> dict:
    target_path = target if target.is_absolute() else (workspace / target)
    target_path = target_path.resolve()
    candidates = []
    for repo in discover_repositories(workspace):
        repo_path = (
            workspace.resolve()
            if repo["path"] == "."
            else (workspace / repo["path"]).resolve()
        )
        if target_path == repo_path or repo_path in target_path.parents:
            candidates.append((len(repo_path.parts), repo))
    if not candidates:
        raise SystemExit(
            f"No repository owns path: {relative_to_workspace(target_path, workspace)}"
        )
    candidates.sort(key=lambda item: item[0], reverse=True)
    if len(candidates) > 1 and candidates[0][0] == candidates[1][0]:
        raise SystemExit(
            f"Ambiguous repository ownership for path: {relative_to_workspace(target_path, workspace)}"
        )
    return candidates[0][1]


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
# Record creation
# ---------------------------------------------------------------------------


def next_number(workspace: Path, prefix: str) -> int:
    pattern = re.compile(rf"^{re.escape(prefix)}:(\d+)$")
    highest = 0
    index, _issues = build_record_index(workspace)
    for record_id in index:
        match = pattern.match(record_id)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def allocate_id(kind: str, slug: str, workspace: Path) -> str:
    if kind == "ticket":
        return f"ticket:{next_number(workspace, 'ticket'):04d}"
    if kind == "decision":
        return f"decision:{next_number(workspace, 'decision'):04d}"
    return f"{kind}:{slug}"


def default_status(kind: str) -> str:
    return {
        "plan": "draft",
        "doc": "draft",
        "verification": "recorded",
        "packet": "compiled",
    }.get(kind, "active")


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


def create_record(
    kind: str,
    slug: str,
    workspace: Path,
    title: str | None = None,
    *,
    status: str | None = None,
    initial_links: dict[str, list[str]] | None = None,
    repository_scope: dict | None = None,
    output_directory: str | None = None,
    record_id: str | None = None,
    file_slug: str | None = None,
) -> Path:
    if kind not in KIND_TO_PATH:
        raise SystemExit(f"Unsupported kind: {kind}")
    final_record_id = record_id or allocate_id(kind, slug, workspace)
    timestamp = utc_now()
    final_file_slug = file_slug or slugify(title or slug)
    normalized_links = normalize_links(initial_links)
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
    path_root = workspace / (output_directory or KIND_TO_PATH[kind])
    path = path_root / f"{final_file_slug}.md"
    frontmatter = {
        "id": final_record_id,
        "kind": kind,
        "schema_version": 1,
        "status": status or default_status(kind),
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
    path.write_text(render_record(frontmatter, kind))
    return path


# ---------------------------------------------------------------------------
# Record mutation helpers (from records.py)
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


def _load_record(workspace: Path, target: str) -> tuple[Path, dict, str]:
    path = resolve_record_path(workspace, target)
    frontmatter, body = read_record(path)
    return path, frontmatter, body


def set_sections(workspace: Path, target: str, updates: dict[str, str]) -> Path:
    path, frontmatter, body = _load_record(workspace, target)
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
