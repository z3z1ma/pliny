---
"id": "al-f9c2"
"status": "closed"
"deps": []
"links": []
"created": "2026-02-17T05:30:59Z"
"type": "task"
"priority": 1
"assignee": "z3z1ma"
"tags": []
"external": {}
---
# Harden Team tmux nudge reliability

Implement post-send confirmation heuristics, busy-aware nudge retries, and durable retry/backoff behavior for sidecar inbox nudges to reduce no-op or swallowed TUI nudges while avoiding spam when agents are actively busy.

## Notes

**2026-02-17T05:36:49Z**

Implemented Team nudge reliability hardening: added pane activity/busy helpers, post-send activity confirmation + retry in target nudge path (reason=unconfirmed_delivery), extracted sidecar nudge/retry logic into sidecar_nudge.py, switched sidecar inbox nudges to busy-aware retry/backoff with per-message scheduling, and added regression test for unconfirmed delivery retries. Core file remains under guardrail (6898 lines). Full gates: ruff, basedpyright, pytest all pass (333 tests).

**2026-02-17T05:40:43Z**

Follow-up included idle-screen robustness: captures are now normalized before hashing (timestamps/time/progress noise stripped) so unchanged-work detection is less brittle and keepalive nudges trigger more reliably.
