# Docs Harness Invocation

## Parent-Side Goal

Use this invocation when the parent has compiled a docs packet and wants one fresh child context to synthesize accepted truth into a durable explanation.

This is a fresh documentation-maintainer pass, not a continuation of the parent's prior reasoning transcript.

The launch should produce a durable explanation that can stand on its own for a later reader.

## Resolving The Command

Resolve the harness invocation using the standard resolution order before launching:

1. **Check `.loom/harness.md`** — if the workspace has operator-defined harness profiles, select the profile that best matches the current task. Read the profile's prose to understand when it applies, then substitute `{{ packet_path }}` and `{{ prompt }}` into the command template.

2. **Discover the current harness** — if no `.loom/harness.md` exists, discover the harness you are running inside. Check the parent process name (`ps -o comm= -p $PPID`), check for environment markers, then learn the discovered tool's headless invocation syntax via its help output. Construct the command using that tool's file-attachment and prompt arguments.

3. **Ask the operator** — if discovery is ambiguous, ask the operator to create `.loom/harness.md` or provide the invocation command directly. Do not guess.

For the full harness profile convention and resolution details, read the harness-invocation-templates appendix in the core rules.

## Preflight Checklist

Before launching docs work, the parent should confirm:

1. the target doc is identified
2. the audience is identified
3. the truth sources are accepted enough to support the doc update
4. the packet declares the allowed write set
5. the parent is ready to review the claims afterward
6. the parent knows whether the work should update an existing doc or create a new governed explanation
7. the harness invocation is resolved (not guessed)

If the surrounding reality is still unsettled, postpone docs work and return to execution or critique first.

## Prompt Shape

Use a short prompt that positively states what the explanation should accomplish.

Recommended prompt template:

```text
Update the target documentation record from the supplied packet. Explain the accepted system shape for the intended audience, use the linked truth sources and verification basis, and return changed files, verification basis used, and stale triggers or remaining gaps.
```

Strong prompt qualities:

- names the audience
- emphasizes accepted reality instead of speculative future state
- asks for stale triggers or remaining gaps, not just changed prose
- keeps the write target bounded

## Child Procedure

Before writing:

- read the packet
- identify the target document, audience, truth sources, and verification basis
- prefer updating or superseding the governed explanation instead of creating a parallel active explanation
- describe accepted reality, not plans that have not landed

The maintainer should write as if the next reader was not present for the implementation but still needs a trustworthy explanation.

When ready:

- update only the allowed target document
- keep the explanation high-level, explanatory, and useful to a future reader who was not present during implementation
- report what changed and what evidence basis supports it

If the packet or truth-source set reveals that no durable explanation should be published yet, surface that honestly instead of forcing a thin doc update.

The child should avoid these failure modes:

- rephrasing tickets instead of explaining accepted system shape
- overclaiming beyond the linked evidence basis
- fragmenting the docs surface by creating a parallel explanation when an existing governed doc should be updated

## Expected Output Shape

The parent should expect:

- changed docs
- verification basis used
- stale triggers or gaps
- any claim that still needs stronger evidence before acceptance

An especially strong output also includes:

- the target audience restated clearly
- the key truth sources that were most important to the explanation
- a note about whether the update supersedes an earlier explanation

## Reconciliation After Return

After the child returns, the parent should:

1. inspect the changed doc
2. confirm the explanation matches the linked truth sources
3. update docs disposition in the relevant ticket if needed
4. record or link verification evidence if the docs pass materially depends on it

If a docs-maintainer launch returns without a durable docs revision, treat the run as failed rather than as good-enough docs work.

Successful process exit without a durable docs revision is not enough.

## Retry Guidance

Recompile the docs packet instead of retrying blindly when:

- the accepted shape changed
- the audience changed
- the truth-source set changed
- the prior draft overclaimed what the evidence supports

## Anti-Pattern

This is a weak docs prompt:

```text
Update the docs to reflect the latest changes.
```

Why this is weak:

- it does not say which document to update
- it does not identify audience or evidence basis
- it does not guard against overclaiming unsettled work
