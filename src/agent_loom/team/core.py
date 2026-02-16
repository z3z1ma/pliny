"""team — tmux-native orchestration for long-horizon, multi-agent software work.

Team is intentionally small and composable.

Authoritative systems:
  - tmux: live execution substrate and observability
  - workspace: git/worktree lifecycle and naming conventions
  - ticket: durable ticket ledger
  - opencode / claude / omp / codex: interactive TUI agents

Team is orchestration only. It does not replace git, tmux, ws, or loom ticket.

Happy-path CLI (human or an outer AI agent):
  - loom team start <team> --objective="..." # create a new team/run
  - loom team attach <team>                  # attach to the manager window
  - loom team disband <team>                 # kill tmux session; worktrees preserved by default

 Manager-facing primitives (called from inside the manager agent pane):
  - loom team spawn <team> <ticket>         # create worktree + spawn worker agent
  - loom team status <team>                 # machine-readable roster + tmux pane metadata
  - loom team send <team> <target> "..."    # send a message via tmux send-keys
  - loom team capture <team> <target>       # capture pane output via tmux capture-pane
   - loom team retire <team> <worker_id>     # kill worker window; worktree stays on disk
   - loom team wait [<team>] <dur>           # manager self-throttle (blocks; wakes early on inbox)
  - loom team inbox <team> list             # disk-backed inbox (durable messages)
    - loom team spawn-integrator <team>       # persistent integrator + worktree (ticketless)
   - loom team merge <team> ...              # merge queue primitives (enqueue/next/done/list)
   - loom team ship <team>                   # merge merge-queue -> target branch (shipping)

Design constraints:
  - Single-file script; no background daemon.
  - State is explicit and inspectable under .loom/team/runs/<team>/run.json
  - Tmux session/window/pane is the source of truth for live state.
  - ws is the exclusive interface for worktree lifecycle.
  - loom ticket is the exclusive interface for durable ticket state.

"""

from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib
import os
import random
import shlex
import shutil
import signal
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

from agent_loom.compound.sync import sync as compound_sync
from agent_loom.core.time import parse_duration_seconds as core_parse_duration_seconds
from agent_loom.pack.core import install_pack as pack_install
from agent_loom.pack.core import update_pack as pack_update
from agent_loom.pack.lock import index_packs as pack_index
from agent_loom.pack.lock import load_lock as pack_load_lock
from agent_loom.team.channels import channel_for, resolve_team_from_session
from agent_loom.team.communication_policy import (
    communication_policy_from_run,
    delivery_suggestions,
    resolve_send_target,
    route_allows_target,
    sender_for_send,
)
from agent_loom.team.composition import load_team_roster_yaml
from agent_loom.team.composition_runtime import (
    ResolvedMemberProfile,
    enforce_member_lifecycle,
    list_always_on_member_profiles,
    resolve_builtin_profile,
    resolve_member_profile,
)
from agent_loom.team.constants import (
    CANONICAL_TICKET_DIRNAME,
    CONTROL_OP_BOUNCE,
    DEFAULT_ARCHITECT_AGENT,
    DEFAULT_AUTOCAPTURE_LINES,
    DEFAULT_AUTOCAPTURE_MAX_S,
    DEFAULT_AUTOCAPTURE_MIN_S,
    DEFAULT_DISBAND_REMINDER_RESEND_S,
    DEFAULT_DONE_CHECK_S,
    DEFAULT_HARNESS,
    DEFAULT_IDLE_SCREEN_S,
    DEFAULT_INTEGRATOR_AGENT,
    DEFAULT_MANAGER_AGENT,
    DEFAULT_MANAGER_WINDOW,
    DEFAULT_OBJECTIVE_NUDGE_S,
    DEFAULT_TMUX_SESSION_PREFIX,
    DEFAULT_WORKER_AGENT,
    ENV_TEAM_NAME,
    ENV_TEAM_ROLE,
    ENV_TEAM_RUN_DIR,
    ENV_TEAM_RUN_ID,
    ENV_TEAM_SPRINT_NAME,
    ENV_TEAM_SPRINT_TAG,
    ENV_TEAM_TICKET_ID,
    ENV_TEAM_WORKER_ID,
    ENV_TICKET_DIR,
    INBOX_KIND_CONTROL,
    ROLE_ARCHITECT,
    ROLE_INTEGRATOR,
    ROLE_MANAGER,
    ROLE_WORKER,
    TMUX_OPT_OWNED,
    TMUX_OPT_REPO_ROOT,
    TMUX_OPT_RUN_DIR,
    TMUX_OPT_RUN_ID,
    TMUX_OPT_TEAM,
)
from agent_loom.team.errors import TeamError
from agent_loom.team.events import (
    _event_stamp,
    best_effort,
    safe_write_event,
    write_event,
)
from agent_loom.team.exec import _require_bin, _run
from agent_loom.team.inbox import (
    _inbox_msg_path,
    _inbox_unacked,
    _inbox_write_and_maybe_nudge,
    inbox_ack_message,
    inbox_list_messages,
    inbox_write_message,
)
from agent_loom.team.io import (
    FileLock,
    _atomic_write_json,
    _atomic_write_text,
    _read_json,
)
from agent_loom.team.merge_queue import (
    _merge_state,
    merge_branch_for_run,
    merge_claim_next,
    merge_enqueue_item,
    merge_list_items,
    merge_mark_done,
)
from agent_loom.team.models import (
    AttachResult,
    BounceResult,
    CaptureResult,
    DisbandResult,
    DoctorResult,
    DoneResult,
    InboxAckResult,
    InboxListResult,
    InboxSendResult,
    InboxShowResult,
    InitAgentsResult,
    JanitorResult,
    MarkRetirableResult,
    MergeDoneResult,
    MergeEnqueueResult,
    MergeListResult,
    MergeNextResult,
    ObjectiveShowResult,
    ObjectiveUpdateResult,
    PauseResult,
    PrepSprintResult,
    ResumeTeamResult,
    RetireResult,
    SendResult,
    ShipResult,
    SpawnIntegratorResult,
    SpawnPersonaResult,
    SpawnResult,
    SprintClearResult,
    SprintSetResult,
    SprintShowResult,
    StartResult,
    StatusResult,
    TuiResult,
    WaitResult,
)
from agent_loom.team.objective_state import (
    apply_objective_mutation as _objective_state_apply_objective_mutation,
    build_prep_sprint_ticket_description as _build_prep_sprint_ticket_description,
    clear_sprint_state as _objective_state_clear_sprint_state,
    objective_show as _objective_state_objective_show,
    read_text_input as _objective_state_read_text_input,
    set_sprint_state as _objective_state_set_sprint_state,
    sprint_state as _objective_state_sprint_state,
    start_sprint_state as _objective_state_start_sprint_state,
)
from agent_loom.team.permissions import (
    _deny_if_role_set,
    _require_role,
    _require_self_worker_id,
)
from agent_loom.team.prompts import (
    render_architect_prompt,
    render_integrator_prompt,
    render_manager_prompt,
    render_persona_prompt,
    render_worker_prompt,
)
from agent_loom.team.run_state import (
    RunPaths,
    _is_path_within,
    canonical_repo_root,
    default_team_name,
    discover_repo_root_for_team,
    ensure_run_tickets_dir,
    load_run,
    locked_run,
    resolve_run_paths,
    resolve_tickets_dir,
    run_root,
    run_session,
    save_run,
)
from agent_loom.team.strings import generate_stable_key, message_preview, sanitize
from agent_loom.team.targets import _resolve_target, _resolve_targets
from agent_loom.team.time import _iso_z
from agent_loom.team.tmux import (
    _pane_can_receive_chat,
    tmux_available,
    tmux_capture,
    tmux_cmd,
    tmux_env_flags,
    tmux_format,
    tmux_get_option,
    tmux_has_session,
    tmux_kill_session,
    tmux_kill_window,
    tmux_list_panes,
    tmux_mark_pane,
    tmux_new_window,
    tmux_select_window,
    tmux_send_text,
    tmux_set_option,
    tmux_signal,
    tmux_unique_window_name,
    tmux_wait_for,
    tmux_window_exists,
)
from agent_loom.ticket.api import create as ticket_create
from agent_loom.ticket.api import sprint_clear as ticket_sprint_clear
from agent_loom.ticket.api import sprint_set as ticket_sprint_set
from agent_loom.ticket.api import show as ticket_show
from agent_loom.ticket.api import sync as ticket_sync
from agent_loom.workspace.core import (
    repo_merge_attempt,
    repo_worktree_ensure,
    repo_worktree_prune,
    repo_worktree_rm,
    repo_worktree_rm_path,
)
from agent_loom.workspace.errors import WorkspaceError

__all__ = [
    "init_agents",
    "attach",
    "bounce",
    "capture",
    "disband",
    "pause_team",
    "resume_team",
    "doctor",
    "done",
    "inbox_ack",
    "inbox_list",
    "inbox_send",
    "inbox_show",
    "janitor",
    "mark_retirable",
    "merge_done",
    "merge_enqueue",
    "merge_list",
    "merge_next",
    "prep_sprint",
    "sprint_show",
    "sprint_set",
    "sprint_clear",
    "objective_append",
    "objective_set",
    "objective_show",
    "retire",
    "send",
    "ship",
    "spawn",
    "spawn_integrator",
    "resume_worker",
    "start",
    "status",
    "tui",
    "wait",
]


def _normalize_harness(value: str) -> str:
    h = str(value or "").strip().lower()
    if h in ("opencode", "claude", "omp", "codex"):
        return h
    return DEFAULT_HARNESS


# -----------------------------
# ws / loom ticket
# -----------------------------


def _git_status_porcelain(*, cwd: Path, pathspec: Optional[str] = None) -> str:
    _require_bin("git")
    argv: List[str] = ["git", "status", "--porcelain"]
    if pathspec:
        argv += ["--", str(pathspec)]
    p = _run(argv, cwd=cwd, timeout=10.0)
    return p.stdout or ""


def _ensure_tickets_synced(*, cwd: Path, tickets_dir: Path) -> Dict[str, Any]:
    """Best-effort stage+commit ticket changes via loom ticket.

    Team ship runs from the canonical repo root. Ticket updates are made via
    loom ticket and live under `.loom/ticket`, which is tracked by git.
    """

    if not _git_status_porcelain(cwd=cwd, pathspec=CANONICAL_TICKET_DIRNAME).strip():
        return {"ok": True, "attempted": False, "committed": False}

    try:
        payload = dataclasses.asdict(ticket_sync(tickets_dir=tickets_dir))
    except Exception as e:
        raise TeamError(f"ticket sync failed: {e}", code="TK", exit_code=1)
    return {"attempted": True, "ok": True, **payload}


def _ensure_compound_synced(*, cwd: Path) -> Dict[str, Any]:
    """Best-effort stage+commit compound learning changes.

    These updates are expected when Team runs with compound learning enabled
    (skills, instincts, AGENTS.md / LOOM_*.md, and agent definitions).
    """

    try:
        payload = dataclasses.asdict(compound_sync(repo=cwd))
    except Exception as e:
        raise TeamError(f"compound sync failed: {e}", code="CP", exit_code=1)
    attempted = bool(payload.get("committed")) or bool(payload.get("count"))
    return {"attempted": attempted, "ok": True, **payload}


def _ensure_worktree(
    *,
    cwd: Path,
    path: Path,
    ticket_id: Optional[str] = None,
    branch: Optional[str] = None,
    base_ref: Optional[str] = None,
    allow_dirty: bool = False,
) -> Dict[str, str]:
    """Ensure a ws worktree exists at `path`.

    By default, worktrees are bound to a loom ticket and use branch:
      team/<ticket_id>

    For system roles (e.g., merge queue), callers may pass an explicit `branch`.
    """

    b = str(branch or "").strip()
    if b:
        # Allow slashes for namespacing (e.g. team/merge-queue), but keep it
        # inside the team/<...> namespace.
        b = sanitize(b, allow=r"a-zA-Z0-9._/-", max_len=120)
        if not b or not b.startswith("team/"):
            raise TeamError(
                f"Invalid branch (must start with 'team/'): {branch}",
                code="ARG",
                exit_code=2,
            )
    else:
        t = str(ticket_id or "").strip()
        if not t:
            raise TeamError("Missing ticket_id or branch", code="ARG", exit_code=2)
        b = f"team/{sanitize(t, max_len=80)}"

    def _looks_like_missing_registered_worktree(err: TeamError) -> bool:
        # git worktree add error (via ws):
        #   "<path> is a missing but already registered worktree; use ... prune ..."
        msg = str(err)
        return "missing but already registered worktree" in msg

    try:
        data = repo_worktree_ensure(
            branch=b,
            path=str(path),
            base_ref=base_ref,
            allow_dirty=bool(allow_dirty),
            root=cwd,
        ).to_dict()
    except WorkspaceError as e:
        if _looks_like_missing_registered_worktree(TeamError(str(e))):
            repo_worktree_prune(root=cwd)
            data = repo_worktree_ensure(
                branch=b,
                path=str(path),
                base_ref=base_ref,
                allow_dirty=bool(allow_dirty),
                root=cwd,
            ).to_dict()
        else:
            raise TeamError(str(e), code="WS", exit_code=2)

    out = dict(data)
    wt_path = str(out.get("path") or "").strip()
    out_branch = str(out.get("branch") or b).strip()
    base = str(out.get("base_branch") or out.get("base_ref") or base_ref or "").strip()
    if not wt_path:
        raise TeamError(
            f"ws worktree ensure returned no path: {data}", code="WS_PROTOCOL"
        )

    requested = path.resolve()
    returned = Path(wt_path).expanduser().resolve()
    if returned != requested:
        raise TeamError(
            "ws reused an existing worktree for this branch, but Team requires a "
            "predictable per-run location.\n\n"
            f"branch: {out_branch or b}\n"
            f"requested: {requested}\n"
            f"returned:  {returned}\n\n"
            "Remediation:\n"
            f"- Remove the existing worktree path and retry:\n  ws repo worktree rm-path {shlex.quote(str(returned))} --yes\n"
            "- If git complains about dangling metadata, prune and retry:\n  ws repo worktree prune\n"
            "- Inspect current worktrees:\n  ws repo worktree ls\n",
            code="WORKTREE_PATH_MISMATCH",
            exit_code=2,
        )
    return {"path": wt_path, "branch": out_branch, "base": base}


def _remove_worktree(*, cwd: Path, path: Path) -> None:
    # ws is authoritative for removal.
    repo_worktree_rm_path(path=str(path), root=cwd, confirm=True)


# -----------------------------
# tmux
# -----------------------------


# -----------------------------
# Pathing + run state
# -----------------------------


# -----------------------------
# Inbox + merge queue (disk-backed scheduling primitives)
# -----------------------------


def _parse_duration_seconds(s: str) -> int:
    """Parse a human-friendly duration string into seconds."""
    try:
        return core_parse_duration_seconds(s)
    except ValueError as e:
        raise TeamError(str(e), code="ARG", exit_code=2) from e


def _message_preview(text: str, *, max_len: int = 100) -> str:
    return message_preview(text, max_len=max_len)


# -----------------------------
# Agent bootstrapping
# -----------------------------


TEAM_AGENT_PROMPT_BEGIN = "<!-- BEGIN:agent-loom-team:prompt -->"
TEAM_AGENT_PROMPT_END = "<!-- END:agent-loom-team:prompt -->"
TEAM_PACK_ID = "loom-team-core"


def _pack_installed(repo_root: Path, *, pack_id: str) -> bool:
    try:
        lock = pack_load_lock(repo_root)
    except Exception:
        return False
    return pack_id in pack_index(lock)


def _required_team_agent_relpaths() -> list[str]:
    names = [
        str(DEFAULT_MANAGER_AGENT),
        str(DEFAULT_WORKER_AGENT),
        str(DEFAULT_ARCHITECT_AGENT),
        str(DEFAULT_INTEGRATOR_AGENT),
    ]
    out: list[str] = []
    for n in names:
        out.append(f".opencode/agents/{n}.md")
        out.append(f".claude/agents/{n}.md")
    return out


def init_agents(
    *, repo: Optional[Path] = None, create_missing: bool = True, force: bool = False
) -> InitAgentsResult:
    """Install/sync Team agent definition files via `loom pack`.

    Team agents are committed artifacts under:
    - `.opencode/agents/`
    - `.claude/agents/`

    When create_missing=False, this only validates that the required files exist.
    """
    root = canonical_repo_root(repo.resolve() if repo else Path.cwd())

    wrote: list[str] = []
    skipped: list[str] = []
    warnings: list[str] = []

    if create_missing:
        if _pack_installed(root, pack_id=TEAM_PACK_ID):
            pr = pack_update(
                repo_root=root,
                pack_id=TEAM_PACK_ID,
                dry_run=False,
                force=bool(force),
            )
        else:
            pr = pack_install(
                repo_root=root,
                pack_id=TEAM_PACK_ID,
                dry_run=False,
                force=bool(force),
            )
        wrote.extend(list(pr.wrote or []))
        skipped.extend(list(pr.skipped or []))
        warnings.extend(list(pr.warnings or []))

    missing: list[str] = []
    for rel in _required_team_agent_relpaths():
        if not (root / rel).exists():
            missing.append(rel)

    return InitAgentsResult(
        repo_root=str(root),
        wrote=sorted(set(wrote)),
        updated=[],
        skipped=sorted(set(skipped)),
        missing=sorted(set(missing)),
        warnings=sorted(set(warnings)),
    )


def _require_agent_file_present(*, workdir: Path, harness: str, agent: str) -> None:
    h = _normalize_harness(harness)
    agent = str(agent or "").strip()
    if not agent:
        raise TeamError("Missing agent name", code="AGENTS", exit_code=2)

    candidates: list[Path]
    if h == "opencode":
        candidates = [(workdir / ".opencode" / "agents" / f"{agent}.md").resolve()]
    elif h == "claude":
        candidates = [(workdir / ".claude" / "agents" / f"{agent}.md").resolve()]
    else:
        candidates = [
            (workdir / ".opencode" / "agents" / f"{agent}.md").resolve(),
            (workdir / ".claude" / "agents" / f"{agent}.md").resolve(),
        ]

    for p in candidates:
        if p.exists():
            return

    expected = " or ".join(str(p) for p in candidates)
    raise TeamError(
        f"Agent file missing in worktree: {expected}",
        code="AGENTS",
        exit_code=2,
        hint=(
            "Run `loom team init` in the repo root and commit the agent files. "
            "Then recreate or update this worktree."
        ),
    )


def _ensure_opencode_worktree_runtime(*, workdir: Path, repo_root: Path) -> None:
    """Ensure opencode can load repo-local plugins inside a worktree.

    opencode loads plugins from `.opencode/plugins`. In this repo, the compound
    plugin relies on dependencies in `.opencode/node_modules`, but `node_modules`
    and `.opencode/package.json` are gitignored (see `.opencode/.gitignore`).

    New git worktrees therefore have plugins present but missing deps, which can
    cause opencode to hang/blank on startup.

    Fix: mirror the repo-root `.opencode` runtime into the worktree.
    """

    root = repo_root.resolve()
    wd = workdir.resolve()
    if wd == root:
        return

    root_op = root / ".opencode"
    wd_op = wd / ".opencode"
    if not root_op.exists() or not wd_op.exists():
        return

    root_nm = root_op / "node_modules"
    wd_nm = wd_op / "node_modules"
    if root_nm.exists() and root_nm.is_dir():
        try:
            # Ensure worktree uses the populated repo-root deps.
            if wd_nm.is_symlink():
                return
            if wd_nm.exists():
                # Only remove empty directories; avoid clobbering user state.
                if wd_nm.is_dir() and not any(wd_nm.iterdir()):
                    wd_nm.rmdir()
                else:
                    return
            wd_nm.symlink_to(root_nm)
        except Exception:
            pass

    root_pkg = root_op / "package.json"
    wd_pkg = wd_op / "package.json"
    if root_pkg.exists() and root_pkg.is_file():
        try:
            txt = root_pkg.read_text(encoding="utf-8")
        except Exception:
            txt = ""
        if txt.strip():
            try:
                if wd_pkg.exists() and wd_pkg.is_file():
                    if wd_pkg.read_text(encoding="utf-8") == txt:
                        return
                _atomic_write_text(wd_pkg, txt, encoding="utf-8")
            except Exception:
                pass


def _parse_mount_specs(
    *,
    repo_root: Path,
    paths: RunPaths,
    specs: list[str],
) -> list[dict[str, str]]:
    """Parse + validate `--mount SRC[:DEST]` specs.

    SRC/DEST are repo-root-relative paths.
    """

    root = repo_root.resolve()
    run_dir = paths.run_dir.resolve()

    def _validate_rel(raw: str, *, field: str) -> str:
        s = str(raw or "").strip()
        if not s:
            raise TeamError(f"Empty mount {field}", code="MOUNT", exit_code=2)
        if s.startswith(("/", "\\")) or s.startswith("~"):
            raise TeamError(
                f"Mount {field} must be repo-root-relative: {s}",
                code="MOUNT",
                exit_code=2,
            )
        p = Path(s)
        if p.is_absolute():
            raise TeamError(
                f"Mount {field} must be repo-root-relative: {s}",
                code="MOUNT",
                exit_code=2,
            )
        if any(part == ".." for part in p.parts):
            raise TeamError(
                f"Mount {field} must not contain '..': {s}",
                code="MOUNT",
                exit_code=2,
            )
        norm = p.as_posix().strip()
        if norm in {"", "."}:
            raise TeamError(
                f"Mount {field} must not be empty or '.': {s}",
                code="MOUNT",
                exit_code=2,
            )
        if norm == ".git" or norm.startswith(".git/"):
            raise TeamError(
                f"Refusing to mount .git: {norm}", code="MOUNT", exit_code=2
            )
        # Avoid recursion/footguns: do not mount run-local state.
        try:
            full = (root / norm).resolve()
            if full.is_relative_to(run_dir):
                raise TeamError(
                    f"Refusing to mount paths under run dir: {norm}",
                    code="MOUNT",
                    exit_code=2,
                )
        except TeamError:
            raise
        except Exception:
            # If resolve/is_relative_to fails (broken symlink), still allow
            # further checks to catch missing sources.
            pass
        return norm

    mounts: list[dict[str, str]] = []
    for raw in specs:
        tok = str(raw or "").strip()
        if not tok:
            raise TeamError("Empty --mount spec", code="MOUNT", exit_code=2)
        if ":" in tok:
            src_raw, dst_raw = tok.split(":", 1)
        else:
            src_raw, dst_raw = tok, tok
        src = _validate_rel(src_raw, field="src")
        dst = _validate_rel(dst_raw, field="dst")

        src_path = (root / src).resolve()
        if not src_path.exists():
            raise TeamError(
                f"Mount source does not exist: {src}",
                code="MOUNT",
                exit_code=2,
                hint=(
                    "Create the source path in the repo root, or remove the mount. "
                    "Mounts are repo-root-relative."
                ),
            )
        if not src_path.is_relative_to(root):
            raise TeamError(
                f"Refusing to mount path outside repo root: {src}",
                code="MOUNT",
                exit_code=2,
            )

        mounts.append({"src": src, "dst": dst})

    # Deterministic ordering.
    mounts.sort(key=lambda m: (m.get("dst", ""), m.get("src", "")))
    return mounts


def _apply_mounts(*, repo_root: Path, worktree_root: Path, mounts: list[dict]) -> None:
    root = repo_root.resolve()
    wt = worktree_root.resolve()
    if wt == root:
        return
    if not mounts:
        return

    for m in mounts:
        if not isinstance(m, dict):
            raise TeamError(
                f"Invalid mount entry: {m!r}", code="BAD_STATE", exit_code=2
            )
        src = str(m.get("src") or "").strip()
        dst = str(m.get("dst") or "").strip()
        if not src or not dst:
            raise TeamError(
                f"Invalid mount entry: {m!r}", code="BAD_STATE", exit_code=2
            )
        if Path(src).is_absolute() or Path(dst).is_absolute():
            raise TeamError(
                f"Mount paths must be relative: src={src} dst={dst}",
                code="MOUNT",
                exit_code=2,
            )
        if any(part == ".." for part in Path(src).parts) or any(
            part == ".." for part in Path(dst).parts
        ):
            raise TeamError(
                f"Mount paths must not contain '..': src={src} dst={dst}",
                code="MOUNT",
                exit_code=2,
            )
        if (
            src == ".git"
            or src.startswith(".git/")
            or dst == ".git"
            or dst.startswith(".git/")
        ):
            raise TeamError(
                f"Refusing to mount .git: src={src} dst={dst}",
                code="MOUNT",
                exit_code=2,
            )

        src_path = (root / src).resolve()
        if not src_path.exists():
            raise TeamError(
                f"Mount source does not exist: {src}",
                code="MOUNT",
                exit_code=2,
                hint="Update mounts via `loom team start <TEAM> --clear-mounts` or by re-starting with corrected --mount flags.",
            )
        try:
            if not src_path.is_relative_to(root):
                raise TeamError(
                    f"Refusing to mount path outside repo root: {src}",
                    code="MOUNT",
                    exit_code=2,
                )
        except AttributeError:
            # Python <3.9 doesn't have Path.is_relative_to; Loom targets 3.11+
            pass

        dst_path = wt / dst
        dst_parent = dst_path.parent

        # Security: refuse mounts where the *parent* escapes the worktree via symlinks.
        # Note that the mount destination itself is a symlink (the intended outcome),
        # so resolving the full dst_path would incorrectly follow the existing mount.
        try:
            resolved_parent = dst_parent.resolve(strict=False)
        except Exception:
            resolved_parent = dst_parent.absolute()
        try:
            if not resolved_parent.is_relative_to(wt):
                raise TeamError(
                    f"Refusing to mount outside worktree: {dst}",
                    code="MOUNT",
                    exit_code=2,
                )
        except AttributeError:
            pass
        if dst == ".git" or dst.startswith(".git/"):
            raise TeamError(
                f"Refusing to mount into .git: {dst}", code="MOUNT", exit_code=2
            )

        dst_parent.mkdir(parents=True, exist_ok=True)

        if dst_path.exists() or dst_path.is_symlink():
            if dst_path.is_symlink():
                try:
                    raw_target = dst_path.readlink()
                    if raw_target.is_absolute():
                        target_abs = raw_target.resolve()
                    else:
                        target_abs = (dst_path.parent / raw_target).resolve()
                except Exception:
                    target_abs = None
                if target_abs is not None and target_abs == src_path:
                    continue
            raise TeamError(
                f"Mount destination already exists: {dst}",
                code="MOUNT",
                exit_code=2,
                hint=f"Remove or rename {dst_path} in the worktree and retry.",
            )

        try:
            dst_path.symlink_to(src_path)
        except Exception as e:
            raise TeamError(
                f"Failed to create mount symlink: {dst} -> {src} ({e!r})",
                code="MOUNT",
                exit_code=2,
            )


def _roster_state_from_run(run: Mapping[str, Any]) -> Dict[str, Any]:
    raw_roster = run.get("roster")
    if isinstance(raw_roster, dict):
        return dict(raw_roster)
    return {}


