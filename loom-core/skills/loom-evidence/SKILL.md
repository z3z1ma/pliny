---
name: loom-evidence
description: "Use when observations, validation outputs, reproductions, logs, screenshots, scans, command results, or artifact pointers should remain available for review or closure claims."
---

# loom-evidence

Evidence is Loom's observation surface.

It records what was seen, how it was seen, what source or record state was
observed, which claims the observation supports or challenges when applicable,
and what the observation does not show.

Evidence gives tickets, audits, research, specs, plans, and knowledge something
honest to reason from. Evidence does not decide acceptance, intended behavior,
policy, audit verdicts, or closure.

## Use This Skill When

Use this skill when:

- an observation should remain available beyond the current session
- ticket closure or review depends on a test, check, inspection, screenshot, log,
  scan, reproduction, artifact, or command result
- audit needs inspectable support or challenge for a claim
- research, specs, plans, tickets, or knowledge need durable observed artifacts
- raw artifacts exist and need a Markdown record that explains what they show
- future trust would be worse without preserving the observation

Small local checks can stay in a ticket journal when durable inspection is not
needed.

## Dispatch

If creating evidence:

- read `references/creating-evidence.md`
- read `references/evidence-quality.md`
- choose `templates/observation.md` for one observation
- choose `templates/dossier.md` when multiple observations compose one validation
  story
- link related records only when useful

If updating evidence:

- preserve the original observation when the record is a single observation
- add clarification, limitations, freshness notes, related records, or supersession
  prose when needed
- create a new evidence record for a new observation unless the record is an
  evidence dossier meant to accumulate multiple observations

If only finding or summarizing evidence:

- inspect `.loom/evidence/`
- report what the record says
- preserve the distinction between observation, inference, support, challenge, and
  acceptance

## Finding Evidence

Evidence records live under `.loom/evidence/`.

Useful starting points:

```bash
find .loom/evidence -maxdepth 1 -name '*.md' -print 2>/dev/null | sort
grep -R '^ID: evidence:' .loom/evidence 2>/dev/null || true
grep -R '^Type: Evidence' .loom/evidence 2>/dev/null || true
grep -R '^Observed:' .loom/evidence 2>/dev/null || true
grep -R 'ACC-[0-9][0-9][0-9]' .loom/evidence 2>/dev/null || true
```

Raw artifacts, when present, live under:

```text
.loom/evidence/artifacts/YYYYMMDD-<slug>/
```

The Markdown evidence record is still required. Raw artifacts and evidence records
are coupled when artifacts exist: the record points at the artifacts and explains
what they do and do not show.

## Evidence IDs And Filenames

Use `evidence:YYYYMMDD-<slug>` IDs.

Use matching filenames without the `evidence:` prefix:

```text
.loom/evidence/YYYYMMDD-<slug>.md
```

Use the actual current date. Do not copy example dates.

If the slug would collide, choose a clearer slug or add a numeric suffix.

## Record Shapes

Evidence has two shapes:

- `Type: Evidence Observation` for one observed check, artifact, reproduction, or
  result
- `Type: Evidence Dossier` when multiple observations compose one validation story

Use these labels near the top:

```text
ID: evidence:YYYYMMDD-<slug>
Type: Evidence Observation
Status: recorded
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Observed: YYYY-MM-DD or YYYY-MM-DD HH:MM UTC
```

For `Type: Evidence Dossier`, `Observed:` may be a date range when the dossier
spans multiple observations.

Use only `Status: recorded`.

Record freshness, invalidation, limitations, and supersession in prose.

## Evidence Invariants

Every evidence record should preserve these invariants:

- observation before inference
- enough procedure or source context to understand how the observation happened
- artifacts, paths, excerpts, or summaries sufficient to interpret the observation
- stable claim IDs in `## What This Shows` when claiming support or challenge
- explicit limits in `## What This Does Not Show`
- source state and procedure detail proportional to the claim risk
- redaction or omission of sensitive values
- no acceptance, closure, policy, behavior, or audit verdict claimed by evidence
  itself

Standalone evidence without claim links is allowed when the observation is worth
preserving. In that case, do not invent weak support or challenge links.

## Done Means

Evidence work is done when:

- the record says what was observed and how
- source state, procedure, artifacts, or excerpts are clear enough to interpret
- claim support or challenge uses stable IDs when present
- limitations prevent overclaiming
- freshness or recheck conditions are clear enough for the consuming surface
- related records can cite the evidence without treating observation as acceptance
  or policy
