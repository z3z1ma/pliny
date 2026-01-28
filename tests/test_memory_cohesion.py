import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
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


class TestMemoryCohesion(unittest.TestCase):
    def test_init_gitignore_is_additive(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / ".memory"
            vault.mkdir(parents=True, exist_ok=True)
            (vault / ".gitignore").write_text("keep/\n", encoding="utf-8")

            _run(["--vault", str(vault), "init"])

            got = (vault / ".gitignore").read_text(encoding="utf-8")
            self.assertIn("keep/\n", got)
            self.assertIn("index.sqlite3", got)
            self.assertIn("personal/", got)

    def test_link_parser_ignores_fenced_code_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / ".memory"
            _run(["--vault", str(vault), "init"])

            _run(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "add",
                    "--title",
                    "B",
                    "--id",
                    "b",
                ],
                stdin="b body\n",
            )

            _run(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "add",
                    "--title",
                    "A",
                    "--id",
                    "a",
                ],
                stdin="```\n[[b]]\n```\n",
            )

            out = _run(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "link",
                    "backlinks",
                    "b",
                ]
            )
            backlinks = json.loads(out)
            self.assertEqual(backlinks, [])

    def test_janitor_reports_and_fixes_stale_file_scopes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            with _Chdir(td_path):
                vault = td_path / ".memory"
                _run(["--vault", str(vault), "init"])

                (td_path / "src").mkdir(parents=True, exist_ok=True)
                f = td_path / "src" / "alive.txt"
                f.write_text("hi\n", encoding="utf-8")

                _run(
                    [
                        "--vault",
                        str(vault),
                        "--format",
                        "json",
                        "add",
                        "--title",
                        "Has file scope",
                        "--id",
                        "has-scope",
                        "--scope",
                        "file:src/alive.txt",
                        "--body",
                        "Body",
                    ]
                )

                f.unlink()

                out = _run(
                    [
                        "--vault",
                        str(vault),
                        "--format",
                        "json",
                        "janitor",
                        "report",
                    ]
                )
                rep = json.loads(out)
                self.assertEqual(rep.get("count"), 1)
                self.assertEqual(rep["notes"][0]["id"], "has-scope")

                out2 = _run(
                    [
                        "--vault",
                        str(vault),
                        "--format",
                        "json",
                        "janitor",
                        "fix",
                    ]
                )
                dry = json.loads(out2)
                self.assertTrue(dry.get("dry_run"))

                out3 = _run(
                    [
                        "--vault",
                        str(vault),
                        "--format",
                        "json",
                        "janitor",
                        "fix",
                        "--apply",
                    ]
                )
                applied = json.loads(out3)
                self.assertEqual(applied.get("updated_notes"), 1)

            vp = memory_vault.vault_paths(vault)
            n = memory_vault.read_note(vp, "has-scope")
            self.assertEqual([s["kind"] for s in n.scopes], [])

    def test_wikilink_path_resolves_by_basename(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            with _Chdir(td_path):
                vault = td_path / ".memory"
                _run(["--vault", str(vault), "init"])

                _run(
                    [
                        "--vault",
                        str(vault),
                        "--format",
                        "json",
                        "add",
                        "--title",
                        "B",
                        "--id",
                        "b",
                        "--body",
                        "b body",
                    ]
                )
                _run(
                    [
                        "--vault",
                        str(vault),
                        "--format",
                        "json",
                        "add",
                        "--title",
                        "A",
                        "--id",
                        "a",
                        "--body",
                        "Link [[notes/x/b]]",
                    ]
                )

                out = _run(
                    [
                        "--vault",
                        str(vault),
                        "--format",
                        "json",
                        "link",
                        "backlinks",
                        "b",
                    ]
                )
                backlinks = json.loads(out)
                self.assertEqual([x["id"] for x in backlinks], ["a"])


if __name__ == "__main__":
    unittest.main()
