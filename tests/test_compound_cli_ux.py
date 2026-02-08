import contextlib
import importlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from collections.abc import Iterator
from pathlib import Path
from typing import Callable, cast


compound_mod = importlib.import_module("agent_loom.compound.cli")
compound_cli = cast(Callable[[list[str]], int], getattr(compound_mod, "main"))


def _run_text(argv: list[str], *, cwd: Path) -> tuple[int, str, str]:
    out = io.StringIO()
    err = io.StringIO()
    old = Path.cwd()
    try:
        os.chdir(cwd)
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = int(compound_cli(argv))
    finally:
        os.chdir(old)
    return rc, out.getvalue(), err.getvalue()


def _run_json(argv: list[str], *, cwd: Path) -> tuple[int, dict]:
    rc, out, _err = _run_text(argv, cwd=cwd)
    payload = out.strip()
    return rc, (json.loads(payload) if payload else {})


def _git(args: list[str], *, cwd: Path, env: dict[str, str]) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), env=env, check=True)


@contextlib.contextmanager
def _git_identity_env() -> Iterator[None]:
    before = os.environ.copy()
    os.environ.update(
        {
            "GIT_AUTHOR_NAME": "Test",
            "GIT_AUTHOR_EMAIL": "test@example.com",
            "GIT_COMMITTER_NAME": "Test",
            "GIT_COMMITTER_EMAIL": "test@example.com",
        }
    )
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(before)


class TestCompoundCliUx(unittest.TestCase):
    def test_help_lists_only_expected_commands(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            rc, out, err = _run_text(["-h"], cwd=Path(td))
        self.assertEqual(rc, 0)
        self.assertTrue(out.strip() or err.strip())
        text = (out + "\n" + err).lower()

        for cmd in ["init", "update", "learn", "sync", "prime"]:
            self.assertIn(cmd, text)

        self.assertIn("{init,sync,update,learn,prime}", text)

        # Deleted surface area should not be discoverable.
        for gone in [
            "refresh",
            "run",
            "status",
            "doctor",
            "rebuild",
            "observations",
            "triage",
            "replay",
            "instinct",
            "docblock",
            "changelog",
        ]:
            self.assertNotIn(gone, text)

    def test_prime_prints_cookbook(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            rc, out, _err = _run_text(["prime"], cwd=Path(td))
        self.assertEqual(rc, 0)
        self.assertIn("Compound Cookbook", out)
        self.assertIn("loom compound init", out)

    def test_removed_command_is_structured_json_error(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            rc, payload = _run_json(["rebuild", "--json"], cwd=Path(td))
        self.assertEqual(rc, 2)
        self.assertFalse(bool(payload.get("ok")))
        self.assertEqual(str(payload.get("code") or ""), "ARGPARSE")
        self.assertTrue(str(payload.get("hint") or ""))

    def test_init_update_learn_sync_json_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "repo"
            root.mkdir(parents=True, exist_ok=True)

            with _git_identity_env():
                env = os.environ.copy()
                # Git repo with an initial commit (learn requires HEAD).
                _git(["init", "-b", "main"], cwd=root, env=env)
                (root / "README.txt").write_text("hi\n", encoding="utf-8")
                _git(["add", "-A"], cwd=root, env=env)
                _git(["commit", "-m", "init"], cwd=root, env=env)

                # init
                rc0, p0 = _run_json(["init", "--dest", str(root), "--json"], cwd=root)
                self.assertEqual(rc0, 0)
                self.assertTrue(bool(p0.get("ok")))
                self.assertTrue(str(p0.get("dest") or ""))

                # update
                rc1, p1 = _run_json(["update", "--repo", str(root), "--json"], cwd=root)
                self.assertEqual(rc1, 0)
                self.assertTrue(bool(p1.get("ok")))

                # create some observations + a diff so the Episode has evidence
                obs = root / ".opencode" / "memory" / "observations.jsonl"
                obs.parent.mkdir(parents=True, exist_ok=True)
                obs.write_text(
                    '{"id":"1","ts":"2026-02-07T00:00:00Z","type":"x"}\n',
                    encoding="utf-8",
                )
                (root / "demo.txt").write_text("hello\n", encoding="utf-8")
                _git(["add", "-N", "demo.txt"], cwd=root, env=env)

                # learn
                rc2, p2 = _run_json(
                    [
                        "learn",
                        "--repo",
                        str(root),
                        "--proposals",
                        "{}",
                        "--json",
                    ],
                    cwd=root,
                )
                self.assertEqual(rc2, 0)
                self.assertTrue(bool(p2.get("ok")))
                self.assertTrue(str(p2.get("episode_id") or ""))
                self.assertTrue(str(p2.get("episode_path") or ""))

                # sync (commit compound-owned paths)
                ctx = root / "LOOM.md"
                ctx.write_text(
                    ctx.read_text(encoding="utf-8") + "\n# touched\n",
                    encoding="utf-8",
                )
                rc3, p3 = _run_json(
                    ["sync", "--repo", str(root), "--json", "-m", "chore: compound"],
                    cwd=root,
                )
                self.assertEqual(rc3, 0)
                self.assertTrue(bool(p3.get("ok")))
                # committed may be False if nothing changed; accept either but require shape.
                self.assertIn("committed", p3)


if __name__ == "__main__":
    unittest.main()
