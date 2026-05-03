---
id: packet:ralph-ticket-routewf10-20260502T234101Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:routewf10
mode: execution
change_class: protocol-authority
risk_class: medium
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-02T23:41:02Z
updated_at: 2026-05-02T23:46:47Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - ticket:routewf10
    - evidence:workflow-route-token-validation
    - packet:ralph-ticket-routewf10-20260502T234101Z
  paths:
    - skills/loom-records/references/route-vocabulary.md
    - skills/loom-tickets/templates/ticket.md
    - skills/loom-tickets/references/readiness.md
    - skills/loom-workspace/references/routing.md
    - skills/loom-workspace/references/status-snapshot.md
    - skills/loom-drive/references/drive-loop.md
    - skills/loom-drive/references/tranche-decision-protocol.md
    - skills/**/SKILL.md
    - .loom/tickets/20260502-routewf10-audit-workflow-route-tokens.md
    - .loom/evidence/20260502-workflow-route-token-validation.md
    - .loom/packets/ralph/20260502T234101Z-ticket-routewf10-iter-01.md
parent_merge_scope:
  records:
    - ticket:routewf10
    - evidence:workflow-route-token-validation
    - packet:ralph-ticket-routewf10-20260502T234101Z
  paths:
    - skills/loom-records/references/route-vocabulary.md
    - skills/loom-tickets/templates/ticket.md
    - skills/loom-tickets/references/readiness.md
    - skills/loom-workspace/references/routing.md
    - skills/loom-drive/references/checkpoint-resume-protocol.md
    - skills/loom-drive/references/continuity-contract.md
    - skills/loom-drive/references/drive-loop.md
    - skills/loom-drive/references/tranche-decision-protocol.md
    - skills/loom-drive/templates/outer-loop-handoff.md
    - .loom/tickets/20260502-routewf10-audit-workflow-route-tokens.md
    - .loom/evidence/20260502-workflow-route-token-validation.md
    - .loom/packets/ralph/20260502T234101Z-ticket-routewf10-iter-01.md
source_fingerprint:
  git_commit: 3bfbe9226ecf2001fc5fd1d07d9efb999f8d156d
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: 3bfbe9226ecf2001fc5fd1d07d9efb999f8d156d
  git_status_summary: clean
  compiled_from:
    - initiative:skills-corpus-template-grammar-safety-pass
    - plan:skills-corpus-template-grammar-safety-pass
    - ticket:routewf10
execution_context:
  branch: main
  push_remote: origin
  worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
  isolation: none
  git_shared_metadata_mutations: forbidden
  destructive_commands: forbidden
  network: forbidden
context_budget:
  posture: normal
  max_source_files: 16
  max_excerpt_lines_per_file: 180
  avoid_full_file_reads: false
sources:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
  ticket:
    - ticket:routewf10
  records:
    - skills/loom-records/references/route-vocabulary.md
    - skills/loom-tickets/templates/ticket.md
    - skills/loom-tickets/references/readiness.md
    - skills/loom-workspace/references/routing.md
    - skills/loom-workspace/references/status-snapshot.md
    - skills/loom-drive/references/drive-loop.md
    - skills/loom-drive/references/tranche-decision-protocol.md
links:
  ticket:
    - ticket:routewf10
---

# Mission

Audit and align workflow route-token guidance so first-class workflow
coordinators such as ship, spike, codemap, and debugging are either represented
in shared route vocabulary or explicitly routed through existing canonical tokens.

# Bound Context

This is the tenth ticket in `plan:skills-corpus-template-grammar-safety-pass` and
covers `initiative:skills-corpus-template-grammar-safety-pass#OBJ-010`. Route
tokens are grep-friendly Markdown vocabulary, not a runtime enum, command router,
or new owner layer.

# Source Snapshot

Baseline commit: `3bfbe9226ecf2001fc5fd1d07d9efb999f8d156d`, matching
`origin/main`. Worktree was clean before packet creation.

Parent inspection found `skills/loom-records/references/route-vocabulary.md`
currently names owner-layer and core execution/review tokens but not explicit
tokens for `debugging`, `spike`, `codemap`, or `ship`. Related references such as
workspace routing already name these as workflow coordinators.

# Change Class

Declared as `protocol-authority`; risk is medium because route-token guidance can
accidentally become a runtime enum or leave first-class workflow moves
inconsistent across templates and references.

# Verification Targets

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-010`
- `ticket:routewf10#ACC-001`
- `ticket:routewf10#ACC-002`
- `ticket:routewf10#ACC-003`
- `ticket:routewf10#ACC-004`

# Task For This Iteration

1. Capture before-state searches for `ship`, `spike`, `codemap`, `debugging`,
   route-token lists, and route-field examples across `skills/`.
2. Audit shared route vocabulary and dependent route-token lists/examples.
3. Add or clarify route tokens only for existing first-class workflow moves that
   need a route value; if an existing token is the correct route, say so rather
   than adding a synonym.
4. Align downstream route-token examples/lists with
   `skills/loom-records/references/route-vocabulary.md`.
5. Preserve the non-runtime framing: no validator, enum, router, CLI, command
   wrapper, hidden helper, or new owner layer.
6. Update `ticket:routewf10` to `review_required` with evidence linked, claim
   matrix current, and next route `critique`.
