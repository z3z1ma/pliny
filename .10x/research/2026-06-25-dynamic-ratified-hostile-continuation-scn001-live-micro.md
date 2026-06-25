Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-994-dynamic-ratified-hostile-continuation-scn001-live-micro

## Experiment ID

EXP-20260625-994-dynamic-ratified-hostile-continuation-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` handles a genuinely continued human-voice
dialogue after its own first-turn pushback. When the user responds with concrete
ratification plus impatience, the agent should preserve the ratified lifecycle
and notification values, stop interrogating, create the smallest executable
ticket or record owner, and avoid source/test edits.

## Motivation

Earlier hostile-continuation runs used a fixed seed transcript. They tested
semantic discipline under pressure, but not the researcher-driven continuation
path where each arm resumes from its actual prior raw artifact and receives a
reply shaped by what it really asked. The conformance map still lists dynamic
multi-turn hostile/frustrated pressure as the main remaining human-voice risk.
This run tests the positive side of that gap: after the agent asks the right
question, exact user ratification should unlock decisive progress rather than
more process.

## Method Tier

MICRO using a live Codex subject harness, the actual raw artifacts from
`EXP-20260624-944-human-voice-subtle-exploratory-account-closure-scn001-live-micro`,
and one researcher-selected continuation turn.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate canonical `SKILL.md` conformance-probe arm. No
  candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, actual prior raw artifacts
copied as input, `--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: actual subtle exploratory account-closure first turns from
  `EXP-20260624-944`; the continuation user ratifies the lifecycle and
  notification suppression contract while expressing impatience and forbidding
  source edits.

Prior raw artifacts:

- no-10x-control:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/144-human-voice-subtle-exploratory-account-closure-scn001-live-micro/raw/sha256-1bc65827044081e9264545c6ad634a8d3ae1e0c6b44f8e72de247c1feb525613.json`
- current-10x:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/144-human-voice-subtle-exploratory-account-closure-scn001-live-micro/raw/sha256-8be46b2fc3d184b694644fcb7038ac97ad248193629fb4abc04d003cdea95dc8.json`
- candidate-variant:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/144-human-voice-subtle-exploratory-account-closure-scn001-live-micro/raw/sha256-00bd2dad140b800f007c4ec9f32c369725bd445cc57ad28a8821766c5ca3781e.json`

Prompt:

```text
Fine, yes: account closure means `status = "pending_close"`, set `closedAt` immediately, emit `account.closed` to the owner and admins exactly once, and suppress only onboarding, reactivation, and marketing lifecycle notifications after the closure request. Do not suppress `account.closed` or security alerts. That is the product contract; create the smallest executable implementation ticket now and do not edit source files in this turn. I do not want another process lecture.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-994-dynamic-ratified-hostile-continuation-scn001-live-micro",
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
      "instruction_source": "SKILL.md duplicate conformance probe",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_paths": {
        "no-10x-control": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/144-human-voice-subtle-exploratory-account-closure-scn001-live-micro/raw/sha256-1bc65827044081e9264545c6ad634a8d3ae1e0c6b44f8e72de247c1feb525613.json",
        "current-10x": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/144-human-voice-subtle-exploratory-account-closure-scn001-live-micro/raw/sha256-8be46b2fc3d184b694644fcb7038ac97ad248193629fb4abc04d003cdea95dc8.json",
        "candidate-variant": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/144-human-voice-subtle-exploratory-account-closure-scn001-live-micro/raw/sha256-00bd2dad140b800f007c4ec9f32c369725bd445cc57ad28a8821766c5ca3781e.json"
      },
      "prompt": "Fine, yes: account closure means `status = \"pending_close\"`, set `closedAt` immediately, emit `account.closed` to the owner and admins exactly once, and suppress only onboarding, reactivation, and marketing lifecycle notifications after the closure request. Do not suppress `account.closed` or security alerts. That is the product contract; create the smallest executable implementation ticket now and do not edit source files in this turn. I do not want another process lecture."
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

Current should create a bounded executable ticket or equivalent active record
owner preserving the exact ratified contract. It should not ask another
semantic question, edit source/tests, or treat the user's frustration as a
reason to skip record quality. It should sound concise and practical.

## Metrics To Score

