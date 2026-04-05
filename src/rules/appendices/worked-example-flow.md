# Appendix I — Worked Example Flow

## Purpose

This appendix shows one complete parent-side flow across the main Loom layers in this repository.

Use it when a fresh agent needs one concrete example of how the protocol behaves end to end.

## Scenario

The parent agent wants to prove and then explain one bounded implementation slice.

The target execution ticket is `<ticket-ref>`.

## Step 1 — Orient In The Workspace

The parent starts with always-on doctrine and workspace health.

Before choosing a task-specific path, the parent reads `constitution:main` so the next actions stay aligned with durable project policy.

Typical actions:

```bash
# Read the loom-workspace skill, these scripts are bundled in that skill
python3 "scripts/diagnose_workspace.py" --json
python3 "scripts/show_status.py" --json
python3 "scripts/resolve_scope.py" --json --path ".loom/constitution/constitution.md"
```

The parent uses these checks to confirm:

- the workspace is structurally healthy
- the root repository is the correct scope owner
- the next action can proceed without scope guessing

The parent also reads the main constitution record and should now know:

- what durable principles constrain the work
- what strategic direction the repository is currently optimizing for
- whether any constitutional decision or roadmap record also needs to be read before proceeding

## Step 2 — Read The Owning Ticket And Its Context

After reading the constitution, the parent reads the ticket and linked plan/spec records.

Typical governing artifacts include:

- the target ticket
- the linked plan
- the linked spec

The parent should now know:

- what the ticket owns
- what current acceptance requires
- what verification should exist afterward

## Step 3 — Compile The Packet

The parent compiles a persisted Ralph packet for the bounded execution step.

Example:

```bash
# Read the loom-ralph skill, this script is bundled in that skill
python3 "scripts/compile_packet.py" "<ticket-ref>" ralph --mode execution --style reference-first --allow-write-ref "<ticket-ref>"
```

The resulting packet is a durable Ralph packet artifact for that ticket.

The packet tells the child:

- the target ticket
- the allowed write set
- the source refs that matter
- the trust boundary
- the required output contract

## Step 4 — Launch The Fresh Child Run

The parent resolves the harness invocation using the standard resolution order (see the harness-invocation-templates appendix), then launches the child.

Resolution:

1. check `.loom/harness.md` for a matching profile
2. if absent, discover the current harness from the parent process (`ps -o comm= -p $PPID`) and learn its headless invocation syntax
3. if discovery is ambiguous, ask the operator

The parent substitutes the packet path and prompt into the resolved command template. For example, if the operator's `default` profile uses OpenCode:

```bash
opencode run -f "<packet-path>" -- "Execute the bounded Ralph packet for the attached ticket target. Perform the implementation or mutation work described by the packet, stay inside the declared write boundary, and return outcome status, files changed, verification summary, blockers, and continue/stop/blocked/escalate recommendation."
```

Or if the operator's `backend` profile uses Claude:

```bash
claude -p "Read @<packet-path> and proceed with: Execute the bounded Ralph packet for the attached ticket target. Perform the implementation or mutation work described by the packet, stay inside the declared write boundary, and return outcome status, files changed, verification summary, blockers, and continue/stop/blocked/escalate recommendation."
```

The specific CLI varies by operator setup. The packet and prompt content are the same regardless of harness.

## Step 5 — Reconcile Back Into Ticket Truth

After the child returns, the parent does not stop at the child output.

The parent:

1. inspects the changed file set
2. confirms the child stayed inside the allowed write set
3. updates the ticket journal or verification section as needed
4. records or links durable verification evidence

The outcome should be recorded in:

- the target ticket
- one or more verification records that justify the claimed progress

## Step 6 — Run Critique When Needed

When the parent needs an adversarial review of the resulting shape, it compiles and launches a critique packet.

Relevant artifacts include:

- one critique packet artifact
- one critique record
- one or more verification records or follow-up tickets

The point of this step is to pressure-test the result before calling it acceptance-ready.

## Step 7 — Update Docs From Accepted Truth

When the parent has accepted enough of the system shape to explain it, it compiles and launches a docs packet.

Relevant artifacts include:

- one docs packet artifact
- one target documentation record
- one or more verification records supporting the explanation

The docs step explains accepted reality. It does not replace ticket truth or unresolved critique.

## Step 8 — Decide The Next Owner

At the end of the flow, the parent asks which subsystem now owns the next decision.

Typical possibilities:

- `loom-ralph` if more bounded execution is clearly next
- `loom-critique` if review is clearly next
- `loom-docs` if explanation is clearly next
- `loom-tickets` if reconciliation or ledger cleanup is clearly next

## Why This Example Matters

This flow demonstrates the core Loom operating model in one place:

- rules first
- constitution before task execution
- explicit scope
- canonical records before packet launch
- packetized fresh child execution
- parent-side reconciliation
- durable verification
- tickets staying primary for live execution truth
