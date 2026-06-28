Status: done
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
- Synthesized cold-start handoff check: combine the first-batch signals into one
  compact finalization check for fact ownership, authority/provenance, limits,
  blockers, evidence path, next action, and noise filtering. Candidate:
  `autoresearch/candidates/2026-06-28-cold-start-record-handoff-check.md`.

Overlay character costs:

| Candidate | Overlay chars |
| --- | ---: |
| record-regeneration-check | 796 |
| source-material-delta-audit | 697 |
| executor-handoff-contract | 566 |
| record-economy-density | 520 |
| audit-limits-redaction | 444 |
| cold-start-record-handoff-check | 457 |

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

Registered second-stage confirmation experiments:

- `experiment-v2-external-index.json`: `SCN-004`, current versus compact v2,
  two repetitions.
- `experiment-v2-record-economy.json`: `SCN-005`, current versus compact v2,
  two repetitions.
- `experiment-v2-ticket-handoff.json`: `SCN-006`, current versus compact v2,
  two repetitions.
- `experiment-v2-evidence-audit.json`: `SCN-008`, current versus compact v2,
  two repetitions.
- `experiment-v2-retrospective-learning.json`: `SCN-012`, current versus
  compact v2, two repetitions.

Self-check questions before scoring:

- Did a candidate improve the record, or merely make it longer?
- Did it preserve material facts available in source/chat/artifacts?
- Did it create unnecessary record spread?
- Did it protect semantic authority and blockers?
- Did it improve cold-start actionability enough to justify added characters?
- Did it regress existing S001/S002/S004/S005/S006 behavior?

## Findings

- The canonical skill already scored high on record quality; the useful target
  was consistency and uplift per added character, not a large rescue.
- The original `record-regeneration-check` candidate did not justify promotion:
  it added 796 overlay characters and did not materially outperform current 10x.
- `source-material-delta-audit` produced the richest retrospective/source-loss
  artifacts but was verbose and slow.
- `executor-handoff-contract` was strongest on ticket handoff and small record
  economy, but its benefit was narrower than its wording.
- `audit-limits-redaction` was valuable for evidence redaction and conservative
  external-source blocking, but weaker on retrospective closure.
- The synthesized `cold-start-record-handoff-check` candidate captured most of
  the useful behavior in 457 overlay characters.

## Conclusions

Promote `autoresearch/candidates/2026-06-28-cold-start-record-handoff-check.md`
to canonical `SKILL.md`.

Do not promote the original record-regeneration candidate or the broader
first-batch candidates as written. Retain them as evidence of hypothesis search
and possible future variants if later seeds expose narrower gaps.
