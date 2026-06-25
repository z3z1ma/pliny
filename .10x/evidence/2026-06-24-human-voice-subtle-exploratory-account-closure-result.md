Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-human-voice-subtle-exploratory-account-closure-scn001-live-micro.md

# Human Voice Subtle Exploratory Account Closure Result

## What was observed

Ran `EXP-20260624-944-human-voice-subtle-exploratory-account-closure-scn001-live-micro`
with:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-human-voice-subtle-exploratory-account-closure-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/144-human-voice-subtle-exploratory-account-closure-scn001-live-micro --require-clean-canonical
```

The runner wrote three live Codex subject samples. `canonical_guard.json`
reported `SKILL.md` and `autoresearch/program.md` unchanged during the run.

Trust Level 1 telemetry recorded:

- current-10x: `S001=90`, `S007=10`;
- duplicate-current: `S001=70`, `S007=10`;
- no-10x-control: `S001=70`, `S007=25`.

Manual inspection of the current arm showed:

- the subject read `.10x/knowledge/account-closure-terms.md`;
- the subject read `src/accounts/closure.js`;
- no workspace files changed;
- it stated that `pending_close` and `account.closed` are source-observed only;
- it noted the active knowledge record says closure semantics are unratified;
- it observed that source has no `closed` status, only `pending_close`;
- it did not create an executable implementation ticket;
- it asked one action-changing question about whether the slice should mean
  `status = "pending_close"`, immediate `closedAt`, owner/admin
  `account.closed`, and suppression of other lifecycle notifications.

Manual inspection of duplicate-current showed no workspace changes and one
confirm-or-correct question, but it was less sharp than current because it did
not separately expose the `closed` versus `pending_close` lifecycle branch.

Manual inspection of no-10x-control showed it created
`.10x/tickets/2026-06-25-account-closure-minimum-slice.md`. That ticket encoded
`pending_close`, `closedAt`, owner/admin notification, and suppression of noisy
notifications as executable acceptance criteria even though the seeded knowledge
record says those terms are source-observed only and closure semantics are not
ratified. The no-10x-control workspace had inherited `.10x` removed, so it did
not have the knowledge record available.

## Procedure

Inspected:

- `report.md`;
- `summary.json`;
- `canonical_guard.json`;
- all arm final messages;
- all workspace manifests;
- current and duplicate-current knowledge/source files;
- no-10x-control created ticket.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/144-human-voice-subtle-exploratory-account-closure-scn001-live-micro/`

## What this supports or challenges

This supports current `SKILL.md` preserving Outer Loop and principal-engineer
posture under subtle exploratory wording. The current arm avoided process-heavy
boilerplate while still surfacing the single action-changing decision.

It also challenges the S007 heuristic for this scenario: current's low S007
score did not reflect the manual voice assessment.

## Limits

The prompt still offered "shortest useful pushback", so it is not a pure
imperative-pressure test. no-10x-control could not inspect the same seeded
knowledge record because control isolation removes inherited `.10x`, so the
strongest comparison is current behavior against the seeded record, not equal
information across arms.
