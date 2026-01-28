from __future__ import annotations

from agent_loom.workspace.constants import (
    INTERNAL_DIR,
    REPO_INTERNAL_DIR,
    REPOS_DIR,
    SERVICES_DIR,
    STATES_DIR,
    SUBSYSTEM_NAME,
    SUBSYSTEM_VERSION,
    WORKSPACE_FILE,
    WORKTREES_DIR,
)
from agent_loom.workspace.models import PrimeResult


def prime() -> PrimeResult:
    payload = {
        "tool": {"name": SUBSYSTEM_NAME, "version": SUBSYSTEM_VERSION},
        "purpose": "Git-adjacent workspace tool for managing poly workspaces and repo-local worktrees",
        "zen": [
            "Two operating models: workspace poly and repo-local workspace are mutually exclusive.",
            "Repo-local workspace runs inside one git repo; poly runs at the workspace root.",
            "One global --json contract.",
        ],
        "storage": {
            "poly_control_plane": {
                "root_markers": [WORKSPACE_FILE, f"{INTERNAL_DIR}/"],
                "internal_dir": INTERNAL_DIR,
                "repos_dir_default": REPOS_DIR,
                "worktrees_dir_default": WORKTREES_DIR,
                "states_dir_default": STATES_DIR,
                "services_dir_default": SERVICES_DIR,
            },
            "repo_mode": {
                "internal_dir": REPO_INTERNAL_DIR,
                "git_exclude": ".git/info/exclude (best-effort ignore for .loom-repo/)",
            },
        },
        "dispatch": {
            "explicit": [
                "loom workspace <repo-command> ...",
                "loom workspace poly <poly-command> ...",
            ],
        },
        "output": {
            "default": "human-readable output",
            "json": "--json can appear anywhere; emits JSON envelope (ok/cmd/root/data/meta)",
            "errors": {
                "ok": False,
                "error": {"type": "string", "message": "string"},
            },
        },
        "safety": {
            "worktree_rm": "Requires --yes (and may pass --force to git worktree remove)",
            "merge_force_clean": "--force-clean hard resets + cleans the worktree (destructive)",
            "poly_guardrails": "workspace poly refuses to operate from within managed repos/worktrees",
        },
        "examples": {
            "copy_paste_for_agents_md": [
                "# Worktrees / workspace",
                "- Run: loom workspace prime",
                "- Use JSON: loom workspace --json status | loom workspace --json worktree ls",
                "- Help: loom workspace -h, loom workspace poly -h, loom workspace <command> -h",
            ],
            "init": [
                "loom workspace -h",
                "loom workspace prime",
                "loom workspace poly -h",
                "loom workspace init",
                "loom workspace -h",
            ],
            "poly_happy_path": [
                "loom workspace poly init",
                "loom workspace poly add <name> <remote>",
                "loom workspace poly sync --all --clone",
                "loom workspace poly context --all",
            ],
            "repo_happy_path": [
                "loom workspace init",
                "loom workspace status",
                "loom workspace worktree ls",
                "loom workspace worktree ensure <branch> --path .loom-repo/worktrees/<branch>",
                "loom workspace worktree rm <branch> --yes",
            ],
            "machine": [
                "loom workspace --json status",
                "loom workspace --json worktree ls",
                "loom workspace --json poly list --all",
            ],
        },
        "help": {
            "root": "loom workspace -h",
            "prime": "loom workspace prime",
            "poly": "loom workspace poly -h",
            "command": "loom workspace <command> -h",
        },
    }

    return PrimeResult(payload=payload)
