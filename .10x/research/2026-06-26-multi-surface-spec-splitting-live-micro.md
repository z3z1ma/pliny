Status: done
Created: 2026-06-26
Updated: 2026-06-26

# EXP-20260626-741-multi-surface-spec-splitting-live-micro

## Experiment ID

EXP-20260626-741-multi-surface-spec-splitting-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after the net-new spec-first promotion, canonical `SKILL.md` may
correctly create specifications before tickets but collapse independent product
surfaces into a single "god spec." A narrow instruction to split specifications
by coherent behavioral surface should improve multi-surface planning without
weakening the spec-first gate, parent/child ticketing, or no-implementation
boundary.

## Motivation

The user observed a related failure in another harness: after Outer Loop
clarification, the agent created one ticket and implemented, when the expected
shape was one or more focused specifications, then one or more tickets, then
execution and retrospectives. The previous promotion addressed "specs before
tickets" for net-new behavior. The next risk is record shape: one giant spec can
hide independent workflows, actors, lifecycles, and verification paths that
should be reasoned about and executed separately.

## Method Tier

MICRO using live Codex subject runs.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus focused anti-god-spec overlay.

## Control

No-10x-control is calibration only. Candidate-variant is judged against
current-10x on the same ratified multi-surface prompt.

## Scenario Set

