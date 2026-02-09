---
name: loom-agile-code-review
description: Perform a structured review (correctness, quality, security, docs, tests).
license: MIT
compatibility: opencode
---

## Goal
Validate claims against reality, not vibes.

## Review dimensions
1) Correctness (requirements, edge cases)
2) Maintainability (structure, naming, complexity)
3) Security (input validation, auth boundaries, secrets)
4) Tests (signal, coverage of critical paths)
5) Docs (onboarding, usage changes)

## Procedure
1) Establish scope
   - What ticket or change is being reviewed?
   - What are the acceptance criteria?

2) Cross-check what actually changed
   - If the repo is git-backed, use git to identify the real diff.
   - Compare the diff to what the ticket claims.

3) Validate acceptance criteria
   - For each AC, find concrete evidence (code paths, tests, UI, docs).
   - Mark as Implemented / Partial / Missing.

4) Review changed files
   - Look for error handling, invariants, and foot-guns.
   - Identify at least a few concrete risks or improvements.

5) Tests
   - Are there tests for the critical behavior?
   - Are tests deterministic and meaningful?

6) Summarize findings
   - Must-fix
   - Should-fix
   - Nice-to-have

7) Persist in Loom
   - `loom ticket add-note <id> "Code review: must-fix ..."`
   - If there is a reusable review pattern, capture it in memory.