def _roster_summary_from_run(run: Mapping[str, Any]) -> Dict[str, Any]:
    raw = _roster_state_from_run(run)

    raw_spec = raw.get("spec")
    spec: Dict[str, Any] = dict(raw_spec) if isinstance(raw_spec, dict) else {}

    raw_metadata = spec.get("metadata")
    metadata: Dict[str, Any] = (
        dict(raw_metadata) if isinstance(raw_metadata, dict) else {}
    )

    name = str(metadata.get("name") or "").strip()
    purpose = str(metadata.get("purpose") or "").strip()
    source = str(raw.get("source") or "").strip()
    loaded_at = str(raw.get("loaded_at") or "").strip()

    version = 0
    raw_version = spec.get("version")
    if isinstance(raw_version, (int, float, str)) and str(raw_version).strip():
        try:
            version = int(str(raw_version).strip())
        except Exception:
            version = 0

    raw_builtins = spec.get("builtins")
    builtins: Dict[str, Any] = (
        dict(raw_builtins) if isinstance(raw_builtins, dict) else {}
    )

    raw_members = spec.get("members")
    members: list[Any] = list(raw_members) if isinstance(raw_members, list) else []

    raw_labels = metadata.get("labels")
    labels: list[Any] = list(raw_labels) if isinstance(raw_labels, list) else []

    if not any((name, purpose, source, loaded_at, version, builtins, members, labels)):
        return {}

    return {
        "name": name,
        "purpose": purpose,
        "source": source,
        "loaded_at": loaded_at,
        "version": version,
        "builtins": len(builtins),
        "members": len(members),
        "labels": [str(label) for label in labels if str(label).strip()],
    }


def _roster_mount_specs_from_run(run: Mapping[str, Any]) -> list[str]:
    raw = _roster_state_from_run(run)
    raw_spec = raw.get("spec")
    spec: Dict[str, Any] = dict(raw_spec) if isinstance(raw_spec, dict) else {}

    raw_mounts = spec.get("mounts")
    if not isinstance(raw_mounts, list):
        return []

    out: list[str] = []
    for item in raw_mounts:
        tok = str(item or "").strip()
        if tok:
            out.append(tok)
    return out


def _write_charter(paths: RunPaths, run: Mapping[str, Any]) -> Path:
    """Write a run-local charter (human/agent reference)."""

    objective = str(run.get("objective") or "").strip()
    objective_rev = int(run.get("objective_rev") or 0)
    objective_updated_at = str(run.get("objective_updated_at") or "").strip()
    tickets_dir = str(run.get("tickets_dir") or "").strip()
    sprint = run.get("sprint") if isinstance(run.get("sprint"), dict) else {}
    sprint_name = str((sprint or {}).get("name") or "").strip()
    sprint_tag = str((sprint or {}).get("tag") or "").strip()
    sprint_started_at = str((sprint or {}).get("started_at") or "").strip()

    lines = []
    lines.append(f"# Team Charter — {paths.team}\n")
    lines.append(f"Run ID: {run.get('run_id', '')}\n")
    lines.append(f"Repo: {run.get('repo_root', '')}\n")
    if tickets_dir:
        lines.append(f"{ENV_TICKET_DIR}: {tickets_dir}\n")
    lines.append("\n")
    lines.append("## Objective (current)\n\n")
    if objective_rev:
        lines.append(f"Objective rev: {objective_rev}\n")
    if objective_updated_at:
        lines.append(f"Objective updated_at: {objective_updated_at}\n")
    lines.append("\n")
    lines.append(objective + "\n\n")

    lines.append("## Sprint (current)\n\n")
    if sprint_name:
        lines.append(f"Name: {sprint_name}\n")
    if sprint_started_at:
        lines.append(f"Started: {sprint_started_at}\n")
    if sprint_tag:
        lines.append(f"Tag: {sprint_tag}\n")
        lines.append(f"Ticket rule: include tag `{sprint_tag}` on sprint tickets.\n")
    if not sprint_name:
        lines.append("(none)\n")
    lines.append("\n")
    roster = _roster_summary_from_run(run)
    lines.append("## Roster (current)\n\n")
    if roster:
        if roster.get("name"):
            lines.append(f"Name: {roster.get('name')}\n")
        if roster.get("version"):
            lines.append(f"Schema version: {roster.get('version')}\n")
        if roster.get("builtins"):
            lines.append(f"Built-ins: {roster.get('builtins')}\n")
        if roster.get("members"):
            lines.append(f"Additional members: {roster.get('members')}\n")
        if roster.get("source"):
            lines.append(f"Source: {roster.get('source')}\n")
        if roster.get("loaded_at"):
            lines.append(f"Loaded at: {roster.get('loaded_at')}\n")
    else:
        lines.append("(none)\n")
    lines.append("\n")
    lines.append("## Manager quickstart\n\n")
    lines.append("Sprint loop:\n")
    lines.append(f'- Start sprint: `loom team prep-sprint {paths.team} --name "..."`\n')
    lines.append(
        "- Fan-out (preferred): spawn an Architect; architect creates tickets directly.\n"
    )
    lines.append("- Plan: decide concurrency + ordering.\n")
    lines.append("- Execute: spawn workers.\n")
    lines.append("- Fan-in: integrate via merge queue; ship.\n")
    lines.append("- Cleanup: retire workers; mark worktrees retirable when safe.\n")
    lines.append("\n")

    lines.append("Core:\n")
    lines.append(f"- Observe roster: `loom team status {paths.team}`\n")
    lines.append(
        f"- Capture output: `loom team capture {paths.team} <manager|worker|ticket>`\n"
    )
    lines.append(f'- Send message: `loom team send {paths.team} <target> "..."`\n')
    lines.append(f"- Spawn worker: `loom team spawn {paths.team} <TICKET_ID>`\n")
    lines.append(
        f"- Resume worker: `loom team resume-worker {paths.team} <WORKER_ID>` (reuse existing worktree)\n"
    )
    lines.append(f"- Retire worker: `loom team retire {paths.team} <WORKER_ID>`\n")
    lines.append(
        f"- Mark worktree retirable: `loom team mark-retirable {paths.team} <WORKER_ID>` (manager-only)\n"
    )
    lines.append(
        f"- Bounce worker: `loom team bounce {paths.team} <WORKER_ID|TICKET_ID>`\n"
    )
    lines.append("\n")
    lines.append("Durability + waiting:\n")
    lines.append(
        f"- Inbox list: `loom team inbox {paths.team} list --to manager --unacked`\n"
    )
    lines.append(f"- Ack message: `loom team inbox {paths.team} ack <MSG_ID>`\n")
    lines.append(
        f"- Wait (blocks; wakes early on inbox): `loom team wait {paths.team} 5m` (or `loom team wait 5m` inside tmux; `snooze` is an alias)\n"
    )
    lines.append(
        f"- Clock out (pause team): `loom team clock-out {paths.team}` (keeps state; stops tmux session)\n"
    )
    lines.append(
        f"- Clock in (resume team): `loom team clock-in {paths.team}` (restores manager + active workers)\n"
    )
    lines.append(
        f'- Update objective: `loom team objective {paths.team} set|append --message "..."`\n'
    )
    lines.append(
        f"- Team hygiene: `loom team janitor {paths.team}` (deletes only marked-retirable worktrees)\n"
    )
    lines.append(
        f"- When 100% done: `loom team disband {paths.team}` (preserves worktrees by default)\n"
    )
    lines.append("\n")
    lines.append("Merge queue (ship code):\n")

    ms = _merge_state(run)
    cfg = dict(ms.get("config") or {})
    target_branch = str(cfg.get("target_branch") or "main").strip() or "main"
    remote = str(cfg.get("remote") or "origin").strip() or "origin"
    push = bool(cfg.get("push"))
    lines.append(
        f"- Ensure integrator exists: `loom team spawn-integrator {paths.team}`\n"
    )
    lines.append(
        f"- Enqueue approved branch: `loom team merge {paths.team} enqueue --ticket <TICKET_ID> --branch <BRANCH> --from-worker <WORKER_ID>`\n"
    )
    lines.append(f"- Queue status: `loom team merge {paths.team} list`\n")
    lines.append(
        f"- Ship (merge-queue -> {remote}/{target_branch}, push={push}): `loom team ship {paths.team}` (nothing is shipped until you do this)\n"
    )
    lines.append("\n")
    lines.append("## Worker protocol\n\n")
    lines.append("Workers must:\n")
    lines.append("- Work exactly one ticket in their assigned worktree.\n")
    lines.append(
        "- Update the ticket via loom ticket at least every ~15 minutes or after major steps.\n"
    )
    lines.append("- Escalate when blocked (structured) and notify manager.\n")
    lines.append("- Request review before considering a ticket complete.\n\n")

    paths.charter_file.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(paths.charter_file, "".join(lines))

    return paths.charter_file


def _opencode_tui_argv(
    *,
    project_dir: Path,
    agent: str,
    prompt: str,
    model: str = "",
    bin: str = "opencode",
) -> List[str]:
    _require_bin(bin)
    argv: List[str] = [bin, str(project_dir)]
    if prompt:
        argv += ["--prompt", prompt]
    if model:
        argv += ["--model", model]
    if agent:
        argv += ["--agent", agent]
    return argv


def _claude_tui_argv(
    *,
    agent: str,
    prompt: str,
    model: str = "",
    bin: str = "claude",
) -> List[str]:
    _require_bin(bin)
    argv: List[str] = [bin]
    if model:
        argv.append(f"--model={model}")
    if agent:
        argv.append(f"--agent={agent}")
    if prompt:
        argv.append(prompt)
    return argv


def _strip_yaml_frontmatter(text: str) -> str:
    lines = str(text or "").splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[i + 1 :]).strip()
    return "\n".join(lines).strip()


