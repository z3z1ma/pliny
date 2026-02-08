from __future__ import annotations

import contextlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

from agent_loom.compound.engine import run_compound
from agent_loom.compound.install import install_opencode
from agent_loom.compound.paths import compound_paths


def _git(args: list[str], *, cwd: Path, env: dict[str, str], check: bool = True) -> str:
    p = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=check,
    )
    return (p.stdout or "").strip()


@contextlib.contextmanager
def _temp_git_repo():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        env = os.environ.copy()
        env.update(
            {
                "GIT_AUTHOR_NAME": "Test",
                "GIT_AUTHOR_EMAIL": "test@example.com",
                "GIT_COMMITTER_NAME": "Test",
                "GIT_COMMITTER_EMAIL": "test@example.com",
            }
        )
        _git(["init"], cwd=root, env=env)
        yield root, env


def test_compound_run_writes_episode_and_applies_proposals() -> None:
    with _temp_git_repo() as (root, env):
        install_opencode(dest=root, dry_run=False)
        _git(["add", "-A"], cwd=root, env=env)
        _git(["commit", "-m", "init"], cwd=root, env=env)

        paths = compound_paths(root)
        paths.observations_file.parent.mkdir(parents=True, exist_ok=True)
        paths.observations_file.write_text(
            "\n".join(
                [
                    json.dumps(
                        {
                            "id": "1",
                            "ts": "2026-02-07T00:00:00Z",
                            "type": "tool.execute.after",
                        }
                    ),
                    json.dumps(
                        {
                            "id": "2",
                            "ts": "2026-02-07T00:01:00Z",
                            "type": "command.executed",
                        }
                    ),
                    "",
                ]
            ),
            encoding="utf-8",
        )

        # Create a diff so the Episode has concrete evidence.
        (root / "demo.txt").write_text("hello\n", encoding="utf-8")

        proposals = {
            "instinct_candidates": [
                {
                    "id": "keep-commands-safe",
                    "title": "Keep shell commands safe",
                    "trigger": "When running shell commands in automation",
                    "action": "Prefer scoped, non-destructive commands and avoid force ops",
                    "confidence": 0.8,
                    "tags": ["safety"],
                }
            ],
            "skill_candidates": [
                {
                    "name": "compound-episode-workflow",
                    "description": "Package evidence into episodes and compile memory",
                    "body": "## Steps\n\n- Run `loom compound learn` with structured proposals.\n- Verify instincts/skills outputs are updated deterministically.\n",
                    "tags": ["compound"],
                    "source_instinct_ids": ["keep-commands-safe"],
                }
            ],
        }

        res = run_compound(root=root, proposals_json=json.dumps(proposals), auto=False)
        assert res.ok is True
        assert res.episode_id
        assert Path(res.episode_path).exists()
        assert (root / ".loom" / "compound" / "episodes").exists()

        assert res.decision_id
        assert res.decision_path
        assert Path(res.decision_path).exists()

        instincts_path = root / ".loom" / "compound" / "instincts.json"
        assert instincts_path.exists()
        store = json.loads(instincts_path.read_text(encoding="utf-8"))
        ids = [i.get("id") for i in store.get("instincts", [])]
        assert "keep-commands-safe" in ids

        skill_path = (
            root / ".opencode" / "skills" / "compound-episode-workflow" / "SKILL.md"
        )
        assert skill_path.exists()
        text = skill_path.read_text(encoding="utf-8")
        assert "source_episode_ids" in text
        assert res.episode_id in text

        before_instincts = instincts_path.read_text(encoding="utf-8")
        before_skill = skill_path.read_text(encoding="utf-8")

        # No accidental churn.
        assert instincts_path.read_text(encoding="utf-8") == before_instincts
        assert skill_path.read_text(encoding="utf-8") == before_skill


def test_compound_run_handles_observation_rotation_without_reingesting() -> None:
    from agent_loom.compound.episodes import load_episode

    with _temp_git_repo() as (root, env):
        install_opencode(dest=root, dry_run=False)
        _git(["add", "-A"], cwd=root, env=env)
        _git(["commit", "-m", "init"], cwd=root, env=env)

        paths = compound_paths(root)
        paths.observations_file.parent.mkdir(parents=True, exist_ok=True)
        paths.observations_file.write_text(
            "\n".join(
                [
                    json.dumps({"id": "1", "ts": "2026-02-07T00:00:00Z", "type": "x"}),
                    json.dumps({"id": "2", "ts": "2026-02-07T00:01:00Z", "type": "y"}),
                    "",
                ]
            ),
            encoding="utf-8",
        )

        (root / "demo.txt").write_text("hello\n", encoding="utf-8")

        r1 = run_compound(root=root, proposals_json="{}", auto=False)
        assert r1.ok is True
        ep1 = load_episode(Path(r1.episode_path))
        ids1 = [
            str(o.get("id")) for o in ep1.observations.included if isinstance(o, dict)
        ]
        assert "1" in ids1
        assert "2" in ids1

        # Simulate rotation/truncation: new file is smaller than the previous cursor offset.
        rotated = paths.observations_file.with_name(
            paths.observations_file.name + ".bak"
        )
        paths.observations_file.rename(rotated)
        paths.observations_file.write_text(
            json.dumps({"id": "3", "ts": "2026-02-07T00:02:00Z", "type": "z"}) + "\n",
            encoding="utf-8",
        )

        r2 = run_compound(root=root, proposals_json="{}", auto=False)
        assert r2.ok is True
        ep2 = load_episode(Path(r2.episode_path))
        ids2 = [
            str(o.get("id")) for o in ep2.observations.included if isinstance(o, dict)
        ]
        assert ids2 == ["3"]
        assert ep2.observations.cursor.reset_detected is True


def test_compound_run_persists_full_patch_blob_when_truncated() -> None:
    from agent_loom.compound.episodes import load_episode

    with _temp_git_repo() as (root, env):
        install_opencode(dest=root, dry_run=False)
        _git(["add", "-A"], cwd=root, env=env)
        _git(["commit", "-m", "init"], cwd=root, env=env)

        paths = compound_paths(root)
        paths.observations_file.parent.mkdir(parents=True, exist_ok=True)
        paths.observations_file.write_text(
            json.dumps({"id": "1", "ts": "2026-02-07T00:00:00Z", "type": "x"}) + "\n",
            encoding="utf-8",
        )

        big = "\n".join([f"line {i}" for i in range(0, 20000)]) + "\n"
        (root / "big.txt").write_text(big, encoding="utf-8")
        # Ensure `git diff` includes the new file (untracked files aren't included by default).
        _git(["add", "-N", "big.txt"], cwd=root, env=env)

        res = run_compound(
            root=root,
            proposals_json="{}",
            auto=False,
            max_patch_bytes=2000,
        )
        assert res.ok is True
        ep = load_episode(Path(res.episode_path))
        assert ep.git.patch_omitted is True
        assert ep.git.patch == ""
        assert ep.git.patch_sha256
        assert ep.git.patch_blob_sha256

        blob = (
            root / ".loom" / "compound" / "blobs" / f"{ep.git.patch_blob_sha256}.diff"
        )
        assert blob.exists()
        txt = blob.read_text(encoding="utf-8")
        assert "diff --git" in txt
