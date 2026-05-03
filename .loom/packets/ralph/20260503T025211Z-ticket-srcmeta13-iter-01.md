---
id: packet:ralph-ticket-srcmeta13-20260503T025211Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:srcmeta13
mode: execution
change_class: documentation-explanation
risk_class: low
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-03T02:52:11Z
updated_at: 2026-05-03T02:53:57Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - None - child returns output only; parent reconciles ticket, evidence, critique, and packet status.
  paths:
    - skills/loom-research/references/source-handling.md
    - skills/loom-research/SKILL.md
parent_merge_scope:
  records:
    - ticket:srcmeta13
  paths:
    - .loom/tickets/20260503-srcmeta13-add-research-source-metadata-guidance.md
    - .loom/evidence/20260503-research-source-metadata-validation.md
    - .loom/critique/research-source-metadata-review.md
    - .loom/packets/ralph/20260503T025211Z-ticket-srcmeta13-iter-01.md
source_fingerprint:
  git_commit: 23305565fd7e4af907de38b70c35c940da122410
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: 23305565fd7e4af907de38b70c35c940da122410
  git_status_summary: clean
  git_status_detail: clean working tree at packet compile time
  compiled_from:
    - ticket:srcmeta13
    - plan:skills-corpus-residual-protocol-sharpening-pass
    - research:skills-corpus-residual-audit-synthesis
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
  max_source_files: 8
  max_excerpt_lines_per_file: 100
  avoid_full_file_reads: true
sources:
  constitution:
    - constitution:main
    - decision:0001
    - decision:0002
    - decision:0006
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  research:
    - research:skills-corpus-residual-audit-synthesis
  spec: []
  plan:
    - plan:skills-corpus-residual-protocol-sharpening-pass
  ticket:
    - ticket:srcmeta13
  files:
    - skills/loom-research/references/source-handling.md
    - skills/loom-research/SKILL.md
links: {}
---

# Mission

Fix `ticket:srcmeta13` by adding research source provenance and freshness
guidance for external or current sources without making research an evidence,
wiki, ticket, or acceptance owner.

# Bound Context

The governing plan is `plan:skills-corpus-residual-protocol-sharpening-pass`.
This ticket follows `ticket:evfresh8` in the strict sequential pass.

Keep these boundaries:

- research owns reusable investigations, tradeoffs, synthesis, conclusions, and
  recommendations;
- evidence owns observed artifacts and outputs;
- wiki owns accepted explanation;
- tickets own live execution and acceptance;
- do not require full raw source dumps in research records;
- do not add source-fetching automation, validators, schemas, CLIs, helper
  scripts, runtime enforcement, or new canonical owner layers.

# Source Snapshot

Current relevant state at baseline `2330556`:

- `skills/loom-research/references/source-handling.md` only says research can draw
  from repository records, code, tests, logs, operator notes, and web sources when
  current information matters.
- The source posture section says to name source quality when it varies, say when
  evidence is incomplete, and state assumptions.
- It does not give concrete metadata expectations for external/current sources,
  access date, provenance, freshness window, or recheck/invalidation triggers.
- `skills/loom-research/SKILL.md` already points readers to `source-handling.md`
  when external sources, current facts, or source quality matter.

# Change Class

Declared above as `documentation-explanation` with low risk, but oracle critique
is mandatory by continuing user instruction.

# Verification Targets

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-016`
- `ticket:srcmeta13#ACC-001`
- `ticket:srcmeta13#ACC-002`
- `ticket:srcmeta13#ACC-003`
- `ticket:srcmeta13#ACC-004`

# Task For This Iteration

Make the smallest corpus edits that satisfy `ticket:srcmeta13`:

1. Add source metadata guidance for external or current research sources,
   including access date and provenance.
2. Ask researchers to state source quality, freshness limits, and recheck or
   invalidation triggers when they matter.
3. Preserve owner boundaries between research synthesis, observed evidence,
   accepted wiki explanation, and ticket acceptance.
4. Keep the guidance Markdown-native and not automation-dependent.

Prefer changing `skills/loom-research/references/source-handling.md`. Touch
`skills/loom-research/SKILL.md` only if a small cross-reference adjustment is
needed.

Do not update Loom tickets, evidence, critique, or this packet. The parent will
reconcile those after inspecting the returned diff.

# Verification Posture

Declared above as `observation-first`.

Before editing, inspect/report current matches for `access date`, `provenance`,
`freshness`, `source quality`, `recheck`, `invalidation`, `evidence`, `wiki`, and
`ticket acceptance` in the write-scope files. After editing, report the same
targeted observations and whether `git diff --check` passes.

# Stop Conditions

Stop and report `blocked` or `escalate` if:

- governing records or child-write-scope files differ materially from this packet;
- the fix would make research own observed evidence, accepted wiki explanation,
  live ticket execution, critique verdicts, or ticket acceptance;
- the fix would require full raw source dumps in research records;
- the fix would add source-fetching automation, runtime validation, schemas,
  command wrappers, helper scripts, or new canonical owner layers;
- satisfying the ticket requires a broader research template redesign.

# Output Contract

Return:

- outcome (`continue|stop|blocked|escalate`);
- files changed;
- records changed (`None` expected);
- before/after observations and `git diff --check` result;
- self-review findings or concerns;
- blockers or residual risks;
- recommended ticket state and next route.

# Working Notes

Parent compiled from clean `main` at `2330556` after pushing `ticket:evfresh8`.

# Child Output

Outcome: stop

Files changed:

- `skills/loom-research/references/source-handling.md`

Records changed: None.

Before observations:

- `access date`, `provenance`, `freshness`, `recheck`, `invalidation`, and
  `ticket acceptance` had no matches in write-scope files.
- `source quality` matched existing guidance in `source-handling.md` and
  `SKILL.md`; `evidence` and `wiki` had existing owner/synthesis references.

After observations:

- Added matches for `access date`, `provenance`, `freshness`, `recheck`,
  `invalidation`, and `ticket acceptance` in `source-handling.md`.
- Preserved existing `source quality`, `evidence`, and `wiki` references and
  added boundary guidance for evidence/wiki/ticket acceptance ownership.

Validation: `git diff --check` passed with no output.

Self-review:

- Change stayed within the preferred file and child write scope.
- Guidance remains Markdown-native and does not require raw source dumps,
  automation, validators, schemas, CLIs, or helper scripts.
- Owner boundaries are explicit: research synthesizes/cites, evidence owns
  observed artifacts, wiki owns accepted explanation, and tickets own ticket
  acceptance.

Blockers/residual risks: no blockers. Parent still needs to reconcile ticket,
evidence, critique, and packet status.

Recommendation: set ticket to `review_required`; next route is parent-side
critique/acceptance review, then ticket reconciliation.

# Parent Merge Notes

Accepted child output as in scope. Parent reviewed the diff, recorded evidence
`evidence:research-source-metadata-validation`, moved `ticket:srcmeta13` to
`review_required`, and routed next to mandatory oracle critique.
