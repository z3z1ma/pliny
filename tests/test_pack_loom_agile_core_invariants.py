from __future__ import annotations

import re
from pathlib import Path

from agent_loom.pack.packs import iter_pack_files, list_pack_ids, load_manifest


def test_loom_agile_core_pack_is_listed_and_loadable() -> None:
    assert "loom-agile-core" in list_pack_ids()
    mf = load_manifest("loom-agile-core")
    assert mf.id == "loom-agile-core"
    assert mf.install_roots


def test_loom_agile_core_pack_contains_expected_commands_and_agents() -> None:
    files = dict(iter_pack_files("loom-agile-core"))
    assert ".opencode/commands/loom-agile-help.md" in files
    assert ".opencode/commands/loom-agile-dev-story.md" in files
    assert ".opencode/agents/loom-agile-developer.md" in files
    assert ".opencode/skills/loom-agile-create-prd/SKILL.md" in files


def test_loom_agile_core_pack_is_language_agnostic_and_not_bmad_branded() -> None:
    forbidden = [
        re.compile(r"\buv\s+run\b", re.IGNORECASE),
        re.compile(r"\bbasedpyright\b", re.IGNORECASE),
        re.compile(r"\bruff\b", re.IGNORECASE),
        re.compile(r"\.claude/"),
        re.compile(r"\bClaude\b", re.IGNORECASE),
        re.compile(r"anthropic", re.IGNORECASE),
        re.compile(r"\bBMad\b", re.IGNORECASE),
        re.compile(r"\bbmad\b", re.IGNORECASE),
    ]

    for rel, p in iter_pack_files("loom-agile-core"):
        ext = Path(rel).suffix.lower()
        if ext not in {".md", ".txt", ".yaml", ".yml", ".xml", ".json"}:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for rx in forbidden:
            assert not rx.search(text), f"forbidden {rx.pattern} in {rel}"


def test_builtin_compound_and_team_manifests_are_loadable() -> None:
    for pack_id in ("loom-compound-core", "loom-team-core"):
        assert pack_id in list_pack_ids()
        mf = load_manifest(pack_id)
        assert mf.id == pack_id
        assert mf.install_roots
        assert mf.managed_globs
        assert mf.protected_globs


def test_builtin_compound_core_contains_expected_critical_files() -> None:
    files = dict(iter_pack_files("loom-compound-core"))
    assert ".opencode/commands/loom-compound.md" in files
    assert ".claude/commands/loom-compound.md" in files
    assert ".opencode/plugins/compound_engineering.ts" in files
    assert ".omp/extensions/compound_engineering.ts" in files
    assert ".loom/compound/config.json" in files
    assert "AGENTS.md" in files
    assert "LOOM.md" in files


def test_builtin_team_core_contains_expected_critical_files() -> None:
    files = dict(iter_pack_files("loom-team-core"))
    assert ".opencode/agents/loom-team-manager.md" in files
    assert ".opencode/agents/loom-team-worker.md" in files
    assert ".claude/agents/loom-team-manager.md" in files
    assert ".claude/agents/loom-team-worker.md" in files
