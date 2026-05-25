# Loom Protocol Compression

ID: spec:loom-protocol-compression
Type: Spec
Status: active
Created: 2026-05-25
Updated: 2026-05-25

## Summary

This spec defines how the model-visible Loom protocol should be compressed. Downstream tickets should cite it when rewriting Core skills, references, agent prompts, Playbooks, docs, or preload surfaces so the result is smaller without losing protocol behavior.

## Product Slice

This spec owns the compression contract for Loom's portable protocol surfaces: shipped skills, skill references, intentionally model-visible agent prompts, and human docs that restate those behaviors.

It does not own Loom Mill UX, harness subprocess mechanics, record storage, package layout, adapter installation, or the exact implementation edits for any slice.

## Spec Set Coverage

This spec fills the behavior gap created by `constitution:main` and `roadmap:loom-mill`: the protocol should become a sharp portable kernel before Loom Mill builds on it.

Adjacent behavior outside this spec:

- `spec:ticket-owned-worker-handoffs` owns worker and review handoff behavior.
- `spec:loom-driver-agent` owns Driver behavior.
- `spec:loom-weaver-agent` owns Weaver behavior.
- `spec:playbook-explicit-macros` owns Playbook invocation behavior.

## Problem

The current Core skill corpus preserves the right behavior but is too verbose. It repeats surface ownership, rationale, and closure doctrine across many files. The compression must remove waste without creating a vague summary that drops the operational constraints models need.

## Desired Behavior

Compressed Loom skills should read like factory station instructions. They should tell the model what station it is at, what truth that station owns, when to use it, how to inspect, how to write or update, when to stop, what never to do, and what evidence or audit must support claims.

The compressed protocol must still work without Loom Mill. A model in chat with the skill pack and file tools should be able to shape, ticket, run Ralph, preserve evidence, audit, close, and promote knowledge from the `.loom/` graph.

## Not Doing

- Do not add new Loom surfaces for compression.
- Do not make Loom Mill required for protocol behavior.
- Do not weaken skill activation discipline.
- Do not remove ticket-owned Ralph handoffs.
- Do not merge evidence and audit.
- Do not turn prose-first records into rigid structured records.
- Do not preserve contributor-facing package process in model-visible doctrine.
- Do not rewrite historical `.loom` records as part of source-surface compression.

## Requirements

- REQ-001: Compressed protocol surfaces MUST preserve the core invariants: shape before execution, route truth to the owning surface, tickets own atomic execution, Ralph runs are bounded and ticket-owned, evidence is backpressure, audit is fresh-context inspection, worker output is a claim until reconciled, and transient prompts are transport.

- REQ-002: Skills SHOULD be operational kernels rather than manuals. Rationale, philosophy, repeated surface maps, and duplicate closure prose should be removed unless the sentence directly prevents a known failure mode.

- REQ-003: `using-loom` MUST remain a complete session kernel. It must preserve first-action skill activation, the surface map, loop order, shaping gate, worker handoff posture, proof posture, safety posture, and active knowledge loading.

- REQ-004: Record skills MUST define one station's job: owner truth, use triggers, inspect/read path, write/update path, status or lifecycle rules, stop conditions, and common non-examples. They must not reteach the entire Loom protocol.

- REQ-005: Skill references SHOULD become detail cards. Keep references when they provide exact record shape, tricky lifecycle/status behavior, high-risk closure or review rules, or examples that prevent common failures. Remove or merge references that only repeat the skill kernel.

- REQ-006: Weaver and Driver prompts MUST align with the factory roles without duplicating full skill doctrine. Weaver is the Design Office. Driver is the Factory Floor coordinator.

- REQ-007: Compression MUST preserve portability. Chat-based shaping, chat-based Driver execution, and any skill-capable harness must remain supported without Loom Mill.

- REQ-008: Compression MUST preserve product-surface hygiene. Model-visible product doctrine must not explain repository workflow, package smoke mechanics, adapter self-justification, dogfood state, or why Loom is built this way.

- REQ-009: Validation MUST include source inspection, package smoke/pack checks where touched, Markdown diff checks, targeted searches for lost or leaked behavior, and fresh-context audit before plan closure.

- REQ-010: If compression discovers that a behavior cannot be safely shortened, the retained prose must be justified by a known failure mode, spec requirement, or audit finding rather than personal preference.

## Scenarios

### SCN-001: Fuzzy Work Still Shapes

