# Add Loom Driver Agent

ID: ticket:20260515-loom-driver-agent
Type: Ticket
Status: closed
Created: 2026-05-15
Updated: 2026-05-15
Risk: high - adds a new model-visible agent persona and cross-harness adapter surfaces for inner-loop execution behavior.
Priority: high - follows operator request to add a Loom Driver inner-loop agent complementing Loom Weaver.

## Summary

Add a Loom Driver agent surface to Agent Loom. Loom Driver is an explicit inner-loop persona that starts from shaped execution targets, creates or consumes Ralph packets, coordinates worker execution including safe parallelization, preserves evidence, routes audit, reconciles tickets, and refuses to mutate high-authority Loom records during execution.

Single closure claim: Agent Loom ships a Loom Driver agent/persona whose behavior satisfies `spec:loom-driver-agent` and whose supported-harness exposure follows the existing Loom Weaver agent pattern without claiming unsupported universal invocation semantics.

## Related Records

- `spec:loom-driver-agent` - owns the Loom Driver behavior contract, write boundary, routing requirements, scenarios, and quality bar.
- `spec:loom-weaver-agent` - provides the complementary outer-loop agent pattern and adapter precedent.
- `research:20260514-direct-interactive-agent-surfaces` - source-backed comparison of OpenCode, Claude Code, Gemini CLI, Cursor, and Codex agent invocation surfaces.
- `ticket:20260514-loom-weaver-agent` - implementation precedent for named Core agent surfaces, validation, and residual risks.
- `packet:20260515T054840Z-loom-driver-agent-implementation` - bounded implementation packet and worker output for this ticket.
- `evidence:20260515-loom-driver-agent-validation` - validation observations for prompt content, OpenCode registration, package inclusion, Claude validation, and diff checks.
- `packet:20260515T060624Z-loom-driver-agent-audit` - Ralph audit packet and worker output for final review.
- `audit:20260515-loom-driver-agent-audit` - final audit record with `clear` verdict and no material findings.
- `packet:20260515T061216Z-loom-driver-final-audit` - narrow final audit packet after the post-audit architecture-doc alignment edit.
- `audit:20260515-loom-driver-final-audit` - final audit record confirming the closure story still holds for the current diff.
- `AGENTS.md` - contributor constraints for product-surface leakage, package shape, adapter entrypoints, and validation commands.
- `INSTALL.md` - current install matrix that should explain how to invoke named agents per harness.

## Scope

May change:

- Core agent prompt files under `loom-core/agents/`, adding a canonical `loom-driver` prompt.
- Codex custom-agent TOML under `loom-core/codex/agents/`, adding `loom-driver.toml` and keeping it aligned with the canonical prompt.
- OpenCode Core entrypoint `loom-core/loom-core.mjs` to register all shipped agents or specifically register `loom-driver` with appropriate permissions and smoke checks.
- Core native adapter manifests and extension-facing files when needed to expose the new agent surface, especially `loom-core/.claude-plugin/plugin.json`.
- Human-facing docs that already describe named Core agents, especially `INSTALL.md`, `README.md`, and `loom-core/README.md`.
- This ticket, new evidence records, and any audit or Ralph packet records needed for implementation and review.

Must not change:

- Do not change `using-loom` doctrine as part of this ticket unless implementation proves the existing doctrine cannot support Driver.
- Do not edit `loom-playbooks/` unless a documentation cross-reference is necessary; Loom Driver belongs to Core unless implementation proves otherwise.
- Do not add app runtime infrastructure, daemons, databases, dashboards, helper CLIs, or non-Markdown product state.
- Do not make Loom Driver the default startup agent automatically unless a separate operator-approved decision changes `spec:loom-driver-agent`.
- Do not dilute Loom Driver into a generic coding agent; keep packet-first inner-loop execution, evidence, audit, and ticket reconciliation central.
- Do not put contributor-only package smoke, adapter mechanics, dogfood state, or repository workflow explanations into model-visible Loom Driver instructions.

System-shape constraints:

- Treat Loom Driver as an optional named persona/surface layered on top of Loom Core, not as a replacement for `using-loom` activation doctrine or existing record skills.
- Keep one canonical Loom Driver behavior source or an explicitly documented minimal duplication strategy so OpenCode, Claude, Gemini, Cursor, and Codex surfaces do not drift.
- Where a harness cannot enforce high-authority Loom record protection mechanically, the prompt and audit must call out the enforcement limit.
- Follow the same harness invocation honesty posture established by Loom Weaver: do not claim Cursor or Codex support `@<agent>` custom-agent invocation unless newer source-backed research proves it.

First likely Ralph packet:

- Compile a source-backed implementation packet that reads `spec:loom-driver-agent`, the Loom Weaver implementation precedent, current Core entrypoints/manifests/package files, and inner-loop doctrine; then implements the smallest complete Core Loom Driver surface and updates docs/validation evidence.

## Acceptance

