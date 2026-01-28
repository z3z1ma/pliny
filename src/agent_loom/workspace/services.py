from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

from agent_loom.workspace.constants import BULLET_RE, SERVICE_HEADER
from agent_loom.workspace.state import iter_repos, ws_repos_dir, ws_services_dir
from agent_loom.workspace.utils import atomic_write_json, atomic_write_text, now_iso


def service_md_path(root: Path, ws: dict, name: str) -> Path:
    return root / ws_services_dir(ws) / f"{name}.md"


def service_index_path(root: Path, ws: dict) -> Path:
    return root / ws_services_dir(ws) / "index.json"


def parse_depends_on_from_md(text: str) -> List[str]:
    """
    Extract dependency repo names from the '## Depends on' section bullet list.
    This is intentionally simple and AI-friendly.
    """

    lines = text.splitlines()
    deps: List[str] = []
    in_dep = False
    for line in lines:
        if line.strip().startswith("## "):
            in_dep = line.strip().lower().startswith("## depends on")
            continue
        if in_dep:
            m = BULLET_RE.match(line)
            if m:
                deps.append(m.group(1).strip())
    # normalize unique preserve order
    seen = set()
    out = []
    for d in deps:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out


def normalize_dep_token(s: str) -> str:
    s = s.strip()
    if s.lower().startswith("repo:"):
        s = s.split(":", 1)[1].strip()
    # Allow annotations after whitespace or parentheses.
    s = re.split(r"[\s(]", s, maxsplit=1)[0].strip()
    return s


def ensure_service_files(root: Path, ws: dict, repo_names: List[str]) -> None:
    for name in repo_names:
        p = service_md_path(root, ws, name)
        if not p.exists():
            atomic_write_text(p, SERVICE_HEADER.format(name=name))


def refresh_services_index(root: Path, ws: dict) -> dict:
    """
    Build services/index.json from services/*.md (Depends on section) and workspace inventory.
    Produces forward deps and reverse deps.
    """

    repos = iter_repos(ws)
    names = sorted(repos.keys())

    ensure_service_files(root, ws, names)

    forward: Dict[str, List[str]] = {}
    external: Dict[str, List[str]] = {}
    for name in names:
        md = service_md_path(root, ws, name).read_text(encoding="utf-8")
        raw = parse_depends_on_from_md(md)
        normed = [normalize_dep_token(d) for d in raw]
        normed = [d for d in normed if d and d != name]
        # normalize unique preserve order
        seen = set()
        uniq: List[str] = []
        for d in normed:
            if d not in seen:
                seen.add(d)
                uniq.append(d)
        forward[name] = [d for d in uniq if d in repos]
        external[name] = [d for d in uniq if d not in repos]

    reverse: Dict[str, List[str]] = {n: [] for n in names}
    for src, deps in forward.items():
        for d in deps:
            reverse[d].append(src)

    index = {
        "generated_at": now_iso(),
        "services": {
            n: {
                "depends_on": forward.get(n, []),
                "depends_on_external": external.get(n, []),
                "used_by": reverse.get(n, []),
                "repo_path": str((root / ws_repos_dir(ws) / n).resolve()),
            }
            for n in names
        },
    }
    atomic_write_json(service_index_path(root, ws), index)
    return index
