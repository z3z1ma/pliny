---
id: repeat-team-merge-until-queue-state-advances
title: Repeat team merge until queue state advances
trigger: When integrating worker-delivered branches from a Loom team merge queue
confidence: 0.7700
status: active
domain: workflow
source: local
created_at: 2026-02-15T23:51:49.846041Z
updated_at: 2026-02-16T00:46:30.022893Z
tags: workflow, team, merge-queue, integration, orchestration
notes: The command produced successive queue-state views in one run, indicating repeated invocation is required to drive and verify merge-queue progression.
---

## Action
Run `loom team merge <team>` in a short loop during integration handoff and use each response state (`sha`, `[queued]`, claimed record) to confirm queue advancement before taking branch-level merge actions.

## Evidence
- ts=2026-02-15T23:51:20.115053Z source_id=obs-merge-235120 source_hash=loom-team-merge-returned-sha
- ts=2026-02-15T23:51:23.027270Z source_id=obs-merge-235123 source_hash=loom-team-merge-queued-ticket
- ts=2026-02-15T23:51:23.560064Z source_id=obs-merge-235123b source_hash=loom-team-merge-claimed-record
- ts=2026-02-15T23:55:44.636341Z source_id=obs-merge-235544 source_hash=loom-team-merge-done
- ts=2026-02-15T23:55:49.171182Z source_id=obs-merge-235549 source_hash=loom-team-merge-empty-then-no-output
- ts=2026-02-16T00:06:47.697398Z source_id=obs-merge-000647 source_hash=loom-team-merge-enqueued-id
- ts=2026-02-16T00:06:51.820180Z source_id=obs-merge-000651 source_hash=loom-team-merge-claimed-record
- ts=2026-02-16T00:24:21.640176Z source_id=obs-merge-002421 source_hash=loom-team-merge-enqueued-id
- ts=2026-02-16T00:24:23.972528Z source_id=obs-merge-002423 source_hash=loom-team-merge-claimed-record-next-pass
- ts=2026-02-16T00:41:15.281447Z source_id=obs-merge-004115 source_hash=loom-team-merge-enqueued-id
- ts=2026-02-16T00:41:18.518136Z source_id=obs-merge-004118 source_hash=loom-team-merge-claimed-record
- ts=2026-02-16T00:43:21.740485Z source_id=obs-merge-004321 source_hash=loom-team-merge-done
- ts=2026-02-16T00:43:24.108097Z source_id=obs-merge-004324 source_hash=loom-team-merge-empty
- ts=2026-02-16T00:43:28.191914Z source_id=obs-merge-004328 source_hash=loom-team-merge-no-output
- ts=2026-02-16T00:45:59.224440Z source_id=obs-merge-004559 source_hash=loom-team-merge-returned-sha
- ts=2026-02-16T00:46:04.423059Z source_id=obs-merge-004604 source_hash=loom-team-merge-claimed-record

## Notes
The command produced successive queue-state views in one run, indicating repeated invocation is required to drive and verify merge-queue progression.
