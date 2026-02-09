import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from agent_loom.memory import cli as memory_cli
from agent_loom.memory import vault as memory_vault


def _run_json(argv: list[str]) -> dict:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = memory_cli(argv)
    if rc != 0:
        raise AssertionError(f"memory exited non-zero: {rc}")
    payload = buf.getvalue().strip()
    return json.loads(payload) if payload else {}


class TestMemoryLinkHydration(unittest.TestCase):
    def test_add_creates_stub_and_rewrites_wikilink(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / ".loom" / "memory"
            _run_json(["--vault", str(vault), "--format", "json", "init"])

            created = _run_json(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "add",
                    "--id",
                    "a",
                    "--title",
                    "A",
                    "--body",
                    "I like [[Python]] so much\n",
                ]
            )
            hyd = dict(created.get("hydration") or {})
            created_notes = list(hyd.get("created_notes") or [])
            self.assertEqual(len(created_notes), 1)
            py_id = str(created_notes[0].get("id") or "")
            self.assertTrue(py_id)
            self.assertIn("python", py_id)

            # Source note rewritten.
            a_path = vault / "notes" / "a.md"
            self.assertTrue(a_path.exists())
            a_text = a_path.read_text("utf-8", errors="replace")
            self.assertIn(f"[[{py_id}|Python]]", a_text)

            # Stub note exists and is readable.
            vp = memory_vault.vault_paths(vault)
            py_note = memory_vault.read_note(vp, py_id)
            self.assertEqual(py_note.title, "Python")

    def test_add_reuses_existing_stub(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / ".loom" / "memory"
            _run_json(["--vault", str(vault), "--format", "json", "init"])

            created1 = _run_json(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "add",
                    "--id",
                    "a",
                    "--title",
                    "A",
                    "--body",
                    "First [[Python]]\n",
                ]
            )
            py_id = str(
                ((created1.get("hydration") or {}).get("created_notes") or [{}])[0].get(
                    "id"
                )
                or ""
            )
            self.assertTrue(py_id)

            created2 = _run_json(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "add",
                    "--id",
                    "b",
                    "--title",
                    "B",
                    "--body",
                    "Second [[Python]]\n",
                ]
            )
            hyd2 = dict(created2.get("hydration") or {})
            self.assertEqual(list(hyd2.get("created_notes") or []), [])

            b_text = (vault / "notes" / "b.md").read_text("utf-8", errors="replace")
            self.assertIn(f"[[{py_id}|Python]]", b_text)

    def test_update_alias_hydrates_append_and_does_not_touch_fenced_code(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / ".loom" / "memory"
            _run_json(["--vault", str(vault), "--format", "json", "init"])

            _run_json(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "add",
                    "--id",
                    "a",
                    "--title",
                    "A",
                    "--body",
                    "```\n[[Python]]\n```\nOutside [[Python]]\n",
                ]
            )

            updated = _run_json(
                [
                    "--vault",
                    str(vault),
                    "--format",
                    "json",
                    "update",
                    "a",
                    "--append",
                    "Also [[Go]]\n",
                ]
            )
            hyd = dict(updated.get("hydration") or {})
            created_notes = list(hyd.get("created_notes") or [])
            self.assertEqual(len(created_notes), 1)
            go_id = str(created_notes[0].get("id") or "")
            self.assertTrue(go_id)
            self.assertIn("go", go_id)

            a_text = (vault / "notes" / "a.md").read_text("utf-8", errors="replace")
            # fenced block preserved
            self.assertIn("```\n[[Python]]\n```", a_text)
            # outside link hydrated (Python stub id is unknown here, but it should have an alias form)
            self.assertIn("Outside [[", a_text)
            self.assertIn("|Python]]", a_text)
            # appended link hydrated
            self.assertIn(f"[[{go_id}|Go]]", a_text)


if __name__ == "__main__":
    unittest.main()
