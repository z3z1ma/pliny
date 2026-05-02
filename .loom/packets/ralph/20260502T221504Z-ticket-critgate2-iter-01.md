---
id: packet:ralph-ticket-critgate2-20260502T221504Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:critgate2
mode: execution
change_class: protocol-authority
risk_class: high
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-02T22:15:03Z
updated_at: 2026-05-02T22:21:29Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - ticket:critgate2
    - evidence:critique-closure-gate-validation
    - packet:ralph-ticket-critgate2-20260502T221504Z
  paths:
    - skills/loom-bootstrap/references/07-validation-and-honesty.md
    - skills/loom-bootstrap/references/05-critique-and-wiki.md
    - .loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md
    - .loom/evidence/20260502-critique-closure-gate-validation.md
    - .loom/packets/ralph/20260502T221504Z-ticket-critgate2-iter-01.md
parent_merge_scope:
  records:
    - ticket:critgate2
    - evidence:critique-closure-gate-validation
    - packet:ralph-ticket-critgate2-20260502T221504Z
  paths: []
source_fingerprint:
  git_commit: 52cc82e344dd82d1fb37a584f59ce8c3f20f5a8e
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: 52cc82e344dd82d1fb37a584f59ce8c3f20f5a8e
  git_status_summary: clean
  compiled_from:
    - initiative:skills-corpus-template-grammar-safety-pass
    - plan:skills-corpus-template-grammar-safety-pass
    - ticket:critgate2
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
  max_source_files: 5
  max_excerpt_lines_per_file: 140
  avoid_full_file_reads: false
sources:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
  ticket:
    - ticket:critgate2
  records:
    - skills/loom-bootstrap/references/07-validation-and-honesty.md
    - skills/loom-bootstrap/references/05-critique-and-wiki.md
links:
  ticket:
    - ticket:critgate2
---

# Mission

Tighten bootstrap closure wording so mandatory critique cannot be read as
deferrable before closure, while recommended critique retains ticket-owned
disposition flexibility.

# Bound Context

This is the second ticket in `plan:skills-corpus-template-grammar-safety-pass` and
covers `initiative:skills-corpus-template-grammar-safety-pass#OBJ-002`. Closure
authority stays with tickets; critique remains an adversarial review layer.

# Source Snapshot

Baseline commit: `52cc82e344dd82d1fb37a584f59ce8c3f20f5a8e`, matching
`origin/main`. Worktree was clean before packet creation.

Parent inspection found the main ambiguity in
`skills/loom-bootstrap/references/07-validation-and-honesty.md`: "required
critique has happened or is explicitly deferred". Bootstrap critique policy in
`05-critique-and-wiki.md` already distinguishes mandatory and recommended
closure effects and should stay aligned.

# Change Class

Declared as `protocol-authority`; risk is high because closure-gate wording
affects fail-closed acceptance.

# Verification Targets

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-002`
- `ticket:critgate2#ACC-001`
- `ticket:critgate2#ACC-002`
- `ticket:critgate2#ACC-003`
- `ticket:critgate2#ACC-004`

# Task For This Iteration

1. Capture before-state searches for required, mandatory, recommended, and
   deferred critique closure wording.
2. Update targeted bootstrap references so mandatory critique clearly blocks
   closure until the required review exists and open medium/high findings have
   ticket-owned disposition.
3. Preserve recommended critique flexibility: it may be completed, deferred, or
   not required only with ticket-owned rationale before closure.
4. Preserve optional critique behavior and ticket-owned acceptance authority.
5. Record `evidence:critique-closure-gate-validation` with before/after searches
   and `git diff --check`.
6. Update `ticket:critgate2` to `review_required` with evidence linked, claim
   matrix current, and next route `critique`.
7. Fill this packet's `# Child Output`. The parent will mark the packet consumed
   after reconciliation.

# Verification Posture

`observation-first`.

Capture before/after searches for `required critique`, `mandatory critique`,
`recommended critique`, `explicitly deferred`, `deferred`, `not_required`, and
closure blocking language. Run `git diff --check` after edits.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- the fix would make optional or recommended critique mandatory;
- the fix would move closure authority out of tickets;
- mandatory/recommended wording cannot be reconciled without broader policy
  change;
- the source fingerprint is materially stale before launch.

# Output Contract

