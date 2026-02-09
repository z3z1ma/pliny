---
name: loom-agile-research
description: Structured research with synthesis (domain, market, or technical).
license: MIT
compatibility: opencode
---

## Outcomes
- A synthesis (not a link dump)
- Decision-relevant conclusions
- Open questions + recommended follow-ups

## Procedure
1) Define research type
   - Domain: concepts, stakeholders, constraints
   - Market: competitors, alternatives, pricing, adoption
   - Technical: libraries, architectures, tradeoffs, integration patterns

2) List hypotheses (3-7)
   - What would be true if this direction is good?

3) Gather sources
   - Prefer primary sources (docs, RFCs, code) over summaries.
   - Capture citations (URLs / file paths).

4) Synthesize
   - What did we learn?
   - What changed our mind?
   - What are the risks?

5) Recommend next actions
   - Convert research into a brief/PRD/architecture as appropriate.

6) Persist
   - Add a ticket note with the synthesis.
   - If the learning is reusable: `loom memory add --title "..." --body "..."`
