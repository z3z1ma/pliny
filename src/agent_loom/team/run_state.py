from __future__ import annotations

import dataclasses
import datetime as dt
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, Mapping, Optional

from agent_loom.team.constants import (
    CANONICAL_TICKET_DIRNAME,
    DEFAULT_RUNS_DIR,
    DEFAULT_WORKTREES_DIRNAME,
    ENV_TICKET_DIR,
)
from agent_loom.team.errors import TeamError
from agent_loom.team.exec import _require_bin, _run
from agent_loom.team.io import FileLock, _atomic_write_json, _read_json
from agent_loom.team.strings import sanitize
from agent_loom.team.time import _iso_z


def _is_path_within(root: Path, p: Path) -> bool:
    try:
        return p.resolve().is_relative_to(root.resolve())
    except Exception:
        return False


def canonical_repo_root(start: Path) -> Path:
    _require_bin("git")
    cwd = start.expanduser().resolve()
    p = _run(
        ["git", "rev-parse", "--git-common-dir"], cwd=cwd, check=False, timeout=10.0
    )
    out = (p.stdout or "").strip()
    if p.returncode != 0 or not out:
        raise TeamError(
            "Unable to determine canonical repo root (git rev-parse failed).\n"
            f"  cwd: {cwd}\n"
            "Hint: run from the primary checkout root, or pass --repo /path/to/repo. "
            f"Team expects {ENV_TICKET_DIR} to point at the centralized {CANONICAL_TICKET_DIRNAME} dir.",
            code="REPO_ROOT",
            exit_code=2,
        )

    common_dir = Path(out)
    if not common_dir.is_absolute():
        common_dir = (cwd / common_dir).resolve()
    else:
        common_dir = common_dir.resolve()

    for candidate in (common_dir, *common_dir.parents):
        if candidate.name == ".git":
            return candidate.parent.resolve()

    raise TeamError(
        "Unable to determine canonical repo root (unexpected git common dir).\n"
        f"  cwd: {cwd}\n"
        f"  git_common_dir: {common_dir}\n"
        "Hint: run from the primary checkout root, or pass --repo /path/to/repo. "
        f"Team expects {ENV_TICKET_DIR} to point at the centralized {CANONICAL_TICKET_DIRNAME} dir.",
        code="REPO_ROOT",
        exit_code=2,
    )


def discover_repo_root_for_team(team: str, *, start: Path) -> Optional[Path]:
    t = sanitize(team, max_len=80)
    if not t:
        return None

    cur = start.expanduser().resolve()
    while True:
        if (cur / DEFAULT_RUNS_DIR / t / "run.json").exists():
            return cur

        # If invoked from within `.loom/team/...`, return the repo root.
        if cur.name == "team" and cur.parent.name == ".loom":
            if (cur / "runs" / t / "run.json").exists():
                return cur.parent.parent

        if cur.name == ".loom":
            if (cur / "team" / "runs" / t / "run.json").exists():
                return cur.parent

        if cur == cur.parent:
            break
        cur = cur.parent
    return None


def resolve_tickets_dir(*, repo_root: Path) -> Path:
    root = repo_root.resolve()
    tickets_dir = (root / CANONICAL_TICKET_DIRNAME).resolve()
    if not _is_path_within(root, tickets_dir):
        raise TeamError(
            f"Canonical tickets dir must live inside repo root: repo_root={root} tickets_dir={tickets_dir}",
            code="TICKET_DIR",
            exit_code=2,
        )
    tickets_dir.mkdir(parents=True, exist_ok=True)
    return tickets_dir


def tickets_env(tickets_dir: Path) -> Dict[str, str]:
    return {ENV_TICKET_DIR: str(tickets_dir.resolve())}


def default_team_name(root: Path) -> str:
    repo = sanitize(root.name, max_len=24) or "repo"
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{repo}-{stamp}-{uuid.uuid4().hex[:6]}"


