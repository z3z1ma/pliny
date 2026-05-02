---
id: evidence:critique-recommendation-vocabulary-validation
kind: evidence
status: recorded
created_at: 2026-05-02T23:30:27Z
updated_at: 2026-05-02T23:35:41Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:critrec9
  packet:
    - packet:ralph-ticket-critrec9-20260502T232902Z
external_refs: {}
---

# Summary

Observed before/after critique recommendation vocabulary searches for
`ticket:critrec9`, plus `git diff --check`.

# Procedure

Timestamp: 2026-05-02T23:30Z. Parent reconciliation recheck timestamp:
2026-05-02T23:34Z.

Commands run from repository root:

```bash
rg -n 'close-ready' 'skills/loom-critique' || true
rg -n 'Acceptance Recommendation|acceptance recommendation|complete pending acceptance|active follow-up required|accepted risk needed|close-ready' 'skills/loom-critique' || true
rg -n 'close-ready|complete pending acceptance|review required|active follow-up required|blocked|accepted risk needed' 'skills/loom-critique' || true
rg -n '\b(ralph|critique|wiki|research|spec|plan|ticket|evidence|route|review_required|complete_pending_acceptance|active|blocked|closed)\b' 'skills/loom-critique' || true
rg -n 'recommendation|status|state|State:|ticket state|route|closure|close|acceptance' 'skills/loom-critique' || true
git diff --check
```

# Artifacts

## Before observation

`close-ready` search output:

```text
skills/loom-critique/templates/critique.md:91:Use a concrete recommendation: close-ready, complete pending acceptance,
```

Acceptance recommendation wording search output:

```text
skills/loom-critique/templates/critique.md:38:acceptance recommendation are complete enough for the ticket to consume. Final
skills/loom-critique/templates/critique.md:89:# Acceptance Recommendation
skills/loom-critique/templates/critique.md:91:Use a concrete recommendation: close-ready, complete pending acceptance,
skills/loom-critique/templates/critique.md:92:review required, active follow-up required, blocked, or accepted risk needed.
```

Ticket-state-looking recommendation label search output:

```text
skills/loom-critique/templates/critique-packet.md:164:Stop or return `blocked` if the declared `review_target`, source fingerprint,
skills/loom-critique/templates/critique.md:91:Use a concrete recommendation: close-ready, complete pending acceptance,
skills/loom-critique/templates/critique.md:92:review required, active follow-up required, blocked, or accepted risk needed.
```

Route-token search output was intentionally broad. Relevant risky hits were the
same `skills/loom-critique/templates/critique.md:91-94` acceptance
recommendation lines because `review required`, `blocked`, and close/acceptance
wording appeared in recommendation prose. Other broad hits were ordinary critique
packet, skill, and reference guidance such as `ticket:<token>`, `evidence`,
`critique`, and packet stop-condition wording.

Recommendation/status wording search output included the same risky template
lines plus already-correct owner-boundary wording, including:

```text
skills/loom-critique/templates/critique.md:37:Set `status: final` only when evidence reviewed, findings, residual risks, and
skills/loom-critique/templates/critique.md:39:critique status does not close the ticket.
skills/loom-critique/templates/critique.md:91:Use a concrete recommendation: close-ready, complete pending acceptance,
skills/loom-critique/templates/critique.md:93:This recommendation informs the ticket-owned acceptance decision; it does not
skills/loom-critique/templates/critique.md:94:close the ticket by itself.
skills/loom-critique/references/finding-format.md:35:Critique records produce findings, verdicts, residual risks, and follow-up
skills/loom-critique/references/finding-format.md:36:recommendations. They do not close ticket work and do not accept their own
```

## After observation

`close-ready` search output:

```text
(no output)
```

Acceptance recommendation wording search output:

```text
skills/loom-critique/templates/critique.md:38:acceptance recommendation are complete enough for the ticket to consume. Final
skills/loom-critique/templates/critique.md:89:# Acceptance Recommendation
```

Ticket-state-looking recommendation label search output:

```text
skills/loom-critique/templates/critique-packet.md:164:Stop or return `blocked` if the declared `review_target`, source fingerprint,
```

The remaining `blocked` hit is a critique-packet stop condition outside this
ticket's recommendation-label target. It is not an acceptance recommendation and
was outside the child write scope.

