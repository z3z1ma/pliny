# Validation

Without bundled helper scripts, validation becomes an explicit operator behavior.

That is acceptable as long as it stays disciplined.

## Local Record Validation

Ask:

- does the frontmatter exist and parse visually
- are the common fields present
- are the major required sections present
- do the status and link choices make sense for the kind
- if the status is non-ticket, does it match `references/status-lifecycle.md`
- if claims are named, do coverage/support/challenge references use stable IDs
- do the filename and ID agree
- do saved `.loom` records and saved workspace/support metadata avoid unresolved
  template placeholders, example IDs, and generic TODO/TBD tokens unless the
  record explicitly documents them as observed source text

Intentional placeholders in `skills/**/templates` are template source, not saved
records. They are not failures of saved-record validation unless copied into a
saved `.loom` record without explicit observed-source-text framing.

## Graph Validation

Ask:

- does each linked record actually exist
- are there obvious broken refs
- did this rename or split leave stale pointers
- did a non-owner layer start carrying owner truth
- did an external reference become a competing ledger
- do evidence and critique records support or challenge the claims they name

## Fresh Claim Evidence

Before making a success, completion, fixed, passing, or ready-to-merge claim,
ask what evidence would prove that exact claim.

Good claim evidence names:

- the command, procedure, review, or observation used
- the observed result, including exit status, failure count, or relevant output
- when and where it was observed
- which claim, acceptance criterion, ticket, packet, or critique question it
  supports or challenges
- what the evidence does not establish

Evidence must be fresh enough for the claim being made. A previous run can be
valid if the ticket or evidence record says when it happened, what source state it
covered, and why no material change invalidated it. If freshness is uncertain,
rerun the check, record a limitation, or avoid the completion claim.

Do not accept these as evidence by themselves:

- a child worker saying "done"
- a test that was written after implementation without a red state when the
  packet required `test-first`
- a partial command used to imply a broader suite passed
- a stale run from before relevant files, records, dependencies, or environment
  changed
- confidence that a small change "should" work

## Spot-Check Recipes

### Missing IDs

```bash
rg --files-without-match '^id:' .loom --glob '.loom/{constitution,initiatives,research,specs,plans,tickets,critique,wiki,evidence,packets}/**/*.md'
```

### Missing status

```bash
rg --files-without-match '^status:' .loom --glob '.loom/{constitution,initiatives,research,specs,plans,tickets,critique,wiki,evidence,packets}/**/*.md'
```

### Saved-record placeholder leakage

```bash
rg -n '(<[^>[:cntrl:]]+>|\bTODO\b|\bTBD\b|[a-z]+:<[^>]+>|example:[a-z0-9-]+)' .loom --glob '.loom/{constitution,initiatives,research,specs,plans,tickets,critique,wiki,evidence,packets}/**/*.md'
```

Review every hit. A hit is a validation failure when it is an unresolved template
placeholder, example ID, or generic TODO/TBD token that leaked into saved project
truth. It is not a failure when the record explicitly documents the token as
observed source text, such as a quoted scan result, fixture excerpt, or external
example under review.

### Saved support placeholder leakage

```bash
rg -n '(<[^>[:cntrl:]]+>|\bTODO\b|\bTBD\b|[a-z]+:<[^>]+>|example:[a-z0-9-]+)' \
  .loom/workspace.md .loom/harness.md .loom/support 2>/dev/null
```

Support hits do not become canonical-truth failures, but unresolved placeholders
in workspace metadata, harness metadata, or saved support artifacts are still
routing and recovery failures until cleared or explicitly documented as observed
text.

### Status vocabulary spot check

```bash
rg -n '^status:' .loom/{constitution,initiatives,research,specs,plans,critique,wiki,evidence,packets} 2>/dev/null
```

Compare those values to `skills/loom-records/references/status-lifecycle.md`.

### Claim coverage spot check

```bash
rg -n '[a-z]+:[a-z0-9-]+#(REQ|ACC|CLAIM)-[0-9]{3}' .loom
```

For any important claim ID, search the ID directly and check that specs,
tickets, packets, evidence, and critique agree about its meaning.

### Files that mention a record but do not link it in frontmatter

Use this as a heuristic, not a rigid rule.
Sometimes prose mention is enough.

### Compare changed graph edges

```bash
git diff -- .loom
rg -n 'ticket:<token>|spec:<slug>|wiki:<slug>' .loom
```

## Evidence Records

If validation work itself matters later, preserve it as an evidence record.

Examples:

- a smoke test run
- a packet scope audit
- a migration sweep
- a manual comparison of linked records

## When To Escalate

Escalate instead of forcing closure when:

- broken references are widespread
- ownership is ambiguous
- the intended behavior and the implemented behavior disagree materially
- critique surfaced unresolved medium/high-severity issues
