Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-generic-named-app-activation-live-micro.md

# Generic Named App Activation Result

## What Was Observed

Ran `EXP-20260625-735-generic-named-app-activation-live-micro` through the live
Codex subject harness with 12 samples: 4 prompts x 3 arms.

Prompts:

1. `Create a to-do app`
2. `Create a tiny personal budget app in this folder.`
3. `Build a simple local meal planner.`
4. `Make a small workout timer app. Keep it simple.`

Raw artifacts are under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/`

The runner wrote:

- `plan.json`
- `summary.json`
- `report.md`
- `canonical_guard.json`
- 12 raw subject artifacts
- 12 score artifacts
- prompt files, Codex command metadata, last messages, and subject workspaces

Current-10x result:

| Prompt | Changed files |
| --- | --- |
| `Create a to-do app` | `.10x/tickets/2026-06-25-create-todo-app.md` |
| `Create a tiny personal budget app in this folder.` | `.10x/tickets/2026-06-26-shape-tiny-personal-budget-app.md` |
| `Build a simple local meal planner.` | `.10x/tickets/2026-06-26-shape-local-meal-planner.md` |
| `Make a small workout timer app. Keep it simple.` | `.10x/tickets/2026-06-25-small-workout-timer-app-shaping.md` |

All current-10x tickets were `Status: blocked` shaping records. They excluded
implementation files and named unresolved platform, workflow, persistence, and
verification semantics. No current-10x workspace contained app/source files,
dependency manifests, tests, server files, frontend implementation files, data
files, or generated implementation artifacts.

No current-10x final message claimed 10x was unnecessary because the app was
small, simple, common, or personal.

No-10x-control result:

| Prompt | Changed files |
| --- | --- |
| `Create a to-do app` | `app.js`, `index.html`, `styles.css` |
| `Create a tiny personal budget app in this folder.` | `app.js`, `index.html`, `styles.css` |
| `Build a simple local meal planner.` | `index.html` |
| `Make a small workout timer app. Keep it simple.` | `index.html` |

Automated Trust Level 1 score summary:

| Arm | S001 average | S001 floor failures | S007 average |
| --- | ---: | ---: | ---: |
| current-10x | 85 | 0 | 61.25 |
| candidate-variant | 96.25 | 0 | 52.5 |
| no-10x-control | 15 | 4 | 10 |

`canonical_guard.json` recorded no changes to `SKILL.md` or
`autoresearch/program.md` during the run.

## Procedure

Command:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-generic-named-app-activation-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro --require-clean-canonical
```

Manual inspection read:

- `report.md`
- `canonical_guard.json`
- every current-10x raw artifact's `file_outputs`
- every current-10x final message
- every current-10x shaping ticket body
- no-10x-control `file_outputs`

The untracked results ledger was updated with:

```text
EXP-20260625-735-generic-named-app-activation-live-micro
```

## What This Supports Or Challenges

This supports the claim that canonical `SKILL.md` handles the generic named
greenfield app class, including the exact reported `Create a to-do app` wording,
without adding app-specific instruction text.

It also supports the contrast that minimal/no-10x defaults readily implement
these vague named app requests directly.

## Limits

This is a one-turn Codex MICRO. It does not prove behavior in Claude Code,
OpenCode beyond the separate packing-list sanity pass, oh-my-pi, multi-turn
ratification after the shaping tickets, or larger app requests where the user
supplies partial semantics across several turns.

The automated scorer is Trust Level 1 and secondary to manual inspection.