Route-token search output remained broad because `skills/loom-critique` normally
mentions `critique`, `ticket:<token>`, `evidence`, and packet routing context.
The changed critique record template now states the recommendation labels are not
route tokens or ticket states:

```text
skills/loom-critique/templates/critique.md:91:Use one concrete non-canonical critique recommendation label:
skills/loom-critique/templates/critique.md:106:These labels are recommendation vocabulary only. They are not ticket states,
skills/loom-critique/templates/critique.md:107:route tokens, finding dispositions, or closure decisions. If a recommendation
skills/loom-critique/templates/critique.md:108:explicitly names a real ticket state or route token, quote it as the ticket-owned
skills/loom-critique/templates/critique.md:109:next action and state that critique does not apply it. This recommendation
skills/loom-critique/templates/critique.md:110:informs the ticket-owned acceptance decision; it does not mutate ticket state or
skills/loom-critique/templates/critique.md:111:close the ticket by itself.
```

Recommendation/status wording search output showed the new non-canonical label
set and reference boundary guidance:

```text
skills/loom-critique/templates/critique.md:91:Use one concrete non-canonical critique recommendation label:
skills/loom-critique/templates/critique.md:93:- `no-critique-blockers` — critique sees no required follow-up before the
skills/loom-critique/templates/critique.md:95:- `ticket-acceptance-review-needed` — the ticket's acceptance gate still needs
skills/loom-critique/templates/critique.md:97:- `follow-up-needed-before-acceptance` — follow-up is needed before ticket-owned
skills/loom-critique/templates/critique.md:101:- `risk-disposition-needed` — critique observed a risk that needs ticket-owned
skills/loom-critique/templates/critique.md:103:- `evidence-insufficient` — the reviewed evidence is not enough to support the
skills/loom-critique/references/finding-format.md:39:Acceptance recommendation labels in critique records are non-canonical advice for
skills/loom-critique/references/finding-format.md:40:the ticket's acceptance gate. They are not ticket lifecycle states, route tokens,
skills/loom-critique/references/finding-format.md:42:ticket state or route token, quote it as the ticket-owned next action and state
```

`git diff --check` output:

```text
(no output)
```

# Supports Claims

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-009`
- `ticket:critrec9#ACC-001`
- `ticket:critrec9#ACC-002`
- `ticket:critrec9#ACC-003`
- `ticket:critrec9#ACC-004`

# Challenges Claims

None - no observed output challenged the scoped vocabulary-cleanup claims. The
pending oracle critique may still challenge the implementation or evidence.

# Environment

Commit: `cac7c7c2446eebe17127346f059c93cc580986b8` plus uncommitted
`ticket:critrec9` working-tree changes.
Branch: `main`
Runtime: Markdown corpus and Git structural validation.
OS: darwin
Relevant config: none observed.

# Validity

Valid for: the `ticket:critrec9` working-tree changes to critique recommendation
vocabulary and related Loom records.
Fresh enough for: parent reconciliation and mandatory critique input before any
later edit to the changed files.
Recheck when: `skills/loom-critique` recommendation wording, the evidence record,
the ticket, or this packet changes before closure.
Invalidated by: new legacy recommendation/state wording, failed `git diff
--check`, or critique findings that challenge the evidence.
Supersedes / superseded by: none.

# Limitations

- The broad route-token search intentionally returns legitimate critique skill and
  packet terminology outside the recommendation-label target.
- This evidence does not provide the mandatory oracle critique verdict.
- This evidence does not validate the full skills corpus or close the ticket.

# Result

The observed after-state removed `close-ready` and legacy ticket-state-looking
acceptance recommendation prose from the critique record template, added explicit
non-canonical recommendation-label guidance, added matching owner-boundary wording
to the finding-format reference, and passed `git diff --check`.

# Interpretation

The before state included copyable acceptance recommendation labels that looked
like ticket states or closure guidance. The after state replaces them with a
non-canonical critique recommendation label set and explicit ticket-ownership
guardrails. Critique recommendations remain present and inform ticket-owned
acceptance without mutating ticket state or closing work.

# Related Records

- `ticket:critrec9`
- `packet:ralph-ticket-critrec9-20260502T232902Z`
- `plan:skills-corpus-template-grammar-safety-pass`
- `initiative:skills-corpus-template-grammar-safety-pass`