@dataclasses.dataclass(frozen=True)
class RunPaths:
    repo_root: Path
    team: str

    @property
    def runs_dir(self) -> Path:
        return self.repo_root / DEFAULT_RUNS_DIR

    @property
    def run_dir(self) -> Path:
        return self.runs_dir / self.team

    @property
    def run_file(self) -> Path:
        return self.run_dir / "run.json"

    @property
    def lock_file(self) -> Path:
        return self.run_dir / "run.json.lock"

    @property
    def worktrees_dir(self) -> Path:
        return self.run_dir / DEFAULT_WORKTREES_DIRNAME

    @property
    def inbox_dir(self) -> Path:
        return self.run_dir / "inbox"

    @property
    def inbox_read_dir(self) -> Path:
        return self.inbox_dir / "read"

    @property
    def events_dir(self) -> Path:
        return self.run_dir / "events"

    @property
    def artifacts_dir(self) -> Path:
        return self.run_dir / "artifacts"

    @property
    def snapshots_dir(self) -> Path:
        return self.run_dir / "snapshots"

    @property
    def status_snapshot_file(self) -> Path:
        return self.snapshots_dir / "status.json"

    @property
    def captures_dir(self) -> Path:
        return self.run_dir / "captures"

    @property
    def merge_dir(self) -> Path:
        return self.run_dir / "merge"

    @property
    def sidecars_dir(self) -> Path:
        return self.run_dir / "sidecars"

    @property
    def health_dir(self) -> Path:
        return self.run_dir / "health"

    @property
    def charter_file(self) -> Path:
        return self.run_dir / "CHARTER.md"


def load_run(paths: RunPaths) -> Dict[str, Any]:
    if not paths.run_file.exists():
        raise TeamError(
            "Run not found.\n"
            f"  team: {paths.team}\n"
            f"  missing: {paths.run_file}\n\n"
            "Hint: start or resume the run with:\n"
            f"  loom team start {paths.team} --repo {paths.repo_root}\n",
            code="NO_RUN",
            exit_code=2,
        )
    data = _read_json(paths.run_file)
    if not isinstance(data, dict):
        raise TeamError(
            f"Invalid run.json: {paths.run_file}", code="BAD_STATE", exit_code=2
        )
    return data


def save_run(paths: RunPaths, run: Dict[str, Any]) -> None:
    run["updated_at"] = _iso_z()
    _atomic_write_json(paths.run_file, run)


@contextmanager
def locked_run(paths: RunPaths, *, save: bool = True) -> Iterator[Dict[str, Any]]:
    with FileLock(paths.lock_file):
        run = load_run(paths)
        try:
            yield run
        finally:
            if save:
                save_run(paths, run)


def run_session(run: Mapping[str, Any]) -> str:
    session = str(run.get("session") or "").strip()
    if not session:
        raise TeamError("run.json missing session", code="BAD_STATE", exit_code=2)
    return session


def run_root(paths: RunPaths, run: Mapping[str, Any]) -> Path:
    return Path(str(run.get("repo_root") or "").strip() or paths.repo_root).resolve()


def ensure_run_tickets_dir(run: Dict[str, Any], *, repo_root: Path) -> Path:
    tickets_dir = resolve_tickets_dir(repo_root=repo_root)
    if str(run.get("tickets_dir") or "") != str(tickets_dir):
        run["tickets_dir"] = str(tickets_dir)
    return tickets_dir


def resolve_run_paths(
    *, team: str, cwd: Optional[Path] = None, repo: Optional[Path] = None
) -> RunPaths:
    if repo is not None:
        root = canonical_repo_root(repo)
    else:
        start = cwd or Path.cwd()
        discovered = discover_repo_root_for_team(team, start=start)
        root = discovered if discovered is not None else canonical_repo_root(start)
    t = sanitize(team, max_len=80)
    if not t:
        raise TeamError("Invalid team name", code="ARG", exit_code=2)
    return RunPaths(repo_root=root, team=t)


def _paths_from_args(args: Any, *, team: Optional[str] = None) -> RunPaths:
    t = team if team is not None else getattr(args, "team", "")
    if not str(t or "").strip():
        raise TeamError("Missing team", code="ARG", exit_code=2)
    repo = Path(args.repo).resolve() if getattr(args, "repo", None) else None
    return resolve_run_paths(team=str(t), repo=repo)


__all__ = [
    "RunPaths",
    "_is_path_within",
    "canonical_repo_root",
    "default_team_name",
    "discover_repo_root_for_team",
    "ensure_run_tickets_dir",
    "load_run",
    "save_run",
    "locked_run",
    "resolve_run_paths",
    "resolve_tickets_dir",
    "run_root",
    "run_session",
    "tickets_env",
    "_paths_from_args",
]
