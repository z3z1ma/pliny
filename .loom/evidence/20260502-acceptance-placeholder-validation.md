---
id: evidence:acceptance-placeholder-validation
kind: evidence
status: recorded
created_at: 2026-05-02T23:00:22Z
updated_at: 2026-05-02T23:05:14Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:accspec6
  packet:
    - packet:ralph-ticket-accspec6-20260502T225846Z
  critique:
    - critique:acceptance-placeholder-ownership-review
external_refs: {}
---

# Summary

Observation-first validation for `ticket:accspec6`, checking that the ticket
template and claim coverage reference distinguish spec-owned acceptance from
ticket-local `ACC-*` criteria without removing ticket-local acceptance for
no-spec work.

# Procedure

Before editing the targeted ticket template and claim coverage reference, ran:

```bash
rg -n 'ACC-|spec-owned acceptance|ticket-local acceptance|acceptance contract|# Acceptance Criteria|# Coverage' \
  'skills/loom-tickets/templates/ticket.md' \
  'skills/loom-records/references/claim-coverage.md'
```

After editing the targeted files and updating `ticket:accspec6`, ran the same
search again, then ran:

```bash
git diff --check
```

# Artifacts

## Before observations

Command result:

```text
skills/loom-tickets/templates/ticket.md:38:# Acceptance Criteria
skills/loom-tickets/templates/ticket.md:42:If a spec owns the acceptance contract, summarize only the ticket-scoped work
skills/loom-tickets/templates/ticket.md:43:here and cite the spec-owned acceptance IDs under `# Coverage`.
skills/loom-tickets/templates/ticket.md:45:If no spec owns the acceptance contract, this ticket may own ticket-local
skills/loom-tickets/templates/ticket.md:49:- ACC-001: <TBD: write the first ticket-local acceptance criterion>
skills/loom-tickets/templates/ticket.md:50:- ACC-002: <TBD: write the second ticket-local acceptance criterion, or remove>
skills/loom-tickets/templates/ticket.md:52:# Coverage
skills/loom-tickets/templates/ticket.md:58:- Use `spec:<slug>#ACC-001` for spec-owned acceptance.
skills/loom-tickets/templates/ticket.md:59:- Use `ticket:<token>#ACC-001` for ticket-local acceptance criteria owned in
skills/loom-records/references/claim-coverage.md:15:- `ACC-001` for acceptance units in the spec or ticket that owns the acceptance
skills/loom-records/references/claim-coverage.md:29:spec:<slug>#ACC-001
skills/loom-records/references/claim-coverage.md:30:ticket:<token>#ACC-001
skills/loom-records/references/claim-coverage.md:66:- ACC-001: Given unresolved high-severity critique, the ticket acceptance gate leaves the ticket open.
skills/loom-records/references/claim-coverage.md:67:- ACC-002: Given missing evidence, the ticket acceptance gate reports the gap and leaves a concrete next step.
skills/loom-records/references/claim-coverage.md:76:# Coverage
skills/loom-records/references/claim-coverage.md:80:- spec:<slug>#ACC-001
skills/loom-records/references/claim-coverage.md:81:- spec:<slug>#ACC-002
skills/loom-records/references/claim-coverage.md:86:When no spec owns the acceptance contract, the ticket may own ticket-local
skills/loom-records/references/claim-coverage.md:87:acceptance criteria. Write the local IDs in `# Acceptance Criteria` and cite them
skills/loom-records/references/claim-coverage.md:88:from packets, evidence, and critique as `ticket:<token>#ACC-001`:
skills/loom-records/references/claim-coverage.md:91:# Acceptance Criteria
skills/loom-records/references/claim-coverage.md:93:- ACC-001: The ticket readiness template is route-neutral.
skills/loom-records/references/claim-coverage.md:94:- ACC-002: Evidence records the structural validation outputs.
skills/loom-records/references/claim-coverage.md:96:# Coverage
skills/loom-records/references/claim-coverage.md:100:- ticket:<token>#ACC-001
skills/loom-records/references/claim-coverage.md:101:- ticket:<token>#ACC-002
skills/loom-records/references/claim-coverage.md:104:Do not use ticket-local `ACC-*` IDs to replace a reusable spec-owned acceptance
skills/loom-records/references/claim-coverage.md:106:a spec and cite `spec:<slug>#ACC-001` instead.
skills/loom-records/references/claim-coverage.md:117:| spec:<slug>#ACC-001 | evidence:<slug> | critique:<slug>#FIND-001 resolved | supported |
skills/loom-records/references/claim-coverage.md:118:| ticket:<token>#ACC-001 | evidence:<slug> | pending | supported_pending_review |
skills/loom-records/references/claim-coverage.md:138:- spec:<slug>#ACC-001
skills/loom-records/references/claim-coverage.md:139:- ticket:<token>#ACC-001
skills/loom-records/references/claim-coverage.md:150:- spec:<slug>#ACC-001
skills/loom-records/references/claim-coverage.md:151:- spec:<slug>#ACC-002
skills/loom-records/references/claim-coverage.md:152:- ticket:<token>#ACC-001
skills/loom-records/references/claim-coverage.md:162:- spec:<slug>#ACC-002
skills/loom-records/references/claim-coverage.md:163:- ticket:<token>#ACC-001
skills/loom-records/references/claim-coverage.md:171:rg -n 'spec:<slug>#ACC-002' .loom
skills/loom-records/references/claim-coverage.md:172:rg -n 'ticket:<token>#ACC-001' .loom
skills/loom-records/references/claim-coverage.md:175:rg -n '^# Coverage|^Covers:' .loom/tickets
```

Observation: the template named spec-owned acceptance first, but the same section
then presented ticket-local `ACC-*` examples without an explicit branch choice.
The claim coverage reference already warned not to replace a spec-owned
acceptance contract with ticket-local `ACC-*` IDs.

## After observations

Command result:

```text
skills/loom-tickets/templates/ticket.md:38:# Acceptance Criteria
skills/loom-tickets/templates/ticket.md:47:Use this branch when a spec owns the reusable acceptance contract. Do not create
skills/loom-tickets/templates/ticket.md:48:ticket-local `ACC-*` criteria here. Summarize only the ticket-scoped work here
skills/loom-tickets/templates/ticket.md:49:and cite the spec-owned acceptance IDs under `# Coverage`.
skills/loom-tickets/templates/ticket.md:53:If no spec owns the acceptance contract, this ticket may own ticket-local
skills/loom-tickets/templates/ticket.md:57:- ACC-001: <TBD: write the first ticket-local acceptance criterion>
skills/loom-tickets/templates/ticket.md:58:- ACC-002: <TBD: write the second ticket-local acceptance criterion, or remove>
skills/loom-tickets/templates/ticket.md:60:# Coverage
skills/loom-tickets/templates/ticket.md:66:- Use `spec:<slug>#ACC-001` for spec-owned acceptance.
skills/loom-tickets/templates/ticket.md:67:- Use `ticket:<token>#ACC-001` for ticket-local acceptance criteria owned in
skills/loom-records/references/claim-coverage.md:15:- `ACC-001` for acceptance units in the spec or ticket that owns the acceptance
skills/loom-records/references/claim-coverage.md:29:spec:<slug>#ACC-001
skills/loom-records/references/claim-coverage.md:30:ticket:<token>#ACC-001
skills/loom-records/references/claim-coverage.md:66:- ACC-001: Given unresolved high-severity critique, the ticket acceptance gate leaves the ticket open.
skills/loom-records/references/claim-coverage.md:67:- ACC-002: Given missing evidence, the ticket acceptance gate reports the gap and leaves a concrete next step.
skills/loom-records/references/claim-coverage.md:76:acceptance contract, cite the spec-owned IDs under `# Coverage` and do not create
skills/loom-records/references/claim-coverage.md:77:ticket-local `ACC-*` criteria for that contract:
skills/loom-records/references/claim-coverage.md:80:# Coverage
skills/loom-records/references/claim-coverage.md:84:- spec:<slug>#ACC-001
skills/loom-records/references/claim-coverage.md:85:- spec:<slug>#ACC-002
skills/loom-records/references/claim-coverage.md:90:When no spec owns the acceptance contract, the ticket may own ticket-local
skills/loom-records/references/claim-coverage.md:91:acceptance criteria. Write the local IDs in `# Acceptance Criteria` and cite them
skills/loom-records/references/claim-coverage.md:92:from packets, evidence, and critique as `ticket:<token>#ACC-001`:
skills/loom-records/references/claim-coverage.md:95:# Acceptance Criteria
skills/loom-records/references/claim-coverage.md:97:- ACC-001: The ticket readiness template is route-neutral.
skills/loom-records/references/claim-coverage.md:98:- ACC-002: Evidence records the structural validation outputs.
skills/loom-records/references/claim-coverage.md:100:# Coverage
skills/loom-records/references/claim-coverage.md:104:- ticket:<token>#ACC-001
skills/loom-records/references/claim-coverage.md:105:- ticket:<token>#ACC-002
skills/loom-records/references/claim-coverage.md:108:Do not use ticket-local `ACC-*` IDs to replace a reusable spec-owned acceptance
skills/loom-records/references/claim-coverage.md:110:a spec and cite `spec:<slug>#ACC-001` instead.
skills/loom-records/references/claim-coverage.md:121:| spec:<slug>#ACC-001 | evidence:<slug> | critique:<slug>#FIND-001 resolved | supported |
skills/loom-records/references/claim-coverage.md:122:| ticket:<token>#ACC-001 | evidence:<slug> | pending | supported_pending_review |
skills/loom-records/references/claim-coverage.md:142:- spec:<slug>#ACC-001
skills/loom-records/references/claim-coverage.md:143:- ticket:<token>#ACC-001
skills/loom-records/references/claim-coverage.md:154:- spec:<slug>#ACC-001
skills/loom-records/references/claim-coverage.md:155:- spec:<slug>#ACC-002
skills/loom-records/references/claim-coverage.md:156:- ticket:<token>#ACC-001
skills/loom-records/references/claim-coverage.md:166:- spec:<slug>#ACC-002
skills/loom-records/references/claim-coverage.md:167:- ticket:<token>#ACC-001
skills/loom-records/references/claim-coverage.md:175:rg -n 'spec:<slug>#ACC-002' .loom
skills/loom-records/references/claim-coverage.md:176:rg -n 'ticket:<token>#ACC-001' .loom
skills/loom-records/references/claim-coverage.md:179:rg -n '^# Coverage|^Covers:' .loom/tickets
```

Observation: the template now requires choosing one acceptance owner branch,
keeps ticket-local `ACC-*` placeholders only in the ticket-local branch, and
warns not to create ticket-local `ACC-*` criteria when a spec owns the reusable
acceptance contract. The claim coverage reference now introduces the same owner
choice before showing the spec-owned coverage example.

## Whitespace validation

`git diff --check` produced no output and exited successfully.

Parent reconciliation check at `2026-05-02T23:03:12Z`:

- `git diff --check` passed with no output.
- Scoped ticket claim statuses use canonical `supported_pending_review`
  vocabulary.
- `packet:ralph-ticket-accspec6-20260502T225846Z` frontmatter is `status:
  consumed` with parent merge notes.

# Supports Claims

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-006`
- `ticket:accspec6#ACC-001`
- `ticket:accspec6#ACC-002`
- `ticket:accspec6#ACC-003`
- `ticket:accspec6#ACC-004`