def _extract_prompt_from_agent_file(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    begin = TEAM_AGENT_PROMPT_BEGIN.strip()
    end = TEAM_AGENT_PROMPT_END.strip()

    start_idx = -1
    for i, line in enumerate(lines):
        if line.strip() == begin:
            start_idx = i
            break

    if start_idx >= 0:
        out_lines: list[str] = []
        for line in lines[start_idx + 1 :]:
            if line.strip() == begin or line.strip() == end:
                continue
            out_lines.append(line)
        text = "\n".join(out_lines).strip()
        if text:
            return text

    return _strip_yaml_frontmatter(raw)


def _agent_prompt_text(*, workdir: Path, agent: str) -> str:
    name = str(agent or "").strip()
    if not name:
        raise TeamError("Missing agent name", code="AGENTS", exit_code=2)

    candidates = [
        (workdir / ".opencode" / "agents" / f"{name}.md").resolve(),
        (workdir / ".claude" / "agents" / f"{name}.md").resolve(),
    ]
    for p in candidates:
        if p.exists():
            prompt = _extract_prompt_from_agent_file(p)
            if prompt:
                return prompt

    expected = " or ".join(str(p) for p in candidates)
    raise TeamError(
        f"Agent file missing in worktree: {expected}",
        code="AGENTS",
        exit_code=2,
        hint=(
            "Run `loom team init` in the repo root and commit the agent files. "
            "Then recreate or update this worktree."
        ),
    )


def _compose_wrapped_agent_prompt(
    *, protocol_preamble: str, user_agent_prompt: str
) -> str:
    protocol = str(protocol_preamble or "").strip()
    user = str(user_agent_prompt or "").strip()
    if protocol and user:
        return f"{protocol}\n\n---\n\n{user}".strip()
    if protocol:
        return protocol
    return user


def _omp_tui_argv(
    *,
    prompt: str,
    model: str,
    system_prompt_append: str,
    session_path: Path,
    tools: list[str] | None,
    bin: str = "omp",
) -> List[str]:
    _require_bin(bin)
    _ = session_path
    argv: List[str] = [bin]
    if model:
        argv += ["--model", model]
    if system_prompt_append:
        argv += ["--append-system-prompt", system_prompt_append]
    if tools:
        argv += ["--tools", ",".join(tools)]
    if prompt:
        argv.append(prompt)
    return argv


def _codex_tui_argv(
    *,
    prompt: str,
    model: str,
    instructions_file: Path,
    resume_last: bool,
    bin: str = "codex",
) -> List[str]:
    _require_bin(bin)
    argv: List[str] = [bin]
    if model:
        argv += ["--model", model]
    argv += ["--dangerously-bypass-approvals-and-sandbox"]
    instructions_value = (
        str(instructions_file).replace("\\", "\\\\").replace('"', '\\"')
    )
    argv += ["--config", f'model_instructions_file="{instructions_value}"']
    if resume_last:
        argv += ["resume", "--last"]
    elif prompt:
        argv.append(prompt)
    return argv


def _seed_codex_home_auth(*, codex_home: Path) -> None:
    shared_home_env = str(os.environ.get("CODEX_HOME") or "").strip()
    shared_home = (
        Path(shared_home_env).expanduser()
        if shared_home_env
        else (Path.home() / ".codex")
    )
    try:
        shared_home_resolved = shared_home.resolve()
        codex_home_resolved = codex_home.resolve()
    except Exception:
        return
    if shared_home_resolved == codex_home_resolved:
        return

    for name in ("auth.json", "config.toml"):
        src = shared_home_resolved / name
        if not src.exists() or not src.is_file():
            continue
        dst = codex_home_resolved / name
        if dst.exists() or dst.is_symlink():
            continue
        try:
            dst.symlink_to(src)
        except Exception:
            try:
                shutil.copy2(src, dst)
            except Exception:
                continue


def _team_tui_argv(
    *,
    project_dir: Path,
    agent: str,
    prompt: str,
    model: str = "",
    harness: str = DEFAULT_HARNESS,
    bin: str = "",
) -> List[str]:
    """Return argv to launch the Team harness that runs an agent."""

    argv: List[str] = ["loom", "team", "tui", str(project_dir)]
    if harness:
        argv += ["--harness", harness]
    if bin:
        argv += ["--bin", bin]
    if agent:
        argv += ["--agent", agent]
    if model:
        argv += ["--model", model]
    if prompt:
        argv += ["--prompt", prompt]
    return argv


def _append_log_line(path: Path, line: str) -> None:
    def _write() -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(line.rstrip("\n") + "\n")
            f.flush()
            best_effort(lambda: os.fsync(f.fileno()), label="append_log_line.fsync")

    best_effort(_write, label="append_log_line")


def _sidecar_pid_file(paths: RunPaths, recipient: str) -> Path:
    safe = (
        sanitize(str(recipient or ""), allow=r"a-zA-Z0-9._-", max_len=48) or "unknown"
    )
    return paths.sidecars_dir / f"{safe}.pid.json"


def _sidecar_pid_write(
    *,
    paths: RunPaths,
    recipient: str,
    pid: int,
    pane_id: str,
    harness: str,
    agent_bin: str,
    argv: List[str],
    project_dir: Path,
    run_id: str,
) -> None:
    if not pid:
        return
    p = _sidecar_pid_file(paths, recipient)
    _atomic_write_json(
        p,
        {
            "pid": int(pid),
            "recipient": str(recipient),
            "pane_id": str(pane_id),
            "harness": str(harness),
            "agent_bin": str(agent_bin),
            "argv": list(argv),
            "project_dir": str(project_dir),
            "run_id": str(run_id),
            "started_at": _iso_z(),
        },
    )


def _sidecar_pid_clear(*, paths: RunPaths, recipient: str) -> None:
    try:
        _sidecar_pid_file(paths, recipient).unlink()
    except FileNotFoundError:
        return
    except Exception:
        return


def _recipient_from_env() -> str:
    role = str(os.getenv(ENV_TEAM_ROLE) or "").strip().lower()
    if role == ROLE_MANAGER:
        return "manager"
    wid = str(os.getenv(ENV_TEAM_WORKER_ID) or "").strip()
    return sanitize(wid, allow=r"a-zA-Z0-9._-", max_len=48)


def _run_paths_from_env() -> Optional[RunPaths]:
    team = sanitize(str(os.getenv(ENV_TEAM_NAME) or ""), max_len=80)
    run_dir_raw = str(os.getenv(ENV_TEAM_RUN_DIR) or "").strip()
    if not team or not run_dir_raw:
        return None

    run_dir = Path(run_dir_raw).expanduser().resolve()
    # Expected: <repo_root>/.loom/team/runs/<team>
    try:
        repo_root = run_dir.parent.parent.parent.parent.resolve()
    except Exception:
        repo_root = None
    if repo_root and (run_dir / "run.json").exists():
        return RunPaths(repo_root=repo_root, team=team)

    # Fallback discovery (best-effort, e.g. if env is wrong).
    discovered = discover_repo_root_for_team(team, start=Path.cwd())
    if discovered is None:
        return None
    return RunPaths(repo_root=discovered, team=team)


def _paths_for(*, team: str, repo: Optional[Path]) -> RunPaths:
    repo_root = repo.resolve() if repo is not None else None
    if repo_root is not None:
        candidate = RunPaths(repo_root=repo_root, team=team)
        if candidate.run_file.exists() or candidate.run_dir.exists():
            return candidate
    return resolve_run_paths(team=team, repo=repo_root)


def _should_nudge(*, last_at: float, now: float, cooldown_s: float) -> bool:
    return (now - last_at) >= cooldown_s


def _capture_pane_and_persist(
    paths: RunPaths,
    *,
    run: Mapping[str, Any],
    pane_id: str,
    target_key: str,
    target_meta: Mapping[str, Any],
    pane: Mapping[str, Any],
    lines: int,
    no_join: bool,
    summary: str,
) -> Dict[str, Any]:
    captured_at = _iso_z()
    out = tmux_capture(pane_id, lines=int(lines), join_wrapped=not bool(no_join))

    # Persist capture for later UI/audit inspection.
    cap_id = uuid.uuid4().hex[:12]
    safe_target = (
        sanitize(str(target_key or ""), allow=r"a-zA-Z0-9._-", max_len=40) or "target"
    )
    base = f"{_event_stamp(captured_at)}_{cap_id}_{safe_target}"
    cap_txt = paths.captures_dir / f"{base}.txt"
    cap_json = paths.captures_dir / f"{base}.json"

    def _persist_capture() -> None:
        paths.captures_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(cap_txt, out)
        _atomic_write_json(
            cap_json,
            {
                "id": cap_id,
                "captured_at": captured_at,
                "team": str(run.get("team") or paths.team),
                "run_id": str(run.get("run_id") or ""),
                "target": dict(target_meta or {}),
                "pane": dict(pane or {}),
                "lines": int(lines),
                "output_file": str(cap_txt),
                "bytes": len(out.encode("utf-8")),
            },
        )

    best_effort(_persist_capture, label="capture.persist")

    safe_write_event(
        paths,
        event_type="capture.saved",
        run=run,
        summary=str(summary or f"Captured {safe_target} lines={int(lines)}"),
        refs={
            **(dict(target_meta or {})),
            "capture_id": cap_id,
            "capture_file": str(cap_txt),
            "capture_meta": str(cap_json),
        },
        data={
            "lines": int(lines),
            "bytes": len(out.encode("utf-8")),
            "no_join": bool(no_join),
        },
    )

    return {
        "id": cap_id,
        "captured_at": captured_at,
        "output": out,
        "output_file": str(cap_txt),
        "meta_file": str(cap_json),
    }


def tui(
    *,
    project_dir: Path,
    harness: str = DEFAULT_HARNESS,
    bin_override: str = "",
    agent: str = "",
    model: str = "",
    prompt: str = "",
    nudge_cooldown_s: float = 300.0,
    stall_threshold_s: float = 1080.0,
    idle_screen_threshold_s: float = DEFAULT_IDLE_SCREEN_S,
    respawn_cap: int = 3,
    respawn_window_s: float = 3600.0,
    objective_nudge_s: float = DEFAULT_OBJECTIVE_NUDGE_S,
    done_check_s: float = DEFAULT_DONE_CHECK_S,
    disband_resend_s: float = DEFAULT_DISBAND_REMINDER_RESEND_S,
) -> TuiResult:
    """Team sidecar harness.

    Runs an agent TUI as a subprocess in this tmux pane and keeps it healthy:
      - inbox wakeups via tmux wait-for
      - stall nudges
      - auto-respawn with backoff + cap
    """

    _require_bin("tmux")

    harness = str(harness or DEFAULT_HARNESS).strip().lower()
    if harness not in ("opencode", "claude", "omp", "codex"):
        harness = DEFAULT_HARNESS
    bin_override = str(bin_override or "").strip()
    agent_bin = bin_override or harness
    _require_bin(agent_bin)

    project_dir = Path(str(project_dir)).expanduser().resolve()
    agent = str(agent or "").strip()
    model = str(model or "").strip()
    prompt = str(prompt or "")

    pane_id = str(os.environ.get("TMUX_PANE") or "").strip()
    paths = _run_paths_from_env()
    recipient = _recipient_from_env()
    role = str(os.getenv(ENV_TEAM_ROLE) or "").strip().lower()
    if not pane_id or not paths or not recipient:
        # Never print into the pane (would corrupt the TUI). Exit quietly.
        return TuiResult(
            recipient=recipient or "", run_id="", exit_reason="missing_env"
        )

    run: Dict[str, Any]
    try:
        run = load_run(paths)
    except Exception:
        return TuiResult(recipient=recipient, run_id="", exit_reason="missing_run")

    run_id = str(run.get("run_id") or "").strip()
    log_path = paths.sidecars_dir / f"{recipient}.log"
    _append_log_line(
        log_path,
        f"{_iso_z()} sidecar start harness={harness} pane={pane_id} role={role} project={project_dir}",
    )

    cooldown_s = float(nudge_cooldown_s or 300.0)
    stall_s = float(stall_threshold_s or 1080.0)
    idle_screen_s = float(idle_screen_threshold_s or DEFAULT_IDLE_SCREEN_S)
    respawn_cap = int(respawn_cap or 3)
    respawn_window_s = float(respawn_window_s or 3600.0)

    objective_nudge_s = float(objective_nudge_s or DEFAULT_OBJECTIVE_NUDGE_S)
    done_check_s = float(done_check_s or DEFAULT_DONE_CHECK_S)
    disband_resend_s = float(disband_resend_s or DEFAULT_DISBAND_REMINDER_RESEND_S)

    safe_write_event(
        paths,
        event_type="sidecar.started",
        run=run,
        summary=f"Sidecar started recipient={recipient}",
        refs={"recipient": recipient, "pane_id": pane_id},
        data={
            "project_dir": str(project_dir),
            "harness": harness,
            "agent": agent,
            "model": model,
            "cooldown_s": cooldown_s,
            "stall_s": stall_s,
            "respawn_cap": respawn_cap,
            "respawn_window_s": respawn_window_s,
        },
    )

    ch = channel_for(run_id=run_id, to=recipient)

    lock = threading.Lock()
    stop = threading.Event()
    wake = threading.Event()
    proc: Optional[subprocess.Popen[Any]] = None
    stop_reason = "stopped"
    last_nudge_at = 0.0
    respawn_times: List[float] = []
    bounce_killed_pid: Optional[int] = None
    bounce_pending = threading.Event()
    has_spawned_once = False

    def stop_all(reason: str) -> None:
        nonlocal stop_reason
        stop_reason = str(reason or "stopped")
        stop.set()
        wake.set()
        with lock:
            p = proc
        if not p or p.poll() is not None:
            return
        try:
            p.send_signal(signal.SIGTERM)
        except Exception:
            try:
                p.terminate()
            except Exception:
                pass
        deadline = time.time() + 1.5
        while time.time() < deadline and p.poll() is None:
            time.sleep(0.05)
        if p.poll() is None:
            try:
                p.kill()
            except Exception:
                pass

    def _handle_signal(sig: int, _frame: Any) -> None:
        stop_all(f"signal:{sig}")

    # If this wrapper process gets signaled (tmux session/window killed), shut down the
    # child TUI promptly. This keeps orphans from hanging around.
    try:
        signal.signal(signal.SIGTERM, _handle_signal)
        signal.signal(signal.SIGHUP, _handle_signal)
        signal.signal(signal.SIGINT, _handle_signal)
    except Exception:
        pass

    def child_alive() -> bool:
        with lock:
            p = proc
        return bool(p and p.poll() is None)

    def safe_nudge(text: str) -> None:
        nonlocal last_nudge_at
        now = time.time()
        if not _should_nudge(last_at=last_nudge_at, now=now, cooldown_s=cooldown_s):
            return
        if not child_alive():
            return
        try:
            session = tmux_format(pane_id, "#{session_name}")
            if not session:
                return
            panes = tmux_list_panes(session)
            pane = panes.get(pane_id)
            if not pane or not _pane_can_receive_chat(pane):
                return
            tmux_send_text(pane_id, text, enter=True, ctrl_enter=(harness == "omp"))
            last_nudge_at = now
        except Exception:
            return

    def _handle_control_message(msg: Mapping[str, Any]) -> bool:
        nonlocal bounce_killed_pid
        kind = str(msg.get("kind") or "").strip()
        if kind != INBOX_KIND_CONTROL:
            return False

        mid = str(msg.get("id") or "").strip()
        meta = msg.get("meta") if isinstance(msg.get("meta"), dict) else {}
        op = str((meta or {}).get("op") or msg.get("message") or "").strip()

        if mid:
            best_effort(
                lambda: inbox_ack_message(paths, mid), label="inbox.control.ack"
            )

        if op != CONTROL_OP_BOUNCE:
            safe_write_event(
                paths,
                event_type="sidecar.control_ignored",
                run=run,
                summary=f"Ignored control op={op} recipient={recipient}",
                refs={"recipient": recipient, "inbox_id": mid},
            )
            return True

        bounce_pending.set()
        wake.set()

        with lock:
            p = proc

        if p and p.poll() is None:
            try:
                bounce_killed_pid = int(p.pid)
            except Exception:
                bounce_killed_pid = None
            try:
                p.send_signal(signal.SIGKILL)
            except Exception:
                best_effort(p.kill, label="sidecar.bounce.kill")

        safe_write_event(
            paths,
            event_type="sidecar.bounce_requested",
            run=run,
            summary=f"Bounce requested recipient={recipient}",
            refs={
                "recipient": recipient,
                "inbox_id": mid,
                "pid": str(getattr(p, "pid", "")),
            },
        )
        return True

    def inbox_nudge() -> None:
        try:
            msgs = inbox_list_messages(paths, to=recipient, unacked_only=True, limit=25)
        except Exception:
            return
        if not msgs:
            return

        user_msgs: List[Dict[str, Any]] = []
        for m in msgs:
            if _handle_control_message(m):
                continue
            user_msgs.append(dict(m))

        if not user_msgs:
            return

        newest = user_msgs[0]
        mid = str(newest.get("id") or "")
        first = (
            str(newest.get("message") or "").splitlines()[0]
            if newest.get("message")
            else ""
        )
        if len(first) > 100:
            first = first[:97] + "..."
        safe_nudge(
            f"TEAM: inbox has {len(user_msgs)} unacked. Run: loom team inbox {paths.team} list --to {recipient} --unacked (newest id={mid}: {first})"
        )

    def inbox_loop() -> None:
        # Startup scan.
        inbox_nudge()
        while not stop.is_set():
            # Block until signaled; periodically wake to re-check stop.
            tmux_wait_for(ch, timeout_s=60.0)
            if stop.is_set():
                return
            inbox_nudge()

    def stall_loop() -> None:
        while not stop.is_set():
            time.sleep(60.0)
            if stop.is_set():
                return
            if not child_alive():
                continue
            try:
                raw = tmux_format(pane_id, "#{pane_last_activity}")
                try:
                    last = float(str(raw).strip())
                except Exception:
                    last = 0.0
                if not last:
                    continue
                if (time.time() - last) >= stall_s:
                    dirty = False
                    try:
                        p = _run(
                            ["git", "status", "--porcelain"],
                            cwd=project_dir,
                            check=False,
                            timeout=5.0,
                        )
                        dirty = bool((p.stdout or "").strip())
                    except Exception:
                        dirty = False
                    safe_nudge(
                        (
                            "TEAM: stall detected. Commit your changes now, then post a loom ticket update; if blocked, escalate with 2 options; notify manager. "
                            f"If you have no moves, you may self-retire (keeps worktree): `loom team retire {paths.team} {recipient}`."
                            if dirty
                            else "TEAM: stall detected. Post a loom ticket update now; if blocked, escalate with 2 options; notify manager. "
                            f"If you have no moves, you may self-retire (keeps worktree): `loom team retire {paths.team} {recipient}`."
                        )
                    )
            except Exception:
                continue

    threading.Thread(target=inbox_loop, daemon=True).start()
    threading.Thread(target=stall_loop, daemon=True).start()

    def orphan_loop() -> None:
        # If the tmux session goes away, this wrapper should exit and take its child with it.
        while not stop.is_set():
            time.sleep(2.0)
            if stop.is_set():
                return
            try:
                session = tmux_format(pane_id, "#{session_name}")
                if not session or not tmux_has_session(session):
                    stop_all("orphaned")
                    return
            except Exception:
                stop_all("orphaned")
                return

    threading.Thread(target=orphan_loop, daemon=True).start()

    # Periodic, low-overhead pane snapshots for the UI.
    # This reuses the same persistence path as `loom team capture`.

    def _next_autocapture_delay_s(*, initial: bool) -> float:
        if initial:
            return 30.0 + (random.random() * 60.0)  # 30s..90s (stagger startup)
        lo = float(min(DEFAULT_AUTOCAPTURE_MIN_S, DEFAULT_AUTOCAPTURE_MAX_S))
        hi = float(max(DEFAULT_AUTOCAPTURE_MIN_S, DEFAULT_AUTOCAPTURE_MAX_S))
        if hi <= 0 or hi <= lo:
            return max(60.0, lo)
        return lo + (random.random() * (hi - lo))

    last_capture_at: float = 0.0
    last_screen_hash: str = ""
    screen_unchanged_since: float = 0.0
    idle_screen_notified: bool = False

    def autocapture_loop() -> None:
        nonlocal last_capture_at
        nonlocal last_screen_hash
        nonlocal screen_unchanged_since
        nonlocal idle_screen_notified
        next_at = time.time() + _next_autocapture_delay_s(initial=True)
        while not stop.is_set():
            time.sleep(30.0)
            if stop.is_set():
                return
            now = time.time()
            if now < next_at:
                continue
            try:
                session = tmux_format(pane_id, "#{session_name}")
                if not session or not tmux_has_session(session):
                    next_at = now + _next_autocapture_delay_s(initial=False)
                    continue
                panes = tmux_list_panes(session)
                pane = panes.get(pane_id)
                if not pane:
                    next_at = now + _next_autocapture_delay_s(initial=False)
                    continue

                r = load_run(paths)
                role = str(os.getenv(ENV_TEAM_ROLE) or "").strip() or (
                    ROLE_MANAGER if recipient == "manager" else ROLE_WORKER
                )
                ticket_id = str(os.getenv(ENV_TEAM_TICKET_ID) or "").strip()
                target_meta: Dict[str, Any] = {"role": role, "pane_id": pane_id}
                if recipient != "manager":
                    target_meta["worker_id"] = recipient
                    if ticket_id:
                        target_meta["ticket_id"] = ticket_id

                cap = _capture_pane_and_persist(
                    paths,
                    run=r,
                    pane_id=pane_id,
                    target_key=recipient,
                    target_meta=target_meta,
                    pane=pane,
                    lines=int(DEFAULT_AUTOCAPTURE_LINES),
                    no_join=False,
                    summary=f"Auto-captured {recipient} lines={int(DEFAULT_AUTOCAPTURE_LINES)}",
                )

                # Idle detection: "screen unchanged" across captures.
                # This is intentionally separate from tmux pane_last_activity (stall detection).
                role_norm = str(role or "").strip().lower()
                if role_norm in (ROLE_WORKER, ROLE_ARCHITECT):
                    out = str((cap or {}).get("output") or "")
                    h = hashlib.sha256(out.encode("utf-8")).hexdigest()
                    if last_screen_hash and h == last_screen_hash:
                        if not screen_unchanged_since:
                            screen_unchanged_since = last_capture_at or now
                        if (
                            not idle_screen_notified
                            and idle_screen_s > 0
                            and (now - screen_unchanged_since) >= idle_screen_s
                        ):
                            safe_nudge(
                                "TEAM: idle screen detected. Post a ticket update now. If you have no moves, you may self-retire (keeps worktree): "
                                f"`loom team retire {paths.team} {recipient}`. Manager can resume you later."
                            )
                            if recipient != "manager":
                                try:
                                    _inbox_write_and_maybe_nudge(
                                        paths=paths,
                                        run=r,
                                        target="manager",
                                        message=(
                                            f"IDLE_SCREEN worker={recipient} role={role_norm} unchanged_s={int(now - screen_unchanged_since)} "
                                            f"ticket={ticket_id or '-'} pane={pane_id}"
                                        ),
                                        sender="team",
                                        kind="idle_screen",
                                        meta_extra={
                                            "worker_id": recipient,
                                            "role": role_norm,
                                            "ticket_id": ticket_id,
                                            "pane_id": pane_id,
                                            "unchanged_s": int(
                                                now - screen_unchanged_since
                                            ),
                                        },
                                        nudge=True,
                                        force=False,
                                        line_info="idle_screen",
                                    )
                                except Exception:
                                    pass
                            idle_screen_notified = True
                    else:
                        last_screen_hash = h
                        screen_unchanged_since = 0.0
                        idle_screen_notified = False
                    last_capture_at = now
            except Exception:
                pass
            next_at = time.time() + _next_autocapture_delay_s(initial=False)

    threading.Thread(target=autocapture_loop, daemon=True).start()

    # Manager-only: keep the objective top-of-mind until disband.
    # This is a lightweight tmux nudge; authoritative details live in CHARTER + inbox.
    if recipient == "manager":

        def objective_loop() -> None:
            last_at = 0.0
            while not stop.is_set():
                time.sleep(60.0)
                if stop.is_set():
                    return
                now = time.time()
                if (now - last_at) < max(60.0, objective_nudge_s):
                    continue
                try:
                    r = load_run(paths)
                    obj = str(r.get("objective") or "").strip()
                    first = (
                        message_preview(obj, max_len=120) if obj else "(no objective)"
                    )
                    safe_nudge(
                        f"TEAM: objective: {first} | if done: loom team disband {paths.team} | update: loom team objective {paths.team} append ..."
                    )
                    last_at = now
                except Exception:
                    continue

        def done_check_loop() -> None:
            # Periodically compute "done" and queue a durable disband reminder.
            while not stop.is_set():
                time.sleep(max(60.0, done_check_s))
                if stop.is_set():
                    return
                try:
                    best_effort(
                        lambda: _maybe_queue_disband_reminder(
                            paths,
                            resend_after_s=disband_resend_s,
                            nudge=True,
                        ),
                        label="done_check",
                    )
                except Exception:
                    continue

        threading.Thread(target=objective_loop, daemon=True).start()
        threading.Thread(target=done_check_loop, daemon=True).start()

    backoff_s = 1.0
    while True:
        if stop.is_set():
            return TuiResult(
                recipient=recipient, run_id=run_id, exit_reason=str(stop_reason)
            )

        now = time.time()
        spawn_due_to_bounce = bounce_pending.is_set()
        if spawn_due_to_bounce:
            backoff_s = 1.0
        respawn_times = [t for t in respawn_times if (now - t) <= respawn_window_s]
        if not spawn_due_to_bounce and len(respawn_times) >= respawn_cap:
            _append_log_line(
                log_path,
                f"{_iso_z()} respawn cap reached cap={respawn_cap} window_s={respawn_window_s}",
            )
            safe_write_event(
                paths,
                event_type="sidecar.respawn_capped",
                run=run,
                ok=False,
                summary=f"Sidecar respawn capped recipient={recipient}",
                refs={"recipient": recipient, "pane_id": pane_id},
                data={"cap": respawn_cap, "window_s": respawn_window_s},
            )
            if recipient != "manager":
                _inbox_write_and_maybe_nudge(
                    paths=paths,
                    run=run,
                    target="manager",
                    message=(
                        f"Sidecar for {recipient} hit respawn cap (cap={respawn_cap}/hr). Pane={pane_id}. See {log_path}"
                    ),
                    sender="team",
                    kind="sidecar",
                    meta_extra={
                        "pane_id": pane_id,
                        "recipient": recipient,
                        "cap": respawn_cap,
                    },
                    nudge=True,
                    force=False,
                    line_info="respawn_cap",
                )
            return TuiResult(
                recipient=recipient,
                run_id=run_id,
                exit_reason="respawn_cap",
            )

        if harness == "opencode":
            # opencode loads `.opencode/plugins` from the project directory.
            # In git worktrees, `.opencode/node_modules` is typically missing because
            # it is gitignored, which can cause opencode to hang/blank.
            try:
                cr = str(os.environ.get("COMPOUND_ROOT") or "").strip()
                if cr:
                    _ensure_opencode_worktree_runtime(
                        workdir=project_dir,
                        repo_root=Path(cr),
                    )
            except Exception:
                pass

        child_env = os.environ.copy()
        user_agent_prompt = _agent_prompt_text(workdir=project_dir, agent=agent)
        wrapped_prompt = _compose_wrapped_agent_prompt(
            protocol_preamble=prompt,
            user_agent_prompt=user_agent_prompt,
        )
        if harness == "opencode":
            child_argv = _opencode_tui_argv(
                project_dir=project_dir,
                agent=agent,
                prompt=wrapped_prompt,
                model=model,
                bin=agent_bin,
            )
        elif harness == "claude":
            child_argv = _claude_tui_argv(
                agent=agent,
                prompt=wrapped_prompt,
                model=model,
                bin=agent_bin,
            )
        elif harness == "codex":
            instructions_dir = paths.run_dir / "agents" / "codex"
            instructions_dir.mkdir(parents=True, exist_ok=True)
            instructions_file = instructions_dir / f"{recipient}.md"
            instructions_file.write_text(
                wrapped_prompt.rstrip() + "\n", encoding="utf-8"
            )
            codex_home = paths.run_dir / "sessions" / "codex" / recipient
            codex_home.mkdir(parents=True, exist_ok=True)
            _seed_codex_home_auth(codex_home=codex_home)
            child_env["CODEX_HOME"] = str(codex_home)
            child_argv = _codex_tui_argv(
                prompt=prompt,
                model=model,
                instructions_file=instructions_file,
                resume_last=has_spawned_once,
                bin=agent_bin,
            )
        else:
            restricted_tools: list[str] | None = None
            if role in (ROLE_MANAGER, ROLE_ARCHITECT, ROLE_INTEGRATOR):
                restricted_tools = [
                    "read",
                    "grep",
                    "find",
                    "bash",
                    "fetch",
                    "web_search",
                    "todo_write",
                ]
            session_dir = paths.run_dir / "sessions" / "omp"
            session_dir.mkdir(parents=True, exist_ok=True)
            session_path = session_dir / f"{recipient}.jsonl"

            child_argv = _omp_tui_argv(
                prompt=prompt,
                model=model,
                system_prompt_append=wrapped_prompt,
                session_path=session_path,
                tools=restricted_tools,
                bin=agent_bin,
            )
        try:
            p = subprocess.Popen(
                child_argv,
                cwd=str(project_dir),
                env=child_env,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
            )
        except Exception as e:
            _append_log_line(log_path, f"{_iso_z()} {harness} spawn failed: {e!r}")
            safe_write_event(
                paths,
                event_type=f"sidecar.{harness}_spawn_failed",
                run=run,
                ok=False,
                summary=f"{harness} spawn failed recipient={recipient}",
                refs={"recipient": recipient, "pane_id": pane_id},
                data={"error": repr(e), "backoff_s": backoff_s},
            )
            time.sleep(min(backoff_s, 30.0))
            backoff_s = min(backoff_s * 2.0, 30.0)
            continue

        with lock:
            proc = p
        has_spawned_once = True

        best_effort(
            lambda: _sidecar_pid_write(
                paths=paths,
                recipient=recipient,
                pid=int(p.pid),
                pane_id=pane_id,
                harness=harness,
                agent_bin=agent_bin,
                argv=child_argv,
                project_dir=project_dir,
                run_id=run_id,
            ),
            label="sidecar.pid.write",
        )

        if not spawn_due_to_bounce:
            respawn_times.append(time.time())
        else:
            bounce_pending.clear()
        _append_log_line(
            log_path,
            f"{_iso_z()} {harness} spawned pid={p.pid} backoff_s={backoff_s}",
        )
        safe_write_event(
            paths,
            event_type=f"sidecar.{harness}_spawned",
            run=run,
            summary=f"{harness} spawned recipient={recipient} pid={p.pid}",
            refs={"recipient": recipient, "pane_id": pane_id},
            data={"pid": int(p.pid), "backoff_s": backoff_s},
        )
        tmux_signal(ch)

        rc = p.wait()
        with lock:
            proc = None

        best_effort(
            lambda: _sidecar_pid_clear(paths=paths, recipient=recipient),
            label="sidecar.pid.clear",
        )

        exit_was_bounce = bool(bounce_killed_pid == p.pid)
        if exit_was_bounce:
            bounce_killed_pid = None

        _append_log_line(log_path, f"{_iso_z()} {harness} exited rc={rc}")
        safe_write_event(
            paths,
            event_type=f"sidecar.{harness}_exited",
            run=run,
            ok=(rc == 0),
            summary=f"{harness} exited recipient={recipient} rc={rc}",
            refs={"recipient": recipient, "pane_id": pane_id},
            data={"rc": int(rc)},
        )

        if recipient != "manager" and not exit_was_bounce:
            _inbox_write_and_maybe_nudge(
                paths=paths,
                run=run,
                target="manager",
                message=f"{harness} exited for {recipient} (rc={rc}); respawning in {backoff_s:.0f}s. Pane={pane_id}",
                sender="team",
                kind="sidecar",
                meta_extra={
                    "pane_id": pane_id,
                    "recipient": recipient,
                    "rc": rc,
                    "backoff_s": round(backoff_s, 3),
                },
                nudge=True,
                force=False,
                line_info="sidecar_exited",
            )

        if exit_was_bounce:
            backoff_s = 1.0
            continue

        wake.wait(timeout=min(backoff_s, 30.0))
        wake.clear()
        backoff_s = min(backoff_s * 2.0, 30.0)


def _default_architect_profile(
    *, run: Mapping[str, Any], harness: str
) -> ResolvedMemberProfile:
    return ResolvedMemberProfile(
        member_id="architect",
        role=ROLE_ARCHITECT,
        lifecycle="always_on",
        source="loom",
        agent=_agent_for_role(run, ROLE_ARCHITECT, harness=harness),
        harness=harness,
        model="",
        workspace="repo_root",
        worktree_key="",
        description="",
        triggers=(),
        primary_workflows=(),
    )


def _always_on_profiles_for_run(run: Mapping[str, Any]) -> list[ResolvedMemberProfile]:
    profiles = list(list_always_on_member_profiles(run))
    if not any(
        str(profile.role or "").strip().lower() == ROLE_ARCHITECT
        for profile in profiles
    ):
        harness = _normalize_harness(str(run.get("harness") or ""))
        profiles.append(_default_architect_profile(run=run, harness=harness))

    deduped: dict[str, ResolvedMemberProfile] = {}
    for profile in profiles:
        member_id = str(profile.member_id or "").strip()
        if not member_id:
            continue
        deduped[member_id] = profile

    return sorted(
        deduped.values(),
        key=lambda profile: (
            0 if str(profile.role or "").strip().lower() == ROLE_ARCHITECT else 1,
            str(profile.member_id or "").strip(),
        ),
    )


def _workspace_for_always_on_profile(profile: ResolvedMemberProfile) -> tuple[str, str]:
    role = str(profile.role or "").strip().lower()
    if role in {ROLE_MANAGER, ROLE_ARCHITECT}:
        return "repo_root", ""
    if role == ROLE_INTEGRATOR:
        return "worktree", "merge-queue"

    workspace = str(profile.workspace or "").strip().lower()
    if workspace not in {"repo_root", "worktree"}:
        workspace = "repo_root"

    worktree_key = sanitize(str(profile.worktree_key or ""), max_len=80) or sanitize(
        str(profile.member_id or ""),
        max_len=80,
    )
    if not worktree_key:
        worktree_key = f"persona-{uuid.uuid4().hex[:8]}"

    return workspace, worktree_key


def _persona_worktree_branch(*, run_id: str, member_id: str) -> str:
    run_key = sanitize(str(run_id or ""), allow=r"a-zA-Z0-9._-", max_len=16) or "run"
    member_key = (
        sanitize(str(member_id or ""), allow=r"a-zA-Z0-9._-", max_len=40) or "persona"
    )
    return f"team/{run_key}-{member_key}"


def _ensure_always_on_personas(*, team: str, repo: Optional[Path] = None) -> None:
    paths = _paths_for(team=team, repo=repo)

    with locked_run(paths) as run:
        session = run_session(run)
        if not tmux_has_session(session):
            raise TeamError(
                f"tmux session not found while ensuring always-on roster: {session}",
                code="TMUX",
                exit_code=2,
            )

        root = run_root(paths, run)
        tickets_dir = ensure_run_tickets_dir(run, repo_root=root)
        sprint = _objective_state_sprint_state(run)
        defaults = run.get("defaults") if isinstance(run.get("defaults"), dict) else {}
        base_ref_default = str((defaults or {}).get("base_ref") or "").strip() or None

        harness_default = _normalize_harness(str(run.get("harness") or ""))
        raw_mounts = run.get("mounts")
        mounts: list[dict] = []
        if isinstance(raw_mounts, list):
            mounts = [dict(item) for item in raw_mounts if isinstance(item, dict)]

        now_iso = _iso_z()
        workers = dict(run.get("workers") or {})

        for profile in _always_on_profiles_for_run(run):
            role = str(profile.role or "").strip().lower()
            if role in {ROLE_MANAGER, ROLE_INTEGRATOR}:
                continue

            member_id = sanitize(str(profile.member_id or ""), max_len=48)
            if not member_id:
                continue

            workspace, workspace_key = _workspace_for_always_on_profile(profile)
            persona_harness = _normalize_harness(
                str(profile.harness or "") or harness_default
            )
            cfg = (
                (run.get(persona_harness) or {})
                if isinstance(run.get(persona_harness), dict)
                else (run.get("opencode") or {})
            )
            agent_bin = str(cfg.get("bin") or "").strip() or persona_harness
            _require_bin(agent_bin)

            agent = str(profile.agent or "").strip() or _agent_for_role(
                run,
                role,
                harness=persona_harness,
            )
            project_dir = root
            branch = ""
            base = ""
            worktree_key = ""

            if workspace == "worktree":
                worktree_key = workspace_key
                desired_wt_path = (paths.worktrees_dir / worktree_key).resolve()
                if not _is_path_within(paths.worktrees_dir, desired_wt_path):
                    raise TeamError(
                        f"Refusing to create worktree outside run worktrees dir: {desired_wt_path}",
                        code="WORKTREE_PATH",
                        exit_code=2,
                    )

                wt = _ensure_worktree(
                    cwd=root,
                    path=desired_wt_path,
                    branch=_persona_worktree_branch(
                        run_id=str(run.get("run_id") or ""),
                        member_id=member_id,
                    ),
                    base_ref=base_ref_default,
                    allow_dirty=True,
                )
                project_dir = Path(str(wt.get("path") or desired_wt_path)).resolve()
                branch = str(wt.get("branch") or "").strip()
                base = str(wt.get("base") or "").strip()
                _apply_mounts(repo_root=root, worktree_root=project_dir, mounts=mounts)
                if persona_harness == "opencode":
                    _ensure_opencode_worktree_runtime(
                        workdir=project_dir, repo_root=root
                    )

            _require_agent_file_present(
                workdir=project_dir,
                harness=persona_harness,
                agent=agent,
            )
            model = _model_for_role(run, role, harness=persona_harness)
            if not model and profile.model:
                model = str(profile.model)

            if role == ROLE_ARCHITECT:
                prompt = render_architect_prompt(
                    run=run,
                    worker_id=member_id,
                    charter_path=paths.charter_file,
                )
            else:
                prompt = render_persona_prompt(
                    run=run,
                    role=role,
                    worker_id=member_id,
                    charter_path=paths.charter_file,
                    description=str(profile.description or ""),
                    triggers=list(profile.triggers),
                    primary_workflows=list(profile.primary_workflows),
                )

            oc_argv = _team_tui_argv(
                project_dir=project_dir,
                agent=agent,
                prompt=prompt,
                model=model,
                harness=persona_harness,
                bin=str(cfg.get("bin") or "").strip(),
            )

            pane_env = {
                ENV_TICKET_DIR: str(tickets_dir),
                ENV_TEAM_NAME: str(run.get("team") or paths.team),
                ENV_TEAM_RUN_ID: str(run.get("run_id") or ""),
                ENV_TEAM_RUN_DIR: str(paths.run_dir),
                ENV_TEAM_ROLE: role,
                ENV_TEAM_WORKER_ID: member_id,
                ENV_TEAM_TICKET_ID: "",
                ENV_TEAM_SPRINT_NAME: sprint.get("name", ""),
                ENV_TEAM_SPRINT_TAG: sprint.get("tag", ""),
                "COMPOUND_ROOT": str(root),
            }

            existing = dict(workers.get(member_id) or {})
            existing_window = str(existing.get("window") or "").strip()
            pane_id = ""
            window = existing_window

            if (
                window
                and not bool(existing.get("retired"))
                and tmux_window_exists(session, window)
            ):
                pane_id = tmux_format(f"{session}:{window}", "#{pane_id}")
            else:
                desired_window = (
                    sanitize(
                        existing_window or member_id,
                        allow=r"a-zA-Z0-9._-",
                        max_len=60,
                    )
                    or member_id
                )
                window = tmux_unique_window_name(session, desired_window)
                tmux_cmd(
                    [
                        "new-window",
                        "-d",
                        "-t",
                        session,
                        "-n",
                        window,
                        "-c",
                        str(project_dir),
                        *tmux_env_flags(pane_env),
                        *oc_argv,
                    ],
                    check=True,
                )
                pane_id = tmux_format(f"{session}:{window}", "#{pane_id}")
                if pane_id:
                    tmux_mark_pane(
                        pane_id=pane_id,
                        role=role,
                        worker_id=member_id,
                        ticket_id="",
                    )

            workers[member_id] = {
                **existing,
                "worker_id": member_id,
                "role": role,
                "ticket_id": "",
                "roster_member_id": str(profile.member_id or ""),
                "roster_source": str(profile.source or ""),
                "roster_lifecycle": str(profile.lifecycle or ""),
                "roster_description": str(profile.description or ""),
                "roster_triggers": list(profile.triggers),
                "roster_primary_workflows": list(profile.primary_workflows),
                "window": window,
                "pane_id": pane_id,
                "workspace": workspace,
                "worktree": str(project_dir),
                "worktree_key": worktree_key,
                "branch": branch,
                "base": base,
                "created_at": str(existing.get("created_at") or now_iso),
                "spawned_at": str(existing.get("spawned_at") or now_iso),
                "revived_at": now_iso
                if bool(existing.get("retired"))
                else str(existing.get("revived_at") or ""),
                "retired": False,
                "retired_at": "",
                "worktree_retirable": False,
                "worktree_retirable_at": "",
            }

        run["workers"] = workers


# -----------------------------
# Prompt construction (initial --prompt only)
# -----------------------------


def start(
    *,
    team: str,
    objective: str = "",
    roster: str = "",
    session: str = "",
    harness: str = "",
    bin_override: str = "",
    model: str = "",
    manager_model: str = "",
    architect_model: str = "",
    worker_model: str = "",
    integrator_model: str = "",
    mounts: Optional[list[str]] = None,
    clear_mounts: bool = False,
    target_branch: str = "",
    remote: str = "",
    push: Optional[bool] = None,
    max_headcount: Optional[int] = None,
    manager_window: str = DEFAULT_MANAGER_WINDOW,
    force: bool = False,
    repo: Optional[Path] = None,
) -> StartResult:
    _require_bin("tmux")
    _deny_if_role_set(action="loom team start")

    if max_headcount is not None:
        max_headcount = int(max_headcount)
        if max_headcount < 0:
            raise TeamError(
                f"Invalid max headcount: {max_headcount}",
                code="ARG",
                exit_code=2,
                hint="Use --max-headcount 0 for unlimited, or a positive integer.",
            )
    harness_raw = str(harness or "")
    harness_provided = bool(harness_raw.strip())
    requested_harness = _normalize_harness(harness_raw)
    requested_bin = str(bin_override or "").strip()

    roster_state: Optional[Dict[str, Any]] = None
    roster_harness = ""
    roster_raw = str(roster or "").strip()
    if roster_raw:
        roster_path = Path(roster_raw).expanduser()
        parsed = load_team_roster_yaml(roster_path)
        roster_state = {
            "source": str(roster_path.resolve()),
            "loaded_at": _iso_z(),
            "spec": parsed.as_dict(),
        }
        manager_profile = resolve_builtin_profile(
            {"roster": roster_state},
            ROLE_MANAGER,
        )
        enforce_member_lifecycle(profile=manager_profile, role=ROLE_MANAGER)
        if manager_profile is not None and manager_profile.harness:
            roster_harness = _normalize_harness(manager_profile.harness)

    # Precedence: explicit CLI override > roster > defaults.
    if not harness_provided and roster_harness:
        requested_harness = roster_harness
    root = canonical_repo_root(repo.resolve() if repo else Path.cwd())
    team = sanitize(team or "", max_len=80) or default_team_name(root)
    # Session selection rules:
    #   - If --session is provided, it wins (and updates run.json).
    #   - Otherwise, prefer an existing run.json session (for idempotent start/resume).
    #   - Fallback: team-<team>.
    session_raw = str(session or "")
    session_provided = bool(session_raw.strip())
    session = sanitize(
        session_raw or f"{DEFAULT_TMUX_SESSION_PREFIX}-{team}",
        max_len=120,
    )

    paths = RunPaths(repo_root=root, team=team)
    paths.run_dir.mkdir(parents=True, exist_ok=True)
    paths.worktrees_dir.mkdir(parents=True, exist_ok=True)
    paths.inbox_dir.mkdir(parents=True, exist_ok=True)
    paths.inbox_read_dir.mkdir(parents=True, exist_ok=True)
    paths.merge_dir.mkdir(parents=True, exist_ok=True)
    paths.sidecars_dir.mkdir(parents=True, exist_ok=True)
    paths.events_dir.mkdir(parents=True, exist_ok=True)
    paths.artifacts_dir.mkdir(parents=True, exist_ok=True)
    paths.snapshots_dir.mkdir(parents=True, exist_ok=True)
    paths.captures_dir.mkdir(parents=True, exist_ok=True)

    created = False
    with FileLock(paths.lock_file):
        if paths.run_file.exists():
            run = load_run(paths)
            run["merge"] = _merge_state(run)
            if not isinstance(run.get("sprint"), dict):
                run["sprint"] = {}
            if roster_state is not None:
                run["roster"] = roster_state
                save_run(paths, run)

            # Mounts: persisted across start/resume.
            # Precedence:
            # - CLI: --clear-mounts / --mount ...
            # - Roster: spec.mounts
            # - Existing run state
            if bool(clear_mounts):
                run["mounts"] = []
                save_run(paths, run)
            elif mounts is not None:
                run["mounts"] = _parse_mount_specs(
                    repo_root=root,
                    paths=paths,
                    specs=list(mounts),
                )
                save_run(paths, run)
            else:
                roster_mount_specs = _roster_mount_specs_from_run(run)
                if roster_mount_specs:
                    run["mounts"] = _parse_mount_specs(
                        repo_root=root,
                        paths=paths,
                        specs=roster_mount_specs,
                    )
                    save_run(paths, run)
                else:
                    raw_mounts = run.get("mounts")
                    if not isinstance(raw_mounts, list):
                        run["mounts"] = []
                        save_run(paths, run)

            if max_headcount is not None:
                raw_limits = run.get("limits")
                limits: Dict[str, Any] = (
                    dict(raw_limits) if isinstance(raw_limits, dict) else {}
                )
                limits["max_headcount"] = max_headcount
                run["limits"] = limits
                save_run(paths, run)

            # Merge/ship config (fail-forward, always visible).
            ms = _merge_state(run)
            cfg = dict(ms.get("config") or {})
            tb = str(target_branch or "").strip()
            rm = str(remote or "").strip()
            if tb:
                st = sanitize(tb, allow=r"a-zA-Z0-9._/-", max_len=120)
                if not st:
                    raise TeamError(
                        f"Invalid target branch: {tb}", code="ARG", exit_code=2
                    )
                cfg["target_branch"] = st
            if rm:
                sr = sanitize(rm, allow=r"a-zA-Z0-9._/-", max_len=80)
                if not sr:
                    raise TeamError(f"Invalid remote: {rm}", code="ARG", exit_code=2)
                cfg["remote"] = sr
            if push is not None:
                cfg["push"] = bool(push)
            # Migration: old runs defaulted push=False; new default is push=True.
            if push is None and bool(cfg.get("push")) is False:
                cfg["push"] = True
            if "push" not in cfg:
                cfg["push"] = True
            ms["config"] = cfg
            run["merge"] = ms

            # Ensure merge-queue branch is stable per run.
            ms["branch"] = merge_branch_for_run(run)
            run["merge"] = ms

            # Defaults: new workers branch off the merge target by default.
            raw_defaults = run.get("defaults")
            defaults: Dict[str, Any] = {}
            if isinstance(raw_defaults, dict):
                defaults.update(raw_defaults)
            if tb:
                defaults["base_ref"] = cfg.get("target_branch")
            defaults.setdefault("base_ref", str(cfg.get("target_branch") or "main"))
            run["defaults"] = defaults

            existing_harness = _normalize_harness(str(run.get("harness") or ""))
            if harness_provided:
                if str(run.get("harness") or "") != requested_harness:
                    run["harness"] = requested_harness
                    save_run(paths, run)
            elif roster_harness:
                if str(run.get("harness") or "") != requested_harness:
                    run["harness"] = requested_harness
                    save_run(paths, run)
            if requested_bin:
                bin_harness = (
                    requested_harness
                    if (harness_provided or roster_harness)
                    else existing_harness
                )
                cfg = run.get(bin_harness)
                if not isinstance(cfg, dict):
                    cfg = {}
                if str(cfg.get("bin") or "") != requested_bin:
                    cfg["bin"] = requested_bin
                    run[bin_harness] = cfg
                    save_run(paths, run)

            # Normalize harness config keys (greenfield, but keep local runs usable).
            for hname in ("opencode", "claude", "omp", "codex"):
                raw_cfg = run.get(hname)
                cfg = dict(raw_cfg) if isinstance(raw_cfg, dict) else {}

                # Agent key migration: merge -> integrator.
                if "integrator_agent" not in cfg:
                    if "merge_agent" in cfg:
                        cfg["integrator_agent"] = cfg.pop("merge_agent")
                    else:
                        cfg["integrator_agent"] = DEFAULT_INTEGRATOR_AGENT

                cfg.setdefault("manager_agent", DEFAULT_MANAGER_AGENT)
                cfg.setdefault("worker_agent", DEFAULT_WORKER_AGENT)
                cfg.setdefault("architect_agent", DEFAULT_ARCHITECT_AGENT)
                cfg.setdefault("bin", str(cfg.get("bin") or ""))

                raw_models = cfg.get("models")
                models: Dict[str, str] = (
                    dict(raw_models) if isinstance(raw_models, dict) else {}
                )
                for rk in (
                    ROLE_MANAGER,
                    ROLE_WORKER,
                    ROLE_ARCHITECT,
                    ROLE_INTEGRATOR,
                ):
                    models.setdefault(rk, "")
                cfg["models"] = models

                # Preserve existing global model key.
                cfg.setdefault("model", str(cfg.get("model") or "").strip())
                run[hname] = cfg

            # Normalize worker roles: merge -> integrator.
            if isinstance(run.get("workers"), dict):
                workers = dict(run.get("workers") or {})
                changed = False
                for wid, w in workers.items():
                    if not isinstance(w, dict):
                        continue
                    if str(w.get("role") or "").strip().lower() == "merge":
                        w2 = dict(w)
                        w2["role"] = ROLE_INTEGRATOR
                        workers[wid] = w2
                        changed = True
                if changed:
                    run["workers"] = workers

            # Apply model overrides (existing runs used to ignore these).
            update_harness = requested_harness if harness_provided else existing_harness
            raw_update_cfg = run.get(update_harness)
            if not isinstance(raw_update_cfg, dict):
                raw_update_cfg = run.get("opencode")
            update_cfg: Dict[str, Any] = (
                dict(raw_update_cfg) if isinstance(raw_update_cfg, dict) else {}
            )

            if str(model or "").strip():
                update_cfg["model"] = str(model).strip()

            raw_models_map = update_cfg.get("models")
            models_map: Dict[str, str] = (
                dict(raw_models_map) if isinstance(raw_models_map, dict) else {}
            )
            if str(manager_model or "").strip():
                models_map[ROLE_MANAGER] = str(manager_model).strip()
            if str(worker_model or "").strip():
                models_map[ROLE_WORKER] = str(worker_model).strip()
            if str(architect_model or "").strip():
                models_map[ROLE_ARCHITECT] = str(architect_model).strip()
            if str(integrator_model or "").strip():
                models_map[ROLE_INTEGRATOR] = str(integrator_model).strip()
            update_cfg["models"] = models_map

            run[update_harness] = update_cfg

            save_run(paths, run)

            # Adopt persisted session unless the caller explicitly overrides.
            persisted = sanitize(str(run.get("session") or ""), max_len=120)
            if not session_provided and persisted:
                session = persisted
            elif session_provided:
                run["session"] = session
        else:
            created = True
            created_at = _iso_z()

            tb = str(target_branch or "").strip() or "main"
            rm = str(remote or "").strip() or "origin"
            tb = sanitize(tb, allow=r"a-zA-Z0-9._/-", max_len=120) or "main"
            rm = sanitize(rm, allow=r"a-zA-Z0-9._/-", max_len=80) or "origin"
            push_default = True if push is None else bool(push)

            run = {
                "version": 1,
                "run_id": uuid.uuid4().hex,
                "team": team,
                "created_at": created_at,
                "harness": requested_harness,
                "objective": str(objective or "").strip(),
                "objective_rev": 1,
                "objective_updated_at": created_at,
                "done_reminder": {},
                "sprint": {},
                "repo_root": str(root),
                "run_dir": str(paths.run_dir),
                "session": session,
                "manager": {},
                "workers": {},
                "mounts": [],
                "limits": {
                    "max_headcount": max_headcount if max_headcount is not None else 0,
                },
                "merge": {
                    "items": [],
                    "branch": "",
                    "config": {
                        "target_branch": tb,
                        "remote": rm,
                        "push": bool(push_default),
                    },
                },
                "defaults": {
                    "base_ref": tb,
                },
                "opencode": {
                    "model": str(model or "").strip(),
                    "models": {
                        "manager": "",
                        "worker": "",
                        "architect": "",
                        "integrator": "",
                    },
                    "manager_agent": DEFAULT_MANAGER_AGENT,
                    "worker_agent": DEFAULT_WORKER_AGENT,
                    "architect_agent": DEFAULT_ARCHITECT_AGENT,
                    "integrator_agent": DEFAULT_INTEGRATOR_AGENT,
                    "bin": "",
                },
                "claude": {
                    "model": str(model or "").strip(),
                    "models": {
                        "manager": "",
                        "worker": "",
                        "architect": "",
                        "integrator": "",
                    },
                    "manager_agent": DEFAULT_MANAGER_AGENT,
                    "worker_agent": DEFAULT_WORKER_AGENT,
                    "architect_agent": DEFAULT_ARCHITECT_AGENT,
                    "integrator_agent": DEFAULT_INTEGRATOR_AGENT,
                    "bin": "",
                },
                "omp": {
                    "model": str(model or "").strip(),
                    "models": {
                        "manager": "",
                        "worker": "",
                        "architect": "",
                        "integrator": "",
                    },
                    "manager_agent": DEFAULT_MANAGER_AGENT,
                    "worker_agent": DEFAULT_WORKER_AGENT,
                    "architect_agent": DEFAULT_ARCHITECT_AGENT,
                    "integrator_agent": DEFAULT_INTEGRATOR_AGENT,
                    "bin": "",
                },
                "codex": {
                    "model": str(model or "").strip(),
                    "models": {
                        "manager": "",
                        "worker": "",
                        "architect": "",
                        "integrator": "",
                    },
                    "manager_agent": DEFAULT_MANAGER_AGENT,
                    "worker_agent": DEFAULT_WORKER_AGENT,
                    "architect_agent": DEFAULT_ARCHITECT_AGENT,
                    "integrator_agent": DEFAULT_INTEGRATOR_AGENT,
                    "bin": "",
                },
            }
            if roster_state is not None:
                run["roster"] = roster_state

            # Apply per-role model overrides to the selected harness.
            cfg = dict(run.get(requested_harness) or {})
            raw_models_created = cfg.get("models")
            models_created = (
                dict(raw_models_created) if isinstance(raw_models_created, dict) else {}
            )
            if str(manager_model or "").strip():
                models_created[ROLE_MANAGER] = str(manager_model).strip()
            if str(worker_model or "").strip():
                models_created[ROLE_WORKER] = str(worker_model).strip()
            if str(architect_model or "").strip():
                models_created[ROLE_ARCHITECT] = str(architect_model).strip()
            if str(integrator_model or "").strip():
                models_created[ROLE_INTEGRATOR] = str(integrator_model).strip()
            cfg["models"] = models_created
            run[requested_harness] = cfg

            if requested_bin:
                cfg = dict((run.get(requested_harness) or {}))
                cfg["bin"] = requested_bin
                run[requested_harness] = cfg

            if bool(clear_mounts):
                run["mounts"] = []
            elif mounts is not None:
                run["mounts"] = _parse_mount_specs(
                    repo_root=root,
                    paths=paths,
                    specs=list(mounts),
                )
            else:
                roster_mount_specs = _roster_mount_specs_from_run(run)
                if roster_mount_specs:
                    run["mounts"] = _parse_mount_specs(
                        repo_root=root,
                        paths=paths,
                        specs=roster_mount_specs,
                    )
            # Per-run merge branch: stable, disposable, and derived from run_id.
            ms = _merge_state(run)
            ms["branch"] = merge_branch_for_run(run)
            run["merge"] = ms

            save_run(paths, run)

        # If session was updated via adoption, persist it back.
        if str(run.get("session") or "") != session:
            run["session"] = session
            save_run(paths, run)

        # Resolve & persist the canonical loom ticket directory (centralized in the repo root).
        tickets_dir = resolve_tickets_dir(repo_root=root)
        if str(run.get("tickets_dir") or "") != str(tickets_dir):
            run["tickets_dir"] = str(tickets_dir)
            save_run(paths, run)

        # Ensure Charter and Team agents (repo root, committed artifacts).
        charter_path = _write_charter(paths=paths, run=run)
        agents_res = init_agents(repo=root, create_missing=False)
        if agents_res.missing:
            missing = ", ".join(agents_res.missing[:6])
            more = (
                ""
                if len(agents_res.missing) <= 6
                else f" (+{len(agents_res.missing) - 6} more)"
            )
            raise TeamError(
                f"Team agents not initialized (missing: {missing}{more})",
                code="AGENTS",
                exit_code=2,
                hint=(
                    f"Run: loom team init --repo {root}\n"
                    "Then commit the generated agent files before starting the team."
                ),
            )

        # Ensure tmux session and manager window
        manager_window = (
            sanitize(
                str(manager_window or ""),
                allow=r"a-zA-Z0-9._-",
                max_len=60,
            )
            or DEFAULT_MANAGER_WINDOW
        )
        harness = _normalize_harness(str(run.get("harness") or requested_harness))
        manager_profile = resolve_builtin_profile(
            run,
            ROLE_MANAGER,
        )
        enforce_member_lifecycle(profile=manager_profile, role=ROLE_MANAGER)
        if manager_profile is not None and manager_profile.harness:
            harness = _normalize_harness(manager_profile.harness)
        cfg = (
            (run.get(harness) or {})
            if isinstance(run.get(harness), dict)
            else (run.get("opencode") or {})
        )
        agent_bin = str(cfg.get("bin") or "").strip() or harness
        _require_bin(agent_bin)
        model = _model_for_role(run, ROLE_MANAGER, harness=harness)
        if not model and manager_profile is not None and manager_profile.model:
            model = str(manager_profile.model)
        manager_agent = (
            str(manager_profile.agent)
            if manager_profile is not None
            else str(cfg.get("manager_agent") or DEFAULT_MANAGER_AGENT)
        )
        manager_prompt = render_manager_prompt(run=run, charter_path=charter_path)
        oc_argv = _team_tui_argv(
            project_dir=root,
            agent=manager_agent,
            prompt=manager_prompt,
            model=model,
            harness=harness,
            bin=str(cfg.get("bin") or "").strip(),
        )

        sprint = _objective_state_sprint_state(run)
        pane_env = {
            ENV_TICKET_DIR: str(tickets_dir),
            ENV_TEAM_NAME: team,
            ENV_TEAM_RUN_ID: str(run.get("run_id") or ""),
            ENV_TEAM_RUN_DIR: str(paths.run_dir),
            ENV_TEAM_ROLE: ROLE_MANAGER,
            ENV_TEAM_WORKER_ID: "",
            ENV_TEAM_TICKET_ID: "",
            ENV_TEAM_SPRINT_NAME: sprint.get("name", ""),
            ENV_TEAM_SPRINT_TAG: sprint.get("tag", ""),
            "COMPOUND_ROOT": str(root),
        }

        if not tmux_has_session(session):
            tmux_cmd(
                [
                    "new-session",
                    "-d",
                    "-s",
                    session,
                    "-n",
                    manager_window,
                    "-c",
                    str(root),
                    *tmux_env_flags(pane_env),
                    *oc_argv,
                ],
                check=True,
            )
        else:
            # If session exists, ensure manager window exists.
            if tmux_window_exists(session, manager_window) and bool(force):
                tmux_kill_window(session, manager_window)

            if not tmux_window_exists(session, manager_window):
                tmux_cmd(
                    [
                        "new-window",
                        "-d",
                        "-t",
                        session,
                        "-n",
                        manager_window,
                        "-c",
                        str(root),
                        *tmux_env_flags(pane_env),
                        *oc_argv,
                    ],
                    check=True,
                )

        # Mark ownership and manager pane.
        tmux_set_option(target=session, option=TMUX_OPT_OWNED, value="1")
        tmux_set_option(target=session, option=TMUX_OPT_TEAM, value=team)
        tmux_set_option(
            target=session, option=TMUX_OPT_RUN_ID, value=str(run.get("run_id") or "")
        )
        tmux_set_option(
            target=session, option=TMUX_OPT_RUN_DIR, value=str(paths.run_dir)
        )
        tmux_set_option(target=session, option=TMUX_OPT_REPO_ROOT, value=str(root))

        # Observability defaults.
        tmux_cmd(["set-option", "-t", session, "history-limit", "200000"], check=False)
        tmux_cmd(["set-option", "-t", session, "remain-on-exit", "on"], check=False)
        tmux_cmd(["set-option", "-t", session, "allow-rename", "off"], check=False)

        manager_pane = tmux_format(f"{session}:{manager_window}", "#{pane_id}")
        if manager_pane:
            tmux_mark_pane(pane_id=manager_pane, role=ROLE_MANAGER)

        run["session"] = session
        run["manager"] = {
            "window": manager_window,
            "pane_id": manager_pane,
        }

        # Help UIs/agents see the ship destination immediately.
        try:
            ms = _merge_state(run)
            cfg = dict(ms.get("config") or {})
            tb = str(cfg.get("target_branch") or "main").strip() or "main"
            rm = str(cfg.get("remote") or "origin").strip() or "origin"
            p = bool(cfg.get("push"))
            mgr = dict(run.get("manager") or {})
            mgr["merge_target"] = f"{rm}/{tb} push={p}"
            run["manager"] = mgr
        except Exception:
            pass
        save_run(paths, run)

        write_event(
            paths,
            event_type=("run.created" if created else "run.resumed"),
            run=run,
            summary=f"{('Created' if created else 'Resumed')} run session={session}",
            refs={"tmux_session": session, "manager_pane_id": manager_pane},
            data={
                "objective": str(run.get("objective") or ""),
                "repo_root": str(run.get("repo_root") or ""),
                "tickets_dir": str(run.get("tickets_dir") or ""),
                "manager_window": manager_window,
                "model": str((run.get("opencode") or {}).get("model") or ""),
            },
        )

    if tmux_has_session(session):
        spawn_integrator(team=paths.team, repo=root)
        _ensure_always_on_personas(team=paths.team, repo=root)

    run = load_run(paths)
    return StartResult(
        team=team,
        session=session,
        run_id=str(run.get("run_id") or ""),
        run_dir=str(paths.run_dir),
        repo_root=str(root),
        tickets_dir=str(run.get("tickets_dir") or ""),
        manager=dict(run.get("manager") or {}),
        charter=str((paths.run_dir / "CHARTER.md").resolve()),
        created=created,
    )


def attach(*, team: str) -> AttachResult:
    _require_bin("tmux")
    _deny_if_role_set(action="loom team attach")
    team_or_session = str(team).strip()
    if not team_or_session:
        raise TeamError("Missing <team>", code="ARG", exit_code=2)

    # Prefer explicit session if it exists.
    session = team_or_session
    if not tmux_has_session(session):
        session = (
            f"{DEFAULT_TMUX_SESSION_PREFIX}-{sanitize(team_or_session, max_len=80)}"
        )

    if not tmux_has_session(session):
        raise TeamError(
            f"tmux session not found: {team_or_session}", code="TMUX", exit_code=2
        )

    # Best-effort: land on manager window.
    manager_window = DEFAULT_MANAGER_WINDOW
    try:
        rd = tmux_get_option(target=session, option=TMUX_OPT_RUN_DIR)
        if rd:
            run_file = Path(rd).expanduser().resolve() / "run.json"
            if run_file.exists():
                run = _read_json(run_file)
                if isinstance(run, dict):
                    mgr = (
                        run.get("manager")
                        if isinstance(run.get("manager"), dict)
                        else {}
                    )
                    manager_window = str((mgr or {}).get("window") or manager_window)
    except Exception:
        pass
    tmux_select_window(session, manager_window)

    return AttachResult(
        team=resolve_team_from_session(session),
        session=session,
        manager_window=manager_window,
    )


# -----------------------------
# Objective + completion + janitor
# -----------------------------


def _parse_rfc3339(ts: str) -> Optional[dt.datetime]:
    raw = str(ts or "").strip()
    if not raw:
        return None
    s = raw.replace("Z", "+00:00")
    try:
        return dt.datetime.fromisoformat(s)
    except Exception:
        return None


def _epoch(ts: Optional[dt.datetime]) -> float:
    if not ts:
        return 0.0
    try:
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=dt.timezone.utc)
        return ts.timestamp()
    except Exception:
        return 0.0