Return outcome, files changed, records changed, before/after observation
commands/results, `git diff --check` result, residual risks, and ticket
recommendation. Include whether the ticket should proceed to mandatory oracle
critique with profiles `closure-honesty`, `operator-clarity`, and
`routing-safety`.

# Working Notes

Parent created this packet after confirming `ticket:pktsupp1` was closed and
pushed and the worktree was clean at the source fingerprint.

# Child Output

Outcome: `stop` — bounded implementation completed; next route is mandatory
critique.

Files changed:

- `skills/loom-bootstrap/references/07-validation-and-honesty.md`
- `skills/loom-bootstrap/references/05-critique-and-wiki.md`
- `.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md`
- `.loom/evidence/20260502-critique-closure-gate-validation.md`
- `.loom/packets/ralph/20260502T221504Z-ticket-critgate2-iter-01.md`

Records changed:

- `ticket:critgate2`
- `evidence:critique-closure-gate-validation`
- `packet:ralph-ticket-critgate2-20260502T221504Z`

Implementation summary:

- Replaced the ambiguous `required critique has happened or is explicitly
  deferred` done-condition with a policy split for mandatory, recommended, and
  optional critique.
- Tightened mandatory critique closure language in both bootstrap references so
  closure is blocked until the required review exists and open medium/high
  findings have ticket-owned disposition; deferral and `not_required` do not
  satisfy mandatory critique.
- Preserved recommended critique flexibility as `completed`, `deferred`, or
  `not_required` only with ticket-owned rationale before closure.
- Preserved optional critique as non-blocking unless a ticket, spec, plan, or
  human gate made it required, and kept ticket-owned acceptance authority intact.

Before observation command/result:

```bash
for pattern in 'required critique' 'mandatory critique' 'recommended critique' 'explicitly deferred' 'deferred' 'not_required' 'blocks `closed`' 'blocks closure' 'block closure'; do
  printf '\n### %s\n' "$pattern"
  rg -n -i "$pattern" \
    "skills/loom-bootstrap/references/07-validation-and-honesty.md" \
    "skills/loom-bootstrap/references/05-critique-and-wiki.md" \
    ".loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md" || true
done
```

Before result highlights:

- `07-validation-and-honesty.md:15` said `required critique has happened or is
  explicitly deferred`.
- `05-critique-and-wiki.md:90` already said mandatory critique blocks `closed`
  until the required review exists and every open medium/high finding has
  ticket-owned disposition.
- Recommended critique already allowed `completed`, `deferred`, or
  `not_required` with rationale in `05-critique-and-wiki.md:96-97` and had a
  shorter matching statement in `07-validation-and-honesty.md:127`.

After observation command/result: same command. Full output is recorded in
`evidence:critique-closure-gate-validation`.

After result highlights:

- `07-validation-and-honesty.md:15-24` now defines the required critique gate by
  policy class: mandatory, recommended, and optional.
- `07-validation-and-honesty.md:136-143` now states mandatory critique blocks
  closure until the required review exists and open medium/high findings have
  ticket-owned disposition, while recommended and optional critique retain their
  distinct closure effects.
- `05-critique-and-wiki.md:90-99` now explicitly says mandatory critique cannot
  be satisfied by deferral or `not_required`; recommended critique still allows
  `completed`, `deferred`, or `not_required` with ticket-owned rationale.

Validation:

- `git diff --check`: passed with no output.

Residual risks:

- Mandatory oracle critique has not yet run.
- No wiki/retrospective promotion decision has been made; ticket leaves both
  pending until after critique.

Ticket recommendation:

- Keep `ticket:critgate2` in `review_required`.
- Proceed to mandatory oracle critique with profiles `closure-honesty`,
  `operator-clarity`, and `routing-safety`.
- If critique passes with no unresolved findings, parent can consider moving the
  ticket toward `complete_pending_acceptance` or closure review after recording
  critique and retrospective/promotion disposition.

# Parent Merge Notes

Parent accepted the child output as scoped and routed the ticket to mandatory
oracle critique. Parent reconciliation normalized `ticket:critgate2` claim matrix
statuses to canonical claim-coverage vocabulary, expanded
`evidence:critique-closure-gate-validation` with standard support and validity
sections, and left the ticket in `review_required` because the required critique
has not yet run.
