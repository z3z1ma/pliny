Status: done
Created: 2026-06-26
Updated: 2026-06-26

# EXP-20260626-752-current-focused-spec-controls-batch-live-micro

## Experiment ID

EXP-20260626-752-current-focused-spec-controls-batch-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after the focused-spec repair, current `SKILL.md` splits natural
multi-surface behavior into focused specs while preserving controls for
existing-spec work, no-code answers, and exact mechanical edits.

## Motivation

The compression salience run found and repaired one source-backed god-spec
regression. This batch protects that patch from both sides: it tests lower-cue
multi-surface decomposition and checks that the new language does not over-split
simple or already-governed work.

## Method Tier

MICRO using live Codex subject runs.

## Variants

- current-10x: canonical patched `SKILL.md`.

## Control

Evaluation-only current run. Historical control and candidate results remain in
prior experiments.

## Scenario Set

1. SCN-001 lower-cue multi-surface static to-do continuation.
2. SCN-006 lower-cue source-backed onboarding decomposition.
3. SCN-006 existing active spec implementation workflow control.
4. SCN-010 no-code/reuse control.
5. SCN-010 exact formatting edit control.

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260626-752-current-focused-spec-controls-batch-live-micro",
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
      "instruction_source": "patched SKILL.md",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/raw/sha256-55b8bac8e47596958c68dc5ceedc082799bbc590c7861460d0fdb718d141dfcc.json",
      "prompt": "Confirmed. Make it a dependency-free static browser app with index.html, styles.css, and app.js. It is for one person managing tasks across projects. It should let me add, edit, and delete tasks; mark tasks active or completed; assign each task to one project; filter by project and completion state; archive and unarchive projects while preserving their tasks; hide archived projects from normal project pickers; export all data to a JSON file; import a JSON file only after explicit confirmation that it will replace current local data; and show an activity log for task created, task edited, task completed, task deleted, project archived, project unarchived, import, and export. Persist tasks, projects, filters, and the activity log in localStorage across refresh. Exclude accounts, backend, sync, dates, priorities, drag/drop, notifications, routing, build tooling, external dependencies, and automated tests. Verification path: manual browser check for task CRUD, filtering, project archive visibility, import replace confirmation, export round trip, activity log entries, and refresh persistence. Proceed with the 10x workflow."
    },
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/source-backed-onboarding-substrate/raw.json",
      "prompt": "Build the first version of team onboarding on the existing local Node HTTP/JSON app. The current records and source already establish the runtime, server shape, auth roles, JSON persistence, local mail outbox, retry helper, audit helper, system actor convention, and node test runner. Admins need to manage invitations by email and role, including pending invite list, resend, and revoke; non-admins must be denied. Invitations are delivered as single-use email tokens, expire after 7 days, create the member account when accepted, cannot be accepted after revoke/expiry/use, and failed delivery retries 3 times before marking delivery_failed. Audit invite create, resend, revoke, accept, expire, and delivery failure with actor, target email, timestamp, and workspace id; automated expire/failure use system actor. Exclude billing, SCIM, bulk upload, custom email templates, mobile UI, analytics, admin role management, new framework dependencies, and non-JSON persistence. Verification path: node --test coverage for invite permissions, token lifecycle, delivery retry failure, revoke/expire rejection, and audit entries. Proceed with the 10x workflow."
    },
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/existing-active-spec-static-todo/raw.json",
      "prompt": "The active spec .10x/specs/static-browser-todo-app.md is approved. Start the 10x implementation workflow for it."
    },
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/correct-answer-no-code/raw.json",
      "prompt": "Add browser-side CSV generation to the reports dashboard so it no longer depends on the server export endpoint."
    },
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/exact-formatting-edit/raw.json",
      "prompt": "In styles.css, change only the .button padding from 4px 8px to 6px 10px. Do only that."
    }
  ],
  "budget": {
    "max_harness_runs": 5,
    "estimated_wall_seconds_per_run": 1200,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current should create focused spec sets for the two lower-cue multi-surface
requests, while avoiding new specs for exact edits, no-code answers, and work
already fully governed by an active spec.

## Metrics To Score

Manual inspection is authoritative. Supporting scores: S001, S002, S003, S005,
and S007.

## Budget And Stop Conditions

Maximum 5 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per scenario.

## Results

Artifact root:
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/232-current-focused-spec-controls-batch-live-micro`.

Manual outcome: pass, 5/5 scenarios.

- Lower-cue static to-do continuation created three focused specs
  (`todo-task-project-workflow.md`, `todo-persistence-import-export.md`,
  `todo-activity-log.md`), a parent plan, and three executable child tickets.
  It stopped before implementation, which matches the non-trivial net-new
  workflow gate.
- Source-backed onboarding created three focused specs
  (`team-invite-management.md`, `team-invite-token-lifecycle.md`,
  `team-invite-delivery-and-audit.md`) plus a parent plan and bounded child
  tickets. The prior god-spec regression did not reproduce.
- Existing active-spec work opened exactly one executable implementation
  ticket against the approved spec and did not over-split.
- No-code/reuse control blocked browser-side CSV generation because an active
  decision owned server export, and asked for explicit supersession instead of
  implementing.
- Exact formatting edit changed only `styles.css` `.button` padding.

Trust Level 1 scorer outcome: no floor failures. Manual inspection agrees with
the scorer for this batch.

Conclusion: the compressed `SKILL.md` preserved the focused-spec repair without
causing obvious over-splitting or process overhead on controls. No `SKILL.md`
mutation is warranted from this batch.
