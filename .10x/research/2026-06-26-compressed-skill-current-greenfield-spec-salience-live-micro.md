Status: active
Created: 2026-06-26
Updated: 2026-06-26

# EXP-20260626-748-compressed-skill-current-greenfield-spec-salience-live-micro

## Experiment ID

EXP-20260626-748-compressed-skill-current-greenfield-spec-salience-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: the compressed current `SKILL.md` preserves the recent salience
gains around always-on 10x activation, net-new specification-first behavior,
bounded ticket creation, and split specifications for independent behavioral
surfaces.

## Motivation

The live `SKILL.md` has gone through a large compression pass. Before resuming
new hill-climbing, rerun high-signal scenarios against current only to confirm
compression did not erase learned behavior. This batch focuses on the most
recent user-observed failures: small greenfield app activation, clarified
greenfield behavior collapsing directly into one ticket or implementation, and
multi-surface behavior requiring separate focused specifications before
implementation tickets.

## Method Tier

MICRO using live Codex subject runs.

## Variants

- current-10x: compressed canonical `SKILL.md`.

## Control

Evaluation-only current run. Historical no-10x-control and candidate results
already exist in the referenced source experiments.

## Scenario Set

1. SCN-001 small greenfield app activation boundary.
2. SCN-001 clarified single-surface greenfield continuation.
3. SCN-001 clarified multi-surface greenfield continuation.
4. SCN-006 source-backed multi-surface onboarding suite.

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260626-748-compressed-skill-current-greenfield-spec-salience-live-micro",
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
      "instruction_source": "compressed SKILL.md",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/small-greenfield-app-activation/raw.json",
      "prompt": "Create a small personal bookmark tracker app in this folder. Keep it simple."
    },
    {
      "id": "SCN-001",
      "prior_raw_path": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/raw/sha256-55b8bac8e47596958c68dc5ceedc082799bbc590c7861460d0fdb718d141dfcc.json",
      "prompt": "Confirmed. Use a dependency-free static browser app with index.html, styles.css, and app.js. Behavior: add a todo with trimmed non-empty text; show todos in creation order; mark a todo complete or active; edit todo text; delete one todo; filter all, active, and completed; show an empty-state message when the selected filter has no todos; clear completed only after an explicit confirmation; persist todos and the selected filter in localStorage across refresh. Exclude accounts, backend, sync, dates, priorities, drag/drop, notifications, routing, build tooling, external dependencies, and automated tests. Verification path: manual browser check for add, edit, complete/uncomplete, filter changes, delete, clear-completed cancel and confirm, empty states, and refresh persistence. Proceed with the 10x workflow."
    },
    {
      "id": "SCN-001",
      "prior_raw_path": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/raw/sha256-55b8bac8e47596958c68dc5ceedc082799bbc590c7861460d0fdb718d141dfcc.json",
      "prompt": "Confirmed. Make it a dependency-free static browser app with index.html, styles.css, and app.js. It is for one person managing tasks across projects. It should let me add, edit, and delete tasks; mark tasks active or completed; assign each task to one project; filter by project and completion state; archive and unarchive projects while preserving their tasks; hide archived projects from normal project pickers; export all data to a JSON file; import a JSON file only after explicit confirmation that it will replace current local data; and show an activity log for task created, task edited, task completed, task deleted, project archived, project unarchived, import, and export. Persist tasks, projects, filters, and the activity log in localStorage across refresh. Exclude accounts, backend, sync, dates, priorities, drag/drop, notifications, routing, build tooling, external dependencies, and automated tests. Verification path: manual browser check for task CRUD, filtering, project archive visibility, import replace confirmation, export round trip, activity log entries, and refresh persistence. Proceed with the 10x workflow."
    },
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/source-backed-onboarding-substrate/raw.json",
      "prompt": "Build the first version of the team onboarding suite on the existing local Node HTTP/JSON substrate. The active knowledge record and source files already define the target runtime, server shape, auth/role model, persistence, mail adapter, retry runner, audit storage, system actor convention, and test runner. Use those existing substrate choices exactly.\n\nThe behavior is ratified:\n\n1. Admin invite-management UI: an admin can invite a member by email and role, see pending invites, resend a pending invite, and revoke a pending invite. Non-admins cannot access this UI.\n2. Invitation delivery and lifecycle: creating or resending an invite sends an email with a single-use token that expires after 7 days; accepting an invite creates the member account; revoked or expired invites cannot be accepted; delivery failures retry 3 times and then mark delivery_failed.\n3. Audit trail: invite_created, invite_resent, invite_revoked, invite_accepted, invite_expired, and invite_delivery_failed are recorded with actor, target email, timestamp, and workspace id. Automated invite_expired and invite_delivery_failed events use actor system.\n\nExplicit exclusions: billing, SCIM, bulk upload, custom email templates, mobile UI, analytics, admin role management, new framework dependencies, and non-JSON persistence.\n\nVerification path: node --test scenarios for UI permissions, token lifecycle, email retry failure, revoke/expire acceptance denial, and audit entries.\n\nProceed with the 10x workflow."
    }
  ],
  "budget": {
    "max_harness_runs": 4,
    "estimated_wall_seconds_per_run": 1200,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current compressed `SKILL.md` should preserve always-on 10x behavior, create
specifications before executable tickets for net-new or important behavior, and
split independent behavior surfaces instead of creating one god spec or one god
ticket. It should not implement in the same turn as shaping non-trivial
greenfield work.

## Metrics To Score

Manual inspection is authoritative. Supporting scores: S001, S002, S003, S005,
S006, and S007.

## Budget And Stop Conditions

Maximum 4 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per scenario.

## Results

Pending.
