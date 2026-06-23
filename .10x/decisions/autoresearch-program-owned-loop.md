Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Autoresearch Program-Owned Loop

## Context

Autoresearch was drifting toward Python-owned long-running orchestration:
resumable state, event logs, stop files, generated-candidate controllers, and
days-oriented loop templates. That architecture conflicted with the intended
Karpathy-style autoresearch pattern: a stable human-owned `program.md` instructs
the LLM researcher, while the LLM itself decides mutations, branches, keep or
discard decisions, and indefinite continuation.

The useful parts of the implementation are the measurement pieces: score
catalogs, scenario catalogs, one-shot MICRO/FULL runners, score artifacts,
reports, calibration, and isolation diagnostics. Those should remain.

## Decision

10x autoresearch uses a program-owned loop:

- `autoresearch/program.md` is the human-owned research program.
- The LLM reasoning engine owns repeated iteration.
- Python utilities run one experiment, score artifacts, validate contracts,
  render reports, or run diagnostics.
- Python utilities do not own long-running strategy, candidate generation,
  resumable state, stop files, or autonomous control flow.
- `autoresearch/run_once.py` is the core execution command for one MICRO or FULL
  experiment.

Canonical `SKILL.md` remains human-promoted. Candidate artifacts may be edited
autonomously during research runs, but `program.md` and canonical `SKILL.md` are
not edited unless the human asks.

## Alternatives Considered

- **Keep `run_loop.py` as optional support.** Rejected. Keeping the controller
  would leave the wrong architecture available and invite future agents to route
  autonomy through Python state management.
- **Demote live candidate generation to an experimental utility.** Rejected for
  the same reason. Candidate generation should be an LLM reasoning activity
  governed by `program.md`, not a separate controller.
- **Delete all autoresearch tooling and keep only prose.** Rejected because the
  scoring harnesses, reports, and calibration utilities are useful and align
  with the one-iteration model.

## Consequences

The system is simpler and closer to the original autoresearch shape. A future
agent can run indefinitely by repeatedly reading `program.md`, editing a
candidate artifact, running `run_once.py`, logging scores, and deciding the next
mutation.

The repository no longer contains Python loop/state controllers. If future work
needs more automation, it should first prove that a one-shot command plus
`program.md` is insufficient.
