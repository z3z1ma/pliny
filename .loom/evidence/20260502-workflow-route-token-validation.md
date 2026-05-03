---
id: evidence:workflow-route-token-validation
kind: evidence
status: recorded
created_at: 2026-05-02T23:42:42Z
updated_at: 2026-05-03T00:04:53Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:routewf10
  packet:
    - packet:ralph-ticket-routewf10-20260502T234101Z
    - packet:ralph-ticket-routewf10-20260502T235105Z
    - packet:ralph-ticket-routewf10-20260503T000116Z
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
external_refs: {}
---

# Summary

Observation-first validation for `ticket:routewf10`: workflow route-token guidance
was checked before and after adding explicit route tokens for first-class workflow
coordinators that need route values: `debugging`, `spike`, `codemap`, and
`ship`.

# Procedure

1. Checked source fingerprint and working tree before edits with
   `git rev-parse HEAD && git status --short`.
2. Captured before-state workflow coordinator mentions with
   `rg -n "ship|spike|codemap|debugging" "skills"`.
3. Captured before-state route-token lists and route-field examples with
   `rg -n 'next route:|Route:|proposed next route:|route-priority|route token|route-token|allowed-token|shared route vocabulary|Canonical Route Tokens|Use \`skills/loom-records/references/route-vocabulary.md\`' "skills"`.
4. Updated shared route vocabulary and dependent route-token lists/examples in
   records, tickets, workspace, and drive guidance.
5. Captured after-state route-token searches with the same workflow and
   route-field searches, plus targeted searches over the touched route surfaces.
6. Ran `git diff --check` after the documentation and record updates.

# Artifacts

## Before observations

- Source fingerprint command returned `HEAD` at
  `3bfbe9226ecf2001fc5fd1d07d9efb999f8d156d`. `git status --short` showed the
  parent-launched ticket update and untracked packet already present:
  `M .loom/tickets/20260502-routewf10-audit-workflow-route-tokens.md` and
  `?? .loom/packets/ralph/20260502T234101Z-ticket-routewf10-iter-01.md`.
- Before workflow search showed first-class coordinators existed in the skill
  corpus, especially:
  - `skills/loom-workspace/references/routing.md` named `loom-debugging`,
    `loom-spike`, `loom-codemap`, and `loom-ship` as workflow/support
    coordinators.
  - `skills/loom-debugging/SKILL.md`, `skills/loom-spike/SKILL.md`,
    `skills/loom-codemap/SKILL.md`, and `skills/loom-ship/SKILL.md` existed as
    workflow skills.
  - `skills/loom-bootstrap/references/02-truth-and-authority.md` already named
    debugging, spikes, code maps, and shipping as workflow skills that route
    durable claims back to owner layers.
- Before route-field search showed route lists/examples in
  `skills/loom-records/references/route-vocabulary.md`,
  `skills/loom-tickets/templates/ticket.md`,
  `skills/loom-tickets/references/readiness.md`,
  `skills/loom-drive/references/checkpoint-resume-protocol.md`,
  `skills/loom-drive/references/continuity-contract.md`, and
  `skills/loom-drive/templates/outer-loop-handoff.md` omitted `debugging`,
  `spike`, `codemap`, and `ship`.
- The first route-field search attempt used an unescaped backtick in the shell
  pattern and produced `zsh:1: permission denied:
  skills/loom-records/references/route-vocabulary.md`; it was discarded and
  rerun safely before edits with a single-quoted pattern.

## After observations

- `skills/loom-records/references/route-vocabulary.md` now includes canonical
  tokens `debugging`, `spike`, `codemap`, and `ship`, while preserving the
  non-runtime statement that route tokens are grep-friendly Markdown vocabulary,
  not an enum, command router, or new owner layer.
- The shared vocabulary now says workflow coordinator tokens exist only when the
  coordinator itself is the next governed move. It explicitly routes narrower
  known truth changes through existing owner tokens such as `research`,
  `evidence`, `wiki`, `ralph`, `critique`, and `acceptance_review` instead of
  adding synonyms.
- Downstream route-token lists/examples now include the four workflow tokens in:
  - `skills/loom-tickets/templates/ticket.md`
  - `skills/loom-tickets/references/readiness.md`
  - `skills/loom-drive/references/checkpoint-resume-protocol.md`
  - `skills/loom-drive/references/continuity-contract.md`
  - `skills/loom-drive/templates/outer-loop-handoff.md`
