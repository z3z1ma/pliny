Status: done
Created: 2026-06-26
Updated: 2026-06-26

# EXP-20260626-742-source-backed-split-spec-child-ticket-live-micro

## Experiment ID

EXP-20260626-742-source-backed-split-spec-child-ticket-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after the focused-spec promotion, current `SKILL.md` should create
focused specifications, a parent plan, and bounded child tickets when a
multi-surface behavior request is ratified and the source/record substrate
settles stack, auth, persistence, mail, retry, audit, system actor, and test
runner choices.

## Motivation

The post-promotion multi-surface run correctly split specifications but stopped
at a blocked parent plan because the seed workspace was empty. That was
conservative, but it left a child-ticket positive-control gap. This experiment
removes the implementation-substrate blocker so current can be judged on
whether it creates child tickets after focused specs instead of stopping early.

## Method Tier

MICRO using live Codex subject runs.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus source-backed child-ticket
  overlay.

## Control

No-10x-control is calibration only. Candidate-variant tests the narrow behavior
that may be promoted only if current fails.

## Scenario Set

1. SCN-006 source-backed multi-surface spec/ticket decomposition:

   Seed:
   `autoresearch/trial-seeds/source-backed-onboarding-substrate/raw.json`

   Prompt:

   ```text
   Build the first version of the team onboarding suite on the existing local Node HTTP/JSON substrate. The active knowledge record and source files already define the target runtime, server shape, auth/role model, persistence, mail adapter, retry runner, audit storage, system actor convention, and test runner. Use those existing substrate choices exactly.

   The behavior is ratified:

   1. Admin invite-management UI: an admin can invite a member by email and role, see pending invites, resend a pending invite, and revoke a pending invite. Non-admins cannot access this UI.
   2. Invitation delivery and lifecycle: creating or resending an invite sends an email with a single-use token that expires after 7 days; accepting an invite creates the member account; revoked or expired invites cannot be accepted; delivery failures retry 3 times and then mark delivery_failed.
   3. Audit trail: invite_created, invite_resent, invite_revoked, invite_accepted, invite_expired, and invite_delivery_failed are recorded with actor, target email, timestamp, and workspace id. Automated invite_expired and invite_delivery_failed events use actor system.

   Explicit exclusions: billing, SCIM, bulk upload, custom email templates, mobile UI, analytics, admin role management, new framework dependencies, and non-JSON persistence.

   Verification path: node --test scenarios for UI permissions, token lifecycle, email retry failure, revoke/expire acceptance denial, and audit entries.

   Proceed with the 10x workflow.
   ```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260626-742-source-backed-split-spec-child-ticket-live-micro",
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
      "instruction_source": "SKILL.md plus source-backed child-ticket overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "After focused specifications are created for a ratified multi-surface request, if inspected active records and source settle the implementation substrate and no execution-critical blockers remain, create the parent plan and bounded child tickets in the same Outer Loop turn. Do not stop at only a blocked parent plan merely because implementation has not begun. This does not authorize implementation in the same turn as creating the governing specs and first tickets."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/source-backed-onboarding-substrate/raw.json",
      "prompt": "Build the first version of the team onboarding suite on the existing local Node HTTP/JSON substrate. The active knowledge record and source files already define the target runtime, server shape, auth/role model, persistence, mail adapter, retry runner, audit storage, system actor convention, and test runner. Use those existing substrate choices exactly.\n\nThe behavior is ratified:\n\n1. Admin invite-management UI: an admin can invite a member by email and role, see pending invites, resend a pending invite, and revoke a pending invite. Non-admins cannot access this UI.\n2. Invitation delivery and lifecycle: creating or resending an invite sends an email with a single-use token that expires after 7 days; accepting an invite creates the member account; revoked or expired invites cannot be accepted; delivery failures retry 3 times and then mark delivery_failed.\n3. Audit trail: invite_created, invite_resent, invite_revoked, invite_accepted, invite_expired, and invite_delivery_failed are recorded with actor, target email, timestamp, and workspace id. Automated invite_expired and invite_delivery_failed events use actor system.\n\nExplicit exclusions: billing, SCIM, bulk upload, custom email templates, mobile UI, analytics, admin role management, new framework dependencies, and non-JSON persistence.\n\nVerification path: node --test scenarios for UI permissions, token lifecycle, email retry failure, revoke/expire acceptance denial, and audit entries.\n\nProceed with the 10x workflow."
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

Current should inspect the active knowledge record and source, create focused
active specs for UI, invitation lifecycle/delivery, and audit behavior, create a
parent plan, create bounded child tickets, and stop without editing source,
tests, package metadata, or data files.

Candidate should behave the same unless current stops at only a blocked parent
or asks for substrate choices that records/source already settle.

## Metrics To Score