7. Record `evidence:workflow-route-token-validation` with before/after searches,
   rationale for unchanged noisy hits, and `git diff --check`.
8. Fill this packet's `# Child Output`. The parent will replace the
   `parent_merge_scope.paths` placeholder with concrete reconciled paths and mark
   the packet consumed after reconciliation.

# Verification Posture

`observation-first`.

Capture route-token searches before and after the edit, plus `git diff --check`.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- the audit requires changing Loom's layer model or creating a new owner layer;
- the fix would turn route tokens into a runtime enum, command router, or command
  wrapper surface;
- the fix would turn every skill display name into a route token;
- the correct handling of a workflow coordinator requires new product direction
  not already present in the initiative, plan, or skill corpus;
- the source fingerprint is materially stale before launch.

# Output Contract

Return outcome, files changed, records changed, before/after observation
commands/results, `git diff --check` result, residual risks, self-review
concerns, and ticket recommendation. Include whether the ticket should proceed to
mandatory oracle critique with profiles `routing-safety`, `operator-clarity`, and
`records-grammar`.

# Working Notes

Parent created this packet after confirming `ticket:critrec9` was closed and
pushed and the worktree was clean at the source fingerprint.

# Child Output

Outcome: `stop` — bounded iteration complete; ticket should proceed to mandatory
oracle critique.

Files changed:

- `skills/loom-records/references/route-vocabulary.md`
- `skills/loom-tickets/templates/ticket.md`
- `skills/loom-tickets/references/readiness.md`
- `skills/loom-workspace/references/routing.md`
- `skills/loom-drive/references/checkpoint-resume-protocol.md`
- `skills/loom-drive/references/continuity-contract.md`
- `skills/loom-drive/templates/outer-loop-handoff.md`
- `skills/loom-drive/references/drive-loop.md`
- `skills/loom-drive/references/tranche-decision-protocol.md`
- `.loom/evidence/20260502-workflow-route-token-validation.md`
- `.loom/tickets/20260502-routewf10-audit-workflow-route-tokens.md`
- `.loom/packets/ralph/20260502T234101Z-ticket-routewf10-iter-01.md`

Records changed:

- `ticket:routewf10`
- `evidence:workflow-route-token-validation`
- `packet:ralph-ticket-routewf10-20260502T234101Z`

Before observations:

- `git rev-parse HEAD && git status --short` returned HEAD
  `3bfbe9226ecf2001fc5fd1d07d9efb999f8d156d` with the parent-created ticket
  modification and untracked packet present.
- `rg -n "ship|spike|codemap|debugging" "skills"` showed these workflow
  coordinators existed in skill and workspace guidance but were absent from the
  shared route-token table and dependent route-value lists.
- `rg -n 'next route:|Route:|proposed next route:|route-priority|route token|route-token|allowed-token|shared route vocabulary|Canonical Route Tokens|Use \`skills/loom-records/references/route-vocabulary.md\`' "skills"`
  showed route lists/examples omitted `debugging`, `spike`, `codemap`, and
  `ship`.

After observations:

- `rg -n "ship|spike|codemap|debugging" "skills"` found the four tokens in
  route vocabulary, downstream route lists, workspace routing, and drive
  decision/reconciliation guidance; remaining noisy hits are ordinary prose,
  skill names, `shipped`/`shipping`, `ownership`, or `relationship`.
- `rg -n 'next route:|Route:|proposed next route:|route-priority|route token|route-token|allowed-token|shared route vocabulary|Canonical Route Tokens|Use \`skills/loom-records/references/route-vocabulary.md\`' "skills"`
  found updated route-bearing surfaces; the remaining `skills/loom-plans` prose
  hit is not a route-value field and was outside child write scope.
- Targeted touched-surface search found `debugging`, `spike`, `codemap`, and
  `ship` in the canonical vocabulary and aligned route lists.

`git diff --check`: passed with no output.

Residual risks / self-review concerns:

- The route-decision priority now names workflow coordinator routes, but oracle
  critique should verify their ordering against owner-layer routing semantics.
- `skills/loom-plans/references/slicing.md` still uses prose labels such as
  "local edit" and "Ralph packet"; this appears non-route-field prose and was
  outside write scope.

Ticket recommendation: keep `ticket:routewf10` in `review_required`, next route
`critique`, and run mandatory oracle critique with profiles `routing-safety`,
`operator-clarity`, and `records-grammar`.

# Parent Merge Notes

2026-05-02T23:46:47Z: Parent accepted the route-token alignment for review and
reconciled it into `ticket:routewf10`,
`evidence:workflow-route-token-validation`, and this packet. Parent replaced the
merge-scope placeholder with concrete paths and marked the packet `consumed`.

Scope note: the child updated `skills/loom-drive/references/checkpoint-resume-protocol.md`,
`skills/loom-drive/references/continuity-contract.md`, and
`skills/loom-drive/templates/outer-loop-handoff.md`, which were dependent
route-list/example files named by the ticket and packet task body but omitted
from the packet frontmatter `child_write_scope.paths`. Parent manually reviewed
and retained those edits as parent-reconciled changes because they are necessary
for `ticket:routewf10#ACC-002` alignment. Mandatory oracle critique must review
this scope reconciliation before closure.