- Workflow routing and drive guidance now map coordinator moves to route tokens
  in:
  - `skills/loom-workspace/references/routing.md`
  - `skills/loom-drive/references/drive-loop.md`
  - `skills/loom-drive/references/tranche-decision-protocol.md`

## Remediation observations

- Remediated `critique:workflow-route-token-review#FIND-001` by updating the
  ticket readiness introductory route list to defer to the canonical vocabulary,
  adding explicit ticket-template readiness prompts for `debugging`, `spike`,
  `codemap`, and `ship`, and rewriting plan/Ralph route-option prose to name
  current route tokens such as `ralph`, `critique`, `acceptance_review`, and
  `ship`.
- Remediated `critique:workflow-route-token-review#FIND-002` by placing
  `debugging`, `spike`, and `codemap` before implementation routes in the drive
  route-priority table, and by narrowing `ralph` to one bounded implementation
  iteration that needs a fresh child packet or explicit write boundary.
- `ship` remains packaging/handoff guidance only; updated ticket, plan, Ralph,
  and drive text continue to say shipping does not close the ticket.

## Third remediation observations

- Remediated the remaining open portion of
  `critique:workflow-route-token-review#FIND-001` identified by
  `critique:workflow-route-token-rereview` by updating broader active route-list
  guidance in:
  - `skills/loom-drive/SKILL.md`
  - `skills/loom-ralph/SKILL.md`
  - `skills/loom-bootstrap/references/03-outer-loop.md`
  - `PROTOCOL.md`
- `skills/loom-drive/SKILL.md` now names the route vocabulary as the source for
  bounded execution route choices and includes `debugging`, `spike`, `codemap`,
  and `ship` in active drive route lists.
- `skills/loom-ralph/SKILL.md` now narrows Ralph away from non-implementation
  canonical routes, includes `debugging`, `spike`, `codemap`, `ship`, and
  `acceptance_review` in parent next-route options, and points parent
  reconciliation to the route vocabulary.
- `skills/loom-bootstrap/references/03-outer-loop.md` now defers ready-ticket
  route-token choice to `skills/loom-records/references/route-vocabulary.md`,
  includes `debugging`, `spike`, `codemap`, and `ship` in decomposition shapes,
  and says `ship` does not own ticket closure.
- `PROTOCOL.md` now defers execution route examples to shared route vocabulary,
  includes `debugging`, `spike`, `codemap`, and `ship`, and keeps `ship` separate
  from ticket closure.

## Validation commands and results

- `rg -n "ship|spike|codemap|debugging" "skills"` after edits found the new
  route-token mentions in route vocabulary, ticket/drive route lists, workspace
  routing, and drive decision/reconciliation guidance. It also still found
  ordinary prose hits such as `shipped`, `shipping`, `ownership`, `relationship`,
  workflow skill names, and bootstrap doctrine examples. These are not active
  route-value fields and do not indicate route-token drift.
- `rg -n 'next route:|Route:|proposed next route:|route-priority|route token|route-token|allowed-token|shared route vocabulary|Canonical Route Tokens|Use \`skills/loom-records/references/route-vocabulary.md\`' "skills"`
  after edits found updated route lists in drive checkpoint/continuity, outer-loop
  handoff, ticket template/readiness, workspace routing, route priority guidance,
  and route vocabulary. Broad hits that remain are ordinary prose or route-token
  guidance rather than stale allowed-token lists.
- Targeted after-state search over touched route surfaces found all four new
  tokens in the canonical vocabulary and dependent route lists.
- `git diff --check`: passed with no output.
- Remediation search
  `rg -n 'debugging|spike|codemap|ship' "skills/loom-tickets/templates/ticket.md" "skills/loom-tickets/references/readiness.md" "skills/loom-drive/references/drive-loop.md" "skills/loom-drive/references/tranche-decision-protocol.md" "skills/loom-plans/references/slicing.md" "skills/loom-ralph/references/work-driver.md" "skills/loom-records/references/route-vocabulary.md"`
  found route-token coverage in the canonical vocabulary, ticket template,
  ticket readiness, drive loop, route priority/reconciliation guidance, plan
  slicing, and Ralph route-decision guidance.