Primary: manual inspection of source/record inspection, created specs, parent
plan, child ticket count and scope, blockers, and absence of implementation
files. Supporting: S003 and S007.

## Quality Floors

Manual inspection is authoritative.

Current passes if it:

- inspects or cites the active substrate knowledge/source;
- creates focused specs for independent surfaces;
- creates a parent plan and bounded child tickets referencing those specs;
- records no unresolved substrate blockers;
- writes no implementation files in the same turn.

Current fails if it creates a god spec, stops at only a blocked parent despite
settled substrate, asks for already-settled stack/substrate choices, creates one
overbroad executable ticket, or implements source/tests directly.

## Budget And Stop Conditions

Maximum three live Codex calls. Timeout 7200 seconds per run. Stop after one
turn per arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/220-source-backed-split-spec-child-ticket-live-micro/`;
- subject workspace `.10x/specs/` and `.10x/tickets/` records;
- this research record execution log updates;
- evidence/review records after inspection;
- a narrow `SKILL.md` mutation only if current fails and candidate passes.

Disallowed writes:

- subject workspace implementation files, tests, dependency manifests, or data
  files;
- canonical `SKILL.md` before current-failure/candidate-pass evidence exists;
- `autoresearch/program.md`.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/220-source-backed-split-spec-child-ticket-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for child-ticket decomposition and write-boundary
quality.

## Manual Inspection Requirement

Inspect current-10x and candidate-variant workspace file lists, created specs,
created tickets, final messages, and no-10x control writes.

## Promotion Rule

Promote only if current fails the child-ticket positive control and candidate
passes without weakening focused-spec, no-implementation, assumption-provenance,
or no-code/reuse invariants.

## Risks

- The prompt is explicit about substrate authority; if current passes, a
  lower-cue source-backed variant remains useful later.
- The candidate may create child tickets with hidden unresolved assumptions.
  Manual inspection must check blockers and ticket acceptance criteria, not only
  file counts.

## Execution Log

- 2026-06-26: Registered from
  `.10x/tickets/done/2026-06-26-source-backed-split-spec-child-ticket-control.md`
  after the anti-god-spec promotion left child-ticket creation under settled
  substrate untested.
- 2026-06-26: Ran the live Codex experiment with no-10x-control,
  current-10x, and candidate-variant. Output is stored under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/220-source-backed-split-spec-child-ticket-live-micro/`.

## Results

Manual inspection is the authoritative result.

No-10x-control did not follow 10x planning discipline. It created a broad
`.10x/specs/team-onboarding-suite.md`, implemented source changes in
`src/onboarding/invitations.js`, `src/server.js`,
`src/jobs/retryInvitationDelivery.js`, and `test/onboarding-substrate.test.js`,
closed a ticket, recorded evidence, and reported `npm test` passing in the
same turn.

Current `SKILL.md` improved over control by staying in the planning boundary
and avoiding source/test edits, but it failed the target decomposition. It
created exactly one suite-wide active specification,
`.10x/specs/team-onboarding-suite.md`, and one broad executable ticket,
`.10x/tickets/2026-06-26-build-team-onboarding-suite.md`, despite the prompt
and active substrate record separating admin UI, invitation lifecycle/delivery,
and audit behavior.

Candidate-variant passed. It created three focused active specifications:

- `.10x/specs/admin-invite-management-json-ui.md`
- `.10x/specs/invitation-delivery-lifecycle.md`
- `.10x/specs/onboarding-invite-audit-trail.md`

It then created a non-executable parent plan,
`.10x/tickets/2026-06-26-team-onboarding-suite.md`, and three bounded child
tickets referencing the focused specs:

- `.10x/tickets/2026-06-26-admin-invite-management-json-ui.md`
- `.10x/tickets/2026-06-26-invitation-delivery-lifecycle.md`
- `.10x/tickets/2026-06-26-onboarding-invite-audit-trail.md`

The candidate inspected the active substrate knowledge/source, recorded no
substrate blockers, and did not modify implementation files, tests, package
metadata, or data files.

## Conclusions

Current `SKILL.md` still allowed a model to collapse a ratified multi-surface
net-new feature into a suite-level spec and broad executable ticket. The
candidate overlay corrected that behavior without weakening the no-
implementation-in-the-same-turn boundary.

Promote a narrow source-backed child-ticket rule: when the spec-first gate
applies and user-ratified behavior plus inspected records/source settle the
implementation substrate, create the focused specification set, parent plan,
and bounded child tickets in the same Outer Loop turn. Do not stop at a broad
spec, a single ticket, or a parent-only plan merely because implementation has
not begun.

## Limits

This was one live Codex repetition per arm. The prompt explicitly said the
substrate was settled, so a lower-cue source-backed variant remains useful
later. The result does not prove non-Codex harness behavior.
