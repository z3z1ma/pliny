# Semantic Link Usage

Typed `links:` are navigation adjacency, not a dumping ground for every
semantic relationship.

Use the most specific section available before falling back to generic links.

## Where Relationships Belong

- Hard execution prerequisite: use `depends_on`.
- Ticket implements or verifies spec acceptance: use `# Acceptance`.
- Ticket acceptance view over claims: use optional `# Claim Matrix`.
- Packet iteration target claims: use `# Verification Targets`.
- Evidence supports a claim: use `# Supports Claims`.
- Evidence weakens or falsifies a claim: use `# Challenges Claims`.
- Critique challenges a claim: use finding `Challenges:`.
- Ticket-owned finding disposition / ticket-owned critique disposition: use
  `# Review And Follow-Through`.
- Superseded record: use record lifecycle `status: superseded` plus successor in
  `links:` or body prose.
- Superseded claim or criterion ID: use owning record prose, optional claim
  matrix, or acceptance state naming the successor ID.
- Accepted risk: use ticket `# Claim Matrix`, ticket acceptance notes,
  review/follow-through notes, or acceptance decision.
- Follow-up ticket: use ticket body follow-up section plus `links:` to the
  related owner records.
- Related ticket with no dependency: use `links:` typed adjacency, not
  `depends_on`.
- Promotion from memory/research/ticket into wiki/spec/etc.: use body prose
  naming source and target, plus `links:` when navigation matters.
- Outside mirrors or requests: use `external_refs`.
- Source records for accepted explanation: use wiki source sections and `links:`.
- Ordinary navigation adjacency: use `links:`.

## Generic Links

Use `links:` for durable adjacency a future agent should navigate:

```yaml
links:
  spec:
    - spec:<slug>
  evidence:
    - evidence:<slug>
```

Replace placeholder refs with real record IDs before saving a real record.

Do not force relationship verbs into frontmatter unless the project has a
stable need. Plain typed adjacency plus specialized sections is enough for most
workspaces.

### Common Semantic Relationships

- Record supersession must name what replaced the old record, either with
  lifecycle `status: superseded` plus a successor in `links:` or in a clear body
  section. Do not leave agents guessing which record to trust next.
- Claim or criterion ID supersession is narrower than record supersession. Mark
  the old `REQ-*`, `ACC-*`, `OBJ-*`, or `CLAIM-*` as superseded in the owning
  record's prose, optional claim matrix, or acceptance state and name the successor ID. Do
  not imply the whole record should have `status: superseded` unless the record
  itself has been replaced.
- Promotion should name the source support or working artifact and the canonical
  owner that now holds the durable truth. Memory may keep a pointer, but the
  promoted owner wins.
- Related tickets belong in `links:` or a ticket body section when they are useful
  adjacency. Use `depends_on` only for a hard execution prerequisite.
- Follow-up tickets should be explicit ticket references, ideally with the reason
  for follow-up. A critique finding or accepted risk can point to the follow-up,
  but the ticket ledger owns live execution state.
- Accepted risk should stay visible in the ticket acceptance, optional claim
  matrix, review/follow-through notes, or acceptance decision. Do not hide
  accepted risk only in a generic link.

## External References As Support Surfaces

Use `external_refs:` for outside systems, external documents, releases, issues,
pull requests, URLs, dashboards, generated context files, harness artifacts, or
package surfaces that help explain provenance or navigation. External refs are
graph aids and support surfaces. They can request, mirror, package, or navigate
Loom work, but they do not own live state, intended behavior, evidence
sufficiency, critique verdicts, or closure unless a constitution record says so.

When an external surface changes, reconcile the Loom owner that owns the fact;
then update the external mirror if useful. Do not treat issue tracker recency,
PR text, dashboard state, generated context, or package metadata as newer truth
than the relevant ticket, spec, evidence, critique, wiki, or constitution record.

## Anti-Patterns

Do not:

- use `links:` instead of `depends_on` for hard execution prerequisites
- bury evidence support only in prose
- bury ticket-owned finding disposition only in prose
- copy outside issue tracker state into `links:`
- let `external_refs:` become a shadow ticket ledger
- use PRs, dashboards, generated context, or release metadata as shadow closure
- make `links:` a substitute for the acceptance dossier
