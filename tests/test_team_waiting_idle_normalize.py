import unittest

from agent_loom.team.waiting import normalize_capture_for_idle


class TestTeamWaitingIdleNormalize(unittest.TestCase):
    def test_normalize_capture_for_idle_strips_time_noise(self) -> None:
        raw = "\n".join(
            [
                "step 1 12:34:56 running",
                "progress 55% 2026-02-17T05:30:00Z",
                "steady output",
            ]
        )
        out = normalize_capture_for_idle(raw)
        self.assertIn("step 1 <time> running", out)
        self.assertIn("progress <pct> <ts>", out)
        self.assertIn("steady output", out)
        self.assertNotIn("12:34:56", out)
        self.assertNotIn("55%", out)


if __name__ == "__main__":
    unittest.main()
