---
id: packet:ralph-ticket-cmdroute-20260502T213017Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:cmdroute
mode: execution
change_class: record-hygiene
risk_class: medium
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-02T21:30:17Z
updated_at: 2026-05-02T21:33:52Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - ticket:cmdroute
    - evidence:command-route-wording-validation
    - packet:ralph-ticket-cmdroute-20260502T213017Z
  paths:
    - skills/**
    - README.md
    - .loom/tickets/20260502-cmdroute-remove-command-route-ambiguity.md
    - .loom/evidence/20260502-command-route-wording-validation.md
    - .loom/packets/ralph/20260502T213017Z-ticket-cmdroute-iter-01.md
parent_merge_scope:
  records:
    - ticket:cmdroute
    - evidence:command-route-wording-validation
    - packet:ralph-ticket-cmdroute-20260502T213017Z
  paths: []
source_fingerprint:
  git_commit: 0458921db7377783651abd73a00159a6bbcf289d
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: 0458921db7377783651abd73a00159a6bbcf289d
  git_status_summary: clean
  compiled_from:
    - initiative:skills-corpus-council-precision-pass
    - plan:skills-corpus-council-precision-pass
    - ticket:cmdroute
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
  max_excerpt_lines_per_file: 120
  avoid_full_file_reads: false
sources:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
  ticket:
    - ticket:cmdroute
  records:
    - skills/loom-records/references/route-vocabulary.md
links:
  ticket:
    - ticket:cmdroute
---

# Mission

Remove product-surface wording that presents optional commands, command surfaces,
or adapters as peers to Loom owner layers or workflow routes.

# Bound Context

This is the final hygiene ticket in
`plan:skills-corpus-council-precision-pass`. It exists to satisfy
`initiative:skills-corpus-council-precision-pass#OBJ-012` without changing
Loom's no-runtime, no-command-truth doctrine.

`skills/loom-records/references/route-vocabulary.md` owns the shared route-token
grammar. It explicitly says command or adapter names are non-routes: commands may
transport a route, but owner records and workflow skills own Loom truth.

# Source Snapshot

Baseline commit: `0458921db7377783651abd73a00159a6bbcf289d` on `main`, matching
`origin/main` after parent refresh. Worktree was clean before packet creation.

Parent before-state searches found these product-surface route-peer phrases:

- `skills/loom-workspace/references/status-snapshot.md`: "Recommend the next owner layer, workflow, or optional command" and "best next owner layer, workflow, or optional command and why".
- `skills/loom-wiki/references/wiki-write.md`: "recommended next owner layer, workflow, or optional command".
- `skills/loom-wiki/references/wiki-audit.md`: "recommended next owner layer, workflow, or optional command per finding".

Legitimate command/adapter doctrine should remain when it clearly says commands
are invocation adapters, transport, or non-routes. Do not remove shell-command
examples or no-command-truth guidance.

# Change Class

Declared as `record-hygiene` with `risk_class: medium`. The mutation is textual
but affects operator routing clarity, so use observation-first structural
validation and mandatory oracle critique afterward.

# Verification Targets

- `initiative:skills-corpus-council-precision-pass#OBJ-012`
- `ticket:cmdroute#ACC-001`
- `ticket:cmdroute#ACC-002`
- `ticket:cmdroute#ACC-003`
- `ticket:cmdroute#ACC-004`

# Task For This Iteration

1. Search `skills/**/*.md` and `README.md` for command/adaptor wording that treats
   optional commands, command surfaces, slash commands, harness commands, MCPs,
   or adapters as peers to owner layers, workflows, or route values.
2. Replace only route-peer phrasing with owner-layer/workflow-route wording.
3. Keep remaining command/adapter references clearly framed as transport,
   invocation convenience, shell examples, or non-route/non-truth guidance.
4. Preserve the shared route vocabulary and no-runtime/no-command-wrapper-truth
   doctrine.
5. Create or update `evidence:command-route-wording-validation` with before/after
   search results and `git diff --check`.
6. Update `ticket:cmdroute` to `review_required` with evidence linked, claim
   matrix statuses current, and next route `critique`.
7. Fill this packet's `# Child Output`. The parent will move packet frontmatter
   from `compiled` to `consumed` during reconciliation.

