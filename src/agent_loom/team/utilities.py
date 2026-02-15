"""Shared utility functions for team operations."""

from __future__ import annotations
import os
from pathlib import Path
from typing import List, Optional

from agent_loom.core.time import parse_duration_seconds as core_parse_duration_seconds
from agent_loom.team.constants import (
    DEFAULT_HARNESS,
    ENV_TEAM_NAME,
    ENV_TEAM_ROLE,
    ENV_TEAM_RUN_DIR,
    ENV_TEAM_WORKER_ID,
    ROLE_MANAGER,
)
from agent_loom.team.errors import TeamError
from agent_loom.team.exec import _require_bin, _run
from agent_loom.team.run_state import (
    RunPaths,
    discover_repo_root_for_team,
    resolve_run_paths,
)
from agent_loom.team.strings import message_preview, sanitize


def _normalize_harness(value: str) -> str:
    h = str(value or "").strip().lower()
    if h in ("opencode", "claude", "omp", "codex"):
        return h
    return DEFAULT_HARNESS


def _parse_duration_seconds(s: str) -> int:
    """Parse a human-friendly duration string into seconds."""
    try:
        return core_parse_duration_seconds(s)
    except ValueError as e:
        raise TeamError(str(e), code="ARG", exit_code=2) from e


def _message_preview(text: str, *, max_len: int = 100) -> str:
    return message_preview(text, max_len=max_len)


def _git_status_porcelain(*, cwd: Path, pathspec: Optional[str] = None) -> str:
    _require_bin("git")
    argv: List[str] = ["git", "status", "--porcelain"]
    if pathspec:
        argv += ["--", str(pathspec)]
    p = _run(argv, cwd=cwd, timeout=10.0)
    return p.stdout or ""


def _recipient_from_env() -> str:
    role = str(os.getenv(ENV_TEAM_ROLE) or "").strip().lower()
    if role == ROLE_MANAGER:
        return "manager"
    wid = sanitize(str(os.getenv(ENV_TEAM_WORKER_ID) or ""), max_len=48)
    return wid or "unknown"


def _run_paths_from_env() -> Optional[RunPaths]:
    team = sanitize(str(os.getenv(ENV_TEAM_NAME) or ""), max_len=80)
    run_dir_raw = str(os.getenv(ENV_TEAM_RUN_DIR) or "").strip()
    if not team or not run_dir_raw:
        return None
    run_dir = Path(run_dir_raw)
    if not run_dir.is_dir():
        return None
    repo_root: Optional[Path] = None
    try:
        discovered = discover_repo_root_for_team(team, start=run_dir)
        if discovered:
            repo_root = discovered
    except Exception:
        pass
    return resolve_run_paths(team=team, repo=repo_root)


def _paths_for(*, team: str, repo: Optional[Path]) -> RunPaths:
    repo_root = repo.resolve() if repo is not None else None
    return resolve_run_paths(team=team, repo=repo_root)
