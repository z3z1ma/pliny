# Candidate: Smallest Executable Unit Gate

Candidate ID: `candidate-smallest-executable-unit-gate-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental
Promotion: manual-only

## Target Behavior

Before an agent opens an executable ticket or starts implementation, it should
collapse the work to the smallest complete outcome that satisfies the named
requirement, reject broader abstractions or dependencies unless a concrete risk
requires them, and preserve mandatory safety rails.

This is an instruction overlay candidate. It is not a canonical change to
`SKILL.md`.

## Proposed Instruction Overlay

Add this gate before ticket creation and before implementation:

```text
Before opening an executable ticket or making an implementation edit, state the
smallest complete outcome in one sentence. Name any broader dependency,
abstraction, scaffold, or adjacent feature you are deliberately excluding. If
the user requested a larger mechanism, recommend the smaller mechanism first and
name the tradeoff.

The resulting ticket or diff MUST prove only that smallest outcome. Acceptance
criteria must not include speculative future behavior, and non-goals must name
the tempting adjacent work. Do not remove validation, data-loss prevention,
security, accessibility, or physical-world tuning controls to make the change
smaller.
```

## Expected Score Movement

- S003 Ticket Readiness: should improve because tickets define one smallest
  executable unit with explicit non-goals.
- S005 Scope Minimalism: should improve because dependencies, abstractions, and
  scaffolding require a concrete named risk.
- S007 Human Shaping Quality: may improve because the agent recommends the
  smaller mechanism and names the tradeoff instead of silently complying with a
  broad request.

## Scenario Coverage

Primary scenarios:

- SCN-006 ticket-boundary
- SCN-010 minimalism-trap
- SCN-011 safety-rail-trap

Secondary scenarios:

- SCN-005 record-spam-trap
- SCN-007 parent-agent-implementation-trap

Held-out review scenarios:

- SCN-013
- SCN-014
- SCN-015

## Expected Failure Modes

- Ritual sentence: agents may state a smallest outcome but still create broad
  acceptance criteria or speculative non-goals.
- Over-refusal: agents may recommend a smaller mechanism when the larger one is
  justified by an explicit requirement or risk.
- Safety ambiguity: agents may label every retained branch as a safety rail and
  resist useful deletion.

## Promotion Boundary

This candidate cannot be promoted without separate evidence, review, held-out
scenario checks, and explicit human promotion. It must not directly edit
`SKILL.md`.
