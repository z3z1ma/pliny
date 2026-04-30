---
id: critique:loom-drive-skill-review
kind: critique
status: final
created_at: 2026-04-28T21:19:44Z
updated_at: 2026-04-28T21:19:44Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: ticket:odpl001
links:
  tickets:
    - ticket:odpl001
  specs:
    - spec:objective-driven-parent-loop
  evidence:
    - evidence:loom-drive-skill-validation
  packets:
    - packet:ralph-ticket-odpl001-20260428T202948Z
external_refs: {}
---

# Summary

Oracle-assisted critique of the `loom-drive` skill after five substantial
improvement passes plus one corrective verification pass. The review targeted
workflow-boundary and protocol-authority risk: whether `loom-drive` can coordinate
chat-initiated objective continuation without becoming a daemon, hidden ledger,
new truth layer, or unsafe autonomy shortcut.

# Review Target

Reviewed files:

- `skills/loom-drive/SKILL.md`
- `skills/loom-drive/references/drive-loop.md`
- `skills/loom-drive/references/continuity-contract.md`
- `skills/loom-drive/references/tranche-decision-protocol.md`
- `skills/loom-drive/references/checkpoint-resume-protocol.md`
- `skills/loom-drive/templates/outer-loop-handoff.md`
- `skills/loom-workspace/references/routing.md`

Reviewed against:

- `spec:objective-driven-parent-loop`
- `ticket:odpl001`
- `evidence:loom-drive-skill-validation`

# Verdict

`pass_with_findings`.

The review found two high-severity design issues during iteration. Both were
resolved before final review. No remaining critical or high-severity findings were
reported by the final Oracle verification pass.

# Findings

## FIND-001: Hard gates could block their own repair routes

Severity: high

Confidence: high

Disposition: resolved

Observation:

The checkpoint/resume protocol initially treated hard gates as preflight blockers
for route federation while also allowing research/spec/plan routes to repair
missing evidence, behavior, or sequencing. That risked a deadlock where the gate
blocked the route needed to clear it.

Why it matters:

`loom-drive` must fail closed without making safe repair impossible. If ambiguity
blocks the spec route that would resolve ambiguity, the parent loop either stalls
or bypasses its own safety model.

Follow-up:

Resolved by splitting gate outcomes into `repair route required` and `execution
blocked`, clarifying that failed gates do not block their own repair routes but do
block implementation, acceptance, and dependent continuation.

Challenges:

- `spec:objective-driven-parent-loop` ACC-006
- `ticket:odpl001` ACC-004

## FIND-002: Checkpoint freshness could be deferred too late

Severity: high

Confidence: high

Disposition: resolved

Observation:

The checkpoint/resume protocol initially allowed the resume gate to pass if
checkpoint fields could be updated before the parent stopped. That left room to
launch child work before the checkpoint was current.

Why it matters:

The whole chat-only model depends on resumability across compaction without a
daemon. Launching child work from stale checkpoint state would undermine the
fresh-agent recovery guarantee.

Follow-up:

Resolved by requiring checkpoint fields to be current before child launch, route
handoff, parent stop, or compaction-sensitive continuation.

Challenges:

- `spec:objective-driven-parent-loop` ACC-005
- `ticket:odpl001` ACC-005

# Evidence Reviewed

- Ralph packet `packet:ralph-ticket-odpl001-20260428T202948Z`
- Validation evidence `evidence:loom-drive-skill-validation`
- Oracle critique pass 1: identified missing concrete persistence of drive state
  and weak claim/coverage traceability.
- Oracle critique pass 2: identified location-less continuity and lack of stable
  objective criterion IDs.
- Oracle critique pass 3: identified missing tranche decision protocol and route
  priority.
- Oracle critique pass 4: identified missing deterministic resume protocol and
  hard gate weaknesses.
- Oracle critique pass 5: identified the two high findings recorded above.
- Oracle verification pass 6: found both high findings resolved and recommended
  formal critique now.
- Final structural checks: `skills/loom-drive/**` file discovery, read-order grep,
  checkpoint/gate grep, forbidden runtime/new-layer grep, and `git diff --check`.

# Residual Risks

- The workflow has not yet been demonstrated in a golden example that starts from
  a vague high-level request and continues through multiple ticket tranches.
- The `outer-loop-handoff` template is intentionally generic; a real first use may
  reveal fields that should be tightened.
- The checkpoint and objective criterion conventions rely on agent discipline in
  owner-record prose rather than automated validation.

# Required Follow-up

No required follow-up blocks this ticket's implementation acceptance.

Recommended follow-up:

- add a golden example for high-level objective -> initiative -> tranche -> Ralph
  -> reconciliation -> next tranche
- consider a future wiki page explaining objective-driven parent loops after the
  first accepted real use

# Acceptance Recommendation

Complete pending acceptance. The ticket has implementation evidence and mandatory
critique with resolved high findings. Final ticket acceptance may still decide
whether to create follow-up work for examples or wiki promotion.
