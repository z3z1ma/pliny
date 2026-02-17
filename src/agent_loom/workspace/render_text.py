from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from agent_loom.core.cli_output import normalize_payload
from agent_loom.workspace.models import (
    AddRepoResult,
    BranchResult,
    ComponentsRefreshIndexResult,
    ContextResult,
    DeepenResult,
    DepsShowResult,
    DepsWhoUsesResult,
    HarnessExecResult,
    HarnessInitResult,
    ImpactResult,
    LeaseAcquireResult,
    LeaseListResult,
    LeaseReleaseResult,
    LeaseRenewResult,
    LeaseShowResult,
    ListReposResult,
    MergeAttemptResult,
    PrimeResult,
    RemoveRepoResult,
    RepoInitResult,
    RepoStatusResult,
    RepoWorktreeAddResult,
    RepoWorktreeEnsureDetachedResult,
    RepoWorktreeListResult,
    RepoWorktreePruneResult,
    RepoWorktreeRemoveResult,
    SnapshotDiffResult,
    SnapshotRestoreResult,
    SnapshotResult,
    StatusResult,
    SyncResult,
    WorktreeAddResult,
    WorktreeDiffResult,
    WorktreeEnsureResult,
    WorktreeGcResult,
    WorktreeGroupDiffResult,
    WorktreeGroupRemoveResult,
    WorktreeListResult,
    WorktreePushResult,
    WorktreeRebaseResult,
)

RenderFn = Callable[[Any], str]


def render_prime_text(payload: dict[str, Any]) -> str:
    text = str(payload.get("markdown") or "")
    if text:
        return text.rstrip() + "\n"
    return ""


def render_services_index_text(index: dict[str, Any]) -> str:
    components = {}
    if isinstance(index, dict):
        components = index.get("components", {}) or index.get("services", {}) or {}
    lines = [f"Components ({len(components)})"]
    for name in sorted(components.keys()):
        entry = components.get(name) or {}
        deps = ", ".join(entry.get("depends_on", []) or []) or "-"
        ext = ", ".join(entry.get("depends_on_external", []) or []) or "-"
        used_by = ", ".join(entry.get("used_by", []) or []) or "-"
        lines.append(f"- {name} deps: {deps} external: {ext} used_by: {used_by}")
    return "\n".join(lines).rstrip() + "\n"


def _bool(value: bool) -> str:
    return "yes" if value else "no"


def _render_json(result: Any) -> str:
    payload = normalize_payload(result)
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _render_worktree_diff(result: WorktreeDiffResult) -> str:
    chunks: list[str] = []
    for file_info in result.files:
        patch = str((file_info or {}).get("patch") or "")
        if patch:
            chunks.append(patch.rstrip("\n") + "\n")
    if not chunks:
        return ""
    return "".join(chunks)


def _render_worktree_group_diff(result: WorktreeGroupDiffResult) -> str:
    lines: list[str] = []
    for row in sorted(result.results, key=lambda x: str((x or {}).get("repo") or "")):
        if str((row or {}).get("status") or "") != "ok":
            continue
        repo = str((row or {}).get("repo") or "")
        worktree = str((row or {}).get("worktree") or "")
        files = row.get("files") if isinstance(row, dict) else None
        patches: list[str] = []
        if isinstance(files, list):
            for file_info in files:
                patch = str((file_info or {}).get("patch") or "")
                if patch:
                    patches.append(patch.rstrip("\n") + "\n")
        if not patches:
            continue
        lines.append(f"===== {repo} ({worktree}) =====\n")
        lines.extend(patches)
    return "".join(lines)


def _render_repo_status(result: RepoStatusResult) -> str:
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


def _render_repo_worktree_add(result: RepoWorktreeAddResult) -> str:
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


def _render_worktree_ensure(result: WorktreeEnsureResult) -> str:
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


def _render_repo_worktree_remove(result: RepoWorktreeRemoveResult) -> str:
    lines = [f"removed: {result.removed}"]
    if result.branch:
        lines.append(f"branch: {result.branch}")
    return "\n".join(lines).rstrip() + "\n"


def _render_repo_worktree_prune(result: RepoWorktreePruneResult) -> str:
    return f"pruned: {_bool(result.pruned)}\n"


def _render_repo_worktree_ensure_detached(result: RepoWorktreeEnsureDetachedResult) -> str:
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


def _render_repo_worktree_list(result: RepoWorktreeListResult) -> str:
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
        suffix = f" ({', '.join(flags)})" if flags else ""
        lines.append(f"- {path} {branch} {head}{suffix}".rstrip())
    return "\n".join(lines).rstrip() + "\n"


