Status: done
Created: 2026-06-28
Updated: 2026-06-28

# Record Richness Score Improvement

## Question

Can a compact cold-start regeneration checklist improve `S010` / Record
Regeneration Quality for records created by 10x without adding fixture-backed
grading, runner complexity, record spam, or weaker existing 10x behavior?

## Hypothesis

Adding a small "record regeneration check" near the Record Graph cold-reader
rule will improve created ticket/spec/evidence richness because it makes the
necessary durable context explicit at the point of writing: objective and state,
authority and provenance, constraints and edge cases, evidence and limits,
blockers and semantic authority, and next action and verification.

The expected improvement is strongest when the subject must create or update a
record from rich source material: a policy-ratification ticket/spec shaping
case and a redacted evidence-capture case.

## Sources And Methods

- Read `SKILL.md`, especially Record Graph, Tickets, Evidence, and closure
  rules.
- Read `autoresearch/program.md` and `autoresearch/README.md`.
- Read `autoresearch/catalogs/scores.json` for `S010`.
- Selected existing `S010` seeds from `autoresearch/trial-seeds/index.json`:
  `explicit-policy-ratification` (`SCN-006`) and
  `redacted-evidence-capture` (`SCN-008`).
- Created candidate overlay
  `autoresearch/candidates/2026-06-28-record-regeneration-check.md`.

Registered experiment definition:

- `.10x/research/.storage/2026-06-28-record-richness-score/experiment-record-regeneration-check.json`
- `.10x/research/.storage/2026-06-28-record-richness-score/experiment-record-regeneration-check-continuation.json`

Planned artifact root:

- `.10x/evidence/.storage/2026-06-28-record-richness-score/record-regeneration-check-codex/`
- `.10x/evidence/.storage/2026-06-28-record-richness-score/record-regeneration-check-continuation-codex/`

## Planned Inspection

Inspect raw transcripts, workspace manifests, archived workspaces, created or
updated `.10x` records, command metadata, and canonical guard. Score each arm
against `S010` sub-scores and hard floors:

- cold-start completeness;
- behavior and edge-case coverage;
- provenance and evidence grounding;
- ambiguity and blocker preservation;
- operational actionability;
- cross-record coherence;
- economy without thinness.

## Findings

Initial experiment completed and exposed a multi-turn blocker in the
policy-ratification seed. The current arm correctly asked what happens to
under-USD-500 payouts that fail age or chargeback eligibility. The candidate
created rich bounded records and preserved that unresolved disposition as an
open bound. A continuation experiment is registered to answer the blocker and
compare the completed record graphs.

The continuation experiment completed with both arms creating or updating
records and no implementation edits. Current 10x was already strong after the
clarification. The candidate's advantage was modest and concentrated in
explicit cold-start ticket context, references, design notes, and stale-bound
repair. The evidence-capture seed did not improve under the candidate, but it
remained above floor and did not leak secrets.

Result evidence:

- `.10x/evidence/2026-06-28-record-richness-candidate-result.md`

Review:

- `.10x/reviews/2026-06-28-record-richness-candidate-review.md`

## Conclusions

Promote the compact record-regeneration check, not the full candidate overlay.
The change should modestly improve `S010` handoff richness while preserving the
existing record-economy and evidence-integrity gates.
