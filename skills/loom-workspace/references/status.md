# Workspace Status Reference

## Purpose

Status gives the parent agent a compact view of current canonical state.

## What A Status View Should Show

At minimum, a useful status view should summarize the workspace from canonical records and include counts by kind and status where useful.

That summary is most useful when the parent wants to know:

- what kinds of records currently exist
- whether execution work is concentrated in tickets, critique, docs, or elsewhere
- whether a subsystem appears missing or unexpectedly empty

Status is an orientation tool. It should help the parent decide what to read next, not pretend to replace the underlying records.

## What Status Does Not Tell You

Status usually does not tell you:

- whether a specific record body is strong or weak
- whether links are healthy
- whether a packet is fresh enough to reuse
- whether one active ticket actually owns the work you care about

Use status for orientation, then read the owning artifacts directly.

## How To Use It

Use status to orient yourself before reading specific records. Then follow up by reading the owning canonical artifacts directly.

If status suggests something surprising, trust the records over the summary and investigate the owning artifacts directly.

Good follow-up moves after status are often:

- read the active ticket if work seems execution-heavy
- read the active critique if review seems to be gating progress
- read the governing spec or plan if behavior or sequencing questions dominate
- inspect the workspace directly if the summary looks suspiciously sparse or inconsistent

## Worked Example

Parent question:

```text
I just entered the workspace. Where is active work concentrated, and which artifact family should I read first?
```

Good use:

- read the compact status view
- notice whether activity clusters in tickets, critique, docs, or planning
- read the owning canonical records directly before taking action

## Anti-Pattern

```text
Status shows three active tickets, so I already understand the current work.
```

Why this is weak:

- status only summarizes counts and distribution
- the actual execution truth still lives in the underlying records
