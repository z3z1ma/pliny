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

The parent-supplied `{{ prompt }}` is the main place to specify critique emphasis. Use it to tell the child what lens to apply while keeping the packet as the bounded target, scope, and evidence contract.

Recommended prompt template:

```text
Run a bounded critique from the supplied packet. Follow the packet contract and review the target using the emphasis below. Answer the review question using the listed evidence, classify findings by severity and confidence, summarize residual risk, and recommend the next action the parent should take.
```

Strong prompt qualities:

- names the review question explicitly
- names the emphasis explicitly
- tells the child to use the packet evidence set rather than broadening scope casually
- asks for verdict, findings, residual risk, and next action
- does not ask the child to both implement and critique in one pass

Good emphasis examples:

- devil's-advocate pressure test: assume the target may hide subtle flaws and look for unsupported optimism, hidden failure modes, and missing edge-case handling
- verifier-style review: test whether the claimed conclusions are actually supported by the cited evidence and note where confidence is too strong for the available proof
- focused review: spend most of the review budget on one area such as tests, packet boundaries, architectural drift, or acceptance readiness

Prompt responsibility:

- the packet carries the bounded contract: target, scope, evidence set, and output expectations
- the prompt carries the dynamic review lens: what to stress, what to doubt most, and where to spend the child's attention

Keep the prompt bounded. It may sharpen the review, but it should not silently widen scope, override the packet, or pre-decide the verdict.

Example prompt patterns:

```text
Run a bounded critique from the supplied packet. Use a devil's-advocate lens: assume the target may still be wrong even if it looks plausible, and spend extra attention on hidden failure modes, edge cases, and unsupported claims. Stay inside the listed evidence and return verdict, findings, residual risks, and next action.
```

```text
Run a bounded critique from the supplied packet. Use a verifier-style lens: focus on whether the target's claims are actually supported by the cited evidence, whether confidence is overstated, and what proof is still missing. Stay inside the listed evidence and return verdict, findings, residual risks, and next action.
```

```text
Run a bounded critique from the supplied packet. Focus most of the review on packet boundary clarity and follow-up readiness. Stay inside the listed evidence and return verdict, findings, residual risks, and next action.
```

## Child Procedure

Before making judgments:

- read the critique packet
- review the target against its broader constitutional, initiative, research, spec, plan, and ticket context when relevant
- look for bugs, unsafe assumptions, missing tests, edge cases, architectural drift, and unsupported claims

The reviewer should assume plausible work may still be wrong and should prefer evidence-backed concerns over impressionistic disagreement.

When the parent supplies an emphasis in the prompt, the child should follow that emphasis without treating it as permission to broaden scope or skip the normal critique quality bar.

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
- the review emphasis is missing
- the evidence boundary is missing
- the child is likely to produce broad, shallow commentary instead of a durable bounded review
