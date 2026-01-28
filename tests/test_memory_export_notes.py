import contextlib
import io
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


class TestContextPack(unittest.TestCase):
    def test_context_pack_is_stable_and_includes_neighbor_distance(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / ".memory"
            _run(["--vault", str(vault), "init"])

            # a -> b (resolved wikilink)
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
                stdin="B body\n",
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
                stdin="Link to [[b]]\n",
            )

            def run_export() -> str:
                return _run(
                    [
                        "--vault",
                        str(vault),
                        "--format",
                        "text",
                        "recall",
                        "Link",
                        "--context",
                        "--expand",
                        "1",
                        "--max-chars",
                        "99999",
                        "--deterministic",
                    ]
                )

            out1 = run_export()
            out2 = run_export()
            self.assertEqual(out1, out2)

            # Deterministic export header omits generated_at
            self.assertIn("<!-- memory:", out1)
            self.assertNotIn("generated_at", out1)

            # Neighbor included with graph_distance.
            self.assertIn("## B  (`b`)", out1)
            self.assertIn("- graph_distance: 1", out1)


if __name__ == "__main__":
    unittest.main()
