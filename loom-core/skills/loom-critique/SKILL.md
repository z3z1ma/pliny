---
name: loom-critique
description: "Run adversarial review. Use for PR/diff/code/security/UX/API/performance/design review, or when behavior, records, evidence, risks, or acceptance claims need pressure-testing before acceptance."
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
- review severity and critique-owned finding state
- follow-up pressure on tickets, specs, plans, and wiki pages

## Naming

Create new direct critique records as `.loom/critique/<YYYYMMDD>-<slug>.md`.
The canonical ID remains `critique:<slug>` without the date prefix. Use the
record creation date for the filename prefix so critique records support temporal
discovery and future retention or cleanup decisions.

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

1. choose the review target and record it in the family-appropriate shape
2. classify the review shape
3. choose critique profiles proportional to the risk
4. inspect the relevant diff, files, records, tests, evidence, and packet output
5. write findings with severity, confidence, and challenged claims when relevant
6. record the verdict and required follow-up
7. link the critique back to the target ticket and related artifacts

For implementation review, read the verification story before the implementation
details when possible: tests, evidence, before/after observations, screenshots,
or performance numbers reveal what the author believes changed. Then inspect the
diff against correctness, simplicity, architecture, security/trust boundary,
performance, and owner-layer fit. Do not rubber-stamp because checks passed.

## Review Target Grammar

- Direct critique records use scalar `review_target` frontmatter: one
  grep-friendly record ref, path, PR, branch, commit, diff range, or concise
  target summary. Put longer target explanation in the `# Review Target` body
  section, not in nested frontmatter.
- Critique packets use structured `review_target` frontmatter because a bounded
  fresh-context review contract benefits from target type, stable reference, diff
  handle, and optional paths. Keep the packet `summary` field human-readable and
  grep-friendly.

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

## Common Rationalizations

- Rationalization: "LGTM is enough."
  - Reality: Durable critique needs target, evidence reviewed, verdict, residual risks, and findings or an explicit no-findings statement.
- Rationalization: "Tests passed, so critique should pass."
  - Reality: Tests are evidence. Critique reviews evidence sufficiency, scope, design, risks, and owner-layer truth.
- Rationalization: "Visual/product quality is taste."
  - Reality: Taste still has inspectable signals: primary task clarity, hierarchy, affordance, density, and before/after evidence.
- Rationalization: "The ticket can disposition findings later."
  - Reality: Critique owns findings and verdict now; tickets consume dispositions before closure.
- Rationalization: "External or subagent feedback is automatically right."
  - Reality: Review feedback is a claim to verify against project reality, specs, evidence, and code before implementing or rejecting it.

## Red Flags

- review target is vague or not tied to actual files, records, diff, or artifact
- critique summarizes implementer output without inspecting the source surface
- findings lack severity, confidence, or follow-up
- UI/product review ignores the baseline and primary user task
- mandatory critique is marked complete before final verdict and evidence review
- review feedback is implemented blindly without checking whether it is correct
  for this codebase, ticket scope, or owner-record truth

## Verification

- [ ] Review target and profiles are explicit.
- [ ] Actual files, records, tests, evidence, screenshots, or diffs were inspected.
- [ ] Findings have severity, confidence, and challenged claims when relevant.
- [ ] Residual risks and acceptance recommendation are explicit.
- [ ] Ticket-owned dispositions remain in the ticket, not the critique record.

## Done Means

- the review target is explicit
- the verdict is explicit
- the major findings are explicit
- code findings cite files or lines when practical
- follow-up implications are explicit
- when packetized critique used a critique packet, `# Parent Merge Notes` say how
  the reviewer output was reconciled into owner layers or why it was rejected
- owner-layer reconciliation is explicit: critique owns findings and verdicts,
  tickets own live execution state and acceptance disposition, and evidence/wiki
  receive only the truths their layers own
- after parent reconciliation of a used critique packet, packet `status` is moved
  from `compiled` to the truthful terminal packet status: `consumed`,
  `superseded`, or `abandoned`

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
