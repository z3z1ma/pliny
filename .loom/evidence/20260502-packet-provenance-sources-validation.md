---
id: evidence:packet-provenance-sources-validation
kind: evidence
status: recorded
created_at: 2026-05-02T22:42:54Z
updated_at: 2026-05-02T22:48:30Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:pktprov4
  packet:
    - packet:ralph-ticket-pktprov4-20260502T224150Z
  critique:
    - critique:packet-provenance-sources-review
external_refs: {}
---

# Summary

Observed packet provenance/context terms before and after the Ralph iteration,
then ran `git diff --check`. The after-state shows shared packet grammar and the
Ralph, critique, and wiki packet templates distinguishing
`source_fingerprint.compiled_from` provenance from `sources` task context while
preserving packet family boundaries.

# Procedure

1. Confirmed the packet source fingerprint commit matched `HEAD`:
   `c70983ffd03d56c5fcf74475c9bc454071e1ae5d`.
2. Captured before-state searches in the targeted packet frontmatter reference
   and Ralph/critique/wiki packet templates.
3. Edited only the allowed packet grammar reference, packet templates, ticket,
   evidence record, and Ralph packet.
4. Captured after-state searches in the same targeted files.
5. Ran `git diff --check`.
6. Parent reconciled ticket claim status vocabulary, packet lifecycle status, and
   evidence structure before mandatory critique.

# Artifacts

## Before search: provenance/context terms

Command:

```bash
rg -n "compiled_from|sources:|source_fingerprint" "skills/loom-records/references/packet-frontmatter.md" "skills/loom-ralph/templates/ralph-packet.md" "skills/loom-critique/templates/critique-packet.md" "skills/loom-wiki/templates/wiki-packet.md"
```

Output:

```text
skills/loom-records/references/packet-frontmatter.md:44:source_fingerprint:
skills/loom-records/references/packet-frontmatter.md:50:  compiled_from:
skills/loom-records/references/packet-frontmatter.md:65:sources: {}
skills/loom-records/references/packet-frontmatter.md:84:- `source_fingerprint`
skills/loom-records/references/packet-frontmatter.md:311:`source_fingerprint` makes the compilation baseline inspectable:
skills/loom-records/references/packet-frontmatter.md:314:source_fingerprint:
skills/loom-records/references/packet-frontmatter.md:320:  compiled_from:
skills/loom-wiki/templates/wiki-packet.md:28:source_fingerprint:
skills/loom-wiki/templates/wiki-packet.md:34:  compiled_from:
skills/loom-wiki/templates/wiki-packet.md:49:sources: {}
skills/loom-critique/templates/critique-packet.md:38:source_fingerprint:
skills/loom-critique/templates/critique-packet.md:44:  compiled_from:
skills/loom-critique/templates/critique-packet.md:59:sources: {}
skills/loom-ralph/templates/ralph-packet.md:30:source_fingerprint:
skills/loom-ralph/templates/ralph-packet.md:36:  compiled_from:
skills/loom-ralph/templates/ralph-packet.md:51:sources:
```

## Before search: packet family template mentions

Command:

```bash
rg -n "Ralph|Critique|Wiki|packet_kind:|verification_posture|review packet|synthesis packet|implementation packet" "skills/loom-records/references/packet-frontmatter.md" "skills/loom-ralph/templates/ralph-packet.md" "skills/loom-critique/templates/critique-packet.md" "skills/loom-wiki/templates/wiki-packet.md"
```

Highlights:

