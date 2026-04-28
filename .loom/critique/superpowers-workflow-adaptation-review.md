---
id: critique:superpowers-workflow-adaptation-review
kind: critique
status: final
created_at: 2026-04-28T08:05:59Z
updated_at: 2026-04-28T15:35:47Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: ticket:k7p4s2q9 and Superpowers workflow adaptation diff
links:
  tickets:
    - ticket:k7p4s2q9
  research:
    - research:superpowers-skill-workflow-adaptation
  evidence:
    - evidence:superpowers-workflow-adaptation-validation
external_refs:
  github:
    - https://github.com/obra/superpowers/tree/main/skills
---

# Summary

Critique of the Superpowers-to-Loom workflow adaptation for workflow-boundary and operator-surface risks.

# Review Target

Reviewed the working-tree changes for `ticket:k7p4s2q9`, including updates to Loom skills, bootstrap references, README/PROTOCOL workflow maps, research/evidence/ticket records, and new references for systematic debugging, handoff options, and skill review.

# Verdict

`pass_with_findings`

The adaptation preserves Loom's owner-layer model and does not import a Superpowers namespace, hidden runtime, or new truth ledger. Four findings were raised during review and resolved before this critique was finalized.

# Findings

## FIND-001: Test-first expected-failure rule drifted across surfaces

Severity: medium
Confidence: high
Disposition: resolved

Observation:

The bootstrap reference required `test-first` checks to fail for the expected reason, while Ralph's verification posture and packet template initially used older stop-condition wording that did not require expected-failure validation.

Why it matters:

Packet templates and Ralph references are the surfaces operators will use when compiling implementation packets. Drift there could weaken the TDD discipline the adaptation intended to preserve.

Follow-up:

Resolved by aligning `skills/loom-ralph/references/verification-posture.md` and `skills/loom-ralph/templates/ralph-packet.md` with the expected-failure requirement.

Challenges:

- ticket:k7p4s2q9/loom-layer-ownership-preserved

## FIND-002: Ship handoff options needed an explicit Git boundary

Severity: medium
Confidence: high
Disposition: resolved

Observation:

The new `handoff-options.md` reference discussed branch/worktree/diff/merge/abandon decisions, but `loom-ship/SKILL.md` initially did not route Git mechanics to `loom-git`.

Why it matters:

Without the read-order bridge, shipping guidance could become a parallel Git workflow surface instead of packaging Loom truth and delegating Git mechanics to the Git workflow skill.

Follow-up:

Resolved by adding `skills/loom-git/SKILL.md` to the conditional `loom-ship` read order and by stating in `handoff-options.md` that Git mechanics belong to `loom-git`.

Challenges:

- ticket:k7p4s2q9/loom-layer-ownership-preserved

## FIND-003: Superpowers source fingerprint was incomplete

Severity: medium
Confidence: high
Disposition: resolved

Observation:

The evidence initially recorded the temp clone path but not the Superpowers commit SHA or exact top-level skill inventory.

Why it matters:

The claim that every meaningful Superpowers skill was accounted for would be less reproducible once `/tmp` was cleaned up or upstream Superpowers changed.

Follow-up:

Resolved by recording Superpowers commit `6efe32c9e2dd002d0c394e861e0529675d1ab32e` and the 14 top-level skill names in `evidence:superpowers-workflow-adaptation-validation`, and by citing the commit in research.

Challenges:

- ticket:k7p4s2q9/adapt-superpowers-skills

## FIND-004: Public workflow maps were partially non-normalized

Severity: low
Confidence: medium
Disposition: resolved

Observation:

`README.md` and `PROTOCOL.md` initially used overlapping but not identical workflow labels after the adaptation, such as `map` versus `code map` and `work` versus `implementation`.

Why it matters:

The public product surface should not make future agents wonder whether these are distinct workflows or aliases.

Follow-up:

Resolved by normalizing `PROTOCOL.md` labels and expanding the README route examples so both surfaces use the same workflow vocabulary.

Challenges:

- ticket:k7p4s2q9/public-skill-surface-structurally-valid

## FIND-005: Critique profile leaked package-specific product-surface assumptions

Severity: medium
Confidence: high
Disposition: resolved

Observation:

The newly added critique profile was named `product-surface` and referred to public docs, `skills/`, and constitutional backing in a way that assumed this repository's distributable package context instead of a generic Loom workspace.

Why it matters:

The `skills/` corpus is distributed into many repositories. A skill reference should teach a reusable Loom protocol lens, not assume the `agent-loom` package itself is the target project.

Follow-up:

Resolved by renaming the profile to `operator-surface` and rewriting it to refer generically to a project's user-facing instructions, Loom skills, templates, examples, adapters, support docs, declared Loom owner graph, and canonical project truth.

Challenges:

- ticket:k7p4s2q9/loom-layer-ownership-preserved

# Evidence Reviewed

- `ticket:k7p4s2q9`
- `research:superpowers-skill-workflow-adaptation`
- `evidence:superpowers-workflow-adaptation-validation`
- `git diff --check` output: clean
- `node open-loom.mjs --smoke` output: ok, seven bootstrap references, 21 skills
- Modified skill surfaces under `skills/loom-bootstrap`, `loom-workspace`, `loom-plans`, `loom-ralph`, `loom-debugging`, `loom-git`, `loom-critique`, `loom-records`, `loom-tickets`, `loom-ship`, `loom-spike`, and `loom-skill-authoring`
- Leakage search across `skills/` for `agent-loom`, `open-loom`, `z3z1ma`, `obra/superpowers`, `/Users/alexanderbutler`, `product-surface`, `public docs`, `outside skills/`, `constitutional backing`, and `this package`: no matches after remediation.
- New references under `skills/loom-debugging/references`, `skills/loom-ship/references`, and `skills/loom-skill-authoring/references`
- `README.md` and `PROTOCOL.md`

# Residual Risks

- The adaptation has not been exercised by a future agent on a live end-to-end workflow.
- No external harness install validation was run beyond the local OpenCode smoke check.

# Required Follow-up

None required before operator acceptance. A future golden example for brainstorming -> plan -> Ralph -> critique -> ship -> retrospective would reduce residual risk.

# Acceptance Recommendation

complete pending acceptance