def _render_merge_attempt(result: MergeAttemptResult) -> str:
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


def _render_harness_init(result: HarnessInitResult) -> str:
    return (
        "\n".join(
            [
                f"workspace_file: {result.workspace_file}",
                f"repos_dir: {result.repos_dir}",
                f"worktrees_dir: {result.worktrees_dir}",
                f"states_dir: {result.states_dir}",
                f"components_dir: {result.components_dir}",
                f"gitignore_path: {result.gitignore_path}",
                f"updated_gitignore: {_bool(bool(result.updated_gitignore))}",
            ]
        ).rstrip()
        + "\n"
    )


def _render_repo_init(result: RepoInitResult) -> str:
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


def _render_harness_exec(result: HarnessExecResult) -> str:
    summary = result.summary or {}
    return (
        "\n".join(
            [
                f"repos: {summary.get('repos')}",
                f"success: {summary.get('success')}",
                f"fail: {summary.get('fail')}",
                f"skip: {summary.get('skip')}",
            ]
        ).rstrip()
        + "\n"
    )


def _render_lease_acquire(result: LeaseAcquireResult) -> str:
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


def _render_lease_release(result: LeaseReleaseResult) -> str:
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


def _render_lease_list(result: LeaseListResult) -> str:
    keys: list[str] = []
    for row in result.leases or []:
        if not isinstance(row, dict):
            continue
        data = row.get("data")
        if not isinstance(data, dict):
            continue
        key = str(data.get("key") or "").strip()
        if key:
            keys.append(key)
    keys = sorted(set(keys))

    lines = [
        f"leases_dir: {result.leases_dir}",
        f"leases: {len(keys)}",
    ]
    pruned_expired = int(getattr(result, "pruned_expired", 0))
    if pruned_expired:
        lines.append(f"pruned_expired: {pruned_expired}")
    for key in keys:
        lines.append(f"- {key}")
    return "\n".join(lines).rstrip() + "\n"


def _render_lease_show(result: LeaseShowResult) -> str:
    lines = [
        f"key: {result.key}",
        f"lease_path: {result.lease_path}",
        f"exists: {_bool(result.exists)}",
        f"active: {_bool(result.active)}",
    ]
    ttl = (result.data or {}).get("ttl_seconds")
    if ttl is not None:
        lines.append(f"ttl_seconds: {ttl}")
    owner = (result.data or {}).get("owner")
    if isinstance(owner, dict):
        user = str(owner.get("user") or "").strip()
        host = str(owner.get("host") or "").strip()
        if user or host:
            lines.append(f"owner: {user}@{host}".rstrip("@"))
    return "\n".join(lines).rstrip() + "\n"


def _render_lease_renew(result: LeaseRenewResult) -> str:
    ttl = (result.data or {}).get("ttl_seconds")
    lines = [
        f"key: {result.key}",
        f"lease_path: {result.lease_path}",
        f"renewed: {_bool(result.renewed)}",
    ]
    if ttl is not None:
        lines.append(f"ttl_seconds: {ttl}")
    return "\n".join(lines).rstrip() + "\n"


def _render_worktree_gc(result: WorktreeGcResult) -> str:
    return (
        "\n".join(
            [
                f"removed: {len(result.removed)}",
                f"skipped: {len(result.skipped)}",
            ]
        ).rstrip()
        + "\n"
    )


def _render_add_repo(result: AddRepoResult) -> str:
    lines = [f"repo: {result.repo}", f"cloned: {_bool(result.cloned)}"]
    entry = result.entry or {}
    for key in ("remote", "default_branch", "shallow", "depth"):
        if key in entry:
            lines.append(f"{key}: {entry.get(key)}")
    return "\n".join(lines).rstrip() + "\n"


def _render_remove_repo(result: RemoveRepoResult) -> str:
    return (
        "\n".join(
            [
                f"repo: {result.repo}",
                f"deleted_clone: {_bool(result.deleted_clone)}",
                f"deleted_component_md: {_bool(result.deleted_component_md)}",
            ]
        ).rstrip()
        + "\n"
    )


def _render_list_repos(result: ListReposResult) -> str:
    lines = [f"repos: {len(result.repos)}"]
    for row in result.repos:
        name = row.get("name")
        remote = row.get("remote")
        default_branch = row.get("default_branch")
        tags = ",".join(row.get("tags") or []) or "-"
        description = row.get("description") or ""
        bits = [str(name), f"({default_branch})", str(remote), f"tags:{tags}"]
        if description:
            bits.append(f"desc:{description}")
        lines.append("- " + " ".join(bits))
    return "\n".join(lines).rstrip() + "\n"


