---
id: evidence:packet-lifecycle-parity-validation
kind: evidence
status: recorded
created_at: 2026-05-02T20:12:20Z
updated_at: 2026-05-02T20:16:28Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:pktlife6
  packet:
    - packet:ralph-ticket-pktlife6-20260502T201044Z
  critique:
    - critique:packet-lifecycle-parity-review
external_refs: {}
---

# Summary

Observed critique/wiki packet lifecycle parity before and after Ralph iteration
`packet:ralph-ticket-pktlife6-20260502T201044Z` for `ticket:pktlife6`.

# Procedure

- Read the active Ralph packet and ticket.
- Read the critique/wiki skills, critique/wiki packet templates, shared packet
  frontmatter reference, and shared status lifecycle reference.
- Captured before-state search output for `parent_merge_scope`, `compiled`,
  `consumed`, `superseded`, `abandoned`, `Parent Merge Notes`, and `Done Means`
  across the six product surfaces named by the packet.
- Updated the allowed product surfaces.
- Captured after-state lifecycle/template search output and ownership guardrail
  search output.
- Ran `git diff --check`.

# Artifacts

## Before-state lifecycle/template search

Command:

```bash
rg -n "parent_merge_scope|compiled|consumed|superseded|abandoned|Parent Merge Notes|Done Means" \
  "skills/loom-critique/SKILL.md" \
  "skills/loom-critique/templates/critique-packet.md" \
  "skills/loom-wiki/SKILL.md" \
  "skills/loom-wiki/templates/wiki-packet.md" \
  "skills/loom-records/references/packet-frontmatter.md" \
  "skills/loom-records/references/status-lifecycle.md"
```

Observed before edits:

- `skills/loom-critique/SKILL.md:100` and `skills/loom-wiki/SKILL.md:85` had
  `## Done Means`, but neither Done Means section mentioned parent merge notes or
  terminal packet status after packetized work.
- `skills/loom-critique/templates/critique-packet.md:24-26` and
  `skills/loom-wiki/templates/wiki-packet.md:19-21` had empty
  `parent_merge_scope` placeholders (`records: []`, `paths: []`).
- Both packet templates had `status: compiled` and `# Parent Merge Notes`, but
  no template-local mention of `consumed`, `superseded`, or `abandoned`.
- `skills/loom-records/references/packet-frontmatter.md` and
  `skills/loom-records/references/status-lifecycle.md` already defined shared
  packet lifecycle status values and parent merge note expectations.

## After-state lifecycle/template search

Command: same targeted `rg` search as above.

Observed after edits:

- Critique Done Means now mentions `# Parent Merge Notes` and terminal packet
  statuses at `skills/loom-critique/SKILL.md:107-114`.
- Wiki Done Means now mentions `# Parent Merge Notes` and terminal packet
  statuses at `skills/loom-wiki/SKILL.md:91-98`.
- Critique packet template now requires non-empty parent merge targets or explicit
  `None - <rationale>` at `skills/loom-critique/templates/critique-packet.md:24-32`
  and explains the rule at lines `71-74`.
- Wiki packet template now requires non-empty parent merge targets or explicit
  `None - <rationale>` at `skills/loom-wiki/templates/wiki-packet.md:19-27` and
  explains the rule at lines `58-60`.
- Critique packet output guidance now requires parent merge notes and a terminal
  packet lifecycle status at `skills/loom-critique/templates/critique-packet.md:157-160`.
- Wiki packet output guidance now requires parent merge notes and a terminal
  packet lifecycle status at `skills/loom-wiki/templates/wiki-packet.md:113-116`.
- Shared packet frontmatter now rejects empty `parent_merge_scope` and documents
  `None - <rationale>` at `skills/loom-records/references/packet-frontmatter.md:39-43`
  and `257-272`.
- Shared status lifecycle now states the packet lifecycle applies to Ralph,
  critique, and wiki packet families while preserving `packet_kind` workflow
  routing at `skills/loom-records/references/status-lifecycle.md:137-139`.

## Ownership and packetization guardrail search

Command:

```bash
rg -n "Ralph-governed|implementation packet|verification_posture|Do not compile a packet by default|decide whether the work merits a wiki packet|packet_kind: critique|packet_kind: wiki" \
  "skills/loom-critique/SKILL.md" \
  "skills/loom-critique/templates/critique-packet.md" \
  "skills/loom-wiki/SKILL.md" \
  "skills/loom-wiki/templates/wiki-packet.md" \
  "skills/loom-records/references/packet-frontmatter.md"
```

Observed:

- Critique and wiki packet templates still use `packet_kind: critique` and
  `packet_kind: wiki`.
- Critique and wiki skills still say their packets are not Ralph implementation
  packets and do not use Ralph `verification_posture`.
- Critique still says not to compile a packet by default for direct artifact
  critique; wiki still says to decide whether the work merits a wiki packet.
- Shared packet frontmatter still says critique/wiki packets may reuse packet
  discipline without becoming Ralph-governed.

## `git diff --check`

Result: passed; exit code 0 with no output.

# Supports Claims

- `initiative:skills-corpus-council-precision-pass#OBJ-006`
- `ticket:pktlife6#ACC-001`
- `ticket:pktlife6#ACC-002`
- `ticket:pktlife6#ACC-003`
- `ticket:pktlife6#ACC-004`

# Challenges Claims

None - this evidence does not falsify the targeted claims.

# Environment

Commit: `3b65266ffe67195bb548c8aa4a8e8db481fd92e1` baseline with expected active
ticket/packet setup edits
Branch: `main`
Runtime: Markdown/file-tool validation
OS: darwin
Relevant config: no network, no Git metadata mutation, no runtime schema helper

# Validity

Valid for: current diff for `ticket:pktlife6` after this Ralph iteration.
Recheck when: critique/wiki packet templates, packet lifecycle references, or
ticket acceptance claims change again.

# Limitations

This evidence is structural. It records lifecycle/template searches, ownership
guardrail searches, and diff sanity, not an oracle critique verdict. Mandatory
critique is recorded in `critique:packet-lifecycle-parity-review`.

# Result

The critique/wiki packet templates and skill guidance now require explicit parent
merge targets or rationale, parent merge notes, owner-layer reconciliation, and
terminal packet lifecycle status after packetized work, while preserving
critique/wiki ownership and optional packetization.

# Interpretation

The evidence supports ACC-001 through ACC-004. Oracle critique in
`critique:packet-lifecycle-parity-review` satisfies ACC-005.

# Related Records

- `ticket:pktlife6`
- `packet:ralph-ticket-pktlife6-20260502T201044Z`
- `critique:packet-lifecycle-parity-review`
