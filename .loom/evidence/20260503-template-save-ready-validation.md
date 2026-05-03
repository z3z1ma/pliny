---
id: evidence:template-save-ready-validation
kind: evidence
status: recorded
created_at: 2026-05-03T05:05:24Z
updated_at: 2026-05-03T05:05:24Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:tplsave3
  packet:
    - packet:ralph-ticket-tplsave3-20260503T050338Z
  initiative:
    - initiative:skills-corpus-context-integrity-hardening-pass
external_refs: {}
---

# Summary

Observed save-ready template guidance for `ticket:tplsave3` and checked ticket
template placeholder/branch pruning, plan template wave/placeholder pruning,
retained closure gates, and absence of forbidden template machinery.

# Procedure

Observed at: 2026-05-03T05:05:24Z

Source state: working tree on `main` based on commit
`e5abe407d9ba526af48dde2e519bc1a1901fc734`, after Ralph child output and before
mandatory critique.

Procedure:

- Ran targeted `rg` checks over ticket and plan templates.
- Added the new Ralph packet to the index with intent-to-add and ran
  `git diff --check` so the check covered new packet content and tracked edits.

Procedure verdict / exit code: pass; targeted positive searches returned expected
lines, forbidden machinery search returned no matches, and `git diff --check`
returned no output.

# Artifacts

## Ticket Template Save-Ready Rule

Command:

```bash
rg -n 'Save-ready rule|replace every placeholder|Remove the unused acceptance owner branch|unused route-readiness branches|closure gates' skills/loom-tickets/templates/ticket.md
```

Output:

```text
22:Save-ready rule: replace every placeholder before saving. Remove the unused
23:acceptance owner branch and unused route-readiness branches; do not remove
24:evidence, critique, retrospective / promotion, acceptance, or closure gates just
```

## Plan Template Save-Ready Rule

Command:

```bash
rg -n 'Save-ready rule|unused wave examples|placeholder rows|meaningful `None - reason`|claim / acceptance coverage|evidence / critique route|readiness|exit, and completion gates' skills/loom-plans/templates/plan.md
```

Output:

```text
54:Save-ready rule: remove unused wave examples and placeholder rows before saving.
56:meaningful `None - reason` when a wave or coverage item genuinely does not
57:apply; keep claim / acceptance coverage, evidence / critique route, readiness,
58:exit, and completion gates intact.
77:Wave readiness table:
```

## Retained Ticket Closure Gates

Command:

```bash
rg -n '^# (Evidence|Critique Disposition|Retrospective / Promotion Disposition|Wiki Disposition|Acceptance Decision)|evidence feeds the ticket-owned acceptance gate|Mandatory critique fail-closed rule|Open medium/high findings|Accepted by:|Residual risks:' skills/loom-tickets/templates/ticket.md
```

Output:

```text
164:Residual risks:
171:# Evidence
181:- Remember: evidence feeds the ticket-owned acceptance gate; evidence does not
184:# Critique Disposition
215:Open medium/high findings must have ticket-owned dispositions of `resolved`,
227:Mandatory critique fail-closed rule:
245:# Retrospective / Promotion Disposition
270:# Wiki Disposition
277:# Acceptance Decision
282:Accepted by:
285:Residual risks:
```

## Retained Plan Gates

Command:

```bash
rg -n '^# (Claim / Acceptance Coverage|Plan Readiness Review|Exit Criteria|Completion Basis)|Evidence Strategy|Evidence / critique route|Stop / loopback conditions' skills/loom-plans/templates/plan.md
```

Output:

```text
40:# Claim / Acceptance Coverage
46:| Source claim / acceptance ID | Downstream ticket | Coverage expectation | Evidence / critique route | Notes |
88:# Evidence Strategy
92:# Plan Readiness Review
112:Stop / loopback conditions:
114:# Exit Criteria
118:# Completion Basis
```

## Forbidden Template Machinery Search

Command:

```bash
rg -n 'template generator|template generators|schemas|separate canonical minimal/full|minimal/full template|minimal-full|template families' skills/loom-tickets/templates/ticket.md skills/loom-plans/templates/plan.md skills/loom-records/references/frontmatter.md
```

Output:

```text
```

Exit status: pass; no forbidden generator/schema/minimal-full-template-family
wording was found.

## Full Diff Whitespace Check

Command:

```bash
git add -N ".loom/packets/ralph/20260503T050338Z-ticket-tplsave3-iter-01.md" && git diff --check
```

Output:

```text
```

Exit status: pass; no whitespace errors were reported.

# Supports Claims

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-004`
- `ticket:tplsave3#ACC-001`
- `ticket:tplsave3#ACC-002`
- `ticket:tplsave3#ACC-003`
- `ticket:tplsave3#ACC-004`

# Challenges Claims

None - no challenged claims were observed.

# Environment

Commit: `e5abe407d9ba526af48dde2e519bc1a1901fc734` plus uncommitted
ticket-scoped working-tree changes

Branch: `main`

Runtime: none; Markdown corpus only

OS: macOS / Darwin

Relevant config: no app runtime or automated test suite

# Validity

Valid for: the listed files observed at 2026-05-03T05:05:24Z.

Fresh enough for: mandatory critique and ticket acceptance review for
`ticket:tplsave3`.

Recheck when: ticket or plan template wording, ticket criteria, or critique
findings change before closure.

Invalidated by: later edits that remove evidence, critique, retrospective,
acceptance, or closure gates, or introduce template generators/schemas/minimal-full
template families.

Supersedes / superseded by: None.

# Limitations

This evidence does not prove the template instructions are sufficient; mandatory
critique and ticket-owned acceptance decide that.

# Result

The observed template changes are concise Markdown guidance and stay within the
declared write scope.

# Interpretation

The observations support the ticket's structural claims, pending critique.

# Related Records

- `ticket:tplsave3`
- `packet:ralph-ticket-tplsave3-20260503T050338Z`
- `initiative:skills-corpus-context-integrity-hardening-pass`
