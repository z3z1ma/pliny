---
id: 20260217045337-team-core-model-baseline-f284c305
title: Team core model baseline
tags:
- architecture
- team
visibility: shared
status: active
created_at: "2026-02-17T04:53:37Z"
updated_at: "2026-02-17T04:54:09Z"
---

Team runtime now standardizes on [[20260217045337-manager-cbdf2be7|manager]], [[20260217045337-architect-0acfa0fb|architect]], [[20260217045337-worker-d1eca054|worker]], and [[20260217045337-integrator-13e082bc|integrator]] only. Use [[20260217045337-team-config-560af978|team-config]] as the single run-level config surface (`loom team start --config`) and treat roster/composition personas/routes as removed by design. [[20260217045337-heartbeat-liveness-d1244f5a|heartbeat-liveness]] is the health source of truth (`alive|stale|dead|missing`) with bounded recovery cooldown/caps; window-exists checks are not sufficient for correctness.