- Remediation search
  ``rg -n '`ralph`|`debugging`|`spike`|`codemap`|`ship`|Route Decision Priority|first true condition' "skills/loom-drive/references/tranche-decision-protocol.md" "skills/loom-records/references/route-vocabulary.md"``
  showed `debugging`, `spike`, and `codemap` before `ralph` in the first-true
  priority table, with `ralph` narrowed to bounded implementation.
- Remediation stale-prose search
  `rg -n 'another Ralph iteration|direct critique|Ralph packet, direct critique|outer-loop refinement|Next route: ralph' "skills/loom-plans/references/slicing.md" "skills/loom-ralph/references/work-driver.md" "skills/loom-tickets/references/readiness.md" "skills/loom-tickets/templates/ticket.md" ".loom/tickets/20260502-routewf10-audit-workflow-route-tokens.md"`
  returned no matches after replacing stale route-option prose and moving the
  ticket next route to `critique`.
- Remediation `git diff --check`: passed with no output.
- Third-remediation target route coverage search
  `rg -n 'debugging|spike|codemap|ship|route-vocabulary|canonical route|local_edit|ralph|critique|wiki|retrospective|evidence|acceptance_review' "skills/loom-drive/SKILL.md" "skills/loom-ralph/SKILL.md" "skills/loom-bootstrap/references/03-outer-loop.md" "PROTOCOL.md"`
  found canonical route vocabulary deferral and route-token coverage in all four
  target stale route-list surfaces.
- Third-remediation stale-prose search
  `rg -n 'local edit, Ralph implementation packet, direct|Ralph again|outer-loop refinement|direct critique|perform a local edit, Ralph|Next route: ralph' "skills/loom-drive/SKILL.md" "skills/loom-ralph/SKILL.md" "skills/loom-bootstrap/references/03-outer-loop.md" "PROTOCOL.md" ".loom/tickets/20260502-routewf10-audit-workflow-route-tokens.md"`
  returned no matches after replacing stale route-option prose and moving the
  ticket next route to `critique`.
- Third-remediation ship/closure search
  `rg -n 'ship.*closure|closure.*ship|does not own ticket closure|does not close|without owning ticket closure' "skills/loom-drive/SKILL.md" "skills/loom-ralph/SKILL.md" "skills/loom-bootstrap/references/03-outer-loop.md" "PROTOCOL.md" "skills/loom-records/references/route-vocabulary.md"`
  found explicit separation of `ship` from ticket closure in the target route
  surfaces and canonical route vocabulary.
- Third-remediation `git diff --check`: passed with no output.

# Supports Claims

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-010`
- `ticket:routewf10#ACC-001`
- `ticket:routewf10#ACC-002`
- `ticket:routewf10#ACC-003`
- `ticket:routewf10#ACC-004`

# Challenges Claims

None observed.

# Environment

Commit: `3bfbe9226ecf2001fc5fd1d07d9efb999f8d156d`
Branch: `main`
Runtime: Markdown structural validation and ripgrep searches
OS: macOS / darwin
Relevant config: no runtime validator, enum, command router, CLI, command wrapper,
hidden helper, schema engine, or new owner layer added.

# Validity

Valid for: the current working tree diff for `ticket:routewf10` at the recorded
source fingerprint.

Fresh enough for: structural route-token alignment review and mandatory oracle
critique.

Recheck when: route vocabulary, workflow coordinator guidance, ticket route
templates, drive checkpoint/continuity guidance, or workspace routing changes.

Invalidated by: adding or removing route-bearing workflow coordinators without
updating shared route vocabulary and dependent route lists.

Supersedes / superseded by: None.

# Limitations

This evidence supports structural route-token alignment. It does not replace the
mandatory oracle critique required by `ticket:routewf10#ACC-005`, and it does not
prove operator clarity beyond the inspected Markdown guidance.

# Result

The shared route vocabulary and dependent route-bearing surfaces now represent
`debugging`, `spike`, `codemap`, and `ship` as first-class route tokens while
preserving Loom's Markdown-native, non-runtime route vocabulary framing.

# Interpretation

The evidence supports `ticket:routewf10#ACC-001` through
`ticket:routewf10#ACC-004` pending mandatory oracle re-review. It does not justify
ticket closure because oracle critique remains required for
`ticket:routewf10#ACC-005`.

# Related Records

- `ticket:routewf10`
- `packet:ralph-ticket-routewf10-20260502T234101Z`
- `packet:ralph-ticket-routewf10-20260502T235105Z`
- `packet:ralph-ticket-routewf10-20260503T000116Z`
- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-010`
