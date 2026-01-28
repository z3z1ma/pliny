from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any, Optional, Sequence

from agent_loom.workspace.constants import (
    REPO_INTERNAL_DIR,
)
from agent_loom.workspace.core import (
    add_repo,
    branch,
    context,
    deepen,
    deps_closure,
    deps_impacted,
    deps_show,
    deps_who_uses,
    lease_acquire,
    lease_list,
    lease_release,
    list_repos,
    poly_exec,
    poly_init,
    poly_repo_edit,
    poly_set_ls,
    poly_set_rm,
    poly_set_show,
    poly_set_upsert,
    prime,
    remove_repo,
    repo_init,
    repo_merge_attempt,
    repo_snapshot_capture,
    repo_snapshot_diff,
    repo_snapshot_restore,
    repo_status,
    repo_worktree_add,
    repo_worktree_check_clean,
    repo_worktree_check_divergence,
    repo_worktree_ensure,
    repo_worktree_ensure_detached,
    repo_worktree_ls,
    repo_worktree_prune,
    repo_worktree_rm,
    repo_worktree_rm_path,
    repo_worktree_status,
    services_refresh_index,
    snapshot,
    snapshot_diff,
    snapshot_restore,
    status,
    sync,
    worktree_add,
    worktree_group_check_clean,
    worktree_group_check_divergence,
    worktree_group_status,
    worktree_prune,
    worktree_ls,
    worktree_push,
    worktree_rebase,
    worktree_rm,
    worktree_gc,
)
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.guards import workspace_root
from agent_loom.workspace.cleanup_ops import (
    repo_worktree_cleanup_apply,
    repo_worktree_cleanup_suggest,
)
from agent_loom.workspace.sandbox_ops import (
    repo_sandbox_create,
    repo_sandbox_gc,
    repo_sandbox_promote,
)
from agent_loom.workspace.poly_sandbox_ops import (
    poly_sandbox_create,
    poly_sandbox_gc,
    poly_sandbox_promote,
)
from agent_loom.workspace.models import (
    AddRepoResult,
    BranchResult,
    ContextResult,
    DeepenResult,
    DepsShowResult,
    DepsWhoUsesResult,
    LeaseAcquireResult,
    LeaseListResult,
    LeaseReleaseResult,
    ListReposResult,
    MergeAttemptResult,
    PolyInitResult,
    PolyExecResult,
    PrimeResult,
    RemoveRepoResult,
    RepoInitResult,
    RepoStatusResult,
    RepoWorktreeAddResult,
    RepoWorktreeEnsureDetachedResult,
    RepoWorktreeListResult,
    RepoWorktreePruneResult,
    RepoWorktreeRemoveResult,
    ServicesRefreshIndexResult,
    SnapshotResult,
    SnapshotDiffResult,
    SnapshotRestoreResult,
    StatusResult,
    SyncResult,
    WorktreeAddResult,
    WorktreeGcResult,
    WorktreeEnsureResult,
    WorktreeGroupRemoveResult,
    WorktreeListResult,
    WorktreePushResult,
    WorktreeRebaseResult,
)
from agent_loom.workspace.repo_ops import repo_root
from agent_loom.workspace.utils import now_iso


def _cmd_name(args: argparse.Namespace) -> str:
    top = getattr(args, "cmd", "") or ""
    if top == "poly":
        cmd = getattr(args, "poly_cmd", "") or ""
        if cmd == "worktree":
            cmd = f"worktree {getattr(args, 'worktree_cmd', '')}".strip()
        elif cmd == "snapshot":
            cmd = f"snapshot {getattr(args, 'snapshot_cmd', '')}".strip()
        elif cmd == "repo":
            cmd = f"repo {getattr(args, 'repo_cmd', '')}".strip()
        elif cmd == "set":
            cmd = f"set {getattr(args, 'set_cmd', '')}".strip()
        elif cmd == "lease":
            cmd = f"lease {getattr(args, 'lease_cmd', '')}".strip()
        elif cmd == "services":
            cmd = f"services {getattr(args, 'services_cmd', '')}".strip()
        elif cmd == "deps":
            cmd = f"deps {getattr(args, 'deps_cmd', '')}".strip()
        elif cmd == "sandbox":
            cmd = f"sandbox {getattr(args, 'sandbox_cmd', '')}".strip()
        return f"poly {cmd}".strip()

    cmd = top
    if cmd == "worktree":
        cmd = f"worktree {getattr(args, 'worktree_cmd', '')}".strip()
    elif cmd == "snapshot":
        cmd = f"snapshot {getattr(args, 'snapshot_cmd', '')}".strip()
    elif cmd == "cleanup":
        cmd = f"cleanup {getattr(args, 'cleanup_cmd', '')}".strip()
    elif cmd == "sandbox":
        cmd = f"sandbox {getattr(args, 'sandbox_cmd', '')}".strip()
    elif cmd == "merge":
        cmd = f"merge {getattr(args, 'merge_cmd', '')}".strip()
    return cmd


