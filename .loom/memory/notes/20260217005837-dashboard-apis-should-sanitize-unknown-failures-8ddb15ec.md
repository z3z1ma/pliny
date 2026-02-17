---
id: 20260217005837-dashboard-apis-should-sanitize-unknown-failures-8ddb15ec
title: Dashboard APIs should sanitize unknown failures
visibility: shared
status: active
created_at: "2026-02-17T00:58:37Z"
updated_at: "2026-02-17T00:58:42Z"
---


In [[20260216165029-loom-dashboard-a67c52fa|Loom Dashboard]], API boundaries should expose domain-typed errors but sanitize unexpected failures with stable envelopes and  correlation. Request parsing should be strict at the edge ([[20260217005837-json-validation-b4c93f48|JSON validation]], typed field coercion) so client mistakes return deterministic 4xx errors while preserving [[20260217005837-internal-error-hygiene-1fb533fa|internal error hygiene]].

Related: [[[[20260217005837-dashboard-contracts-21aef31e|dashboard contracts]]]] [[[[20260217005837-error-mapping-ed38bdd3|error mapping]]]] [[[[20260217005837-request-parsing-94ae5a0a|request parsing]]]]

Use stable error_id correlation in details for unknown 5xx responses.
