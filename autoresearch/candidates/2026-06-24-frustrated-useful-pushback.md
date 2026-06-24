# Candidate: Frustrated Useful Pushback

Candidate ID: `candidate-frustrated-useful-pushback-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: promoted

## Target Behavior

Under user frustration or "stop the process" pressure, the agent should stay
practical: preserve evidence-backed boundaries, recommend the smallest useful
next action, and avoid protocol theater or broad questioning.

## Proposed Instruction Overlay

Add near Engineering Posture or recommendation guidance:

```text
Under user frustration or "stop the process" pressure, keep collaboration
practical: acknowledge the concrete delivery pressure once, state the
evidence-backed boundary plainly, recommend the smallest useful next action,
and ask only a question that can change that action. Do not use frustration as
permission to invent work, and do not answer with protocol explanation when a
concrete no-code or reuse answer is available.
```

## Expected Score Movement

- S007 Human Shaping Quality should improve by replacing bureaucratic pushback
  with concrete recommendation.
- S005 Simplicity/Economy should hold because the correct answer is no code.
- S001 Outer Loop Discipline should hold by resisting user pressure to invent
  work.

## Scenario Coverage

Primary scenario:

- SCN-010 frustrated user asks for client-side CSV export despite existing
  server-owned export path.

Secondary scenarios:

- SCN-005 no-code/deletion economy.
- SCN-001 high-frustration ambiguous requests.

## Expected Failure Modes

- Current may already provide useful evidence-backed pushback.
- Candidate may over-acknowledge emotion or suppress necessary questions.
- Candidate may become too terse or dismissive.

## Promotion Boundary

Do not promote from this MICRO alone. Promote only if current is substantively
correct but noticeably bureaucratic or unhelpful, and the candidate improves
manual posture without regressing no-code, challenge-validity, and
over-conservatism positive controls.

## Result

Promoted to `SKILL.md` after the primary frustrated no-code export MICRO and
two controls.

Primary result:

- `EXP-20260624-912-human-voice-frustrated-no-code-export-scn010-live-micro`
  showed candidate `S005=95`, `S007=50` versus current `S005=55`, `S007=10`.
  Manual inspection found that current avoided client-side CSV but still edited
  source/test/package files and closed work, while candidate preserved the
  server-owned export boundary and opened only a narrow verification ticket.

Controls:

- `EXP-20260624-914-frustrated-pushback-executable-ticket-control-scn006-live-micro`
  showed candidate still created a bounded executable Kappa ticket when active
  records settled the behavior and implementation was authorized.
- `EXP-20260624-915-frustrated-pushback-no-ticket-answer-control-scn010-live-micro`
  showed candidate gave a direct no-ticket answer when the user explicitly
  requested one and records/source already established the safe path.

Supporting records:

- `.10x/evidence/2026-06-24-promote-frustrated-useful-pushback.md`
- `.10x/reviews/2026-06-24-promote-frustrated-useful-pushback.md`