# Verification Posture

`observation-first`.

Capture before-state search output before editing, then after-state search output
showing no remaining product guidance presents optional commands as route peers.
Run `git diff --check` after edits. Evidence should state limits: structural
searches do not prove every future phrasing choice, but they cover the known
route-peer wording patterns.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- changing the wording would require new product direction beyond this ticket;
- a command surface appears to own protocol truth in a way that needs
  constitution or initiative changes;
- the fix would add a runtime, command wrapper, helper dependency, or new owner
  layer;
- the shared route vocabulary seems insufficient for the wording repair;
- the source fingerprint is materially stale before launch.

# Output Contract

Return outcome, files changed, records changed, before/after observation
commands/results, `git diff --check` result, residual risks, and ticket
recommendation. Include whether the ticket should proceed to mandatory oracle
critique with profiles `operator-clarity`, `routing-safety`, and
`records-grammar`.

# Working Notes

Parent created this packet after confirming `ticket:cmdroute` dependencies were
closed in prior work and the current branch was clean at the source fingerprint.

# Child Output

Outcome: `stop` — bounded wording hygiene completed and ticket is ready for
mandatory critique.

Files changed:

- `skills/loom-workspace/references/status-snapshot.md`
- `skills/loom-wiki/references/wiki-write.md`
- `skills/loom-wiki/references/wiki-audit.md`

Records changed:

- `ticket:cmdroute`
- `evidence:command-route-wording-validation`
- `packet:ralph-ticket-cmdroute-20260502T213017Z` child output only

Before observation commands/results:

```bash
rg -n "optional command|owner layer, workflow|workflow, or optional command" skills README.md
```

```text
skills/loom-wiki/references/wiki-write.md:43:- recommended next owner layer, workflow, or optional command
skills/loom-wiki/references/wiki-audit.md:46:- recommended next owner layer, workflow, or optional command per finding
skills/loom-workspace/references/status-snapshot.md:24:6. Recommend the next owner layer, workflow, or optional command. When naming a
skills/loom-workspace/references/status-snapshot.md:137:- best next owner layer, workflow, or optional command and why
```

```bash
rg -n -i "(owner layers?.{0,80}(command|adapter|adaptor|mcp)|workflows?.{0,80}(command|adapter|adaptor|mcp)|(command|adapter|adaptor|mcp).{0,80}(owner layers?|workflow|route value|route token|route))" skills README.md
```

Result included the four route-peer matches above plus legitimate non-runtime,
non-route, transport, and inspection references recorded in
`evidence:command-route-wording-validation`.

After observation commands/results:

```bash
rg -n "optional command|owner layer, workflow|workflow, or optional command" skills README.md
```

No output.

```bash
rg -n -i "(owner layers?.{0,80}(command|adapter|adaptor|mcp)|workflows?.{0,80}(command|adapter|adaptor|mcp)|(command|adapter|adaptor|mcp).{0,80}(owner layers?|workflow|route value|route token|route))" skills README.md
```

Remaining output is recorded in
`evidence:command-route-wording-validation`; the matches are framed as
non-runtime doctrine, command/adaptor non-route guidance, invocation transport,
or ordinary atlas inspection examples.

`git diff --check`: produced no output and exited successfully.

Residual risks: structural searches cannot prove every possible future phrasing
choice, but they cover the known route-peer wording and related command/adaptor
route terms in `skills/` and `README.md`.

Ticket recommendation: keep `ticket:cmdroute` in `review_required` and proceed to
mandatory oracle critique with profiles `operator-clarity`, `routing-safety`, and
`records-grammar`.

# Parent Merge Notes

Parent accepted the bounded wording hygiene result for critique handoff. The
iteration removed optional-command route-peer phrasing from workspace and wiki
guidance, recorded structural evidence with before/after searches and
`git diff --check`, and left `ticket:cmdroute` in `review_required` for mandatory
oracle critique. Parent marked packet frontmatter `status: consumed` during
reconciliation.
