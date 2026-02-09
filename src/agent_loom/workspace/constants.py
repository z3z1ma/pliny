from __future__ import annotations

import re

SUBSYSTEM_NAME = "agent-loom-workspace"
SUBSYSTEM_VERSION = "0.1.0"

WORKSPACE_FILE = "workspace.json"
INTERNAL_DIR = ".loom"
# Workspace harness (multi-repo control plane) state is rooted under:
#   <harness_root>/.loom/workspaces/
HARNESS_DIR = "workspaces"
REPO_INTERNAL_DIR = ".loom/workspace"
# Harness defaults (relative to the harness root).
REPOS_DIR = ".loom/workspaces/repos"
WORKTREES_DIR = ".loom/workspaces/worktrees"
STATES_DIR = ".loom/workspaces/states"
COMPONENTS_DIR = ".loom/workspaces/components"

DEFAULT_DEFAULT_BRANCH = "main"

COMPONENT_HEADER = """# Component: {name}

This file is maintained by an AI agent. It is the workspace's cached understanding of this component.
It should be kept accurate and updated as changes are made.

## Kind
- service | library | cli | tool | infra | unknown

## Summary
- Language:
- Owner (optional):
- Purpose:

## Exposes (interfaces)
- HTTP:
- Events:
- gRPC:
- CLI:
- Library API:
- Other:

## Depends on (other components / repos)
- (list other component repo names)

## Used by (reverse dependencies)
- (optional; can be computed via index)

## Key files / entrypoints
- (pointers to relevant files in the repo)

## Notes
- (freeform; include invariants, gotchas, migration notes)
"""

DEP_SECTION_RE = re.compile(r"^## Depends on.*?$", re.MULTILINE)
BULLET_RE = re.compile(r"^\s*-\s+(.*\S)\s*$")

SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
REPO_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

__all__ = [
    "SUBSYSTEM_NAME",
    "SUBSYSTEM_VERSION",
    "BULLET_RE",
    "COMPONENT_HEADER",
    "COMPONENTS_DIR",
    "DEFAULT_DEFAULT_BRANCH",
    "DEP_SECTION_RE",
    "HARNESS_DIR",
    "INTERNAL_DIR",
    "REPO_INTERNAL_DIR",
    "REPO_NAME_RE",
    "REPOS_DIR",
    "SHA_RE",
    "STATES_DIR",
    "WORKSPACE_FILE",
    "WORKTREES_DIR",
]
