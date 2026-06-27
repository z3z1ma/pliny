Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: none
Depends-On: .10x/decisions/superseded/autoresearch-subject-harness-policy.md, .10x/tickets/done/2026-06-23-candidate-executing-evaluation-surface.md

# Add Dynamic Subject Continuations

## Scope

Support subject-agent clarification questions without adding a loop controller,
fixed follow-up arrays, or Python completion heuristics.

Included:

- Let one live Codex subject run continue from a prior raw artifact's transcript
  and workspace.
- Let the LLM researcher provide arm-specific next user messages because
  different stochastic subject agents may ask different questions.
- Record the prior raw artifact, prior turn count, combined transcript, and new
  turn artifacts.
- Keep `run_once.py` as a one-iteration runner; do not add resume loops,
  stop files, candidate generation, or automatic "done" decisions.

Excluded:

- Automatic answer generation by Python.
- Automatic detection that a subject question is answered or that a task is
  complete.
- Static follow-up arrays in scenario definitions.
- Canonical `SKILL.md` changes.

## Acceptance Criteria

- AC-001: A continuation scenario can map each arm to its prior raw artifact.
- AC-002: A continuation scenario can provide a different next user message for
  each arm.
- AC-003: The runner writes a raw artifact whose transcript contains prior
  turns plus exactly one new user/assistant turn.
- AC-004: The score artifact validates against the existing scorer contract.
- AC-005: Public plans do not expose full prompts or instruction text.
- AC-006: Documentation states that the LLM researcher, not the runner, decides
  whether to continue, score, mark inconclusive, or ask the human.

## Progress And Notes

- 2026-06-23: Opened after operator pointed out that fixed follow-up arrays are
  invalid for stochastic subject agents. A subject may ask questions in a
  different order or phrase a different material uncertainty, so continuation
  input must be selected after reading the transcript.
- 2026-06-23: Updated `autoresearch/run_codex_subject.py` so scenarios may use
  `prior_raw_paths` for per-arm transcript/workspace continuation and
  `prompts_by_arm` for per-arm next user messages.
- 2026-06-23: Added focused unit coverage in
  `autoresearch/tests/test_run_codex_subject.py` showing that a continuation
  records one new live call per arm, preserves the prior turn count, combines
  transcript turns, accepts arm-specific answers, validates score artifacts, and
  sanitizes prompts in the public plan.
- 2026-06-23: Updated `autoresearch/program.md`, `autoresearch/README.md`,
  `autoresearch/templates/experiment.md`, and
  `.10x/decisions/superseded/autoresearch-subject-harness-policy.md` to make dynamic,
  researcher-owned continuation the only documented clarification path.
- 2026-06-23: Evidence recorded at
  `.10x/evidence/2026-06-23-dynamic-subject-continuations.md`.

## Blockers

None.