def _emit_json(obj: dict) -> None:
    sys.stdout.write(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def _payload(obj: Any) -> Any:
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    return obj


def emit_ok(args: argparse.Namespace, root: Path, data: Any = None) -> None:
    _emit_json(
        {
            "ok": True,
            "cmd": _cmd_name(args),
            "root": str(root.resolve()),
            "data": _payload(data),
            "meta": {"generated_at": now_iso()},
        }
    )


def emit_error(
    args: argparse.Namespace, root: Optional[Path], err: BaseException
) -> None:
    _emit_json(
        {
            "ok": False,
            "cmd": _cmd_name(args),
            "root": str(root.resolve()) if root else None,
            "error": {"type": type(err).__name__, "message": str(err)},
            "meta": {"generated_at": now_iso()},
        }
    )


def _render_prime_text(payload: dict[str, Any]) -> str:
    md: list[str] = []
    md.append(f"# loom workspace (v{payload['tool']['version']})")
    md.append("")
    md.append("Run `loom workspace -h` for help.")
    md.append("Run `loom workspace <command> -h` for command-specific help.")
    md.append("Run `loom workspace poly -h` for poly workspace help.")
    md.append("")

    md.append("## Purpose")
    md.append(f"- {payload['purpose']}")
    md.append("")

    md.append("## Zen")
    md.extend([f"- {x}" for x in payload["zen"]])
    md.append("")

    md.append("## Storage")
    md.append("- poly control plane")
    md.append(
        f"  - root markers: `{', '.join(payload['storage']['poly_control_plane']['root_markers'])}`"
    )
    md.append(
        f"  - internal dir: `{payload['storage']['poly_control_plane']['internal_dir']}/`"
    )
    md.append(
        f"  - repos/worktrees defaults: `{payload['storage']['poly_control_plane']['repos_dir_default']}/`, `{payload['storage']['poly_control_plane']['worktrees_dir_default']}/`"
    )
    md.append("- repo mode")
    md.append(f"  - internal dir: `{payload['storage']['repo_mode']['internal_dir']}/`")
    md.append(f"  - ignore: {payload['storage']['repo_mode']['git_exclude']}")
    md.append("")

    md.append("## Dispatch")
    md.append("- explicit:")
    md.extend([f"  - {x}" for x in payload["dispatch"]["explicit"]])
    md.append("")

    md.append("## Output")
    md.append(f"- default: {payload['output']['default']}")
    md.append(f"- json: {payload['output']['json']}")
    md.append("")

    md.append("## Safety")
    md.append(f"- {payload['safety']['worktree_rm']}")
    md.append(f"- {payload['safety']['merge_force_clean']}")
    md.append(f"- {payload['safety']['poly_guardrails']}")
    md.append("")

    md.append("## Copy/paste")
    md.extend(payload["examples"]["copy_paste_for_agents_md"])
    md.append("")

    md.append("## Canonical examples")
    for section, cmds in payload["examples"].items():
        if section == "copy_paste_for_agents_md":
            continue
        md.append(f"### {section}")
        md.extend([f"- `{c}`" for c in cmds])
        md.append("")

    md.append("tip: run `loom workspace -h` or `loom workspace poly -h`.")
    md.append("")

    return "\n".join(md).rstrip() + "\n"


def _render_services_index_text(index: dict[str, Any]) -> str:
    services = index.get("services", {}) if isinstance(index, dict) else {}
    lines = [f"Services ({len(services)})"]
    for name in sorted(services.keys()):
        entry = services.get(name) or {}
        deps = ", ".join(entry.get("depends_on", []) or []) or "-"
        ext = ", ".join(entry.get("depends_on_external", []) or []) or "-"
        used_by = ", ".join(entry.get("used_by", []) or []) or "-"
        lines.append(f"- {name} deps: {deps} external: {ext} used_by: {used_by}")
    return "\n".join(lines).rstrip() + "\n"


def _bool(value: bool) -> str:
    return "yes" if value else "no"


def _render_text(result: Any) -> str:
    if isinstance(result, RepoStatusResult):
        return (
            "\n".join(
                [
                    f"repo: {result.repo_root}",
                    f"branch: {result.branch}",
                    f"commit: {result.commit}",
                    f"dirty: {_bool(result.dirty)}",
                    f"default_branch: {result.default_branch}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, RepoWorktreeAddResult):
        return (
            "\n".join(
                [
                    f"branch: {result.branch}",
                    f"path: {result.path}",
                    f"existed: {_bool(result.existed)}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, WorktreeEnsureResult):
        return (
            "\n".join(
                [
                    f"branch: {result.branch}",
                    f"path: {result.path}",
                    f"existed: {_bool(result.existed)}",
                    f"reused: {_bool(result.reused)}",
                    f"base_ref: {result.base_ref}",
                    f"base_branch: {result.base_branch}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, RepoWorktreeRemoveResult):
        lines = [f"removed: {result.removed}"]
        if result.branch:
            lines.append(f"branch: {result.branch}")
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, RepoWorktreePruneResult):
        return f"pruned: {_bool(result.pruned)}\n"

    if isinstance(result, RepoWorktreeEnsureDetachedResult):
        return (
            "\n".join(
                [
                    f"path: {result.path}",
                    f"ref: {result.ref}",
                    f"commit: {result.commit}",
                    f"existed: {_bool(result.existed)}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, RepoWorktreeListResult):
        lines = ["worktrees:"]
        for row in result.worktrees:
            path = row.get("path", "")
            branch = row.get("branch") or "(detached)"
            head = row.get("head", "")
            flags: list[str] = []
            if row.get("detached"):
                flags.append("detached")
            if row.get("locked"):
                flags.append("locked")
            tail = f" ({', '.join(flags)})" if flags else ""
            lines.append(f"- {path} {branch} {head}{tail}".rstrip())
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, MergeAttemptResult):
        lines = [
            f"merged: {_bool(result.merged)}",
            f"worktree: {result.worktree}",
            f"base: {result.base}",
            f"base_commit: {result.base_commit}",
            f"topic: {result.topic}",
        ]
        if result.merge_commit:
            lines.append(f"merge_commit: {result.merge_commit}")
        if result.error:
            lines.append(f"error: {result.error}")
        if result.hint:
            lines.append(f"hint: {result.hint}")
        if result.stdout:
            lines.append(f"stdout: {result.stdout}")
        if result.stderr:
            lines.append(f"stderr: {result.stderr}")
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, PolyInitResult):
        return (
            "\n".join(
                [
                    f"workspace_file: {result.workspace_file}",
                    f"repos_dir: {result.repos_dir}",
                    f"worktrees_dir: {result.worktrees_dir}",
                    f"states_dir: {result.states_dir}",
                    f"services_dir: {result.services_dir}",
                    f"gitignore_path: {result.gitignore_path}",
                    f"updated_gitignore: {_bool(bool(result.updated_gitignore))}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, RepoInitResult):
        return (
            "\n".join(
                [
                    f"repo_root: {result.repo_root}",
                    f"internal_dir: {result.internal_dir}",
                    f"worktrees_dir: {result.worktrees_dir}",
                    f"git_exclude_path: {result.git_exclude_path}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, PolyExecResult):
        s = result.summary or {}
        return (
            "\n".join(
                [
                    f"repos: {s.get('repos')}",
                    f"success: {s.get('success')}",
                    f"fail: {s.get('fail')}",
                    f"skip: {s.get('skip')}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, LeaseAcquireResult):
        return (
            "\n".join(
                [
                    f"key: {result.key}",
                    f"lease_path: {result.lease_path}",
                    f"existed: {_bool(result.existed)}",
                    f"forced: {_bool(result.forced)}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, LeaseReleaseResult):
        return (
            "\n".join(
                [
                    f"key: {result.key}",
                    f"lease_path: {result.lease_path}",
                    f"released: {_bool(result.released)}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, LeaseListResult):
        return (
            "\n".join(
                [
                    f"leases_dir: {result.leases_dir}",
                    f"leases: {len(result.leases)}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, WorktreeGcResult):
        return (
            "\n".join(
                [
                    f"removed: {len(result.removed)}",
                    f"skipped: {len(result.skipped)}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, AddRepoResult):
        lines = [f"repo: {result.repo}", f"cloned: {_bool(result.cloned)}"]
        entry = result.entry or {}
        for key in ("remote", "default_branch", "shallow", "depth"):
            if key in entry:
                lines.append(f"{key}: {entry.get(key)}")
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, RemoveRepoResult):
        return (
            "\n".join(
                [
                    f"repo: {result.repo}",
                    f"deleted_clone: {_bool(result.deleted_clone)}",
                    f"deleted_service_md: {_bool(result.deleted_service_md)}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, ListReposResult):
        lines = [f"repos: {len(result.repos)}"]
        for row in result.repos:
            name = row.get("name")
            remote = row.get("remote")
            default_branch = row.get("default_branch")
            tags = ",".join(row.get("tags") or []) or "-"
            desc = row.get("description") or ""
            bits = [str(name), f"({default_branch})", str(remote), f"tags:{tags}"]
            if desc:
                bits.append(f"desc:{desc}")
            lines.append("- " + " ".join(bits))
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, SyncResult):
        lines = [f"repos: {len(result.results)}"]
        for row in result.results:
            name = row.get("repo")
            actions = ",".join(row.get("actions") or [])
            warnings = "; ".join(row.get("warnings") or [])
            parts = [f"- {name}"]
            if actions:
                parts.append(f"actions:{actions}")
            if warnings:
                parts.append(f"warnings:{warnings}")
            if row.get("error"):
                parts.append(f"error:{row.get('error')}")
            lines.append(" ".join(parts))
        if result.services_index is not None:
            lines.append("services_index: refreshed")
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, StatusResult):
        lines = [f"repos: {len(result.repos)}"]
        for row in result.repos:
            lines.append(
                f"- {row.get('repo')} {row.get('branch')} {row.get('sha')} {row.get('status')}"
            )
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, BranchResult):
        lines = [f"branch: {result.branch}"]
        for row in result.repos:
            lines.append(f"- {row.get('repo')} {row.get('branch')}")
        if result.services_index is not None:
            lines.append("services_index: refreshed")
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, WorktreeAddResult):
        lines = [f"group: {result.group}"]
        for row in result.worktrees:
            lines.append(
                f"- {row.get('repo')} {row.get('path')} existed:{_bool(bool(row.get('existed')))}"
            )
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, WorktreeGroupRemoveResult):
        lines = [f"group: {result.group}", f"removed: {len(result.removed)}"]
        for path in result.removed:
            lines.append(f"- {path}")
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, WorktreeListResult):
        lines = [f"worktrees: {len(result.worktrees)}"]
        for row in result.worktrees:
            lines.append(
                f"- {row.get('group')} {row.get('repo')} {row.get('branch')} {row.get('sha')} {row.get('status')}"
            )
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, WorktreeRebaseResult):
        lines = [f"group: {result.group}"]
        for row in result.results:
            parts = [f"- {row.get('repo')}", str(row.get("status"))]
            if row.get("onto"):
                parts.append(f"onto:{row.get('onto')}")
            if row.get("reason"):
                parts.append(f"reason:{row.get('reason')}")
            lines.append(" ".join(parts))
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, WorktreePushResult):
        lines = [f"group: {result.group}"]
        for row in result.results:
            parts = [f"- {row.get('repo')}", str(row.get("status"))]
            if row.get("reason"):
                parts.append(f"reason:{row.get('reason')}")
            if row.get("branch"):
                parts.append(f"branch:{row.get('branch')}")
            lines.append(" ".join(parts))
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, SnapshotResult):
        repo_count = len(result.snapshot.get("repos", {}))
        return (
            "\n".join(
                [
                    f"snapshot_path: {result.snapshot_path}",
                    f"repos: {repo_count}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, SnapshotDiffResult):
        s = result.summary or {}
        return (
            "\n".join(
                [
                    f"snapshot_path: {result.snapshot_path}",
                    f"repos: {s.get('repos')}",
                    f"match: {s.get('match')}",
                    f"changed: {s.get('changed')}",
                    f"missing: {s.get('missing')}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, SnapshotRestoreResult):
        s = result.summary or {}
        return (
            "\n".join(
                [
                    f"snapshot_path: {result.snapshot_path}",
                    f"repos: {s.get('repos')}",
                    f"success: {s.get('success')}",
                    f"skipped: {s.get('skipped')}",
                    f"failed: {s.get('failed')}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, ServicesRefreshIndexResult):
        services = (
            result.index.get("services", {}) if isinstance(result.index, dict) else {}
        )
        return (
            "\n".join(
                [
                    f"services_index_path: {result.services_index_path}",
                    f"services: {len(services)}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, DepsShowResult):
        data = result.data or {}
        deps = ", ".join(data.get("depends_on", []) or []) or "-"
        ext = ", ".join(data.get("depends_on_external", []) or []) or "-"
        used_by = ", ".join(data.get("used_by", []) or []) or "-"
        return (
            "\n".join(
                [
                    f"service: {result.service}",
                    f"depends_on: {deps}",
                    f"depends_on_external: {ext}",
                    f"used_by: {used_by}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, DepsWhoUsesResult):
        used_by = ", ".join(result.used_by or []) or "-"
        return (
            "\n".join(
                [
                    f"service: {result.service}",
                    f"used_by: {used_by}",
                ]
            ).rstrip()
            + "\n"
        )

    if isinstance(result, DeepenResult):
        lines = [f"repo: {result.repo}"]
        if result.skipped:
            lines.append("skipped: yes")
            if result.reason:
                lines.append(f"reason: {result.reason}")
        else:
            lines.append(f"depth: {result.depth}")
        return "\n".join(lines).rstrip() + "\n"

    if isinstance(result, PrimeResult):
        return _render_prime_text(result.payload)

    if isinstance(result, ContextResult):
        payload = _payload(result)
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"

    payload = _payload(result)
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def emit_result(args: argparse.Namespace, root: Path, result: Any) -> None:
    if getattr(args, "json", False):
        emit_ok(args, root, result)
        return

    if isinstance(result, ServicesRefreshIndexResult) and bool(
        getattr(args, "print", False)
    ):
        sys.stdout.write(_render_services_index_text(result.index))
        return

    sys.stdout.write(_render_text(result))


def cmd_repo_status(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_status(root=root)
    emit_result(args, root, res)


def cmd_repo_worktree_add(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_add(
        branch=args.branch,
        base_ref=args.base_ref,
        path=args.path,
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_worktree_ensure(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_ensure(
        branch=args.branch,
        path=getattr(args, "path", None),
        base_ref=args.base_ref,
        allow_dirty=bool(args.allow_dirty),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_worktree_rm(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_rm(
        branch=args.branch,
        force=bool(args.force),
        confirm=bool(args.yes),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_worktree_rm_path(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_rm_path(
        path=args.path,
        force=bool(args.force),
        confirm=bool(args.yes),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_worktree_prune(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_prune(root=root)
    emit_result(args, root, res)


def cmd_repo_worktree_ensure_detached(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_ensure_detached(path=args.path, ref=args.ref, root=root)
    emit_result(args, root, res)


def cmd_repo_worktree_ls(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_ls(root=root)
    emit_result(args, root, res)


def cmd_repo_worktree_status(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_status(
        worktree=str(getattr(args, "worktree", "") or ""), root=root
    )
    emit_result(args, root, res)


def cmd_repo_worktree_check_clean(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_check_clean(
        worktree=str(getattr(args, "worktree", "") or ""),
        allow_untracked=bool(getattr(args, "allow_untracked", False)),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_worktree_check_divergence(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_check_divergence(
        base=str(getattr(args, "base", "") or ""),
        worktree=str(getattr(args, "worktree", "") or ""),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_worktree_annotate(args: argparse.Namespace) -> None:
    root = repo_root()
    from agent_loom.workspace.worktree_meta import repo_worktree_annotate

    res = repo_worktree_annotate(
        repo_root=root,
        branch=str(args.branch),
        purpose=str(args.purpose),
        ticket_id=str(getattr(args, "ticket", "") or ""),
        owner=str(getattr(args, "owner", "") or ""),
        ttl=str(getattr(args, "ttl", "") or ""),
        kind=str(getattr(args, "kind", "normal") or "normal"),
    )
    emit_result(args, root, res)


def cmd_repo_snapshot_capture(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_snapshot_capture(
        name=str(args.name),
        worktree=str(getattr(args, "worktree", "") or ""),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_snapshot_diff(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_snapshot_diff(name=str(args.name), root=root)
    emit_result(args, root, res)


def cmd_repo_snapshot_restore(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_snapshot_restore(
        name=str(args.name),
        confirm=bool(getattr(args, "yes", False)),
        force_clean=bool(getattr(args, "force_clean", False)),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_cleanup_suggest(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_cleanup_suggest(root=root)
    emit_result(args, root, res)


def cmd_repo_cleanup_apply(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_cleanup_apply(
        ids=list(args.id or []),
        confirm=bool(args.yes),
        force=bool(args.force),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_sandbox_create(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_sandbox_create(
        base_ref=str(args.base),
        name=str(getattr(args, "name", "") or ""),
        ttl=str(getattr(args, "ttl", "") or "2h"),
        purpose=str(getattr(args, "purpose", "sandbox") or "sandbox"),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_sandbox_promote(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_sandbox_promote(
        from_branch=str(args.from_branch),
        to_branch=str(args.to_branch),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_sandbox_gc(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_sandbox_gc(confirm=bool(args.yes), force=bool(args.force), root=root)
    emit_result(args, root, res)


def cmd_repo_merge_attempt(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_merge_attempt(
        worktree=args.worktree,
        base=args.base,
        topic=args.topic,
        force_clean=bool(args.force_clean),
        root=root,
    )
    emit_result(args, root, res)


def cmd_poly_init(args: argparse.Namespace) -> None:
    root = Path.cwd().resolve()
    res = poly_init(root=root)
    emit_result(args, root, res)


def cmd_repo_init(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_init(root=root)
    emit_result(args, root, res)


def cmd_add(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = add_repo(
        name=args.name,
        remote=args.remote,
        default_branch=args.default_branch,
        shallow=bool(args.shallow),
        depth=int(args.depth),
        clone=bool(args.clone),
        force=bool(args.force),
        root=root,
    )
    emit_result(args, root, res)


def cmd_remove(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = remove_repo(
        name=args.name,
        delete_clone=bool(args.delete_clone),
        delete_service_md=bool(args.delete_service_md),
        confirm_delete=bool(args.yes_delete),
        root=root,
    )
    emit_result(args, root, res)


def cmd_list(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = list_repos(root=root)
    emit_result(args, root, res)


def cmd_sync(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = sync(
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        clone=bool(args.clone),
        jobs=int(args.jobs),
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_status(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = status(
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        jobs=int(args.jobs),
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_context(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = context(
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        jobs=int(args.jobs),
        root=root,
    )
    emit_result(args, root, res)


def cmd_branch(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = branch(
        branch=args.branch,
        reset=bool(args.reset),
        allow_dirty=bool(args.allow_dirty),
        clone=bool(args.clone),
        base_ref=args.base_ref,
        refresh_index=bool(args.refresh_index),
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        confirm_reset=bool(args.yes),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_add(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_add(
        group=args.group,
        base_ref=args.base_ref,
        claim=bool(getattr(args, "claim", False)),
        clone=bool(args.clone),
        allow_dirty=bool(args.allow_dirty),
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_rm(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_rm(
        group=args.group,
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        force=bool(args.force),
        confirm=bool(args.yes),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_ls(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_ls(root=root)
    emit_result(args, root, res)


def cmd_worktree_prune(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_prune(
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_group_status(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_group_status(
        group=args.group,
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_group_check_clean(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_group_check_clean(
        group=args.group,
        allow_untracked=bool(args.allow_untracked),
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_group_check_divergence(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_group_check_divergence(
        group=args.group,
        base=str(args.base),
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_group_annotate(args: argparse.Namespace) -> None:
    root = workspace_root()
    from agent_loom.workspace.worktree_meta import poly_group_annotate

    res = poly_group_annotate(
        ws_root=root,
        group=str(args.group),
        purpose=str(args.purpose),
        ticket_id=str(getattr(args, "ticket", "") or ""),
        owner=str(getattr(args, "owner", "") or ""),
        ttl=str(getattr(args, "ttl", "") or ""),
        kind=str(getattr(args, "kind", "normal") or "normal"),
    )
    emit_result(args, root, res)


def cmd_poly_sandbox_create(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = poly_sandbox_create(
        group=str(args.group),
        base_ref=str(args.base_ref),
        ttl=str(getattr(args, "ttl", "2h") or "2h"),
        purpose=str(getattr(args, "purpose", "sandbox") or "sandbox"),
        claim=bool(getattr(args, "claim", False)),
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        clone=bool(getattr(args, "clone", False)),
        root=root,
    )
    emit_result(args, root, res)


def cmd_poly_sandbox_promote(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = poly_sandbox_promote(group=str(args.group), root=root)
    emit_result(args, root, res)


def cmd_poly_sandbox_gc(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = poly_sandbox_gc(confirm=bool(args.yes), force=bool(args.force), root=root)
    emit_result(args, root, res)


def cmd_worktree_rebase(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_rebase(
        group=args.group,
        base_ref=args.base_ref,
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_push(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_push(
        group=args.group,
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        force=bool(args.force),
        force_with_lease=bool(args.force_with_lease),
        set_upstream=bool(args.set_upstream),
        confirm_force=bool(args.yes),
        root=root,
    )
    emit_result(args, root, res)


def cmd_snapshot_capture(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = snapshot(
        name=args.name,
        group=args.group,
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_snapshot_diff(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = snapshot_diff(name=args.name, root=root)
    emit_result(args, root, res)


def cmd_snapshot_restore(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = snapshot_restore(
        name=args.name,
        confirm=bool(args.yes),
        force_clean=bool(args.force_clean),
        root=root,
    )
    emit_result(args, root, res)


def cmd_services_refresh_index(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = services_refresh_index(root=root)
    emit_result(args, root, res)


def cmd_deps_show(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = deps_show(service=args.service, root=root)
    emit_result(args, root, res)


def cmd_deps_who_uses(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = deps_who_uses(service=args.service, root=root)
    emit_result(args, root, res)


def cmd_deps_closure(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = deps_closure(service=args.service, root=root)
    emit_result(args, root, res)


def cmd_deps_impacted(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = deps_impacted(service=args.service, root=root)
    emit_result(args, root, res)


def cmd_poly_exec(args: argparse.Namespace) -> None:
    root = workspace_root()
    cmd = list(getattr(args, "cmd_argv", []) or [])
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    res = poly_exec(
        cmd=cmd,
        group=args.group,
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        jobs=int(args.jobs),
        require_clean=bool(args.require_clean),
        root=root,
    )
    emit_result(args, root, res)


def cmd_poly_repo_edit(args: argparse.Namespace) -> None:
    root = workspace_root()
    shallow: Optional[bool]
    if bool(getattr(args, "shallow", False)):
        shallow = True
    elif bool(getattr(args, "no_shallow", False)):
        shallow = False
    else:
        shallow = None

    res = poly_repo_edit(
        name=args.name,
        remote=getattr(args, "remote", None),
        default_branch=getattr(args, "default_branch", None),
        add_tags=getattr(args, "add_tag", None),
        rm_tags=getattr(args, "rm_tag", None),
        description=getattr(args, "description", None),
        shallow=shallow,
        depth=getattr(args, "depth", None),
        root=root,
    )
    emit_result(args, root, res)


def cmd_poly_set_upsert(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = poly_set_upsert(name=args.name, items=args.items, root=root)
    emit_result(args, root, res)


def cmd_poly_set_rm(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = poly_set_rm(name=args.name, root=root)
    emit_result(args, root, res)


def cmd_poly_set_show(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = poly_set_show(name=args.name, root=root)
    emit_result(args, root, res)


def cmd_poly_set_ls(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = poly_set_ls(root=root)
    emit_result(args, root, res)


def cmd_lease_acquire(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = lease_acquire(key=args.key, force=bool(args.force), root=root)
    emit_result(args, root, res)


def cmd_lease_release(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = lease_release(key=args.key, root=root)
    emit_result(args, root, res)


def cmd_lease_ls(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = lease_list(root=root)
    emit_result(args, root, res)


def cmd_worktree_gc(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_gc(
        older_than_days=int(args.older_than),
        unclaimed_only=bool(args.unclaimed_only),
        force=bool(args.force),
        confirm=bool(args.yes),
        root=root,
    )
    emit_result(args, root, res)


def cmd_deepen(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = deepen(repo=args.repo, depth=int(args.depth), root=root)
    emit_result(args, root, res)


def cmd_prime(args: argparse.Namespace) -> None:
    res = prime()
    payload = res.payload
    root = Path.cwd().resolve()
    if getattr(args, "json", False):
        _emit_json(
            {
                "ok": True,
                "cmd": "prime",
                "root": str(root),
                "data": payload,
                "meta": {"generated_at": now_iso()},
            }
        )
        return
    sys.stdout.write(_render_prime_text(payload))


def _add_poly_parser(root_sub: Any) -> None:
    p = root_sub.add_parser(
        "poly",
        help="Workspace-level control plane (polyrepo)",
        description="Workspace-level control plane (polyrepo)",
    )
    sub = p.add_subparsers(dest="poly_cmd", required=True)

    sp = sub.add_parser(
        "init", help="Initialize workspace.json + dirs + baseline .gitignore"
    )
    sp.set_defaults(func=cmd_poly_init)

    sp = sub.add_parser(
        "exec", help="Run a command across repos (optionally a worktree group)"
    )
    sp.add_argument(
        "--group",
        default=None,
        help="Run in worktrees/<group>/<repo> instead of repos/<repo>",
    )
    sp.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    sp.add_argument("--repos", nargs="*", help="Subset of repos (default all)")
    sp.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    sp.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="Parallelism for command execution (default: 1)",
    )
    sp.add_argument(
        "--require-clean",
        action="store_true",
        help="Skip dirty repos/worktrees",
    )
    sp.add_argument(
        "cmd_argv",
        nargs=argparse.REMAINDER,
        help="Command to run (use: exec -- <cmd...>)",
    )
    sp.set_defaults(func=cmd_poly_exec)

    sp = sub.add_parser("repo", help="Edit workspace repo metadata")
    sub_repo = sp.add_subparsers(dest="repo_cmd", required=True)

    spe = sub_repo.add_parser("edit", help="Edit a repo entry in workspace.json")
    spe.add_argument("name")
    spe.add_argument("--remote", default=None)
    spe.add_argument("--default-branch", dest="default_branch", default=None)
    spe.add_argument("--description", default=None)
    spe.add_argument("--add-tag", action="append", default=[])
    spe.add_argument("--rm-tag", action="append", default=[])
    sh = spe.add_mutually_exclusive_group()
    sh.add_argument("--shallow", action="store_true")
    sh.add_argument("--no-shallow", dest="no_shallow", action="store_true")
    spe.add_argument("--depth", type=int, default=None)
    spe.set_defaults(func=cmd_poly_repo_edit)

    sp = sub.add_parser("set", help="Manage repo sets (workspace.json repo_sets)")
    sub_set = sp.add_subparsers(dest="set_cmd", required=True)

    sps = sub_set.add_parser("upsert", help="Create/update a repo set")
    sps.add_argument("name")
    sps.add_argument("items", nargs="*")
    sps.set_defaults(func=cmd_poly_set_upsert)

    sps = sub_set.add_parser("rm", help="Remove a repo set")
    sps.add_argument("name")
    sps.set_defaults(func=cmd_poly_set_rm)

    sps = sub_set.add_parser("show", help="Show a repo set")
    sps.add_argument("name")
    sps.set_defaults(func=cmd_poly_set_show)

    sps = sub_set.add_parser("ls", help="List repo sets")
    sps.set_defaults(func=cmd_poly_set_ls)

    sp = sub.add_parser("lease", help="Coordination leases (agent-safe locks)")
    sub_lease = sp.add_subparsers(dest="lease_cmd", required=True)

    spl = sub_lease.add_parser("acquire", help="Acquire a lease key")
    spl.add_argument("key")
    spl.add_argument("--force", action="store_true", help="Steal an existing lease")
    spl.set_defaults(func=cmd_lease_acquire)

    spl = sub_lease.add_parser("release", help="Release a lease key")
    spl.add_argument("key")
    spl.set_defaults(func=cmd_lease_release)

    spl = sub_lease.add_parser("ls", help="List leases")
    spl.set_defaults(func=cmd_lease_ls)

    sp = sub.add_parser("sandbox", help="Sandbox worktrees (poly)")
    subs = sp.add_subparsers(dest="sandbox_cmd", required=True)

    spc = subs.add_parser("create", help="Create sandbox worktrees for a group")
    spc.add_argument("group")
    spc.add_argument("--base-ref", required=True, help="Base ref-ish")
    spc.add_argument("--ttl", default="2h")
    spc.add_argument("--purpose", default="sandbox")
    spc.add_argument(
        "--claim",
        action="store_true",
        help="Acquire lease group:<group> before creating worktrees",
    )
    spc.add_argument(
        "--clone", action="store_true", help="Clone missing repos automatically"
    )
    spc.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    spc.add_argument("--repos", nargs="*", help="Subset of repos (default all)")
    spc.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    spc.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    spc.set_defaults(func=cmd_poly_sandbox_create)

    spp = subs.add_parser("promote", help="Promote a sandbox group (metadata only)")
    spp.add_argument("group")
    spp.set_defaults(func=cmd_poly_sandbox_promote)

    spg = subs.add_parser("gc", help="Remove expired sandbox groups (requires --yes)")
    spg.add_argument("--force", action="store_true")
    spg.add_argument("--yes", action="store_true")
    spg.set_defaults(func=cmd_poly_sandbox_gc)

    sp = sub.add_parser(
        "add", help="Imperatively add a repo to workspace.json (optionally clone)"
    )
    sp.add_argument("name")
    sp.add_argument("remote")
    sp.add_argument(
        "--default-branch",
        default="",
        help="Default branch (if omitted: infer when --clone, otherwise use main)",
    )
    sp.add_argument(
        "--shallow", action="store_true", help="Use shallow clone/fetch for this repo"
    )
    sp.add_argument(
        "--depth",
        type=int,
        default=1,
        help="History depth for shallow repos (default: 1)",
    )
    sp.add_argument("--clone", action="store_true", help="Clone + fetch immediately")
    sp.add_argument(
        "--force", action="store_true", help="Overwrite existing repo entry"
    )
    sp.set_defaults(func=cmd_add)

    sp = sub.add_parser(
        "remove",
        help="Remove a repo from workspace.json (optionally delete clone/metadata)",
    )
    sp.add_argument("name")
    sp.add_argument("--delete-clone", action="store_true")
    sp.add_argument("--delete-service-md", action="store_true")
    sp.add_argument(
        "--yes-delete",
        dest="yes_delete",
        action="store_true",
        help="Confirm deletions when using --delete-clone",
    )
    sp.set_defaults(func=cmd_remove)

    sp = sub.add_parser("list", help="List configured repos")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser(
        "sync",
        help="Fetch/prune repos; optionally clone missing; refresh services index",
    )
    sp.add_argument(
        "--clone", action="store_true", help="Clone missing repos before fetching"
    )
    sp.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    sp.add_argument("--repos", nargs="*", help="Subset of repos (default all)")
    sp.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    sp.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="Parallelism for network/git operations (default: 1)",
    )
    sp.set_defaults(func=cmd_sync)

    sp = sub.add_parser("status", help="Show branch/sha/dirty for repos")
    sp.add_argument("--repos", nargs="*", help="Subset of repos (default all)")
    sp.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    sp.add_argument(
        "--jobs", type=int, default=1, help="Parallelism for git status (default: 1)"
    )
    sp.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser(
        "context", help="Emit a compact workspace context bundle (ideal for AI prompts)"
    )
    sp.add_argument("--repos", nargs="*", help="Subset of repos (default all)")
    sp.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    sp.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="Parallelism for data gathering (default: 1)",
    )
    sp.set_defaults(func=cmd_context)

    sp = sub.add_parser(
        "branch",
        help="Ensure+checkout a branch across repos (use --reset for git checkout -B)",
    )
    sp.add_argument("branch")
    sp.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    sp.add_argument("--repos", nargs="*", help="Subset of repos (default all)")
    sp.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    sp.add_argument("--base-ref", help="Base ref (default origin/<default_branch>)")
    sp.add_argument(
        "--clone", action="store_true", help="Clone missing repos automatically"
    )
    sp.add_argument(
        "--reset",
        action="store_true",
        help="Reset branch to base_ref (destructive; uses git checkout -B)",
    )
    sp.add_argument(
        "--yes",
        action="store_true",
        help="Confirm destructive operations (required with --reset)",
    )
    sp.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow switching/creating branches when repos have local changes",
    )
    sp.add_argument(
        "--refresh-index",
        action="store_true",
        help="Refresh services index after branching",
    )
    sp.set_defaults(func=cmd_branch)

    sp = sub.add_parser("worktree", help="Worktree operations")
    sub2 = sp.add_subparsers(dest="worktree_cmd", required=True)

    sp2 = sub2.add_parser("add", help="Add worktrees under worktrees/<group>/<repo>")
    sp2.add_argument("group")
    sp2.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    sp2.add_argument("--repos", nargs="*", help="Subset of repos (default all)")
    sp2.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp2.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    sp2.add_argument("--base-ref", help="Base ref (default origin/<default_branch>)")
    sp2.add_argument(
        "--claim",
        action="store_true",
        help="Acquire lease group:<group> before creating worktrees",
    )
    sp2.add_argument(
        "--clone", action="store_true", help="Clone missing repos automatically"
    )
    sp2.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow checking out a safe branch when local changes exist",
    )
    sp2.set_defaults(func=cmd_worktree_add)

    sp2 = sub2.add_parser(
        "ensure",
        help="Ensure worktrees exist under worktrees/<group>/<repo> (resumable)",
    )
    sp2.add_argument("group")
    sp2.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    sp2.add_argument("--repos", nargs="*", help="Subset of repos (default all)")
    sp2.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp2.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    sp2.add_argument("--base-ref", help="Base ref (default origin/<default_branch>)")
    sp2.add_argument(
        "--claim",
        action="store_true",
        help="Acquire lease group:<group> before creating worktrees",
    )
    sp2.add_argument(
        "--clone", action="store_true", help="Clone missing repos automatically"
    )
    sp2.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow checking out a safe branch when local changes exist",
    )
    sp2.set_defaults(func=cmd_worktree_add)

    sp2 = sub2.add_parser(
        "rm", help="Remove worktrees for a group (optionally subset repos)"
    )
    sp2.add_argument("group")
    sp2.add_argument(
        "--yes",
        action="store_true",
        help="Confirm deletion (required)",
    )
    sp2.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    sp2.add_argument(
        "--repos", nargs="*", help="Subset of repos (default: all under group)"
    )
    sp2.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp2.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    sp2.add_argument(
        "--force",
        action="store_true",
        help="Force removal even if worktree has local changes",
    )
    sp2.set_defaults(func=cmd_worktree_rm)

    sp2 = sub2.add_parser(
        "ls", help="List all worktrees with group/repo/branch/sha/status"
    )
    sp2.set_defaults(func=cmd_worktree_ls)

    sp2 = sub2.add_parser("prune", help="Prune stale git worktree metadata in repos")
    sp2.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    sp2.add_argument("--repos", nargs="*", help="Subset of repos (default all)")
    sp2.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp2.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    sp2.set_defaults(func=cmd_worktree_prune)

    sp2 = sub2.add_parser("status", help="Show status for a worktree group")
    sp2.add_argument("group")
    sp2.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    sp2.add_argument(
        "--repos", nargs="*", help="Subset of repos (default: all under group)"
    )
    sp2.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp2.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    sp2.set_defaults(func=cmd_worktree_group_status)

    sp2 = sub2.add_parser("check-clean", help="Fail if any group worktree is dirty")
    sp2.add_argument("group")
    sp2.add_argument(
        "--allow-untracked",
        action="store_true",
        help="Ignore untracked files when determining cleanliness",
    )
    sp2.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    sp2.add_argument(
        "--repos", nargs="*", help="Subset of repos (default: all under group)"
    )
    sp2.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp2.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    sp2.set_defaults(func=cmd_worktree_group_check_clean)

    sp2 = sub2.add_parser(
        "check-divergence", help="Ahead/behind vs --base for group worktrees"
    )
    sp2.add_argument("group")
    sp2.add_argument("--base", required=True, help="Base ref-ish")
    sp2.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    sp2.add_argument(
        "--repos", nargs="*", help="Subset of repos (default: all under group)"
    )
    sp2.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp2.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    sp2.set_defaults(func=cmd_worktree_group_check_divergence)

    sp2 = sub2.add_parser("annotate", help="Annotate a group with purpose/ttl")
    sp2.add_argument("group")
    sp2.add_argument("--purpose", required=True)
    sp2.add_argument("--ticket", default="")
    sp2.add_argument("--owner", default="")
    sp2.add_argument("--ttl", default="")
    sp2.add_argument("--kind", default="normal", choices=["normal", "sandbox"])
    sp2.set_defaults(func=cmd_worktree_group_annotate)

    sp2 = sub2.add_parser(
        "rebase", help="Rebase worktrees for a group onto their base branch"
    )
    sp2.add_argument("group")
    sp2.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    sp2.add_argument(
        "--repos", nargs="*", help="Subset of repos (default: all under group)"
    )
    sp2.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp2.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    sp2.add_argument("--base-ref", help="Base ref (default origin/<default_branch>)")
    sp2.set_defaults(func=cmd_worktree_rebase)

    sp2 = sub2.add_parser(
        "push", help="Push worktrees for a group to their remote branch"
    )
    sp2.add_argument("group")
    sp2.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    sp2.add_argument(
        "--repos", nargs="*", help="Subset of repos (default: all under group)"
    )
    sp2.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    sp2.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")

    push_mode = sp2.add_mutually_exclusive_group()
    push_mode.add_argument(
        "-u", "--set-upstream", action="store_true", help="Set upstream tracking branch"
    )
    push_mode.add_argument(
        "--force", action="store_true", help="Force push (use with caution)"
    )
    push_mode.add_argument(
        "--force-with-lease", action="store_true", help="Force push with lease (safer)"
    )
    sp2.add_argument(
        "--yes",
        action="store_true",
        help="Confirm destructive operations (required with --force/--force-with-lease)",
    )
    sp2.set_defaults(func=cmd_worktree_push)

    sp2 = sub2.add_parser(
        "gc",
        help="Garbage collect old worktrees (requires --yes; optionally unclaimed-only)",
    )
    sp2.add_argument(
        "--older-than",
        type=int,
        default=0,
        help="Only remove groups older than N days (0 = no age filter)",
    )
    sp2.add_argument(
        "--unclaimed-only",
        action="store_true",
        help="Only remove groups without a group:<name> lease",
    )
    sp2.add_argument(
        "--force",
        action="store_true",
        help="Force removal even if worktrees have local changes",
    )
    sp2.add_argument("--yes", action="store_true", help="Confirm deletions")
    sp2.set_defaults(func=cmd_worktree_gc)

    sp = sub.add_parser(
        "snapshot", help="Snapshot/compare/restore repo or worktree state"
    )
    sub_snap = sp.add_subparsers(dest="snapshot_cmd", required=True)

    spc = sub_snap.add_parser(
        "capture",
        help="Write states/<name>.json with branch/sha/dirty per repo (or per worktree group)",
    )
    spc.add_argument("name")
    spc.add_argument(
        "--group",
        default=None,
        help="Capture from worktrees/<group>/<repo> instead of repos/<repo>",
    )
    spc.add_argument(
        "--all",
        action="store_true",
        help="Confirm operating on multiple repos when no selection is provided",
    )
    spc.add_argument("--repos", nargs="*", help="Subset of repos (default all)")
    spc.add_argument("--set", dest="sets", action="append", help="Select repos by set")
    spc.add_argument("--tag", dest="tags", action="append", help="Select repos by tag")
    spc.set_defaults(func=cmd_snapshot_capture)

    spd = sub_snap.add_parser("diff", help="Compare current state to a snapshot")
    spd.add_argument("name")
    spd.set_defaults(func=cmd_snapshot_diff)

    spr = sub_snap.add_parser(
        "restore",
        help="Restore repos/worktrees to a snapshot (requires --yes)",
    )
    spr.add_argument("name")
    spr.add_argument("--yes", action="store_true", help="Confirm restore")
    spr.add_argument(
        "--force-clean",
        action="store_true",
        help="Abort merges, hard reset, and clean before restoring",
    )
    spr.set_defaults(func=cmd_snapshot_restore)

    sp = sub.add_parser("services", help="Service metadata cache operations")
    sub3 = sp.add_subparsers(dest="services_cmd", required=True)

    sp3 = sub3.add_parser(
        "refresh-index", help="Rebuild services/index.json from services/*.md"
    )
    sp3.add_argument(
        "--print", action="store_true", help="Print a concise view after refresh"
    )
    sp3.set_defaults(func=cmd_services_refresh_index)

    sp = sub.add_parser("deps", help="Dependency queries (from services/index.json)")
    sub4 = sp.add_subparsers(dest="deps_cmd", required=True)

    sp4 = sub4.add_parser("show", help="Show deps + reverse deps for a service")
    sp4.add_argument("service")
    sp4.set_defaults(func=cmd_deps_show)

    sp4 = sub4.add_parser("who-uses", help="List services that depend on a service")
    sp4.add_argument("service")
    sp4.set_defaults(func=cmd_deps_who_uses)

    sp4 = sub4.add_parser(
        "closure", help="Transitive deps + reverse deps for a service"
    )
    sp4.add_argument("service")
    sp4.set_defaults(func=cmd_deps_closure)

    sp4 = sub4.add_parser(
        "impacted", help="Transitive reverse deps (who is impacted by changes)"
    )
    sp4.add_argument("service")
    sp4.set_defaults(func=cmd_deps_impacted)

    sp = sub.add_parser("deepen", help="Deepen history of a shallow repo")
    sp.add_argument("repo", help="Repo name")
    sp.add_argument(
        "--depth", type=int, default=50, help="Number of commits to deepen by"
    )
    sp.set_defaults(func=cmd_deepen)

    return None


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="loom workspace",
        description="Workspace + worktree tooling",
    )
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("prime", help="Operating manual + canonical examples")
    sp.set_defaults(func=cmd_prime)

    sp = sub.add_parser("status", help="Show branch/sha/dirty for this repo")
    sp.set_defaults(func=cmd_repo_status)

    sp = sub.add_parser(
        "init",
        help=f"Initialize {REPO_INTERNAL_DIR}/worktrees and ignore bookkeeping",
    )
    sp.set_defaults(func=cmd_repo_init)

    sp = sub.add_parser("worktree", help="Worktree operations (single repo)")
    sub2 = sp.add_subparsers(dest="worktree_cmd", required=True)

    sp2 = sub2.add_parser(
        "add",
        help=f"Add a worktree for a branch under {REPO_INTERNAL_DIR}/worktrees/<branch>",
    )
    sp2.add_argument("branch")
    sp2.add_argument("--base-ref", help="Base ref for new branch")
    sp2.add_argument("--path", help="Override destination path")
    sp2.set_defaults(func=cmd_repo_worktree_add)

    sp2 = sub2.add_parser(
        "ensure",
        help=f"Ensure a branch worktree exists (resumable) under {REPO_INTERNAL_DIR}/worktrees/<branch>",
    )
    sp2.add_argument("branch")
    sp2.add_argument("--path", required=False, help="Destination path (optional)")
    sp2.add_argument("--base-ref", help="Base ref for new branch")
    sp2.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow returning an existing worktree with uncommitted changes",
    )
    sp2.set_defaults(func=cmd_repo_worktree_ensure)

    sp2 = sub2.add_parser("status", help="Show branch/sha/dirty for a worktree")
    sp2.add_argument(
        "--worktree",
        default="",
        help="Branch name or path (default: repo root)",
    )
    sp2.set_defaults(func=cmd_repo_worktree_status)

    sp2 = sub2.add_parser("check-clean", help="Fail if a worktree is dirty")
    sp2.add_argument(
        "--worktree",
        default="",
        help="Branch name or path (default: repo root)",
    )
    sp2.add_argument(
        "--allow-untracked",
        action="store_true",
        help="Ignore untracked files when determining cleanliness",
    )
    sp2.set_defaults(func=cmd_repo_worktree_check_clean)

    sp2 = sub2.add_parser(
        "check-divergence", help="Ahead/behind vs --base for a worktree"
    )
    sp2.add_argument("--base", required=True, help="Base ref-ish")
    sp2.add_argument(
        "--worktree",
        default="",
        help="Branch name or path (default: repo root)",
    )
    sp2.set_defaults(func=cmd_repo_worktree_check_divergence)

    sp2 = sub2.add_parser(
        "annotate", help="Annotate a branch worktree with purpose/ttl"
    )
    sp2.add_argument("branch")
    sp2.add_argument("--purpose", required=True)
    sp2.add_argument("--ticket", default="")
    sp2.add_argument("--owner", default="")
    sp2.add_argument("--ttl", default="")
    sp2.add_argument("--kind", default="normal", choices=["normal", "sandbox"])
    sp2.set_defaults(func=cmd_repo_worktree_annotate)

    sp2 = sub2.add_parser("rm", help="Remove a worktree for a branch (requires --yes)")
    sp2.add_argument("branch")
    sp2.add_argument("--yes", action="store_true", help="Confirm deletion")
    sp2.add_argument(
        "--force", action="store_true", help="Pass --force to git worktree remove"
    )
    sp2.set_defaults(func=cmd_repo_worktree_rm)

    sp2 = sub2.add_parser("rm-path", help="Remove a worktree by path (requires --yes)")
    sp2.add_argument("path")
    sp2.add_argument("--yes", action="store_true", help="Confirm deletion")
    sp2.add_argument(
        "--force", action="store_true", help="Pass --force to git worktree remove"
    )
    sp2.set_defaults(func=cmd_repo_worktree_rm_path)

    sp2 = sub2.add_parser("prune", help="Prune stale git worktree metadata")
    sp2.set_defaults(func=cmd_repo_worktree_prune)

    sp2 = sub2.add_parser(
        "ensure-detached",
        help="Ensure a detached worktree exists at a path",
    )
    sp2.add_argument("--path", required=True, help="Destination path")
    sp2.add_argument(
        "--ref", required=True, help="Ref-ish (branch, origin/branch, SHA)"
    )
    sp2.set_defaults(func=cmd_repo_worktree_ensure_detached)

    sp2 = sub2.add_parser("ls", help="List worktrees")
    sp2.set_defaults(func=cmd_repo_worktree_ls)

    sp = sub.add_parser("merge", help="Merge helpers (single repo)")
    subm = sp.add_subparsers(dest="merge_cmd", required=True)

    spm = subm.add_parser(
        "attempt",
        help="Attempt a local merge in a dedicated worktree (returns merged=true/false)",
    )
    spm.add_argument("--worktree", required=True, help="Worktree path")
    spm.add_argument("--base", required=True, help="Base ref-ish")
    spm.add_argument("--topic", required=True, help="Topic ref/branch")
    spm.add_argument(
        "--force-clean",
        action="store_true",
        help="Hard reset + clean the worktree before merging",
    )
    spm.set_defaults(func=cmd_repo_merge_attempt)

    sp = sub.add_parser("cleanup", help="Suggest/apply safe worktree cleanup")
    subc = sp.add_subparsers(dest="cleanup_cmd", required=True)

    spc = subc.add_parser("suggest", help="Suggest cleanup candidates")
    spc.set_defaults(func=cmd_repo_cleanup_suggest)

    spa = subc.add_parser("apply", help="Apply cleanup (requires --yes)")
    spa.add_argument(
        "--id", action="append", default=[], help="Candidate id (repeatable)"
    )
    spa.add_argument("--force", action="store_true", help="Force git worktree remove")
    spa.add_argument("--yes", action="store_true")
    spa.set_defaults(func=cmd_repo_cleanup_apply)

    sp = sub.add_parser("sandbox", help="Create/promote/gc sandbox worktrees")
    subs = sp.add_subparsers(dest="sandbox_cmd", required=True)

    spc = subs.add_parser("create", help="Create a sandbox worktree")
    spc.add_argument("--base", required=True, help="Base ref-ish")
    spc.add_argument("--name", default="", help="Optional sandbox name")
    spc.add_argument("--ttl", default="2h")
    spc.add_argument("--purpose", default="sandbox")
    spc.set_defaults(func=cmd_repo_sandbox_create)

    spp = subs.add_parser("promote", help="Promote a sandbox branch")
    spp.add_argument("--from", dest="from_branch", required=True)
    spp.add_argument("--to", dest="to_branch", required=True)
    spp.set_defaults(func=cmd_repo_sandbox_promote)

    spg = subs.add_parser(
        "gc", help="Remove expired sandbox worktrees (requires --yes)"
    )
    spg.add_argument("--force", action="store_true")
    spg.add_argument("--yes", action="store_true")
    spg.set_defaults(func=cmd_repo_sandbox_gc)

    sp = sub.add_parser("snapshot", help="Snapshot/compare/restore repo/worktree state")
    subs = sp.add_subparsers(dest="snapshot_cmd", required=True)

    spc = subs.add_parser("capture", help="Capture a snapshot")
    spc.add_argument("name")
    spc.add_argument(
        "--worktree",
        default="",
        help="Branch name or path (default: repo root)",
    )
    spc.set_defaults(func=cmd_repo_snapshot_capture)

    spd = subs.add_parser("diff", help="Diff current vs snapshot")
    spd.add_argument("name")
    spd.set_defaults(func=cmd_repo_snapshot_diff)

    spr = subs.add_parser("restore", help="Restore snapshot (requires --yes)")
    spr.add_argument("name")
    spr.add_argument("--yes", action="store_true")
    spr.add_argument("--force-clean", action="store_true")
    spr.set_defaults(func=cmd_repo_snapshot_restore)

    _add_poly_parser(sub)

    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = list(argv) if argv is not None else sys.argv[1:]

    # Global JSON contract: accept --json anywhere.
    json_anywhere = "--json" in argv
    if json_anywhere:
        argv = [a for a in argv if a != "--json"]

    parser = build_parser()

    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        return int(e.code or 0)
    if json_anywhere:
        args.json = True
    try:
        args.func(args)
        return 0
    except WorkspaceError as e:
        if getattr(args, "json", False):
            try:
                if getattr(args, "cmd", "") == "poly":
                    if getattr(args, "poly_cmd", "") == "init":
                        root = Path.cwd().resolve()
                    else:
                        root = workspace_root()
                else:
                    root = repo_root()
            except Exception:
                root = Path.cwd().resolve()
            emit_error(args, root, e)
            return 2
        print(str(e), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        if getattr(args, "json", False):
            emit_error(args, Path.cwd().resolve(), KeyboardInterrupt("Interrupted"))
            return 130
        print("Interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
