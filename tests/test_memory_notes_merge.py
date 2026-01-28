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


class TestVisibilityMoves(unittest.TestCase):
    def test_edit_visibility_moves_and_recall_filters(self) -> None:
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
                    "Secret",
                    "--id",
                    "secret",
                ],
                stdin="sensitive\n",
            )

            # Move to personal.
            _run(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "edit",
                    "secret",
                    "--visibility",
                    "personal",
                ]
            )

            # Default recall only includes shared.
            out = _run(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "recall",
                    "sensitive",
                    "--limit",
                    "10",
                    "--deterministic",
                ]
            )
            self.assertEqual(json.loads(out), [])

            out2 = _run(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "recall",
                    "sensitive",
                    "--limit",
                    "10",
                    "--visibility",
                    "personal",
                    "--deterministic",
                ]
            )
            res2 = json.loads(out2)
            self.assertEqual([r["id"] for r in res2], ["secret"])


if __name__ == "__main__":
    unittest.main()
