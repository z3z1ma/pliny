# Workspace Examples

## Typical Parent Questions

Good `loom-workspace` questions look like this:

- which repository owns this path?
- is the workspace healthy enough to trust for packetized work?
- which subsystem skill should I load next?
- what kinds of canonical records currently exist?

These questions are about orientation, trust, and routing. That is why they belong to the workspace skill rather than to one artifact-owning sibling skill.

## Example Fresh-Entry Procedure

```text
1. Inspect status to see where active work is concentrated.
2. Run workspace diagnostics before trusting packet or review workflows.
3. Resolve repository ownership for the target path or artifact.
4. Choose the owning artifact skill only after health and scope are clear.
```

## Example Routing Pattern

```text
If the main question is “what owns this work?” or “is the workspace healthy enough to proceed?”, start with loom-workspace.
If the main question is about one specific artifact family, switch to the owning sibling skill after workspace diagnosis.
```

## Worked Parent Example

```text
Situation: You just entered a repository and the user asked for help on a long-running change.

Good first questions:
- Is the workspace structurally healthy?
- Which repository owns the target path or artifact?
- Which Loom layer owns the next durable mutation or review step?

Good next action:
- Use workspace diagnosis first.
- Then switch to the owning sibling skill once the next step is clear.
```

## Example Implementation Helper Pattern

```bash
scripts/workspace.py diagnose --json
scripts/workspace.py status --json
scripts/workspace.py scope --json --path "<target-path>"
```

These commands are only one implementation of the larger control-plane procedure above. The important concept is:

- establish trust
- establish scope ownership
- choose the next owning Loom layer

The scripts help mechanize those steps, but they are not the whole meaning of the workspace layer.

## What A Good Outcome Looks Like

- diagnose workspace reports structural readiness clearly
- show status gives quick orientation by record kind and status
- resolve scope assigns one owning repository or fails closed

The good outcome is a clearer next decision, not just a prettier report.

## Example Strong Parent Reasoning

```text
I know the user wants work on a long-running change, but I do not yet know whether the next durable action belongs to tickets, critique, docs, or planning.

I will first establish workspace trust, then establish scope ownership, then choose the owning layer.
```

## Example Failure Case

This is a bad parent move:

```text
The repository seems fine. I'll just guess which skill owns the work and start editing.
```

It is bad because it skips the exact control-plane work that prevents scope mistakes, wrong-skill routing, and premature packet launches.

## Better Parent Reasoning Pattern

```text
I do not yet know whether this is a ticket update, a critique pass, a docs update, or a planning task.

First I should confirm the workspace is healthy enough to trust.
Then I should confirm which repository owns the target.
Then I should choose the owning sibling skill and move into that artifact layer.
```

## Example Weak Parent Reasoning

```text
This sounds like docs, so I will jump straight into editing explanations.
```

Why this is weak:

- the workspace may not be healthy enough to trust yet
- the work may actually belong to tickets, critique, or specs instead
- scope ownership may still be ambiguous
