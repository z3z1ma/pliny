# Skill Review

Use skill review when a skill change affects how future agents route, execute,
verify, critique, accept, or close work.

Skill review is not a new layer. It routes through evidence and critique when the
change deserves durable support or pressure-testing.

## Review Questions

Ask:

- does the skill own one coherent subsystem or workflow route
- does it duplicate an existing owner skill
- does the description name activation triggers without becoming a shortcut for
  the full workflow
- does the skill body say what it owns and does not own
- are references immediate vs conditional for a reason
- are templates present only when the skill owns an artifact shape
- does the skill preserve Loom's owner-layer boundaries
- does it depend on a hidden runtime, helper, command wrapper, or harness feature
  as the true source of behavior

## Pressure Scenarios

Use pressure scenarios when a skill enforces discipline that agents may skip under
pressure, such as test-first work, verification before completion, root-cause
debugging, critique gates, or destructive-operation confirmation.

A useful pressure scenario combines realistic temptations:

- time pressure
- sunk cost
- a tempting shortcut
- authority or social pressure
- fatigue or desire to finish
- ambiguity about whether the rule applies

The scenario should force a concrete choice. Record whether the skill makes the
correct choice obvious enough without adding a hidden runtime.

## Evidence And Critique

For low-risk skill edits, a diff review and targeted `rg` check may be enough.

For medium or high-risk skill edits, create or update critique when the review
should persist. Create evidence when validation output, pressure-scenario results,
or structural checks should remain citable by a ticket or future critique.

Do not claim a skill is proven because it reads well. Claim only what was
actually validated.

## Common Findings

- activation too broad, causing ceremony or skill spam
- activation too narrow, causing missed routing
- body repeats doctrine that belongs in bootstrap
- workflow creates a shadow ledger outside tickets or owner records
- reference is mandatory even though only rare users need it
- template permits placeholder IDs or vague completion claims
- skill tells agents to skip critique, evidence, or ticket reconciliation