# Challenges Claims

None observed.

# Environment

Commit: `26964cef5ba528eb70cb1e4ece42efcf812c97c0`
Branch: `main`
Runtime: Markdown record and source inspection with `rg`; whitespace validation
with `git diff --check`
OS: Darwin 24.6.0 arm64
Relevant config: packet `packet:ralph-ticket-accspec6-20260502T225846Z`,
observation-first verification posture

# Validity

Valid for: the targeted ticket template and claim coverage reference diff
produced by this Ralph iteration and parent reconciliation.
Fresh enough for: mandatory oracle critique of `ticket:accspec6` from this source
state.
Recheck when: the ticket template, claim coverage reference, or acceptance owner
boundary changes.
Invalidated by: later edits that reintroduce ticket-local `ACC-*` placeholders as
the apparent default when a spec owns acceptance.
Supersedes / superseded by: None.

# Limitations

This evidence records structural observations and whitespace validation. It does
not provide the oracle critique verdict, acceptance decision, or ticket closure.

# Result

The observed diff separates spec-owned and ticket-local acceptance guidance in
the ticket template while preserving ticket-local `ACC-*` criteria for work with
no spec-owned acceptance contract. `git diff --check` passed.

# Interpretation

The evidence supports `ticket:accspec6#ACC-001` through
`ticket:accspec6#ACC-004`. Oracle critique and ticket-owned acceptance are
recorded separately.

# Related Records

- `ticket:accspec6`
- `packet:ralph-ticket-accspec6-20260502T225846Z`
- `critique:acceptance-placeholder-ownership-review`
