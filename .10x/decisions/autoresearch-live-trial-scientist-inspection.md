Status: active
Created: 2026-06-27
Updated: 2026-06-27

# Autoresearch Live Trial And Scientist Inspection

Supersedes:

- `.10x/decisions/superseded/autoresearch-initial-implementation-defaults.md`
- `.10x/decisions/superseded/autoresearch-program-owned-loop.md`
- `.10x/decisions/superseded/autoresearch-subject-harness-policy.md`

## Context

Autoresearch is not a fixture-backed scoring pipeline. Its useful shape is an
LLM researcher acting as the scientist: it registers a hypothesis, prepares a
clean-room trial, uses fresh subject-agent contexts to run the trial, inspects
raw outputs against the rubric, and records the verdict in durable `.10x/`
records.

The earlier tooling kept static offline fixtures, an offline heuristic scorer,
calibration labels, a fixture-backed MICRO runner, and score-artifact reports.
Those artifacts proved plumbing, but they made an attractive wrong path: a run
could look rigorous without executing candidate instructions or preserving the
researcher's judgment.

Live seed workspaces and prior raw artifacts are different. They are trial
starting states for fresh subject-agent runs, not canned pass/fail answer keys.
They remain useful for regression scenarios and hypothesis tests.

## Decision

Autoresearch uses a live-trial, scientist-inspected loop:

- `autoresearch/program.md` is the human-owned research program.
- The LLM reasoning engine owns repeated iteration, candidate design, trial
  interpretation, grading, and keep/discard decisions.
- Python utilities run one registered trial, validate static contracts, render
  trial artifact reports, or run diagnostics.
- The core execution command remains `autoresearch/run_once.py`.
- MICRO and FULL are scenario breadth tiers. Both execute the subject harness
  when used for candidate or current-skill evaluation.
- The live Codex subject runner records raw artifacts, command metadata, prompts,
  workspace archives, manifests, and summaries. It does not grade, calibrate, or
  emit score artifacts.
- Static offline fixtures, fixture-backed MICRO execution, heuristic offline
  scoring, and scorer calibration utilities are removed from the live tooling
  surface.
- Durable conclusions live in `.10x/research/`, `.10x/evidence/`, and
  `.10x/reviews/` records written by the researcher after inspection.

## Consequences

The setup is smaller and closer to the intended methodology. Experiments can
serve both as hypothesis tests and as regression/evaluation cases because each
trial is a reproducible prompt, workspace state, instruction arm, and artifact
bundle reviewed against the rubric.

Reports become secondary views over trial artifacts, not score authorities.
Promotion still requires explicit human approval for canonical `SKILL.md`.

The historical fixture-backed evidence remains history. It should not be used as
current proof that a candidate or the current skill works.
