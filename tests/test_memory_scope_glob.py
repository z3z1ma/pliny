import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

from agent_loom.memory import cli as memory_cli


def _run_json(argv: list[str]) -> object:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = memory_cli(argv)
    if rc != 0:
        raise AssertionError(f"memory exited non-zero: {rc}")
    payload = buf.getvalue().strip()
    return json.loads(payload) if payload else {}


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


class TestMemoryScopeGlob(unittest.TestCase):
    def test_recall_scope_file_allows_glob_patterns(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with _Chdir(root):
                # Create a small fake repo tree for file scopes.
                (root / "src" / "agent_loom" / "memory").mkdir(parents=True)
                (root / "src" / "agent_loom" / "pack").mkdir(parents=True)
                (root / "src" / "agent_loom" / "memory" / "a.py").write_text(
                    "a\n", encoding="utf-8"
                )
                (root / "src" / "agent_loom" / "pack" / "b.py").write_text(
                    "b\n", encoding="utf-8"
                )

                vault = root / ".loom" / "memory"
                _run_json(["--vault", str(vault), "--format", "json", "init"])

                _run_json(
                    [
                        "--vault",
                        str(vault),
                        "--format",
                        "json",
                        "add",
                        "--id",
                        "note-a",
                        "--title",
                        "A",
                        "--scope",
                        "file:src/agent_loom/memory/a.py",
                        "--body",
                        "alpha\n",
                    ]
                )
                _run_json(
                    [
                        "--vault",
                        str(vault),
                        "--format",
                        "json",
                        "add",
                        "--id",
                        "note-b",
                        "--title",
                        "B",
                        "--scope",
                        "file:src/agent_loom/pack/b.py",
                        "--body",
                        "bravo\n",
                    ]
                )

                out = _run_json(
                    [
                        "--vault",
                        str(vault),
                        "--format",
                        "json",
                        "recall",
                        "",
                        "--scope",
                        "file:src/agent_loom/memory/*.py",
                        "--limit",
                        "1",
                        "--deterministic",
                    ]
                )
                assert isinstance(out, list)
                ids = [str(it.get("id") or "") for it in out if isinstance(it, dict)]
                self.assertEqual(ids, ["note-a"])


if __name__ == "__main__":
    unittest.main()
