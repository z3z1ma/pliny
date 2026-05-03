# Implementation Reality

Software work has one extra truth boundary that is not a Loom record layer:
the codebase owns current implementation reality.

That does not make code the owner of intended behavior. It means the source
tree is the observable system that may or may not match the records.

## Ownership Split

- spec owns intended behavior
- source code owns current implementation reality
- tests are executable instruments for expectations
- evidence records observed artifacts
- tickets own live execution state
- critique owns adversarial judgment about sufficiency and risk
- wiki owns accepted explanation

## Common Mistakes

Do not treat a spec as evidence that the code works.

Do not treat the current code as evidence that the project intended that behavior.

Do not treat a green test as a complete acceptance decision when required
critique, evidence, or retrospective / promotion follow-through remains open.

## Bridge Through Evidence

The usual software chain is:

```text
spec -> test or observation -> code behavior -> evidence -> critique -> ticket acceptance
```

If intended behavior and implementation reality diverge, route to the owner:

- intended behavior unclear -> `loom-specs`
- current behavior unknown -> evidence or `loom-debugging`
- implementation change needed -> `loom-tickets` and `loom-ralph`
- evidence weak or risky -> `loom-critique`
- accepted explanation stale -> `loom-wiki`

## Practical Check

When a ticket touches code, ask:

- what does the spec or ticket say should happen
- what does the current implementation actually do
- what executable or observable instrument shows the difference
- what evidence records the observed result
- what critique, if any, should challenge the sufficiency of that evidence
