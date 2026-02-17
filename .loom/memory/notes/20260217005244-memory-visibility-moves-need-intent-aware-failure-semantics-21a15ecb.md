---
id: 20260217005244-memory-visibility-moves-need-intent-aware-failure-semantics-21a15ecb
title: Memory visibility moves need intent-aware failure semantics
visibility: shared
status: active
created_at: "2026-02-17T00:52:44Z"
updated_at: "2026-02-17T00:52:44Z"
---

In [[20260216165029-loom-memory-43f728c2|Loom Memory]], note relocation should encode intent: explicit visibility changes must fail loudly, while implicit reconciliation can degrade with a structured warning payload that includes id/from/to/error context. This keeps [[20260217005244-correctness-78c43e29|Correctness]] strict where users requested change and preserves resilience in background consistency paths.

Related: [[[[20260217005244-memory-edit-754edbf2|memory edit]]]] [[[[20260217005244-visibility-migration-13480cd3|visibility migration]]]] [[[[20260217005244-error-contracts-8c70bded|error contracts]]]]
