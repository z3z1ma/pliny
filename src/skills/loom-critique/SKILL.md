---
name: loom-critique
description: First-class Loom review skill for durable adversarial critique, review packets, explicit verdicts, audits, risk analysis, and structured findings with severity, confidence, and follow-up action. Use when code, docs, packets, or workflow changes need durable review before acceptance. Not for implementation, optimistic self-review, or silent execution-ledger mutation.
compatibility: Designed for this Markdown-first Loom repository. Assumes repository-local scripts, canonical Markdown records, and harness-agnostic child launches resolved through `.loom/harness.md` profiles, harness self-discovery, or operator guidance.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: review
---

# loom-critique

Critique is the first-class Loom review layer.

Use this skill when work must survive beyond the current chat and be judged adversarially against its contract, broader project context, and likely failure modes.

Treat critique as durable review, not inline self-congratulation.

## Use This Skill When

- a result needs adversarial review before acceptance
- a packet output, docs claim, or system shape feels risky enough to pressure-test
- you need durable verdict and findings rather than transient chat review

## Do Not Use This Skill When

- the next step is implementation rather than review
- the work only needs a lightweight local sanity check
- you are trying to silently mutate execution truth instead of reviewing it

## What This Skill Governs

- critique records
- critique findings
- critique packet artifacts
- critique outcomes

## Critique Is Distinct From Neighboring Loom Layers

- Ralph may call critique repeatedly, but critique is still its own durable review layer
- tickets remain the live execution ledger
- docs remain the explanatory layer after accepted reality is known
- critique findings and verdicts should remain useful whether or not a Ralph loop is active

## Default Critique Posture

- assume plausible output may still be wrong
- look for hidden flaws, unsafe assumptions, missing tests, edge cases, architectural drift, and unsupported claims
- name residual risk explicitly
- preserve findings durably instead of leaving them in chat
- write verdicts and findings that show the reasoning chain, not just the conclusion

## Before You Review

1. read the target artifact first so the review question is anchored in real material
2. define the exact review question before creating critique state
3. decide whether this needs only local review or a fresh-context packetized critique run
4. resolve repository ownership if the review spans multiple surfaces

## Execution Playbook

1. create a critique record when the review needs a durable home for verdict and findings
2. if you create one, populate review question, focus areas, relevant context, and evidence reviewed immediately
3. compile a packet only when a fresh child review run is actually needed
4. link reviewed artifacts, follow-up work, and verification evidence after the review shape is clear
5. create verification records for supporting checks or run outputs when those should be durable
6. validate the critique record and the surrounding graph before calling the review complete

## Finding Quality Bar

A good finding answers all of these:

1. what is the problem
2. why it matters
3. what evidence supports it
4. how severe it is
5. how confident the reviewer is
6. what action should follow

If a launched critique lands no durable review state, treat that as a failed critique pass rather than as a successful review.

## How To Use The Scripts

Read `references/scripts.md` for the bundled CLI surface, including argument meanings and example invocations.

- `create_critique.py`: use when the review needs a durable critique record in `.loom/critique/`
- `create_critique.py`: after running it, populate the review body immediately; the script only creates the shell
- `compile_packet.py`: use when a bounded fresh-context critique run is required
- `link_records.py`: use to add or remove reviewed-artifact, follow-up, and verification refs after the body is real
- `create_verification.py`: use when the critique run or its supporting checks produce durable evidence
- `validate_record.py`: use before trusting the review result as durable
- `check_links.py`: use to confirm graph integrity across reviewed artifacts and follow-up refs
- `resolve_scope.py`: use before compiling a review set with ambiguous ownership

## What Good Looks Like

- the review question is bounded
- findings are actionable and evidence-backed
- the verdict is explicit
- residual risks are named rather than implied
- follow-up actions are obvious to the next actor

## Failure Conditions

Treat critique as failed or incomplete when:

- the review returns a verdict without evidence-backed reasoning
- no durable critique run or findings land after a launched review
- findings stay vague or unactionable
- the review silently mutates execution truth instead of producing durable review artifacts

## Done Means

- the critique record captures a bounded review question and a real verdict
- findings are durable, evidence-backed, and actionable
- follow-up refs and verification refs are explicit where needed
- `validate_record.py` passes and `check_links.py` does not surface unresolved graph problems

## Read In This Order

1. `references/critique-invocation.md`
2. `references/schema-critique.md`
3. `references/scripts.md`
4. `references/examples.md`

## References

- `references/schema-critique.md`
- `references/critique-invocation.md`
- `references/scripts.md`
- `references/examples.md`
