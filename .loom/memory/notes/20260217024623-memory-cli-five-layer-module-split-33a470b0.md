---
id: 20260217024623-memory-cli-five-layer-module-split-33a470b0
title: Memory CLI five-layer module split
tags:
- architecture
- memory
visibility: shared
status: active
created_at: "2026-02-17T02:46:23Z"
updated_at: "2026-02-17T02:46:23Z"
---

The [[20260217015632-memory-cli-52a58d8c|memory-cli]] architecture now follows a five-layer split: shim (`cli.py`), runtime entrypoint (`cli_runtime.py`), parser (`cli_parser.py`), command handlers (`cli_handlers.py`), and output mapping (`cli_output.py`), plus dedicated edit option staging (`cli_edit_options.py`). This pattern preserves behavior while isolating complexity and making guardrails map directly to true hotspots. Related: [[20260217020055-parser-hotspots-9afdcc53|parser-hotspots]], [[20260217015632-shim-boundaries-7b53ab6a|shim-boundaries]], [[20260216233522-behavior-stable-refactor-ff3ee4c3|behavior-stable-refactor]].