def objective_show(*, team: str, repo: Optional[Path] = None) -> ObjectiveShowResult:
    paths = _paths_for(team=team, repo=repo)
    run = load_run(paths)
    return _objective_state_objective_show(paths=paths, run=run)


def objective_set(
    *,
    team: str,
    message: str = "",
    file_path: str = "",
    stdin_ok: bool = False,
    nudge: bool = True,
    force: bool = False,
    repo: Optional[Path] = None,
) -> ObjectiveUpdateResult:
    _require_role(action="loom team objective set", allowed_roles={ROLE_MANAGER})
    paths = _paths_for(team=team, repo=repo)
    text = _objective_state_read_text_input(
        message=str(message or ""),
        file_path=str(file_path or ""),
        stdin_ok=bool(stdin_ok),
    )
    with locked_run(paths) as run:
        now = _iso_z()
        payload = _objective_state_apply_objective_mutation(
            run=run,
            mode="set",
            text=text,
            now=now,
        )
        charter_path = _write_charter(paths=paths, run=run)

        msg = (
            f"Objective replaced (rev={run['objective_rev']}) at {now}.\n\n"
            f"Team: {paths.team}\n"
            f"Charter: {charter_path}\n\n"
            "Next actions (manager):\n"
            "- Re-read CHARTER and pivot immediately.\n"
            "- Map objective -> tickets (loom ticket).\n"
            "- If no crisp tickets exist: spawn an Architect to produce a ticket set.\n"
            "- When 100% done (tickets closed + merges shipped): disband the team.\n\n"
            "Current objective:\n"
            f"{str(run.get('objective') or '').strip()}\n"
        )
        inbox_msg, _recipient, nudged, reason, _meta = _inbox_write_and_maybe_nudge(
            paths=paths,
            run=run,
            target="manager",
            message=msg,
            sender="team",
            kind="objective",
            meta_extra={"objective_rev": int(run.get("objective_rev") or 0), "mode": "set"},
            nudge=bool(nudge),
            force=bool(force),
            line_info=f"objective_set rev={run['objective_rev']}",
        )
        write_event(
            paths,
            event_type="objective.updated",
            run=run,
            summary=f"Objective set rev={run['objective_rev']} nudged={nudged}",
            refs={
                "objective_rev": int(run.get("objective_rev") or 0),
                "inbox_id": str(inbox_msg.get("id") or ""),
            },
            data={"mode": "set", "nudged": bool(nudged), "nudge_reason": reason},
        )
        payload.update(
            {
                "team": paths.team,
                "charter": str(charter_path.resolve()),
                "inbox_id": str(inbox_msg.get("id") or ""),
                "nudged": bool(nudged),
            }
        )
    return ObjectiveUpdateResult(
        team=str(payload.get("team") or paths.team),
        mode="set",
        objective_rev=int(payload.get("objective_rev") or 0),
        objective_updated_at=str(payload.get("objective_updated_at") or ""),
        charter=str(payload.get("charter") or ""),
        inbox_id=str(payload.get("inbox_id") or ""),
        nudged=bool(payload.get("nudged")),
    )


def objective_append(
    *,
    team: str,
    message: str = "",
    file_path: str = "",
    stdin_ok: bool = False,
    nudge: bool = True,
    force: bool = False,
    repo: Optional[Path] = None,
) -> ObjectiveUpdateResult:
    _require_role(action="loom team objective append", allowed_roles={ROLE_MANAGER})
    paths = _paths_for(team=team, repo=repo)
    text = _objective_state_read_text_input(
        message=str(message or ""),
        file_path=str(file_path or ""),
        stdin_ok=bool(stdin_ok),
    )
    with locked_run(paths) as run:
        now = _iso_z()
        payload = _objective_state_apply_objective_mutation(
            run=run,
            mode="append",
            text=text,
            now=now,
        )
        charter_path = _write_charter(paths=paths, run=run)

        msg = (
            f"Objective appended (rev={run['objective_rev']}) at {now}.\n\n"
            f"Team: {paths.team}\n"
            f"Charter: {charter_path}\n\n"
            "Next actions (manager):\n"
            "- Re-read CHARTER and pivot immediately.\n"
            "- Map objective -> tickets (loom ticket).\n"
            "- If no crisp tickets exist: spawn an Architect to produce a ticket set.\n"
            "- When 100% done (tickets closed + merges shipped): disband the team.\n\n"
            "Current objective:\n"
            f"{str(run.get('objective') or '').strip()}\n"
        )
        inbox_msg, _recipient, nudged, reason, _meta = _inbox_write_and_maybe_nudge(
            paths=paths,
            run=run,
            target="manager",
            message=msg,
            sender="team",
            kind="objective",
            meta_extra={
                "objective_rev": int(run.get("objective_rev") or 0),
                "mode": "append",
            },
            nudge=bool(nudge),
            force=bool(force),
            line_info=f"objective_append rev={run['objective_rev']}",
        )
        write_event(
            paths,
            event_type="objective.updated",
            run=run,
            summary=f"Objective append rev={run['objective_rev']} nudged={nudged}",
            refs={
                "objective_rev": int(run.get("objective_rev") or 0),
                "inbox_id": str(inbox_msg.get("id") or ""),
            },
            data={"mode": "append", "nudged": bool(nudged), "nudge_reason": reason},
        )
        payload.update(
            {
                "team": paths.team,
                "charter": str(charter_path.resolve()),
                "inbox_id": str(inbox_msg.get("id") or ""),
                "nudged": bool(nudged),
            }
        )
    return ObjectiveUpdateResult(
        team=str(payload.get("team") or paths.team),
        mode="append",
        objective_rev=int(payload.get("objective_rev") or 0),
        objective_updated_at=str(payload.get("objective_updated_at") or ""),
        charter=str(payload.get("charter") or ""),
        inbox_id=str(payload.get("inbox_id") or ""),
        nudged=bool(payload.get("nudged")),
    )


def _compute_done_locked(
    *,
    run: Dict[str, Any],
    tickets_dir: Path,
) -> Tuple[bool, Dict[str, Any]]:
    # Conservative definition: false negatives > false positives.
    ms = _merge_state(run)
    merge_items = [i for i in (ms.get("items") or []) if isinstance(i, dict)]
    pending = [
        i for i in merge_items if str(i.get("state") or "") in ("queued", "claimed")
    ]
    unshipped = [
        i
        for i in merge_items
        if str(i.get("state") or "") == "done"
        and str(i.get("result") or "") == "merged"
        and not str(i.get("shipped_at") or "").strip()
    ]
    blocked = [
        i
        for i in merge_items
        if str(i.get("state") or "") == "done"
        and str(i.get("result") or "") == "blocked"
    ]

    active_workers = []
    ticket_ids: List[str] = []
    for wid, w in (run.get("workers") or {}).items():
        if not isinstance(w, dict):
            continue
        role = str(w.get("role") or "")
        if role == ROLE_INTEGRATOR:
            continue
        if not bool(w.get("retired")):
            active_workers.append(wid)
        tid = str(w.get("ticket_id") or "").strip()
        if tid:
            ticket_ids.append(tid)
    ticket_ids = sorted(set(ticket_ids))

    detail: Dict[str, Any] = {
        "merge_pending": len(pending),
        "merge_unshipped": len(unshipped),
        "merge_blocked": len(blocked),
        "active_workers": list(active_workers),
        "ticket_ids": list(ticket_ids),
        "tickets": {},
    }

    if pending or unshipped or blocked or active_workers:
        return False, detail

    if not ticket_ids:
        detail["reason"] = "no_tracked_tickets"
        return False, detail

    for tid in ticket_ids:
        try:
            ticket = ticket_show(ticket_id=tid, tickets_dir=tickets_dir)
            status = str(ticket.ticket.status or "")
            detail["tickets"][tid] = {"status": status}
            if status != "closed":
                return False, detail
        except Exception as e:
            detail["tickets"][tid] = {"status": "unknown", "error": str(e)}
            return False, detail

    return True, detail


