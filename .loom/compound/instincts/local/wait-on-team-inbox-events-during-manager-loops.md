---
id: wait-on-team-inbox-events-during-manager-loops
title: Wait on team inbox events during manager loops
trigger: When managing active team runs and expecting asynchronous worker responses
confidence: 0.7900
status: active
domain: workflow
source: local
created_at: 2026-02-15T23:49:19.074072Z
updated_at: 2026-02-16T00:46:30.022893Z
tags: workflow, team, wait, orchestration, efficiency
notes: This reduces busy polling while still keeping manager response latency low after worker updates arrive.
---

## Action
Use `loom team wait <team>` to block for inbox activity, then immediately inspect `loom team inbox <team>` to process and acknowledge resulting messages.

## Evidence
- ts=2026-02-15T23:42:58.315960Z source_id=obs-team-wait-234258 source_hash=loom-team-wait-awake
- ts=2026-02-15T23:48:36.538550Z source_id=obs-team-wait-234836 source_hash=loom-team-wait-awake
- ts=2026-02-15T23:55:45.180603Z source_id=obs-team-wait-235545 source_hash=loom-team-wait-awake-manager
- ts=2026-02-16T00:01:04.383373Z source_id=obs-team-wait-000104 source_hash=loom-team-wait-awake-manager-round2
- ts=2026-02-16T00:05:51.927466Z source_id=obs-team-wait-000551 source_hash=loom-team-wait-awake-integrator
- ts=2026-02-16T00:24:12.377363Z source_id=obs-team-wait-002412 source_hash=loom-team-wait-awake-manager
- ts=2026-02-16T00:24:23.775718Z source_id=obs-team-wait-002423 source_hash=loom-team-wait-before-merge-check
- ts=2026-02-16T00:38:54.953734Z source_id=obs-team-wait-003854 source_hash=loom-team-wait-awake-manager-yaml-sprint
- ts=2026-02-16T00:41:03.246260Z source_id=obs-team-wait-004103 source_hash=loom-team-wait-awake-manager-ready-check
- ts=2026-02-16T00:43:22.281037Z source_id=obs-team-wait-004322 source_hash=loom-team-wait-awake-followed-by-inbox
- ts=2026-02-16T00:45:51.835447Z source_id=obs-team-wait-004551 source_hash=loom-team-wait-miyagido-awake-manager
- ts=2026-02-16T00:45:59.628527Z source_id=obs-team-wait-004559 source_hash=loom-team-wait-10m-awake-integrator
- ts=2026-02-16T00:46:02.558198Z source_id=obs-team-wait-004602 source_hash=loom-team-wait-miyagido-post-merge

## Notes
This reduces busy polling while still keeping manager response latency low after worker updates arrive.
