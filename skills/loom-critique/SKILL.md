---
name: loom-critique
description: "Run adversarial review as a first-class Loom layer. Use when code changes, behavior changes, Loom records, or other work products need pressure-testing against evidence before acceptance."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: owner-layer
  owns_layer: critique
---

# loom-critique

Critique is the adversarial review layer.

It applies to code changes and to Loom artifacts.
This skill exists so review has the same durability and rigor as execution.

## What This Skill Owns

- critique records
- critique packets
- findings and verdicts
- code review and artifact review
- direct artifact critique
- packetized implementation critique
- named critique profiles
- review severity and disposition
- follow-up pressure on tickets, specs, plans, and wiki pages

Critique owns findings and verdicts. Tickets own live execution state,
acceptance disposition, accepted risk, and closure.

Critique packets use `kind: packet` with `packet_kind: critique` under
`.loom/packets/critique/`. They are critique-owned review contracts, not Ralph
implementation packets, and they do not use Ralph `verification_posture` unless
this skill later defines a critique-specific field.

## Use This Skill When

- code changes need review before acceptance
- implementation claims need pressure-testing
- behavior changes need review against a spec or acceptance target
- Loom artifacts need review for owner-layer, scope, evidence, or clarity risk
- accepted-shape claims feel risky
- evidence may be weaker than the prose suggests
- the change class calls for review before acceptance
- a wiki page may be overstating certainty

## Do Not Use This Skill When

- the next move is clearly implementation
- you only need a tiny local sanity check
- you want to silently mutate the ticket instead of leaving a review record

## Critique Posture

Critique should be:

- skeptical but fair
- evidence-oriented
- explicit about severity and confidence
- durable enough for future agents to inspect

## Default Procedure

1. choose the review target
2. classify the review shape
3. choose critique profiles proportional to the risk
4. inspect the relevant diff, files, records, tests, evidence, and packet output
5. write findings with severity, confidence, and challenged claims when relevant
6. record the verdict and required follow-up
7. link the critique back to the target ticket and related artifacts

## Review Shapes

### Direct artifact critique

Use for reviewing a Loom artifact as an artifact: ticket clarity, plan
sequence, spec acceptance, packet quality, wiki certainty, evidence strength, or
external summary fidelity.

Do not compile a packet by default. Read the artifact, read enough owner context
to judge it, and write a critique record if the findings should persist.

### Packetized implementation critique

Use for reviewing code or behavior changes, especially after a Ralph iteration.

The parent normally compiles a critique packet that includes:

- target ticket
- parent plan or initiative
- relevant spec, research, and evidence
- prior Ralph packet output
- acceptance or claim coverage targets
- git diff or changed-file summary
- required critique profiles

The reviewer should use the packet and the diff as the main review surface.

## Done Means

- the review target is explicit
- the verdict is explicit
- the major findings are explicit
- code findings cite files or lines when practical
- follow-up implications are explicit

## Read In This Order

Read immediately for any substantive critique:

1. `references/critique-lens.md` when choosing review profiles or deciding what
   evidence the target type needs.
2. `references/review-pass-splitting.md` when the review may need multiple
   passes or when deciding direct artifact critique vs packetized
   implementation review.

Then read conditionally:

3. `references/finding-format.md` before writing durable findings or tracking
   finding dispositions.
4. `skills/loom-evidence/SKILL.md` when evidence strength, observed artifacts, or
   claim support/challenge need direct inspection.
5. `templates/critique.md` when creating a critique record.
6. `templates/critique-packet.md` only for packetized implementation/code
   review or high-risk fresh-context artifact review.
