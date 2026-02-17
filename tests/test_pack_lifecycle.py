from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_loom.pack.core import (
    doctor,
    install_pack,
    status,
    uninstall_pack,
    update_pack,
)
from agent_loom.pack.lock import LockFileError, load_lock_detail, lock_path
from agent_loom.pack.packs import list_pack_ids, load_manifest
from agent_loom.pack.lock import load_lock
from agent_loom.pack.util import sha256_text


def test_pack_lists_builtin_sample_pack() -> None:
    assert "sample" in list_pack_ids()
    assert "loom-compound-core" in list_pack_ids()
    assert "loom-team-core" in list_pack_ids()
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


def test_pack_install_records_drifted_managed_files_in_lock(tmp_path: Path) -> None:
    repo = tmp_path

    # Pre-create a managed file with conflicting contents before install.
    p = repo / ".opencode" / "commands" / "pack-sample.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("preexisting drift\n", encoding="utf-8")

    res = install_pack(repo_root=repo, pack_id="sample", dry_run=False, force=False)
    assert ".opencode/commands/pack-sample.md" in res.drifted

    lock = load_lock(repo)
    ip = next(p for p in lock.packs if p.id == "sample")
    assert any(e.path == ".opencode/commands/pack-sample.md" for e in ip.files)

    st = status(repo)
    drifted_val = st.get("drifted")
    assert (drifted_val if isinstance(drifted_val, int) else 0) == 1
    doc = doctor(repo, pack_id="sample")
    assert doc.get("ok") is False
    res0 = doc.get("results")
    assert isinstance(res0, list) and res0
    r0 = res0[0]
    assert isinstance(r0, dict)
    drifted = r0.get("drifted")
    assert isinstance(drifted, list)
    assert ".opencode/commands/pack-sample.md" in drifted


def test_pack_update_records_untracked_drifted_managed_files_in_lock(
    tmp_path: Path,
) -> None:
    repo = tmp_path
    install_pack(repo_root=repo, pack_id="sample", dry_run=False)

    # Create drift and then simulate a legacy lock missing the entry.
    rel = ".opencode/commands/pack-sample.md"
    p = repo / rel
    p.write_text("drift\n", encoding="utf-8")

    lp = lock_path(repo)
    doc = json.loads(lp.read_text(encoding="utf-8"))
    packs = doc.get("packs")
    assert isinstance(packs, list)
    for pr in packs:
        if isinstance(pr, dict) and pr.get("id") == "sample":
            files = pr.get("files")
            if isinstance(files, list):
                pr["files"] = [f for f in files if f.get("path") != rel]
    lp.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    res = update_pack(repo_root=repo, pack_id="sample", dry_run=False, force=False)
    assert rel in res.drifted

    lock = load_lock(repo)
    ip = next(p for p in lock.packs if p.id == "sample")
    assert any(e.path == rel for e in ip.files)


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


def test_lockfile_duplicate_entries_are_deduplicated_and_repaired(tmp_path: Path) -> None:
    repo = tmp_path
    lp = lock_path(repo)
    lp.parent.mkdir(parents=True, exist_ok=True)
    sha = sha256_text("x")
    lp.write_text(
        json.dumps(
            {
                "version": 1,
                "packs": [
                    {
                        "id": "sample",
                        "version": "1.0.0",
                        "installed_at": "2026-01-01T00:00:00Z",
                        "files": [
                            {"path": ".opencode/commands/pack-sample.md", "sha256": sha},
                            {"path": ".opencode/commands/pack-sample.md", "sha256": sha},
                        ],
                    },
                    {
                        "id": "sample",
                        "version": "1.0.0",
                        "installed_at": "2026-01-01T00:00:00Z",
                        "files": [
                            {"path": ".opencode/commands/pack-sample.md", "sha256": sha},
                        ],
                    },
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    payload = status(repo)
    warnings = payload.get("warnings")
    assert isinstance(warnings, list)
    assert len(warnings) == 2

    doc = json.loads(lp.read_text(encoding="utf-8"))
    packs = doc.get("packs")
    assert isinstance(packs, list)
    assert len(packs) == 1
    files = packs[0].get("files")
    assert isinstance(files, list)
    assert len(files) == 1


def test_lockfile_conflicting_duplicate_file_entries_fail(tmp_path: Path) -> None:
    repo = tmp_path
    lp = lock_path(repo)
    lp.parent.mkdir(parents=True, exist_ok=True)
    lp.write_text(
        json.dumps(
            {
                "version": 1,
                "packs": [
                    {
                        "id": "sample",
                        "version": "1.0.0",
                        "installed_at": "2026-01-01T00:00:00Z",
                        "files": [
                            {
                                "path": ".opencode/commands/pack-sample.md",
                                "sha256": "a" * 64,
                            },
                            {
                                "path": ".opencode/commands/pack-sample.md",
                                "sha256": "b" * 64,
                            },
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(LockFileError):
        load_lock_detail(repo)


def test_lockfile_conflicting_duplicate_pack_entries_fail(tmp_path: Path) -> None:
    repo = tmp_path
    lp = lock_path(repo)
    lp.parent.mkdir(parents=True, exist_ok=True)
    lp.write_text(
        json.dumps(
            {
                "version": 1,
                "packs": [
                    {
                        "id": "sample",
                        "version": "1.0.0",
                        "installed_at": "2026-01-01T00:00:00Z",
                        "files": [],
                    },
                    {
                        "id": "sample",
                        "version": "2.0.0",
                        "installed_at": "2026-01-01T00:00:00Z",
                        "files": [],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(LockFileError):
        doctor(repo)


def test_lockfile_invalid_file_path_fails_validation(tmp_path: Path) -> None:
    repo = tmp_path
    lp = lock_path(repo)
    lp.parent.mkdir(parents=True, exist_ok=True)
    lp.write_text(
        json.dumps(
            {
                "version": 1,
                "packs": [
                    {
                        "id": "sample",
                        "version": "1.0.0",
                        "installed_at": "2026-01-01T00:00:00Z",
                        "files": [
                            {
                                "path": "../outside.md",
                                "sha256": "a" * 64,
                            }
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(LockFileError):
        load_lock_detail(repo)
