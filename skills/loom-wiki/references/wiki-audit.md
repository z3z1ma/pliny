# Wiki Audit

Wiki audit checks whether accepted explanation still matches accepted owner truth.

It surfaces maintenance debt. It should not silently rewrite substantive pages.

## Goals

- verify cited sources still exist
- check that page claims still match source records
- surface stale, duplicate, or overlapping pages
- surface policy or behavior-contract authority that leaked into wiki
- apply only low-risk mechanical fixes

## Classifications

- `current`: page is accurate and grounded
- `needs-update`: frame is still correct, but accepted owner truth or sources moved
- `stale`: page no longer matches accepted owner truth
- `duplicate`: page overlaps another page and should be merged
- `misplaced-authority`: page carries truth owned by constitution, spec, plan,
  ticket, or critique

## Procedure

1. Walk every page in scope.
2. Read frontmatter, cited sources, and major claims.
3. Compare claims to canonical owners and evidence.
4. Classify findings.
5. Apply only mechanical link or stale-marker fixes when obvious.
6. Route substantive rewrites to wiki write mode or the owning layer.

## Native Queries

```bash
find .loom/wiki -type f -name '*.md' | sort
rg -n '^(id|status|page_type):' .loom/wiki --glob '*.md'
rg -n '<term>' .loom/{wiki,research,specs,plans,tickets,critique,evidence} --glob '*.md'
```

## Output

- pages scanned
- findings table: page, classification, evidence, action
- mechanical fixes applied
- recommended next owner layer or workflow route per finding
