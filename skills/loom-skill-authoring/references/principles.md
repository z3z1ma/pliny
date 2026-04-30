# Principles

## 1. One owner

A skill should own one coherent subsystem.

Owner-layer skills should name the layer they own. Workflow, control-plane,
inner-loop, authoring, support, and shared-grammar skills should say what they
coordinate and which existing records receive durable output.

## 2. Strong description

The description should make activation discoverable without loading the whole skill first.

Descriptions should include the clearest "use when" trigger and, when relevant,
the owner boundary that tells the agent where durable output belongs.

Prefer trigger-focused descriptions over workflow summaries. The description
helps the harness or model decide whether to load the skill; the body should own
the procedure. A description that summarizes a multi-step workflow can become a
shortcut that future agents follow instead of reading the skill.

## 3. Operational clarity

A skill should tell the agent what to do, not just what the skill is about.

## 4. Templates when needed

If the skill creates records or pages, include templates.

## 5. Reference depth without bloat

Put nuance in `references/`.
Keep the main skill file strong enough to orient the reader quickly.

## 6. Progressive disclosure with judgment

Do not make `Read In This Order` a bare index.

Name which references are immediate for normal use and which are conditional.
Each entry should say when the agent should open it.

## 7. Verification proportional to behavior

Skill edits are behavior edits when they change routing, discipline, acceptance,
operator decisions, or protocol authority.

Use the smallest honest validation for the change:

- structural review for low-risk wording or link changes
- pressure scenarios for discipline-enforcing guidance that agents may
  rationalize away
- direct critique for workflow, authority, or acceptance changes
- evidence records when validation output should remain citable

Do not require a hidden test harness for every skill edit. Do require evidence
strong enough for the claim being made.