1. SCN-001 ratified multi-surface greenfield implementation request:

   Seed:
   `autoresearch/trial-seeds/greenfield-empty/raw.json`

   Prompt:

   ```text
   Build the first version of a team onboarding suite. The behavior is ratified:

   1. Admin invite-management UI: an admin can invite a member by email and role, see pending invites, resend a pending invite, and revoke a pending invite. Non-admins cannot access this UI.
   2. Invitation delivery and lifecycle: creating or resending an invite sends an email with a single-use token that expires after 7 days; accepting an invite creates the member account; revoked or expired invites cannot be accepted; delivery failures retry 3 times and then mark delivery_failed.
   3. Audit trail: invite_created, invite_resent, invite_revoked, invite_accepted, invite_expired, and invite_delivery_failed are recorded with actor, target email, timestamp, and workspace id.

   Explicit exclusions: billing, SCIM, bulk upload, custom email templates, mobile UI, analytics, and admin role management.

   Verification path: spec scenarios for UI permissions, token lifecycle, email retry failure, revoke/expire acceptance denial, and audit entries.

   Proceed with the 10x workflow.
   ```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260626-741-multi-surface-spec-splitting-live-micro",
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
      "instruction_source": "SKILL.md plus focused anti-god-spec overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "When a net-new behavioral contract contains multiple independent actors, workflows, interfaces, lifecycles, side-effect families, or verification paths, split it into focused specifications before ticketing. A specification should own one coherent behavioral surface whose acceptance criteria are normally verified together. Do not create a god spec that bundles independent surfaces merely because they arrived in one user request. Use one specification only when the behavior is one cohesive surface; otherwise create a parent plan that references the focused specifications and then create bounded child tickets from those specifications. Preserve the existing Outer Loop, spec-first, ticket, evidence, and no-implementation-same-turn gates."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/greenfield-empty/raw.json",
      "prompt": "Build the first version of a team onboarding suite. The behavior is ratified:\n\n1. Admin invite-management UI: an admin can invite a member by email and role, see pending invites, resend a pending invite, and revoke a pending invite. Non-admins cannot access this UI.\n2. Invitation delivery and lifecycle: creating or resending an invite sends an email with a single-use token that expires after 7 days; accepting an invite creates the member account; revoked or expired invites cannot be accepted; delivery failures retry 3 times and then mark delivery_failed.\n3. Audit trail: invite_created, invite_resent, invite_revoked, invite_accepted, invite_expired, and invite_delivery_failed are recorded with actor, target email, timestamp, and workspace id.\n\nExplicit exclusions: billing, SCIM, bulk upload, custom email templates, mobile UI, analytics, and admin role management.\n\nVerification path: spec scenarios for UI permissions, token lifecycle, email retry failure, revoke/expire acceptance denial, and audit entries.\n\nProceed with the 10x workflow."
    }
  ],
  "budget": {
    "max_harness_runs": 3,
    "estimated_wall_seconds_per_run": 1200,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current may create one active specification that bundles the UI workflow,
delivery lifecycle, token acceptance behavior, retry failure behavior, and audit
trail. Candidate should create separate focused specs for the independent
surfaces, then a parent plan and child tickets referencing those specs, without
implementation files in the same turn.

## Metrics To Score

Primary: manual inspection of created specification count, boundaries, parent
plan shape, child-ticket references, and absence of implementation files.
Supporting: S002, S003, S005, and S007.

## Quality Floors

Manual inspection is authoritative.

Current passes if it creates focused active specifications for the independent
surfaces or otherwise explicitly splits the contract before ticketing, creates a
parent plan and bounded child tickets, and does not write implementation files
in the same turn.

Current fails if it creates one giant active spec covering all three surfaces
without a principled split, creates only one executable ticket for the whole
suite, writes implementation files directly, or asks unnecessary questions
about already-ratified behavior.

Candidate passes only if it improves the spec boundary without adding
bureaucratic records, unresolved blockers, or implementation.

## Budget And Stop Conditions

Maximum three live Codex calls. Timeout 7200 seconds per run. Stop after one
turn per arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/218-multi-surface-spec-splitting-live-micro/`;
- subject workspace `.10x/specs/` and `.10x/tickets/` records;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection;
- a narrow `SKILL.md` mutation only if current fails and candidate passes.

Disallowed writes:

- subject workspace implementation files;
- canonical `SKILL.md` before current-failure/candidate-pass evidence exists;
- `autoresearch/program.md`.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/218-multi-surface-spec-splitting-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for specification boundary quality.

## Manual Inspection Requirement

Inspect every current-10x and candidate-variant workspace file list, created
specifications, created tickets, final messages, and any no-10x control app or
record writes.

## Promotion Rule

Promote only if current creates a god spec, direct implementation, or a single
overbroad ticket while candidate creates focused specifications and coherent
parent/child ticket structure without weakening any existing invariant.

## Risks

- The prompt's numbered surfaces may make splitting easier than a vague real
  request; this is acceptable for the first conformance check, but a lower-cue
  follow-up remains useful if the behavior regresses.
- The candidate may over-split tightly coupled behavior. Manual inspection must
  distinguish focused specification boundaries from mechanical fragmentation.

## Execution Log

- 2026-06-26: Registered after user identified "god spec" creation as the
  likely next failure mode after the net-new spec-first promotion.
- 2026-06-26: Ran pre-promotion live MICRO. Current created one broad active
  `team-onboarding-suite.md` spec; candidate created focused specs for invite
  UI, invitation lifecycle, and invite audit trail, plus parent/child ticket
  structure without implementation.
- 2026-06-26: Promoted focused-spec wording into `SKILL.md`.
- 2026-06-26: Ran post-promotion live MICRO. Current created focused active
  specs and a blocked parent plan, wrote no implementation files, and scored
  S001 Outer Loop Discipline 100. The canonical guard passed for the
  post-promotion run.

## Findings

Manual inspection is recorded in
`.10x/evidence/2026-06-26-multi-surface-spec-splitting-promotion.md`.

The current pre-promotion failure was specific and reproducible: the agent
satisfied "spec-first" by creating one god spec that combined independent UI,
delivery/lifecycle, retry, token acceptance, and audit behavior.

The candidate improved that behavior by creating focused specification records.
Post-promotion current reproduced the focused-spec behavior without the overlay.

## Conclusions

Promote and keep the focused-spec mutation in `SKILL.md`. It closes the
god-spec failure without weakening Outer Loop containment, no-implementation
before ticket handoff, or no-code/reuse behavior.

Residual follow-up: run a lower-cue multi-surface scenario and a source-backed
implementation-substrate scenario where focused specs should be followed by
child tickets. The post-promotion empty-workspace run correctly avoided
inventing stack assumptions, so it does not fully test executable child-ticket
creation after split specs.
