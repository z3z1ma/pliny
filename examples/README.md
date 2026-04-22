# Loom Protocol Examples

These examples are golden protocol fixtures and traces.

They exist so contributors can judge whether a Loom change preserves the
intended route through owner layers.

They are not automated tests and not canonical project truth.

Each example names:

- starting `.loom` slice
- operator request
- expected route
- expected artifacts
- expected final state
- common wrong behavior

Each example should include:

```text
before/
operator-request.md
expected-route.md
after/
common-wrong-behavior.md
```

Examples are outside the core product source. They may demonstrate the product,
but they do not define Loom truth. Keep them minimal but conformant because
agents learn protocol shape from examples.
