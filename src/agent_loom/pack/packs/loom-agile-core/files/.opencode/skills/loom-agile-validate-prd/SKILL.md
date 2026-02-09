---
name: loom-agile-validate-prd
description: Validate a PRD for completeness, measurability, and implementation leakage.
license: MIT
compatibility: opencode
---

## Output
- Overall status: Pass / Warning / Critical
- A short results table
- Must-fix / Should-fix / Nice-to-have
- Next action recommendation

## Validation dimensions
1) Format and clarity
   - Readable structure with headings
   - Terms defined (no ambiguous jargon)

2) Information density
   - Not too vague (hand-wavy)
   - Not too bloated (repeats, filler)

3) Brief coverage
   - PRD matches the brief/goals
   - No accidental scope drift

4) Measurability
   - Goals include measurable success metrics
   - Acceptance criteria are testable statements

5) Traceability
   - Journeys -> requirements -> acceptance criteria

6) Implementation leakage
   - Requirements are not disguised solutions
   - Tech choices only appear when they are hard constraints

7) Domain and project fit
   - Non-functional constraints reflect the domain (security, privacy, compliance)
   - Project type assumptions are explicit (internal tool vs public app, etc.)

8) Completeness
   - Open questions captured
   - Risks captured
   - Out of scope captured

## Procedure
1) Read the PRD end-to-end.
2) For each dimension above, rate severity:
   - Pass / Warning / Critical
3) Produce a short results table (one line per dimension).
4) List findings as:
   - Must-fix (blocks implementation)
   - Should-fix (significant quality risk)
   - Nice-to-have
5) Recommend the next command:
   - If requirements are unclear: `/loom-agile-edit-prd`
   - If ready to plan: `/loom-agile-create-epics-and-stories`
   - If ready to design: `/loom-agile-create-architecture`
6) Persist in Loom:
   - `loom ticket add-note <id> "PRD validation: Overall=<...>. Must-fix: ..."`
