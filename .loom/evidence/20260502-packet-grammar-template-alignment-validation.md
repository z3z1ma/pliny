---
id: evidence:packet-grammar-template-alignment-validation
kind: evidence
status: recorded
created_at: 2026-05-02T19:56:36Z
updated_at: 2026-05-02T20:09:25Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:pktgram5
  packet:
    - packet:ralph-ticket-pktgram5-20260502T195332Z
    - packet:ralph-ticket-pktgram5-20260502T200144Z
  critique:
    - critique:packet-grammar-template-alignment-review
    - critique:packet-grammar-template-alignment-rereview
external_refs: {}
---

# Summary

Observed packet grammar/template alignment before and after Ralph iteration
`packet:ralph-ticket-pktgram5-20260502T195332Z` for `ticket:pktgram5`.

# Procedure

- Read the active Ralph packet, ticket, shared packet frontmatter reference,
  naming reference, Ralph packet template and contract, critique packet template,
  and wiki packet template.
- Compared before-state field coverage across:
  - `skills/loom-records/references/packet-frontmatter.md`
  - `skills/loom-records/references/naming-and-ids.md`
  - `skills/loom-ralph/templates/ralph-packet.md`
  - `skills/loom-ralph/references/packet-contract.md`
  - `skills/loom-critique/templates/critique-packet.md`
  - `skills/loom-wiki/templates/wiki-packet.md`
- Updated the allowed references/templates and ran targeted packet-field searches.
- Ran `git diff --check` after creating this evidence record.
- During parent reconciliation, corrected remaining generic Ralph filename examples
  in `skills/loom-records/references/naming-and-ids.md` from `iter-01` to
  `iter-<NN>` so they match frontmatter `iteration`.
- During repair iteration 2, checked the oracle findings by searching the changed
  product surfaces for dogfood-specific `ticket:pktgram5` examples and for
  critique packet naming language around `review_target`.

# Artifacts

## Before-state comparison

- Shared packet frontmatter listed required common fields but did not identify a
  family-field matrix for `change_class`, `risk_class`, `iteration`,
  `verification_posture`, or `review_target`.
- Ralph template included `change_class`, `verification_posture`, and
  `iteration: 1`; critique template included `change_class` and `review_target`;
  wiki template omitted `change_class` and Ralph `verification_posture`.
- Naming reference used ambiguous packet ID placeholders such as
  `packet:ralph-<target>-<UTC compact timestamp>` while the Ralph filename
  pattern used `ticket-<token>-iter-01`.
- Ralph packet contract recommended `context_budget.posture: tight`, while the
  Ralph, critique, and wiki templates used `posture: normal`.
- Freshness stop guidance was strongest in the Ralph template/contract; critique
  and wiki templates did not consistently name source-fingerprint staleness in
  packet-family terms.

## After-state comparison

- Shared packet frontmatter now keeps required common fields separate from
  optional/family fields:
  - `change_class`: required by current Ralph and critique templates; omitted by
    wiki unless intentionally needed for synthesis context.
  - `risk_class`: optional shared grammar that does not replace ticket-owned
    critique disposition.
  - `iteration`: required by Ralph and mirrored by `iter-<NN>` in Ralph packet
    filenames.
  - `verification_posture`: required by Ralph and omitted by critique/wiki.
  - `review_target`: critique-family grammar.
- Naming reference and templates now use encoded packet targets such as
  `ticket:abc123xy` -> `ticket-abc123xy` and align ID/filename examples.
- Ralph packet contract and templates now use `context_budget.posture: normal` as
  the default while documenting `tight` and `expansive` as intentional choices.
- Ralph, critique, and wiki packet templates now state freshness/staleness stop
  conditions without making critique or wiki packets Ralph-governed.

## Targeted search result

Targeted search over the six changed product surfaces found the packet fields and
paths in the expected owner surfaces:

- `packet-frontmatter.md` defines required shared fields, optional/family fields,
  encoded packet IDs, filename patterns, source freshness expectations, and
  context budget defaults.
