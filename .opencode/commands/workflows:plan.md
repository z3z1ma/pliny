---
description: Plan → create tickets (loom ticket) and a detailed implementation plan, using memory recall (loom memory).
agent: plan
subtask: false
---

You are running the **Plan** phase of the workflow.

User idea / request:
$ARGUMENTS

Goals:
- Turn the idea into a concrete, ticketed plan (loom ticket).
- Use recalled memory notes (loom memory) so we don't re-learn the same lesson twice.
- Do **not** implement code in this phase.

Process:
1) Run `compound_bootstrap` to ensure scaffolding exists.
2) Recall memory notes relevant to planning this idea:
   - Call `compound_memory_recall` with:
     - query: the user idea
     - command: "workflows:plan"
     - format: "prompt"
3) Inspect current ticket backlog:
   - `compound_ticket(argv=["list"])` (if it fails due to missing init, run `compound_ticket(argv=["init"])` then retry)
4) Create tickets:
   - 1 epic ticket that describes the user-facing outcome and acceptance criteria.
   - N task tickets (small, sequential) that implement it.
   - Add dependencies if sequencing matters.
5) Write a plan that includes:
   - ticket IDs + titles
   - sequencing and “definition of done”
   - tests/checks to run
   - risks and rollback plan
6) Finish by calling `compound_sync` to refresh AI-managed indexes in docs.

Output:
- A concise plan document.
- A list of created/updated ticket IDs.