def _maybe_queue_disband_reminder(
    paths: RunPaths,
    *,
    resend_after_s: float = DEFAULT_DISBAND_REMINDER_RESEND_S,
    notify: bool = True,
    nudge: bool = True,
) -> Dict[str, Any]:
    # In check-only mode, avoid mutating run.json.
    with locked_run(paths, save=bool(notify)) as run:
        root = run_root(paths, run)
        if notify:
            tickets_dir = ensure_run_tickets_dir(run, repo_root=root)
        else:
            td_raw = str(run.get("tickets_dir") or "").strip()
            tickets_dir = (
                Path(td_raw).expanduser().resolve()
                if td_raw
                else resolve_tickets_dir(repo_root=root)
            )
        done, detail = _compute_done_locked(run=run, tickets_dir=tickets_dir)
        if not done:
            return {"ok": True, "team": paths.team, "done": False, "detail": detail}

        if not notify:
            return {"ok": True, "team": paths.team, "done": True, "detail": detail}

        dr = dict(run.get("done_reminder") or {})
        existing_id = str(dr.get("inbox_id") or "").strip()
        if existing_id and _inbox_unacked(paths, existing_id):
            return {
                "ok": True,
                "team": paths.team,
                "done": True,
                "sent": False,
                "existing_inbox_id": existing_id,
                "detail": detail,
            }

        sent_at = _parse_rfc3339(str(dr.get("sent_at") or ""))
        if existing_id and sent_at:
            # If it was acked, avoid spam: resend only after a long interval.
            if (time.time() - _epoch(sent_at)) < float(resend_after_s or 0.0):
                return {
                    "ok": True,
                    "team": paths.team,
                    "done": True,
                    "sent": False,
                    "cooldown": True,
                    "detail": detail,
                }

        now = _iso_z()
        msg = (
            "Run appears 100% done.\n\n"
            f"Team: {paths.team}\n"
            f"Charter: {paths.charter_file}\n\n"
            "Definition used (conservative):\n"
            "- No active non-integrator workers\n"
            "- No pending merge items\n"
            "- No unshipped merged items (ship already happened)\n"
            "- All worker tickets are closed\n\n"
            "Next action (manager):\n"
            f"- Disband now: loom team disband {paths.team}\n"
        )
        inbox_msg, _recipient, nudged, reason, _meta = _inbox_write_and_maybe_nudge(
            paths=paths,
            run=run,
            target="manager",
            message=msg,
            sender="team",
            kind="disband",
            meta_extra={"done_check": detail},
            nudge=bool(nudge),
            force=False,
            line_info="disband_reminder",
        )
        run["done_reminder"] = {
            "inbox_id": str(inbox_msg.get("id") or ""),
            "sent_at": now,
        }
        write_event(
            paths,
            event_type="run.done_reminder",
            run=run,
            summary=f"Queued disband reminder inbox_id={str(inbox_msg.get('id') or '')} nudged={nudged}",
            refs={"inbox_id": str(inbox_msg.get("id") or "")},
            data={"nudged": bool(nudged), "nudge_reason": reason, "detail": detail},
        )
        return {
            "ok": True,
            "team": paths.team,
            "done": True,
            "sent": True,
            "inbox_id": str(inbox_msg.get("id") or ""),
            "nudged": bool(nudged),
            "detail": detail,
        }


def done(
    *,
    team: str,
    notify: bool = False,
    resend_after_s: float = DEFAULT_DISBAND_REMINDER_RESEND_S,
    repo: Optional[Path] = None,
) -> DoneResult:
    paths = _paths_for(team=team, repo=repo)
    payload = _maybe_queue_disband_reminder(
        paths,
        resend_after_s=float(resend_after_s),
        notify=bool(notify),
        nudge=bool(notify),
    )
    return DoneResult(
        team=str(payload.get("team") or paths.team),
        done=bool(payload.get("done")),
        detail=dict(payload.get("detail") or {}),
        sent=bool(payload.get("sent", False)),
        inbox_id=str(payload.get("inbox_id") or ""),
        existing_inbox_id=str(payload.get("existing_inbox_id") or ""),
        cooldown=bool(payload.get("cooldown", False)),
        nudged=bool(payload.get("nudged", False)),
    )


def janitor(
    *,
    team: str,
    older_than: str = "7d",
    dry_run: bool = False,
    keep_worktrees: bool = False,
    prune_orphans: bool = False,
    keep_retired_workers: bool = False,
    repo: Optional[Path] = None,
) -> JanitorResult:
    _require_role(action="loom team janitor", allowed_roles={ROLE_MANAGER})
    paths = _paths_for(team=team, repo=repo)
    older_than_s = _parse_duration_seconds(str(older_than or "7d"))
    dry_run = bool(dry_run)
    keep_worktrees = bool(keep_worktrees)
    prune_orphans = bool(prune_orphans)
    keep_retired_workers = bool(keep_retired_workers)

    removed_workers: List[str] = []
    removed_worktrees: List[str] = []
    pruned_orphans: List[str] = []
    skipped_active_paths: List[str] = []

    with locked_run(paths, save=not dry_run) as run:
        session = str(run.get("session") or "")
        root = run_root(paths, run)
        cutoff = time.time() - float(older_than_s)

        panes: Dict[str, Dict[str, str]] = {}
        if session and tmux_available() and tmux_has_session(session):
            panes = tmux_list_panes(session)
        active_paths = {
            str((p or {}).get("path") or "").strip() for p in panes.values()
        }

        workers = dict(run.get("workers") or {})

        # Policy:
        # - Retiring a worker never deletes its worktree.
        # - Janitor only deletes worktrees that the manager has explicitly marked retirable.
        # - By default, janitor does NOT prune unreferenced worktrees.

        retired_old: List[str] = []
        retirable_old: List[str] = []

        for wid, w in workers.items():
            if not isinstance(w, dict):
                continue
            retired = bool(w.get("retired"))
            retired_at = _parse_rfc3339(str(w.get("retired_at") or ""))
            if not (
                retired
                and retired_at
                and _epoch(retired_at)
                and _epoch(retired_at) <= cutoff
            ):
                continue
            retired_old.append(wid)
            if bool(w.get("worktree_retirable")):
                retirable_old.append(wid)

        removed_worktrees_by_wid: Dict[str, str] = {}

        # Remove worktrees for long-retired workers ONLY if marked retirable.
        if not keep_worktrees:
            for wid in retirable_old:
                w = dict((workers.get(wid) or {}))
                wt_raw = str(w.get("worktree") or "").strip()
                if not wt_raw:
                    continue
                wt = Path(wt_raw).expanduser().resolve()
                if not _is_path_within(paths.worktrees_dir, wt):
                    continue
                if str(wt) in active_paths:
                    skipped_active_paths.append(str(wt))
                    continue
                if dry_run:
                    removed_worktrees.append(str(wt))
                    removed_worktrees_by_wid[wid] = str(wt)
                    continue
                try:
                    _remove_worktree(cwd=root, path=wt)
                    removed_worktrees.append(str(wt))
                    removed_worktrees_by_wid[wid] = str(wt)
                except Exception:
                    continue

            # Optional: prune orphan run/worktrees dirs (explicit flag only).
            if prune_orphans and paths.worktrees_dir.exists():
                referenced = set()
                for w in workers.values():
                    if not isinstance(w, dict):
                        continue
                    wt_raw = str(w.get("worktree") or "").strip()
                    if wt_raw:
                        referenced.add(str(Path(wt_raw).expanduser().resolve()))
                ms = _merge_state(run)
                mw = str(ms.get("worktree") or "").strip()
                if mw:
                    referenced.add(str(Path(mw).expanduser().resolve()))

                for child in sorted(paths.worktrees_dir.iterdir()):
                    if not child.is_dir() or child.is_symlink():
                        continue
                    try:
                        r = child.resolve()
                    except Exception:
                        continue
                    if not _is_path_within(paths.worktrees_dir, r):
                        continue
                    if str(r) in referenced:
                        continue
                    if str(r) in active_paths:
                        skipped_active_paths.append(str(r))
                        continue
                    try:
                        if child.stat().st_mtime > cutoff:
                            continue
                    except Exception:
                        continue
                    if dry_run:
                        pruned_orphans.append(str(r))
                        continue
                    try:
                        _remove_worktree(cwd=root, path=r)
                        pruned_orphans.append(str(r))
                    except Exception:
                        continue

            # Best-effort: prune stale worktree registrations.
            if not dry_run:
                best_effort(
                    lambda: repo_worktree_prune(root=root), label="janitor.ws_prune"
                )

        if not keep_retired_workers and dry_run:
            if keep_worktrees:
                removed_workers.extend(list(retired_old))
            else:
                removed_workers.extend(
                    [wid for wid in retired_old if wid in removed_worktrees_by_wid]
                )

        # Remove retired workers from run state only after their worktree is removed.
        if not keep_retired_workers and not dry_run:
            keep_workers: Dict[str, Any] = {}
            for wid, w in workers.items():
                if wid not in retired_old:
                    keep_workers[wid] = w
                    continue
                if keep_worktrees:
                    removed_workers.append(wid)
                    continue
                if wid in removed_worktrees_by_wid:
                    removed_workers.append(wid)
                    continue
                # Keep record until the manager marks the worktree retirable.
                keep_workers[wid] = w
            run["workers"] = keep_workers

        if not dry_run:
            write_event(
                paths,
                event_type="janitor.ran",
                run=run,
                summary=(
                    f"Janitor older_than_s={older_than_s} removed_workers={len(removed_workers)} "
                    f"removed_worktrees={len(removed_worktrees)} pruned_orphans={len(pruned_orphans)} dry_run={dry_run}"
                ),
                data={
                    "older_than_s": int(older_than_s),
                    "dry_run": bool(dry_run),
                    "keep_worktrees": bool(keep_worktrees),
                    "prune_orphans": bool(prune_orphans),
                    "keep_retired_workers": bool(keep_retired_workers),
                    "removed_workers": list(removed_workers),
                    "removed_worktrees": list(removed_worktrees),
                    "pruned_orphans": list(pruned_orphans),
                    "skipped_active_paths": list(skipped_active_paths),
                },
            )

    return JanitorResult(
        team=paths.team,
        older_than_s=int(older_than_s),
        dry_run=bool(dry_run),
        removed_workers=list(removed_workers),
        removed_worktrees=list(removed_worktrees),
        pruned_orphans=list(pruned_orphans),
        skipped_active_paths=list(skipped_active_paths),
    )


def _cleanup_run_dir(paths: RunPaths) -> None:
    # Best-effort removal; do not explode if leftover.
    try:
        shutil.rmtree(paths.run_dir)
    except FileNotFoundError:
        return
    except Exception:
        return


def disband(
    *,
    team: str,
    keep_worktrees: bool = True,
    keep_state: bool = False,
    repo: Optional[Path] = None,
) -> DisbandResult:
    _require_bin("tmux")
    _require_role(action="loom team disband", allowed_roles={ROLE_MANAGER})
    team_or_session = str(team).strip()
    if not team_or_session:
        raise TeamError("Missing <team>", code="ARG", exit_code=2)

    session = (
        team_or_session
        if tmux_has_session(team_or_session)
        else f"{DEFAULT_TMUX_SESSION_PREFIX}-{sanitize(team_or_session, max_len=80)}"
    )
    team = resolve_team_from_session(session)

    # Try to locate run_dir/run.json via repo root if available.
    run: Optional[Dict[str, Any]] = None
    paths: Optional[RunPaths] = None
    root: Optional[Path] = None

    if repo is not None:
        try:
            root = canonical_repo_root(repo.resolve())
        except Exception:
            root = None

    if root is None:
        # Try to discover run_dir from tmux session option.
        if tmux_has_session(session):
            rd = tmux_get_option(target=session, option=TMUX_OPT_RUN_DIR)
            if rd:
                try:
                    run_dir = Path(rd).expanduser().resolve()
                    # repo root is the parent of `.loom/team/runs/<team>` if run_dir follows our layout.
                    # If not, we still use run_dir as a starting point.
                    # Find the repo root via the nearest `.loom/team` marker.
                    cur = run_dir
                    while cur != cur.parent:
                        if (cur / ".loom" / "team").exists():
                            root = cur
                            break
                        if cur.name == "team" and cur.parent.name == ".loom":
                            root = cur.parent.parent
                            break
                        if cur.name == ".loom" and (cur / "team").exists():
                            root = cur.parent
                            break
                        cur = cur.parent
                except Exception:
                    root = None

    if root is not None:
        paths = RunPaths(repo_root=root, team=sanitize(team, max_len=80) or team)
        if paths.run_file.exists():
            try:
                run = load_run(paths)
            except Exception:
                run = None

    # Best-effort audit log (may be deleted if --keep-state is not set).
    if paths is not None:
        safe_write_event(
            paths,
            event_type="run.disbanded",
            run=run,
            summary=f"Disband requested session={session}",
            refs={"tmux_session": session},
            data={
                "keep_worktrees": bool(keep_worktrees),
                "keep_state": bool(keep_state),
            },
        )

    # Kill tmux session (this should stop pane processes). Do not attempt PID-based
    # cleanup here: PID harvesting is brittle and can kill unrelated tmux servers.
    tmux_session_killed = False
    if tmux_has_session(session):
        tmux_kill_session(session)
        tmux_session_killed = True

    # Best-effort: clear sidecar pidfiles (state cleanup only).
    pidfiles_removed: List[str] = []
    pidfiles_left: List[str] = []
    sidecar_pidfiles: List[str] = []
    if paths is not None:
        try:
            if paths.sidecars_dir.exists():
                for f in sorted(paths.sidecars_dir.glob("*.pid.json")):
                    sidecar_pidfiles.append(str(f))
                    try:
                        f.unlink()
                        pidfiles_removed.append(str(f))
                    except Exception:
                        pidfiles_left.append(str(f))
        except Exception:
            pidfiles_left = list(pidfiles_left) or sidecar_pidfiles

    process_cleanup: Dict[str, Any] = {
        "tmux_session_killed": bool(tmux_session_killed),
        "sidecar_pidfiles": list(sidecar_pidfiles),
        "pidfiles_removed": list(pidfiles_removed),
        "pidfiles_left": list(pidfiles_left),
    }

    if paths is not None:
        safe_write_event(
            paths,
            event_type="run.disband.process_cleanup",
            run=run,
            summary=(
                f"Disband process cleanup tmux_session_killed={tmux_session_killed} "
                f"pidfiles_removed={len(pidfiles_removed)} pidfiles_left={len(pidfiles_left)}"
            ),
            refs={"tmux_session": session},
            data=process_cleanup,
        )

    # Optionally remove worktrees via ws.
    if not keep_worktrees and run and root and paths:
        wt_root = paths.worktrees_dir
        if wt_root.exists():
            for child in sorted(wt_root.iterdir()):
                # Only attempt directories.
                if not child.is_dir():
                    continue
                if child.is_symlink():
                    continue
                if not _is_path_within(wt_root, child.resolve()):
                    continue
                try:
                    _remove_worktree(cwd=root, path=child)
                except Exception:
                    # Best-effort cleanup.
                    pass

    # Optionally remove the run directory.
    if not keep_state and paths:
        _cleanup_run_dir(paths)

    return DisbandResult(
        team=team,
        session=session,
        worktrees_removed=not keep_worktrees,
        state_removed=not keep_state,
        process_cleanup=process_cleanup,
    )


# -----------------------------
# Team lifecycle (pause/resume)
# -----------------------------


def pause_team(*, team: str, repo: Optional[Path] = None) -> PauseResult:
    """Pause a team run (clock-out): stop tmux session, keep state on disk."""

    _require_bin("tmux")
    _require_role(action="loom team clock-out", allowed_roles={ROLE_MANAGER})
    paths = _paths_for(team=team, repo=repo)
    paused_at = _iso_z()

    session = ""
    run_snapshot: Dict[str, Any] = {}
    with locked_run(paths) as run:
        session = run_session(run)
        run["paused"] = True
        run["paused_at"] = paused_at
        run_snapshot = dict(run)

    session_killed = False
    if session and tmux_has_session(session):
        tmux_kill_session(session)
        session_killed = True

    safe_write_event(
        paths,
        event_type="run.paused",
        run=run_snapshot,
        summary=f"Paused run session={session}",
        refs={"tmux_session": session},
        data={"paused_at": paused_at, "tmux_session_killed": bool(session_killed)},
    )

    return PauseResult(
        team=str(run_snapshot.get("team") or paths.team),
        session=session,
        paused_at=paused_at,
        session_killed=bool(session_killed),
    )


def _respawn_active_worker_if_missing(
    *,
    paths: RunPaths,
    run: Dict[str, Any],
    worker_id: str,
    worker: Dict[str, Any],
    session: str,
    repo_root: Path,
) -> tuple[bool, Dict[str, Any]]:
    role = str(worker.get("role") or "").strip().lower()
    if role != ROLE_WORKER:
        return False, dict(worker)

    ticket_id = str(worker.get("ticket_id") or "").strip()
    if not ticket_id:
        raise TeamError(
            f"Worker missing ticket_id: {worker_id}",
            code="BAD_STATE",
            exit_code=2,
        )

    worktree_raw = str(worker.get("worktree") or "").strip()
    if not worktree_raw:
        raise TeamError(
            f"Worker missing worktree path: {worker_id}",
            code="BAD_STATE",
            exit_code=2,
        )
    worktree_path = Path(worktree_raw).expanduser().resolve()
    if not worktree_path.exists():
        raise TeamError(
            f"Worker worktree path does not exist: {worker_id} worktree={worktree_path}",
            code="WORKTREE_MISSING",
            exit_code=2,
        )

    # If the recorded window still exists, just refresh pane_id.
    win = str(worker.get("window") or "").strip()
    if win and tmux_window_exists(session, win):
        pane_id = tmux_format(f"{session}:{win}", "#{pane_id}")
        out = dict(worker)
        out["pane_id"] = pane_id
        return False, out

    harness = _normalize_harness(str(run.get("harness") or ""))
    profile = resolve_member_profile(
        run,
        role=role,
        ticket_id=ticket_id,
        worktree_key=str(worker.get("worktree_key") or ""),
    )
    enforce_member_lifecycle(profile=profile, role=role)
    if profile is not None and profile.harness:
        harness = _normalize_harness(profile.harness)

    cfg = (
        (run.get(harness) or {})
        if isinstance(run.get(harness), dict)
        else (run.get("opencode") or {})
    )
    agent_bin = str(cfg.get("bin") or "").strip() or harness
    _require_bin(agent_bin)

    tickets_dir = ensure_run_tickets_dir(run, repo_root=repo_root)
    ticket_payload = ticket_show(ticket_id=ticket_id, tickets_dir=tickets_dir)
    ticket = {
        "id": ticket_payload.ticket.id,
        "title": ticket_payload.ticket.title,
        "status": ticket_payload.ticket.status,
    }
    ticket_payload_dict = dataclasses.asdict(ticket_payload)
    ticket = {**ticket, "id": str(ticket.get("id") or ticket_id)}

    charter_path = paths.charter_file
    branch = str(worker.get("branch") or "").strip()
    base = str(worker.get("base") or "").strip()
    prompt = render_worker_prompt(
        run=run,
        role=role,
        worker_id=worker_id,
        ticket=ticket,
        ticket_payload=ticket_payload_dict,
        worktree_path=worktree_path,
        branch=branch,
        base=base,
        charter_path=charter_path,
    )

    agent = (
        str(profile.agent)
        if profile is not None
        else _agent_for_role(run, role, harness=harness)
    )
    _require_agent_file_present(workdir=worktree_path, harness=harness, agent=agent)
    model = _model_for_role(run, role, harness=harness)
    if not model and profile is not None and profile.model:
        model = str(profile.model)
    oc_argv = _team_tui_argv(
        project_dir=worktree_path,
        agent=agent,
        prompt=prompt,
        model=model,
        harness=harness,
        bin=str(cfg.get("bin") or "").strip(),
    )

    sprint = _objective_state_sprint_state(run)
    pane_env = {
        ENV_TICKET_DIR: str(tickets_dir),
        ENV_TEAM_NAME: str(run.get("team") or paths.team),
        ENV_TEAM_RUN_ID: str(run.get("run_id") or ""),
        ENV_TEAM_RUN_DIR: str(paths.run_dir),
        ENV_TEAM_ROLE: role,
        ENV_TEAM_WORKER_ID: worker_id,
        ENV_TEAM_TICKET_ID: ticket_id,
        ENV_TEAM_SPRINT_NAME: sprint.get("name", ""),
        ENV_TEAM_SPRINT_TAG: sprint.get("tag", ""),
        "COMPOUND_ROOT": str(repo_root),
    }

    desired_window = win or f"{worker_id}-{sanitize(ticket_id, max_len=24)}"
    window = tmux_unique_window_name(session, desired_window)
    tmux_cmd(
        [
            "new-window",
            "-d",
            "-t",
            session,
            "-n",
            window,
            "-c",
            str(worktree_path),
            *tmux_env_flags(pane_env),
            *oc_argv,
        ],
        check=True,
    )

    pane_id = tmux_format(f"{session}:{window}", "#{pane_id}")
    if pane_id:
        tmux_mark_pane(
            pane_id=pane_id,
            role=role,
            worker_id=worker_id,
            ticket_id=ticket_id,
        )

    out = dict(worker)
    out["window"] = window
    out["pane_id"] = pane_id
    out["revived_at"] = _iso_z()
    out["retired"] = False
    out["retired_at"] = ""
    return True, out


def resume_team(*, team: str, repo: Optional[Path] = None) -> ResumeTeamResult:
    """Resume a paused team run (clock-in): recreate tmux session and respawn workers."""

    _require_bin("tmux")
    _require_role(action="loom team clock-in", allowed_roles={ROLE_MANAGER})
    paths = _paths_for(team=team, repo=repo)

    # Require a durable run.json. Resuming should not implicitly create a new run.
    if not paths.run_file.exists():
        raise TeamError(
            "Run not found.\n"
            f"  team: {paths.team}\n"
            f"  missing: {paths.run_file}\n\n"
            f"Hint: start a new run with: loom team start {paths.team} --repo {paths.repo_root}\n",
            code="NO_RUN",
            exit_code=2,
        )

    # Ensure tmux session + manager window exist.
    start_res = start(team=team, repo=repo)
    resumed_at = _iso_z()

    resumed_workers: List[str] = []
    skipped_workers: List[Dict[str, str]] = []

    integrator_args: Dict[str, Any] = {}

    with locked_run(paths) as run:
        session = run_session(run)
        if not tmux_has_session(session):
            raise TeamError(
                f"tmux session not found after resume: {session}",
                code="TMUX",
                exit_code=2,
            )

        repo_root = run_root(paths, run)

        raw_workers = run.get("workers")
        workers: Dict[str, Any] = (
            dict(raw_workers) if isinstance(raw_workers, dict) else {}
        )
        for wid in sorted(workers):
            w = workers.get(wid)
            if not isinstance(w, dict):
                continue
            if bool(w.get("retired")):
                continue

            role = str(w.get("role") or "").strip().lower()
            if role == ROLE_INTEGRATOR:
                integrator_args = {
                    "worker_id": str(w.get("worker_id") or wid or "integrator"),
                    "window": str(w.get("window") or "integrator"),
                    "worktree": str(w.get("worktree_key") or "merge-queue"),
                    "branch": str(w.get("branch") or merge_branch_for_run(run)),
                    "base_ref": str(w.get("base") or ""),
                }
                continue

            if role != ROLE_WORKER:
                continue

            try:
                did, updated = _respawn_active_worker_if_missing(
                    paths=paths,
                    run=run,
                    worker_id=str(wid),
                    worker=dict(w),
                    session=session,
                    repo_root=repo_root,
                )
            except TeamError as e:
                skipped_workers.append(
                    {
                        "worker_id": str(wid),
                        "code": str(getattr(e, "code", "")) or "ERROR",
                        "error": str(e),
                    }
                )
                continue

            if did:
                resumed_workers.append(str(wid))
            workers[wid] = updated

        run["workers"] = workers
        run["paused"] = False
        run["paused_at"] = ""

        safe_write_event(
            paths,
            event_type="run.resumed",
            run=run,
            summary=f"Resumed run session={session}",
            refs={"tmux_session": session},
            data={
                "resumed_at": resumed_at,
                "resumed_workers": list(resumed_workers),
                "skipped_workers": list(skipped_workers),
            },
        )

    # Ensure integrator exists (best-effort).
    integrator_out: Dict[str, Any] = {}
    if integrator_args:
        try:
            # If base_ref wasn't persisted, default to target branch.
            if not str(integrator_args.get("base_ref") or "").strip():
                run2 = load_run(paths)
                ms = _merge_state(run2)
                cfg = dict(ms.get("config") or {})
                integrator_args["base_ref"] = str(cfg.get("target_branch") or "main")
            res_int = spawn_integrator(
                team=paths.team,
                worker_id=str(integrator_args.get("worker_id") or "integrator"),
                window=str(integrator_args.get("window") or "integrator"),
                worktree=str(integrator_args.get("worktree") or "merge-queue"),
                branch=str(integrator_args.get("branch") or ""),
                base_ref=str(integrator_args.get("base_ref") or ""),
                repo=repo,
            )
            integrator_out = dataclasses.asdict(res_int)
        except Exception as e:
            integrator_out = {"ok": False, "error": str(e)}

    return ResumeTeamResult(
        team=str(start_res.team),
        session=str(start_res.session),
        resumed_at=resumed_at,
        manager=dict(start_res.manager or {}),
        resumed_workers=list(resumed_workers),
        skipped_workers=list(skipped_workers),
        integrator=dict(integrator_out or {}),
    )


# -----------------------------
# Worker lifecycle commands (manager-facing)
# -----------------------------


def _next_worker_id(run: Mapping[str, Any]) -> str:
    existing = set((run.get("workers") or {}).keys())
    for i in range(1, 1000):
        wid = f"w{i}"
        if wid not in existing:
            return wid
    return f"w{uuid.uuid4().hex[:4]}"


def _agent_for_role(run: Mapping[str, Any], role: str, *, harness: str) -> str:
    h = _normalize_harness(harness)
    cfg = (
        (run.get(h) or {})
        if isinstance(run.get(h), dict)
        else (
            (run.get("opencode") or {}) if isinstance(run.get("opencode"), dict) else {}
        )
    )
    if role == ROLE_WORKER:
        return str(cfg.get("worker_agent") or DEFAULT_WORKER_AGENT)
    if role == ROLE_ARCHITECT:
        return str(cfg.get("architect_agent") or DEFAULT_ARCHITECT_AGENT)
    if role == ROLE_INTEGRATOR:
        return str(cfg.get("integrator_agent") or DEFAULT_INTEGRATOR_AGENT)
    if role == ROLE_MANAGER:
        return str(cfg.get("manager_agent") or DEFAULT_MANAGER_AGENT)
    return str(cfg.get("worker_agent") or DEFAULT_WORKER_AGENT)


def _model_for_role(run: Mapping[str, Any], role: str, *, harness: str) -> str:
    h = _normalize_harness(harness)
    cfg = (
        (run.get(h) or {})
        if isinstance(run.get(h), dict)
        else (
            (run.get("opencode") or {}) if isinstance(run.get("opencode"), dict) else {}
        )
    )
    models = cfg.get("models") if isinstance(cfg.get("models"), dict) else {}
    m = str((models or {}).get(str(role or "").strip()) or "").strip()
    if m:
        return m
    return str(cfg.get("model") or "").strip()


def _max_headcount(run: Mapping[str, Any]) -> int:
    raw_limits = run.get("limits")
    limits: Dict[str, Any] = dict(raw_limits) if isinstance(raw_limits, dict) else {}
    raw = limits.get("max_headcount", 0)
    try:
        n = int(raw)
    except Exception:
        return 0
    return n if n > 0 else 0


def _active_spawn_headcount(
    run: Mapping[str, Any],
) -> tuple[int, list[str], dict[str, str]]:
    raw_workers = run.get("workers")
    workers: Dict[str, Any] = dict(raw_workers) if isinstance(raw_workers, dict) else {}
    active_ids: list[str] = []
    active_roles: dict[str, str] = {}
    for wid in sorted(workers):
        w = workers.get(wid)
        if not isinstance(w, dict):
            continue
        if bool(w.get("retired")):
            continue
        role = str(w.get("role") or "").strip().lower()
        if role != ROLE_WORKER:
            continue
        active_ids.append(str(wid))
        active_roles[str(wid)] = role
    return len(active_ids), active_ids, active_roles


