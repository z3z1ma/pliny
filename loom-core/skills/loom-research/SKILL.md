---
name: loom-research
description: "Preserve reusable investigations. Use when compatibility, framework/library behavior, tradeoffs, rejected options, null results, performance/security/migration evidence, or external-source synthesis should remain citable."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: owner-layer
  owns_layer: research
---

# loom-research

Research owns reusable discovery.

Use it when the work would benefit from not having to rediscover the same reasoning later.

Research may use an optional source-material store at
`.loom/research/artifacts/<research-slug>/` for articles, fetched web pages, PDFs,
papers, repository snapshots, exported notes, model/advisor outputs, or other raw
inputs that helped the investigation. That directory is support material, usually
gitignored, and may be absent. The research record remains primary: it owns the
synthesis, source evaluation, conclusions, limitations, and downstream route.

## What This Skill Owns

- investigations
- option comparisons
- experiments
- spike and sketch conclusions as research variants when discovery should remain
  citable
- evidence synthesis
- optional source-material stores under `.loom/research/artifacts/<research-slug>/`
- rejected options and null results worth preserving
- deferred questions that are not yet ready for their own investigation
- conclusions and recommendations grounded in evidence

## Use This Skill When

- the project lacks evidence for a decision
- multiple options need comparison
- an experiment result should remain citable
- a spike or sketch produced conclusions, rejected variants, or null results
  that should become reusable research; use optional `loom-spike` or an
  equivalent exploration workflow for procedural spike or sketch detail
- a significant implementation discovery should survive beyond the ticket journal
- a rejected option or null result would otherwise have to be rediscovered
- open questions are accumulating and need a durable home before they are ready to be investigated

## Do Not Use This Skill When

- the work is now a behavior contract
- the work is now a rollout strategy
- the work is just live progress tracking

## Good Research Questions

A strong research note answers:

- what was being investigated
- why it mattered
- how it was investigated
- what evidence was gathered
- what conclusions are justified
- what downstream work should do next
- which options, hypotheses, or variants were rejected and why
- what remains uncertain

## Common Rationalizations

- Rationalization: "I already know the answer."
  - Reality: Research exists when evidence or tradeoffs matter; record the evidence so future agents do not rediscover it.
- Rationalization: "Rejected options are not worth writing down."
  - Reality: Rejections prevent future churn when another agent is tempted by the same path.
- Rationalization: "Generated support analysis is authoritative."
  - Reality: Generated output is source material. Research owns synthesis and limits, not imported authority.
- Rationalization: "Open questions mean the research failed."
  - Reality: Honest open questions are useful when they are routed or deferred explicitly.

## Red Flags

- conclusions are stronger than the cited evidence
- sources lack provenance or freshness notes when current facts matter
- alternatives are listed but not actually compared
- null results are missing after failed attempts
- recommendations do not name the downstream owner layer

## Verification

- [ ] Sources include enough provenance to recheck material claims.
- [ ] Evidence synthesis separates observation from conclusion.
- [ ] Rejected options and null results say what future agents should avoid.
- [ ] Recommendations are bounded and routed to owner layers.

## Done Means

- another agent could reuse the note without rerunning the whole investigation
- uncertainty is visible
- recommendations are bounded by actual evidence

## Read In This Order

Read immediately for normal research creation or review:

1. `references/research-shape.md` when structuring investigation, rejected
   options, null results, conclusions, or recommendations.
2. `references/source-handling.md` when external sources, current facts, or
   source quality matter.
3. `templates/research.md` only when creating or substantially reshaping a
   research record.
