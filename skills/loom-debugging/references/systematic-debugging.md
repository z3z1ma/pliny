# Systematic Debugging

Systematic debugging is the high-discipline shape of `loom-debugging`.

Use it when a failure exists and the root cause is not yet proven. The operating
rule is simple: no durable fix claim before root-cause evidence.

## Phase 1: Reproduce And Observe

Before proposing a fix:

1. read the error, stack trace, log, diff, or failing output completely
2. capture exact reproduction steps or record why reproduction is not yet stable
3. check recent changes that could explain the failure
4. gather boundary evidence in multi-component systems: what entered each layer,
   what exited each layer, and where state or configuration changed
5. preserve the observation as evidence when future acceptance or critique will
   need it

If the failure cannot be reproduced, do not guess. Record the failed reproduction
attempt, add instrumentation or a narrower observation plan, and keep the ticket
or research truth honest.

## Phase 2: Localize Root Cause

Find the source, not just the symptom.

Use root-cause tracing when the failure appears deep in a call stack or downstream
component:

1. name the immediate symptom
2. identify the direct cause
3. ask what called or supplied that state
4. keep walking backward until the original trigger is found
5. fix at the source when practical

Use pattern comparison when a similar path works:

- find a working example in the same codebase
- compare the working and broken paths line by line or step by step
- list every difference before deciding which difference matters
- verify dependencies, configuration, environment, and assumptions

If multiple independent failures exist, group them by problem domain before
launching parallel investigation. Use `loom-git` and `loom-plans` parallel-wave
rules before any parallel child mutates files.

## Phase 3: Hypothesize And Test Minimally

Write the hypothesis plainly:

```text
I think <root cause> causes <observed failure> because <evidence>.
```

Then test one variable at a time. A hypothesis test may be a small diagnostic
change, a targeted command, a temporary log, a failing automated check, or a
minimal reproduction.

If the hypothesis fails, update research or ticket notes and form a new one. Do
not stack unrelated fixes until something passes.

If three fix attempts fail or each attempt exposes a new coupling problem, stop
and route outward. That is usually an architecture, spec, or plan problem, not a
request for a fourth guess.

## Phase 4: Fix Through The Owner Graph

Once root cause is supported:

1. tighten intended behavior in spec when needed
2. tighten or create the fix ticket
3. use a Ralph packet with `verification_posture: test-first` when the behavior
   can be exercised
4. create the failing check before implementation
5. implement the smallest root-cause fix
6. preserve red and green evidence
7. route critique when risk warrants

Observation-first is acceptable when the behavior cannot yet be automated, but it
still requires before/after evidence.

## Defense In Depth

After a root-cause fix, ask whether one check merely hides the symptom or whether
the system should reject the bad state at multiple boundaries.

Common layers:

- input or API boundary validation
- business-rule validation near the operation
- environment or safety guard around dangerous contexts
- diagnostic logging that makes future failures localizable

Do not add broad validation as a reflex. Add it where the evidence shows the bad
state can enter or propagate.

## Condition-Based Waiting

For flaky or timing-dependent tests, wait for the real condition rather than a
guessed duration.

Prefer:

```text
wait until event/state/file/count/condition exists, with a timeout and useful error
```

over:

```text
sleep for an arbitrary duration and hope the system caught up
```

Arbitrary waits are acceptable only when timing itself is the behavior under test
and the wait is tied to a documented timing contract.

## Loopbacks

Route out of implementation when:

- reproduction remains unstable
- intended behavior is disputed or missing
- root cause points at a broader design flaw
- evidence cannot support the acceptance claim
- the fix would widen scope beyond the ticket
- prior fixes failed enough to challenge the architecture

Typical loopbacks:

- debugging -> evidence when more observation is needed
- debugging -> research when hypotheses or rejected paths should persist
- debugging -> spec when intended behavior is unclear
- debugging -> plan when the fix needs sequencing or decomposition
- debugging -> constitution only when a durable principle or architectural
  precedent is being challenged
