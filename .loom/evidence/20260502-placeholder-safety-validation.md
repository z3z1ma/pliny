---
id: evidence:placeholder-safety-validation
kind: evidence
status: recorded
created_at: 2026-05-02T23:22:58Z
updated_at: 2026-05-02T23:27:33Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:phsafe8
  packet:
    - packet:ralph-ticket-phsafe8-20260502T232054Z
  critique:
    - critique:placeholder-safety-review
external_refs: {}
---

# Summary

Observed before/after placeholder and authoritative-status searches for the
`ticket:phsafe8` placeholder safety iteration, plus `git diff --check`.

# Procedure

Timestamp: 2026-05-02T23:22Z.

Commands run from repository root:

```bash
rg -n 'TBD' 'skills' --glob '**/templates/*.md' --glob '**/references/*.md'
rg -n 'Replace with' 'skills' --glob '**/templates/*.md' --glob '**/references/*.md'
rg -n 'status: (accepted|final|completed|recorded|active)' 'skills' --glob '**/templates/*.md' --glob '**/references/*.md'
rg -n -C 2 'status: (accepted|final|completed|recorded|active)' 'skills' --glob '**/templates/*.md' --glob '**/references/*.md'
git diff --check
```

# Artifacts

## Before observation

Before `TBD` search found one bare unsafe copyable placeholder and many explicit
fail-closed placeholders:

```text
skills/loom-bootstrap/references/06-filesystem-and-tooling.md:82:TBD
skills/loom-drive/templates/outer-loop-handoff.md:22:  gate_status: "<TBD: choose clear or blocked before saving>"
skills/loom-drive/templates/outer-loop-handoff.md:25:    - "<TBD: proposal-time record write refs, or None - no writes>"
skills/loom-drive/templates/outer-loop-handoff.md:27:    - "<TBD: proposal-time paths, or None - no writes>"
skills/loom-tickets/templates/ticket.md:5:change_class: "<TBD: choose one change class before saving>"
skills/loom-tickets/templates/ticket.md:6:risk_class: "<TBD: choose low, medium, or high before saving>"
skills/loom-tickets/templates/ticket.md:57:- ACC-001: <TBD: write the first ticket-local acceptance criterion>
skills/loom-tickets/templates/ticket.md:58:- ACC-002: <TBD: write the second ticket-local acceptance criterion, or remove>
skills/loom-tickets/templates/ticket.md:89:Next route: <TBD: choose one route token before saving>
skills/loom-tickets/templates/ticket.md:147:Risk class: <TBD: repeat frontmatter risk_class>
skills/loom-tickets/templates/ticket.md:154:Critique policy: <TBD: choose optional, recommended, or mandatory>
skills/loom-tickets/templates/ticket.md:182:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-tickets/templates/ticket.md:197:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-plans/references/plan-shape.md:39:- no placeholders: no `TBD`, `TODO`, vague "handle edge cases", or
skills/loom-critique/templates/critique-packet.md:6:target: "<TBD: ticket:<token>, record ref, review target slug, diff handle, or external summary ID>"
skills/loom-critique/templates/critique-packet.md:8:  kind: "<TBD: choose record, code_change, pull_request, branch, commit, diff, external_summary, release_package, or handoff_package>"
skills/loom-critique/templates/critique-packet.md:10:  ref: "<TBD: record ref, path, branch, commit, PR, package ID, or none>"
skills/loom-critique/templates/critique-packet.md:11:  diff: "<TBD: branch, commit range, PR, diff target, or none>"
skills/loom-critique/templates/critique-packet.md:13:    - "<TBD: changed paths under review, or None - no path-specific target>"
skills/loom-critique/templates/critique-packet.md:15:change_class: "<TBD: choose one change class before saving>"
skills/loom-critique/templates/critique-packet.md:17:# risk_class: "<TBD: choose low, medium, or high before saving>"
skills/loom-critique/templates/critique-packet.md:27:    - "<TBD: critique child write refs, or None - reviewer returns output only>"
skills/loom-critique/templates/critique-packet.md:29:    - "<TBD: critique child write paths, or None - reviewer returns output only>"
skills/loom-critique/templates/critique-packet.md:33:    - "<TBD: ticket:<token> when a ticket owns execution, owner record ref, or None - no parent record reconciliation needed>"
skills/loom-critique/templates/critique-packet.md:36:    - "<TBD: .loom/critique/<slug>.md, other owner path, or None - no parent path reconciliation needed>"
skills/loom-critique/templates/critique.md:48:Severity: <TBD: choose low, medium, or high>
skills/loom-critique/templates/critique.md:49:Confidence: <TBD: choose low, medium, or high>
skills/loom-critique/templates/critique.md:50:State: <TBD: choose open or withdrawn>
skills/loom-wiki/templates/wiki-packet.md:6:target: "<TBD: wiki:<slug>, source record ref, ticket:<token>, or synthesis target slug>"
skills/loom-wiki/templates/wiki-packet.md:19:    - "<TBD: wiki page paths the child may modify, or None - rationale>"
skills/loom-wiki/templates/wiki-packet.md:23:    - "<TBD: ticket:<token> when a ticket owns follow-through, originating owner ref, or None - no additional parent record reconciliation needed>"
skills/loom-wiki/templates/wiki-packet.md:26:    - "<TBD: .loom/wiki/<slug>.md, other owner path, or None - no parent path reconciliation needed>"
skills/loom-specs/templates/spec.md:35:- REQ-001: <TBD: write the first stable requirement before saving>
skills/loom-specs/templates/spec.md:45:- ACC-001: <TBD: write the first acceptance criterion before saving>
skills/loom-ralph/templates/ralph-packet.md:8:change_class: "<TBD: choose one change class before saving>"
skills/loom-ralph/templates/ralph-packet.md:10:# risk_class: "<TBD: choose low, medium, or high before saving>"
skills/loom-ralph/templates/ralph-packet.md:11:style: "<TBD: choose reference-first, snapshot-first, or hermetic before saving>"
skills/loom-ralph/templates/ralph-packet.md:12:verification_posture: "<TBD: choose test-first, observation-first, or none before saving>"
skills/loom-ralph/templates/ralph-packet.md:13:iteration: "<TBD: positive integer>"
skills/loom-ralph/templates/ralph-packet.md:22:    - "<TBD: record refs the child may modify, or None - rationale>"
skills/loom-ralph/templates/ralph-packet.md:24:    - "<TBD: paths or globs the child may modify, or None - rationale>"
skills/loom-ralph/templates/ralph-packet.md:29:    - "<TBD: paths the parent must reconcile, or None - rationale>"
```

