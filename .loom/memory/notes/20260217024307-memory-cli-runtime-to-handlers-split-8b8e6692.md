---
id: 20260217024307-memory-cli-runtime-to-handlers-split-8b8e6692
title: Memory CLI runtime-to-handlers split
tags:
- architecture
- memory
visibility: shared
status: active
created_at: "2026-02-17T02:43:07Z"
updated_at: "2026-02-17T02:43:07Z"
---

Advanced [[20260217015632-memory-cli-52a58d8c|memory-cli]] decomposition by isolating execution handlers into `cli_handlers.py` and keeping `cli_runtime.py` as an entry boundary only (parse + error mapping + delegation). This makes it easier to split handler families without touching the runtime error contract and keeps architecture guardrails aligned with the true dispatch hotspot. Related: [[20260217020055-parser-hotspots-9afdcc53|parser-hotspots]], [[20260217015632-shim-boundaries-7b53ab6a|shim-boundaries]], [[20260216233522-behavior-stable-refactor-ff3ee4c3|behavior-stable-refactor]].
