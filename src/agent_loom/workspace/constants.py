from __future__ import annotations

import re

SUBSYSTEM_NAME = "agent-loom-workspace"
SUBSYSTEM_VERSION = "0.1.0"

WORKSPACE_FILE = "workspace.json"
INTERNAL_DIR = ".loom"
REPO_INTERNAL_DIR = ".loom-repo"
REPOS_DIR = "repos"
WORKTREES_DIR = "worktrees"
STATES_DIR = "states"
SERVICES_DIR = "services"

DEFAULT_DEFAULT_BRANCH = "main"

SERVICE_HEADER = """# Service: {name}

This file is maintained by an AI agent. It is the workspace's cached understanding of this service.
It should be kept accurate and updated as changes are made.

## Summary
- Language:
- Owner (optional):
- Purpose:

## Exposes (interfaces)
- HTTP:
- Events:
- gRPC:
- Other:

## Depends on (other services / repos)
- (list other service repo names)

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

FS_SAFE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.@+"


__all__ = [
    "SUBSYSTEM_NAME",
    "SUBSYSTEM_VERSION",
    "BULLET_RE",
    "DEFAULT_DEFAULT_BRANCH",
    "DEP_SECTION_RE",
    "FS_SAFE",
    "INTERNAL_DIR",
    "REPO_INTERNAL_DIR",
    "REPO_NAME_RE",
    "REPOS_DIR",
    "SERVICE_HEADER",
    "SERVICES_DIR",
    "SHA_RE",
    "STATES_DIR",
    "WORKSPACE_FILE",
    "WORKTREES_DIR",
]
