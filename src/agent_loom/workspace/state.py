from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List
from urllib.parse import quote, unquote

from agent_loom.workspace.constants import (
    DEFAULT_DEFAULT_BRANCH,
    FS_SAFE,
    REPO_NAME_RE,
    REPOS_DIR,
    SERVICES_DIR,
    STATES_DIR,
    WORKSPACE_FILE,
    WORKTREES_DIR,
)
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.utils import atomic_write_json, read_json


@dataclass
class Repo:
    name: str
    remote: str
    default_branch: str = DEFAULT_DEFAULT_BRANCH
    shallow: bool = False
    depth: int = 1
    repos_dir: str = REPOS_DIR
    tags: List[str] = field(default_factory=list)
    description: str = ""

    @property
    def path(self) -> Path:
        return Path(self.repos_dir) / self.name


def validate_repo_name(name: str) -> None:
    if not REPO_NAME_RE.match(name):
        raise WorkspaceError(
            "Invalid repo name. Use letters/digits plus '._-' only (must not contain '/')."
        )


def fs_escape(name: str) -> str:
    """Reversible encoding for filesystem path segments.

    Git branch names commonly contain '/', which must not be treated as a directory.
    """

    return quote(name, safe=FS_SAFE)


def fs_unescape(seg: str) -> str:
    return unquote(seg)


def worktrees_base(root: Path, ws: dict, group: str) -> Path:
    return root / ws_worktrees_dir(ws) / fs_escape(group)


def snapshot_path(root: Path, ws: dict, name: str) -> Path:
    return root / ws_states_dir(ws) / f"{fs_escape(name)}.json"


def _ws_str(ws: dict, key: str, default: str) -> str:
    v = ws.get(key, default)
    if not isinstance(v, str) or not v.strip():
        raise WorkspaceError(f"workspace.json: '{key}' must be a non-empty string")
    return v.strip()


def ws_repos_dir(ws: dict) -> str:
    return _ws_str(ws, "repos_dir", REPOS_DIR)


def ws_worktrees_dir(ws: dict) -> str:
    return _ws_str(ws, "worktrees_dir", WORKTREES_DIR)


def ws_states_dir(ws: dict) -> str:
    return _ws_str(ws, "states_dir", STATES_DIR)


def ws_services_dir(ws: dict) -> str:
    return _ws_str(ws, "services_dir", SERVICES_DIR)


def default_workspace_json() -> dict:
    return {
        "version": 1,
        "repos_dir": REPOS_DIR,
        "worktrees_dir": WORKTREES_DIR,
        "states_dir": STATES_DIR,
        "services_dir": SERVICES_DIR,
        "repo_sets": {},
        "repos": {
            # "billing": {"remote": "git@github.com:org/billing.git", "default_branch": "main"}
        },
    }


def _is_within_dir(path: Path, root: Path) -> bool:
    root_r = root.resolve()
    path_r = path.resolve()
    return path_r == root_r or root_r in path_r.parents


def _require_rel_dir(root: Path, key: str, rel: str) -> str:
    p = Path(rel)
    if p.is_absolute():
        raise WorkspaceError(
            f"workspace.json: '{key}' must be a relative path (got absolute: {rel})"
        )
    resolved = (root / p).resolve()
    if not _is_within_dir(resolved, root):
        raise WorkspaceError(
            f"workspace.json: '{key}' must be under the workspace root (got: {rel})"
        )
    if resolved == root.resolve():
        raise WorkspaceError(
            f"workspace.json: '{key}' must not be the workspace root (got: {rel})"
        )
    return rel


def validate_workspace(root: Path, data: dict) -> dict:
    if not isinstance(data, dict):
        raise WorkspaceError("workspace.json: must be a JSON object")

    v = data.get("version", 1)
    if v != 1:
        raise WorkspaceError(f"workspace.json: unsupported version: {v} (expected 1)")
    data["version"] = 1

    data.setdefault("repos_dir", REPOS_DIR)
    data.setdefault("worktrees_dir", WORKTREES_DIR)
    data.setdefault("states_dir", STATES_DIR)
    data.setdefault("services_dir", SERVICES_DIR)
    data.setdefault("repo_sets", {})
    data.setdefault("repos", {})

    if not isinstance(data["repos"], dict):
        raise WorkspaceError("workspace.json: 'repos' must be a map/object")
    if not isinstance(data["repo_sets"], dict):
        raise WorkspaceError("workspace.json: 'repo_sets' must be a map/object")
    for set_name, items in data["repo_sets"].items():
        if not isinstance(set_name, str) or not set_name.strip():
            raise WorkspaceError(
                "workspace.json: repo_sets keys must be non-empty strings"
            )
        if not isinstance(items, list) or any(not isinstance(x, str) for x in items):
            raise WorkspaceError(
                f"workspace.json: repo_sets['{set_name}'] must be a list of strings"
            )

    # Validate dirs early so later code can rely on them.
    data["repos_dir"] = _require_rel_dir(root, "repos_dir", ws_repos_dir(data))
    data["worktrees_dir"] = _require_rel_dir(
        root, "worktrees_dir", ws_worktrees_dir(data)
    )
    data["states_dir"] = _require_rel_dir(root, "states_dir", ws_states_dir(data))
    data["services_dir"] = _require_rel_dir(root, "services_dir", ws_services_dir(data))
    return data


def load_workspace(root: Path) -> dict:
    wf = root / WORKSPACE_FILE
    if not wf.exists():
        raise WorkspaceError(
            f"Missing {WORKSPACE_FILE}. Run `loom workspace poly init` first."
        )
    data = read_json(wf)
    return validate_workspace(root, data)


def save_workspace(root: Path, data: dict) -> None:
    validate_workspace(root, data)
    atomic_write_json(root / WORKSPACE_FILE, data)


def iter_repos(ws: dict) -> Dict[str, Repo]:
    out: Dict[str, Repo] = {}
    repos_dir = ws_repos_dir(ws)
    for name, spec in ws["repos"].items():
        validate_repo_name(name)
        if isinstance(spec, str):
            out[name] = Repo(name=name, remote=spec, repos_dir=repos_dir)
            continue

        if not isinstance(spec, dict):
            raise WorkspaceError(
                f"workspace.json: repo '{name}' must be string or object"
            )

        remote = spec.get("remote")
        if not isinstance(remote, str) or not remote.strip():
            raise WorkspaceError(f"workspace.json: repo '{name}' missing remote")

        tags: List[str] = []
        if "tags" in spec:
            raw_tags = spec.get("tags")
            if not isinstance(raw_tags, list) or any(
                not isinstance(t, str) for t in raw_tags
            ):
                raise WorkspaceError(
                    f"workspace.json: repo '{name}' tags must be a list[str]"
                )
            tags = [t.strip() for t in raw_tags if t.strip()]

        description = spec.get("description", "")
        if description is None:
            description = ""
        if not isinstance(description, str):
            raise WorkspaceError(
                f"workspace.json: repo '{name}' description must be a string"
            )

        out[name] = Repo(
            name=name,
            remote=remote.strip(),
            default_branch=spec.get("default_branch", DEFAULT_DEFAULT_BRANCH),
            shallow=bool(spec.get("shallow", False)),
            depth=int(spec.get("depth", 1)),
            repos_dir=repos_dir,
            tags=tags,
            description=description.strip(),
        )

    return out
