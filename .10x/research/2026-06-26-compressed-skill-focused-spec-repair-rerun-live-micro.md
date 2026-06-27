Status: done
Created: 2026-06-26
Updated: 2026-06-26

# EXP-20260626-751-compressed-skill-focused-spec-repair-rerun-live-micro

## Experiment ID

EXP-20260626-751-compressed-skill-focused-spec-repair-rerun-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: the focused-spec boundary patch restores the source-backed
multi-surface decomposition behavior lost during `SKILL.md` compression while
remaining under the 40,000-character body budget.

## Motivation

`EXP-20260626-748-compressed-skill-current-greenfield-spec-salience-live-micro`
showed a real compression regression: the source-backed onboarding scenario
created one suite-wide active spec instead of focused specs for admin invite
management, invitation lifecycle/delivery, and audit behavior. The patch adds
only the operational rule that child-ticket boundaries imply focused-spec
boundaries, especially for numbered behavior groups.

## Method Tier

MICRO using a live Codex subject run.

## Variants

- current-10x: patched compressed canonical `SKILL.md`.

## Control

Evaluation-only current rerun. Historical failing current output is in
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/228-compressed-skill-current-greenfield-spec-salience-live-micro/`.

## Scenario Set

1. SCN-006 source-backed multi-surface onboarding suite.

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260626-751-compressed-skill-focused-spec-repair-rerun-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "evaluation_only": true,
  "repetitions": 1,
  "arms": [
    {
      "id": "current-10x",
      "instruction_source": "patched compressed SKILL.md",
      "instruction_path": "SKILL.md"
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
    "max_harness_runs": 1,
    "estimated_wall_seconds_per_run": 1200,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current should inspect the source-backed substrate, create focused active specs
for admin invite management, invitation lifecycle/delivery, and audit behavior,
then create a parent plan and bounded child tickets referencing those focused
specs. It must not write implementation files or tests.

## Metrics To Score

Manual inspection is authoritative. Supporting score: S003.

## Budget And Stop Conditions

Maximum 1 live Codex call. Timeout 7200 seconds. Stop after one turn.

## Results

Ran 2026-06-26. Output:
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/231-compressed-skill-focused-spec-repair-rerun-live-micro/`.

Before the rerun, the patched `SKILL.md` body measured 39,032 characters,
leaving 968 characters of headroom under the 40,000-character budget.

Trust Level 1 score: `S003=100`.

Manual inspection is authoritative. Current passed:

- Created focused active specs:
  - `.10x/specs/admin-invite-management-ui.md`
  - `.10x/specs/invitation-delivery-lifecycle.md`
  - `.10x/specs/invite-audit-trail.md`
- Created parent plan
  `.10x/tickets/2026-06-26-team-onboarding-suite-plan.md`.
- Created bounded child tickets for UI, lifecycle, audit, and verification.
- Wrote no implementation files and ran no tests.

Conclusion: the narrow focused-spec boundary patch repaired the compression
regression while staying under the size budget.
