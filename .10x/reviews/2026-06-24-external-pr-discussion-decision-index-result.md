Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Target: .10x/research/2026-06-24-external-pr-discussion-decision-index-scn004-live-micro.md
Verdict: concerns

# External PR Discussion Decision Index Result Review

## Target

`.10x/research/2026-06-24-external-pr-discussion-decision-index-scn004-live-micro.md`
and raw artifacts under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/129-external-pr-discussion-decision-index-scn004-live-micro/`.

## Findings

- pass: Current created the correct decision-class `.10x/decisions/` record.
- pass: Current captured the accepted `provider_delivery_id` decision and the
  rejected `event_id` alternative without copying the whole PR thread.
- pass: Current avoided source edits and implementation-ticket creation.
- concern: Current omitted available external provenance fields: canonical URL,
  thread id, observed PR status, and export timestamp.
- concern: The duplicate-current arm included the canonical URL, showing the
  omission is stochastic rather than impossible under current `SKILL.md`, but it
  still did not fully preserve status/thread metadata.
- concern: The existing broad phrase "durable pointer" may be too underspecified
  for heterogeneous external artifacts such as PR discussions, Jira issues, and
  exported design-doc revisions.

## Verdict

Concerns. Current passed the record-type and economy behavior but fell short of
the stated provenance quality floor.

## Residual Risk

A targeted candidate should test whether adding compact provenance-field
language improves external artifact index quality without causing wholesale
copying or over-applying thin-index behavior when local `.10x` is explicitly
made canonical.
