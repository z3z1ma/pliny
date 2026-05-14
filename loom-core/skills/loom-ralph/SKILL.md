---
name: loom-ralph
description: "Use when Loom work needs a Ralph packet for a bounded subagent, harness run, implementation slice, review pass, or worker handoff built from records, files, evidence, claims, or other bounded context."
---

# loom-ralph

Ralph is Loom's packetized worker technique.

A Ralph packet gathers the context for one bounded worker run, adds packet labels,
names the target and launch transport, and gives the worker a clear mission, read
scope, write scope, stop conditions, and output contract.

Most Ralph runs use a harness-native subagent. A Ralph packet can also be handed to
a headless harness command or another transport that reads the packet and returns
the required output. Regardless of transport, the launch points to the packet path
and requests the packet's output contract.

Ralph supplies packet mechanics. The consuming surface still records the judgment,
state, or durable result it owns. Tickets may use Ralph for implementation, audit
may use Ralph for adversarial review, and other Loom surfaces may use Ralph when
bounded worker execution improves the work.

A Ralph run has two parts: an on-disk packet under `.loom/packets/ralph/` and the
launch transport that points the worker at that packet. The packet is the worker
contract. The launch wrapper should stay thin so future agents can inspect the
handoff from the repository graph.

## Use This Skill When

Use this skill when:

- creating a packet from Loom records, files, evidence, diffs, claims, or external
  references
- choosing live-reference, hermetic, or hybrid context packaging
- launching a bounded subagent or harness run from a packet
- defining read scope, write scope, stop conditions, or worker output
- updating packet status or worker output
- deciding whether packet context is current enough to run
- finding or summarizing packet state

Shape the work before packetizing it. A Ralph packet should begin from a clear
target, mission, context boundary, write boundary, and output expectation.

## Dispatch

If creating a packet:

- read `references/packet-shape.md`
- read `references/running-packets.md`
- read `references/verification-posture.md` when the packet needs implementation
  or validation evidence
- read the records and source material needed to bind the packet context
- use `templates/packet.md`
- write a packet narrow enough for one worker run
- when launching, point the worker at the packet path and the packet's output
  contract

If executing from a packet:

- read the whole packet before editing or reviewing
- read live references or inlined context according to `Context Style:`
- stay inside the declared read scope and write scope
- update the records named by the packet when those updates are part of the worker
  contract
- stop when a stop condition applies
- return the required worker output

If reading worker output after a packet:

- read the packet, worker output, changed records, evidence, and changed files
- update the consuming surface when additional judgment or routing is needed
- decide whether the next move is another packet, audit, closure, shaping,
  knowledge promotion, or another Loom surface

If only finding or summarizing packets:

- inspect `.loom/packets/`
- report packet status, target, mode, context style, and visible next move without
  changing records unless the operator asked for a change

## Finding Packets

Ralph packets live under:

```text
.loom/packets/ralph/
```

Useful starting points:

```bash
find .loom/packets/ralph -name '*.md' -print 2>/dev/null | sort
grep -R '^ID: packet:' .loom/packets/ralph 2>/dev/null || true
grep -R '^Type: Packet' .loom/packets/ralph 2>/dev/null || true
grep -R '^Status:' .loom/packets/ralph 2>/dev/null || true
grep -R '^Target:' .loom/packets/ralph 2>/dev/null || true
grep -R '^Mode:' .loom/packets/ralph 2>/dev/null || true
grep -R '^Context Style:' .loom/packets/ralph 2>/dev/null || true
```

## Packet IDs And Filenames

Packets use compact UTC timestamps; several may be created on the same day.

Use this ID shape:

```text
packet:YYYYMMDDTHHMMSSZ-<target-or-task-slug>
```

Use matching filenames without the `packet:` prefix:

```text
.loom/packets/ralph/YYYYMMDDTHHMMSSZ-<target-or-task-slug>.md
```

Use the actual current UTC timestamp. Do not copy example timestamps.

Choose a slug that helps future agents find the packet by target, task, or run
purpose.

## Required Top Labels

Packets use plain body labels near the top:

```text
ID: packet:YYYYMMDDTHHMMSSZ-<target-or-task-slug>
Type: Packet
Status: compiled
Created: YYYY-MM-DD HH:MM UTC
Updated: YYYY-MM-DD HH:MM UTC
Target: record ID, claim, path, diff, branch, package, or task slug
Packet Kind: Ralph
Mode: execution|review|research|synthesis|other
Context Style: live-reference|hermetic|hybrid
Worker: subagent|harness command|manual handoff
Branch: branch name, none, or unknown - reason
Worktree: path, none, or unknown - reason
```

Add only when useful:

```text
Iteration: positive integer or run label
Risk: low|medium|high - reason
Verification Posture: test-first|observation-first|none
Review Lens: audit, code review, evidence sufficiency, or another lens
Change Class: short label or prose
```

## Status Lifecycle

Use this lifecycle:

- `compiled`: packet is ready for launch and no worker has started from it
- `running`: a worker launch has started and output has not yet been recorded
- `consumed`: worker output was recorded and the packet has been used
- `superseded`: target, context, scope, source state, or assumptions changed enough
  that another packet replaces it
- `abandoned`: packet will not be launched and no successor is intended

Packet status describes the packet only. The consuming surface records its own
execution state, findings, evidence sufficiency, acceptance, closure, or knowledge
updates.

## Context Styles

Use one of these context styles:

- `live-reference`: the packet names the records, files, evidence, diffs, or
  external references the worker should read in the workspace
- `hermetic`: the packet inlines the relevant record text, excerpts, diffs, or
  artifacts needed for the run
- `hybrid`: the packet inlines the critical context and also points at live sources
  for inspection

Live-reference packets are useful when current workspace state matters. Hermetic
packets are useful when a worker should review a frozen context bundle.

## Worker Outcomes

The worker returns one outcome:

- `continue`: useful progress happened and another packet is likely
- `stop`: this packet's work is complete
- `blocked`: a concrete blocker prevents safe progress
- `escalate`: the next move needs higher-level shaping, policy, review, or another
  Loom surface

Worker outcome is packet output. The consuming surface decides what that outcome
means for its own record.

## Packet Invariants

Every Ralph packet should preserve these invariants:

- explicit target or target set
- one bounded worker run
- context packaged as live references, hermetic content, or a deliberate hybrid
- clear mission and output contract
- explicit read scope and write scope
- worker permission to update only the records, files, and evidence artifacts named
  by the packet
- worker output recorded durably when the result supports closure, acceptance,
  evidence, audit, research, knowledge, or future recovery
- branch and worktree named when repository files may change
- evidence, review, or verification expectation appropriate to the mode
- stop conditions that fail closed instead of widening scope
- worker output sufficient for the next agent to continue, inspect, or review
- no secret, credential, private key, token, password, or sensitive personal data
- no stale packet used after the target, scope, context, or assumptions changed

## Done Means

Ralph work is done when:

- the packet is compiled, consumed, superseded, or abandoned truthfully
- the worker stayed inside the packet boundary or stopped when it could not
- named record and evidence updates were made or explicitly reported as missing
- worker output states what happened, what changed, what was observed, what remains
  unverified, and what next move is recommended
- the consuming surface can use the packet output without replaying the worker's
  tool log
