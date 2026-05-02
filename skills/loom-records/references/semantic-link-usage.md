# Semantic Link Usage

Typed `links:` are navigation adjacency, not a dumping ground for every
semantic relationship.

Use the most specific section available before falling back to generic links.

## Where Relationships Belong

| Relationship | Use |
| --- | --- |
| hard execution prerequisite | `depends_on` |
| ticket implements or verifies spec acceptance | `# Coverage` |
| ticket acceptance view over claims | `# Claim Matrix` |
| packet iteration target claims | `# Verification Targets` |
| evidence supports a claim | `# Supports Claims` |
| evidence weakens or falsifies a claim | `# Challenges Claims` |
| critique challenges a claim | finding `Challenges:` |
| critique finding state on a ticket | `# Critique Disposition` |
| superseded record | record lifecycle `status: superseded` plus successor in `links:` or body prose |
| superseded claim or criterion ID | owning record prose, claim matrix, or coverage state naming the successor ID |
| accepted risk | ticket `# Claim Matrix`, ticket acceptance notes, or critique disposition |
| follow-up ticket | ticket body follow-up section plus `links:` to the related owner records |
| related ticket with no dependency | `links:` typed adjacency, not `depends_on` |
| promotion from memory/research/ticket into wiki/spec/etc. | body prose naming source and target, plus `links:` when navigation matters |
| outside mirrors or requests | `external_refs` |
| source records for accepted explanation | wiki source sections and `links:` |
| ordinary navigation adjacency | `links:` |

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
  record's prose, claim matrix, or coverage state and name the successor ID. Do
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
- Accepted risk should stay visible in the ticket acceptance or claim matrix and,
  when applicable, in critique disposition. Do not hide accepted risk only in a
  generic link.

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
- bury critique finding disposition only in prose
- copy outside issue tracker state into `links:`
- let `external_refs:` become a shadow ticket ledger
- use PRs, dashboards, generated context, or release metadata as shadow closure
- make `links:` a substitute for the acceptance dossier
