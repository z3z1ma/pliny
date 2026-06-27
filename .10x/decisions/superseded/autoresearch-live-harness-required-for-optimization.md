Status: superseded
Created: 2026-06-23
Updated: 2026-06-23

# Autoresearch Optimization Requires Live Harness Execution

Superseded by:

- `.10x/decisions/superseded/autoresearch-subject-harness-policy.md`

## Context

The first active SKILL.md autoresearch run exposed a false-validity path:
fixture-backed MICRO and fixture-smoke FULL runs can produce score artifacts and
reports while never executing candidate instruction text. That is useful for
scorer calibration and report regression, but it cannot measure whether a
candidate improves agent behavior.

The earlier implementation also introduced an `execution_mode` flag to select a
live Codex subject path. That blurred concepts. MICRO and FULL are method tiers
that describe scenario breadth and experimental scope. They are not execution
mechanisms. Harness choice belongs to the `harness` field and the experiment's
scenario/fixture shape.

## Decision

Optimization experiments MUST execute the subject harness. A candidate arm must
run with the candidate instructions loaded, and its score must come from the
observed subject output, not from a prewritten pass fixture.

MICRO and FULL remain scenario breadth tiers:

- MICRO isolates a specific behavior or failure mode in a narrow task.
- FULL broadens scenario coverage and realism.

Both MICRO and FULL may use the same live harness. For the first Codex harness,
`harness: codex-cli` with no fixture mappings means a live Codex subject run.
Fixture-backed or fixture-smoke runners are allowed only for calibration,
regression testing, scorer debugging, and plumbing validation.

Do not use an `execution_mode` experiment flag to choose live candidate
execution.

## Alternatives Considered

Keep fixture-backed MICRO as the optimization loop.

Rejected because it can assign the candidate arm to a pass fixture and report
good scores without executing the candidate instructions.

Keep `execution_mode: codex-live-subject`.

Rejected because it hides the real model. The method tier should answer "how
broad is this experiment?" and the harness should answer "what executes the
subject?"

Use only FULL for live harnesses.

Rejected because MICRO is supposed to test one specific behavior cheaply and
quickly. A narrow live Codex task is a valid MICRO experiment.

## Consequences

Autoresearch results based only on fixture-backed or fixture-smoke runs are not
candidate-quality evidence.

`run_once.py` dispatches `codex-cli` definitions without fixture mappings to the
live Codex subject runner, while fixture-backed runners remain available for
calibration and regression checks.

Future candidate promotion attempts must include live or manually inspected
subject-agent output where the candidate instruction text was actually loaded.