Exercises: REQ-001, REQ-003, REQ-004

GIVEN a user gives a broad product or engineering request
WHEN a model has only the compressed protocol loaded
THEN it routes through shaping and the owning surface before implementation
AND it does not create a ticket or patch from hidden direction choices.

### SCN-002: Ticket Execution Still Runs

Exercises: REQ-001, REQ-004, REQ-007

GIVEN an executable ticket has scope, acceptance, related records, worker context, evidence posture, and stop conditions
WHEN a Driver or ordinary model acts from the compressed protocol
THEN it can launch or coordinate a bounded Ralph run from the ticket
AND reconcile worker output before claiming progress.

### SCN-003: Proof Still Gates Closure

Exercises: REQ-001, REQ-009

GIVEN source changes and evidence exist for a non-trivial ticket
WHEN closure is considered
THEN evidence is tied to the exact acceptance claim
AND audit is run or explicitly justified before closure.

### SCN-004: Product Surface Stays Clean

Exercises: REQ-008

GIVEN a compressed model-visible skill or agent prompt
WHEN a consuming workspace loads it
THEN it teaches runtime behavior without leaking package workflow, dogfood assumptions, smoke-check explanations, or adapter mechanics.

### SCN-005: Compression Refuses False Minimalism

Exercises: REQ-002, REQ-005, REQ-010

GIVEN a verbose section prevents a known failure mode
WHEN shortening would remove the operational guardrail
THEN the compressed surface keeps the guardrail in sharper form rather than deleting it for line count.

## Evidence Plan

- REQ-001 / SCN-001 / SCN-002 / SCN-003: Fresh-context audit over the final diff and key compressed surfaces confirms core behavior remains present.
- REQ-002 / REQ-005 / SCN-005: Before/after line counts and source inspection show material reduction while retained prose maps to required behavior or known failure modes.
- REQ-003: Source inspection confirms `using-loom` and all preload surfaces remain aligned.
- REQ-006: Source inspection confirms Driver/Weaver prompts use factory roles and avoid full doctrine duplication.
- REQ-008 / SCN-004: Targeted grep/source inspection over model-visible surfaces checks for contributor-facing leakage.
- REQ-009: Core smoke, Core pack check, Playbooks smoke/pack where touched, `git diff --check`, targeted searches, and audit records support closure.

## Quality Bar

The compressed protocol should feel like station instructions in a software factory: brief, operational, hard to misread, and strong enough for a fresh frontier model to maintain the `.loom/` graph without chat history.

## Interface Contract

- Inputs: Existing Loom skills, references, templates, agent prompts, specs, plans, constitution records, research, and docs that expose protocol behavior.
- Outputs: Smaller model-visible protocol surfaces with the same behavior contract.
- Side effects: May update docs, specs, plans, tickets, evidence, audit, and knowledge when compression reveals needed alignment.
- Error semantics: If behavior preservation and compression conflict, preserve behavior and record why the prose remains.
- Compatibility or deprecation: No protocol surface is retired by compression unless a separate constitution/spec decision authorizes it.

## Examples And Non-Examples

Example compressed posture:

"Tickets own one executable work order. Create one only when scope, acceptance, evidence, and first Ralph boundary are clear. Stop if direction is still being invented."

Non-example compressed posture:

"Use tickets for tasks." This is too short because it drops execution readiness, evidence, and Ralph context.

## Constraints

- This spec implements the compression direction in `constitution:main` and `roadmap:loom-mill`.
- Product-visible doctrine must remain runtime behavior for installed workspaces.
- The protocol must remain prose-first and grep/find friendly.

## Open Questions

- Hard line-count budgets: not blocking. Compression quality is behavior-first; child tickets should record before/after line counts and explain retained verbosity.
- Exact final reference topology: not blocking. Tickets may merge, remove, or keep references when they satisfy REQ-005.

## Related Records

- `constitution:main` - defines Loom as protocol and Loom Mill as factory application.
- `roadmap:loom-mill` - names protocol compression as the current foundation chapter.
- `research:20260524-loom-mill-software-factory` - investigation that identified verbosity as the key protocol issue.
- `spec:ticket-owned-worker-handoffs` - worker handoff behavior compression must preserve.
- `spec:loom-driver-agent` - Driver behavior compression must preserve.
- `spec:loom-weaver-agent` - Weaver behavior compression must preserve.
