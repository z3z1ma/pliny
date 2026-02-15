"""Team lifecycle command handlers."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from agent_loom.team.constants import (
    DEFAULT_INTEGRATOR_AGENT,
    DEFAULT_INVESTIGATOR_AGENT,
    DEFAULT_MANAGER_AGENT,
    DEFAULT_WORKER_AGENT,
    ENV_TICKET_DIR,
    SUBSYSTEM_NAME,
)
from agent_loom.team.core import (
    attach,
    disband,
    doctor,
    done,
    init_agents,
    janitor,
    pause_team,
    resume_team,
    start,
    status,
)
from agent_loom.team.exec import _require_bin, _run
from agent_loom.team.prime import prime


def _maybe_worktree_root(invoked_from: Path) -> Path | None:
    try:
        _require_bin("git")
        p = _run(["git", "rev-parse", "--show-toplevel"], cwd=invoked_from, timeout=5.0)
        return Path((p.stdout or "").strip()).resolve() if p.stdout else None
    except Exception:
        return None


def emit_json_result(result: object) -> None:
    from agent_loom.core.cli_output import emit_json, make_ok_envelope, normalize_payload

    emit_json(make_ok_envelope(normalize_payload(result)), indent=2)


def cmd_start(args: argparse.Namespace) -> None:
    repo = Path(args.repo).resolve() if args.repo else None
    mounts = getattr(args, "mount", None)
    res = start(
        team=args.team,
        objective=args.objective,
        session=args.session,
        harness=args.harness,
        bin_override=args.bin,
        model=args.model,
        manager_model=str(getattr(args, "manager_model", "") or ""),
        investigator_model=str(getattr(args, "investigator_model", "") or ""),
        worker_model=str(getattr(args, "worker_model", "") or ""),
        integrator_model=str(getattr(args, "integrator_model", "") or ""),
        mounts=(list(mounts) if mounts is not None else None),
        clear_mounts=bool(getattr(args, "clear_mounts", False)),
        target_branch=str(getattr(args, "target_branch", "") or ""),
        remote=str(getattr(args, "remote", "") or ""),
        push=getattr(args, "push", None),
        max_headcount=getattr(args, "max_headcount", None),
        manager_window=args.manager_window,
        force=bool(args.force),
        repo=repo,
    )
    if args.json:
        emit_json_result(res)
        return

    invoked_from = repo if repo else Path.cwd().resolve()
    worktree_root = _maybe_worktree_root(invoked_from)

    print(f"{SUBSYSTEM_NAME} started")
    print(f"- team: {res.team}")
    print(f"- tmux session: {res.session}")
    print(f"- repo_root: {res.repo_root}")
    if worktree_root and worktree_root != Path(res.repo_root).resolve():
        print(f"- note: invoked from git worktree {worktree_root}")
    print(f"- run_dir: {res.run_dir}")
    print(f"- tickets_dir: {res.tickets_dir} ({ENV_TICKET_DIR})")
    print(f"- charter: {res.charter}")
    if isinstance(res.manager, dict) and res.manager.get("merge_target"):
        print(f"- merge_target: {res.manager.get('merge_target')}")
    print("")
    print(f"Next: {SUBSYSTEM_NAME} attach {res.team}")


def cmd_init(args: argparse.Namespace) -> None:
    repo = Path(args.repo).resolve() if args.repo else None
    res = init_agents(repo=repo, create_missing=True, force=bool(args.force))
    if args.json:
        emit_json_result(res)
        return

    print(f"{SUBSYSTEM_NAME} init")
    print(f"- repo_root: {res.repo_root}")
    print("- pack: loom-team-core")
    print("- note: commit .loom/pack/lock.json")
    if res.wrote:
        print(f"- wrote: {len(res.wrote)}")
    if res.updated:
        print(f"- updated: {len(res.updated)}")
    if res.skipped:
        print(f"- skipped: {len(res.skipped)}")
    if res.warnings:
        print("warnings:")
        for w in res.warnings:
            print(f"- {w}")

    from agent_loom.pack.diff import any_pack_diffs, diff_pack_files

    repo_root = Path(res.repo_root).resolve()
    pack_id = "loom-team-core"
    rels = [
        f".opencode/agents/{DEFAULT_MANAGER_AGENT}.md",
        f".opencode/agents/{DEFAULT_WORKER_AGENT}.md",
        f".opencode/agents/{DEFAULT_INVESTIGATOR_AGENT}.md",
        f".opencode/agents/{DEFAULT_INTEGRATOR_AGENT}.md",
        f".claude/agents/{DEFAULT_MANAGER_AGENT}.md",
        f".claude/agents/{DEFAULT_WORKER_AGENT}.md",
        f".claude/agents/{DEFAULT_INVESTIGATOR_AGENT}.md",
        f".claude/agents/{DEFAULT_INTEGRATOR_AGENT}.md",
    ]

    if not bool(getattr(args, "diff", False)) and any_pack_diffs(
        repo_root=repo_root, pack_id=pack_id, relpaths=rels
    ):
        print("note: some Team agent files differ; rerun with --diff to view")

    if bool(getattr(args, "diff", False)):
        diffs = diff_pack_files(
            repo_root=repo_root,
            pack_id=pack_id,
            relpaths=rels,
            max_lines=400,
        )
        for d in diffs:
            print(f"diff (skipped): {d.relpath}")
            sys.stdout.write(d.diff)


def cmd_attach(args: argparse.Namespace) -> None:
    res = attach(team=args.team)
    os.execvp("tmux", ["tmux", "attach-session", "-t", res.session])


def cmd_status(args: argparse.Namespace) -> None:
    res = status(team=args.team, repo=Path(args.repo).resolve() if args.repo else None)
    if args.json:
        emit_json_result(res)
        return

    print(f"team: {res.team}  session: {res.session}")
    print(f"run_id: {res.run_id}")
    if res.repo_root:
        print(f"repo_root: {res.repo_root}")
    if res.run_dir:
        print(f"run_dir: {res.run_dir}")
    if res.tickets_dir:
        print(f"tickets_dir: {res.tickets_dir} ({ENV_TICKET_DIR})")
    if res.sprint and res.sprint.get("name"):
        print(f"sprint: {res.sprint.get('name')} tag={res.sprint.get('tag')}")
    print(
        f"inbox: unacked_to_manager={res.inbox.get('unacked_to_manager', 0)} unacked_total={res.inbox.get('unacked_total', 0)}"
    )
    print(
        f"merge_queue: pending={res.merge_queue.get('pending', 0)} queued={res.merge_queue.get('queued', 0)} claimed={res.merge_queue.get('claimed', 0)}"
    )
    mt_remote = str(res.merge_queue.get("remote") or "")
    mt_branch = str(res.merge_queue.get("target_branch") or "")
    if mt_remote and mt_branch:
        print(
            f"merge_target: {mt_remote}/{mt_branch} push={bool(res.merge_queue.get('push'))} merge_branch={res.merge_queue.get('merge_branch', '')}"
        )
    print(
        f"manager: pane={res.manager.get('pane_id', '')} window={res.manager.get('window', '')}"
    )

    active_workers = {
        wid: w for wid, w in res.workers.items() if not bool((w or {}).get("retired"))
    }
    alive_workers = {
        wid: w for wid, w in active_workers.items() if bool((w or {}).get("alive"))
    }
    dead_workers = {
        wid: w for wid, w in active_workers.items() if not bool((w or {}).get("alive"))
    }

    print(
        f"workers: alive={len(alive_workers)} total={len(active_workers)} dead_or_unsafe={len(dead_workers)}"
    )
    for wid, w in alive_workers.items():
        t = str((w or {}).get("ticket_id") or "")
        role = str((w or {}).get("role") or "")
        print(
            f"- {wid} ({role}) {t} [alive] window={(w or {}).get('window')} pane={(w or {}).get('pane_id')}"
        )
    if dead_workers and not bool(getattr(args, "show_dead", False)):
        print(
            f"dead/unsafe workers hidden (use: loom team status {res.team} --show-dead)"
        )
    if bool(getattr(args, "show_dead", False)):
        for wid, w in dead_workers.items():
            t = str((w or {}).get("ticket_id") or "")
            role = str((w or {}).get("role") or "")
            print(
                f"- {wid} ({role}) {t} [dead/unsafe] window={(w or {}).get('window')} pane={(w or {}).get('pane_id')}"
            )

    if res.warnings:
        print("warnings:")
        for w in res.warnings:
            print(f"- {w.get('code')}: {w.get('message')}")


def cmd_doctor(args: argparse.Namespace) -> None:
    res = doctor(team=args.team, repo=Path(args.repo).resolve() if args.repo else None)
    if args.json:
        emit_json_result(res)
        return
    if not res.issues:
        print("ok")
        return
    print(f"issues: {len(res.issues)}")
    for it in res.issues:
        code = str((it or {}).get("code") or "")
        msg = str((it or {}).get("message") or "")
        print(f"- {code}: {msg}")
    if res.suggestions:
        print("next:")
        for s in res.suggestions:
            print(f"- {s}")


def cmd_disband(args: argparse.Namespace) -> None:
    res = disband(
        team=args.team,
        keep_worktrees=not bool(getattr(args, "remove_worktrees", False)),
        keep_state=bool(getattr(args, "keep_state", False)),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print(f"disbanded {res.team} ({res.session})")


def cmd_done(args: argparse.Namespace) -> None:
    from agent_loom.team.constants import DEFAULT_DISBAND_REMINDER_RESEND_S

    res = done(
        team=args.team,
        notify=bool(getattr(args, "notify", False)),
        resend_after_s=float(
            getattr(args, "resend_after_s", DEFAULT_DISBAND_REMINDER_RESEND_S)
        ),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print("done" if res.done else "not_done")


def cmd_janitor(args: argparse.Namespace) -> None:
    res = janitor(
        team=args.team,
        older_than=str(getattr(args, "older_than", "7d") or "7d"),
        dry_run=bool(getattr(args, "dry_run", False)),
        keep_worktrees=bool(getattr(args, "keep_worktrees", False)),
        prune_orphans=bool(getattr(args, "prune_orphans", False)),
        keep_retired_workers=bool(getattr(args, "keep_retired_workers", False)),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print("ok")


def cmd_pause(args: argparse.Namespace) -> None:
    res = pause_team(
        team=args.team,
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print(f"paused {res.team} ({res.session})")


def cmd_resume(args: argparse.Namespace) -> None:
    res = resume_team(
        team=args.team,
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print(f"resumed {res.team} ({res.session})")
    print(f"- workers_respawned: {len(res.resumed_workers)}")
    if res.skipped_workers:
        print(f"- workers_skipped: {len(res.skipped_workers)}")
    if res.integrator:
        ok = bool(res.integrator.get("respawned") or res.integrator.get("worker"))
        print(f"- integrator: {'ok' if ok else 'skipped'}")


def cmd_prime(args: argparse.Namespace) -> None:
    res = prime()
    if args.json:
        emit_json_result(res)
        return
    text = str(getattr(res, "markdown", "") or "")
    if text:
        sys.stdout.write(text.rstrip() + "\n")
