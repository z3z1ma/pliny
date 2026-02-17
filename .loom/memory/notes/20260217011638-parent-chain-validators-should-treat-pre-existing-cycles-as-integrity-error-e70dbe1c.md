---
id: 20260217011638-parent-chain-validators-should-treat-pre-existing-cycles-as-integrity-error-e70dbe1c
title: Parent-chain validators should treat pre-existing cycles as integrity errors
visibility: shared
status: active
created_at: "2026-02-17T01:16:38Z"
updated_at: "2026-02-17T01:16:38Z"
---

In Loom Ticket update flows, parent-chain traversal should fail explicitly when a pre-existing ancestor cycle is detected, even if the cycle does not yet include the ticket being updated. Silent returns hide graph corruption and weaken integrity guarantees.

Related: [[[[20260217011638-ticket-graph-integrity-1f794a36|ticket graph integrity]]]] [[[[20260217011638-parent-chain-e29c8ec9|parent chain]]]] [[[[20260217011638-explicit-failures-5ddf84cc|explicit failures]]]]