- ACC-001: A canonical Loom Driver behavior source exists and matches `spec:loom-driver-agent`: inner-loop execution posture, shaped-target gate, packet-first behavior, safe parallelization, evidence and audit routing, ticket reconciliation, and high-authority record read-only boundary.
  - Evidence: source inspection plus targeted grep over canonical prompt/agent files for inner-loop language, Ralph packet language, parallelization constraints, evidence/audit language, ticket reconciliation, and high-authority record mutation prohibition.
  - Audit: review should challenge whether the prompt duplicates `using-loom` doctrine, acts as a generic coder, or leaks contributor-only package details.

- ACC-002: OpenCode exposes Loom Driver as a directly user-selectable and explicitly invokable agent surface comparable to Loom Weaver, with permissions appropriate for inner-loop execution.
  - Evidence: source inspection of OpenCode Core configuration plus Core smoke/pack checks.
  - Audit: review should challenge whether OpenCode agent registration is shipped in the package artifact, whether Driver permissions are too broad or too restrictive, and whether existing Weaver behavior still passes checks.

- ACC-003: Claude, Cursor, Gemini, and Codex package surfaces expose or ship Loom Driver consistently with the existing Loom Weaver support pattern without overstating unsupported invocation semantics.
  - Evidence: source inspection of manifests, `loom-core/agents/loom-driver.md`, `loom-core/codex/agents/loom-driver.toml`, install docs, and relevant package checks or validators when available.
  - Audit: review should challenge manifest inclusion, Codex custom-agent install language, Cursor slash/natural-language semantics, and Gemini delegated-subagent wording.

- ACC-004: Human-facing docs explain both named Core agents without becoming a second source of model behavior.
  - Evidence: source inspection of updated docs plus grep showing model-critical behavior remains in shipped agent prompt surfaces and Codex TOML, not only in README/INSTALL prose.
  - Audit: review should challenge docs for universal syntax claims, default-agent claims, and product-surface leakage.

- ACC-005: Package and Markdown validation appropriate to touched files passes.
  - Evidence: at minimum `npm --prefix loom-core run smoke`, `npm --prefix loom-core run pack:check`, and `git diff --check`; additionally run Claude/Gemini validators after their manifests/extensions change, and run Playbooks checks only if Playbooks files are touched.
  - Audit: review should challenge whether package `files` include new shippable agent/prompt artifacts and whether validation omitted a touched adapter surface.

- ACC-006: A fresh Ralph-backed audit pass challenges the Loom Driver prompt, adapter exposure, validation, and record story before closure.
  - Evidence: `loom-audit` record or Ralph review packet output covering prompt safety, high-authority record boundary, packet-first behavior, harness support honesty, package inclusion, and product-surface leakage.
  - Audit: this criterion requires separate audit/review; do not close on implementation self-report alone.

## Current State

Closed. Agent Loom now ships optional Loom Driver surfaces with a canonical prompt in `loom-core/agents/loom-driver.md`, OpenCode agent registration, Claude/Cursor/Gemini agent-directory exposure through existing package surfaces, and Codex custom-agent TOML support in `loom-core/codex/agents/loom-driver.toml` with documented install under `~/.codex/agents/`.

Acceptance is supported by `evidence:20260515-loom-driver-agent-validation`, full audit `audit:20260515-loom-driver-agent-audit`, and final follow-up audit `audit:20260515-loom-driver-final-audit`. Core smoke, Core pack dry-run, `git diff --check`, and Claude plugin validation passed after implementation; the Ralph audits returned `clear` with no material findings. Live runtime invocation was not tested in OpenCode, Claude Code, Codex, Cursor, or Gemini. OpenCode high-authority record permission matching was source/smoke-inspected but not runtime-tested. Cursor and Gemini runtime/plugin validation was not rerun because their manifests were not changed. These are explicit residual risks, not closure claims.

## Journal

- 2026-05-15: Created ticket from operator request to add Loom Driver as an inner-loop counterpart to Loom Weaver. Linked `spec:loom-driver-agent`, Weaver precedent, and direct-agent research as the behavior and harness constraints.
- 2026-05-15: Set status to active and began consuming `packet:20260515T054840Z-loom-driver-agent-implementation` for the bounded implementation slice.
- 2026-05-15: Implemented Driver prompt, Codex TOML, OpenCode registration and smoke checks, Claude manifest exposure, and docs updates. Recorded validation in `evidence:20260515-loom-driver-agent-validation`; audit remains required before closure.
- 2026-05-15: Moved status to review for a fresh Ralph-backed audit pass before closure.
- 2026-05-15: Ralph audit `packet:20260515T060624Z-loom-driver-agent-audit` returned `clear` with no material findings. Recorded `audit:20260515-loom-driver-agent-audit`.
- 2026-05-15: Closed ticket with residual risks called out: no live runtime invocation tests, OpenCode permission matching not runtime-tested, Cursor/Gemini runtime validation not rerun, Codex remains explicit custom-agent TOML install, and high-authority record protection is prompt-level outside OpenCode.
- 2026-05-15: Ran final narrow audit `packet:20260515T061216Z-loom-driver-final-audit` after a small `ARCHITECTURE.md` alignment edit. Recorded `audit:20260515-loom-driver-final-audit`; verdict remained `clear` with no material findings.
