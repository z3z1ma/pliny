# Playbook Explicit Macros

ID: spec:playbook-explicit-macros
Type: Spec
Status: active
Created: 2026-05-15
Updated: 2026-05-16

## Summary

This spec defines the intended behavior of Loom Playbooks as explicitly invoked workflow macros rather than automatically activated workflow skills.

Downstream tickets should cite this spec when changing Playbook packaging, adapter manifests, command files, skill metadata, smoke checks, activation tests, or docs.

## Product Slice

This spec owns Playbook invocation behavior across supported harnesses: whether and how Playbooks enter the model context, how users invoke them, and how they relate to Core Loom routing.

This spec does not own each Playbook's internal workflow guidance, exact command names, complete adapter file formats, installer UX, or the behavior of Core record skills except where Playbooks must not override Core routing.

## Spec Set Coverage

This spec fills the behavior gap between Core record-skill activation and optional workflow lenses. Without this spec, implementation tickets would have to infer whether Playbooks are automatic skills, route-gated skills, command macros, or harness-specific explicit-only skills.

Adjacent behavior outside this spec:

- Core `using-loom` activation doctrine remains owned by the `using-loom` skill and its references.
- Loom Weaver and Loom Driver behavior remains owned by `spec:loom-weaver-agent` and `spec:loom-driver-agent`.
- Individual Playbook content quality may need separate tickets or specs if a Playbook's workflow behavior changes beyond invocation mechanics.

## Problem

Playbooks currently ship as broad model-visible skills in multiple adapters. Once installed, Core activation discipline makes every plausibly relevant Playbook a mandatory first-action candidate, which can stack workflow pressure before the owning Core surface has shaped the work.

Research shows Playbooks remain valuable as debugging, UI, security, source-authority, release, migration, TDD, and other workflow lenses, but their current automatic activation competes with Core's record-surface routing. The intended product behavior is explicit user invocation, not natural-language auto-triggering.

## Desired Behavior

Loom Playbooks should behave like explicit workflow macros. A user chooses a Playbook when they want that lens, or a Core route may recommend invoking one after the owning surface has established that the workflow lens is the next useful pressure.

Ordinary natural-language prompts should not cause Playbook content to enter model context merely because the prompt contains broad words like UI, auth, source, review, testing, debugging, implementation, migration, performance, or release.

Supported harnesses should use the strongest explicit surface they support:

- OpenCode should expose Playbooks through explicit command entries or command files, not `config.skills.paths` auto-discovery.
- Gemini CLI should expose Playbooks through extension `commands/*.toml`, not model-activated extension skills.
- Claude Code should expose Playbooks through commands or skills that are explicitly user-invoked only; if implemented as skills, they must use `disable-model-invocation: true`.
- Cursor should expose Playbooks through plugin commands or explicit-only skills; if implemented as skills, they must use `disable-model-invocation: true`.
- Codex should expose Playbooks as explicit-only plugin skills with `policy.allow_implicit_invocation: false` unless Codex later documents plugin-contributed prompt commands.

Generated command descriptions should use the existing Playbook source description.
Explicitness belongs in the command surface, explicit-only metadata, docs, and macro
body framing, not in a mechanically added description prefix such as `Explicit
optional workflow macro for`.

## Not Doing

- Do not keep Playbooks as broad auto-activated skills in the default Playbooks package surface.
- Do not claim all harnesses support the same command syntax or packaging mechanism.
- Do not claim Codex supports plugin-contributed custom prompt commands unless source-backed docs prove it.
- Do not remove Core record skills or weaken their natural-language activation behavior.
- Do not make Playbook macros a shortcut around Core routing, ticket shaping, evidence, audit, or ticket-owned Ralph worker/review discipline.
- Do not duplicate every Playbook into divergent harness-specific bodies when a shared source or generation path can prevent drift.
- Do not make stale natural-prompt activation tests pass by expecting Playbooks to auto-trigger.

## Requirements

- REQ-001: Loom Playbooks MUST be user-invoked or explicitly selected workflow macros, not automatic first-action skills triggered by ordinary natural-language task descriptions.

- REQ-002: Core record skills MUST remain the natural-language activation owners for Loom surfaces. Playbook macros may add workflow pressure only after explicit user invocation or after Core routing recommends that lens as the next useful step.

- REQ-003: Supported adapters MUST avoid exposing Playbooks through implicit model skill discovery when the harness provides a true command or prompt-macro surface.

- REQ-004: If a supported harness routes explicit commands through skill machinery, the Playbook package MUST use that harness's explicit-only control so the model cannot implicitly invoke the Playbook from the user prompt.

- REQ-005: Codex Playbooks MUST use explicit-only plugin skills with `policy.allow_implicit_invocation: false` unless a newer source-backed Codex record establishes plugin-contributed prompt commands. Docs and tests must not claim Codex custom Playbook slash commands before that support exists.

