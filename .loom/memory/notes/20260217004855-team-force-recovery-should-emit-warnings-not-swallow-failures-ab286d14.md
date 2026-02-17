---
id: 20260217004855-team-force-recovery-should-emit-warnings-not-swallow-failures-ab286d14
title: Team force-recovery should emit warnings, not swallow failures
visibility: shared
status: active
created_at: "2026-02-17T00:48:55Z"
updated_at: "2026-02-17T00:48:55Z"
---

In [[20260216165029-loom-team-3ac24401|Loom Team]], force-recovery paths like integrator respawn should remain best-effort but must emit structured warnings for each failed cleanup step instead of silent exception swallowing. This improves [[20260216233522-operational-observability-c5bca2be|Operational Observability]] and preserves behavior stability while making diagnostics explicit.

Related: [[[[20260217004855-run-warning-a4918a08|run.warning]]]] [[[[20260217004855-spawn-integrator-5a8ef101|spawn_integrator]]]] [[[[20260217004855-failure-visibility-2471dca2|failure visibility]]]]
