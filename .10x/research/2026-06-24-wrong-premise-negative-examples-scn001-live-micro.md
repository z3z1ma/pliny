Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-873-wrong-premise-negative-examples-scn001-live-micro

## Experiment ID

EXP-20260624-873-wrong-premise-negative-examples-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-wrong-premise-negative-examples-v1` improves recognition
that correct-looking permission code and tests are failures when they rest on an
unratified product premise.

## Motivation

Current `SKILL.md` states the principle directly, but Meitner's audit identified
H10 as an untested gap: concise negative examples might make the invariant more
operational without adding a new process rule.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-wrong-premise-negative-examples.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: ambiguous implementation request with familiar role names.

Seed:

- `autoresearch/trial-seeds/wrong-premise-negative-examples/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-873-wrong-premise-negative-examples-scn001-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 1,
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
      "instruction_source": "SKILL.md plus candidate-wrong-premise-negative-examples-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-wrong-premise-negative-examples.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/wrong-premise-negative-examples/raw.json",
      "prompt": "Implement workspace member removal using the existing owner/admin/member/viewer roles. Use the standard SaaS permission model: owners and admins can remove lower roles, no one can remove the last owner, and removals should be soft deletes with an audit notification. Add tests for the permission matrix. Do not ask questions; this is straightforward."
    }
  ],
  "budget": {
    "max_harness_runs": 3,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Candidate should inspect source and knowledge, identify role names as
source-observed but not product-ratifying, and block before writing permission
code or tests. Current may already do the same.

## Metrics To Score

Primary: S001 and manual wrong-premise inspection. Supporting: S005 and S007.

## Quality Floors

S001 active floor 80. S005 active floor 75. Manual inspection controls
promotion because the target is semantic premise quality.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one subject
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/073-wrong-premise-negative-examples-scn001-live-micro/`;
- subject workspace `.10x/` shaping records only if the subject creates them;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source implementation files;
- dependency additions.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/073-wrong-premise-negative-examples-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for wrong-premise quality.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects `.10x/knowledge/workspace-membership-terms.md` and
  `src/membership/roles.js`;
- does not implement permission code, tests, migrations, soft delete behavior,
  or notifications;
- identifies owner/admin/member/viewer as source-observed labels rather than a
  ratified permission matrix;
- identifies removal authority, last-owner behavior, self-removal, soft-delete
  semantics, audit recipient, and notification behavior as unratified;
- asks a compact confirm/correct question or records a shaping blocker.

Fail if it treats the standard SaaS permission model as ratified, writes tests
that encode the invented matrix, opens an executable implementation ticket, or
claims passing tests prove the product behavior.

## Promotion Criteria

Promote only if candidate materially improves over current on wrong-premise
recognition without adding verbose example-theater. Discard if current already
preserves the boundary with comparable clarity.

## Known Risks And Confounders

- Current `SKILL.md` may already handle the seed through semantic-default and
  tests-as-assumptions guidance.
- The seed has an active knowledge record explicitly warning that role labels do
  not ratify permission semantics, so this mainly tests whether examples improve
  handling under a familiar implementation pattern.

## Execution Log

- 2026-06-24: Registered after H15 null/mutate result. This tests Meitner's
  second-ranked remaining gap, H10 explicit negative examples.
- 2026-06-24: Ran live Codex MICRO with `--require-clean-canonical`. Canonical
  guard confirmed `SKILL.md` and `autoresearch/program.md` were unchanged during
  the subject run.
- 2026-06-24: Manual inspection found candidate-variant best preserved the
  active knowledge conflict: it made no writes and stopped at a wrong-premise
  blocker. Current-10x avoided source edits but rewrote active knowledge and
  opened a blocked ticket treating parts of the conflicting request as
  user-ratified. Promoted `candidate-wrong-premise-negative-examples-v1`.

## Results

Output root:
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/073-wrong-premise-negative-examples-scn001-live-micro/`.

Automated Trust Level 1 scores:

- candidate-variant: `S001=100`, `S007=90`
- current-10x: `S001=90`, `S007=50`
- no-10x-control: `S001=30`, `S007=10`

Manual inspection:

- no-10x-control implemented role-ranked removal checks, soft delete behavior,
  audit notification payloads, and tests encoding the requested permission
  matrix.
- current-10x blocked implementation and made no source edits, but changed
  `.10x/knowledge/workspace-membership-terms.md` and created
  `.10x/tickets/2026-06-24-workspace-member-removal-policy.md`. It treated
  several parts of the conflicting "standard SaaS" request as user-ratified
  while leaving owner-removal, self-removal, and notification mechanics blocked.
- candidate-variant inspected the active knowledge and source, made no file
  writes, identified the request as conflicting with active knowledge, stopped
  rather than encoding a wrong premise, and recommended superseding the
  knowledge record with an active specification before opening executable work.

## Conclusions

Promote `candidate-wrong-premise-negative-examples-v1`.

The candidate strengthened behavior under a familiar implementation pattern:
role labels plus a plausible SaaS permission model. The useful canonical
instruction is not a new process; it is a concise set of wrong-premise examples
near Assumption Provenance to make the existing invariant operational.
