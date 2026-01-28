import hashlib
import unittest
from typing import Callable, cast

from agent_loom.team import core as team

_parse_duration_seconds = cast(
    Callable[[str], int], getattr(team, "_parse_duration_seconds")
)


class TestSanitize(unittest.TestCase):
    def test_sanitize_basic(self) -> None:
        self.assertEqual(team.sanitize("  hello   world "), "hello-world")
        self.assertEqual(team.sanitize("a/b:c"), "a-b-c")
        self.assertEqual(team.sanitize("."), "")
        self.assertEqual(team.sanitize(".."), "")
        self.assertEqual(team.sanitize(""), "")

    def test_sanitize_allow_and_max_len(self) -> None:
        self.assertEqual(team.sanitize("a/b", allow=r"a-zA-Z0-9._/-"), "a/b")
        self.assertEqual(team.sanitize("aaaa bbbb", max_len=5), "aaaa")


class TestGenerateStableKey(unittest.TestCase):
    def test_returns_input_when_unchanged(self) -> None:
        self.assertEqual(team.generate_stable_key("hello"), "hello")

    def test_sanitization_adds_hash_suffix(self) -> None:
        raw = "hello world"
        h = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8]
        self.assertEqual(team.generate_stable_key(raw), f"hello-world-{h}")

    def test_truncation_keeps_within_max_len(self) -> None:
        raw = "a" * 200
        out = team.generate_stable_key(raw, max_len=10)
        h = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8]
        self.assertEqual(out, f"a-{h}")

    def test_empty_or_invalid_returns_empty(self) -> None:
        self.assertEqual(team.generate_stable_key("  "), "")
        self.assertEqual(team.generate_stable_key(".."), "")


class TestParseDurationSeconds(unittest.TestCase):
    def test_numeric_units_and_compound(self) -> None:
        self.assertEqual(_parse_duration_seconds("90"), 90)
        self.assertEqual(_parse_duration_seconds("15m"), 15 * 60)
        self.assertEqual(_parse_duration_seconds("1h30m"), 1 * 3600 + 30 * 60)

    def test_clock_formats(self) -> None:
        self.assertEqual(_parse_duration_seconds("02:03"), 2 * 60 + 3)
        self.assertEqual(_parse_duration_seconds("01:02:03"), 1 * 3600 + 2 * 60 + 3)

    def test_invalid_raises(self) -> None:
        with self.assertRaises(team.TeamError):
            _parse_duration_seconds("")
        with self.assertRaises(team.TeamError):
            _parse_duration_seconds("1w")
        with self.assertRaises(team.TeamError):
            _parse_duration_seconds("0s")


class TestChannelFor(unittest.TestCase):
    def test_channel_is_stable_and_sanitized(self) -> None:
        self.assertEqual(
            team.channel_for(run_id="1234567890abcdef", to="worker-1"),
            "team:1234567890ab:to:worker-1",
        )

    def test_missing_or_invalid_returns_empty(self) -> None:
        self.assertEqual(team.channel_for(run_id="", to="worker-1"), "")
        self.assertEqual(team.channel_for(run_id="abc", to="!!!"), "")


class TestMessagePreview(unittest.TestCase):
    def test_takes_first_line(self) -> None:
        self.assertEqual(team._message_preview("hi\nthere"), "hi")

    def test_truncates_with_ellipsis(self) -> None:
        self.assertEqual(team._message_preview("a" * 120, max_len=10), "a" * 7 + "...")


if __name__ == "__main__":
    unittest.main()
