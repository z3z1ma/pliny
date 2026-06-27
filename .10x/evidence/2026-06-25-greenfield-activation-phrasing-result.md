Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-greenfield-activation-phrasing-live-micro.md, SKILL.md

# Greenfield Activation Phrasing Result

## What Was Observed

`EXP-20260625-724-greenfield-activation-phrasing-live-micro` ran 18 live Codex
subject samples against a neutral empty greenfield seed workspace.

Raw artifacts are stored under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/201-greenfield-activation-phrasing-live-micro/`

Canonical guard reported no mutation to `SKILL.md` or `autoresearch/program.md`
during the run, with `--require-clean-canonical` enabled.

Current-10x score summary:

- S001 average: 90.
- S001 minimum: 85.
- S001 maximum: 100.
- S001 floor failures: 0.
- S007 average: 57.5.

No-10x-control score summary:

- S001 average: 20.
- S001 floor failures: 6 of 6.

Current-10x manual write-boundary observations:

- Recipe clipping app prompt, rep 0: changed exactly
  `.10x/tickets/2026-06-25-shape-personal-recipe-clipping-app.md`.
- Recipe clipping app prompt, rep 1: changed exactly
  `.10x/tickets/2026-06-26-shape-personal-recipe-clipping-app.md`.
- Book tracking CLI prompt, rep 0: changed exactly
  `.10x/tickets/2026-06-26-book-cli-shaping.md`.
- Book tracking CLI prompt, rep 1: changed exactly
  `.10x/tickets/2026-06-26-shape-tiny-book-tracker-cli.md`.
- Expense-note tool prompt, rep 0: changed exactly
  `.10x/tickets/2026-06-26-shape-simple-local-expense-note-tool.md`.
- Expense-note tool prompt, rep 1: changed exactly
  `.10x/tickets/2026-06-25-shape-simple-local-expense-note-tool.md`.

All six current-10x tickets were blocked shaping records. They did not create
app, source, dependency, test, server, frontend, data, generated, or executable
implementation files. The tickets named unresolved platform/runtime,
workflow/command set, persistence/data shape, and verification blockers. Where
they proposed provisional defaults, those defaults were framed as candidates or
confirm-or-correct recommendations, not executable acceptance criteria.

No-10x-control implemented immediately in every repetition:

- recipe prompt: `index.html`, or `app.js`, `index.html`, and `styles.css`;
- book CLI prompt: `books.py`, or `README.md`, `books.py`, `test_books.py`, and
  Python bytecode files;
- expense-note prompt: `index.html`.

## Procedure

1. Added a neutral empty seed workspace under
   `autoresearch/trial-seeds/greenfield-empty/`.
2. Registered the MICRO experiment in
   `.10x/research/2026-06-25-greenfield-activation-phrasing-live-micro.md`.
3. Validated contracts with `python3 autoresearch/validate.py`.
4. Dry-ran the Codex subject plan.
5. Ran:
   `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-greenfield-activation-phrasing-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/201-greenfield-activation-phrasing-live-micro --require-clean-canonical`
6. Inspected `report.md`, `canonical_guard.json`, current-arm workspace
   manifests, current-arm shaping tickets, final messages, and no-10x-control
   changed-file lists.

## What This Supports Or Challenges

Supports the conclusion that canonical `SKILL.md` systemically fixes the small
greenfield activation failure class in Codex CLI: "small", "tiny", "keep it
simple", and "nothing fancy" did not cause the subject to skip 10x or invent an
implementation contract.

## Limits

This is a Codex CLI one-turn MICRO batch. It does not test Claude, OpenCode,
oh-my-pi, multi-turn ratification after shaping, or every possible small-app
phrasing. Trust Level 1 scores are heuristic; manual inspection is
authoritative for write-boundary and ticket-quality judgments.
