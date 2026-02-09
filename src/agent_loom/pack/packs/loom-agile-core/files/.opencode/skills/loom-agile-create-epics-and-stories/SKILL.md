---
name: loom-agile-create-epics-and-stories
description: Derive epics and stories from a PRD with clear done criteria.
license: MIT
compatibility: opencode
---

## Outcomes
- A small set of epics
- Stories that are implementation-ready
- A clear dependency order

## Procedure
1) Prerequisites
   - Confirm the PRD exists and is good enough to plan from.
   - If validation is missing, run PRD validation first.

2) Extract capability areas from journeys
   - For each journey, list the capabilities it requires.
   - Group capabilities into 3-8 coherent epics.

3) Define epics
   - Epic title
   - Outcome (measurable)
   - Scope boundaries
   - Risks

4) Derive stories per epic
   - Keep stories small and verifiable.
   - Each story must include:
     - user-facing value
     - acceptance criteria
     - verification note (how to prove it works)
   - Only include implementation notes when necessary to prevent rework.

5) Sequence and dependencies
   - Order stories so early work unlocks later work.
   - Explicitly mark dependencies.

6) Map to Loom tickets
   - Create tickets for the next executable stories:
     - `loom ticket create "<story title>" --status ready`
   - Link dependencies when applicable:
     - `loom ticket dep-add <child> <parent>`

7) Persist
   - Add a summary note to the parent ticket with:
     - epic list
     - story list
     - recommended execution order
