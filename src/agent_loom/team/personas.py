from __future__ import annotations

from pathlib import Path
from typing import Optional

from agent_loom.team.composition_runtime import resolve_member_profile
from agent_loom.team.constants import (
    ENV_TEAM_NAME,
    ENV_TEAM_ROLE,
    ENV_TEAM_RUN_DIR,
    ENV_TEAM_RUN_ID,
    ENV_TEAM_SPRINT_NAME,
    ENV_TEAM_SPRINT_TAG,
    ENV_TEAM_TICKET_ID,
    ENV_TEAM_WORKER_ID,
    ENV_TICKET_DIR,
    ROLE_ARCHITECT,
    ROLE_INTEGRATOR,
    ROLE_MANAGER,
    ROLE_WORKER,
)
from agent_loom.team.errors import TeamError
from agent_loom.team.exec import _require_bin
from agent_loom.team.models import SpawnPersonaResult
from agent_loom.team.objective_state import sprint_state
from agent_loom.team.permissions import _require_role
from agent_loom.team.prompts import render_persona_prompt
from agent_loom.team.run_state import locked_run, run_root, run_session
from agent_loom.team.strings import sanitize
from agent_loom.team.time import _iso_z
from agent_loom.team.tmux import (
    tmux_cmd,
    tmux_env_flags,
    tmux_format,
    tmux_has_session,
    tmux_mark_pane,
    tmux_unique_window_name,
    tmux_window_exists,
)


def spawn_persona(
    *,
    team: str,
    member_id: str,
    repo: Optional[Path] = None,
    force: bool = False,
) -> SpawnPersonaResult:
    from agent_loom.team.core import (
        _agent_for_role,
        _apply_mounts,
        _ensure_opencode_worktree_runtime,
        _ensure_worktree,
        _is_path_within,
        _model_for_role,
        _normalize_harness,
        _paths_for,
        _persona_worktree_branch,
        _require_agent_file_present,
        _team_tui_argv,
        _workspace_for_always_on_profile,
        ensure_run_tickets_dir,
    )

    _require_bin("tmux")
    _require_role(action="loom team spawn-persona", allowed_roles={ROLE_MANAGER})

    requested_member_id = str(member_id or "").strip()
    if not requested_member_id:
        raise TeamError("Missing member_id", code="ARG", exit_code=2)
    if requested_member_id in {
        ROLE_MANAGER,
        ROLE_WORKER,
        ROLE_ARCHITECT,
        ROLE_INTEGRATOR,
    }:
        raise TeamError(
            f"Cannot spawn built-in role via spawn-persona: {requested_member_id}",
            code="ARG",
            exit_code=2,
        )

    paths = _paths_for(team=team, repo=repo)

    with locked_run(paths) as run:
        session = run_session(run)
        if not tmux_has_session(session):
            raise TeamError(
                f"tmux session not found: {session} (run {paths.team}). Start it with: loom team start ...",
                code="TMUX",
                exit_code=2,
            )

        root = run_root(paths, run)
        tickets_dir = ensure_run_tickets_dir(run, repo_root=root)
        sprint = sprint_state(run)
        defaults = run.get("defaults") if isinstance(run.get("defaults"), dict) else {}
        base_ref_default = str((defaults or {}).get("base_ref") or "").strip() or None

        harness_default = _normalize_harness(str(run.get("harness") or ""))
        raw_mounts = run.get("mounts")
        mounts: list[dict] = []
        if isinstance(raw_mounts, list):
            mounts = [dict(item) for item in raw_mounts if isinstance(item, dict)]

        profile = resolve_member_profile(
            run,
            role="",
            member_id=requested_member_id,
        )
        if profile is None:
            raise TeamError(
                f"Roster member not found: {requested_member_id}",
                code="ARG",
                exit_code=2,
            )

        role = str(profile.role or "").strip().lower()
        if role in {ROLE_MANAGER, ROLE_WORKER, ROLE_ARCHITECT, ROLE_INTEGRATOR}:
            raise TeamError(
                f"spawn-persona only supports custom roles; member_id={requested_member_id} role={role}",
                code="ARG",
                exit_code=2,
            )

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
                    member_id=requested_member_id,
                ),
                base_ref=base_ref_default,
                allow_dirty=True,
            )
            project_dir = Path(str(wt.get("path") or desired_wt_path)).resolve()
            branch = str(wt.get("branch") or "").strip()
            base = str(wt.get("base") or "").strip()
            _apply_mounts(repo_root=root, worktree_root=project_dir, mounts=mounts)
            if persona_harness == "opencode":
                _ensure_opencode_worktree_runtime(workdir=project_dir, repo_root=root)

        _require_agent_file_present(
            workdir=project_dir,
            harness=persona_harness,
            agent=agent,
        )

        model = _model_for_role(run, role, harness=persona_harness)
        if not model and profile.model:
            model = str(profile.model)

        prompt = render_persona_prompt(
            run=run,
            role=role,
            worker_id=requested_member_id,
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
            ENV_TEAM_WORKER_ID: requested_member_id,
            ENV_TEAM_TICKET_ID: "",
            ENV_TEAM_SPRINT_NAME: sprint.get("name", ""),
            ENV_TEAM_SPRINT_TAG: sprint.get("tag", ""),
            "COMPOUND_ROOT": str(root),
        }

        workers = dict(run.get("workers") or {})
        existing = dict(workers.get(requested_member_id) or {})
        existing_window = str(existing.get("window") or "").strip()

        if force and existing_window and tmux_window_exists(session, existing_window):
            tmux_cmd(["kill-window", "-t", f"{session}:{existing_window}"], check=False)
            existing_window = ""

        pane_id = ""
        window = existing_window

        if (
            window
            and not bool(existing.get("retired"))
            and tmux_window_exists(session, window)
        ):
            pane_id = tmux_format(f"{session}:{window}", "#{pane_id}")
            workers[requested_member_id] = {
                **existing,
                "pane_id": pane_id,
                "retired": False,
            }
            run["workers"] = workers
            return SpawnPersonaResult(
                team=str(run.get("team") or paths.team),
                member_id=requested_member_id,
                role=role,
                window=window,
                pane_id=pane_id,
                workspace=workspace,
                worktree=str(project_dir),
                worktree_key=worktree_key,
                respawned=False,
                worker=dict(workers.get(requested_member_id) or {}),
            )

        desired_window = (
            sanitize(
                existing_window or requested_member_id,
                allow=r"a-zA-Z0-9._-",
                max_len=60,
            )
            or requested_member_id
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
                worker_id=requested_member_id,
                ticket_id="",
            )

        now_iso = _iso_z()
        workers[requested_member_id] = {
            **existing,
            "worker_id": requested_member_id,
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

        return SpawnPersonaResult(
            team=str(run.get("team") or paths.team),
            member_id=requested_member_id,
            role=role,
            window=window,
            pane_id=pane_id,
            workspace=workspace,
            worktree=str(project_dir),
            worktree_key=worktree_key,
            respawned=True,
            worker=dict(workers.get(requested_member_id) or {}),
        )


__all__ = ["spawn_persona"]