- REQ-006: OpenCode and Gemini CLI Playbooks MUST use true command or prompt-macro surfaces and stop registering Playbook skill directories for implicit model activation.

- REQ-007: Claude Code and Cursor Playbooks MUST use commands or explicit-only skills. If either adapter uses skills, those skills must disable model invocation.

- REQ-008: Playbook macro bodies MUST preserve Loom loop order. They may add workflow-specific pressure, but they must still route durable truth to Core surfaces and must not shorten required spec, plan, ticket, evidence, audit, or ticket-owned Ralph worker/review procedures.

- REQ-009: Playbook command surfaces, macro framing, and docs MUST present
  Playbooks as optional explicit lenses. They must not teach agents that a broad
  natural-language task requires Playbook activation before Core routing. Generated
  command descriptions are governed by REQ-013.

- REQ-010: Playbook packaging SHOULD keep canonical Playbook content in one source of truth or a generation workflow that prevents adapter-specific command bodies from drifting.

- REQ-011: Verification MUST include negative activation coverage proving representative natural prompts do not auto-load Playbooks, plus positive explicit-invocation coverage proving each supported adapter exposes the intended macro surface.

- REQ-012: Model-visible Playbook macro content MUST avoid contributor-facing leakage such as package smoke mechanics, adapter self-justification, dogfood state, test harness details, npm packaging, or repository workflow commentary.

- REQ-013: Generated Playbook command descriptions MUST reuse the source Playbook
  frontmatter description without adding an `Explicit optional workflow macro for`
  prefix or other generic explicitness preamble. The command or explicit-only
  surface, macro body framing, and docs remain responsible for communicating that
  Playbooks are deliberately invoked lenses rather than natural-prompt activation
  owners.

## Scenarios

### SCN-001: Natural Prompt Does Not Auto-Load Playbook

Exercises: REQ-001, REQ-002, REQ-003, REQ-011

GIVEN Playbooks are installed in a supported harness
WHEN a user sends a broad natural prompt such as "Let's make a React todo list"
THEN Core Loom routing may activate the relevant Core surface or ask to shape the work
AND no Playbook macro is automatically loaded merely because the prompt mentions a UI or implementation domain.

### SCN-002: User Explicitly Invokes A Playbook

Exercises: REQ-001, REQ-008, REQ-009, REQ-011

GIVEN Playbooks are installed in a supported harness
WHEN the user invokes a Playbook through the harness-specific explicit macro syntax
THEN that Playbook's workflow guidance enters the conversation
AND it preserves Core surface ownership, evidence posture, audit posture, ticket boundaries, and ticket-owned Ralph worker/review discipline while adding the selected workflow lens.

### SCN-003: Harness Uses Explicit-Only Skills

Exercises: REQ-004, REQ-005, REQ-007, REQ-011

GIVEN a harness packages Playbooks as skills because commands are unavailable or merged into skills
WHEN the Playbook package is installed
THEN each Playbook is marked explicit-only using the harness-supported control
AND the model cannot implicitly invoke it from ordinary user text
AND users can still invoke it through the documented explicit syntax.

### SCN-004: Codex Limiting Case

Exercises: REQ-005, REQ-009, REQ-011

GIVEN Codex plugin docs do not expose a plugin-contributed prompt-command component
WHEN Agent Loom packages Playbooks for Codex
THEN the package uses explicit-only skills with `policy.allow_implicit_invocation: false`
AND docs describe explicit skill invocation rather than unsupported custom slash commands.

### SCN-005: Adapter Content Drift Check

Exercises: REQ-008, REQ-010, REQ-012

GIVEN Playbook macro content is emitted for multiple harnesses
WHEN a Playbook body changes
THEN the adapter-specific emitted surfaces stay aligned with the canonical Playbook content
AND model-visible bodies remain free of contributor-only repository, package, smoke, and dogfood details.

### SCN-006: Command Description Uses Source Description

Exercises: REQ-009, REQ-013

GIVEN a Playbook source `SKILL.md` has a frontmatter `description`
WHEN OpenCode or Gemini command metadata is generated from the Playbook catalog
THEN the generated command description matches the source Playbook description
AND it does not add a generic explicitness preamble such as `Explicit optional workflow macro for`.

## Evidence Plan

