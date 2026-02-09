---
name: loom-agile-create-architecture
description: Produce a minimal architecture plan with explicit decisions and tradeoffs.
license: MIT
compatibility: opencode
---

## Outcomes
- A clear approach that enables implementation
- Decisions + tradeoffs captured
- A verification strategy

## Procedure
1) Context
   - Constraints and non-negotiables
   - Existing system boundaries

2) Proposed design
   - Components and responsibilities
   - Data flow
   - Interfaces (only as detailed as needed)

3) Decisions
   - For each major decision: options, decision, why
   - Record durable decisions in Loom memory when useful:
     - `loom memory add --title "..." --body "..."`

4) Risks and failure modes
5) Test/verification plan (language/toolchain agnostic)
6) Persist
   - Add a ticket note linking the architecture artifact.
