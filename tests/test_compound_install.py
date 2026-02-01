from __future__ import annotations

from importlib import resources
from pathlib import Path

from agent_loom.compound.install import install_opencode


def _template_text(*parts: str) -> str:
    traversable = resources.files("agent_loom.compound").joinpath("opencode", *parts)
    with resources.as_file(traversable) as p:
        return Path(p).read_text(encoding="utf-8")


def test_compound_install_does_not_overwrite_scaffold_without_force(
    tmp_path: Path,
) -> None:
    dest = tmp_path
    dest.mkdir(parents=True, exist_ok=True)

    plugin_path = dest / ".opencode" / "plugins" / "compound_engineering.ts"
    plugin_path.parent.mkdir(parents=True, exist_ok=True)
    plugin_path.write_text("// old\n", encoding="utf-8")

    res = install_opencode(dest=dest, dry_run=False)
    assert res.dest == str(dest.resolve())
    actual = plugin_path.read_text(encoding="utf-8")
    assert actual == "// old\n"


def test_compound_install_overwrites_scaffold_with_force(tmp_path: Path) -> None:
    dest = tmp_path
    dest.mkdir(parents=True, exist_ok=True)

    plugin_path = dest / ".opencode" / "plugins" / "compound_engineering.ts"
    plugin_path.parent.mkdir(parents=True, exist_ok=True)
    plugin_path.write_text("// old\n", encoding="utf-8")

    install_opencode(dest=dest, dry_run=False, force=True)
    expected = _template_text(".opencode", "plugins", "compound_engineering.ts")
    actual = plugin_path.read_text(encoding="utf-8")
    assert actual == expected


def test_compound_install_patches_agents_md_without_clobbering(tmp_path: Path) -> None:
    dest = tmp_path
    agents = dest / "AGENTS.md"
    agents.write_text("# AGENTS\n\nhello\n", encoding="utf-8")

    install_opencode(dest=dest, dry_run=False)
    new = agents.read_text(encoding="utf-8")
    assert "hello" in new

    required = [
        "agents-ai-behavior",
        "workflow-commands",
        "loom-core-context",
        "instincts-index",
        "rules-index",
    ]
    for ident in required:
        assert f"<!-- BEGIN:compound:{ident} -->" in new
        assert f"<!-- END:compound:{ident} -->" in new


def test_compound_install_creates_loom_docs_if_missing(tmp_path: Path) -> None:
    dest = tmp_path
    install_opencode(dest=dest, dry_run=False)

    assert (dest / "LOOM_ROADMAP.md").exists()
    assert not (dest / "LOOM_PROJECT.md").exists()
    assert not (dest / "LOOM_CHANGELOG.md").exists()


def test_compound_install_template_uses_compoundspec_v2(tmp_path: Path) -> None:
    dest = tmp_path
    install_opencode(dest=dest, dry_run=False)

    skill = dest / ".opencode" / "skills" / "compound-apply-spec" / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    assert "schema_version" in text
    assert "CompoundSpec v1" not in text


def test_compound_install_dry_run_does_not_write_files(tmp_path: Path) -> None:
    dest = tmp_path
    res = install_opencode(dest=dest, dry_run=True)

    assert res.dry_run is True
    assert not (dest / ".opencode").exists()
    assert not (dest / "LOOM_ROADMAP.md").exists()
    assert not (dest / "AGENTS.md").exists()

    assert any(
        p.endswith(".opencode/plugins/compound_engineering.ts") for p in res.wrote
    )


def test_compound_install_ensures_loom_doc_fences(tmp_path: Path) -> None:
    dest = tmp_path
    p = dest / "LOOM_ROADMAP.md"
    p.write_text("# LOOM_ROADMAP\n", encoding="utf-8")

    install_opencode(dest=dest, dry_run=False)
    text = p.read_text(encoding="utf-8")
    assert "<!-- BEGIN:compound:roadmap-backlog -->" in text
    assert "<!-- END:compound:roadmap-backlog -->" in text
    assert "<!-- BEGIN:compound:roadmap-ai-notes -->" in text
    assert "<!-- END:compound:roadmap-ai-notes -->" in text
    assert "<!-- BEGIN:compound:changelog-entries -->" in text
    assert "<!-- END:compound:changelog-entries -->" in text


def test_compound_install_never_overwrites_instincts_store(tmp_path: Path) -> None:
    dest = tmp_path
    install_opencode(dest=dest, dry_run=False)

    instincts = dest / ".opencode" / "memory" / "instincts.json"
    instincts.write_text(
        '{"version": 1, "instincts": [{"id": "x"}]}\n', encoding="utf-8"
    )

    install_opencode(dest=dest, dry_run=False, force=True)
    assert '"id": "x"' in instincts.read_text(encoding="utf-8")
