from __future__ import annotations

import json
from pathlib import Path

from agent_loom.pack.core import install_pack, uninstall_pack, update_pack
from agent_loom.pack.lock import lock_path
from agent_loom.pack.packs import list_pack_ids, load_manifest


def test_pack_lists_builtin_sample_pack() -> None:
    assert "sample" in list_pack_ids()
    mf = load_manifest("sample")
    assert mf.id == "sample"


def test_pack_install_writes_files_and_lock(tmp_path: Path) -> None:
    repo = tmp_path
    res = install_pack(repo_root=repo, pack_id="sample", dry_run=False)
    assert res.ok is True
    assert (repo / ".opencode" / "commands" / "pack-sample.md").exists()

    lp = lock_path(repo)
    assert lp.exists()
    doc = json.loads(lp.read_text(encoding="utf-8"))
    assert doc["version"] == 1
    assert any(p["id"] == "sample" for p in doc["packs"])


def test_pack_install_loom_agile_core_pack(tmp_path: Path) -> None:
    repo = tmp_path
    res = install_pack(repo_root=repo, pack_id="loom-agile-core", dry_run=False)
    assert res.ok is True
    assert (repo / ".opencode" / "commands" / "loom-agile-help.md").exists()
    assert (repo / ".opencode" / "agents" / "loom-agile-developer.md").exists()


def test_pack_update_respects_drift_without_force(tmp_path: Path) -> None:
    repo = tmp_path
    install_pack(repo_root=repo, pack_id="sample", dry_run=False)

    p = repo / ".opencode" / "commands" / "pack-sample.md"
    p.write_text("drift\n", encoding="utf-8")

    res = update_pack(repo_root=repo, pack_id="sample", dry_run=False, force=False)
    assert p.read_text(encoding="utf-8") == "drift\n"
    assert ".opencode/commands/pack-sample.md" in res.drifted
    assert ".opencode/commands/pack-sample.md" in res.skipped


def test_pack_update_overwrites_drift_with_force(tmp_path: Path) -> None:
    repo = tmp_path
    install_pack(repo_root=repo, pack_id="sample", dry_run=False)

    p = repo / ".opencode" / "commands" / "pack-sample.md"
    p.write_text("drift\n", encoding="utf-8")

    res = update_pack(repo_root=repo, pack_id="sample", dry_run=False, force=True)
    assert "drift" not in p.read_text(encoding="utf-8")
    assert ".opencode/commands/pack-sample.md" in res.drifted
    assert ".opencode/commands/pack-sample.md" in res.wrote


def test_pack_uninstall_keeps_drift_without_force(tmp_path: Path) -> None:
    repo = tmp_path
    install_pack(repo_root=repo, pack_id="sample", dry_run=False)

    p = repo / ".opencode" / "commands" / "pack-sample.md"
    p.write_text("drift\n", encoding="utf-8")

    res = uninstall_pack(repo_root=repo, pack_id="sample", dry_run=False, force=False)
    assert p.exists()
    assert ".opencode/commands/pack-sample.md" in res.drifted
    assert ".opencode/commands/pack-sample.md" in res.skipped


def test_pack_uninstall_removes_drift_with_force(tmp_path: Path) -> None:
    repo = tmp_path
    install_pack(repo_root=repo, pack_id="sample", dry_run=False)

    p = repo / ".opencode" / "commands" / "pack-sample.md"
    p.write_text("drift\n", encoding="utf-8")

    res = uninstall_pack(repo_root=repo, pack_id="sample", dry_run=False, force=True)
    assert not p.exists()
    assert ".opencode/commands/pack-sample.md" in res.removed
    assert (repo / ".loom" / "pack" / "lock.json").exists()
