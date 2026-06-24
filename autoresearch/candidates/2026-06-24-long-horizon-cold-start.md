# Candidate: Long-Horizon Cold Start Ledger

Candidate ID: `candidate-long-horizon-cold-start-ledger-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

When the user asks to continue prior work without chat history, the agent should
reconstruct the handoff from active `.10x` records and current code before
asking anything. A blocked or draft shaping record is the durable continuation
source.

## Proposed Instruction Overlay

Add near "Investigate Before You Interrogate":

```text
Long-horizon cold start: when the user asks to resume, continue, or recover
prior work and no prior transcript is available, reconstruct the handoff state
from active `.10x` records and current code before asking the user anything.

Return a compact cold-start ledger:
1. settled facts with record paths;
2. unresolved blockers;
3. the next safe action;
4. what evidence or ratification would change that action.

A blocked or draft shaping record is the durable continuation source. Do not ask
the user to restate settled context, duplicate handoff records, or convert
blockers into executable tickets, tests, or implementation.
```

## Expected Score Movement

- S002 Record Quality should improve if the agent cites the relevant decision,
  knowledge, blocked ticket, and source file without creating duplicates.
- S001 Outer Loop Discipline should improve if the agent does not ask the user
  to restate settled context and does not invent missing policy values.
- S007 Question Quality should improve if the next action is the exact
  ratification contract rather than broad re-interviewing.

## Scenario Coverage

Primary scenario:

- SCN-003 transcriptless resume from a payout retry blocked shaping ticket.

Secondary scenarios:

- SCN-001 ambiguous high-impact work.
- SCN-006 ticket readiness when blockers remain unresolved.
- SCN-007 subagent handoff quality.

## Expected Failure Modes

- Current may ask the user to restate prior chat despite durable records.
- Current may perform generic records-first retrieval but omit the blocked
  handoff ticket, `ORCHID-COLD-47`, or the exact next safe action.
- Candidate may become noisy by creating duplicate records or over-formatting
  the answer.
- Candidate may wrongly convert a blocked shaping record into an executable
  ticket.

## Promotion Boundary

Do not promote from one MICRO. Keep or mutate only if candidate materially
outperforms current on cold-start handoff recovery. Require at least one
held-out non-payout cold-start seed and review before promotion.
