---
id: poll-team-inbox-for-acks-and-status
title: Poll team inbox for acknowledgements and worker status
trigger: While managing an active team run with asynchronous worker updates
confidence: 0.8600
status: active
domain: workflow
source: local
created_at: 2026-02-15T23:40:44.698691Z
updated_at: 2026-02-16T00:46:30.022893Z
tags: workflow, team, inbox, orchestration, acknowledgements
notes: Observed across multiple ack cycles for different recipients, confirming this is durable orchestration behavior.
---

## Action
Use `loom team inbox <team>` repeatedly during active coordination loops to collect worker updates, verify ack transitions, and drive follow-up actions from observed status rather than assumptions.

## Evidence
- ts=2026-02-15T23:47:31.559884Z source_id=obs-inbox-234731 source_hash=loom-team-inbox-miyagido-unack-w2
- ts=2026-02-15T23:47:33.805581Z source_id=obs-inbox-234733 source_hash=loom-team-inbox-miyagido-ack-w2
- ts=2026-02-15T23:47:54.462103Z source_id=obs-inbox-234754 source_hash=loom-team-inbox-miyagido-unack-manager
- ts=2026-02-15T23:47:57.139136Z source_id=obs-inbox-234757 source_hash=loom-team-inbox-miyagido-ack-manager
- ts=2026-02-15T23:48:32.969803Z source_id=obs-inbox-234832 source_hash=loom-team-inbox-miyagido-unack-w2-round2
- ts=2026-02-15T23:48:35.738466Z source_id=obs-inbox-234835 source_hash=loom-team-inbox-miyagido-ack-w2-round2
- ts=2026-02-15T23:51:08.311306Z source_id=obs-inbox-235108 source_hash=loom-team-inbox-miyagido-unack-ready-for-review
- ts=2026-02-15T23:51:12.409203Z source_id=obs-inbox-235112 source_hash=loom-team-inbox-miyagido-acked-ready-for-review
- ts=2026-02-15T23:55:49.329065Z source_id=obs-inbox-235549 source_hash=loom-team-inbox-merge-unack-detail
- ts=2026-02-15T23:55:52.819040Z source_id=obs-inbox-235552 source_hash=loom-team-inbox-ack-merge-message
- ts=2026-02-16T00:01:10.655931Z source_id=obs-inbox-000110 source_hash=loom-team-inbox-unack-send-w3
- ts=2026-02-16T00:06:44.968497Z source_id=obs-inbox-000644 source_hash=loom-team-inbox-ack-ready-for-review
- ts=2026-02-16T00:40:56.134261Z source_id=obs-inbox-004056 source_hash=loom-team-inbox-unack-manager-followup
- ts=2026-02-16T00:41:00.134342Z source_id=obs-inbox-004100 source_hash=loom-team-inbox-ack-worker-followup
- ts=2026-02-16T00:41:10.853288Z source_id=obs-inbox-004110 source_hash=loom-team-inbox-ack-manager-status
- ts=2026-02-16T00:43:27.378769Z source_id=obs-inbox-004327 source_hash=loom-team-inbox-unack-merge-manager
- ts=2026-02-16T00:43:31.765702Z source_id=obs-inbox-004331 source_hash=loom-team-inbox-merge-acked-detail
- ts=2026-02-16T00:43:32.140397Z source_id=obs-inbox-004332 source_hash=loom-team-inbox-sidecar-acked-detail
- ts=2026-02-16T00:45:23.062375Z source_id=obs-inbox-004523 source_hash=loom-team-inbox-unack-send-to-w6
- ts=2026-02-16T00:45:25.790308Z source_id=obs-inbox-004525 source_hash=loom-team-inbox-ack-send-to-w6
- ts=2026-02-16T00:45:53.359239Z source_id=obs-inbox-004553 source_hash=loom-team-inbox-unack-ready-for-review
- ts=2026-02-16T00:45:56.266812Z source_id=obs-inbox-004556 source_hash=loom-team-inbox-ack-ready-for-review

## Notes
Observed across multiple ack cycles for different recipients, confirming this is durable orchestration behavior.
