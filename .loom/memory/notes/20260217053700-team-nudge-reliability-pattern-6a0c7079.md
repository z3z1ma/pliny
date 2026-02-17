---
id: 20260217053700-team-nudge-reliability-pattern-6a0c7079
title: Team nudge reliability pattern
tags:
- reliability
- team
- tmux
visibility: shared
status: active
created_at: "2026-02-17T05:37:00Z"
updated_at: "2026-02-17T05:37:08Z"
---

Use [[20260217045337-heartbeat-liveness-d1244f5a|heartbeat-liveness]] for health and treat tmux nudge as best-effort transport. For interactive TUIs, reduce no-op behavior by combining [[20260217053700-busy-aware-d195f5bb|busy-aware]] defer logic with post-send activity confirmation and retry/backoff keyed by unacked inbox message id. Keep this logic isolated from core orchestration (for example in a dedicated sidecar nudge module) so core orchestration files stay under architecture guardrails.
