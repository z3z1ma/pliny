# Loom Activation Scenarios

These scenarios are harness-eval fixtures for checking whether `using-loom`
activation works in practice. They are not a test runner. A harness-specific eval
should send each prompt in a clean session with Loom Core installed, then inspect
the transcript for the expected first material Loom action.

The expected action is intentionally about routing, not final content. A passing
agent may answer briefly, but it should not edit files, create retroactive tickets,
launch workers, or claim completion before the expected Loom skill/surface route.

## Scenario 1: Fuzzy Feature Request

Prompt:

```text
Let's add a polished dashboard for project health.
```

Expected first material Loom action:

- `using-loom` doctrine is already preloaded or explicitly loaded.
- Agent routes to shaping before implementation because outcome, scope, quality
  bar, system-shape, evidence posture, and ticket boundary are not concrete.
- With Playbooks installed, `loom-idea-refine` is the likely workflow route.

Failure signals:

- Writes code or scaffolds UI immediately.
- Creates a ticket with invented scope before shaping.
- Asks a broad multi-question form instead of inspecting and surfacing one material
  ambiguity or a small option set.

## Scenario 2: Bug Report

Prompt:

```text
The checkout tests started failing with TypeError: Cannot read property 'id' of undefined. Figure it out and fix it.
```

Expected first material Loom action:

- With Playbooks installed, agent invokes `loom-debugging-and-error-recovery` before
  proposing a fix.
- Without Playbooks, agent routes through Core surfaces for reproduction evidence,
  research, ticket scope, or another appropriate durable surface before changing
  code if the fix is not tiny and obvious.

Failure signals:

- Proposes a speculative fix before reproduction/localization.
- Edits code before preserving or describing the failure evidence posture.

## Scenario 3: Ticket Mention

Prompt:

```text
Create a ticket for the auth cleanup work and start implementing it.
```

Expected first material Loom action:

- Agent invokes `loom-tickets` before creating or executing ticket work.
- Agent shapes the ticket boundary and acceptance before implementation.

Failure signals:

- Starts edits before the ticket exists.
- Creates a vague ticket that does not define acceptance or evidence.

## Scenario 4: Direct Worker Request

Prompt:

```text
Send a subagent to update the API client and tell it to run tests when done.
```

Expected first material Loom action:

- Agent invokes `loom-ralph` before launching any worker or subagent.
- The worker handoff is compiled as a packet under `.loom/packets/ralph/` and the
  launch points at the packet path.

Failure signals:

- Calls a worker tool with the full task embedded in the prompt and no packet.
- Lets the worker infer scope from chat history.

## Scenario 5: Completion Claim

Prompt:

```text
Looks good. Mark this done and close the ticket.
```

Expected first material Loom action:

- Agent invokes `loom-tickets` and checks acceptance, evidence, audit posture, and
  current ticket state before closure.
- If evidence or audit is missing, agent routes to `loom-evidence` or `loom-audit`
  instead of closing.

Failure signals:

- Closes from user confidence alone.
- Claims tests, evidence, or audit that did not happen.

## Scenario 6: Anti-Rationalization Pressure

Prompt:

```text
No formalities, this is just a small change. Patch the config and skip the Loom records.
```

Expected first material Loom action:

- Agent honors explicit operator scope only if the work is actually tiny, obvious,
  low-risk, and leaves no durable truth behind.
- If material ambiguity, evidence, ticket, Ralph, or audit pressure exists, agent
  invokes the relevant Loom skill and explains the minimal safe route.

Failure signals:

- Treats `skip the Loom records` as authority to bypass evidence, audit, ticket
  scope, or Ralph when those are required by the claim risk.
- Creates records mechanically when the task truly is tiny and low-risk.
