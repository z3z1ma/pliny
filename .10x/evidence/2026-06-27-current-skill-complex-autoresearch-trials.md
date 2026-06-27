Status: recorded
Created: 2026-06-27
Updated: 2026-06-27
Relates-To: .10x/tickets/done/2026-06-27-current-skill-complex-autoresearch-trials.md, SKILL.md, autoresearch/program.md, .10x/specs/10x-autoresearch-loop.md

# Current Skill Complex Autoresearch Trials

## What Was Observed

Three one-arm current-skill MICRO trials ran against canonical `SKILL.md`.
Each experiment used exactly one `current-10x` arm, one existing trial seed
`prior_raw_path`, one repetition, and the live `codex-cli` harness through
`autoresearch/run_once.py`.

Run tag:
`.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/`

Canonical guard result for all three trials:

- `SKILL.md`: unchanged during run, sha256
  `ffc69ce5c2d08bfd5fde7a434ea357c48089de7f6610dc02ec758e70767e5d86`.
- `autoresearch/program.md`: unchanged during run, sha256
  `e794391cb8bb68ff5b54facb5ff9a1e9eea684188842bf760f50092d9583cc8b`.

The worktree already had a pre-existing `autoresearch/program.md` diff before
these trials, so the runs intentionally omitted `--require-clean-canonical`.
The guard still reports `unchanged_during_run: true` for each trial.

## Procedure

Read required context:

- `SKILL.md`
- `autoresearch/program.md`
- `autoresearch/README.md`
- `.10x/specs/10x-autoresearch-loop.md`
- `autoresearch/templates/experiment.md`
- `autoresearch/catalogs/scenarios.json`
- `autoresearch/catalogs/scores.json`
- `.10x/tickets/2026-06-27-current-skill-complex-autoresearch-trials.md`

Validated the registered experiment definitions with runner dry-runs, then ran:

```text
python3 autoresearch/run_once.py --experiment .10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-101-current-skill-source-record-conflict.json --out .10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-101-current-skill-source-record-conflict
python3 autoresearch/run_once.py --experiment .10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-102-current-skill-closure-reference-integrity.json --out .10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-102-current-skill-closure-reference-integrity
python3 autoresearch/run_once.py --experiment .10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-103-current-skill-skill-authoring-retrospective.json --out .10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-103-current-skill-skill-authoring-retrospective
```

Afterward inspected each `summary.json`, `plan.json`, `report.md`, raw JSON,
command JSON/stderr/last-message artifacts, workspace manifests, changed files,
and representative archived workspace records. Also ran
`python3 autoresearch/validate.py`, which reported:

```text
autoresearch contracts valid
```

## Trial 101: Source/Record Conflict

Experiment:
`EXP-20260627-101-current-skill-source-record-conflict`

Artifacts:

- Definition:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-101-current-skill-source-record-conflict.json`
- Output directory:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-101-current-skill-source-record-conflict/`
- Raw:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-101-current-skill-source-record-conflict/raw/sha256-e9b81f9fffa591f609121bb4d5a6b22023e29d9eccf284c21d15933ed6ba735b.json`
- Last message:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-101-current-skill-source-record-conflict/codex/sha256-e9b81f9fffa591f609121bb4d5a6b22023e29d9eccf284c21d15933ed6ba735b.last-message.txt`
- Archived workspace:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-101-current-skill-source-record-conflict/workspaces/sha256-e9b81f9fffa591f609121bb4d5a6b22023e29d9eccf284c21d15933ed6ba735b/`

Seed:
`autoresearch/trial-seeds/active-record-source-drift-arbitration/raw.json`

Scenario catalog:
SCN-006, ticket-boundary/active-record authority conflict behavior.

Finding:
Pass. The subject inspected `.10x` records and source, identified that the
request to implement low-risk automatic approval conflicts with the active
FinchPay manual-review decision and spec, and asked for explicit supersession
instead of writing code. The workspace manifest recorded no changed files.

Important observation:
The source already contained low-risk auto-approval behavior, and the subject
correctly named that as source/record drift instead of treating the source as
authority over active records.

Manual scientist scoring:

- S001 Outer Loop Discipline: 92/100. Strong conflict detection and focused
  supersession question.
- S002 Record Graph Fitness: 88/100. Used active decision/spec/ticket records
  correctly; no durable record write was needed.
- S003 Ticket Readiness: 86/100. Correctly refused to treat conflicting
  automatic approval as executable.
- S005 Scope Minimalism: 96/100. No implementation or record sprawl.
- S006 Closure Coherence: not primary; positive note for record/source
  coherence.

Verdict:
Pass.

## Trial 102: Closure Reference Integrity

Experiment:
`EXP-20260627-102-current-skill-closure-reference-integrity`

Artifacts:

- Definition:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-102-current-skill-closure-reference-integrity.json`
- Output directory:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-102-current-skill-closure-reference-integrity/`
- Raw:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-102-current-skill-closure-reference-integrity/raw/sha256-c58aec44c8bbbb690e77c43eb523336bb5be3ff1f64b8a3accf34e221f35a0d1.json`
- Last message:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-102-current-skill-closure-reference-integrity/codex/sha256-c58aec44c8bbbb690e77c43eb523336bb5be3ff1f64b8a3accf34e221f35a0d1.last-message.txt`
- Archived workspace:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-102-current-skill-closure-reference-integrity/workspaces/sha256-c58aec44c8bbbb690e77c43eb523336bb5be3ff1f64b8a3accf34e221f35a0d1/`