```text
skills/loom-records/references/packet-frontmatter.md:151:- `ralph` — implementation packet owned by the Ralph inner loop.
skills/loom-records/references/packet-frontmatter.md:152:- `critique` — review packet owned by the critique workflow.
skills/loom-records/references/packet-frontmatter.md:153:- `wiki` — synthesis packet owned by the wiki workflow.
skills/loom-records/references/packet-frontmatter.md:155:Critique and wiki packets may reuse packet discipline without becoming
skills/loom-records/references/packet-frontmatter.md:156:Ralph-governed. Do not infer Ralph child obligations merely because a critique or
skills/loom-critique/templates/critique-packet.md:77:Critique owns this review packet's workflow; using packet grammar does not make
skills/loom-critique/templates/critique-packet.md:78:the review Ralph-governed.
skills/loom-critique/templates/critique-packet.md:116:Critique packets do not use Ralph `verification_posture`. Review quality comes
skills/loom-wiki/templates/wiki-packet.md:68:Wiki owns this synthesis packet's workflow; using packet grammar does not make
skills/loom-wiki/templates/wiki-packet.md:69:the synthesis Ralph-governed.
skills/loom-wiki/templates/wiki-packet.md:76:Wiki packets do not use Ralph `verification_posture`. Synthesis quality comes
```

## After search: provenance/context terms

Command:

```bash
rg -n "compiled_from|sources:|source_fingerprint" "skills/loom-records/references/packet-frontmatter.md" "skills/loom-ralph/templates/ralph-packet.md" "skills/loom-critique/templates/critique-packet.md" "skills/loom-wiki/templates/wiki-packet.md"
```

Output:

```text
skills/loom-records/references/packet-frontmatter.md:44:source_fingerprint:
skills/loom-records/references/packet-frontmatter.md:51:  compiled_from:
skills/loom-records/references/packet-frontmatter.md:67:sources: {}
skills/loom-records/references/packet-frontmatter.md:86:- `source_fingerprint`
skills/loom-records/references/packet-frontmatter.md:98:`source_fingerprint.compiled_from` and `sources` answer different questions.
skills/loom-records/references/packet-frontmatter.md:100:- `source_fingerprint.compiled_from` is provenance for packet compilation. It
skills/loom-records/references/packet-frontmatter.md:109:short, truthful `compiled_from` list plus a task-specific `sources` mapping over
skills/loom-records/references/packet-frontmatter.md:329:`source_fingerprint` makes the compilation baseline inspectable:
skills/loom-records/references/packet-frontmatter.md:332:source_fingerprint:
skills/loom-records/references/packet-frontmatter.md:339:  compiled_from:
skills/loom-records/references/packet-frontmatter.md:396:`source_fingerprint.compiled_from`; put task-reading context here.
skills/loom-wiki/templates/wiki-packet.md:28:source_fingerprint:
skills/loom-wiki/templates/wiki-packet.md:35:  compiled_from:
skills/loom-wiki/templates/wiki-packet.md:51:sources: {}
skills/loom-wiki/templates/wiki-packet.md:73:Use `source_fingerprint.compiled_from` for packet compilation provenance and
skills/loom-ralph/templates/ralph-packet.md:30:source_fingerprint:
skills/loom-ralph/templates/ralph-packet.md:37:  compiled_from:
skills/loom-ralph/templates/ralph-packet.md:53:sources:
skills/loom-ralph/templates/ralph-packet.md:76:Use `source_fingerprint.compiled_from` for packet compilation provenance and
skills/loom-critique/templates/critique-packet.md:38:source_fingerprint:
skills/loom-critique/templates/critique-packet.md:45:  compiled_from:
skills/loom-critique/templates/critique-packet.md:61:sources: {}
skills/loom-critique/templates/critique-packet.md:82:Use `source_fingerprint.compiled_from` for packet compilation provenance and
```

## After search: packet family template mentions

Command:

```bash
rg -n "Provenance|Context:|Provenance Versus Context Sources|Ralph|Critique|Wiki|verification_posture|Ralph-governed|implementation packet|review packet|synthesis packet" "skills/loom-records/references/packet-frontmatter.md" "skills/loom-ralph/templates/ralph-packet.md" "skills/loom-critique/templates/critique-packet.md" "skills/loom-wiki/templates/wiki-packet.md"
```

Highlights:

