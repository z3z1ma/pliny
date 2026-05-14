---
name: loom-audit
description: "Use when claims, code changes, Loom records, evidence, risks, acceptance, or follow-through need Ralph-backed adversarial review before they can be trusted."
---

# loom-audit

Audit is Loom's adversarial review record surface for Ralph-backed review
judgments.

It records what was reviewed, what claims or risks were challenged, what context
and evidence were inspected, what findings were produced, what verdict the auditor
reached, and what must happen before the consuming surface can honestly proceed.

Audit surfaces weak claims, missing evidence, scope drift, and unresolved risk.

Audit does not own intended behavior, ticket closure, risk acceptance, policy,
implementation, evidence, or finding disposition. It gives the consuming surfaces
an adversarial judgment to use.

## Use This Skill When

Use this skill when:

- ticket work has reached the point where implementation and evidence need an
  independent pass before closure
- a ticket, plan, spec, research conclusion, evidence record, constitution change,
  code change, diff, pull request, package, or handoff needs adversarial review
- acceptance or closure depends on claims that could be overstated
- evidence may be partial, stale, missing, or weaker than the prose suggests
- implementation may not match intended behavior, acceptance, or scope
- risk is broad, subtle, user-facing, security-relevant, architecture-affecting,
  policy-affecting, expensive to reverse, or likely to mislead future agents
- review findings should remain available beyond the current session

Tiny local sanity checks are not audit. Use audit when independent adversarial
judgment would materially improve trust, acceptance, recovery, or follow-through.
Tickets are the most common audit consumer, but audit can target any Loom surface
with claims worth challenging.

## Ralph Review Requirement

Substantive audit requires a Ralph review packet.

The context that shaped or implemented the target may prepare the audit request,
gather bounded context, and record the result. The adversarial judgment itself
must come from the Ralph review run.

Route the bounded review through an on-disk Ralph packet under
`.loom/packets/ralph/`. The packet is the audit request and worker contract. Audit
records the adversarial judgment after the Ralph review run returns.

When a Ralph review cannot be run, say audit was not performed. Local inspection
may still be useful review, but do not save it as `Type: Audit`.

## Dispatch

If preparing or recording an audit:

- read `references/audit-shape.md`
- read `references/audit-lenses.md`
- read `references/findings-and-verdicts.md`
- identify the concrete target
- identify the claims, risks, acceptance criteria, or review concerns being
  challenged
- gather only the context needed for a bounded Ralph review packet
- prefer source records, diffs, evidence, and files over summaries when the source
  is needed for judgment
- compile and launch a Ralph review packet for substantive audit
- after the Ralph review run, record the result with `templates/audit.md`

If consuming audit findings:

- read the full audit record
- inspect cited files, records, evidence, claims, or findings before acting
- treat findings as claims to verify, not commands to obey blindly
- route fixes, risk acceptance, follow-up tickets, spec changes, evidence updates,
  or operator decisions to the surface that owns them
- keep ticket acceptance, finding disposition, and closure decisions in tickets

If only finding or summarizing audits:

- inspect `.loom/audit/`
- report what the audit says
- preserve the distinction between audit verdict, acceptance, closure, policy, and
  implemented disposition

## Finding Audits

Audit records live under `.loom/audit/`.

Useful starting points:

```bash
find .loom/audit -maxdepth 1 -name '*.md' -print 2>/dev/null | sort
grep -R '^ID: audit:' .loom/audit 2>/dev/null || true
grep -R '^Type: Audit' .loom/audit 2>/dev/null || true
grep -R '^Status: recorded' .loom/audit 2>/dev/null || true
grep -R '^Target:' .loom/audit 2>/dev/null || true
grep -R 'FIND-[0-9][0-9][0-9]' .loom/audit 2>/dev/null || true
```

## Audit IDs And Filenames

Use `audit:YYYYMMDD-<slug>` IDs.

Use matching filenames without the `audit:` prefix:

```text
.loom/audit/YYYYMMDD-<slug>.md
```

Use the actual current date. Do not copy example dates.

If the slug would collide, choose a clearer slug or add a numeric suffix.

## Record Shape

Audit has one record shape:

- `Type: Audit`

Use these labels near the top:

```text
ID: audit:YYYYMMDD-<slug>
Type: Audit
Status: recorded
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Audited: YYYY-MM-DD or YYYY-MM-DD HH:MM UTC
Target: ticket:YYYYMMDD-<slug> or path/ref/claim
```

Use only `Status: recorded`.

Audit is an adversarial pass, not a live execution state. Supersession,
invalidation, follow-up, and stale-context notes belong in prose.

`Target:` should be a short grepable handle. Put longer target explanation in the
body.

## Audit Invariants

Every audit record should preserve these invariants:

- Ralph review was performed
- target is explicit and grepable
- audited claims, risks, or review concerns are clear
- reviewed context, files, records, diffs, claims, and evidence are named enough
  to understand the pass
- lenses or review concerns are visible
- material findings have stable `FIND-*` IDs
- verdict explains the auditor's judgment without claiming acceptance or closure
- required follow-up and residual risk are explicit
- ticket-owned dispositions remain in tickets
- evidence remains observation, research remains investigation, specs remain
  intended behavior, and constitution remains durable judgment

## Done Means

Audit work is done when:

- the target and Ralph review boundary are clear
- the audit says what was inspected and what was not inspected
- findings are concrete enough to act on or intentionally absent
- the verdict is bounded by the reviewed context and evidence
- follow-up and residual risk are visible
- consuming surfaces can cite the audit without treating it as the owner of
  acceptance, closure, implementation, policy, evidence, or intended behavior