def _render_sync(result: SyncResult) -> str:
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
    if result.components_index is not None:
        lines.append("components_index: refreshed")
    return "\n".join(lines).rstrip() + "\n"


def _render_status(result: StatusResult) -> str:
    lines = [f"repos: {len(result.repos)}"]
    for row in result.repos:
        lines.append(
            f"- {row.get('repo')} {row.get('branch')} {row.get('sha')} {row.get('status')}"
        )
    return "\n".join(lines).rstrip() + "\n"


def _render_branch(result: BranchResult) -> str:
    lines = [f"branch: {result.branch}"]
    for row in result.repos:
        lines.append(f"- {row.get('repo')} {row.get('branch')}")
    if result.components_index is not None:
        lines.append("components_index: refreshed")
    return "\n".join(lines).rstrip() + "\n"


def _render_worktree_add(result: WorktreeAddResult) -> str:
    lines = [f"group: {result.group}"]
    for row in result.worktrees:
        lines.append(
            f"- {row.get('repo')} {row.get('path')} existed:{_bool(bool(row.get('existed')))}"
        )
    return "\n".join(lines).rstrip() + "\n"


def _render_worktree_group_remove(result: WorktreeGroupRemoveResult) -> str:
    lines = [f"group: {result.group}", f"removed: {len(result.removed)}"]
    for path in result.removed:
        lines.append(f"- {path}")
    if result.warnings:
        lines.append(f"warnings: {len(result.warnings)}")
        for warning in result.warnings:
            lines.append(f"! {warning}")
    return "\n".join(lines).rstrip() + "\n"


def _render_worktree_list(result: WorktreeListResult) -> str:
    lines = [f"worktrees: {len(result.worktrees)}"]
    for row in result.worktrees:
        lines.append(
            f"- {row.get('group')} {row.get('repo')} {row.get('branch')} {row.get('sha')} {row.get('status')}"
        )
    return "\n".join(lines).rstrip() + "\n"


def _render_worktree_rebase(result: WorktreeRebaseResult) -> str:
    lines = [f"group: {result.group}"]
    for row in result.results:
        parts = [f"- {row.get('repo')}", str(row.get("status"))]
        if row.get("onto"):
            parts.append(f"onto:{row.get('onto')}")
        if row.get("reason"):
            parts.append(f"reason:{row.get('reason')}")
        lines.append(" ".join(parts))
    return "\n".join(lines).rstrip() + "\n"


def _render_worktree_push(result: WorktreePushResult) -> str:
    lines = [f"group: {result.group}"]
    for row in result.results:
        parts = [f"- {row.get('repo')}", str(row.get("status"))]
        if row.get("reason"):
            parts.append(f"reason:{row.get('reason')}")
        if row.get("branch"):
            parts.append(f"branch:{row.get('branch')}")
        lines.append(" ".join(parts))
    return "\n".join(lines).rstrip() + "\n"


def _render_snapshot(result: SnapshotResult) -> str:
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


def _render_snapshot_diff(result: SnapshotDiffResult) -> str:
    summary = result.summary or {}
    return (
        "\n".join(
            [
                f"snapshot_path: {result.snapshot_path}",
                f"repos: {summary.get('repos')}",
                f"match: {summary.get('match')}",
                f"changed: {summary.get('changed')}",
                f"missing: {summary.get('missing')}",
            ]
        ).rstrip()
        + "\n"
    )


def _render_snapshot_restore(result: SnapshotRestoreResult) -> str:
    summary = result.summary or {}
    return (
        "\n".join(
            [
                f"snapshot_path: {result.snapshot_path}",
                f"repos: {summary.get('repos')}",
                f"success: {summary.get('success')}",
                f"skipped: {summary.get('skipped')}",
                f"failed: {summary.get('failed')}",
            ]
        ).rstrip()
        + "\n"
    )


def _render_components_refresh_index(result: ComponentsRefreshIndexResult) -> str:
    components = result.index.get("components", {}) if isinstance(result.index, dict) else {}
    return (
        "\n".join(
            [
                f"components_index_path: {result.components_index_path}",
                f"components: {len(components)}",
            ]
        ).rstrip()
        + "\n"
    )


