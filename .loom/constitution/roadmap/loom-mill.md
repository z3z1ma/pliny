# Loom Mill Roadmap

ID: roadmap:loom-mill
Type: Constitution Roadmap
Status: active
Created: 2026-05-24
Updated: 2026-05-24

## Strategic Frame

Loom Mill is the factory application built on the Loom protocol. It provides two first-class experiences that chat-based workflows cannot: a Design Office for interactive record shaping, and a Factory Floor for visible, steerable autonomous execution.

Mill does not replace chat-based Loom usage. It augments it. The protocol remains portable and functional without Mill. Mill is the machinery that makes the protocol run at industrial tempo.

## Current Chapter

**Chapter 1: Foundation**

Two parallel work streams:

1. Protocol compression: make the skills lean enough that the protocol is a sharp, portable kernel. This is prerequisite for confidence that Mill builds on stable ground.

2. Mill architecture and MVP: prove the core loop works. Worktree isolation, harness subprocess management, file watching, inter-iteration processes, and basic operator visibility.

The Factory Floor (execution visibility) is the first Mill surface because it solves the biggest current pain point and is architecturally simpler than the Design Office.

## Milestones As Strategic Signals

### Protocol Is Compressed

Skills are operational kernels. No repeated philosophy. No manual-length explanations. Models behave correctly from short, sharp doctrine. Evidence: a model given only the compressed skills produces correct Loom behavior on representative tasks.

### Factory Floor MVP Ships

The operator can: start execution against a ticket or set of tickets, watch progress via summaries and pipeline state, see backpressure signals, pause, steer (reshape a record), and resume. The MVP shells out to at least one coding harness. Worktree isolation works. At least one inter-iteration process (summarize) runs.

### Design Office MVP Ships

The operator can: see the `.loom/` graph visually, open a record in a split view, shape it via conversation (chat panel shelling out to a harness), see changes reflected live, and get readiness signals for execution.

### Full Factory Operational

Both tabs work together. The operator shapes in the Design Office until work is ready, then watches it fabricate on the Factory Floor. Inter-iteration processes (summarize, retrospect, aggregate, check evidence, detect patterns, select next work) all run. The loop improves itself via knowledge promotion.

## Bets And Assumptions

- Frontier models will continue to handle 12+ hour autonomous loop sessions when prompted correctly and given proper context engineering. Mill's visibility layer is additive, not a replacement for model capability.
- Web interfaces (ChatGPT, Claude.ai, etc.) will increasingly support skills and context injection, making the portable protocol more valuable over time, not less.
- Coding harnesses will continue to offer headless/exec modes that Mill can shell out to.
- Single-piece flow (one ticket per workstation) will remain the right default even as models get better. Batching hides defects.
- The prose-first record design will remain correct. Models that can reason about prose will always be available and improving.

## Tensions

- **Compression vs. completeness**: Aggressive compression risks losing behavior that models need. Must validate empirically.
- **Mill complexity vs. "just a loop"**: Mill should stay as simple as possible while providing real visibility. Danger of over-engineering what is fundamentally a file watcher + subprocess manager.
- **Portability vs. first-class experience**: Mill provides experiences chat cannot, but each Mill-only feature is something the portable protocol alone cannot deliver. Keep the protocol self-sufficient.
- **Automation vs. operator involvement**: The factory should run autonomously but the operator must be able to steer. Finding the right default (run until stopped vs. pause for approval) matters.

## Not Yet

- Multi-operator / collaborative Mill (not a current goal)
- Hosted/cloud version of Mill
- Mill as a service for teams
- Integration with external project management tools
- Mobile interface
- Marketplace for skills or inter-iteration processes
- Revenue model or commercial packaging

## Completion Or Supersession Conditions

This roadmap is complete when the full factory is operational: both modes work, the loop improves itself, and the operator can shape and observe a complete fabrication cycle from idea to shipped software.

Supersede if: the protocol fundamentally changes shape (e.g., moves away from prose-first records), or Mill's architecture proves wrong and needs a different structural frame.

## Related

- `constitution:main` - project identity and principles this roadmap serves
- `research:20260524-loom-mill-software-factory` - investigation that produced this strategic direction