```text
skills/loom-records/references/packet-frontmatter.md:96:## Provenance Versus Context Sources
skills/loom-records/references/packet-frontmatter.md:169:- `ralph` — implementation packet owned by the Ralph inner loop.
skills/loom-records/references/packet-frontmatter.md:170:- `critique` — review packet owned by the critique workflow.
skills/loom-records/references/packet-frontmatter.md:171:- `wiki` — synthesis packet owned by the wiki workflow.
skills/loom-records/references/packet-frontmatter.md:173:Critique and wiki packets may reuse packet discipline without becoming
skills/loom-records/references/packet-frontmatter.md:174:Ralph-governed. Do not infer Ralph child obligations merely because a critique or
skills/loom-ralph/templates/ralph-packet.md:52:# Context: source set the Ralph child should read or trust for this bounded iteration.
skills/loom-critique/templates/critique-packet.md:60:# Context: source set the critique reviewer should read or trust for this bounded review.
skills/loom-critique/templates/critique-packet.md:79:Critique owns this review packet's workflow; using packet grammar does not make
skills/loom-critique/templates/critique-packet.md:80:the review Ralph-governed.
skills/loom-wiki/templates/wiki-packet.md:50:# Context: source set the wiki synthesizer should read or trust for this bounded synthesis.
skills/loom-wiki/templates/wiki-packet.md:70:Wiki owns this synthesis packet's workflow; using packet grammar does not make
skills/loom-wiki/templates/wiki-packet.md:71:the synthesis Ralph-governed.
```

## Validation command

Command:

```bash
git diff --check
```

Result: passed with no output.

# Parent Reconciliation Check

Observed at `2026-05-02T22:45:58Z` after parent reconciliation:

- `git diff --check`: passed with no output.
- Scoped ticket claim statuses now use canonical `supported_pending_review`
  vocabulary.
- `packet:ralph-ticket-pktprov4-20260502T224150Z` frontmatter is `status:
  consumed` with parent merge notes.

# Supports Claims

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-004`
- `ticket:pktprov4#ACC-001`
- `ticket:pktprov4#ACC-002`
- `ticket:pktprov4#ACC-003`
- `ticket:pktprov4#ACC-004`

# Challenges Claims

None - the observations did not challenge a scoped claim.

# Environment

Commit: `c70983ffd03d56c5fcf74475c9bc454071e1ae5d` plus the scoped uncommitted
`ticket:pktprov4` diff.
Branch: `main`.
Runtime: Markdown corpus; no app runtime or automated test suite.
OS: macOS/Darwin.
Relevant config: repository-local Loom records and `skills/` product corpus.

# Validity

Valid for: the `ticket:pktprov4` packet frontmatter reference/template changes
and parent reconciliation at `2026-05-02T22:45:58Z`.
Recheck when: the shared packet frontmatter reference, Ralph packet template,
critique packet template, wiki packet template, ticket, evidence record, or Ralph
packet changes again before acceptance.

# Limitations

- Does not establish `ticket:pktprov4#ACC-005` by itself; final critique records
  own the oracle verdict.
- Does not validate packet surfaces outside the targeted shared reference and
  three packet templates.
- Does not close the ticket or own the acceptance decision.

# Result

The targeted shared reference and packet templates now distinguish packet
compilation provenance from consumer task context while preserving packet family
boundaries.

# Interpretation

- `source_fingerprint.compiled_from` now has explicit provenance wording in the
  shared reference and copied packet templates.
- `sources` now has explicit context-source wording for the packet consumer,
  Ralph child, critique reviewer, and wiki synthesizer.
- Existing packet family boundaries remained visible: Ralph owns implementation
  packets; critique owns review packets; wiki owns synthesis packets; critique
  and wiki templates still omit Ralph `verification_posture`.

# Residual Risks

- This evidence is structural and observational. Oracle critique passed with no
  findings, but evidence remains separate from critique verdicts and ticket
  acceptance.

# Related Records

- `initiative:skills-corpus-template-grammar-safety-pass`
- `plan:skills-corpus-template-grammar-safety-pass`
- `ticket:pktprov4`
- `packet:ralph-ticket-pktprov4-20260502T224150Z`
- `critique:packet-provenance-sources-review`
