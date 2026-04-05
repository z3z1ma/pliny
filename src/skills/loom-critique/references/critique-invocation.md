# Critique Harness Invocation

## Parent-Side Goal

Use this invocation when the parent has compiled a critique packet and wants one bounded review pass in a fresh child context.

This is a fresh reviewer session, not a continuation of the executor's prior reasoning.

The launch should create a clean review pass that is durable enough to remain useful after the current session ends.

## Resolving The Command

Resolve the harness invocation using the standard resolution order before launching:

1. **Check `.loom/harness.md`** — if the workspace has operator-defined harness profiles, select the profile that best matches the current task. Read the profile's prose to understand when it applies, then substitute `{{ packet_path }}` and `{{ prompt }}` into the command template.

2. **Discover the current harness** — if no `.loom/harness.md` exists, discover the harness you are running inside. Check the parent process name (`ps -o comm= -p $PPID`), check for environment markers, then learn the discovered tool's headless invocation syntax via its help output. Construct the command using that tool's file-attachment and prompt arguments.

3. **Ask the operator** — if discovery is ambiguous, ask the operator to create `.loom/harness.md` or provide the invocation command directly. Do not guess.

For the full harness profile convention and resolution details, read the harness-invocation-templates appendix in the core rules.

## Preflight Checklist

Before launching critique, the parent should confirm:

1. the review question is explicit
2. the focus areas are explicit
3. the evidence set is narrow enough for one bounded review
4. the packet says what kind of output is expected
5. the parent knows where the durable critique result should land
6. the harness invocation is resolved (not guessed)

If the review question is vague, fix that before launch. Broad critique prompts create broad, shallow review.

## Prompt Shape

Use a short prompt that tells the child what review job to perform.

Recommended prompt template:

```text
Run a bounded critique from the supplied packet. Answer the review question using the listed evidence, classify findings by severity and confidence, summarize residual risk, and recommend the next action the parent should take.
```

Strong prompt qualities:

- names the review question explicitly
- tells the child to use the packet evidence set rather than broadening scope casually
- asks for verdict, findings, residual risk, and next action
- does not ask the child to both implement and critique in one pass

## Child Procedure

Before making judgments:

- read the critique packet
- review the target against its broader constitutional, initiative, research, spec, plan, and ticket context when relevant
- look for bugs, unsafe assumptions, missing tests, edge cases, architectural drift, and unsupported claims

The reviewer should assume plausible work may still be wrong and should prefer evidence-backed concerns over impressionistic disagreement.

When done:

- land a durable critique result
- preserve each concrete issue as a durable finding when needed
- recommend follow-up work explicitly instead of leaving review debt in chat

If the evidence is insufficient, the reviewer should say what is missing and what would resolve the uncertainty.

The reviewer should also avoid two common failure modes:

- restating the packet summary without performing a real review
- inventing a strong verdict when the evidence set is obviously incomplete

## Expected Output Shape

The parent should expect:

- verdict
- findings list
- residual risks
- follow-up recommendations
- confidence or evidence-strength notes where appropriate

An especially strong output also includes:

- reviewed artifact identity
- the evidence basis that mattered most to the verdict
- explicit unknowns that still block strong confidence

## Reconciliation After Return

After the child returns, the parent should:

1. persist or update the critique record
2. create or link follow-up tickets when execution work is needed
3. update the reviewed ticket, plan, or spec if critique changes the next durable step

If a critique launch returns without a durable critique result, treat the review as failed.

Successful process exit without a durable critique result is not a valid review outcome.

## Retry Guidance

Recompile the critique packet instead of retrying blindly when:

- the review question changed
- key evidence was missing
- the target changed materially after the prior packet was compiled

## Anti-Pattern

This is a bad critique launch prompt:

```text
Review this and let me know what you think.
```

Why this is bad:

- the review question is missing
- the evidence boundary is missing
- the child is likely to produce broad, shallow commentary instead of a durable bounded review