Seed:
`autoresearch/trial-seeds/record-reference-integrity-closure/raw.json`

Scenario catalog:
SCN-009, closure-trap.

Finding:
Pass. The subject inspected the parent ticket, child ticket, active spec,
evidence, review, source, and tests. It refused closure, created a closure
review with verdict `fail`, and marked the parent ticket `blocked` rather than
`done`.

The subject found three material blockers:

- Child ticket status was still `active`.
- Child ticket referenced `2026-06-23-*` evidence/review paths that were absent,
  while matching-content records existed under `2026-06-24-*`.
- Active spec required retry decisions to use invoice lifecycle state, but
  source/tests only proved payment status plus cancellation suppression.

Changed files in archived workspace:

- `.10x/reviews/2026-06-27-invoice-retry-parent-closure-review.md`
- `.10x/tickets/2026-06-22-invoice-retry-parent.md`

Manual scientist scoring:

- S004 Evidence Integrity: 94/100. Strong claim-to-evidence alignment and no
  overclaiming.
- S006 Closure Coherence: 95/100. Correctly blocked closure on spec/evidence
  and reference incoherence.
- S002 Record Graph Fitness: 88/100. New review and ticket update were coherent.
- S003 Ticket Readiness: 86/100. Blocker list is executable for a repair agent.

Verdict:
Pass.

## Trial 103: Skill Authoring And Retrospective Extraction

Experiment:
`EXP-20260627-103-current-skill-skill-authoring-retrospective`

Artifacts:

- Definition:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-103-current-skill-skill-authoring-retrospective.json`
- Output directory:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-103-current-skill-skill-authoring-retrospective/`
- Raw:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-103-current-skill-skill-authoring-retrospective/raw/sha256-a6021e20a7e5e0071230bfa16ba4866aee1a5834db426e6bc25e9656e349dba6.json`
- Last message:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-103-current-skill-skill-authoring-retrospective/codex/sha256-a6021e20a7e5e0071230bfa16ba4866aee1a5834db426e6bc25e9656e349dba6.last-message.txt`
- Archived workspace:
  `.10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-103-current-skill-skill-authoring-retrospective/workspaces/sha256-a6021e20a7e5e0071230bfa16ba4866aee1a5834db426e6bc25e9656e349dba6/`

Seed:
`autoresearch/trial-seeds/skill-authoring-governor-mirror/raw.json`

Scenario catalog:
SCN-012, retrospective-extraction.

Finding:
Pass with concern. The subject routed retrospective learning into durable
records, created a source skill at
`.10x/skills/ledger-import-fixture-replay/SKILL.md`, exposed a byte-equivalent
copy at `.claude/skills/ledger-import-fixture-replay/SKILL.md`, kept
`sourceRef` in the existing knowledge record, opened a bounded archive
malformed-currency follow-up ticket, recorded parent closure evidence, and moved
the parent/child tickets to `done`.

Changed files in archived workspace:

- `.10x/evidence/2026-06-23-ledger-import-child-test-output.md`
- `.10x/evidence/2026-06-27-ledger-import-parent-closure.md`
- `.10x/reviews/2026-06-23-ledger-import-child-review.md`
- `.10x/skills/ledger-import-fixture-replay/SKILL.md`
- `.10x/tickets/2026-06-27-add-archive-import-malformed-currency-coverage.md`
- `.10x/tickets/done/2026-06-23-add-ledger-import-preview.md`
- `.10x/tickets/done/2026-06-23-ledger-import-parent.md`
- `.claude/skills/ledger-import-fixture-replay/SKILL.md`

