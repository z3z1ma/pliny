"""workspace — Git-adjacent workspace tool.

Non-negotiable invariant
  `workspace harness` (multi-repo control plane) and repo-local `workspace` (single repo)
  are orthogonal operating models.
  They are mutually exclusive by design and never cooperate at runtime.

Operating models
  workspace harness  Workspace harness control plane: owns manifest, repo inventory,
           cross-repo ops, component metadata, and derived indexes.
  workspace          Repo-native local tooling (single repo): owns worktrees + branch/worktree
           mapping for one repository.

Workspace library + CLI (loom).
"""

from __future__ import annotations

from agent_loom.workspace.harness.core import (
    add_repo,
    branch,
    context,
    deepen,
    deps_show,
    deps_who_uses,
    list_repos,
    harness_init,
    remove_repo,
    components_refresh_index,
    services_refresh_index,
    snapshot,
    snapshot_diff,
    snapshot_restore,
    status,
    sync,
    worktree_add,
    worktree_group_check_clean,
    worktree_group_check_divergence,
    worktree_group_diff,
    worktree_group_status,
    worktree_ls,
    worktree_prune,
    worktree_push,
    worktree_rebase,
    worktree_rm,
)
from agent_loom.workspace.harness.exec import harness_exec
from agent_loom.workspace.harness.cleanup import (
    harness_cleanup_apply,
    harness_cleanup_suggest,
)
from agent_loom.workspace.harness.deps import deps_closure, deps_impacted
from agent_loom.workspace.harness.impact import (
    harness_impact_repos,
    harness_impact_snapshot,
)
from agent_loom.workspace.harness.gc import worktree_gc
from agent_loom.workspace.harness.leases import (
    lease_acquire,
    lease_is_active,
    lease_list,
    lease_release,
    lease_renew,
    lease_require_active,
    lease_show,
)
from agent_loom.workspace.harness.meta import (
    harness_repo_edit,
    harness_set_ls,
    harness_set_rm,
    harness_set_show,
    harness_set_upsert,
)
from agent_loom.workspace.prime import prime
from agent_loom.workspace.repo.core import (
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
    repo_worktree_diff,
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
    "repo_worktree_diff",
    "repo_worktree_rm",
    "repo_worktree_rm_path",
    "repo_worktree_prune",
    "repo_worktree_ensure_detached",
    "repo_worktree_ls",
    "repo_merge_attempt",
    "harness_init",
    "harness_exec",
    "harness_cleanup_suggest",
    "harness_cleanup_apply",
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
    "worktree_group_diff",
    "worktree_rebase",
    "worktree_push",
    "snapshot",
    "snapshot_diff",
    "snapshot_restore",
    "components_refresh_index",
    "services_refresh_index",
    "deps_show",
    "deps_who_uses",
    "deps_closure",
    "deps_impacted",
    "harness_impact_repos",
    "harness_impact_snapshot",
    "deepen",
    "harness_repo_edit",
    "harness_set_upsert",
    "harness_set_rm",
    "harness_set_show",
    "harness_set_ls",
    "lease_acquire",
    "lease_release",
    "lease_list",
    "lease_show",
    "lease_renew",
    "lease_is_active",
    "lease_require_active",
    "worktree_gc",
]
