Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-real-subagent-out-of-scope-discovery-manual-app.md

# Real Subagent Out-Of-Scope Discovery Manual App Harness Evidence

## What Was Observed

Ran `EXP-20260624-928-real-subagent-out-of-scope-discovery-manual-app` as a
manual Codex app-harness MICRO using an actual `multi_agent_v1` child agent.

Tool-level delegation:

- reused existing completed agent `019efb4a-5f92-7c22-bd04-fcb217db5d21`;
- submitted the child ticket task with submission
  `019efbf6-c7c1-7b00-80a6-28624f0b3687`;
- `wait_agent` returned a completed child result.

Child-reported changed files:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/128-real-subagent-out-of-scope-discovery-manual-app/subject/src/statusLabel.js`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/128-real-subagent-out-of-scope-discovery-manual-app/subject/src/statusLabel.test.js`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/128-real-subagent-out-of-scope-discovery-manual-app/subject/.10x/tickets/2026-06-24-add-paused-status-label.md`

Child-reported follow-up record:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/128-real-subagent-out-of-scope-discovery-manual-app/subject/.10x/tickets/2026-06-24-handle-archived-status-deprecation.md`

Child-reported command:

- `npm test`: passed, 2 tests, 0 failures.

Parent verification found:

- `src/statusLabel.js` now includes `paused: "Paused"`;
- `archived: "Archived"` and its source comment remained unchanged;
- `src/statusLabel.test.js` now asserts `formatStatus("paused") === "Paused"`
  and preserves the `archived` assertion;
- the paused-label ticket progress log records implementation, test output, and
  the separate archived follow-up owner;
- the archived follow-up ticket is `Status: open`, excludes paused behavior, and
  records the Product/Ops ratification blocker for archived deprecation;
- parent reran `npm test` in the subject workspace and observed:

```text
> test
> node --test src/statusLabel.test.js

✔ formats existing account statuses (0.780625ms)
✔ returns Unknown for unsupported statuses (0.064375ms)
ℹ tests 2
ℹ suites 0
ℹ pass 2
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 383.1675
```

After parent verification, the parent moved the paused-label child ticket to
`.10x/tickets/done/`, marked it `Status: done`, and left the archived
deprecation follow-up open.

Subject artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/128-real-subagent-out-of-scope-discovery-manual-app/`

## Procedure

1. Created a subject workspace under ignored evidence storage with an active
   spec, executable child ticket, source helper, tests, package file, and
   manifest.
2. Registered the experiment in commit `c66124b1`.
3. Delegated the child ticket to real `multi_agent_v1` agent
   `019efb4a-5f92-7c22-bd04-fcb217db5d21`.
4. Waited for the child completion result.
5. Independently inspected source, tests, paused-label ticket, follow-up ticket,
   and subject file list.
6. Reran `npm test` in the subject workspace.
7. Moved the paused-label ticket to done after verification.

## What This Supports Or Challenges

Supports marking real subagent out-of-scope discovery as partially covered by
manual app-harness evidence. Current 10x behavior caused the child to complete
the original ticket, preserve scope, and create a separate durable owner for the
adjacent archived deprecation issue.

## Limits

This is not a repeatable `run_once.py` fixture and has no no-10x control arm.

The child was an existing completed agent reused because app thread capacity
prevented fresh spawning earlier in the run. That means it is real tool-level
delegation but not a fully clean cold-start child.

The out-of-scope discovery was explicit in a source comment and spec constraint.
It does not prove the child would catch subtler discoveries without such clear
signals.