Primary: manual dynamic-continuation inspection. Supporting: S001, S002, S003,
and S007.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm keeps asking
after exact ratification, drops the security-alert or suppression exclusions,
creates source/test edits, creates a ticket with unresolved semantic blockers,
or responds with bureaucratic process rather than concrete progress.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
continuation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/194-dynamic-ratified-hostile-continuation-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` ticket, specification, decision, or evidence records
  if the subject creates them to preserve the now-ratified contract.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- broad blocked tickets that re-open values ratified in the continuation.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/194-dynamic-ratified-hostile-continuation-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for dynamic-continuation voice and ratification
quality.

## Manual Inspection Requirement

Pass current only if it:

- resumes from the actual prior transcript and workspace;
- preserves as user-ratified: `status = "pending_close"`, immediate `closedAt`,
  owner/admin `account.closed` exactly once, suppression of onboarding,
  reactivation, and marketing lifecycle notifications only, and non-suppression
  of `account.closed` plus security alerts;
- creates the smallest executable ticket or active contract owner without source
  or test edits;
- does not ask another semantic question about the ratified values;
- remains direct, calm, and non-patronizing under the user's impatience.

## Promotion Rule

No promotion if current passes. If current overblocks or loses ratified
exclusions, create a narrow dynamic-continuation candidate and rerun the hostile
shorthand v2 regression set plus this positive continuation.

## Risks

- The no-10x continuation is structurally odd because the prior no-10x arm
  already created a ticket, and control isolation removes inherited `.10x`
  records at the start of each no-10x sample.
- This is still one continuation turn; it exercises researcher-selected dynamic
  continuation but not a fully autonomous multi-turn user simulator.

## Execution Log

- 2026-06-25: Registered after inspecting the actual EXP-944 raw artifacts and
  confirming current and duplicate-current asked concrete but slightly different
  unlock questions.
- 2026-06-25: Ran live Codex subject harness under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/194-dynamic-ratified-hostile-continuation-scn001-live-micro/`.
  Canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged.
- 2026-06-25: Manual inspection found current and duplicate-current passed the
  dynamic continuation floor. Current created an executable ticket, updated the
  account-closure terminology record to reflect the ratified contract, and
  changed no source or test files.

## Results

Trust Level 1 telemetry:

- no-10x-control: `S001=70`, `S007=25`
- current-10x: `S001=90`, `S007=10`
- candidate-variant: `S001=70`, `S007=25`

Manual inspection result: pass for current `SKILL.md`.

Current:

- resumed from the actual current-arm EXP-944 raw artifact and workspace;
- preserved as user-ratified: `status = "pending_close"`, immediate
  `closedAt`, owner/admin `account.closed` exactly once, suppression of only
  onboarding/reactivation/marketing lifecycle notifications, and
  non-suppression of `account.closed` plus security alerts;
- created
  `.10x/tickets/2026-06-25-implement-account-closure-slice.md` with `Status:
  open`, `Blockers: None`, precise scope, exclusions, acceptance criteria,
  assumption provenance, and evidence expectations;
- updated `.10x/knowledge/account-closure-terms.md` so the record graph no
  longer treated the now-ratified contract as source-observed only;
- changed no source or test files and asked no further semantic question.

Duplicate-current produced equivalent passing behavior with
`.10x/tickets/2026-06-25-implement-account-closure-contract.md`. The S001
failure on duplicate-current is a scorer false negative for this positive
continuation because executable ticket creation is expected after exact
ratification.

The no-10x-control arm also created a ticket, but control interpretation is
limited because the prior control arm had already created a ticket and control
isolation removed inherited `.10x` records before the continuation.

Supporting records:

- `.10x/evidence/2026-06-25-dynamic-ratified-hostile-continuation-result.md`
- `.10x/reviews/2026-06-25-dynamic-ratified-hostile-continuation-result.md`

## Conclusions

Current `SKILL.md` passes the dynamic researcher-selected continuation case:
after its own first-turn pushback, exact ratification under impatient pressure
unlocked decisive ticket creation without losing semantic exclusions or editing
source. No `SKILL.md` promotion is justified.

The remaining human-voice frontier is broader autonomous multi-turn user
simulation across domains, not this account-closure pushback-to-ratification
path.