Before `Replace with` search found one unsafe plain placeholder:

```text
skills/loom-initiatives/templates/initiative.md:55:- OBJ-001: Replace with one durable objective criterion.
```

Before authoritative-status search found these relevant copyable/default or
instructional occurrences:

```text
skills/loom-bootstrap/references/06-filesystem-and-tooling.md:70:status: active
skills/loom-critique/templates/critique.md:37:Set `status: final` only when evidence reviewed, findings, residual risks, and
skills/loom-memory/templates/entities.md:7:key facts | status: active | last: YYYY-MM-DD | -> [[related-page-or-record]]
skills/loom-initiatives/templates/initiative.md:4:status: active
skills/loom-initiatives/templates/initiative.md:82:When `status: completed`, explain which success metrics were met and what
skills/loom-evidence/templates/evidence.md:4:status: recorded
skills/loom-initiatives/references/initiative-shape.md:21:- Completion Basis when `status: completed`
skills/loom-wiki/templates/index.md:5:status: accepted
skills/loom-workspace/templates/harness.md:4:status: active
skills/loom-plans/templates/plan.md:4:status: active
skills/loom-plans/templates/plan.md:114:When `status: completed`, explain which exit criteria were met and where any
skills/loom-constitution/templates/constitution.md:4:status: active
skills/loom-plans/references/plan-shape.md:17:- Completion Basis when `status: completed`
skills/loom-research/templates/research.md:4:status: active
skills/loom-constitution/templates/roadmap.md:4:status: active
skills/loom-constitution/templates/roadmap.md:43:When `status: completed`, explain which milestones were reached and what
skills/loom-workspace/templates/workspace.md:4:status: active
skills/loom-constitution/templates/decision.md:4:status: active
```

Judgment from before-state review:

- Unsafe and changed: wiki index `status: accepted` over placeholder navigation
  lists; bootstrap here-doc bare `TBD`; initiative success metric `Replace with`
  placeholder.
- Safe to leave unchanged: explicit `<TBD: ... before saving>` placeholders;
  lifecycle-status examples that explain when to use `completed` or `final`;
  support-local memory status example; and allowed initial statuses for record
  kinds where replacing with `draft` would be invalid or less truthful.

## After observation

After `TBD` search shows no bare `TBD`; remaining matches are explicit fail-closed
placeholders or the plan-shape rule naming the forbidden token:

