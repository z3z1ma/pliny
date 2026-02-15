---
"id": "al-7d1d"
"status": "closed"
"deps": []
"links": []
"created": "2026-02-15T19:25:42Z"
"type": "bug"
"priority": 0
"assignee": "w2"
"tags":
- "infra"
- "bug"
"external": {}
---
# Diagnose and resolve worker sidecar (omp) crashes

Worker w2 sidecar (omp) is crashing with rc=1. Log error: 'Model zai-coding-plan/glm-5 not found'. We need to investigate why this model is being referenced and fix the configuration so workers can execute correctly.

## Notes

**2026-02-15T19:27:36Z**

Sprint prep discovery update:
- Reviewed CHARTER objective rev2; this omp crash is now the active blocker for worker execution in sprint "Public Launch Architecture Cleanup".
- Backlog context: sprint-tagged open tickets are al-8d66, al-f968, al-18ec, al-58c0, al-9bf8 (+ non-sprint al-c09c). Current bug blocks execution throughput.
- Repo state for this worktree is clean except mounted .venv symlink.
- Verified runtime evidence in run artifacts:
  - run.json has harness=omp and omp.models.worker="zai-coding-plan/glm-5".
  - sidecar.started event for w2 shows model="zai-coding-plan/glm-5".
  - capture output shows repeated "Model \"zai-coding-plan/glm-5\" not found" followed by respawn-capped events.
Next: write sprint brief into this ticket and create child execution tickets with explicit ordering/dependencies.

**2026-02-15T19:28:04Z**

## Sprint Brief

### Objective restatement
Unblock worker execution by eliminating OMP sidecar crash loops caused by unresolved model selection (`zai-coding-plan/glm-5`), while preserving the broader sprint goal (public-launch architecture cleanup).

### Proposed sprint name
OMP Model Reliability

### Sprint focus and why this is the best next step
Focus this sprint slice on model-resolution correctness + guardrails in Team runtime. Current architecture tickets (al-8d66, al-f968, al-18ec, al-58c0, al-9bf8) depend on functioning worker panes. Until sidecar model resolution fails safely and predictably, we cannot execute planned architecture work.

### Current state (tickets + codebase)
- Open sprint-tagged tickets: al-8d66, al-f968, al-18ec, al-58c0, al-9bf8.
- Assigned bug ticket al-7d1d is now active and has no dependencies yet.
- Runtime evidence:
  - `.loom/team/runs/MiyagiDo/run.json` has `harness=omp` and `omp.models.worker="zai-coding-plan/glm-5"`.
  - `events/*sidecar.started*` for recipient w2 records `model="zai-coding-plan/glm-5"`.
  - `captures/*_w2.txt` records repeated `Model "zai-coding-plan/glm-5" not found`.
  - `events/*sidecar.respawn_capped*` confirms repeated crash + cap behavior.
- Relevant code path:
  - `src/agent_loom/team/core.py::_model_for_role` resolves role model -> harness fallback.
  - `src/agent_loom/team/core.py::tui` spawns OMP with resolved model and currently does no model preflight/validation.
  - `src/agent_loom/team/core.py::start` initializes per-harness model config and applies per-role overrides only for selected harness.

### Plan overview
1) Add a ticket to map exact model resolution path and failure mode end-to-end (run state -> spawn argv -> sidecar behavior).
2) Add a ticket to implement guardrails so invalid model config does not cause opaque crash loops (clear validation + actionable error path).
3) Add a ticket to provide runtime recovery/update workflow for existing runs and codify verification coverage in tests/docs.

### Risks and unknowns + resolution approach
- Unknown: whether OMP has a machine-readable model listing command suitable for strict validation.
  - Resolve by probing CLI capabilities; if unavailable, fail with deterministic preflight error for known-bad/empty config and explicit remediation steps.
- Risk: validating too aggressively could block valid custom/private models.
  - Resolve with phased guardrail: first ensure explicit, high-signal error and no respawn loop; add optional strict validation only when discoverability is reliable.
- Risk: fixes may handle new runs but miss existing persisted run.json state.
  - Resolve by including a migration/recovery path ticket for active runs and replay verification against captured failure case.

**2026-02-15T19:36:57Z**

Investigator sprint-prep completion update:

Created ticket set (children of al-7d1d)
- al-411a (P0 bug): Trace OMP model-resolution path end-to-end with repro evidence and code references.
- al-44f5 (P0 bug, depends on al-411a): Implement OMP preflight + fail-fast sidecar behavior to stop invalid-model respawn loops.
- al-1b53 (P1 task, depends on al-44f5): Add start-time OMP model validation and explicit recovery workflow/docs/tests.

Suggested ordering
1) al-411a
2) al-44f5
3) al-1b53

Parallelization guidance
- The three al-7d1d child tickets are intentionally serialized because each ticket feeds constraints/helpers into the next.
- Existing architecture tickets (al-8d66, al-f968, al-18ec, al-58c0, al-9bf8) can continue in parallel once worker sidecar stability is restored (after al-44f5).

Assignment update
- Per manager nudge, assigned diagnosis stream to worker execution:
  - al-7d1d assignee -> w2
  - al-44f5 assignee -> w2

Commands/evidence executed in this investigation
- loom ticket list -T sprint:Public-Launch-Architecture-Cleanup
- loom ticket list --status open
- git status --short --branch
- git log -n 20 --oneline
- read CHARTER + run.json + sidecar events + worker capture outputs
- omp --help
- omp --list-models zai-coding-plan/glm-5 (no match)
- omp --list-models opus (returns available models)

Primary risk remaining
- OMP model discoverability may vary by provider/token; implementation tickets include explicit handling to distinguish definite model-missing vs ambiguous listing failures.
