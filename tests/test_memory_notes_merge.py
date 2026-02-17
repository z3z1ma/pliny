import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from agent_loom.memory import core as memory_core
from agent_loom.memory import vault as memory_vault
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

            # Default recall includes shared+personal.
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
            res = json.loads(out)
            self.assertEqual([r["id"] for r in res], ["secret"])

            # Explicitly restrict to shared to hide personal notes.
            out_shared = _run(
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
                    "shared",
                    "--deterministic",
                ]
            )
            self.assertEqual(json.loads(out_shared), [])

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

    def test_edit_warns_when_implicit_visibility_move_conflicts(self) -> None:
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
                    "Mismatch",
                    "--id",
                    "mismatch",
                ],
                stdin="body\n",
            )

            vp = memory_vault.vault_paths(vault)
            shared_path = vp.notes_dir / "mismatch.md"
            conflict_path = vault / "personal" / "notes" / "mismatch.md"
            conflict_path.parent.mkdir(parents=True, exist_ok=True)
            conflict_path.write_text(
                (
                    "---\n"
                    "id: conflict-note\n"
                    "title: Conflict\n"
                    "visibility: personal\n"
                    "status: active\n"
                    "created_at: 2026-01-01T00:00:00Z\n"
                    "updated_at: 2026-01-01T00:00:00Z\n"
                    "---\n"
                    "conflict\n"
                ),
                "utf-8",
            )

            new_path, moved, warning = memory_core._move_note_for_visibility(
                vp=vp,
                note_id="mismatch",
                note_path=shared_path,
                note_rel=memory_vault.note_rel_path(vp, shared_path),
                target_base=vp.personal_notes_dir,
                explicit_visibility_change=False,
            )
            self.assertEqual(new_path, shared_path)
            self.assertFalse(moved)
            self.assertIsNotNone(warning)
            assert warning is not None
            self.assertIn("note move skipped", warning)
            self.assertIn("destination already exists", warning)

    def test_edit_visibility_change_errors_on_destination_conflict(self) -> None:
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
                    "Secret",
                    "--id",
                    "secret",
                ],
                stdin="body\n",
            )

            conflict_path = vault / "personal" / "notes" / "secret.md"
            conflict_path.parent.mkdir(parents=True, exist_ok=True)
            conflict_path.write_text(
                (
                    "---\n"
                    "id: conflict-note\n"
                    "title: Conflict\n"
                    "visibility: personal\n"
                    "status: active\n"
                    "created_at: 2026-01-01T00:00:00Z\n"
                    "updated_at: 2026-01-01T00:00:00Z\n"
                    "---\n"
                    "conflict\n"
                ),
                "utf-8",
            )

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = memory_cli(
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
            self.assertEqual(rc, 2)
            payload = json.loads(buf.getvalue())
            self.assertFalse(payload.get("ok"))
            self.assertEqual(payload.get("code"), "CONFLICT")


if __name__ == "__main__":
    unittest.main()
