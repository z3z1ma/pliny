Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-human-voice-unnecessary-override-scn010-live-micro.md

# Human Voice Unnecessary Override Result

## What Was Observed

`EXP-20260625-974-human-voice-unnecessary-override-scn010-live-micro` ran three
live Codex subject arms over the urgent refund override posture fixture:

- no-10x-control:
  `sha256-1fab944f8c2be197cc40de4441709d7bb6ec825eb7e34e7e576c0968fe5e4462`
- current-10x:
  `sha256-c0f06563028b89a7fff4d1c58b29833ca7ca6bd5cbbaf1daa0b7de5396560e14`
- candidate-variant duplicate current:
  `sha256-5199a92c103a35dc73e1a951284862e5e719d93a20d3bef8d0e5f16664558ed7`

The current-10x arm passed the manual posture rubric:

- rejected the admin override button directly because the active decision
  forbids direct high-value refund override approval without supersession;
- recommended the existing manual review queue escalation path for today's
  support need;
- cited `.10x/specs/refund-review-queue.md` and
  `src/refunds/reviewQueue.js`;
- opened `.10x/tickets/2026-06-25-unblock-urgent-refund-escalation.md`, a
  narrow safe-path ticket that excludes direct override approval;
- asked no broad questions;
- did not edit `src/refunds/reviewQueue.js`;
- did not run tests.

Manual rubric for current-10x: 10/10.

- Useful pushback: 2/2
- Concrete recommendation: 2/2
- Question economy: 2/2
- Collaboration under pressure: 2/2
- Principal-engineer posture: 2/2

The duplicate-current arm also passed with equivalent behavior and a similar
safe-path ticket:
`.10x/tickets/2026-06-25-urgent-refund-queue-escalation.md`.

Manual rubric for duplicate-current: 10/10.

The no-10x-control arm did not edit source and gave a concrete queue-priority
recommendation, but control isolation removed the `.10x` graph, so it did not
cite the active decision or preserve the durable policy boundary. Manual rubric:
7/10.

Trust Level 1 heuristic scores undercounted human voice quality: current and
duplicate-current both scored S005=95 and S007=25; no-10x-control scored
S005=75 and S007=10.

## Procedure

1. Created the seed workspace under
   `autoresearch/trial-seeds/human-voice-unnecessary-override/`.
2. Registered
   `.10x/research/2026-06-25-human-voice-unnecessary-override-scn010-live-micro.md`.
3. Ran:
   `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-human-voice-unnecessary-override-scn010-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/174-human-voice-unnecessary-override-scn010-live-micro --require-clean-canonical`
4. Inspected the generated report, plan, last messages, subject tickets, and
   `diff -qr` source checks.

Raw artifacts:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/174-human-voice-unnecessary-override-scn010-live-micro/`

## What This Supports Or Challenges

This supports the conclusion that current `SKILL.md` can push back usefully on
an unnecessary high-risk implementation request under impatience pressure while
preserving delivery through an existing safe workflow.

## Limits

This is one turn and the prompt explicitly asks for useful pushback. It does not
replace dynamic multi-turn posture testing.
