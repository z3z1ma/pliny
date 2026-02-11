from __future__ import annotations

import re

SUBSYSTEM_NAME = "agent-loom-memory"
SUBSYSTEM_VERSION = "1.2.0"

DEFAULT_VAULT_DIR = ".loom/memory"
META_FILENAME = "meta.json"
DB_FILENAME = "index.sqlite3"

SCHEMA_VERSION = 1
DB_SCHEMA_VERSION = 1

VISIBILITIES = ("shared", "personal", "ephemeral")
STATUSES = ("active", "deprecated")

RE_NOTE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
RE_TAG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
RE_WORD = re.compile(r"[A-Za-z0-9_]+")

WIKILINK_RE = re.compile(r"\[\[([^\[\]]+?)\]\]")
MDLINK_RE = re.compile(r"(?<!\!)\[[^\]]*?\]\(([^)]+?)\)")

FENCED_CODE_RE = re.compile(r"(?ms)^```.*?^```\s*$")
FENCED_TILDE_RE = re.compile(r"(?ms)^~~~.*?^~~~\s*$")

SCOPE_KINDS = ("file", "folder", "filetype", "command", "tag")
SCOPE_KIND_KEY = {
    "file": "path",
    "folder": "path",
    "filetype": "ext",
    "command": "pattern",
    "tag": "tag",
}

SCOPE_MATCH_SCORE = {
    "file": 50,
    "folder": 40,
    "command": 20,
    "filetype": 10,
    "tag": 5,
}


__all__ = [
    "DB_FILENAME",
    "DB_SCHEMA_VERSION",
    "DEFAULT_VAULT_DIR",
    "FENCED_CODE_RE",
    "FENCED_TILDE_RE",
    "MDLINK_RE",
    "META_FILENAME",
    "RE_NOTE_ID",
    "RE_TAG",
    "RE_WORD",
    "SCHEMA_VERSION",
    "SCOPE_KIND_KEY",
    "SCOPE_KINDS",
    "SCOPE_MATCH_SCORE",
    "STATUSES",
    "VISIBILITIES",
    "WIKILINK_RE",
]
