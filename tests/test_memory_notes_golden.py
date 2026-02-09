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


class TestFormats(unittest.TestCase):
    def test_recall_format_md(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / ".loom" / "memory"
            _run(["--vault", str(vault), "init"])

            _run(
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

            out = _run(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "md",
                    "recall",
                    "Body",
                    "--limit",
                    "10",
                    "--deterministic",
                ]
            )
            self.assertIn("- [[hello]]", out)

    def test_link_validate_format_md(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / ".loom" / "memory"
            _run(["--vault", str(vault), "init"])

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
                stdin="Missing link [[nope]]\n",
            )

            out = _run(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "md",
                    "link",
                    "validate",
                ]
            )
            # Wikilink hydration auto-creates stubs, so this is no longer missing.
            self.assertEqual(out.strip(), "")


if __name__ == "__main__":
    unittest.main()