def spawn(
    *,
    team: str,
    ticket_id: str,
    role: str = ROLE_WORKER,
    worker_id: str = "",
    window: str = "",
    worktree_key: str = "",
    branch: str = "",
    base_ref: str = "",
    resume: bool = False,
    repo: Optional[Path] = None,
) -> SpawnResult:
    _require_bin("tmux")
    _require_role(action="loom team spawn", allowed_roles={ROLE_MANAGER})

    paths = _paths_for(team=team, repo=repo)

    with locked_run(paths) as run:
        harness = _normalize_harness(str(run.get("harness") or ""))
        session = run_session(run)
        if not tmux_has_session(session):
            raise TeamError(
                f"tmux session not found: {session} (run {paths.team}). Start it with: loom team start ...",
                code="TMUX",
                exit_code=2,
            )

        role = str(role or ROLE_WORKER).strip().lower()
        if role != ROLE_WORKER:
            raise TeamError(f"Invalid role: {role}", code="ARG", exit_code=2)

        ticket_id = str(ticket_id).strip()
        if not ticket_id:
            raise TeamError("Missing ticket", code="ARG", exit_code=2)

        max_headcount = _max_headcount(run)
        if max_headcount > 0:
            active_count, active_ids, active_roles = _active_spawn_headcount(run)
            if active_count >= max_headcount:
                raise TeamError(
                    f"Headcount limit reached: active={active_count} max={max_headcount}",
                    code="HEADCOUNT",
                    exit_code=2,
                    hint=(
                        "Wait for existing workers to finish, then retire them before spawning more. "
                        "Use status to identify who is still active."
                    ),
                    suggestions=[
                        f"loom team status {paths.team} --show-dead",
                        f"loom team wait {paths.team} 5m",
                        f"loom team retire {paths.team} <WORKER_ID>",
                    ],
                    data={
                        "team": paths.team,
                        "max_headcount": int(max_headcount),
                        "active_count": int(active_count),
                        "active_worker_ids": list(active_ids),
                        "active_roles": dict(active_roles),
                    },
                )

        root = run_root(paths, run)

        # Resolve the canonical (repo-root) ticket directory and persist it.
        tickets_dir = ensure_run_tickets_dir(run, repo_root=root)

        # Fetch ticket context (loom ticket is authoritative).
        ticket_payload = ticket_show(ticket_id=ticket_id, tickets_dir=tickets_dir)
        ticket = {
            "id": ticket_payload.ticket.id,
            "title": ticket_payload.ticket.title,
            "status": ticket_payload.ticket.status,
        }
        ticket_payload_dict = dataclasses.asdict(ticket_payload)
        # Normalization: ensure id is set.
        ticket = {**ticket, "id": str(ticket.get("id") or ticket_id)}

        workers = dict(run.get("workers") or {})
        requested_worker_id = sanitize(str(worker_id or ""), max_len=16)
        resume = bool(resume)

        base_ref_effective = str(base_ref or "").strip()
        if not base_ref_effective:
            defaults = (
                run.get("defaults") if isinstance(run.get("defaults"), dict) else {}
            )
            base_ref_effective = str((defaults or {}).get("base_ref") or "").strip()
        base_ref_for_ws = base_ref_effective or None

        if resume and not requested_worker_id:
            raise TeamError("--resume requires --worker-id", code="ARG", exit_code=2)

        existing: Optional[Dict[str, Any]] = None
        if requested_worker_id and requested_worker_id in workers:
            existing = dict(workers.get(requested_worker_id) or {})
            if not resume:
                raise TeamError(
                    f"worker_id already exists: {requested_worker_id}",
                    code="ARG",
                    exit_code=2,
                )

            if not bool(existing.get("retired")):
                raise TeamError(
                    f"Refusing to resume non-retired worker: {requested_worker_id}",
                    code="ARG",
                    exit_code=2,
                )
            if bool(existing.get("worktree_retirable")):
                raise TeamError(
                    f"Refusing to resume worker with retirable worktree: {requested_worker_id}",
                    code="ARG",
                    exit_code=2,
                )
            existing_role = str(existing.get("role") or "").strip().lower()
            if existing_role != ROLE_WORKER:
                raise TeamError(
                    f"Refusing to resume role={existing_role} (only worker)",
                    code="ARG",
                    exit_code=2,
                )
            if role != existing_role:
                raise TeamError(
                    f"Role mismatch on resume: requested={role} existing={existing_role}",
                    code="ARG",
                    exit_code=2,
                )
            existing_ticket_id = str(existing.get("ticket_id") or "").strip()
            if existing_ticket_id and existing_ticket_id != ticket_id:
                raise TeamError(
                    f"Ticket mismatch on resume: requested={ticket_id} existing={existing_ticket_id}",
                    code="ARG",
                    exit_code=2,
                )

            wt_raw = str(existing.get("worktree") or "").strip()
            if not wt_raw:
                raise TeamError(
                    f"Cannot resume worker without worktree: {requested_worker_id}",
                    code="BAD_STATE",
                    exit_code=2,
                )
            worktree_path = Path(wt_raw).expanduser().resolve()
            if not _is_path_within(paths.worktrees_dir, worktree_path):
                raise TeamError(
                    f"Refusing to resume worker with worktree outside run dir: {worktree_path}",
                    code="WORKTREE_SAFETY",
                    exit_code=2,
                )

            worktree_key = (
                sanitize(str(existing.get("worktree_key") or ""), max_len=80)
                or worktree_path.name
            )
            branch_override = str(existing.get("branch") or "").strip() or (
                str(branch or "").strip() or None
            )
            wt = _ensure_worktree(
                cwd=root,
                ticket_id=ticket_id,
                path=worktree_path,
                branch=branch_override,
                base_ref=base_ref_for_ws,
                allow_dirty=True,
            )
        else:
            if resume:
                raise TeamError(
                    f"Cannot resume unknown worker_id: {requested_worker_id}",
                    code="ARG",
                    exit_code=2,
                )
            worker_id_final = requested_worker_id or _next_worker_id(run)

            # Worktree key and path are per-run.
            raw_worktree_key = str(worktree_key or "").strip()
            worktree_key = (
                sanitize(raw_worktree_key, max_len=80)
                if raw_worktree_key
                else generate_stable_key(ticket_id, max_len=80)
            )
            if not worktree_key:
                worktree_key = f"{sanitize(ticket_id, max_len=40)}-{worker_id_final}"

            desired_wt_path = (paths.worktrees_dir / worktree_key).resolve()
            if not _is_path_within(paths.worktrees_dir, desired_wt_path):
                raise TeamError(
                    f"Refusing to create worktree outside run worktrees dir: {desired_wt_path}",
                    code="WORKTREE_PATH",
                    exit_code=2,
                )

            branch_override = str(branch or "").strip() or None
            wt = _ensure_worktree(
                cwd=root,
                ticket_id=ticket_id,
                path=desired_wt_path,
                branch=branch_override,
                base_ref=base_ref_for_ws,
            )
            worktree_path = Path(wt["path"]).resolve()

            requested_worker_id = worker_id_final

        worker_id = str(requested_worker_id or "").strip()
        if not worker_id:
            raise TeamError(
                "worker_id resolution failed", code="BAD_STATE", exit_code=2
            )

        profile = resolve_member_profile(
            run,
            role=role,
            ticket_id=ticket_id,
            worktree_key=worktree_key,
        )
        enforce_member_lifecycle(profile=profile, role=role)
        if profile is not None and profile.harness:
            harness = _normalize_harness(profile.harness)

        cfg = (
            (run.get(harness) or {})
            if isinstance(run.get(harness), dict)
            else (run.get("opencode") or {})
        )
        agent_bin = str(cfg.get("bin") or "").strip() or harness
        _require_bin(agent_bin)

        raw_mounts = run.get("mounts")
        mounts: list[dict] = []
        if isinstance(raw_mounts, list):
            mounts = [dict(x) for x in raw_mounts if isinstance(x, dict)]
        _apply_mounts(repo_root=root, worktree_root=worktree_path, mounts=mounts)

        if harness == "opencode":
            _ensure_opencode_worktree_runtime(workdir=worktree_path, repo_root=root)

        # Build worker prompt and spawn window.
        charter_path = paths.run_dir / "CHARTER.md"
        prompt = render_worker_prompt(
            run=run,
            role=role,
            worker_id=worker_id,
            ticket=ticket,
            ticket_payload=ticket_payload_dict,
            worktree_path=worktree_path,
            branch=wt.get("branch") or "",
            base=wt.get("base") or "",
            charter_path=charter_path,
        )

        agent = (
            str(profile.agent)
            if profile is not None
            else _agent_for_role(run, role, harness=harness)
        )
        _require_agent_file_present(workdir=worktree_path, harness=harness, agent=agent)
        model = _model_for_role(run, role, harness=harness)
        if not model and profile is not None and profile.model:
            model = str(profile.model)
        oc_argv = _team_tui_argv(
            project_dir=worktree_path,
            agent=agent,
            prompt=prompt,
            model=model,
            harness=harness,
            bin=str(cfg.get("bin") or "").strip(),
        )

        sprint = _objective_state_sprint_state(run)
        pane_env = {
            ENV_TICKET_DIR: str(tickets_dir),
            ENV_TEAM_NAME: str(run.get("team") or paths.team),
            ENV_TEAM_RUN_ID: str(run.get("run_id") or ""),
            ENV_TEAM_RUN_DIR: str(paths.run_dir),
            ENV_TEAM_ROLE: role,
            ENV_TEAM_WORKER_ID: worker_id,
            ENV_TEAM_TICKET_ID: ticket_id,
            ENV_TEAM_SPRINT_NAME: sprint.get("name", ""),
            ENV_TEAM_SPRINT_TAG: sprint.get("tag", ""),
            "COMPOUND_ROOT": str(root),
        }

        desired_window = window or f"{worker_id}-{sanitize(ticket_id, max_len=24)}"
        window = tmux_unique_window_name(session, desired_window)

        tmux_cmd(
            [
                "new-window",
                "-d",
                "-t",
                session,
                "-n",
                window,
                "-c",
                str(worktree_path),
                *tmux_env_flags(pane_env),
                *oc_argv,
            ],
            check=True,
        )

        pane_id = tmux_format(f"{session}:{window}", "#{pane_id}")
        if pane_id:
            tmux_mark_pane(
                pane_id=pane_id, role=role, worker_id=worker_id, ticket_id=ticket_id
            )

        workers = dict(run.get("workers") or {})
        prev = dict(workers.get(worker_id) or {})
        now_iso = _iso_z()
        workers[worker_id] = {
            **prev,
            "worker_id": worker_id,
            "role": role,
            "ticket_id": ticket_id,
            "roster_member_id": str(profile.member_id) if profile is not None else "",
            "roster_source": str(profile.source) if profile is not None else "",
            "roster_lifecycle": str(profile.lifecycle) if profile is not None else "",
            "window": window,
            "pane_id": pane_id,
            "worktree": str(worktree_path),
            "worktree_key": worktree_key,
            "branch": wt.get("branch") or "",
            "base": wt.get("base") or "",
            "created_at": str(prev.get("created_at") or now_iso),
            "revived_at": (
                now_iso
                if bool(resume) and bool(prev)
                else str(prev.get("revived_at") or "")
            ),
            "retired": False,
            "retired_at": "",
            "worktree_retirable": bool(prev.get("worktree_retirable"))
            if prev
            else False,
            "worktree_retirable_at": str(prev.get("worktree_retirable_at") or "")
            if prev
            else "",
        }
        run["workers"] = workers

        write_event(
            paths,
            event_type="worker.spawned",
            run=run,
            summary=(
                f"Resumed {worker_id} role={role} ticket={ticket_id}"
                if bool(resume) and bool(prev)
                else f"Spawned {worker_id} role={role} ticket={ticket_id}"
            ),
            refs={
                "worker_id": worker_id,
                "ticket_id": ticket_id,
                "branch": workers[worker_id].get("branch"),
                "worktree": workers[worker_id].get("worktree"),
                "window": window,
                "pane_id": pane_id,
            },
            data={
                "role": role,
                "worktree_key": worktree_key,
                "base_ref": str(base_ref_effective or ""),
                "branch_override": branch_override or "",
                "resumed": bool(resume) and bool(prev),
                "roster_member_id": str(profile.member_id)
                if profile is not None
                else "",
                "roster_source": str(profile.source) if profile is not None else "",
            },
        )
    return SpawnResult(
        team=str(run.get("team") or paths.team),
        session=str(run.get("session") or ""),
        repo_root=str(root),
        run_dir=str(paths.run_dir),
        tickets_dir=str(tickets_dir),
        worker=dict(workers[worker_id]),
        ticket={
            "id": ticket.get("id"),
            "title": ticket.get("title"),
            "status": ticket.get("status"),
        },
    )


def resume_worker(
    *,
    team: str,
    worker_id: str,
    repo: Optional[Path] = None,
) -> SpawnResult:
    """Resume a retired worker in its existing worktree."""

    _require_role(action="loom team resume-worker", allowed_roles={ROLE_MANAGER})
    paths = _paths_for(team=team, repo=repo)
    run = load_run(paths)
    raw_workers = run.get("workers")
    workers: Dict[str, Any] = dict(raw_workers) if isinstance(raw_workers, dict) else {}
    wid = str(worker_id or "").strip()
    w = workers.get(wid)
    if not isinstance(w, dict):
        raise TeamError(f"Unknown worker_id: {wid}", code="ARG", exit_code=2)
    if not bool(w.get("retired")):
        raise TeamError(f"Worker is not retired: {wid}", code="ARG", exit_code=2)
    tid = str(w.get("ticket_id") or "").strip()
    if not tid:
        raise TeamError(
            f"Worker has no ticket_id: {wid}", code="BAD_STATE", exit_code=2
        )
    role = str(w.get("role") or "").strip().lower()
    if role != ROLE_WORKER:
        raise TeamError(
            f"Refusing to resume role={role} (only worker)",
            code="ARG",
            exit_code=2,
        )

    return spawn(
        team=team,
        ticket_id=tid,
        role=role,
        worker_id=wid,
        resume=True,
        repo=repo,
    )


def _sync_ticket_sprint_context(
    *, tickets_dir: Path, sprint_name: str, sprint_tag: str
) -> None:
    ticket_sprint_set(tickets_dir=tickets_dir, name=sprint_name, tag=sprint_tag)


def _clear_ticket_sprint_context(*, tickets_dir: Path) -> None:
    ticket_sprint_clear(tickets_dir=tickets_dir)


def prep_sprint(
    *,
    team: str,
    name: str,
    force: bool = False,
    notify_architect: bool = True,
    ticket_type: str = "task",
    ticket_priority: int = 1,
    repo: Optional[Path] = None,
) -> PrepSprintResult:
    """Set the current sprint and create a prep ticket, then notify architect personas."""

    _require_role(action="loom team prep-sprint", allowed_roles={ROLE_MANAGER})
    paths = _paths_for(team=team, repo=repo)
    sprint_name = str(name or "").strip()
    now = _iso_z()

    with locked_run(paths) as run:
        sprint = _objective_state_start_sprint_state(
            run=run,
            name=sprint_name,
            force=bool(force),
            now=now,
        )
        tag = str(sprint.get("tag") or "")
        rev = int(sprint.get("rev") or 0)
        root = run_root(paths, run)
        tickets_dir = ensure_run_tickets_dir(run, repo_root=root)
        _sync_ticket_sprint_context(
            tickets_dir=tickets_dir,
            sprint_name=sprint_name,
            sprint_tag=tag,
        )

        # Update charter with sprint metadata.
        _write_charter(paths=paths, run=run)

        write_event(
            paths,
            event_type="sprint.started",
            run=run,
            summary=f"Sprint started name={sprint_name}",
            refs={"sprint": sprint_name, "tag": tag, "rev": rev},
        )

        objective = str(run.get("objective") or "").strip()
        desc = _build_prep_sprint_ticket_description(
            objective=objective,
            sprint_name=sprint_name,
            tag=tag,
        )

        created = ticket_create(
            tickets_dir=tickets_dir,
            title=f"Sprint prep: {sprint_name}",
            type=str(ticket_type or "task"),
            priority=int(ticket_priority or 1),
            tags=f"{tag},fanout",
            description=desc,
        )

    spawned = False
    wid = ""
    run2 = load_run(paths)

    if notify_architect:
        architects = [
            recipient
            for recipient in _resolve_targets(run2, "role:architect")
            if str(recipient.get("worker_id") or "").strip()
        ]
        if not architects:
            raise TeamError(
                "No active architect persona available for sprint prep notification",
                code="BAD_STATE",
                exit_code=2,
                suggestions=[f"loom team start {paths.team} --repo {paths.repo_root}"],
            )
        for recipient in architects:
            architect_id = str(recipient.get("worker_id") or "").strip()
            if not wid:
                wid = architect_id
            _inbox_write_and_maybe_nudge(
                paths=paths,
                run=run2,
                target=architect_id,
                message=(
                    f"Sprint prep ticket created: {created.id}. "
                    f"Sprint={sprint_name} tag={tag}. "
                    "Complete prep ticket and fan out sprint tickets."
                ),
                sender="team",
                kind="sprint",
                meta_extra={"sprint": dict(run2.get("sprint") or {})},
                nudge=True,
                force=False,
                line_info=f"sprint_prep_to={architect_id}",
            )
        spawned = True

    # Notify manager (durable), with sprint prefixing handled centrally.
    _inbox_write_and_maybe_nudge(
        paths=paths,
        run=run2,
        target="manager",
        message=(
            f"Sprint started. Tag tickets with `{tag}`. "
            f"Prep ticket={created.id}. "
            + (f"Architect={wid}." if spawned and wid else "")
        ),
        sender="team",
        kind="sprint",
        meta_extra={"sprint": dict(run2.get("sprint") or {})},
        nudge=True,
        force=False,
        line_info="sprint_started",
    )

    return PrepSprintResult(
        team=paths.team,
        sprint=sprint,
        ticket_id=str(created.id),
        worker_id=wid,
        spawned=spawned,
    )


def sprint_show(
    *,
    team: str,
    repo: Optional[Path] = None,
) -> SprintShowResult:
    """Show current sprint metadata."""
    paths = _paths_for(team=team, repo=repo)
    with locked_run(paths) as run:
        sprint_raw = run.get("sprint") if isinstance(run.get("sprint"), dict) else {}
        sprint = dict(sprint_raw or {})
        return SprintShowResult(
            team=paths.team,
            sprint=sprint,
            rev=int((sprint or {}).get("rev") or 0),
        )


def sprint_set(
    *,
    team: str,
    name: str,
    tag: Optional[str] = None,
    repo: Optional[Path] = None,
) -> SprintSetResult:
    """Update sprint metadata (name and/or tag) without spawning tickets."""
    _require_role(action="loom team sprint set", allowed_roles={ROLE_MANAGER})
    paths = _paths_for(team=team, repo=repo)
    now = _iso_z()
    with locked_run(paths) as run:
        sprint = _objective_state_set_sprint_state(
            run=run,
            name=str(name or ""),
            tag=str(tag or ""),
            now=now,
        )
        sprint_name = str(sprint.get("name") or "")
        sprint_tag = str(sprint.get("tag") or "")
        rev = int(sprint.get("rev") or 0)
        root = run_root(paths, run)
        tickets_dir = ensure_run_tickets_dir(run, repo_root=root)
        _sync_ticket_sprint_context(
            tickets_dir=tickets_dir,
            sprint_name=sprint_name,
            sprint_tag=sprint_tag,
        )
        charter_path = _write_charter(paths=paths, run=run)

        write_event(
            paths,
            event_type="sprint.updated",
            run=run,
            summary=f"Sprint updated name={sprint_name} tag={sprint_tag}",
            refs={"sprint": sprint_name, "tag": sprint_tag, "rev": rev},
        )

        return SprintSetResult(
            team=paths.team,
            sprint=sprint,
            rev=rev,
            charter=str(charter_path.resolve()),
        )


def sprint_clear(
    *,
    team: str,
    repo: Optional[Path] = None,
) -> SprintClearResult:
    """Clear sprint metadata from the run."""
    _require_role(action="loom team sprint clear", allowed_roles={ROLE_MANAGER})
    paths = _paths_for(team=team, repo=repo)
    with locked_run(paths) as run:
        rev = _objective_state_clear_sprint_state(run=run)
        root = run_root(paths, run)
        tickets_dir = ensure_run_tickets_dir(run, repo_root=root)
        _clear_ticket_sprint_context(tickets_dir=tickets_dir)
        charter_path = _write_charter(paths=paths, run=run)

        write_event(
            paths,
            event_type="sprint.cleared",
            run=run,
            summary="Sprint cleared",
            refs={"rev": rev},
        )

        return SprintClearResult(
            team=paths.team,
            rev=rev,
            charter=str(charter_path.resolve()),
        )


def spawn_integrator(
    *,
    team: str,
    worker_id: str = "integrator",
    window: str = "integrator",
    worktree: str = "merge-queue",
    branch: str = "",
    base_ref: str = "",
    force: bool = False,
    require_clean: bool = False,
    target_branch: str = "",
    remote: str = "",
    push: Optional[bool] = None,
    repo: Optional[Path] = None,
) -> SpawnIntegratorResult:
    """Spawn (or respawn) the persistent integrator.

    This worker is intentionally ticketless and operates out of a dedicated worktree.
    """

    _require_bin("tmux")
    _require_role(action="loom team spawn-integrator", allowed_roles={ROLE_MANAGER})

    paths = _paths_for(team=team, repo=repo)

    with locked_run(paths) as run:
        harness = _normalize_harness(str(run.get("harness") or ""))
        profile = resolve_builtin_profile(
            run,
            ROLE_INTEGRATOR,
        )
        enforce_member_lifecycle(profile=profile, role=ROLE_INTEGRATOR)
        if profile is not None and profile.harness:
            harness = _normalize_harness(profile.harness)
        cfg = (
            (run.get(harness) or {})
            if isinstance(run.get(harness), dict)
            else (run.get("opencode") or {})
        )
        agent_bin = str(cfg.get("bin") or "").strip() or harness
        _require_bin(agent_bin)
        session = str(run.get("session") or "")
        if not session:
            raise TeamError(
                "Run has no tmux session; did you run `loom team start`?",
                code="BAD_STATE",
            )
        if not tmux_has_session(session):
            raise TeamError(
                f"tmux session not found: {session}", code="TMUX", exit_code=2
            )

        root = run_root(paths, run)
        tickets_dir = ensure_run_tickets_dir(run, repo_root=root)
        paths.inbox_dir.mkdir(parents=True, exist_ok=True)
        paths.worktrees_dir.mkdir(parents=True, exist_ok=True)

        worker_id = sanitize(str(worker_id or "integrator"), max_len=32) or "integrator"
        window_hint = str(window or "integrator").strip() or "integrator"
        worktree_key = (
            sanitize(str(worktree or "merge-queue"), max_len=60) or "merge-queue"
        )
        merge_branch = str(branch or "").strip() or merge_branch_for_run(run)

        ms = _merge_state(run)
        cfg = dict(ms.get("config") or {})
        if target_branch:
            cfg["target_branch"] = str(target_branch)
        if remote:
            cfg["remote"] = str(remote)
        if push is not None:
            cfg["push"] = bool(push)
        # Migration: old runs defaulted push=False; new default is push=True.
        cfg.setdefault("push", True)
        ms["config"] = cfg
        ms["branch"] = merge_branch
        run["merge"] = ms

        target_branch = str(cfg.get("target_branch") or "main").strip() or "main"
        remote = str(cfg.get("remote") or "origin").strip() or "origin"
        base_ref = str(base_ref or "").strip() or target_branch

        # Ensure merge worktree exists (ws-managed).
        desired_wt_path = (paths.worktrees_dir / worktree_key).resolve()
        if not _is_path_within(paths.worktrees_dir, desired_wt_path):
            raise TeamError(
                f"Refusing to create worktree outside run worktrees dir: {desired_wt_path}",
                code="WORKTREE_PATH",
                exit_code=2,
            )
        if bool(force):
            # Best-effort recovery:
            # - kill existing tmux window
            # - remove run-scoped worktree path
            # - remove any existing worktree for merge branch
            # - prune metadata
            try:
                existing = dict((run.get("workers") or {}).get(worker_id) or {})
                win = str(existing.get("window") or "")
                if (
                    win
                    and tmux_has_session(session)
                    and tmux_window_exists(session, win)
                ):
                    tmux_kill_window(session, win)
            except Exception:
                pass
            try:
                repo_worktree_rm_path(
                    path=str(desired_wt_path),
                    root=root,
                    force=True,
                    confirm=True,
                )
            except Exception:
                pass
            try:
                repo_worktree_rm(
                    branch=merge_branch,
                    root=root,
                    force=True,
                    confirm=True,
                )
            except Exception:
                pass
            try:
                # Force means: treat the merge branch as disposable.
                # If it's corrupted (e.g. accidental commits), delete and recreate from base_ref.
                _run(["git", "branch", "-D", merge_branch], cwd=root, timeout=30.0)
            except Exception:
                pass
            try:
                repo_worktree_prune(root=root)
            except Exception:
                pass

        # Integrator is the system role responsible for cleaning/repairing its own
        # merge-queue worktree when needed. Do not block spawn on a dirty worktree
        # unless the caller explicitly requires it.
        wt = _ensure_worktree(
            cwd=root,
            path=desired_wt_path,
            branch=merge_branch,
            base_ref=base_ref,
            allow_dirty=not bool(require_clean),
        )
        wt_path = Path(wt["path"]).resolve()

        raw_mounts = run.get("mounts")
        mounts: list[dict] = []
        if isinstance(raw_mounts, list):
            mounts = [dict(x) for x in raw_mounts if isinstance(x, dict)]
        _apply_mounts(repo_root=root, worktree_root=wt_path, mounts=mounts)

        if harness == "opencode":
            _ensure_opencode_worktree_runtime(workdir=wt_path, repo_root=root)

        agent = (
            str(profile.agent)
            if profile is not None
            else _agent_for_role(run, ROLE_INTEGRATOR, harness=harness)
        )
        _require_agent_file_present(workdir=wt_path, harness=harness, agent=agent)
        cfg = (
            (run.get(harness) or {})
            if isinstance(run.get(harness), dict)
            else (run.get("opencode") or {})
        )
        model = _model_for_role(run, ROLE_INTEGRATOR, harness=harness)
        if not model and profile is not None and profile.model:
            model = str(profile.model)
        prompt = render_integrator_prompt(
            run=run,
            worker_id=worker_id,
            worktree_path=wt_path,
            branch=str(wt.get("branch") or merge_branch),
            base=str(wt.get("base") or base_ref),
            charter_path=paths.charter_file,
        )
        oc_argv = _team_tui_argv(
            project_dir=wt_path,
            agent=agent,
            prompt=prompt,
            model=model,
            harness=harness,
            bin=str(cfg.get("bin") or "").strip(),
        )

        sprint = _objective_state_sprint_state(run)
        pane_env = {
            ENV_TICKET_DIR: str(tickets_dir),
            ENV_TEAM_NAME: str(run.get("team") or paths.team),
            ENV_TEAM_RUN_ID: str(run.get("run_id") or ""),
            ENV_TEAM_RUN_DIR: str(paths.run_dir),
            ENV_TEAM_ROLE: ROLE_INTEGRATOR,
            ENV_TEAM_WORKER_ID: worker_id,
            ENV_TEAM_TICKET_ID: "",
            ENV_TEAM_SPRINT_NAME: sprint.get("name", ""),
            ENV_TEAM_SPRINT_TAG: sprint.get("tag", ""),
            "COMPOUND_ROOT": str(root),
        }

        workers = dict(run.get("workers") or {})
        existing = dict(workers.get(worker_id) or {})

        # Idempotency: if it exists and tmux window still exists, just return refreshed meta.
        if existing and not existing.get("retired"):
            win = str(existing.get("window") or "")
            if win and tmux_window_exists(session, win):
                pane_id = tmux_format(f"{session}:{win}", "#{pane_id}")
                existing["pane_id"] = pane_id
                existing["worktree"] = str(wt_path)
                existing["ticket_id"] = ""
                existing["role"] = ROLE_INTEGRATOR
                workers[worker_id] = existing
                run["workers"] = workers
                ms = _merge_state(run)
                ms["worker_id"] = worker_id
                ms["worktree"] = str(wt_path)
                ms["branch"] = str(wt.get("branch") or merge_branch)
                run["merge"] = ms

                write_event(
                    paths,
                    event_type="integrator.refreshed",
                    run=run,
                    summary=f"Integrator present worker_id={worker_id}",
                    refs={
                        "worker_id": worker_id,
                        "window": win,
                        "pane_id": pane_id,
                        "worktree": str(wt_path),
                        "branch": str(wt.get("branch") or merge_branch),
                    },
                )
                return SpawnIntegratorResult(
                    team=str(run.get("team") or paths.team),
                    worker_id=worker_id,
                    window=str(existing.get("window") or ""),
                    pane_id=str(existing.get("pane_id") or ""),
                    worktree=str(wt_path),
                    respawned=False,
                    worker=dict(existing),
                )
            else:
                # Record respawn history (best-effort).
                hist = list(existing.get("respawn_history") or [])
                hist.append(
                    {
                        "at": _iso_z(),
                        "window": win,
                        "pane_id": existing.get("pane_id"),
                        "reason": "missing",
                    }
                )
                existing["respawn_history"] = hist

        window = tmux_unique_window_name(session, window_hint)
        pane_id = tmux_new_window(
            session=session,
            name=window,
            cwd=wt_path,
            command=oc_argv,
            env=pane_env,
            set_options={
                TMUX_OPT_OWNED: "1",
                TMUX_OPT_TEAM: run.get("team"),
                TMUX_OPT_RUN_ID: run.get("run_id"),
            },
        )
        tmux_mark_pane(
            pane_id=pane_id,
            role=ROLE_INTEGRATOR,
            worker_id=worker_id,
            ticket_id=None,
        )

        workers[worker_id] = {
            "worker_id": worker_id,
            "role": ROLE_INTEGRATOR,
            "ticket_id": "",
            "roster_member_id": str(profile.member_id) if profile is not None else "",
            "roster_source": str(profile.source) if profile is not None else "",
            "roster_lifecycle": str(profile.lifecycle) if profile is not None else "",
            "worktree": str(wt_path),
            "worktree_key": worktree_key,
            "branch": str(wt.get("branch") or merge_branch),
            "base": str(wt.get("base") or base_ref),
            "window": window,
            "pane_id": pane_id,
            "spawned_at": _iso_z(),
            "retired": False,
            "worktree_retirable": False,
            "worktree_retirable_at": "",
            **(
                {"respawn_history": existing.get("respawn_history")}
                if existing.get("respawn_history")
                else {}
            ),
        }
        run["workers"] = workers

        ms = _merge_state(run)
        ms["worker_id"] = worker_id
        ms["worktree"] = str(wt_path)
        ms["branch"] = str(wt.get("branch") or merge_branch)
        # Allow configuration knobs for the integrator (optional).
        cfg = dict(ms.get("config") or {})
        if target_branch:
            cfg["target_branch"] = str(target_branch)
        if remote:
            cfg["remote"] = str(remote)
        if push is not None:
            cfg["push"] = bool(push)
        ms["config"] = cfg
        run["merge"] = ms

        write_event(
            paths,
            event_type="integrator.spawned",
            run=run,
            summary=f"Spawned integrator worker_id={worker_id}",
            refs={
                "worker_id": worker_id,
                "window": window,
                "pane_id": pane_id,
                "worktree": str(wt_path),
                "branch": str(wt.get("branch") or merge_branch),
            },
            data={
                "base_ref": base_ref,
                "forced": bool(force),
                "config": dict(cfg),
                "roster_member_id": str(profile.member_id)
                if profile is not None
                else "",
                "roster_source": str(profile.source) if profile is not None else "",
            },
        )
    return SpawnIntegratorResult(
        team=str(run.get("team") or paths.team),
        worker_id=worker_id,
        window=window,
        pane_id=pane_id,
        worktree=str(wt_path),
        respawned=True,
        worker=dict(workers.get(worker_id) or {}),
    )