- REQ-001 / SCN-001: Negative activation tests or harness smoke output show representative natural prompts do not auto-load Playbook content when Playbooks are installed.
- REQ-002 / SCN-001: Source inspection shows Core skill exposure remains available and Playbook package changes do not remove or weaken Core record-skill activation.
- REQ-003 / REQ-006: Source inspection shows OpenCode and Gemini Playbooks are exposed through command surfaces and not through implicit Playbook skill paths.
- REQ-004 / SCN-003: Source inspection shows explicit-only flags in harnesses that route command behavior through skills.
- REQ-005 / SCN-004: Source inspection shows Codex Playbooks use `policy.allow_implicit_invocation: false`, and docs avoid claiming unsupported custom slash commands.
- REQ-007 / SCN-003: Source inspection shows Claude and Cursor command or explicit-only skill packaging follows the selected adapter route.
- REQ-008 / SCN-002: Source inspection of representative macro bodies shows Playbooks preserve Core surface routing, evidence, audit, ticket, and ticket-owned Ralph worker/review discipline.
- REQ-010 / SCN-005: Diff or generation checks show adapter-specific Playbook bodies are derived from a canonical source or otherwise synchronized.
- REQ-011: Updated smoke or activation tests include both positive explicit invocation and negative natural-prompt cases.
- REQ-012 / SCN-005: Grep checks over model-visible Playbook macro content show no contributor-facing package, smoke, adapter-mechanics, dogfood, or repository workflow leakage.
- REQ-013 / SCN-006: Source inspection and generated-command checks show command
  descriptions are emitted from Playbook frontmatter descriptions without a generic
  explicitness prefix.

## Open Questions

- Command naming convention: does not block implementation as long as names are explicit, documented per harness, and avoid unsupported universal syntax claims.
- Claude and Cursor surface choice: does not block implementation because both commands and explicit-only skills satisfy the behavior contract when implicit invocation is disabled.
- Canonical source layout: does not block implementation, but the ticket or plan must choose a layout before duplicating all Playbook bodies across adapters.

## Quality Bar

Playbooks should feel like deliberate specialist lenses selected by the operator, not ambient model pressure. A reviewer should be able to inspect a natural-prompt run and see Core routing first, then inspect an explicit Playbook invocation and see the selected workflow guidance apply without bypassing Loom surfaces.

The adapter implementation should be honest about harness differences. Correctness is measured by explicit invocation behavior, not by forcing a uniform slash-command story across platforms that do not support it.

## Interface Contract

- Inputs: User-invoked Playbook macros through harness-specific syntax, or explicit recommendations from Core routing that the user may choose.
- Outputs: Workflow-specific prompt guidance added to the current conversation or run.
- Side effects: Packaging changes may add command files, explicit-only skill metadata, generated command bodies, manifests, smoke checks, and docs. Invocation itself must not write Loom records or source files unless the active macro routes through the appropriate Loom skill and user task.
- Error semantics: If a harness lacks true command support, the package must use explicit-only skills or document the lack of support rather than silently falling back to implicit skills.
- Validation boundary: A passing explicit macro invocation proves discoverability for that harness. A passing natural prompt proves only that Core routing still works unless negative checks show Playbooks stayed out of context.
- Compatibility or deprecation: Existing Playbook names may remain if they do not imply implicit activation. Natural-language Playbook autoactivation is deprecated by this spec.

## Examples And Non-Examples

Example posture after explicit invocation:

"Use this debugging lens after Core routing has identified a reproducible failure or investigation target. Preserve the failing observation first, then route durable facts to evidence, research, ticket, or audit as appropriate."

Non-example posture:

"Any bug report or suspicious behavior means you must load this Playbook before asking questions, inspecting code, or routing through Core."

Non-example packaging:

Registering `loom-playbooks/skills/` as a broad implicit model-visible skill path in OpenCode while also adding command files, because natural prompts would still be allowed to auto-load Playbooks.

## Constraints

- Model-visible product surfaces must not leak contributor-only repository process.
- Core record skills remain the owners of Loom surface routing.
- Harness-specific implementation must follow source-backed research instead of aspirational syntax claims.
- Codex remains explicit-only skill based until source-backed research proves plugin command support.

## Amendment Notes

- 2026-05-16: Added REQ-013 and SCN-006 after operator direction from
  `research:20260516-product-surface-scan`: generated Playbook command
  descriptions should use existing Playbook descriptions and should not add the
  `Explicit optional workflow macro for` prefix. This amendment does not remove the
  requirement that Playbooks remain explicit lenses rather than natural-language
  autoactivation owners.

## Related Records

- `research:20260515-playbook-command-surfaces` - identifies supported explicit macro or explicit-only skill surfaces by harness.
- `research:20260515-playbooks-core-activation-pressure` - explains why Playbooks should become explicit lenses instead of automatic activation owners.
- `evidence:20260515-playbook-activation-stacking` - preserves observed Playbook stacking and current smoke-test gaps.
- `research:20260514-direct-interactive-agent-surfaces` - prior supported-harness capability survey.
- `spec:loom-weaver-agent` - defines the complementary explicit outer-loop shaping persona.
- `spec:loom-driver-agent` - defines the complementary explicit inner-loop coordination persona.
- `spec:ticket-owned-worker-handoffs` - defines the worker/review handoff model Playbooks must preserve when adding workflow pressure.
- `loom-core/skills/using-loom/SKILL.md` - owns Core activation and routing doctrine.
- `loom-playbooks/` - current package surface to convert.
- `research:20260516-product-surface-scan` - records the command description polish finding and operator disposition.
