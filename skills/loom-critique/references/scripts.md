# Critique Script Reference

Use package-local script paths from this skill bundle.

The examples below assume invocation through `scripts/critique.py` inside `loom-critique`.

## Direct Critique Query Ideas

The bundled CLI creates critique records, critique packets, links, and verification artifacts.

The queries below are examples, not a canonical command surface. Use them as portable patterns when you need to inspect `.loom/critique/`, `.loom/runs/critique/`, and critique-linked verification directly.

Critique records by state and recency:

```bash
rg -n '"status":\s*"(active|revised|superseded)"|"updated_at":' .loom/critique/*.md
```

Critique sections that usually determine what to do next:

```bash
rg -n '^# (Verdict|Residual Risks|Follow-up Tickets|Evidence Reviewed)$' .loom/critique/*.md
```

Everything that references critique records downstream:

```bash
rg -n 'critique:' .loom/{tickets,plans,specs,docs,verification,runs}
```

Compiled critique packets that may still need reconciliation:

```bash
rg -n '"status":\s*"compiled"|"generated_at":|"ref":' .loom/runs/critique/*.md
```

## `scripts/critique.py create`

Purpose:

- create a critique record scaffold under `.loom/critique/`

Example:

```bash
scripts/critique.py create review-ticket-0002 --link ticket=ticket:0002
```

## `scripts/critique.py packet`

Purpose:

- scaffold a critique packet record under `.loom/runs/critique/`
- pair with a parent-supplied launch prompt that tells the child what review lens or emphasis to apply

Example:

```bash
scripts/critique.py packet "ticket:0002" critique --mode review-only --style reference-first
```

Common pattern after packet creation:

```text
Run a bounded critique from the supplied packet. Use a verifier-style lens: focus on whether the ticket's claims are actually supported by the cited evidence, and call out where confidence is stronger than the proof warrants.
```

## `scripts/critique.py link`

Purpose:

- add or remove reviewed-artifact, follow-up, or verification links on a critique record

Example:

```bash
scripts/critique.py link "critique:review-ticket-0002" --add "doc:admin-query-contract-reference"
```

## `scripts/critique.py verify`

Purpose:

- create verification evidence for critique-supporting checks or review runs

Example:

```bash
scripts/critique.py verify critique-ticket-0002-evidence --link "critique:review-ticket-0002"
