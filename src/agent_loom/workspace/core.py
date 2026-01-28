"""workspace — Git-adjacent workspace tool.

Non-negotiable invariant
  `workspace poly` and repo-local `workspace` are orthogonal operating models.
  They are mutually exclusive by design and never cooperate at runtime.

Operating models
  workspace poly  Workspace-level control plane (polyrepo): owns workspace layout, repo inventory,
           cross-repo ops, services metadata, and derived indexes.
  workspace       Repo-native local tooling (single repo): owns worktrees + branch/worktree
           mapping for one repository.

Workspace library + CLI (loom).
"""

from __future__ import annotations

from agent_loom.workspace.poly_ops import (
    add_repo,
    branch,
    context,
    deepen,
    deps_show,
    deps_who_uses,
    list_repos,
    poly_init,
    remove_repo,
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
    worktree_ls,
    worktree_prune,
    worktree_push,
    worktree_rebase,
    worktree_rm,
)
from agent_loom.workspace.exec_ops import poly_exec
from agent_loom.workspace.deps_ops import deps_closure, deps_impacted
from agent_loom.workspace.gc_ops import worktree_gc
from agent_loom.workspace.leases import lease_acquire, lease_list, lease_release
from agent_loom.workspace.meta_ops import (
    poly_repo_edit,
    poly_set_ls,
    poly_set_rm,
    poly_set_show,
    poly_set_upsert,
)
from agent_loom.workspace.prime import prime
from agent_loom.workspace.repo_ops import (
    repo_merge_attempt,
    repo_init,
    repo_root,
    repo_status,
    repo_snapshot_capture,
    repo_snapshot_diff,
    repo_snapshot_restore,
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
)

__all__ = [
    "prime",
    "repo_root",
    "repo_init",
    "repo_status",
    "repo_snapshot_capture",
    "repo_snapshot_diff",
    "repo_snapshot_restore",
    "repo_worktree_add",
    "repo_worktree_ensure",
    "repo_worktree_status",
    "repo_worktree_check_clean",
    "repo_worktree_check_divergence",
    "repo_worktree_rm",
    "repo_worktree_rm_path",
    "repo_worktree_prune",
    "repo_worktree_ensure_detached",
    "repo_worktree_ls",
    "repo_merge_attempt",
    "poly_init",
    "poly_exec",
    "add_repo",
    "remove_repo",
    "list_repos",
    "context",
    "sync",
    "status",
    "branch",
    "worktree_add",
    "worktree_rm",
    "worktree_ls",
    "worktree_prune",
    "worktree_group_status",
    "worktree_group_check_clean",
    "worktree_group_check_divergence",
    "worktree_rebase",
    "worktree_push",
    "snapshot",
    "snapshot_diff",
    "snapshot_restore",
    "services_refresh_index",
    "deps_show",
    "deps_who_uses",
    "deps_closure",
    "deps_impacted",
    "deepen",
    "poly_repo_edit",
    "poly_set_upsert",
    "poly_set_rm",
    "poly_set_show",
    "poly_set_ls",
    "lease_acquire",
    "lease_release",
    "lease_list",
    "worktree_gc",
]
