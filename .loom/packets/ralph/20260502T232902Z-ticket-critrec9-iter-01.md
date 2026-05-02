---
id: packet:ralph-ticket-critrec9-20260502T232902Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:critrec9
mode: execution
change_class: protocol-authority
risk_class: medium
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-02T23:29:02Z
updated_at: 2026-05-02T23:35:41Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - ticket:critrec9
    - evidence:critique-recommendation-vocabulary-validation
    - packet:ralph-ticket-critrec9-20260502T232902Z
  paths:
    - skills/loom-critique/templates/critique.md
    - skills/loom-critique/references/*.md
    - .loom/tickets/20260502-critrec9-normalize-critique-recommendations.md
    - .loom/evidence/20260502-critique-recommendation-vocabulary-validation.md
    - .loom/packets/ralph/20260502T232902Z-ticket-critrec9-iter-01.md
parent_merge_scope:
  records:
    - ticket:critrec9
    - evidence:critique-recommendation-vocabulary-validation
    - packet:ralph-ticket-critrec9-20260502T232902Z
  paths:
    - skills/loom-critique/templates/critique.md
    - skills/loom-critique/references/finding-format.md
    - .loom/tickets/20260502-critrec9-normalize-critique-recommendations.md
    - .loom/evidence/20260502-critique-recommendation-vocabulary-validation.md
    - .loom/packets/ralph/20260502T232902Z-ticket-critrec9-iter-01.md
source_fingerprint:
  git_commit: cac7c7c2446eebe17127346f059c93cc580986b8
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: cac7c7c2446eebe17127346f059c93cc580986b8
  git_status_summary: clean
  compiled_from:
    - initiative:skills-corpus-template-grammar-safety-pass
    - plan:skills-corpus-template-grammar-safety-pass
    - ticket:critrec9
execution_context:
  branch: main
  push_remote: origin
  worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
  isolation: none
  git_shared_metadata_mutations: forbidden
  destructive_commands: forbidden
  network: forbidden
context_budget:
  posture: tight
  max_source_files: 8
  max_excerpt_lines_per_file: 160
  avoid_full_file_reads: false
sources:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
  ticket:
    - ticket:critrec9
  records:
    - skills/loom-critique/templates/critique.md
    - skills/loom-critique/references/finding-format.md
    - skills/loom-critique/references/review-pass-splitting.md
    - skills/loom-tickets/references/state-machine.md
    - skills/loom-records/references/route-vocabulary.md
links:
  ticket:
    - ticket:critrec9
---

# Mission

Normalize critique acceptance recommendation wording so it cannot be mistaken for
ticket lifecycle states, route tokens, or critique-owned closure authority.

# Bound Context

This is the ninth ticket in `plan:skills-corpus-template-grammar-safety-pass` and
covers `initiative:skills-corpus-template-grammar-safety-pass#OBJ-009`. Critique
records own findings, verdicts, residual risks, and recommendations. Tickets own
live state, acceptance, risk disposition, and closure.

# Source Snapshot

Baseline commit: `cac7c7c2446eebe17127346f059c93cc580986b8`, matching
`origin/main`. Worktree was clean before packet creation.

Parent search found the primary risky wording in
`skills/loom-critique/templates/critique.md:89-94`: acceptance recommendations
include phrases such as `close-ready`, `complete pending acceptance`, `review
required`, `blocked`, and `accepted risk needed`. Some resemble ticket states or
routes but are not explicitly framed as non-canonical recommendation labels.

# Change Class

Declared as `protocol-authority`; risk is medium because critique recommendation
wording can accidentally teach critique records to mutate ticket truth.

# Verification Targets

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-009`
- `ticket:critrec9#ACC-001`
- `ticket:critrec9#ACC-002`
- `ticket:critrec9#ACC-003`
- `ticket:critrec9#ACC-004`

# Task For This Iteration

1. Capture before-state searches in `skills/loom-critique` for `close-ready`,
   acceptance recommendation wording, ticket-state-looking recommendation labels,
   route tokens, and recommendation/status wording.
2. Update `skills/loom-critique/templates/critique.md` and related critique
   references only as needed so acceptance recommendation vocabulary is clearly a
   non-canonical recommendation label set unless it explicitly names an existing
   ticket state or route token.
3. State clearly that critique recommendations inform ticket-owned acceptance but
   do not mutate ticket state or close work.
4. Preserve critique acceptance recommendations; do not remove the section.
5. Preserve critique ownership of findings/verdicts and ticket ownership of live
   state, accepted risk, and closure.
6. Update `ticket:critrec9` to `review_required` with evidence linked, claim
   matrix current, and next route `critique`.
7. Record `evidence:critique-recommendation-vocabulary-validation` with
   before/after searches and `git diff --check`.
8. Fill this packet's `# Child Output`. The parent will replace the
   `parent_merge_scope.paths` placeholder with concrete reconciled paths and mark
   the packet consumed after reconciliation.

# Verification Posture

`observation-first`.

Capture before/after recommendation/status vocabulary searches and `git diff
--check`.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- fixing the wording would require changing route vocabulary or ticket state
  machine grammar outside the critique skill;
- the fix would remove critique acceptance recommendations entirely;
- the fix would give critique records closure or acceptance authority;
- the fix would add validators, automation, schema enforcement, command wrappers,
  runtime requirements, hidden helpers, or a new owner layer;
- the source fingerprint is materially stale before launch.

# Output Contract

Return outcome, files changed, records changed, before/after observation
commands/results, `git diff --check` result, residual risks, self-review
concerns, and ticket recommendation. Include whether the ticket should proceed to
mandatory oracle critique with profiles `owner-boundary`, `records-grammar`, and
`closure-honesty`.

# Working Notes

Parent created this packet after confirming `ticket:phsafe8` was closed and
pushed and the worktree was clean at the source fingerprint.

# Child Output

Outcome: `stop`.

Changed files:

- `skills/loom-critique/templates/critique.md`
- `skills/loom-critique/references/finding-format.md`
- `.loom/tickets/20260502-critrec9-normalize-critique-recommendations.md`
- `.loom/evidence/20260502-critique-recommendation-vocabulary-validation.md`
- `.loom/packets/ralph/20260502T232902Z-ticket-critrec9-iter-01.md`

Records changed:

- `ticket:critrec9`
- `evidence:critique-recommendation-vocabulary-validation`
- `packet:ralph-ticket-critrec9-20260502T232902Z`

Evidence gathered:

- Before searches in `skills/loom-critique` found `close-ready`, `complete
  pending acceptance`, `review required`, `blocked`, and `accepted risk needed`
  in the critique record template's acceptance recommendation prose.
- After searches show no `close-ready` hit and no legacy acceptance
  recommendation wording; the only remaining ticket-state-looking hit is
  critique-packet stop-condition wording for `blocked`, outside this packet's
  recommendation-label target and outside child write scope.
- Updated template now defines non-canonical critique recommendation labels and
  states they are not ticket states, route tokens, finding dispositions, closure
  decisions, or ticket-state mutations.
- Updated finding-format reference states critique acceptance recommendation
  labels are non-canonical advice for the ticket acceptance gate.
- `git diff --check`: passed with no output.

Residual risks / self-review concerns:

- Broad route-token searches still return legitimate critique skill/packet uses
  of `ticket`, `critique`, and `evidence`; evidence records this as expected
  noise rather than unresolved recommendation vocabulary.
- I did not edit route vocabulary or ticket state-machine files.
- Mandatory oracle critique remains required before ticket closure.

Ticket recommendation:

- `ticket:critrec9` should remain `review_required` and proceed to mandatory
  oracle critique using profiles `owner-boundary`, `records-grammar`, and
  `closure-honesty`.

# Parent Merge Notes

2026-05-02T23:34:35Z: Parent accepted the bounded child output for review and
reconciled it into `ticket:critrec9`,
`evidence:critique-recommendation-vocabulary-validation`, and this packet. Parent
normalized the ticket claim matrix to canonical claim-coverage statuses, expanded
the ticket coverage list with ticket-local acceptance IDs, expanded the evidence
record with support/challenge/environment/validity sections, and replaced the
merge-scope placeholder with concrete paths. The ticket remains
`review_required`; closure is not accepted until mandatory oracle critique passes
and the ticket acceptance gate is updated.
