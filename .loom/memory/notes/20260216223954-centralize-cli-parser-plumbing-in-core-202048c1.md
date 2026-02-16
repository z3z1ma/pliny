---
id: 20260216223954-centralize-cli-parser-plumbing-in-core-202048c1
title: Centralize CLI parser plumbing in core
visibility: shared
status: active
created_at: "2026-02-16T22:39:54Z"
updated_at: "2026-02-16T22:39:54Z"
---

Prefer shared parser primitives in [[20260216223954-agent-loom-core-cli-args-e1fe729e|agent_loom.core.cli_args]] (ArgParseError, StrictArgumentParser, did_you_mean) instead of per-module duplicates. Also centralize git root fallback via [[20260216223954-agent-loom-core-git-resolve-repo-root-ddf5cf56|agent_loom.core.git.resolve_repo_root]] and precise timestamps via [[20260216223954-agent-loom-core-time-now-iso-precise-0357e57b|agent_loom.core.time.now_iso_precise]] to reduce drift and cross-module inconsistency.
