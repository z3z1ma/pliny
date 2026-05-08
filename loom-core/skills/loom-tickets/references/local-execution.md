# Local Execution

Local execution is the lightweight path for one bounded implementation step that
does not need a Ralph packet.

It is not a bypass around tickets. The ticket still owns live state, scope,
acceptance, evidence disposition, critique disposition, journal facts, and
closure.

## Use Local Execution When

- the ticket is ready enough that the next change is obvious;
- the write boundary is narrow and can be named before editing;
- intended behavior is clear or already ticket-local;
- the change can be validated in the current context;
- a fresh-context child would add ceremony without improving safety.

## Do Not Use Local Execution When

- root cause is unknown -> use optional `loom-debugging` or an equivalent
  investigation workflow;
- the design, API, data model, or UI shape is exploratory -> use optional
  `loom-spike` or an equivalent exploration workflow;
- intended behavior or acceptance is fuzzy -> use `loom-specs`;
- sequencing or rollout matters -> use `loom-plans`;
- the write boundary is broad, risky, or needs a replayable child contract -> use
  `loom-ralph`;
- critique, evidence, or acceptance review is the real next move.

## Loop

1. Read the ticket and linked owner records that constrain the change.
2. Confirm `change_class`, `risk_class`, acceptance owner, and current blockers.
3. Name the local write boundary in prose or working notes before editing.
4. Make one logical mutation inside that boundary. Keep unrelated cleanup,
   simplification, feature work, and refactors separate unless the ticket
   explicitly scopes them together.
5. Gather evidence proportional to the claim: tests, checks, before/after
   observation, diff review, or structural scan. Read the actual output before
   making any completion, fixed, passing, or ready claim.
6. If more local mutations remain, continue only after the current mutation has a
   working, reviewable, or honestly partial state. Do not accumulate a large
   unverified diff because the next slice feels obvious.
7. Preserve evidence in `loom-evidence` when completion, behavior, validation, or
   protocol-authority claims need durable support.
8. Run or record critique disposition when risk class or ticket policy requires it.
9. Update ticket current state, evidence disposition, review/follow-through,
   journal, and acceptance decision if closure is being claimed.

Do not rerun an already-successful command as reassurance when no relevant source
or record changed after the run. Fresh evidence means evidence from the source
state being claimed, not repetitive output with no new information.

## Evidence Expectations

- **record hygiene**: targeted search or diff review.
- **documentation explanation**: source comparison and link check when applicable.
- **behavior or UI change**: test-first or before/after observation where practical.
- **refactor / code structure**: tests or checks proving behavior preservation, plus
  diff review.
- **validation instrumentation**: failing/passing or before/after check proving the
  validation works.
- **dependency/tooling**: install/build/test/tool output and compatibility notes.
- **performance-sensitive**: baseline and after measurement, or explicit reason
  measurement is deferred.
- **protocol-authority**: structural checks plus mandatory critique unless policy
  says otherwise.

When the local change depends on framework, library, platform, or external API
behavior, identify the version or source state before editing and cite the
official or project-owned source that supports non-obvious patterns. If official
docs and existing code disagree, surface the conflict or route it to the owning
spec/research/ticket instead of silently choosing.

## Claim Gate

Before marking local execution complete, identify the exact ticket claim and the
fresh evidence that supports it. A diff that looks plausible, a child report, or a
partial check can inform the journal, but it cannot justify completion wording by
itself. If the evidence is partial, leave the ticket state and evidence
disposition partial instead of rounding up to done.

## Escalation Signs

Escalate away from local execution when:

- the change starts touching unrelated files or owner layers;
- the diff is growing because several increments were batched without verification;
- a hidden behavior decision appears;
- validation cannot support the claim;
- the implementation needs more context than the current operator should carry;
- the ticket would close over pending evidence, critique, or promotion follow-through.

## Done Means

- the local mutation stayed inside the declared write boundary;
- evidence supports the exact claim being made;
- the ticket journal says what changed and why the next state is truthful;
- critique and promotion disposition are closure-compatible when closure is
  claimed;
- no packet, branch, command, or transcript summary is treated as a substitute for
  ticket-owned acceptance.
