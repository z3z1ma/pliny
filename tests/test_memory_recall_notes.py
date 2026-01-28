import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from agent_loom.memory import cli as memory_cli


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


class TestRecallNotes(unittest.TestCase):
    def test_scope_ranking_is_deterministic(self) -> None:
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
                    "Exact",
                    "--id",
                    "exact",
                    "--scope",
                    "file:docs/memory-notes-v1-spec.md",
                ],
                stdin="alpha\n",
            )
            _run(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "add",
                    "--title",
                    "Folder",
                    "--id",
                    "folder",
                    "--scope",
                    "folder:docs/",
                ],
                stdin="alpha\n",
            )
            _run(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "add",
                    "--title",
                    "Filetype",
                    "--id",
                    "filetype",
                    "--scope",
                    "filetype:md",
                ],
                stdin="alpha\n",
            )

            out = _run(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "recall",
                    "--scope",
                    "file:docs/memory-notes-v1-spec.md",
                    "--limit",
                    "10",
                    "--deterministic",
                ]
            )
            res = json.loads(out)
            self.assertEqual([r["id"] for r in res], ["exact", "folder", "filetype"])
            self.assertTrue(all(float(r["score"]["recency"]) == 0.0 for r in res))


if __name__ == "__main__":
    unittest.main()