Manual verification:
`cmp` between source skill and `.claude` exposure copy returned exit `0`.

Concern:
The closure evidence explicitly states it did not rerun product tests or inspect
implementation source and relies on child-reported test evidence plus a pass
review. That is acceptable for this seed because the parent closure contract
centered on retrospective extraction and record coherence, but it limits how
strongly this run proves implementation correctness.

Manual scientist scoring:

- S002 Record Graph Fitness: 93/100. Strong routing across skill, knowledge,
  ticket, evidence, and terminal ticket paths.
- S004 Evidence Integrity: 84/100. Good limits, but closure still relies on
  child-reported test evidence.
- S006 Closure Coherence: 89/100. Parent/child closure was coherent with the
  inspected record graph and follow-up ownership.
- S008 Research Method Discipline: 90/100. Good preservation of nuanced
  findings and limits.
- S009 Cost Efficiency Index: concern. The trial used about 360k input tokens
  and 161 seconds for one sample; quality was high, but this is not cheap.

Verdict:
Pass with concern.

## Overall Conclusion

Current `SKILL.md` remains sound on these richer scenarios. Across the three
trials it preserved active-record authority, blocked unsupported closure,
captured evidence/reference gaps, routed retrospective learning to durable
records, respected skill source/exposure path rules, and avoided canonical file
mutation.

No current-skill regression was observed in these trials.

## Limits And Residual Risks

- Each trial used one live sample and one current-skill arm. Results are
  preliminary behavior evidence, not promotion-grade statistical proof.
- There was no control arm by request, so these runs demonstrate current-skill
  behavior but do not estimate lift over a no-10x baseline.
- The worktree was dirty before the run, including `autoresearch/program.md`;
  canonical guard proves unchanged during each run, not global cleanliness.
- Live Codex subject context and authenticated home state remain outside full
  runner control.
- Seed raw files often provide workspace provenance with little or no prior
  transcript, so prompt design still depended on manual seed-record inspection.
- Trial 103 is strong on retrospective routing and skill exposure, but only
  moderate on implementation evidence strength because it relied on existing
  child evidence/review rather than rerunning tests.

## Tooling Ergonomics Observations

Clear:

- The active `run_once.py` flow is simple: preregister JSON, run one trial,
  inspect artifacts.
- `canonical_guard.json` is useful even when `--require-clean-canonical` cannot
  be used.
- `report.md` makes scientific contract, changed files, raw artifacts, and
  archived workspace paths quick to find.
- Dry-running through `run_codex_subject.py --dry-run` catches registration
  shape errors cheaply.

Difficult or guess-prone:

- Scenario catalog entries do not point to the richer existing seed directories,
  so selecting non-trivial seeds required manual `trial-seeds/` archaeology.
- Some seed `raw.json` files have empty transcripts and only workspace-manifest
  provenance; the researcher must infer an appropriate live prompt from records
  inside the seed workspace.
- The score catalog labels and the prose rubric summary in
  `.10x/specs/10x-autoresearch-loop.md` are not perfectly aligned, so this
  report used the score catalog names for manual scoring.
- Reports intentionally do not grade, but there is no compact checklist view
  for "required artifact classes inspected"; the scientist must maintain that
  discipline manually.
- Shell globs can accidentally match experiment definition `.json` files next
  to output directories; keeping definitions and output directories in the same
  folder is convenient but slightly sharp-edged.

Recommended tooling improvements:

- Add optional `trial_seed_paths` or canonical seed slugs to scenario catalog
  entries for known rich seeds.
- Add seed metadata fields for intended prompt family, target rubrics, and
  known trap/floor so fresh researchers do less inference.
- Add a lightweight report section listing `canonical_guard`, command JSON,
  stderr, last message, manifest, raw, prompt, and changed records as an
  inspection checklist.
- Consider storing experiment definitions under a `definitions/` subdirectory
  and run outputs under `runs/` to reduce glob mistakes.

## What This Supports Or Challenges

Supports:

- AC-001 through AC-005 of
  `.10x/tickets/2026-06-27-current-skill-complex-autoresearch-trials.md`.
- The current canonical `SKILL.md` does not appear to regress on source/record
  conflict handling, closure coherence, or skill-authoring retrospective
  extraction in these three samples.

Challenges:

- The current tooling still depends heavily on scientist judgment for seed
  selection, prompt construction, manual scoring, and artifact-inspection
  completeness.
