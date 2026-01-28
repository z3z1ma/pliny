import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
import sys
import os

from agent_loom.memory import cli as memory_cli
from agent_loom.memory import vault as memory_vault


def _run(argv: list[str], *, stdin: str | None = None) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        if stdin is None:
            rc = memory_cli(argv)
        else:
            old_stdin = sys.stdin
            try:
                sys.stdin = io.StringIO(stdin)
                rc = memory_cli(argv)
            finally:
                sys.stdin = old_stdin
    if rc != 0:
        raise AssertionError(f"memory exited non-zero: {rc}")
    return buf.getvalue()


class _Chdir:
    def __init__(self, p: Path):
        self.p = p
        self._old: str | None = None

    def __enter__(self) -> None:
        self._old = os.getcwd()
        os.chdir(str(self.p))

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._old is not None:
            os.chdir(self._old)


class TestMemoryNotes(unittest.TestCase):
    def test_init_add_read_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / ".memory"

            _run(["--vault", str(vault), "init"])

            out = _run(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "add",
                    "--title",
                    "Hello",
                    "--id",
                    "hello",
                ],
                stdin="Body\n",
            )
            created = json.loads(out)
            self.assertTrue(created.get("ok"))
            self.assertEqual(created.get("id"), "hello")
            self.assertIn("links", created)
            self.assertIn("summary", created.get("links") or {})

            vp = memory_vault.vault_paths(vault)
            n = memory_vault.read_note(vp, "hello")
            self.assertEqual(n.id, "hello")
            self.assertEqual(n.title, "Hello")
            self.assertEqual(n.body.strip(), "Body")
            self.assertEqual(n.visibility, "shared")

            # Non-git safety: init writes a vault-local .gitignore.
            gi = (vault / ".gitignore").read_text("utf-8")
            self.assertIn("index.sqlite3", gi)
            self.assertIn("personal/", gi)

    def test_prime_exists(self) -> None:
        out = _run(["prime"])
        payload = json.loads(out)
        self.assertTrue(payload.get("ok"))
        self.assertIn("schema_version", payload)

    def test_add_rejects_missing_file_scope_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            with _Chdir(td_path):
                vault = td_path / ".memory"
                _run(["--vault", str(vault), "init"])

                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = memory_cli(
                        [
                            "--vault",
                            str(vault),
                            "--format",
                            "json",
                            "add",
                            "--title",
                            "X",
                            "--scope",
                            "file:does_not_exist.txt",
                            "--body",
                            "Body",
                        ]
                    )
                self.assertEqual(rc, 2)
                payload = json.loads(buf.getvalue())
                self.assertFalse(payload.get("ok"))
                self.assertEqual(payload.get("code"), "NOT_FOUND")
                self.assertTrue(str(payload.get("hint") or ""))


if __name__ == "__main__":
    unittest.main()