def _render_deps_show(result: DepsShowResult) -> str:
    data = result.data or {}
    deps = ", ".join(data.get("depends_on", []) or []) or "-"
    external = ", ".join(data.get("depends_on_external", []) or []) or "-"
    used_by = ", ".join(data.get("used_by", []) or []) or "-"
    return (
        "\n".join(
            [
                f"component: {result.component}",
                f"depends_on: {deps}",
                f"depends_on_external: {external}",
                f"used_by: {used_by}",
            ]
        ).rstrip()
        + "\n"
    )


def _render_deps_who_uses(result: DepsWhoUsesResult) -> str:
    used_by = ", ".join(result.used_by or []) or "-"
    return (
        "\n".join(
            [
                f"component: {result.component}",
                f"used_by: {used_by}",
            ]
        ).rstrip()
        + "\n"
    )


def _render_impact(result: ImpactResult) -> str:
    source = result.source or {}
    lines: list[str] = []
    kind = str(source.get("kind") or "").strip()
    if kind:
        lines.append(f"source: {kind}")
    if kind == "snapshot":
        name = str(source.get("name") or "").strip()
        if name:
            lines.append(f"snapshot: {name}")
    lines.append(f"changed: {len(result.changed)}")
    for item in result.changed:
        lines.append(f"- {item}")
    if result.unknown:
        lines.append(f"unknown: {len(result.unknown)}")
        for item in result.unknown:
            lines.append(f"- {item}")
    lines.append(f"impacted: {len(result.impacted)}")
    for item in result.impacted:
        lines.append(f"- {item}")
    lines.append(f"all: {len(result.all)}")
    return "\n".join(lines).rstrip() + "\n"


def _render_deepen(result: DeepenResult) -> str:
    lines = [f"repo: {result.repo}"]
    if result.skipped:
        lines.append("skipped: yes")
        if result.reason:
            lines.append(f"reason: {result.reason}")
    else:
        lines.append(f"depth: {result.depth}")
    return "\n".join(lines).rstrip() + "\n"


def _render_prime(result: PrimeResult) -> str:
    return render_prime_text(result.payload)


TEXT_RENDERERS: list[tuple[type[Any], RenderFn]] = [
    (WorktreeDiffResult, _render_worktree_diff),
    (WorktreeGroupDiffResult, _render_worktree_group_diff),
    (RepoStatusResult, _render_repo_status),
    (RepoWorktreeAddResult, _render_repo_worktree_add),
    (WorktreeEnsureResult, _render_worktree_ensure),
    (RepoWorktreeRemoveResult, _render_repo_worktree_remove),
    (RepoWorktreePruneResult, _render_repo_worktree_prune),
    (RepoWorktreeEnsureDetachedResult, _render_repo_worktree_ensure_detached),
    (RepoWorktreeListResult, _render_repo_worktree_list),
    (MergeAttemptResult, _render_merge_attempt),
    (HarnessInitResult, _render_harness_init),
    (RepoInitResult, _render_repo_init),
    (HarnessExecResult, _render_harness_exec),
    (LeaseAcquireResult, _render_lease_acquire),
    (LeaseReleaseResult, _render_lease_release),
    (LeaseListResult, _render_lease_list),
    (LeaseShowResult, _render_lease_show),
    (LeaseRenewResult, _render_lease_renew),
    (WorktreeGcResult, _render_worktree_gc),
    (AddRepoResult, _render_add_repo),
    (RemoveRepoResult, _render_remove_repo),
    (ListReposResult, _render_list_repos),
    (SyncResult, _render_sync),
    (StatusResult, _render_status),
    (BranchResult, _render_branch),
    (WorktreeAddResult, _render_worktree_add),
    (WorktreeGroupRemoveResult, _render_worktree_group_remove),
    (WorktreeListResult, _render_worktree_list),
    (WorktreeRebaseResult, _render_worktree_rebase),
    (WorktreePushResult, _render_worktree_push),
    (SnapshotResult, _render_snapshot),
    (SnapshotDiffResult, _render_snapshot_diff),
    (SnapshotRestoreResult, _render_snapshot_restore),
    (ComponentsRefreshIndexResult, _render_components_refresh_index),
    (DepsShowResult, _render_deps_show),
    (DepsWhoUsesResult, _render_deps_who_uses),
    (ImpactResult, _render_impact),
    (DeepenResult, _render_deepen),
    (PrimeResult, _render_prime),
    (ContextResult, _render_json),
]


def render_text(result: Any) -> str:
    for result_type, renderer in TEXT_RENDERERS:
        if isinstance(result, result_type):
            return renderer(result)
    return _render_json(result)


__all__ = ["render_prime_text", "render_services_index_text", "render_text"]
