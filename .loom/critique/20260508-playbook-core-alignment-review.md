---
id: critique:playbook-core-alignment-review
kind: critique
status: final
created_at: 2026-05-08T05:19:50Z
updated_at: 2026-05-08T05:19:50Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: "ticket:pbalign8 playbook/core alignment diff"
links:
  ticket:
    - ticket:pbalign8
  evidence:
    - evidence:playbook-core-alignment-check
  spec:
    - spec:core-and-playbooks-package-contract
external_refs: {}
---

# Summary

Reviewed the `ticket:pbalign8` playbook alignment diff for consistency with core
Loom vocabulary and truth boundaries.

# Review Target

Target: the current working-tree diff affecting `loom-playbooks/skills/**`,
`.loom/tickets/20260508-pbalign8-align-playbooks-with-core.md`, and
`.loom/evidence/20260508-playbook-core-alignment-check.md`.

The review checked whether playbook guidance still contradicted core rules around
owner layers, ticket-owned live state and acceptance, critique severity and
finding dispositions, Ralph child outcomes, evidence ownership, support artifacts,
and workflow-vs-owner boundaries.

# Verdict

`pass_with_findings`

The alignment diff corrected the originally identified high-confidence playbook
drift and subsequent review findings were addressed. The remaining risks are
soft operator-clarity risks rather than closure blockers, provided the ticket
records finding dispositions.

# Findings

## FIND-001: Support checkpoints must not clear ship gates

Severity: medium
Confidence: medium-high
State: open

Observation:

An intermediate diff in `loom-ship` allowed drive hard preflight gates to be
satisfied from "owner records or support checkpoint facts." That phrasing could
teach operators that support checkpoints clear packaging or ship gates.

Why it matters:

Core doctrine treats support artifacts and checkpoint facts as recovery or
transport surfaces, not owners of objective state, live ticket state, acceptance,
evidence sufficiency, critique verdicts, wiki truth, canonical truth, or packet
lifecycle.

Follow-up:

Resolved in the current diff by `loom-playbooks/skills/loom-ship/SKILL.md:83-85`
and `loom-playbooks/skills/loom-ship/references/handoff-options.md:23-27`, which
now say current owner records clear gates and support checkpoints only locate or
summarize those facts.

Challenges: ticket:pbalign8#ACC-003

## FIND-002: Evidence scan summary needed exact scan detail

Severity: low
Confidence: medium
State: open

Observation:

The first evidence record summary said the targeted scan returned only intentional
`loom-code-review` warning examples, while the actual scan also intentionally
mentioned `done_with_concerns` and `needs_context` as non-Ralph transport labels.

Why it matters:

Evidence should preserve enough concrete procedure detail for a future reviewer to
judge the observation without trusting a compressed summary.

Follow-up:

Resolved in `evidence:playbook-core-alignment-check` by embedding exact targeted
grep patterns, result counts, and the remaining intentional match explanations in
the `# Artifacts` and `# Supports Claims` sections.

Challenges: ticket:pbalign8#ACC-001, ticket:pbalign8#ACC-002

# Evidence Reviewed

- Current working-tree diff for `loom-playbooks/skills/**`.
- `evidence:playbook-core-alignment-check`.
- `ticket:pbalign8`.
- Core references for truth boundaries, packet outcomes, critique/finding
  vocabulary, ticket acceptance, support artifacts, and status lifecycle.
- Package and structural validation summarized in `evidence:playbook-core-alignment-check`.
- Focused post-fix rechecks that found `FIND-001` resolved and then `FIND-002`
  resolved after evidence detail was expanded.

# Residual Risks

- Long-term operator clarity remains empirical; future use may expose softer
  overlap between specialist playbooks and core routes.
- Targeted scans can miss semantic drift that uses different wording.
- The diff aligns playbook prose; it does not validate every possible future
  operator interpretation.

# Required Follow-up

Ticket `ticket:pbalign8` should record `FIND-001` and `FIND-002` as resolved with
the patch and evidence-update basis before closure.

# Acceptance Recommendation

`no-critique-blockers` — after ticket-owned finding dispositions are recorded,
the critique sees no remaining blocker to accepting this alignment pass.
