---
id: ticket:pbalign8
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-08T04:51:16Z
updated_at: 2026-05-08T05:21:35Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  spec:
    - spec:core-and-playbooks-package-contract
  research:
    - research:peer-playbook-integration-candidates
  ticket:
    - ticket:plybk508
  evidence:
    - evidence:playbook-core-alignment-check
  critique:
    - critique:playbook-core-alignment-review
external_refs: {}
depends_on: []
---

# Summary

Align `loom-playbooks/skills` wording and examples with `loom-core` authority,
status, critique, packet, and owner-layer vocabulary so optional playbooks do not
teach noncanonical Loom grammar.

# Context

Operator review asked whether the core and playbook skill corpora had reached near
full coherence. The review found that the core doctrine is largely coherent, but a
small set of playbook references still leak peer vocabulary or workflow shorthand
that conflicts with core-owned status, critique, finding-disposition, and owner
layer rules.

This follow-up is constrained by `spec:core-and-playbooks-package-contract`,
especially `REQ-004`, `REQ-005`, and `REQ-008`: playbooks are optional workflow
composition over core and must not redefine canonical layers, acceptance,
evidence, critique, ticket state, or packet lifecycle.

# Scope

In:

- Audit `loom-playbooks/skills/**` against core-owned vocabulary and truth
  boundaries.
- Correct high-confidence conflicts in playbook prose and examples.
- Preserve playbook usefulness while mapping shorthand back to core grammar.
- Run structural scans and package smoke checks proportional to the edited surface.

Out:

- Changing playbook membership or package manifests.
- Changing core doctrine, templates, or owner-layer grammar unless a direct
  playbook alignment issue proves core text is wrong.
- Reopening `ticket:plybk508` or reworking the whole peer adaptation.
- Adding scripts, validators, command wrappers, or hidden runtimes.

Assumptions / decision triggers:

| Assumption or question | Reversible? | Blocks execution? | Disposition |
| --- | --- | --- | --- |
| Core vocabulary is the authority for status, critique severity, finding dispositions, packet outcomes, and owner-layer routing. | yes, but costly | no | accepted from using-Loom doctrine and `loom-records` references |
| The requested pass can be satisfied by playbook edits and structural review without changing package membership. | yes | no | accepted unless scans find a membership-level contradiction |

# Acceptance

Owner: ticket-local, constrained by `spec:core-and-playbooks-package-contract`.

Criteria / covered IDs:

- `spec:core-and-playbooks-package-contract#REQ-004`
- `spec:core-and-playbooks-package-contract#REQ-005`
- `spec:core-and-playbooks-package-contract#REQ-008`
- `ticket:pbalign8#ACC-001`
- `ticket:pbalign8#ACC-002`
- `ticket:pbalign8#ACC-003`

Ticket-local criteria, only when no spec owns the reusable contract:

- ACC-001: Playbook critique and code-review guidance uses core critique severity
  and ticket-owned finding disposition vocabulary.
- ACC-002: Playbook orchestration and child-output guidance either uses Ralph
  outcome vocabulary or explicitly frames alternative labels as non-Ralph harness
  transport that must be mapped back before reconciliation.
- ACC-003: Playbook discovery, TDD, and drive guidance routes durable truth to core
  owner layers and does not name workflow skills, bug reports, implementation
  state, or generic gate words as canonical owners or interchangeable statuses.

# Current State

Status rationale:

Closed. The scoped playbook alignment edits landed, structural evidence is
recorded, and critique findings have ticket-owned dispositions.

Blockers:

None.

Execution notes:

- Initial review identified vocabulary conflicts in `loom-code-review`,
  `loom-agent-orchestration`, `loom-product-discovery`, `loom-tdd`, and
  `loom-drive`.
- Existing unrelated untracked files under `examples/00-todo-app/**` are present
  before this ticket's edits and are outside scope.

Continuation note:

Next action: None for this ticket. Future operator-use feedback may create a new
follow-up if softer playbook overlap appears.

# Evidence

Disposition: sufficient

Records:

- evidence:playbook-core-alignment-check — supports `ticket:pbalign8#ACC-001`,
  `ticket:pbalign8#ACC-002`, `ticket:pbalign8#ACC-003`, and the scoped package
  contract requirements.

Gaps / limits:

Smoke checks prove package discovery shape only. Semantic alignment is supported
by targeted text scans and critique, but long-term operator clarity remains
empirical.

# Review And Follow-Through

Critique policy: recommended
Critique rationale: This changes optional skill guidance that affects future
operator routing, review, and closure vocabulary, but it aligns playbooks to
existing core doctrine instead of changing core authority.
Critique disposition: completed

Required critique profiles:

- protocol-change
- operator-clarity

Findings:

- critique:playbook-core-alignment-review#FIND-001 — resolved by changing ship
  guidance to require current owner records for drive preflight gates and framing
  support checkpoints as locate/summarize aids only.
- critique:playbook-core-alignment-review#FIND-002 — resolved by expanding
  `evidence:playbook-core-alignment-check` with exact targeted grep patterns,
  result counts, and intentional remaining-match explanations.

Promotion disposition: not_required
Promotion / deferral rationale: Durable learning is embodied in the edited
playbook guidance, the evidence record, and the critique. No separate wiki,
research, spec, plan, or constitution update is needed for this scoped alignment
pass.

Promoted / deferred:

- None - no separate promotion artifact needed.

Wiki disposition: not_required - no accepted explanation page is needed beyond the
playbook source updates.

# Acceptance Decision

Required before closure when acceptance, accepted risk, or operator provenance
needs to be explicit.

Accepted by: OpenCode agent on operator request
Accepted at: 2026-05-08T05:21:35Z
Basis: Accepted because the scoped playbook prose now uses core critique severity
and ticket-owned finding disposition vocabulary, Ralph child outcomes or explicit
non-Ralph transport mapping, owner-layer routing for spike/codemap/ship/drive and
support checkpoints, and source-vs-intended-behavior boundaries; the empty orphan
`loom-verification` directory was removed; `npm run pack:check` passed for
`loom-playbooks`; `npm run smoke` passed for `loom-core`; scoped `git diff --check`
passed; targeted scans found no active noncanonical guidance beyond deliberate
warning examples; and `critique:playbook-core-alignment-review` has no remaining
blocker after ticket-owned finding dispositions.
Residual risks: Long-term operator clarity is empirical, and targeted scans may
miss future semantic drift that uses different wording.

# Dependencies

No hard upstream ticket prerequisites. This work follows `ticket:plybk508` as a
coherence follow-up and is constrained by the package contract spec.

# Journal

- 2026-05-08T04:51:16Z: Created active ticket for the playbook/core alignment
  sweep after operator review found remaining vocabulary drift in optional
  playbooks.
- 2026-05-08T05:21:35Z: Patched playbook vocabulary and owner-boundary drift,
  removed the empty orphan `loom-verification` directory, recorded structural
  evidence, completed critique, dispositioned both critique findings as resolved,
  reran final playbook pack validation, and accepted/closed the ticket.