def spawn_persona(
    *,
    team: str,
    member_id: str,
    repo: Optional[Path] = None,
    force: bool = False,
) -> SpawnPersonaResult:
    from agent_loom.team.personas import spawn_persona as _spawn_persona

    return _spawn_persona(team=team, member_id=member_id, repo=repo, force=force)


def status(*, team: str, repo: Optional[Path] = None) -> StatusResult:
    _require_bin("tmux")
    paths = _paths_for(team=team, repo=repo)
    run = load_run(paths)
    session = str(run.get("session") or "")
    if not session:
        raise TeamError("run.json missing session", code="BAD_STATE", exit_code=2)

    panes: Dict[str, Dict[str, str]] = {}
    if tmux_has_session(session):
        panes = tmux_list_panes(session)

    # Inbox + merge queue summaries (disk-backed durability).
    inbox_unacked_mgr = len(
        inbox_list_messages(paths, to="manager", unacked_only=True, limit=1000)
    )
    inbox_unacked_all = len(
        inbox_list_messages(paths, to=None, unacked_only=True, limit=1000)
    )
    merge_items = merge_list_items(run, include_done=False)
    merge_queued = len(
        [i for i in merge_items if str(i.get("state") or "") == "queued"]
    )
    merge_claimed = len(
        [i for i in merge_items if str(i.get("state") or "") == "claimed"]
    )

    ms = _merge_state(run)
    merge_cfg = dict(ms.get("config") or {})
    merge_target_branch = (
        str(merge_cfg.get("target_branch") or "main").strip() or "main"
    )
    merge_remote = str(merge_cfg.get("remote") or "origin").strip() or "origin"
    merge_push = bool(merge_cfg.get("push"))
    merge_branch = merge_branch_for_run(run)
    # Annotate workers with liveness.
    workers_out: Dict[str, Any] = {}
    for wid, w in (run.get("workers") or {}).items():
        pane_id = str((w or {}).get("pane_id") or "")
        pane = panes.get(pane_id) if pane_id else None
        workers_out[wid] = {
            **(w or {}),
            "alive": bool(pane and _pane_can_receive_chat(pane)),
            "tmux": pane or {},
        }

    mgr = dict(run.get("manager") or {})
    mgr_pane = str(mgr.get("pane_id") or "")
    mgr_info = panes.get(mgr_pane) if mgr_pane else None

    # Warnings (pathing + anchoring guardrails).
    warnings: List[Dict[str, str]] = []

    run_repo_root = Path(
        str(run.get("repo_root") or "").strip() or paths.repo_root
    ).resolve()
    run_dir = Path(str(run.get("run_dir") or "").strip() or paths.run_dir).resolve()
    tickets_dir = (
        Path(str(run.get("tickets_dir") or "").strip() or "").resolve()
        if str(run.get("tickets_dir") or "").strip()
        else None
    )

    if run_repo_root != paths.repo_root.resolve():
        warnings.append(
            {
                "code": "REPO_ROOT_MISMATCH",
                "message": f"run.json repo_root={run_repo_root} but discovered repo_root={paths.repo_root}",
            }
        )
    if run_dir != paths.run_dir.resolve():
        warnings.append(
            {
                "code": "RUN_DIR_MISMATCH",
                "message": f"run.json run_dir={run_dir} but expected run_dir={paths.run_dir}",
            }
        )
    if not _is_path_within(run_repo_root, run_dir):
        warnings.append(
            {
                "code": "RUN_DIR_OUTSIDE_REPO",
                "message": f"run_dir must be inside repo_root (repo_root={run_repo_root} run_dir={run_dir})",
            }
        )
    if tickets_dir and not _is_path_within(run_repo_root, tickets_dir):
        warnings.append(
            {
                "code": "TICKET_DIR_OUTSIDE_REPO",
                "message": f"tickets_dir must be inside repo_root (repo_root={run_repo_root} tickets_dir={tickets_dir})",
            }
        )
    if not tmux_has_session(session):
        warnings.append(
            {
                "code": "TMUX_SESSION_MISSING",
                "message": f"tmux session not found: {session} (run `loom team start {paths.team} --repo {paths.repo_root}`)",
            }
        )

    # Worker worktree mismatch warnings.
    active_workers_for_checks = {
        wid: w
        for wid, w in (run.get("workers") or {}).items()
        if not bool((w or {}).get("retired"))
    }
    for wid, w in active_workers_for_checks.items():
        workspace = str((w or {}).get("workspace") or "").strip().lower()
        if workspace == "repo_root":
            continue
        wt = str((w or {}).get("worktree") or "").strip()
        if wt and not _is_path_within(paths.worktrees_dir, Path(wt)):
            warnings.append(
                {
                    "code": "WORKTREE_OUTSIDE_RUN",
                    "message": f"worker {wid} worktree not under {paths.worktrees_dir}: {wt}",
                }
            )

    payload = {
        "team": str(run.get("team") or paths.team),
        "run_id": str(run.get("run_id") or ""),
        "session": session,
        "repo_root": str(run.get("repo_root") or ""),
        "run_dir": str(run.get("run_dir") or paths.run_dir),
        "tickets_dir": str(run.get("tickets_dir") or ""),
        "sprint": dict(run.get("sprint") or {}),
        "roster": _roster_summary_from_run(run),
        "inbox": {
            "unacked_to_manager": inbox_unacked_mgr,
            "unacked_total": inbox_unacked_all,
        },
        "merge_queue": {
            "queued": merge_queued,
            "claimed": merge_claimed,
            "pending": len(merge_items),
            "merge_branch": merge_branch,
            "target_branch": merge_target_branch,
            "remote": merge_remote,
            "push": merge_push,
        },
        "manager": {**mgr, "tmux": mgr_info or {}},
        "workers": workers_out,
        "warnings": warnings,
    }

    # Disk-backed snapshot for UI/state inspection.
    def _persist_status_snapshot() -> None:
        paths.snapshots_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write_json(paths.status_snapshot_file, payload)

    best_effort(_persist_status_snapshot, label="status.snapshot.persist")

    safe_write_event(
        paths,
        event_type="status.snapshot",
        run=run,
        summary=f"Status snapshot workers={len(workers_out)} inbox_unacked_mgr={inbox_unacked_mgr} merge_pending={len(merge_items)}",
        data={
            "workers_total": len(workers_out),
            "workers_alive": len(
                [
                    wid
                    for wid, w in workers_out.items()
                    if not bool((w or {}).get("retired")) and bool(w.get("alive"))
                ]
            ),
            "inbox_unacked_to_manager": inbox_unacked_mgr,
            "inbox_unacked_total": inbox_unacked_all,
            "merge_pending": len(merge_items),
            "merge_queued": merge_queued,
            "merge_claimed": merge_claimed,
            "warnings": len(warnings),
        },
    )

    return StatusResult(
        team=str(payload.get("team") or paths.team),
        run_id=str(payload.get("run_id") or ""),
        session=session,
        repo_root=str(payload.get("repo_root") or ""),
        run_dir=str(payload.get("run_dir") or ""),
        tickets_dir=str(payload.get("tickets_dir") or ""),
        sprint=dict(payload.get("sprint") or {}),
        roster=dict(payload.get("roster") or {}),
        inbox=dict(payload.get("inbox") or {}),
        merge_queue=dict(payload.get("merge_queue") or {}),
        manager=dict(payload.get("manager") or {}),
        workers=dict(payload.get("workers") or {}),
        warnings=list(payload.get("warnings") or []),
    )


def doctor(*, team: str, repo: Optional[Path] = None) -> DoctorResult:
    """Diagnose tmux/run-state drift and suggest remediation commands.

    Doctor is advisory: it does not kill processes or delete worktrees.
    """

    paths = _paths_for(team=team, repo=repo)
    run = load_run(paths)
    session = str(run.get("session") or "").strip()
    run_id = str(run.get("run_id") or "").strip()

    issues: List[Dict[str, Any]] = []
    suggestions: List[str] = []

    def add_suggestion(cmd: str) -> None:
        c = str(cmd or "").strip()
        if not c:
            return
        if c not in suggestions:
            suggestions.append(c)

    if not session:
        issues.append(
            {
                "code": "BAD_STATE",
                "message": "run.json missing tmux session",
            }
        )
        add_suggestion(f"loom team start {paths.team} --repo {paths.repo_root}")
        return DoctorResult(
            team=str(run.get("team") or paths.team),
            run_id=run_id,
            session=session,
            issues=issues,
            suggestions=suggestions,
        )

    panes: Dict[str, Dict[str, str]] = {}
    if tmux_has_session(session):
        panes = tmux_list_panes(session)
    else:
        issues.append(
            {
                "code": "TMUX_SESSION_MISSING",
                "message": f"tmux session not found: {session}",
            }
        )
        add_suggestion(f"loom team start {paths.team} --repo {paths.repo_root}")

    raw_workers = run.get("workers")
    workers: Dict[str, Any] = dict(raw_workers) if isinstance(raw_workers, dict) else {}

    # Worker pane/window drift
    for wid, w in sorted((workers or {}).items()):
        if not isinstance(w, dict):
            continue
        if bool(w.get("retired")):
            continue
        role = str(w.get("role") or "").strip().lower()
        win = str(w.get("window") or "").strip()
        pane_id = str(w.get("pane_id") or "").strip()

        if (
            session
            and tmux_has_session(session)
            and win
            and not tmux_window_exists(session, win)
        ):
            issues.append(
                {
                    "code": "WORKER_WINDOW_MISSING",
                    "message": f"worker {wid} window missing: {win}",
                    "worker_id": wid,
                    "window": win,
                    "role": role,
                }
            )
            add_suggestion(f"loom team status {paths.team} --show-dead")
            if role == ROLE_INTEGRATOR or wid == "integrator":
                add_suggestion(f"loom team spawn-integrator {paths.team}")
            else:
                add_suggestion(f"loom team retire {paths.team} {wid}")
                add_suggestion(f"loom team resume-worker {paths.team} {wid}")

        if panes and pane_id and pane_id not in panes:
            refreshed = ""
            if (
                session
                and win
                and tmux_has_session(session)
                and tmux_window_exists(session, win)
            ):
                try:
                    refreshed = tmux_format(f"{session}:{win}", "#{pane_id}")
                except Exception:
                    refreshed = ""
            issues.append(
                {
                    "code": "PANE_MISSING",
                    "message": f"worker {wid} pane not found: {pane_id}",
                    "worker_id": wid,
                    "pane_id": pane_id,
                    "window": win,
                    "role": role,
                    **({"refreshed_pane_id": refreshed} if refreshed else {}),
                }
            )
            add_suggestion(f"loom team status {paths.team} --show-dead")
            if role == ROLE_INTEGRATOR or wid == "integrator":
                add_suggestion(f"loom team spawn-integrator {paths.team}")
                add_suggestion(f"loom team spawn-integrator {paths.team} --force")
            else:
                add_suggestion(f"loom team retire {paths.team} {wid}")
                add_suggestion(f"loom team resume-worker {paths.team} {wid}")

    # Merge queue stalled on missing integrator.
    merge_items = merge_list_items(run, include_done=False)
    claimed = [i for i in (merge_items or []) if str(i.get("state") or "") == "claimed"]
    if claimed and panes:
        integrators = [
            (wid, w)
            for wid, w in (workers or {}).items()
            if isinstance(w, dict)
            and not bool(w.get("retired"))
            and str(w.get("role") or "").strip().lower() == ROLE_INTEGRATOR
        ]
        alive = False
        for wid, w in integrators:
            pid = str(w.get("pane_id") or "").strip()
            pane = panes.get(pid) if pid else None
            if pane and _pane_can_receive_chat(pane):
                alive = True
                break
        if not alive:
            issues.append(
                {
                    "code": "MERGE_QUEUE_STALLED",
                    "message": f"merge queue has {len(claimed)} claimed items but no live integrator pane",
                }
            )
            add_suggestion(f"loom team spawn-integrator {paths.team}")

    # Integrator worktree dirtiness (best-effort).
    try:
        _require_bin("git")
        integ = (workers or {}).get("integrator") if isinstance(workers, dict) else None
        if isinstance(integ, dict):
            wt = str(integ.get("worktree") or "").strip()
            if wt:
                p = _run(
                    ["git", "status", "--porcelain"],
                    cwd=Path(wt),
                    check=False,
                    timeout=5.0,
                )
                if bool((p.stdout or "").strip()):
                    issues.append(
                        {
                            "code": "INTEGRATOR_WORKTREE_DIRTY",
                            "message": f"integrator worktree has uncommitted changes: {wt}",
                            "worktree": wt,
                        }
                    )
                    add_suggestion(
                        f"loom team spawn-integrator {paths.team} --require-clean"
                    )
    except Exception:
        pass

    return DoctorResult(
        team=str(run.get("team") or paths.team),
        run_id=run_id,
        session=session,
        issues=issues,
        suggestions=suggestions,
    )


def capture(
    *,
    team: str,
    target: str,
    lines: int = 200,
    no_join: bool = False,
    repo: Optional[Path] = None,
) -> CaptureResult:
    _require_bin("tmux")
    paths = _paths_for(team=team, repo=repo)
    with locked_run(paths) as run:
        session = str(run.get("session") or "")
        if not tmux_has_session(session):
            raise TeamError(
                f"tmux session not found: {session}",
                code="TMUX",
                exit_code=2,
                hint="Start (or resume) the team tmux session first.",
                suggestions=[
                    f"loom team start {paths.team} --repo {paths.repo_root}",
                    f"loom team status {paths.team}",
                ],
            )

        pane_id, meta = _resolve_target(run, target)
        panes = tmux_list_panes(session)
        pane = panes.get(pane_id)

        if not pane:
            # Pane ids can drift. Try to refresh using the worker's window name.
            wid = str((meta or {}).get("worker_id") or "").strip()
            w = (
                (run.get("workers") or {}).get(wid)
                if wid and isinstance(run.get("workers"), dict)
                else None
            )
            win = (
                str((w or {}).get("window") or "").strip()
                if isinstance(w, dict)
                else ""
            )
            if wid and win and tmux_window_exists(session, win):
                refreshed = tmux_format(f"{session}:{win}", "#{pane_id}")
                if refreshed:
                    pane_id = refreshed
                    meta = {**dict(meta or {}), "pane_id": pane_id}
                    try:
                        workers = dict(run.get("workers") or {})
                        w2 = dict(workers.get(wid) or {})
                        w2["pane_id"] = pane_id
                        workers[wid] = w2
                        run["workers"] = workers
                    except Exception:
                        pass
                    panes = tmux_list_panes(session)
                    pane = panes.get(pane_id)

        if not pane:
            role = str((meta or {}).get("role") or "").strip().lower()
            wid = str((meta or {}).get("worker_id") or "").strip()
            sugg = [f"loom team status {paths.team} --show-dead"]
            if role == ROLE_INTEGRATOR or (
                str(target or "").strip() in {"integrator", "merge-queue"}
            ):
                sugg += [
                    f"loom team spawn-integrator {paths.team}",
                    f"loom team spawn-integrator {paths.team} --force",
                ]
            elif wid:
                sugg += [
                    f"loom team retire {paths.team} {wid}",
                    f"loom team resume-worker {paths.team} {wid}",
                ]
            raise TeamError(
                f"pane not found: {pane_id}",
                code="TMUX",
                exit_code=2,
                hint="The run state references a tmux pane that no longer exists.",
                suggestions=sugg,
                data={
                    "target": str(target or ""),
                    "pane_id": pane_id,
                    "meta": dict(meta or {}),
                },
            )

    cap = _capture_pane_and_persist(
        paths,
        run=run,
        pane_id=pane_id,
        target_key=str(target or ""),
        target_meta=meta,
        pane=pane,
        lines=int(lines),
        no_join=bool(no_join),
        summary=f"Captured {target} lines={int(lines)}",
    )

    captured_at = str(cap.get("captured_at") or "")
    out = str(cap.get("output") or "")

    return CaptureResult(
        team=str(run.get("team") or paths.team),
        target=dict(meta or {}),
        pane=dict(pane or {}),
        captured_at=captured_at,
        output=out,
        output_file=str(cap.get("output_file") or ""),
        meta_file=str(cap.get("meta_file") or ""),
    )


def send(
    *,
    team: str,
    target: str,
    message: str,
    force: bool = False,
    repo: Optional[Path] = None,
) -> SendResult:
    """Send a message to a Team target.

    Delivery semantics are intentionally durable:
      - Message is always persisted to the disk inbox for the run.
      - tmux nudge is best-effort; sidecars wake via tmux wait-for.
    """

    paths = _paths_for(team=team, repo=repo)

    msg = str(message or "").rstrip("\n")
    if not msg:
        raise TeamError("Empty message", code="ARG", exit_code=2)

    with locked_run(paths, save=False) as run:
        sender_role, sender_target = sender_for_send()
        requested_target = str(target or "").strip()
        concrete_target, used_escalation = resolve_send_target(
            run=run,
            target=requested_target,
            sender_role=sender_role,
        )

        resolved_targets = _resolve_targets(run, concrete_target)
        policy = communication_policy_from_run(run)
        routes = dict(policy.get("routes") or {})
        allowed_tokens = tuple(routes.get(sender_role) or ())

        if not allowed_tokens:
            raise TeamError(
                f"Communication route forbidden: role {sender_role} has no allowed routes",
                code="PERMISSION",
                exit_code=2,
            )

        requested_norm = str(requested_target or "").strip().lower()
        if used_escalation:
            requested_norm = "escalate"

        for recipient in resolved_targets:
            if not route_allows_target(
                allowed_tokens=allowed_tokens,
                requested_target=requested_norm,
                recipient=recipient,
            ):
                raise TeamError(
                    (
                        "Communication route forbidden: "
                        f"{sender_role} -> {recipient.get('role') or 'unknown'} "
                        f"for target {requested_target!r}"
                    ),
                    code="PERMISSION",
                    exit_code=2,
                    data={
                        "sender_role": sender_role,
                        "sender_target": sender_target,
                        "requested_target": requested_target,
                        "recipient": dict(recipient),
                        "allowed": list(allowed_tokens),
                    },
                )

        deliveries: List[Dict[str, Any]] = []
        suggestion_set: set[str] = set()

        for recipient in resolved_targets:
            dispatch_target = str(recipient.get("worker_id") or "").strip() or "manager"
            inbox_msg, _recipient, delivered, delivery_reason, meta = (
                _inbox_write_and_maybe_nudge(
                    paths=paths,
                    run=run,
                    target=dispatch_target,
                    message=msg,
                    sender="team",
                    kind="send",
                    meta_extra={
                        "team": str(run.get("team") or paths.team),
                        "requested_target": requested_target,
                        "dispatch_target": dispatch_target,
                    },
                    nudge=True,
                    force=bool(force),
                    line_info=f"to={dispatch_target}",
                )
            )

            entry = {
                "requested_target": requested_target,
                "dispatch_target": dispatch_target,
                "role": str(recipient.get("role") or ""),
                "worker_id": str(recipient.get("worker_id") or ""),
                "ticket_id": str(recipient.get("ticket_id") or ""),
                "inbox_id": str(inbox_msg.get("id") or ""),
                "delivered": bool(delivered),
                "delivery_reason": str(delivery_reason or ""),
                "meta": dict(meta or {}),
            }
            deliveries.append(entry)

            if not delivered:
                for suggestion in delivery_suggestions(
                    paths=paths,
                    target=dispatch_target,
                    delivery_reason=str(delivery_reason or ""),
                    meta=dict(meta or {}),
                ):
                    suggestion_set.add(suggestion)

        all_delivered = bool(deliveries) and all(
            bool(item.get("delivered")) for item in deliveries
        )
        any_delivered = any(bool(item.get("delivered")) for item in deliveries)
        if all_delivered:
            delivery_reason = ""
        elif any_delivered:
            delivery_reason = "partial_delivery"
        else:
            first_reason = (
                str(deliveries[0].get("delivery_reason") or "") if deliveries else ""
            )
            delivery_reason = first_reason or "undelivered"

        inbox_ids = [
            str(item.get("inbox_id") or "")
            for item in deliveries
            if str(item.get("inbox_id") or "")
        ]
        inbox_summary: Dict[str, Any] = {
            "id": inbox_ids[0] if inbox_ids else "",
            "ids": inbox_ids,
            "count": len(inbox_ids),
        }
        target_summary: Dict[str, Any] = {
            "target": requested_target,
            "resolved": len(deliveries),
        }
        if len(deliveries) == 1:
            target_summary = {
                **target_summary,
                "role": str(deliveries[0].get("role") or ""),
                "worker_id": str(deliveries[0].get("worker_id") or ""),
                "ticket_id": str(deliveries[0].get("ticket_id") or ""),
            }

        write_event(
            paths,
            event_type="message.sent",
            run=run,
            summary=(
                f"Message queued target={requested_target} recipients={len(deliveries)} "
                f"delivered={all_delivered}"
            ),
            refs={
                "sender_role": sender_role,
                "sender_target": sender_target,
                "requested_target": requested_target,
                "inbox_id": str(inbox_summary.get("id") or ""),
            },
            data={
                "target": requested_target,
                "resolved_target": concrete_target,
                "used_escalation": bool(used_escalation),
                "delivered": bool(all_delivered),
                "delivery_reason": str(delivery_reason or ""),
                "deliveries": deliveries,
            },
        )

    return SendResult(
        team=str(run.get("team") or paths.team),
        target=target_summary,
        delivered=bool(all_delivered),
        delivery_reason=str(delivery_reason or ""),
        inbox=dict(inbox_summary),
        deliveries=list(deliveries),
        suggestions=sorted(suggestion_set),
    )


def inbox_list(
    *,
    team: str,
    to: str = "",
    unacked_only: bool = False,
    limit: int = 200,
    repo: Optional[Path] = None,
) -> InboxListResult:
    paths = _paths_for(team=team, repo=repo)
    msgs = inbox_list_messages(
        paths,
        to=str(to or "").strip() or None,
        unacked_only=bool(unacked_only),
        limit=int(limit),
    )
    return InboxListResult(team=paths.team, count=len(msgs), messages=list(msgs))


def inbox_show(
    *, team: str, msg_id: str, repo: Optional[Path] = None
) -> InboxShowResult:
    paths = _paths_for(team=team, repo=repo)
    p = _inbox_msg_path(paths, str(msg_id or ""))
    if not p or not p.exists():
        raise TeamError(f"inbox message not found: {msg_id}", code="ARG", exit_code=2)
    msg = _read_json(p)
    if not isinstance(msg, dict):
        raise TeamError(f"invalid inbox message: {p}", code="BAD_STATE", exit_code=2)
    return InboxShowResult(team=paths.team, message=msg)


def inbox_ack(*, team: str, msg_id: str, repo: Optional[Path] = None) -> InboxAckResult:
    paths = _paths_for(team=team, repo=repo)
    msg = inbox_ack_message(paths, str(msg_id or ""))

    run0 = best_effort(lambda: load_run(paths), label="inbox.acked.load_run")
    run = run0 if isinstance(run0, dict) else None
    safe_write_event(
        paths,
        event_type="inbox.acked",
        run=run,
        summary=f"Inbox acked id={str(msg.get('id') or '')}",
        refs={"inbox_id": str(msg.get("id") or ""), "to": str(msg.get("to") or "")},
        data={
            "from": str(msg.get("from") or ""),
            "kind": str(msg.get("kind") or ""),
            "created_at": str(msg.get("created_at") or ""),
            "acked_at": str(msg.get("acked_at") or ""),
        },
    )
    return InboxAckResult(team=paths.team, message=dict(msg))


