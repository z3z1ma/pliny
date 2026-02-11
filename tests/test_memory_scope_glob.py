import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

from agent_loom.memory import cli as memory_cli


def _run_json_with_rc(argv: list[str]) -> tuple[int, object]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = memory_cli(argv)
    payload = buf.getvalue().strip()
    return rc, (json.loads(payload) if payload else {})


def _run_json(argv: list[str]) -> object:
    rc, payload = _run_json_with_rc(argv)
    if rc != 0:
        raise AssertionError(f"memory exited non-zero: {rc}")
    return payload


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

    def test_unknown_scope_kind_in_note_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with _Chdir(root):
                (root / "src" / "agent_loom" / "memory").mkdir(parents=True)
                (root / "src" / "agent_loom" / "memory" / "a.py").write_text(
                    "a\n", encoding="utf-8"
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

                legacy_note = (
                    "---\n"
                    "id: unknown-scope\n"
                    "title: Unknown scope\n"
                    "created_at: 2026-01-01T00:00:00Z\n"
                    "updated_at: 2026-01-01T00:00:00Z\n"
                    "scopes:\n"
                    "  - kind: glob\n"
                    "    raw: src/agent_loom/memory/*.py\n"
                    "---\n\n"
                    "unknown\n"
                )
                (vault / "notes" / "unknown-scope.md").write_text(
                    legacy_note,
                    encoding="utf-8",
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
                        "file:src/agent_loom/memory/a.py",
                        "--scoped-only",
                        "--deterministic",
                    ]
                )
                assert isinstance(out, list)
                ids = [str(it.get("id") or "") for it in out if isinstance(it, dict)]
                self.assertEqual(ids, ["note-a"])

    def test_unknown_scope_kind_in_context_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with _Chdir(root):
                (root / "src").mkdir(parents=True)
                (root / "src" / "a.py").write_text("a\n", encoding="utf-8")

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
                        "--body",
                        "alpha\n",
                    ]
                )

                rc, payload = _run_json_with_rc(
                    [
                        "--vault",
                        str(vault),
                        "--format",
                        "json",
                        "recall",
                        "",
                        "--scope",
                        "glob:src/**/*.py",
                    ]
                )
                self.assertEqual(rc, 0)
                assert isinstance(payload, list)
                ids = [
                    str(it.get("id") or "") for it in payload if isinstance(it, dict)
                ]
                self.assertEqual(ids, ["note-a"])


if __name__ == "__main__":
    unittest.main()
