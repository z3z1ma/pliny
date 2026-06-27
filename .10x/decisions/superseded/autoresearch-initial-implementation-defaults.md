Status: superseded
Created: 2026-06-23
Updated: 2026-06-27

Superseded-By:

- `.10x/decisions/autoresearch-live-trial-scientist-inspection.md`

# Autoresearch Initial Implementation Defaults

## Context

The 10x autoresearch specification is ready to implement, but several defaults
control how the first tickets should be sliced: first harness, control policy,
artifact storage, budget boundaries, scorer authority, and score-weight policy.

The operator accepted a MICRO-first simulator route followed by Codex FULL runs,
confirmed that no-10x controls must suppress default `AGENTS.md` / `CLAUDE.md`
loading, and delegated initial budget sizing to the agent with the constraint
that limits should be large enough to avoid routine friction but not unbounded.

## Decision

Use these initial implementation defaults:

- Build the MICRO layer against transcript/file-output fixtures first.
- Use Codex as the first FULL harness after MICRO scoring is credible.
- Compare three arms by default: minimal no-10x harness defaults, current
  canonical `SKILL.md`, and candidate variant.
- Ensure the no-10x control arm prevents harness-default 10x instructions from
  loading through `AGENTS.md`, `CLAUDE.md`, or equivalent files.
- Record the actual model and harness used per run rather than baking model names
  into the score semantics.
- Use a MICRO campaign cap of 300 subject-agent samples or 10 wall-clock hours.
- Use a FULL campaign cap of 20 harness runs or 36 wall-clock hours, with a
  3-hour suggested cap per individual FULL run.
- Apply no monetary cap to subscription-backed Codex, Claude, OpenCode, or
  oh-my-pi runs.
- Require a new budget decision before using metered APIs or paid cloud resources
  beyond USD 250 estimated spend.
- Store claim-supporting raw artifacts under `.10x/evidence/.storage/` and
  exploratory source material under `.10x/research/.storage/`.
- Place reusable implementation assets outside `.10x/` under a top-level
  `autoresearch/` directory so `.10x/` remains the durable record graph rather
  than the code/tooling tree.
- Keep Trust Level 3 scorer approval human-only until a later decision delegates
  it.
- Track human inspection time separately at first.
- Keep score weights fixed and transparent until enough human verdicts justify a
  later scoring-policy decision.

## Alternatives Considered

- Start with a full Codex runner immediately: rejected because score and scenario
  credibility should be proven cheaply before full harness complexity.
- Use only current 10x as the control: rejected because no-guidance behavior is
  needed to know whether a scenario elicits the target failure.
- Put raw artifacts only in research storage: rejected because claim-supporting
  run artifacts are evidence, not just research source material.
- Set tight monetary caps: rejected for subscription-backed tools because the
  operator does not care about marginal subscription usage and operational caps
  are more relevant.
- Learn score weights immediately: rejected because there are not enough human
  verdicts to justify learned weighting.

## Consequences

The first implementation can be sliced without further product ambiguity. Early
work should produce static catalogs, validators, fixture-based offline scoring,
and then MICRO execution before FULL Codex integration.

The no-10x control requires harness isolation. Any runner that invokes Codex,
Claude Code, OpenCode, or oh-my-pi must be able to prevent project-level 10x
instruction files from contaminating the control arm.

Budget enforcement is operational rather than financial for subscription-backed
harnesses. If later work introduces metered APIs or paid cloud resources, the
budget decision must be revisited before spend exceeds the recorded threshold.
