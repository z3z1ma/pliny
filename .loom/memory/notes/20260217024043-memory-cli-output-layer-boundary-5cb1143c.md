---
id: 20260217024043-memory-cli-output-layer-boundary-5cb1143c
title: Memory CLI output layer boundary
tags:
- architecture
- memory
visibility: shared
status: active
created_at: "2026-02-17T02:40:43Z"
updated_at: "2026-02-17T02:40:43Z"
---

Separated output concerns from runtime in [[20260217015632-memory-cli-52a58d8c|memory-cli]] by introducing `cli_output.py` for payload mapping and text/json rendering. This keeps command execution in `cli_runtime.py` focused on orchestration and option handling, while output formatting is isolated for future command-family extraction. Guardrails now monitor [[20260217020055-parser-hotspots-9afdcc53|parser-hotspots]] and output hotspot growth independently. Related: [[20260217015632-shim-boundaries-7b53ab6a|shim-boundaries]], [[20260216233522-behavior-stable-refactor-ff3ee4c3|behavior-stable-refactor]].
