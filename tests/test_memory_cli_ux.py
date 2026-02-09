import contextlib
import importlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Callable, cast


memory_cli_mod = importlib.import_module("agent_loom.memory.cli")
memory_cli = cast(Callable[[list[str]], int], getattr(memory_cli_mod, "main"))


def _run_json(argv: list[str]) -> tuple[int, dict]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = memory_cli(argv)
    payload = buf.getvalue().strip()
    return rc, (json.loads(payload) if payload else {})


def _run_text(argv: list[str]) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = memory_cli(argv)
    return rc, buf.getvalue()


class TestMemoryCliUx(unittest.TestCase):
    def test_unknown_command_is_structured_json_error(self) -> None:
        rc, payload = _run_json(["nope"])
        self.assertEqual(rc, 2)
        self.assertFalse(payload.get("ok"))
        self.assertEqual(payload.get("code"), "ARGPARSE")
        self.assertTrue(str(payload.get("hint") or ""))

    def test_vault_missing_is_not_found(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / ".loom" / "memory"
            rc, payload = _run_json(["--vault", str(vault), "add", "Hello"])
        self.assertEqual(rc, 2)
        self.assertFalse(payload.get("ok"))
        self.assertEqual(payload.get("code"), "NOT_FOUND")
        self.assertIn("init", str(payload.get("hint") or "").lower())

    def test_add_positional_title_rewrites(self) -> None:
        norm = memory_cli_mod._normalize_argv(["add", "Hello"])
        args = memory_cli_mod.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "title", "") or ""), "Hello")

    def test_add_command_flag_parses(self) -> None:
        norm = memory_cli_mod._normalize_argv(
            ["add", "Hello", "--command", "uv run pytest"]
        )
        args = memory_cli_mod.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "command", "") or ""), "uv run pytest")

    def test_add_two_positional_args_become_title_and_body(self) -> None:
        norm = memory_cli_mod._normalize_argv(["add", "Hello", "Body"])
        args = memory_cli_mod.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "title", "") or ""), "Hello")
        self.assertEqual(str(getattr(args, "body", "") or ""), "Body")

    def test_recall_alias_parses(self) -> None:
        args = memory_cli_mod.build_parser().parse_args(["get", "hello"])
        self.assertEqual(str(getattr(args, "cmd", "") or ""), "get")

    def test_empty_recall_returns_recent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / ".loom" / "memory"
            rc0, payload0 = _run_json(["--vault", str(vault), "init"])
            self.assertEqual(rc0, 0)
            self.assertTrue(payload0.get("ok"))

            rc1, payload1 = _run_json(
                [
                    "--vault",
                    str(vault),
                    "add",
                    "--title",
                    "Hello",
                    "--body",
                    "Body",
                ]
            )
            self.assertEqual(rc1, 0)
            self.assertTrue(payload1.get("ok"))

            rc2, payload2 = _run_json(["--vault", str(vault), "recall", ""])
            self.assertEqual(rc2, 0)
            self.assertIsInstance(payload2, list)
            self.assertTrue(any(str(x.get("title") or "") == "Hello" for x in payload2))

    def test_forget_requires_filter(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / ".loom" / "memory"
            rc0, payload0 = _run_json(["--vault", str(vault), "init"])
            self.assertEqual(rc0, 0)
            self.assertTrue(payload0.get("ok"))

            rc, payload = _run_json(["--vault", str(vault), "forget"])
            self.assertEqual(rc, 2)
            self.assertFalse(payload.get("ok"))
            self.assertEqual(payload.get("code"), "ARG")

    def test_link_validate_positional_id_rewrites(self) -> None:
        norm = memory_cli_mod._normalize_argv(["link", "validate", "abc"])
        args = memory_cli_mod.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "id", "") or ""), "abc")

    def test_body_dash_requires_piped_stdin(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / ".loom" / "memory"
            # init vault so we get to the body '-' validation
            rc0, payload0 = _run_json(["--vault", str(vault), "init"])
            self.assertEqual(rc0, 0)
            self.assertTrue(payload0.get("ok"))

            class _TtyStdin(io.StringIO):
                def isatty(self) -> bool:  # type: ignore[override]
                    return True

            old_stdin = sys.stdin
            try:
                sys.stdin = _TtyStdin("")
                rc, payload = _run_json(
                    ["--vault", str(vault), "add", "Hello", "--body", "-"]
                )
            finally:
                sys.stdin = old_stdin
            self.assertEqual(rc, 2)
            self.assertFalse(payload.get("ok"))
            self.assertEqual(payload.get("code"), "ARG")
            self.assertIn("stdin", str(payload.get("error") or "").lower())

    def test_prime_prints_cookbook(self) -> None:
        rc, text = _run_text(["prime"])
        self.assertEqual(rc, 0)
        self.assertIn("Memory Cookbook", text)
        self.assertIn("loom memory add", text)

    def test_prime_json_includes_markdown(self) -> None:
        rc, payload = _run_json(["prime", "--format", "json"])
        self.assertEqual(rc, 0)
        self.assertTrue(payload.get("ok"))
        content = str(payload.get("markdown") or "")
        self.assertIn("Memory Cookbook", content)
