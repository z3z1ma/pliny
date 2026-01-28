from __future__ import annotations

from typing import Dict, List, Optional, Sequence

from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.state import Repo


def _repos_by_tag(repos: Dict[str, Repo], tag: str) -> List[str]:
    t = tag.strip()
    if not t:
        return []
    return sorted([name for name, r in repos.items() if t in r.tags])


def _expand_repo_set(
    ws: dict, repos: Dict[str, Repo], set_name: str, seen: Optional[set] = None
) -> List[str]:
    if seen is None:
        seen = set()
    if set_name in seen:
        raise WorkspaceError(
            f"workspace.json: repo_sets contains a cycle at '{set_name}'"
        )
    seen.add(set_name)

    sets = ws.get("repo_sets", {})
    items = sets.get(set_name)
    if items is None:
        raise WorkspaceError(f"Unknown repo set: {set_name}")

    try:
        out: List[str] = []
        for raw in items:
            item = raw.strip()
            if not item:
                continue
            if item.startswith("@"):
                out.extend(_expand_repo_set(ws, repos, item[1:], seen=seen))
            elif item.startswith("tag:"):
                out.extend(_repos_by_tag(repos, item.split(":", 1)[1]))
            else:
                out.append(item)
        return out
    finally:
        seen.remove(set_name)


def resolve_repo_names(
    ws: dict,
    repos: Dict[str, Repo],
    repos_args: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
) -> List[str]:
    """Resolve selected repos.

    Selection primitives (union):
    - explicit names via --repos
    - sets via --set or --repos @setname
    - tags via --tag or repo_sets entries like tag:<tag>
    """

    if not repos:
        return []

    selected: List[str] = []
    any_filter = False

    if repos_args:
        any_filter = True
        for token in repos_args:
            for part in str(token).split(","):
                t = part.strip()
                if not t:
                    continue
                if t.startswith("@"):
                    selected.extend(_expand_repo_set(ws, repos, t[1:]))
                else:
                    selected.append(t)

    if sets:
        any_filter = True
        for s in sets:
            for part in str(s).split(","):
                if part and part.strip():
                    selected.extend(_expand_repo_set(ws, repos, part.strip()))

    if tags:
        any_filter = True
        for t in tags:
            for part in str(t).split(","):
                if part and part.strip():
                    selected.extend(_repos_by_tag(repos, part))

    if not any_filter:
        return sorted(repos.keys())

    # Unique + validate; preserve the order implied by user input but stable for repeated expansions.
    seen = set()
    out: List[str] = []
    for name in selected:
        if name in seen:
            continue
        seen.add(name)
        if name not in repos:
            raise WorkspaceError(f"Unknown repo: {name}")
        out.append(name)
    return out


def poly_has_selection(
    *,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
) -> bool:
    return bool(repos or sets or tags or allow_all)


def poly_resolve_repo_names(
    ws: dict,
    repos: Dict[str, Repo],
    *,
    repo_names: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    require_intent_for_multi: bool = False,
    allow_all: bool = False,
) -> List[str]:
    names = resolve_repo_names(ws, repos, repo_names, sets, tags)

    if (
        require_intent_for_multi
        and len(names) > 1
        and not poly_has_selection(
            repos=repo_names, sets=sets, tags=tags, allow_all=allow_all
        )
    ):
        raise WorkspaceError(
            "Refusing to operate on multiple repos without explicit intent. "
            "Pass --all, or select repos via --repos/--set/--tag."
        )

    return names