- `naming-and-ids.md` defines encoded packet ID families, packet paths, and Ralph
  filename `iter-<NN>` mapping to frontmatter `iteration`.
- `ralph-packet.md` includes `change_class`, optional commented `risk_class`,
  `verification_posture`, `iteration`, shared scope/fingerprint/budget fields,
  ID/filename mapping, and Ralph freshness stop conditions.
- `critique-packet.md` includes `change_class`, optional commented `risk_class`,
  `review_target`, shared scope/fingerprint/budget fields, critique-owned
  freshness stop conditions, and explicit omission of Ralph `verification_posture`.
- `wiki-packet.md` includes shared scope/fingerprint/budget fields, encoded
  target naming, explicit omission of Ralph `verification_posture`, default
  omission of `change_class`, and wiki-owned freshness stop conditions.
- `packet-contract.md` repeats Ralph-specific required fields, optional
  `risk_class`, ID/filename mapping, freshness checks, and `normal` context
  budget default.

## `git diff --check`

Result: passed; exit code 0 with no output.

## Repair iteration 2 observations

- Replaced product-surface examples using `ticket:pktgram5` with neutral
  fictional examples using `ticket:abc123xy` -> `ticket-abc123xy` in:
  - `skills/loom-records/references/packet-frontmatter.md`
  - `skills/loom-records/references/naming-and-ids.md`
  - `skills/loom-critique/templates/critique-packet.md`
- Clarified critique packet naming so packet IDs and filenames encode the packet
  `target` or an explicitly chosen lowercase change slug for discovery, while the
  structured `review_target` field records the artifact, diff, PR, branch,
  commit, or record under review.
- Search over the three changed product surfaces for `ticket[:\-]pktgram5`
  returned no matches after the repair.
- Search over `skills/loom-critique/templates/critique-packet.md` confirmed the
  template now distinguishes encoded packet `target` / explicit change slug from
  structured `review_target`.
- Repair `git diff --check` result: passed; exit code 0 with no output.

# Supports Claims

- `initiative:skills-corpus-council-precision-pass#OBJ-005`
- `ticket:pktgram5#ACC-001`
- `ticket:pktgram5#ACC-002`
- `ticket:pktgram5#ACC-003`
- `ticket:pktgram5#ACC-004`

# Challenges Claims

None - this evidence does not falsify the targeted claims.

# Environment

Commit: `cceb6422bf5c95cfaf2c45983bb6a412c748c94f` baseline with expected active ticket/packet setup edits
Branch: `main`
Runtime: Markdown/file-tool validation
OS: darwin
Relevant config: no network, no Git metadata mutation, no runtime schema helper

# Validity

Valid for: current diff for `ticket:pktgram5` after parent reconciliation.
Recheck when: packet grammar references/templates, ticket acceptance claims, or
write-scope files change again.

# Limitations

This evidence is structural. It records reference/template comparison, repair
searches, and diff sanity, not an oracle critique verdict. Mandatory critique is
recorded in `critique:packet-grammar-template-alignment-review` and
`critique:packet-grammar-template-alignment-rereview`.

# Result

The packet references and templates now present a consistent shared/family packet
grammar, explicit packet ID/filename mapping, aligned context budget defaults,
and family-local freshness stop guidance while preserving critique/wiki route
ownership.

# Interpretation

The evidence supports ACC-001 through ACC-004. Repair iteration 2 provides
observations addressing `PKTGRAM5-CRIT-001` and `PKTGRAM5-CRIT-002`; oracle
re-critique in `critique:packet-grammar-template-alignment-rereview` satisfies
ACC-005.

# Related Records

- `ticket:pktgram5`
- `packet:ralph-ticket-pktgram5-20260502T195332Z`
- `packet:ralph-ticket-pktgram5-20260502T200144Z`
- `critique:packet-grammar-template-alignment-review`
- `critique:packet-grammar-template-alignment-rereview`
