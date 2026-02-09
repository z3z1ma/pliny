---
"id": "al-4b4b"
"status": "in_progress"
"deps": []
"links": []
"created": "2026-02-09T21:19:57Z"
"type": "chore"
"priority": 2
"assignee": "z3z1ma"
"tags":
- "docs"
- "readme"
- "ux"
"external": {}
---
Add copy/pasteable barebones starter snippets in README for agent-facing subsystems (Ticket/Memory/Workspace/Compound). Each snippet should focus on WHAT/WHY/WHEN; push HOW to progressive disclosure via `loom <subsystem> -h` and `loom <subsystem> prime`. Explicitly steer agents toward using Loom commands instead of hand-editing `.loom/**`.

## Notes

**2026-02-09T21:23:32Z**

Adjust README starter snippets to begin with definitive declarations: "We use <x> for <y>" for each subsystem.

**2026-02-09T21:24:04Z**

README snippets updated so each subsystem snippet begins with a definitive declaration: "We use <x> for <y>". Kept the WHAT/WHY/WHEN focus and deferred HOW to `-h`/`prime`.

**2026-02-09T21:25:48Z**

Feedback incorporated: keep explicit WHAT/WHY/WHEN lines (don’t rely on the "We use …" declaration alone), and expand those sections for stronger LLM instruction-following. Will update README snippets accordingly.

**2026-02-09T21:26:35Z**

README starter snippets revised: each snippet starts with "We use … for …" AND retains explicit WHAT/WHY/WHEN lines (expanded for stronger model compliance). Kept HOW as progressive disclosure via `-h`/`prime`.

**2026-02-09T21:29:17Z**

Overhauled README starter snippets to be much more directive/convincing: added subsystem mental model, expanded WHAT/WHY/WHEN for Ticket/Memory/Workspace/Compound, and added small "if you are coordinating/risky" command blocks while keeping HOW primarily in `-h`/`prime`.

**2026-02-09T21:32:17Z**

Expanded README starter snippets substantially using cookbook-derived details: clarified canonical loop, strengthened WHAT/WHY/WHEN (locks/audit/claims for Ticket; derived index/scopes/link graph/janitor for Memory; repo vs harness + selection guardrails + cleanup/snapshots for Workspace; Skills + evidence/governance + determinism for Compound). Added a few high-leverage command blocks while keeping deep HOW in `-h`/`prime`.,description:Add ticket note about major expansion

**2026-02-09T21:33:24Z**

Further expanded README snippets: added more cookbook-backed WHAT/WHEN details (Ticket ref normalization + avoid hand-editing; Memory visibilities + evidence capture; Workspace sandbox/TTL + harness blast-radius intent; Compound institutional memory framing). Added explicit "common failure mode" lines to make the value visceral.

**2026-02-09T21:38:10Z**

Reformat pass: convert explicit WHAT/WHY/WHEN lines into cohesive paragraphs while preserving all content (no deletions), improving flow and instruction clarity for LLMs.

**2026-02-09T21:39:29Z**

Reformatted README starter snippets: removed explicit WHAT/WHY/WHEN labels and rewrote each snippet as cohesive paragraphs while preserving all existing content (no deletions) and keeping progressive disclosure (`-h`/`prime`) + command blocks intact.
