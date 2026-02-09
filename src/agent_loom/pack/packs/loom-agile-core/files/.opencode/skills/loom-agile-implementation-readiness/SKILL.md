---
name: loom-agile-implementation-readiness
description: Check readiness to implement (inputs, risks, sequencing, test plan).
license: MIT
compatibility: opencode
---

## Readiness checklist
- Requirements are clear enough to build
- Acceptance criteria are testable
- Key risks identified
- Dependencies known
- A test/verification approach exists

## Procedure
1) Review current artifacts (brief/PRD/architecture)
2) Ask: what is the smallest shippable slice?
3) Check for blockers
   - missing decisions
   - unclear acceptance criteria
   - missing data/permissions/integrations
4) Identify the riskiest unknowns
   - propose a spike or proof-of-concept if needed
5) Confirm sequencing
   - what must be done first?
6) Confirm verification plan
   - what tests/checks prove acceptance criteria?
   - what manual verification is needed?
7) Produce a readiness report:
   - Ready: yes/no
   - Blockers
   - Risks
   - Next action (usually one command)
8) Add the report to the ticket.
