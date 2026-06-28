Status: active
Created: 2026-06-28
Updated: 2026-06-28

# Record Richness Hypothesis Search

## Question

What compact `SKILL.md` change, if any, produces the best `S010` record-quality
uplift per added character while preserving existing 10x behavior around
ambiguity, evidence, record economy, and closure?

## Starting Correction

The previous record-regeneration-check promotion was under-evidenced. It is now
rolled back from canonical `SKILL.md` and retained as a candidate. The
experiment program will compare it against alternative mechanisms before any
future promotion.

## Hypothesis Space

Holistic inspection of `SKILL.md` suggests record richness can be influenced at
several points, not only by a cold-start regeneration checklist:

- Record regeneration framing: ensure a future agent can reconstruct the work
  from records alone. Candidate:
  `autoresearch/candidates/2026-06-28-record-regeneration-check.md`.
- Source-to-record losslessness: compare record content against source, chat,
  and artifacts to avoid dropping available material facts. Candidate:
  `autoresearch/candidates/2026-06-28-source-material-delta-audit.md`.
- Executor handoff contract: make tickets/specs optimized for a cold executor's
  next action and verification path. Candidate:
  `autoresearch/candidates/2026-06-28-executor-handoff-contract.md`.
- Economy/density guard: prevent both thin records and record spam. Candidate:
  `autoresearch/candidates/2026-06-28-record-economy-density.md`.
- Evidence/research auditability: preserve procedures, observations, limits,
  redactions, and null results without overclaiming. Candidate:
  `autoresearch/candidates/2026-06-28-audit-limits-redaction.md`.

Overlay character costs:

| Candidate | Overlay chars |
| --- | ---: |
| record-regeneration-check | 796 |
| source-material-delta-audit | 697 |
| executor-handoff-contract | 566 |
| record-economy-density | 520 |
| audit-limits-redaction | 444 |

## Sources And Methods

- Inspect `SKILL.md` holistically, not only the Record Graph section.
- Use `autoresearch/catalogs/scores.json` `S010` sub-scores and hard floors.
- Select existing seed workspaces from `autoresearch/trial-seeds/index.json`.
- Register experiments under
  `.10x/research/.storage/2026-06-28-record-richness-hypothesis-search/`.
- Preserve raw outputs under
  `.10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/`.

Registered first-batch experiments:

- `experiment-external-index.json`: `SCN-004`, external canonical PRD index.
- `experiment-record-economy.json`: `SCN-005`, account-export docs/test record
  economy.
- `experiment-ticket-handoff.json`: `SCN-006`, mixed active/terminal authority
  ticket handoff.
- `experiment-evidence-audit.json`: `SCN-008`, redacted evidence capture.
- `experiment-retrospective-learning.json`: `SCN-012`, retrospective learning
  versus noisy notes.

Self-check questions before scoring:

- Did a candidate improve the record, or merely make it longer?
- Did it preserve material facts available in source/chat/artifacts?
- Did it create unnecessary record spread?
- Did it protect semantic authority and blockers?
- Did it improve cold-start actionability enough to justify added characters?
- Did it regress existing S001/S002/S004/S005/S006 behavior?

## Findings

Pending.

## Conclusions

Pending.