```text
skills/loom-ralph/templates/ralph-packet.md:8:change_class: "<TBD: choose one change class before saving>"
skills/loom-ralph/templates/ralph-packet.md:10:# risk_class: "<TBD: choose low, medium, or high before saving>"
skills/loom-ralph/templates/ralph-packet.md:11:style: "<TBD: choose reference-first, snapshot-first, or hermetic before saving>"
skills/loom-ralph/templates/ralph-packet.md:12:verification_posture: "<TBD: choose test-first, observation-first, or none before saving>"
skills/loom-ralph/templates/ralph-packet.md:13:iteration: "<TBD: positive integer>"
skills/loom-ralph/templates/ralph-packet.md:22:    - "<TBD: record refs the child may modify, or None - rationale>"
skills/loom-ralph/templates/ralph-packet.md:24:    - "<TBD: paths or globs the child may modify, or None - rationale>"
skills/loom-ralph/templates/ralph-packet.md:29:    - "<TBD: paths the parent must reconcile, or None - rationale>"
skills/loom-drive/templates/outer-loop-handoff.md:22:  gate_status: "<TBD: choose clear or blocked before saving>"
skills/loom-drive/templates/outer-loop-handoff.md:25:    - "<TBD: proposal-time record write refs, or None - no writes>"
skills/loom-drive/templates/outer-loop-handoff.md:27:    - "<TBD: proposal-time paths, or None - no writes>"
skills/loom-critique/templates/critique-packet.md:6:target: "<TBD: ticket:<token>, record ref, review target slug, diff handle, or external summary ID>"
skills/loom-critique/templates/critique-packet.md:8:  kind: "<TBD: choose record, code_change, pull_request, branch, commit, diff, external_summary, release_package, or handoff_package>"
skills/loom-critique/templates/critique-packet.md:10:  ref: "<TBD: record ref, path, branch, commit, PR, package ID, or none>"
skills/loom-critique/templates/critique-packet.md:11:  diff: "<TBD: branch, commit range, PR, diff target, or none>"
skills/loom-critique/templates/critique-packet.md:13:    - "<TBD: changed paths under review, or None - no path-specific target>"
skills/loom-critique/templates/critique-packet.md:15:change_class: "<TBD: choose one change class before saving>"
skills/loom-critique/templates/critique-packet.md:17:# risk_class: "<TBD: choose low, medium, or high before saving>"
skills/loom-critique/templates/critique-packet.md:27:    - "<TBD: critique child write refs, or None - reviewer returns output only>"
skills/loom-critique/templates/critique-packet.md:29:    - "<TBD: critique child write paths, or None - reviewer returns output only>"
skills/loom-critique/templates/critique-packet.md:33:    - "<TBD: ticket:<token> when a ticket owns execution, owner record ref, or None - no parent record reconciliation needed>"
skills/loom-critique/templates/critique-packet.md:36:    - "<TBD: .loom/critique/<slug>.md, other owner path, or None - no parent path reconciliation needed>"
skills/loom-plans/references/plan-shape.md:39:- no placeholders: no `TBD`, `TODO`, vague "handle edge cases", or
skills/loom-critique/templates/critique.md:48:Severity: <TBD: choose low, medium, or high>
skills/loom-critique/templates/critique.md:49:Confidence: <TBD: choose low, medium, or high>
skills/loom-critique/templates/critique.md:50:State: <TBD: choose open or withdrawn>
skills/loom-bootstrap/references/06-filesystem-and-tooling.md:86:<TBD: write the research question before saving>
skills/loom-specs/templates/spec.md:35:- REQ-001: <TBD: write the first stable requirement before saving>
skills/loom-specs/templates/spec.md:45:- ACC-001: <TBD: write the first acceptance criterion before saving>
skills/loom-wiki/templates/wiki-packet.md:6:target: "<TBD: wiki:<slug>, source record ref, ticket:<token>, or synthesis target slug>"
skills/loom-wiki/templates/wiki-packet.md:19:    - "<TBD: wiki page paths the child may modify, or None - rationale>"
skills/loom-wiki/templates/wiki-packet.md:23:    - "<TBD: ticket:<token> when a ticket owns follow-through, originating owner ref, or None - no additional parent record reconciliation needed>"
skills/loom-wiki/templates/wiki-packet.md:26:    - "<TBD: .loom/wiki/<slug>.md, other owner path, or None - no parent path reconciliation needed>"
skills/loom-tickets/templates/ticket.md:5:change_class: "<TBD: choose one change class before saving>"
skills/loom-tickets/templates/ticket.md:6:risk_class: "<TBD: choose low, medium, or high before saving>"
skills/loom-tickets/templates/ticket.md:57:- ACC-001: <TBD: write the first ticket-local acceptance criterion>
skills/loom-tickets/templates/ticket.md:58:- ACC-002: <TBD: write the second ticket-local acceptance criterion, or remove>
skills/loom-tickets/templates/ticket.md:89:Next route: <TBD: choose one route token before saving>
skills/loom-tickets/templates/ticket.md:147:Risk class: <TBD: repeat frontmatter risk_class>
skills/loom-tickets/templates/ticket.md:154:Critique policy: <TBD: choose optional, recommended, or mandatory>
skills/loom-tickets/templates/ticket.md:182:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-tickets/templates/ticket.md:197:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-initiatives/templates/initiative.md:55:- OBJ-001: <TBD: write one durable objective criterion before saving>
```

