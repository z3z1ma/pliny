Status: recorded
Created: 2026-06-26
Updated: 2026-06-26
Target: SKILL.md child-ticket-boundary corrective mutation
Verdict: pass

# Promote Ticket Boundary Corrective

## Target

The `SKILL.md` mutation that requires child-ticket boundaries to use the same
independence test as specification boundaries. The change prevents splitting
one cohesive implementation into setup, styling, interaction, verification,
evidence, or record-maintenance tickets merely because those activities occur
in sequence.

## Findings

- Pass: The mutation targets a concrete observed failure. In
  `EXP-20260626-745`, current `SKILL.md` avoided god specs and app-file
  implementation, but split one cohesive static app into shell, interaction,
  and verification child tickets.
- Pass: The mutation preserves the key invariants. It does not weaken
  spec-first behavior, the Outer Loop/Inner Loop gate, parent/child ownership,
  evidence requirements, or anti-god-spec pressure.
- Pass: The new behavior is narrow. It tells the agent to keep one coherent
  implementation plus its required proof in one executable child ticket when
  the same executor can complete and verify the outcome.
- Pass: The mutation still permits real decomposition. It allows child splits
  for independent deliverables, distinct governing specifications or behavior
  surfaces, real handoff dependencies, materially different execution
  environments, and verification/review work that requires distinct authority.
- Concern: The language may reduce separate verification-ticket creation for
  some workflows where independent verification is useful but not strictly
  required. This is acceptable because formal review remains available, and the
  ticket still must record evidence before closure.
- Concern: The corrective evidence is Codex-only and one repetition. It should
  be treated as enough for this narrow promotion, not as broad harness proof.

## Verdict

Pass. Promote the mutation.

## Residual Risk

Non-Codex harness behavior remains unproven. Future experiments should test the
same spec-first and ticket-boundary behavior in Claude Code, OpenCode, and
oh-my-pi, especially for todo-app-style greenfield requests and multi-surface
requests where separate specs and separate child tickets are genuinely required.