def inbox_send(
    *,
    team: str,
    to: str,
    message: str,
    kind: str = "note",
    sender: str = "team",
    nudge: bool = True,
    force: bool = False,
    repo: Optional[Path] = None,
) -> InboxSendResult:
    paths = _paths_for(team=team, repo=repo)
    to = str(to or "").strip()
    if not to:
        raise TeamError("--to is required", code="ARG", exit_code=2)
    message = str(message or "").rstrip("\n")
    if not message:
        raise TeamError("--message is required", code="ARG", exit_code=2)
    kind = str(kind or "note").strip()
    sender = str(sender or "team").strip()

    with locked_run(paths, save=False) as run:
        inbox_msg, _recipient, nudged, _reason, _meta = _inbox_write_and_maybe_nudge(
            paths=paths,
            run=run,
            target=to,
            message=message,
            sender=sender,
            kind=kind,
            nudge=bool(nudge),
            force=bool(force),
            line_info=f"kind={kind} from={sender}",
        )

        write_event(
            paths,
            event_type="inbox.sent",
            run=run,
            summary=f"Inbox message queued to={to} kind={kind} nudged={nudged}",
            refs={"inbox_id": str(inbox_msg.get("id") or ""), "to": str(to)},
            data={
                "sender": sender,
                "kind": kind,
                "nudged": bool(nudged),
                "bytes": len(message.encode("utf-8")),
            },
        )

    return InboxSendResult(team=paths.team, inbox=dict(inbox_msg), nudged=bool(nudged))


def _infer_team_from_tmux_env() -> Optional[str]:
    """Best-effort: infer Team name from the current tmux client/pane."""

    if not os.environ.get("TMUX"):
        return None
    pane = os.environ.get("TMUX_PANE") or ""
    if not pane:
        return None
    try:
        p = tmux_cmd(["display-message", "-p", "-t", pane, "#{session_name}"])
        session = (p.stdout or "").strip()
    except Exception:
        return None
    if not session:
        return None
    team = tmux_get_option(target=session, option=TMUX_OPT_TEAM)
    if team:
        return sanitize(team, max_len=80) or None
    # Fallback: resolve from session name prefix.
    try:
        return resolve_team_from_session(session)
    except Exception:
        return None


def wait(
    *,
    team: Optional[str],
    duration: str,
    repo: Optional[Path] = None,
) -> WaitResult:
    """Block for a duration, waking early on manager inbox signals."""

    team_value = sanitize(str(team or ""), max_len=80)
    dur_raw = str(duration or "").strip()

    if not team_value:
        inferred = _infer_team_from_tmux_env()
        if inferred:
            team_value = inferred

    if not team_value:
        raise TeamError(
            "Team is required when not running inside a team tmux session. Use: loom team wait <TEAM> <DUR>",
            code="ARG",
            exit_code=2,
        )

    seconds = _parse_duration_seconds(dur_raw)

    paths = _paths_for(team=team_value, repo=repo)
    run = load_run(paths)
    run_id = str(run.get("run_id") or "")
    session = str(run.get("session") or "")
    recipient = "manager"
    if os.environ.get("TMUX"):
        role = str(os.getenv(ENV_TEAM_ROLE) or "").strip().lower()
        if role and role != ROLE_MANAGER:
            wid = sanitize(str(os.getenv(ENV_TEAM_WORKER_ID) or ""), max_len=48)
            if wid:
                recipient = wid
    ch = channel_for(run_id=run_id, to=recipient)

    op_id = uuid.uuid4().hex[:12]
    start_t = time.time()
    safe_write_event(
        paths,
        event_type="wait.started",
        run=run,
        summary=f"Wait started recipient={recipient} seconds={seconds}",
        refs={"recipient": recipient},
        data={"seconds": int(seconds), "use_tmux": bool(os.environ.get("TMUX"))},
        op_id=op_id,
    )

    use_tmux = False
    if session and tmux_available():
        try:
            use_tmux = tmux_has_session(session)
        except Exception:
            use_tmux = False

    wake_reason = "sleep"
    signaled = False
    if use_tmux:
        signaled = tmux_wait_for(ch, timeout_s=float(seconds))
        wake_reason = "signal" if signaled else "timeout"
    else:
        time.sleep(seconds)
    safe_write_event(
        paths,
        event_type="wait.finished",
        run=run,
        summary=f"Wait finished recipient={recipient} reason={wake_reason}",
        refs={"recipient": recipient},
        data={
            "seconds": int(seconds),
            "elapsed_s": round(time.time() - start_t, 3),
            "wake_reason": wake_reason,
            "signaled": bool(signaled),
            "channel": ch,
        },
        op_id=op_id,
    )

    # Manager operational rigor:
    # If the manager keeps timing out (no inbox wake), proactively check in with workers.
    # This prevents "everyone is waiting" deadlocks and helps unstick agent UIs.
    if recipient == "manager":
        _maybe_manager_checkin_after_wait(
            paths=paths,
            wake_reason=wake_reason,
        )

    return WaitResult(
        team=team_value,
        recipient=recipient,
        seconds=int(seconds),
        wake_reason=wake_reason,
        signaled=bool(signaled),
        elapsed_s=round(time.time() - start_t, 3),
        channel=ch,
    )


def _maybe_manager_checkin_after_wait(*, paths: RunPaths, wake_reason: str) -> None:
    timeout_like = str(wake_reason or "").strip().lower() in {"timeout", "sleep"}
    now = time.time()

    # Check-in policy (kept intentionally simple and deterministic):
    # - after N consecutive timeout-like waits, nudge up to K active workers
    # - per-worker cooldown prevents harassment
    streak_threshold = 2
    per_worker_cooldown_s = 20.0 * 60.0
    max_targets = 2

    def _get_ops_dict(run: Dict[str, Any]) -> Dict[str, Any]:
        raw = run.get("ops")
        return dict(raw) if isinstance(raw, dict) else {}

    def _get_mgr_dict(ops: Dict[str, Any]) -> Dict[str, Any]:
        raw = ops.get("manager")
        return dict(raw) if isinstance(raw, dict) else {}

    def _get_checkin_dict(mgr: Dict[str, Any]) -> Dict[str, Any]:
        raw = mgr.get("checkin")
        return dict(raw) if isinstance(raw, dict) else {}

    def _coerce_float(v: Any) -> float:
        try:
            return float(v)
        except Exception:
            return 0.0

    def _coerce_int(v: Any) -> int:
        try:
            return int(v)
        except Exception:
            return 0

    with locked_run(paths) as run:
        ops = _get_ops_dict(run)
        mgr = _get_mgr_dict(ops)
        checkin = _get_checkin_dict(mgr)

        streak = _coerce_int(checkin.get("timeout_streak"))
        by_worker_raw = checkin.get("by_worker")
        by_worker: Dict[str, float] = {}
        if isinstance(by_worker_raw, dict):
            for k, v in by_worker_raw.items():
                kk = str(k).strip()
                if kk:
                    by_worker[kk] = _coerce_float(v)

        if not timeout_like:
            # Any inbox signal (or other wake) breaks the streak.
            checkin["timeout_streak"] = 0
            checkin["updated_at"] = now
            mgr["checkin"] = checkin
            ops["manager"] = mgr
            run["ops"] = ops
            return

        streak += 1

        # Persist the streak even if we don't check in this time.
        checkin["timeout_streak"] = streak
        checkin["updated_at"] = now

        if streak < streak_threshold:
            mgr["checkin"] = checkin
            ops["manager"] = mgr
            run["ops"] = ops
            return

        active_count, active_ids, _active_roles = _active_spawn_headcount(run)
        if active_count <= 0:
            # Nothing to check in on; keep streak but don't spam.
            mgr["checkin"] = checkin
            ops["manager"] = mgr
            run["ops"] = ops
            return

        eligible: list[str] = []
        for wid in active_ids:
            last = float(by_worker.get(str(wid), 0.0))
            if last <= 0.0 or (now - last) >= per_worker_cooldown_s:
                eligible.append(str(wid))

        # Pick the least-recently-checkin workers first (stable ordering).
        eligible.sort(key=lambda w: (by_worker.get(w, 0.0), w))
        targets = eligible[: int(max_targets)]
        if not targets:
            # Cooldown blocks all; just persist streak.
            mgr["checkin"] = checkin
            ops["manager"] = mgr
            run["ops"] = ops
            return

        sent_to: list[str] = []
        for wid in targets:
            try:
                msg = (
                    "TEAM: manager check-in. Please post a loom ticket update (status + next step). "
                    "If blocked, summarize what you tried and give 2 options. "
                    "If you have no moves, you may self-retire (keeps worktree): "
                    f"`loom team retire {paths.team} {wid}`."
                )
                _inbox_write_and_maybe_nudge(
                    paths=paths,
                    run=run,
                    target=wid,
                    message=msg,
                    sender="manager",
                    kind="checkin",
                    meta_extra={
                        "op": "manager_checkin",
                        "timeout_streak": streak,
                        "worker_id": wid,
                    },
                    nudge=True,
                    force=False,
                    line_info="manager_checkin",
                )
                by_worker[str(wid)] = now
                sent_to.append(str(wid))
            except Exception:
                continue

        if sent_to:
            # Reset streak after a successful check-in to avoid repeated mass nudges.
            checkin["timeout_streak"] = 0
            checkin["last_checkin_at"] = now
            checkin["by_worker"] = dict(by_worker)

            write_event(
                paths,
                event_type="manager.checkin",
                run=run,
                summary=f"Manager check-in sent_to={','.join(sent_to)}",
                refs={"recipients": ",".join(sent_to)},
                data={
                    "sent_to": list(sent_to),
                    "timeout_streak": int(streak),
                    "cooldown_s": int(per_worker_cooldown_s),
                    "max_targets": int(max_targets),
                },
            )

        mgr["checkin"] = checkin
        ops["manager"] = mgr
        run["ops"] = ops


def merge_enqueue(
    *,
    team: str,
    branch: str,
    ticket_id: str = "",
    from_worker: str = "",
    note: str = "",
    nudge: bool = True,
    repo: Optional[Path] = None,
) -> MergeEnqueueResult:
    _require_role(action="loom team merge enqueue", allowed_roles={ROLE_MANAGER})
    paths = _paths_for(team=team, repo=repo)
    branch = str(branch or "").strip()
    if not branch:
        raise TeamError("--branch is required", code="ARG", exit_code=2)
    ticket_id = str(ticket_id or "").strip()
    from_worker = str(from_worker or "").strip()
    note = str(note or "").strip()

    with locked_run(paths) as run:
        item = merge_enqueue_item(
            run, branch=branch, ticket_id=ticket_id, from_worker=from_worker, note=note
        )

        tmux_signal(
            channel_for(
                run_id=str(run.get("run_id") or ""),
                to=str(_merge_state(run).get("worker_id") or "integrator"),
            )
        )

        # Nudge integrator if present.
        nudged = False
        if bool(nudge):
            ms = _merge_state(run)
            mwid = str(ms.get("worker_id") or "integrator")
            session = str(run.get("session") or "")
            if session and tmux_has_session(session):
                try:
                    pane_id, _ = _resolve_target(run, mwid)
                    panes = tmux_list_panes(session)
                    pane = panes.get(pane_id)
                    if pane and _pane_can_receive_chat(pane):
                        line = f"TEAM merge_queue enqueued id={item['id']} ticket={ticket_id or '-'} branch={branch}"
                        tmux_send_text(
                            pane_id,
                            line,
                            enter=True,
                            ctrl_enter=(
                                str(run.get("harness") or "").strip().lower() == "omp"
                            ),
                        )
                        nudged = True
                except Exception:
                    nudged = False

        write_event(
            paths,
            event_type="merge.enqueued",
            run=run,
            summary=f"Merge enqueued item={str(item.get('id') or '')} ticket={ticket_id or '-'}",
            refs={
                "merge_item_id": str(item.get("id") or ""),
                "ticket_id": ticket_id,
                "branch": branch,
                "from_worker": from_worker,
            },
            data={"note": note, "nudged": bool(nudged)},
        )

    return MergeEnqueueResult(team=paths.team, item=dict(item), nudged=bool(nudged))


def merge_list(
    *, team: str, include_done: bool = False, repo: Optional[Path] = None
) -> MergeListResult:
    paths = _paths_for(team=team, repo=repo)
    run = load_run(paths)
    items = merge_list_items(run, include_done=bool(include_done))
    return MergeListResult(team=paths.team, count=len(items), items=list(items))


def merge_next(
    *, team: str, claim_by: str = "", repo: Optional[Path] = None
) -> MergeNextResult:
    _require_role(
        action="loom team merge next", allowed_roles={ROLE_MANAGER, ROLE_INTEGRATOR}
    )
    paths = _paths_for(team=team, repo=repo)
    claimed_by = str(claim_by or "").strip()
    with locked_run(paths) as run:
        item = merge_claim_next(run, claimed_by=claimed_by)

        write_event(
            paths,
            event_type="merge.claimed",
            run=run,
            summary=(
                f"Merge claimed item={str((item or {}).get('id') or '')} by={claimed_by or '-'}"
                if item
                else f"Merge claim empty by={claimed_by or '-'}"
            ),
            refs={
                "merge_item_id": str((item or {}).get("id") or ""),
                "ticket_id": str((item or {}).get("ticket_id") or ""),
                "branch": str((item or {}).get("branch") or ""),
                "claimed_by": claimed_by,
            },
            data={"empty": (item is None)},
        )
    return MergeNextResult(team=paths.team, item=dict(item) if item else None)


def merge_done(
    *,
    team: str,
    item_id: str,
    result: str,
    note: str = "",
    repo: Optional[Path] = None,
) -> MergeDoneResult:
    _require_bin("tmux")
    _require_role(
        action="loom team merge done", allowed_roles={ROLE_MANAGER, ROLE_INTEGRATOR}
    )
    paths = _paths_for(team=team, repo=repo)
    item_id = str(item_id or "").strip()
    if not item_id:
        raise TeamError("item_id required", code="ARG", exit_code=2)
    result = str(result or "").strip()
    if result not in ("merged", "blocked", "dropped"):
        raise TeamError(
            "--result must be one of: merged, blocked, dropped", code="ARG", exit_code=2
        )
    note = str(note or "").strip()
    with locked_run(paths) as run:
        item = merge_mark_done(run, item_id=item_id, result=result, note=note)

        # Notify manager + retire originating worker when merged.

        if result == "merged":
            tid = str(item.get("ticket_id") or "")
            from_worker = str(item.get("from_worker") or "").strip()

            _inbox_write_and_maybe_nudge(
                paths=paths,
                run=run,
                target="manager",
                message=(
                    f"MERGED into merge-queue: item={item_id} ticket={tid or '-'} from_worker={from_worker or '-'} "
                    f"| next: ship with `loom team ship {paths.team}`; when safe: mark-retirable worker={from_worker or '-'}"
                ),
                sender="team",
                kind="merge",
                meta_extra={
                    "item_id": item_id,
                    "ticket_id": tid,
                    "from_worker": from_worker,
                },
                nudge=True,
                force=False,
                line_info="merge_done",
            )

            # Auto-retire worker (keep worktree) for robustness.
            if from_worker and from_worker in dict(run.get("workers") or {}):
                workers = dict(run.get("workers") or {})
                w = dict(workers.get(from_worker) or {})
                if w and not bool(w.get("retired")):
                    session = str(run.get("session") or "")
                    window = str(w.get("window") or "")
                    if session and window and tmux_has_session(session):
                        tmux_kill_window(session, window)
                    w["retired"] = True
                    w["retired_at"] = _iso_z()
                    workers[from_worker] = w
                    run["workers"] = workers

        write_event(
            paths,
            event_type="merge.done",
            run=run,
            summary=f"Merge done item={item_id} result={result}",
            refs={
                "merge_item_id": item_id,
                "ticket_id": str(item.get("ticket_id") or ""),
                "branch": str(item.get("branch") or ""),
                "from_worker": str(item.get("from_worker") or ""),
            },
            data={"result": result, "note": note},
        )

    # Best-effort: if this unblocks completion, remind manager to disband.
    best_effort(
        lambda: _maybe_queue_disband_reminder(paths, notify=True, nudge=True),
        label="done_reminder.after_merge_done",
    )

    return MergeDoneResult(team=paths.team, item=dict(item))


def ship(
    *,
    team: str,
    force_clean: bool = False,
    push: Optional[bool] = None,
    repo: Optional[Path] = None,
) -> ShipResult:
    """Ship merge-queue branch into the target branch.

    Nothing is shipped until the manager runs this.
    """

    _require_role(action="loom team ship", allowed_roles={ROLE_MANAGER})

    _require_bin("git")

    paths = _paths_for(team=team, repo=repo)
    force_clean = bool(force_clean)

    push_override = push

    with locked_run(paths) as run:
        root = run_root(paths, run)

        # Resolve the canonical (repo-root) ticket directory and persist it.
        tickets_dir = ensure_run_tickets_dir(run, repo_root=root)

        ms = _merge_state(run)
        cfg = dict(ms.get("config") or {})
        target_branch = str(cfg.get("target_branch") or "main")
        remote = str(cfg.get("remote") or "origin")
        push_enabled = bool(cfg.get("push"))
        if push_override is not None:
            push_enabled = bool(push_override)

        merge_branch = merge_branch_for_run(run)

        write_event(
            paths,
            event_type="ship.attempted",
            run=run,
            summary=f"Ship attempted base={target_branch} topic={merge_branch}",
            refs={"target_branch": target_branch, "merge_branch": merge_branch},
            data={"force_clean": bool(force_clean), "push": bool(push_enabled)},
        )

        # Auto-sync/commit ticket changes so ship isn't blocked by `.loom/ticket`.
        _ensure_tickets_synced(cwd=root, tickets_dir=tickets_dir)

        # Auto-sync/commit compound learning changes so ship isn't blocked by skills/docs drift.
        _ensure_compound_synced(cwd=root)

        res = repo_merge_attempt(
            worktree=str(root),
            base=target_branch,
            topic=merge_branch,
            force_clean=force_clean,
            root=root,
        )
        res_dict = res.to_dict()
        merged = bool(res.merged)

        shipped_ids: List[str] = []
        shipped_at = _iso_z() if merged else ""
        if merged:
            items = [i for i in (ms.get("items") or []) if isinstance(i, dict)]
            for it in items:
                if str(it.get("state") or "") != "done":
                    continue
                if str(it.get("result") or "") != "merged":
                    continue
                if str(it.get("shipped_at") or "").strip():
                    continue
                it["shipped_at"] = shipped_at
                it["shipped_to"] = target_branch
                shipped_ids.append(str(it.get("id") or ""))
            ms["items"] = items
            run["merge"] = ms

    # Best-effort push after leaving the lock.
    push_ok = False
    push_err = ""
    if merged and push_enabled:
        try:
            _run(["git", "push", remote, target_branch], cwd=root, timeout=120.0)
            push_ok = True
        except Exception as e:
            push_err = str(e)

    # Timeline event (don’t rely on inbox messages alone).
    safe_write_event(
        paths,
        event_type="ship.finished",
        run=run,
        ok=bool(merged),
        summary=f"Ship finished merged={merged} shipped_items={len(shipped_ids)}",
        refs={"target_branch": target_branch, "merge_branch": merge_branch},
        data={
            "merged": bool(merged),
            "shipped_at": shipped_at,
            "shipped_ids": shipped_ids,
            "push": bool(push_enabled),
            "push_ok": bool(push_ok),
            "push_error": push_err,
            "ws": res_dict,
        },
    )

    # Durable manager notification.
    try:
        _inbox_write_and_maybe_nudge(
            paths=paths,
            run=run,
            target="manager",
            message=(
                f"SHIP {('OK' if merged else 'NOOP/BLOCKED')} base={target_branch} topic={merge_branch} "
                f"shipped_items={len(shipped_ids)} push={push_enabled} push_ok={push_ok}"
                + (f" push_error={push_err}" if push_err else "")
            ),
            sender="team",
            kind="ship",
            meta_extra={
                "merged": merged,
                "target_branch": target_branch,
                "merge_branch": merge_branch,
                "shipped_at": shipped_at,
                "shipped_ids": shipped_ids,
                "push": push_enabled,
                "push_ok": push_ok,
                "push_error": push_err,
            },
            nudge=True,
            force=False,
            line_info="ship",
        )
    except Exception:
        pass

    if merged and push_enabled and not push_ok:
        raise TeamError(
            "Ship merged locally, but push failed",
            code="PUSH",
            exit_code=1,
            suggestions=[
                f"git push {remote} {target_branch}",
                f"loom team ship {paths.team} --no-push",
            ],
            data={
                "remote": remote,
                "target_branch": target_branch,
                "error": push_err,
                "merge_branch": merge_branch,
            },
        )

    # Best-effort: shipping often completes the run.
    best_effort(
        lambda: _maybe_queue_disband_reminder(paths, notify=True, nudge=True),
        label="done_reminder.after_ship",
    )

    return ShipResult(
        team=paths.team,
        merged=bool(merged),
        target_branch=target_branch,
        merge_branch=merge_branch,
        shipped_at=shipped_at,
        shipped_ids=list(shipped_ids),
        ws=dict(res_dict),
        push={"enabled": push_enabled, "ok": push_ok, "error": push_err},
    )


def retire(
    *,
    team: str,
    worker_id: str,
    repo: Optional[Path] = None,
) -> RetireResult:
    _require_bin("tmux")
    _require_self_worker_id(action="loom team retire", requested_worker_id=worker_id)

    paths = _paths_for(team=team, repo=repo)

    with locked_run(paths) as run:
        session = run_session(run)

        wid = str(worker_id).strip()
        workers = dict(run.get("workers") or {})
        w = workers.get(wid)
        if not isinstance(w, dict):
            raise TeamError(f"Unknown worker_id: {wid}", code="ARG", exit_code=2)

        window = str(w.get("window") or "").strip()
        worktree = (
            Path(str(w.get("worktree") or "")).expanduser()
            if w.get("worktree")
            else None
        )

        if tmux_has_session(session) and window:
            tmux_kill_window(session, window)

        # Mark retired in state.
        w2 = dict(w)
        w2["retired_at"] = _iso_z()
        w2["retired"] = True
        workers[wid] = w2
        run["workers"] = workers

        write_event(
            paths,
            event_type="worker.retired",
            run=run,
            summary=f"Retired worker {wid}",
            refs={
                "worker_id": wid,
                "ticket_id": str(w.get("ticket_id") or ""),
                "window": window,
                "pane_id": str(w.get("pane_id") or ""),
                "worktree": str(worktree.resolve() if worktree else ""),
            },
            data={"worktree_preserved": True},
        )

    # Best-effort: if this was the last active work, remind manager to disband.
    best_effort(
        lambda: _maybe_queue_disband_reminder(paths, notify=True, nudge=True),
        label="done_reminder.after_retire",
    )

    return RetireResult(team=paths.team, worker_id=wid, retired=True)


def mark_retirable(
    *,
    team: str,
    worker_id: str,
    repo: Optional[Path] = None,
) -> MarkRetirableResult:
    """Mark a retired worker's worktree as eligible for janitor deletion."""

    _require_role(action="loom team mark-retirable", allowed_roles={ROLE_MANAGER})
    paths = _paths_for(team=team, repo=repo)
    wid = str(worker_id).strip()
    if not wid:
        raise TeamError("worker_id required", code="ARG", exit_code=2)

    with locked_run(paths) as run:
        workers = dict(run.get("workers") or {})
        w = workers.get(wid)
        if not isinstance(w, dict):
            raise TeamError(f"Unknown worker_id: {wid}", code="ARG", exit_code=2)
        if not bool(w.get("retired")):
            raise TeamError(
                f"Refusing to mark non-retired worker retirable: {wid}",
                code="ARG",
                exit_code=2,
            )

        w2 = dict(w)
        w2["worktree_retirable"] = True
        w2["worktree_retirable_at"] = _iso_z()
        workers[wid] = w2
        run["workers"] = workers

        write_event(
            paths,
            event_type="worktree.marked_retirable",
            run=run,
            summary=f"Worktree marked retirable worker={wid}",
            refs={
                "worker_id": wid,
                "ticket_id": str(w.get("ticket_id") or ""),
                "worktree": str(w.get("worktree") or ""),
            },
        )

    return MarkRetirableResult(team=paths.team, worker_id=wid, marked=True)


def bounce(
    *,
    team: str,
    target: str,
    reason: str = "",
    repo: Optional[Path] = None,
) -> BounceResult:
    """Force-restart a worker's agent process via its sidecar.

    Bounce is a durable control message delivered via the run inbox.
    The worker pane's sidecar (loom team tui) receives the message, SIGKILLs
    the child agent process, and then respawns it.
    """

    _require_bin("tmux")
    _require_role(action="loom team bounce", allowed_roles={ROLE_MANAGER})

    paths = _paths_for(team=team, repo=repo)
    run = load_run(paths)

    session = str(run.get("session") or "")
    if not tmux_has_session(session):
        raise TeamError(f"tmux session not found: {session}", code="TMUX", exit_code=2)

    pane_id, meta = _resolve_target(run, str(target or ""))
    if str(meta.get("role") or "").strip().lower() == ROLE_MANAGER:
        raise TeamError("Refusing to bounce manager", code="ARG", exit_code=2)

    worker_id = str(meta.get("worker_id") or "").strip()
    if not worker_id:
        raise TeamError(f"Target is not a worker: {target}", code="ARG", exit_code=2)

    workers = dict(run.get("workers") or {})
    w = workers.get(worker_id)
    if not isinstance(w, dict):
        raise TeamError(f"Unknown worker_id: {worker_id}", code="ARG", exit_code=2)
    if bool(w.get("retired")):
        raise TeamError(
            f"Refusing to bounce retired worker: {worker_id}",
            code="ARG",
            exit_code=2,
        )

    panes = tmux_list_panes(session)
    pane = panes.get(pane_id)
    if not pane:
        raise TeamError(
            f"pane not found for worker {worker_id}: {pane_id}",
            code="TMUX",
            exit_code=2,
        )
    if not _pane_can_receive_chat(pane):
        role = str(w.get("role") or "")
        if role == ROLE_INTEGRATOR:
            raise TeamError(
                f"integrator pane is not alive/interactive: {worker_id}. Run: loom team spawn-integrator {paths.team} --force",
                code="DEAD_PANE",
                exit_code=2,
            )
        raise TeamError(
            f"worker pane is not alive/interactive: {worker_id}. Run: loom team retire {paths.team} {worker_id} && loom team resume-worker {paths.team} {worker_id}",
            code="DEAD_PANE",
            exit_code=2,
        )

    run_id = str(run.get("run_id") or "")
    reason = str(reason or "").strip()
    sprint0 = run.get("sprint")
    sprint = dict(sprint0) if isinstance(sprint0, dict) else {}
    inbox_msg = inbox_write_message(
        paths,
        to=worker_id,
        sender="team",
        kind=INBOX_KIND_CONTROL,
        message=CONTROL_OP_BOUNCE,
        meta={
            "op": CONTROL_OP_BOUNCE,
            "reason": reason,
            "requested_by": str(os.getenv("USER") or ""),
            "run_id": run_id,
            "sprint": sprint,
            "worker_id": worker_id,
            "pane_id": pane_id,
            "target": str(target or ""),
        },
    )
    tmux_signal(channel_for(run_id=run_id, to=worker_id))

    safe_write_event(
        paths,
        event_type="worker.bounce_requested",
        run=run,
        summary=f"Bounce requested worker={worker_id}",
        refs={
            "worker_id": worker_id,
            "pane_id": pane_id,
            "inbox_id": str(inbox_msg.get("id") or ""),
        },
        data={"reason": reason, "target": str(target or "")},
    )

    return BounceResult(
        team=str(run.get("team") or paths.team),
        worker_id=worker_id,
        inbox_id=str(inbox_msg.get("id") or ""),
    )
