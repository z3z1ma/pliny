---
name: loom-frontend-ui-engineering
description: "Use when user-facing UI engineering needs coordinated behavior/design handling: components, pages, flows, layouts, interactions, responsive/accessibility/visual quality, frontend state, data fetching, or browser runtime evidence."
---

# loom-frontend-ui-engineering

Frontend UI engineering is a Loom playbook for user-facing interface work.

It turns design intent into specs, slices implementation through tickets and Ralph
packets, records browser evidence, and routes accessibility, performance, and
visual risks through audit.

## Loom Routing

Common routes use these Loom skills for durable records or follow-up workflow:
`loom-specs`, `loom-tickets`, `loom-ralph`, `loom-evidence`, `loom-audit`,
`loom-knowledge`, and `loom-retrospective`.

Ensure the `using-loom` skill is loaded before applying this workflow.

When routing to any named Loom skill, follow that skill's procedure and guidance
completely. This playbook adds workflow pressure; it does not shorten the target
skill's requirements.

Keep broad product or design intent in outer-loop shaping until the
operator-facing direction, scope and exclusion choices, information hierarchy,
state boundaries, quality bar, evidence posture, and ticket boundary are clear
enough to route.

## Use This Playbook When

Use this playbook when:

- creating or modifying UI components, pages, flows, layouts, or interactions
- visual quality, responsive behavior, or accessibility matters
- browser runtime state must be observed
- frontend state, data fetching, loading, error, or empty states are in scope
- design system adherence or existing UI patterns constrain the work
- UI work needs screenshots, DOM inspection, console/network checks, or performance
  observations

## Route

Use this route:

```text
intent -> contract -> slice -> build -> observe -> review -> preserve
```

## Intent

Clarify:

- user task or operator workflow
- what the UI should include and intentionally leave out
- information hierarchy, domain model, and primary objects
- primary state and secondary states
- success, empty, loading, error, disabled, permission, and offline states
- desktop and mobile behavior
- accessibility expectations
- design system or existing component patterns
- performance or responsiveness constraints
- non-goals and adjacent UI not being changed

When the request is still a rough product idea, use `loom-idea-refine` or
outer-loop shaping before writing the UI contract. Design adjectives become useful
only when they resolve into direction, examples or non-examples, constraints, and
evidence.

Do not let a vague visual or product direction become UI implementation until the
design's domain model and state boundaries are explicit enough to review.

Route durable intended behavior to `loom-specs` when it affects more than one
ticket or future work.

## Contract

Good UI specs include:

- `REQ-*` for behavior, state, accessibility, and quality constraints
- `SCN-*` for visible scenarios and interaction probes
- examples or non-examples when visual quality is fuzzy
- evidence plan for screenshots, DOM, accessibility tree, console, network, and
  runtime behavior

Use existing design-system docs, component atlases, and source patterns as context.
Promote reusable UI conventions to `loom-knowledge`.

## Build

Implement from ticket-ready slices:

- component structure before broad integration
- one user path before all variants
- data loading before interaction polish when the flow depends on data
- accessibility and keyboard behavior with the component, not after it
- responsive behavior before claiming visual completion

Use a plan when the UI work has independent stack, data, shell, interaction,
visual, browser-verification, or audit closure stories.

Prefer composition over configuration-heavy components. Separate data loading from
presentation when it improves clarity. Match the project's existing state and
styling conventions.

## Observe

For browser-backed UI work, use `loom-browser-testing-with-devtools` or equivalent
runtime observation.

Evidence may include:

- screenshots before and after
- DOM or accessibility tree excerpts
- console output showing no relevant errors
- network requests and payload shape
- viewport checks at important breakpoints
- keyboard navigation or focus observations
- performance trace, LCP, INP, or CLS when relevant

Record observations with `loom-evidence` when they support ticket closure or audit.

## Review

Review UI against:

- intended behavior and scenarios
- accessibility
- responsive layout
- visual hierarchy and spacing
- loading, empty, error, and permission states
- state management and data-fetching boundaries
- security of rendered external data
- performance and unnecessary rerenders
- consistency with existing component patterns

Use `loom-audit` for Ralph-backed UI review when closure depends on subjective
quality, accessibility, performance, or browser evidence.

When that review is delegated to a worker, compile a Ralph packet and launch the
worker from the packet path.

## Done Means

The UI pass is done when:

- behavior and quality expectations are written or scoped in the ticket
- desktop and mobile states in scope were checked
- accessibility and keyboard expectations were checked when interactive UI changed
- runtime browser observations exist when static code review is insufficient
- evidence supports the exact UI claim
- reusable UI patterns or traps are promoted through retrospective when they will
  prevent likely rediscovery or document an accepted UI convention
