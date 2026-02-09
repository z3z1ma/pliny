---
"id": "al-30fe"
"status": "review"
"deps": []
"links": []
"created": "2026-02-09T05:06:58Z"
"type": "task"
"priority": 2
"assignee": "z3z1ma"
"tags":
- "memory"
- "opencode"
- "compound"
"external": {}
---
# Improve OpenCode nudges for tickets+memory

Extend compound OpenCode plugin to inject per-turn ticket+memory reminder and add post-tool nudges; add --command shorthand to loom memory add/edit; refresh derived docs and tests.

## Notes

**2026-02-09T05:12:20Z**

Implemented --command shorthand for loom memory add/edit (core+cli+README+tests). Added derived LOOM always-on doc updates for ticket+memory protocol. Next: extend compound OpenCode plugin template with per-turn reminder injection + post-bash tool nudges (throttled).

**2026-02-09T05:14:15Z**

Removed hard-coded bash command allowlist for tool nudges. Tool nudge now triggers on failures by default; optional opt-in via COMPOUND_NUDGE_COMMAND_REGEX (regex list) for success cases. Also improved main-only behavior by tracking child sessions from session.created and skipping injection/nudges for those sessions.

**2026-02-09T05:18:12Z**

All quality gates passing: uv run ruff check ., uv run basedpyright, uv run pytest (192 passed). OpenCode compound plugin template now injects per-turn Loom protocol reminder (experimental.chat.messages.transform) and adds post-bash failure nudges (throttled). No hard-coded command allowlist; optional COMPOUND_NUDGE_COMMAND_REGEX for opt-in success nudges.
