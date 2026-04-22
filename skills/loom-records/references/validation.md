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

## Graph Validation

Ask:

- does each linked record actually exist
- are there obvious broken refs
- did this rename or split leave stale pointers
- did a non-owner layer start carrying owner truth
- did an external reference become a competing ledger
- do evidence and critique records support or challenge the claims they name

## Spot-Check Recipes

### Missing IDs

```bash
rg -L '^id:' .loom --glob '*.md'
```

### Missing status

```bash
rg -L '^status:' .loom --glob '*.md'
```

### Status vocabulary spot check

```bash
rg -n '^status:' .loom/{constitution,initiatives,research,specs,plans,critique,wiki,evidence,packets} 2>/dev/null
```

Compare those values to `skills/loom-records/references/status-lifecycle.md`.

### Claim coverage spot check

```bash
rg -n 'REQ-[0-9]{3}|ACC-[0-9]{3}|CLAIM-[0-9]{3}' .loom
```

For any important claim ID, search the ID directly and check that specs,
tickets, packets, evidence, and critique agree about its meaning.

### Files that mention a record but do not link it in frontmatter

Use this as a heuristic, not a rigid rule.
Sometimes prose mention is enough.

### Compare changed graph edges

```bash
git diff -- .loom
rg -n 'ticket:abcd1234|spec:packet-discipline|wiki:ralph' .loom
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
