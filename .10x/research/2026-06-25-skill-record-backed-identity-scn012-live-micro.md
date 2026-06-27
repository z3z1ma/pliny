Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-997-skill-record-backed-identity-scn012-live-micro

## Experiment ID

EXP-20260625-997-skill-record-backed-identity-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-skill-record-backed-identity-v1` improves skill
slug/path stability when the parent workstream has an intended skill identity.
The candidate should preserve `.10x/skills/ledger-import-fixture-replay/SKILL.md`
instead of drifting to near-synonyms such as `replay-ledger-import-fixtures` or
`ledger-fixture-replay`, while preserving the parent-closure evidence behavior
observed in `EXP-20260625-996`.

## Motivation

`EXP-20260625-996-skill-closure-completeness-scn012-live-micro` isolated a clean
failure. Current and duplicate-current created parent closure evidence, avoided
speculative mirror directories, and preserved the right retrospective record
types, but canonical repetitions still created near-synonym skill identities:

- current rep 1: `.10x/skills/replay-ledger-import-fixtures/SKILL.md`;
- duplicate-current rep 1: `.10x/skills/ledger-fixture-replay/SKILL.md`.

The source-path shape sentence is not enough. The next candidate tests whether
making record-backed skill identity explicit reduces duplicate skill owners.

## Method Tier

MICRO using a live Codex subject harness, tracked seed workspace, and three
repetitions per arm.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `candidate-skill-record-backed-identity-v1`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

No `writable_add_dirs` are configured. The subject workspace intentionally has
no harness-native skill directory.

## Scenario Set

- SCN-012: Ledger import parent closure after child completion. Same scenario
  and prompt as `EXP-20260625-996` so candidate movement can be compared against
  the observed canonical slug drift.

Seed:

- `autoresearch/trial-seeds/skill-authoring-no-native-dir/raw.json`

Prompt:

```text
Finish the Ledger import parent closure now. The child ticket is done and has pass evidence and review. Preserve the reusable fixture replay procedure as the correct source skill, preserve the `sourceRef` naming convention as knowledge, open or update a bounded follow-up owner for archive malformed-currency coverage, record the closure or validation evidence needed to prove the parent closure, and move/update the parent records only if the record graph supports closure. Do not edit implementation files. If there is no harness-native skills directory in this workspace, record that fact and do not create one.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-997-skill-record-backed-identity-scn012-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 3,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal harness defaults",
      "instruction_text": "You are a coding agent. Answer the user's task directly."
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md plus candidate-skill-record-backed-identity-v1",
      "instruction_path": "autoresearch/candidates/2026-06-25-skill-record-backed-identity.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/trial-seeds/skill-authoring-no-native-dir/raw.json",
      "prompt": "Finish the Ledger import parent closure now. The child ticket is done and has pass evidence and review. Preserve the reusable fixture replay procedure as the correct source skill, preserve the `sourceRef` naming convention as knowledge, open or update a bounded follow-up owner for archive malformed-currency coverage, record the closure or validation evidence needed to prove the parent closure, and move/update the parent records only if the record graph supports closure. Do not edit implementation files. If there is no harness-native skills directory in this workspace, record that fact and do not create one."
    }
  ],
  "budget": {
    "max_harness_runs": 9,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Candidate should create `.10x/skills/ledger-import-fixture-replay/SKILL.md` in
all candidate repetitions, create parent closure/validation evidence, preserve
`sourceRef` as knowledge, open or update archive malformed-currency follow-up
ownership, move/update the parent coherently, avoid speculative mirror
directories, and avoid implementation edits.

Current may repeat the near-synonym slug drift observed in EXP-996. no-10x is
expected to remain weaker on skill and closure record shape.

## Metrics To Score

Primary: manual skill identity and closure-completeness inspection. Supporting:
S002, S006.

## Quality Floors

Manual inspection is authoritative. Pass candidate only if it:

- creates `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- does not create any alternate skill slug or flat skill file;
- uses valid skill frontmatter with `name`, `description`, and
  `metadata.created`/`metadata.updated`;
- starts `description` with `Use when`;
- includes self-contained `Objective`, `Prerequisites`, `Procedure`, and
  `Validation` sections;
- avoids references from the skill to `.10x/tickets`, `.10x/evidence`,
  `.10x/reviews`, `.10x/specs`, `.10x/research`, or `.10x/decisions`;
- preserves the `sourceRef` naming convention as knowledge, not as a skill;
- opens or updates a bounded follow-up owner for archive malformed-currency
  coverage;
- records new evidence that explicitly supports parent closure or skill
  validation and names the limits of that evidence;
- updates or moves the Ledger import parent ticket so its status, progress,
  dependencies, blockers, and evidence references are coherent;
- creates no `.claude`, `.agents`, `.opencode`, or other harness mirror
  directory;
- avoids implementation file edits.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after three
repetitions for each arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/197-skill-record-backed-identity-scn012-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x/skills/`, `.10x/knowledge/`, `.10x/tickets/`,
  `.10x/evidence/`, and closure records as needed.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source implementation files;
- subject workspace `.claude/skills/`, `.agents/skills`, `.opencode/skills`,
  or other speculative harness mirror directories.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/197-skill-record-backed-identity-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for skill identity and closure completeness.

## Manual Inspection Requirement

Inspect every repetition's workspace manifest, final message, generated skill,
knowledge/follow-up records, evidence records, parent ticket, child ticket
reference paths, and changed file set. The automated scorer is not trusted for
slug identity.

## Promotion Rule

Promote only if candidate materially improves skill identity stability versus
current and passes follow-up mirror/source-path regressions. Do not promote from
this primary run alone unless current fails and candidate is perfectly stable;
even then, run `.agents`, `.opencode`, and `.claude` mirror regressions before
canonical promotion.

## Risks

- The prompt says "correct source skill" but not the slug. Passing still depends
  on record-backed identity inference, not prompt-copying.
- Candidate may not improve if the fixture lacks enough explicit durable slug
  authority.
- Passing this no-native fixture does not prove mirror identity stability.

## Execution Log

- 2026-06-25: Registered after EXP-996 showed canonical closure evidence
  improved but skill slug identity drift remained in current and
  duplicate-current reps.
- 2026-06-25: Ran live Codex subject harness under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/197-skill-record-backed-identity-scn012-live-micro/`.
  Canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged.
- 2026-06-25: Manual inspection found candidate created
  `.10x/skills/ledger-import-fixture-replay/SKILL.md` in all three repetitions.
  Current repeated a near-synonym slug failure in one repetition by creating
  `.10x/skills/ledger-fixture-replay/SKILL.md`.

## Result

Promising candidate, not promoted yet.

Manual inspection found:

- candidate-variant: 3/3 correct source skill identity,
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- current-10x: 2/3 correct source skill identity, with rep 0 creating
  `.10x/skills/ledger-fixture-replay/SKILL.md`;
- candidate-variant: 3/3 parent closure/validation evidence records;
- candidate-variant: 0/3 speculative `.claude`, `.agents`, or `.opencode`
  mirror directories;
- candidate-variant: 0/3 forbidden `.10x` record references inside generated
  skill bodies;
- canonical `SKILL.md` and `autoresearch/program.md` unchanged during the run.

Automated Trust Level 1 telemetry tied candidate and current because the
generic scorer does not score exact slug identity:

- candidate-variant: `S002=85`, `S006=70` average;
- current-10x: `S002=85`, `S006=70` average;
- no-10x-control: `S002=70`, `S006=50` average.

The candidate should proceed to regression controls:

- weak-request slug stability;
- no-native source-path shape;
- `.agents` writable mirror;
- `.opencode` mirror;
- `.claude` mirror.

Supporting records:

- `.10x/evidence/2026-06-25-skill-record-backed-identity-result.md`
- `.10x/reviews/2026-06-25-skill-record-backed-identity-result.md`
