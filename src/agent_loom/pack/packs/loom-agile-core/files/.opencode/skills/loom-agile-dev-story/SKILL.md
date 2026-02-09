---
name: loom-agile-dev-story
description: Implement a story/ticket in a worktree with tight feedback loops.
license: MIT
compatibility: opencode
---

## Goal
Ship a ticket with real verification, keeping the work visible in Loom.

## Procedure
1) Load the ticket and confirm scope
   - `loom ticket show <id>`
   - If scope is unclear, ask targeted questions before coding.
   - `loom ticket update <id> --status in_progress`

2) Create/ensure an isolated worktree
   - `loom workspace worktree ensure ticket-<id> --base-ref main`

3) Define done criteria (if missing)
   - Summarize acceptance criteria as a short checklist.
   - Add it to the ticket:
     - `loom ticket add-note <id> "AC: ..."`

4) Implement in small verifiable steps
   - Prefer the loop:
     - write/extend tests or verification first
     - implement minimal code
     - rerun relevant checks
   - After each step, add a progress note:
     - what changed
     - what was verified
     - what remains

5) Run repo-native verification
   - Discover the repo's canonical commands (Makefile/just/package scripts/go/cargo/mvn/gradle/etc).
   - Run the smallest set of checks that gives confidence.
   - If uncertain, ask the user what the canonical commands are.

6) Close out
   - Add a final ticket note with:
     - files changed (high level)
     - tests/checks run
     - follow-ups / known limitations
   - `loom ticket update <id> --status closed`
   - If you learned something reusable, capture it:
     - `loom memory add --title "..." --body "..."`