After `Replace with` search output:

```text
(no output)
```

After authoritative-status search shows `skills/loom-wiki/templates/index.md` no
longer defaults to `status: accepted`; remaining `status: accepted` wiki hit is
an instruction to replace placeholders before accepting:

```text
skills/loom-bootstrap/references/06-filesystem-and-tooling.md:66:not use `draft` status; keep `status: active` only when the copied record has a
skills/loom-bootstrap/references/06-filesystem-and-tooling.md:74:status: active
skills/loom-critique/templates/critique.md:37:Set `status: final` only when evidence reviewed, findings, residual risks, and
skills/loom-constitution/templates/constitution.md:4:status: active
skills/loom-plans/references/plan-shape.md:17:- Completion Basis when `status: completed`
skills/loom-evidence/templates/evidence.md:4:status: recorded
skills/loom-memory/templates/entities.md:7:key facts | status: active | last: YYYY-MM-DD | -> [[related-page-or-record]]
skills/loom-constitution/templates/decision.md:4:status: active
skills/loom-initiatives/templates/initiative.md:4:status: active
skills/loom-initiatives/templates/initiative.md:82:When `status: completed`, explain which success metrics were met and what
skills/loom-plans/templates/plan.md:4:status: active
skills/loom-plans/templates/plan.md:114:When `status: completed`, explain which exit criteria were met and where any
skills/loom-initiatives/references/initiative-shape.md:21:- Completion Basis when `status: completed`
skills/loom-research/templates/research.md:4:status: active
skills/loom-workspace/templates/workspace.md:4:status: active
skills/loom-wiki/templates/index.md:16:Replace placeholder lists before setting `status: accepted`.
skills/loom-workspace/templates/harness.md:4:status: active
skills/loom-constitution/templates/roadmap.md:4:status: active
skills/loom-constitution/templates/roadmap.md:43:When `status: completed`, explain which milestones were reached and what
```

`git diff --check` output:

```text
(no output)
```

Parent reconciliation check at `2026-05-02T23:24:37Z`:

- `git diff --check` passed with no output.
- Scoped ticket claim statuses use canonical `supported_pending_review`
  vocabulary.
- `packet:ralph-ticket-phsafe8-20260502T232054Z` frontmatter is `status:
  consumed` with concrete `parent_merge_scope.paths` and parent merge notes.

# Supports Claims

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-008`
- `ticket:phsafe8#ACC-001`
- `ticket:phsafe8#ACC-002`
- `ticket:phsafe8#ACC-003`
- `ticket:phsafe8#ACC-004`

# Challenges Claims

None - the observations did not falsify scoped acceptance claims.

# Environment

Commit: 4b85062b04ca9ba6c0b5c6402865f1fcdc6af54f
Branch: main
Runtime: Markdown/source corpus edits only; no app runtime
OS: Darwin 24.6.0 arm64
Relevant config: source worktree already contained parent ticket/packet updates
before child edits.

# Validity

Valid for: current working tree after the `ticket:phsafe8` child edits and parent
reconciliation.
Fresh enough for: parent reconciliation and mandatory critique of this iteration.
Recheck when: any `skills/**/templates/*.md`, relevant `skills/**/references/*.md`,
or this ticket changes before acceptance.
Invalidated by: later edits that add or remove placeholder/status search matches.
Supersedes / superseded by: None.

# Limitations

This evidence records structural search observations and a whitespace check. It
does not constitute oracle critique, ticket acceptance, or proof that every future
operator will interpret the templates correctly.

# Result

The targeted unsafe surfaces were hardened: the wiki index template now starts as
`draft`, the bootstrap here-doc no longer contains a bare `TBD` and warns to keep
`status: active` only after replacing placeholders, and the initiative success
metric now uses an explicit `<TBD: ... before saving>` placeholder. `git diff
--check` reported no whitespace errors.

# Interpretation

The observations support that the scoped placeholder safety cleanup landed and
that remaining scanned matches are either fail-closed placeholders, lifecycle
grammar examples, or allowed default statuses. Oracle critique and ticket-owned
acceptance are recorded separately.

# Related Records

- `ticket:phsafe8`
- `packet:ralph-ticket-phsafe8-20260502T232054Z`
- `critique:placeholder-safety-review`
