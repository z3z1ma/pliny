# Task Routing Catalog

This catalog maps ordinary coding prompts to Loom owner layers and workflow
skills. Use it after `routing.md` when the user asks in product, code, or tool
language rather than Loom layer language.

Named playbook routes are optional package-dependent helpers. If one is absent,
use the listed core owner layers plus local execution, Ralph, or a project-provided
equivalent workflow that leaves durable truth in the same owner layers.

Do not save these rows as route fields. They are prompts for agent judgment. The
ticket, spec, plan, evidence, critique, or other owner record must still carry the
truth that makes the next action recoverable.

## Common Coding Prompts

- User request shape: "Fix this bug", failing test, broken build, regression, flaky behavior, incident, unexpected error
  - First owner question: Is the failure reproduced and is root cause known?
  - Usual Loom route: optional `loom-debugging` or equivalent investigation -> evidence -> `loom-tickets` -> local execution or `loom-ralph`
- User request shape: Add feature, change product behavior, alter UX flow, change API behavior
  - First owner question: Is intended behavior or acceptance fuzzy?
  - Usual Loom route: `loom-specs` if fuzzy -> `loom-tickets` -> local execution or `loom-ralph`
- User request shape: Refactor, cleanup, simplify, reduce complexity without behavior change
  - First owner question: Is behavior preservation clear and bounded?
  - Usual Loom route: `loom-tickets` with `code-structure` -> evidence for preservation -> critique when nontrivial
- User request shape: Add or change tests, fixtures, smoke checks, browser checks, CI validation
  - First owner question: Is this validating existing acceptance or defining new expectations?
  - Usual Loom route: `loom-tickets` with `validation-instrumentation`; update `loom-specs` if expectations become behavior contract
- User request shape: Dependency upgrade, package manager change, build/lint/typecheck/tooling config
  - First owner question: Is compatibility or migration risk unknown?
  - Usual Loom route: `loom-research` when unknown -> `loom-tickets` with `dependency-tooling` -> evidence and critique
- User request shape: Performance problem, slow path, bundle size, Core Web Vitals, high traffic concern
  - First owner question: Is there a baseline measurement?
  - Usual Loom route: `loom-evidence` baseline -> `loom-research` or optional `loom-spike` or equivalent exploration workflow -> ticket -> after evidence -> performance critique
- User request shape: Security, auth, permissions, secrets, untrusted input, data exposure
  - First owner question: Is policy or intended trust boundary unclear?
  - Usual Loom route: `loom-specs` or `loom-constitution` if policy-bearing -> ticket -> evidence -> security critique
- User request shape: UI page, component, styling, responsive layout, accessibility, visual polish
  - First owner question: Is primary user task and quality bar clear?
  - Usual Loom route: `loom-specs` if fuzzy -> optional `loom-spike` or equivalent exploration workflow for variants when needed -> ticket -> visual/product evidence -> critique
- User request shape: API, module boundary, public interface, contract between systems
  - First owner question: Is the interface contract stable enough?
  - Usual Loom route: `loom-specs` and possibly `loom-research` -> plan/ticket -> critique for interface risk
- User request shape: Architecture improvement, module deepening, codebase more testable, tangled dependency
  - First owner question: Is this investigation, decision, or execution?
  - Usual Loom route: optional `loom-codemap` or equivalent atlas workflow, or `loom-research` -> `loom-specs` or `loom-constitution` for decisions -> plan/ticket
- User request shape: Database schema, storage, data migration, import/export, persistence safety
  - First owner question: Does order, rollback, or idempotency matter?
  - Usual Loom route: `loom-plans` when planning/decomposition matters -> ticket with `data-migration` -> before/after evidence -> critique
- User request shape: Documentation, ADR, troubleshooting note, domain terminology, shared language
  - First owner question: Is this policy, behavior, investigation, or accepted explanation?
  - Usual Loom route: `loom-constitution`, `loom-specs`, `loom-research`, or `loom-wiki` by owner truth
- User request shape: "Grill me", stress-test this idea/plan, refine idea, ideate, challenge assumptions
  - First owner question: Is the output a behavior contract, investigation, planning decision, or accepted explanation?
  - Usual Loom route: `loom-workspace` problem shaping -> `loom-research`, `loom-specs`, `loom-plans`, or `loom-wiki` by owner truth
- User request shape: Prototype this, try a few designs, sanity-check a state model, let me play with it
  - First owner question: What question should the throwaway artifact answer?
  - Usual Loom route: optional `loom-spike` or equivalent exploration workflow -> evidence/research -> spec/wiki/ticket route after conclusion
- User request shape: Use TDD, test-first, red/green/refactor, add regression coverage
  - First owner question: Which acceptance or bug claim should the failing check prove?
  - Usual Loom route: ticket/Ralph/local execution with `test-first` posture -> evidence red/green -> critique when warranted
- User request shape: Review comments, fix feedback, reviewer says, apply suggestions
  - First owner question: Are the findings understood and valid for this ticket/codebase?
  - Usual Loom route: `loom-critique` finding disposition -> ticket-owned disposition -> local execution/Ralph if fixes are needed
- User request shape: "Where is X?", unfamiliar code, understand this module, map architecture
  - First owner question: Is durable orientation useful for future agents?
  - Usual Loom route: optional `loom-codemap` or equivalent atlas workflow -> evidence/research -> wiki atlas when accepted
- User request shape: PR description, changelog, release note, launch, rollback, monitoring, handoff, merge package
  - First owner question: Are tickets/evidence/critique already truthful?
  - Usual Loom route: optional `loom-ship` or equivalent shipping workflow; route back to tickets/evidence/critique if not truthful
- User request shape: "Is this done?", "close it", "ready to merge?", acceptance or residual risk check
  - First owner question: Does ticket-owned acceptance support closure?
  - Usual Loom route: `loom-tickets` acceptance gate; optional `loom-ship` only after truth is current
- User request shape: User asks to keep going on a broad outcome
  - First owner question: Is there delegated objective, success criteria, and stop conditions?
  - Usual Loom route: optional `loom-drive` or equivalent objective driver -> owner layers -> tickets/Ralph/evidence/critique

## Ambiguity Gates

Route outward before implementation when:

- product direction would be invented by the agent;
- behavior could be implemented in materially different ways;
- success criteria or quality bar is missing;
- hidden assumptions, target user, or not-doing boundary would change the shape;
- evidence baseline is missing for a performance, bug, or migration claim;
- security, privacy, data-loss, or trust-boundary risk is unclear;
- the change is wider than one bounded ticket or write scope.

## Shared-Language Prompts

When the user uses domain terms, project jargon, or ambiguous nouns that matter to
the implementation, do not let the meaning stay in chat.

Route the clarification by owner:

- reusable behavior meaning -> `loom-specs`
- accepted explanation or glossary -> `loom-wiki`
- uncertainty or term conflict investigation -> `loom-research`
- project policy or durable naming principle -> `loom-constitution`
- one-ticket assumption that will not be reused -> `loom-tickets`

## Local vs Ralph

After the owning ticket is clear, choose execution shape:

- local execution when the write boundary is tiny, obvious, and safe in the
  current context;
- `loom-ralph` when the implementation/refactor/test/migration slice benefits
  from fresh context, explicit child write scope, replayable packet contract, or
  stronger isolation;
- optional `loom-debugging` or equivalent investigation workflow when root cause
  is unknown;
- optional `loom-spike` or equivalent exploration workflow when the right design,
  API, data model, or UI shape is still being explored.
