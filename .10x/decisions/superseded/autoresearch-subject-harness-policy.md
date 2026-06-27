Status: superseded
Created: 2026-06-23
Updated: 2026-06-27

Superseded-By:

- `.10x/decisions/autoresearch-live-trial-scientist-inspection.md`

# Autoresearch Subject Harness Policy

Supersedes:

- `.10x/decisions/superseded/autoresearch-live-harness-required-for-optimization.md`

## Context

The first active SKILL.md autoresearch run exposed two false-validity paths:

- Fixture-backed MICRO runs can assign the candidate arm to a prewritten pass
  fixture and produce good-looking score artifacts without executing candidate
  instructions.
- The earlier Codex FULL fixture-smoke runner could produce FULL-shaped
  artifacts without invoking Codex as the subject agent.

Those paths are useful only for calibration, plumbing, or historical debugging.
They are not optimization evidence.

The earlier implementation also briefly introduced an `execution_mode` flag for
live Codex subject execution. That blurred concepts: MICRO and FULL are method
tiers describing scenario breadth, while `harness` and scenario shape describe
execution.

## Decision

Optimization experiments MUST execute the subject harness. A candidate arm must
run with candidate instructions loaded, and its score must come from observed
subject output rather than a prewritten pass fixture.

MICRO and FULL remain scenario breadth tiers:

- MICRO isolates one behavior or failure mode in a narrow task.
- FULL broadens scenario coverage and realism.

Both MICRO and FULL may use the same live harness. For the first Codex harness,
`harness: codex-cli` with prompt scenarios means a live Codex subject run.

`run_once.py` is live-only. It runs MICRO and FULL experiments through the live
subject harness path. Fixture-backed calibration remains a separate
`run_micro.py` utility, not an autoresearch iteration path.

Do not use an `execution_mode` experiment flag to choose live candidate
execution.

Subject-agent clarification is also outside runner control. When a subject asks
a question, the LLM researcher reads the raw transcript and may register one
continuation turn with `prior_raw_paths` plus `prompts_by_arm` for arm-specific
answers. The runner executes that single registered turn against the prior
transcript and workspace. It does not carry fixed follow-up arrays or decide
when the conversation is complete.

## Alternatives Considered

Keep fixture-backed MICRO as the optimization loop.

Rejected because it can assign the candidate arm to a pass fixture and report
good scores without executing candidate instructions.

Keep `execution_mode: codex-live-subject`.

Rejected because it hides the real model. The method tier should answer "how
broad is this experiment?" and the harness should answer "what executes the
subject?"

Keep the FULL fixture-smoke runner as a calibration utility.

Rejected because it creates an attractive wrong path: a FULL-labeled run that
does not execute the subject harness. MICRO fixture calibration is enough for
scorer/report plumbing.

Use only FULL for live harnesses.

Rejected because MICRO is supposed to test one specific behavior cheaply and
quickly. A narrow live Codex task is a valid MICRO experiment.

## Consequences

Autoresearch results based only on fixture-backed runs are not
candidate-quality evidence.

`run_once.py` dispatches live Codex subject definitions for both MICRO and FULL.
Fixture and smoke definitions are not part of the `run_once.py` surface.

Future candidate promotion attempts must include live or manually inspected
subject-agent output where the candidate instruction text was actually loaded.

Clarification-heavy scenarios require the researcher to preserve per-arm
conversation state explicitly. This adds a little experiment-definition work,
but it avoids pretending stochastic subject questions can be handled by one
prewritten follow-up sequence.
