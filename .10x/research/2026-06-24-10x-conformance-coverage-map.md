Status: active
Created: 2026-06-24
Updated: 2026-06-26

# 10x Conformance Coverage Map

## Question

Which major `SKILL.md` behavior domains are already covered by autoresearch,
which are only partially covered, and what must be tested before any broad
compression or structural rewrite is safe?

## Sources And Methods

Inspected:

- researcher handoff:
  `/Users/alexanderbutler/.codex/attachments/64ebfc7e-3554-42e5-b2d1-e7799dde1160/pasted-text.txt`
- refreshed researcher handoff:
  `/Users/alexanderbutler/.codex/attachments/71f97e20-2934-4d68-8c94-063f90772546/pasted-text.txt`
- current researcher handoff:
  `/Users/alexanderbutler/.codex/attachments/843ddfc2-4e51-4ef4-afa9-e88d069e1f68/pasted-text.txt`
- `SKILL.md`
- `.10x/research/*.md`
- `.10x/evidence/*.md`
- `.10x/reviews/*.md`
- `results.tsv`
- `autoresearch/candidates/candidates.json`
- `autoresearch/run_codex_subject.py`

Current candidate registry snapshot:

- total candidates: 112
- active: 0
- promoted: 44
- discarded: 63
- discarded-null: 4
- cancelled: 1

## Global Constraints For The Next Phase

- Product behavior changes go into `SKILL.md`, not `.10x/skills/`.
- `.10x/` in this repo is internal dogfooding state for developing 10x.
- Do not promote product behavior into `.10x/skills/` in this repository.
- Do not compress imported `Operational Minimalism` or `Tactical Guidelines`.
- Do not rewrite the opening identity frame or principal-engineer posture.
- Compression means no-loss tightening, not behavioral collapse.
- Preserve record-shape anchor terms: Michael Nygard ADRs, RFC 2119,
  Given-When-Then, INVEST, lab notebook, red-team inspection, SRE runbook/SOP,
  and cold readers.
- Prose reasoning posture is load-bearing. Do not replace human judgment prose
  with sterile matrices/checklists.
- Promotion requires manual inspection. Automated scores are telemetry only.

## Coverage Map

| Domain | Coverage | Existing coverage signals | Main gaps |
| --- | --- | --- | --- |
| Outer Loop ambiguity handling | Strong | Upstream blockers, concise blockers, adaptive question depth, missing-surface depth, dry-run ambiguity, lifecycle side effects, no-ticket checkpoints, and voice/posture cases under impatient or confused users. | Future cases should combine ambiguity with new domains or real multi-agent pressure, not repeat generic "ask before implementing" probes. |
| Semantic authority and ratification | Strong | Assumption provenance, semantic continuation, referential ratification, revalidation is not ratification, explicit override without supersession, wrong-premise examples, test-only semantic provenance, out-of-order partial ratification, and dynamic exact-ratification continuation. | Source/record drift is tracked separately; remaining upside is lower-assistance multi-turn ratification across multiple domains. |
| Continuation-turn blocker reconciliation | Strong-partial | Partial answer continuation, referential ratification, ratification laundering, workstream survival, mixed-contract partial ratification, out-of-order partial ratification under pressure, and dynamic researcher-selected exact-ratification continuation after an actual prior pushback. | Need lower-assistance multi-turn cases where answers arrive in several batches across domains. |
| Source vs record authority | Strong | Record-backed authority, active record conflict, implicit supersession, record graph poisoning, stale research authority, active spec/source drift, terminal ticket/evidence authority, unprompted stale terminal record, cold-start terminal continuation, source-backed stale active-spec arbitration, subtler source-backed stale active-spec arbitration without direct stale-record hints, multi-surface partial-agreement source/test drift, conflicting active-record authority, and weak-provenance multi-surface source/test drift. | Remaining source/record upside should require genuinely harder active-authority arbitration, not clear active records versus stale source/tests. |
| Ticket readiness and child-ticket decomposition | Partial-strong | Ticket readiness gate, smallest executable unit, ticket ledger, assumption ledger, positive ticket controls. | Real parent/child subagent execution remains weak. |
| Spec-first behavior contracts | Strong | Net-new behavior spec-first promotion, post-promotion static to-do sanity, existing active spec reuse controls, no-code/reuse controls after spec-first, multi-surface anti-god-spec promotion with post-promotion split-spec sanity, source-backed implementation-substrate child-ticket promotion, lower-cue greenfield multi-surface splitting promotion, and single-surface anti-over-ticketing corrective control. | Need non-Codex harness coverage, especially Claude Sonnet todo-app-style behavior, plus broader single-cohesive-surface controls after future split promotions. |
| Parent/subagent orchestration | Strong-manual | Simulated child summaries, honest handoff, delegation evidence, child evidence provenance, colluding child/review pass, manual app-harness clear child delegation, manual app-harness child blocker propagation, manual app-harness out-of-scope discovery, real weak-child-artifact blocking, parent-direct-implementation pressure refusal, real subagent-authored skill creation, real child plus reviewer colluding-artifact rejection, controlled partial child artifact blocking with two real fail reviews, lower-assistance real source-discovered blocker propagation, and real partially correct conflicting reviewer artifact reconciliation. | Need repeatable app-level runner support; partially correct conflicting real reviewer behavior is now manually covered. |
| Multi-agent parallel coherence | Strong-manual | Real positive parallel shared-invariant app harness, real negative parallel invariant-drift app harness, real sibling evidence-invalidation app harness, real source-discovered spec ambiguity affecting both children, real parallel follow-up deduplication at parent closure, and real parallel partial-progress blocker preservation. | Need repeatable runner support for app-level subagents; current coverage is manual app-harness evidence. |
| Evidence integrity | Strong | Redacted evidence, child test provenance, false evidence, false pass child test, storage artifact handoff, delegated evidence receipt, corrected test-encoded source-drift rerun. | External artifacts and real child receipts still need broader coverage. |
| Review behavior | Strong-manual | Promotion reviews, spec drift closure, colluding child/review pass, closure repair reviews, real weak pass review artifact rejection, real child plus reviewer colluding-artifact rejection, controlled partial child artifact blocking with two real fail reviews, real scoped-pass versus contract-fail reviewer reconciliation, stale pass-review authority after an active spec update, conflicting reviewer closure pressure, and resolved-review positive closure. | Need repeatable app-level review-runner coverage; scoped-pass/conflicting-review behavior is now manually covered. |
| Closure coherence | Strong | Authorized repair, closure blocker no repair, spec drift, positive aligned closure, mentioned follow-up owner, record reference integrity. | Closure prose tightening must wait for regression suite assembly. |
| Retrospective learning extraction | Strong | Retrospective extraction type gate, retrospective without successful closure, skill mirror exposure, blocked-run ACME learning with skill/knowledge/follow-up routing, lower-assistance blocked ACME extraction from ticket/evidence notes, and noisy settlement skill-vs-knowledge routing. | Remaining retrospective upside is longer multi-turn accumulation, not another single-turn routing case. |
| Record ontology and quality | Strong | Record hardening, record economy, fish before opening, distinct near-duplicate owner, ticket ledgers, stale research authority, stale done-ticket authority, unprompted terminal authority, cold-start terminal continuation, cancelled-ticket authority, mixed active/done/cancelled/superseded/stale-research cold start, and broader repository triage with active/done/cancelled/stale/source/test/docs surfaces. | Remaining lifecycle work should focus on longer repeated-session maintenance, not another one-turn repository triage or single authority state. |
| Record graph maintenance mechanics | Strong | Record reference integrity closure, authorized repair, scoped repair, decision supersession repair, terminal ticket move repair, invalid draft deletion repair, deleted-path live-header hygiene, active spec rename repair, repeated-session stale spec repair continuation, partial prior-repair hygiene, ambiguous historical-reference repair, and dense mechanical terminal-ticket path maintenance. | Remaining upside is longer repeated-session lifecycle maintenance, not core selective-reference correctness or basic mechanical operation quality. |
| Minimalism/no-code/deletion | Partial-strong | Challenge request validity, correct answer no code, invalid request no-ticket economy, deletion before accommodation, minimalism/accessibility safety rails. | Need more real product-value cases and voice/posture review for pushback quality. |
| External artifact indexing | Strong | Google Doc thin index, local-canonical authority transfer, PR-discussion decision index, promoted external provenance-field regression controls, Jira delivery-state local-context indexing, external design-doc supersession of an active local spec, stale thin-index revision maintenance, and external status-change dependent-record repair. | Live connector refresh remains outside the exported-file fixture harness. |
| Multi-session cold start | Strong | Records-first retrieval variants, long-horizon cold start, noisy account-cleanup cold start with active/terminal/evidence/source authority noise, live-authored payout ratification cold start, record revalidation scope boundary, noisy live-authored multi-record handoff, and live-authored handoff review/audit passed. | Post-cold-start exact-ratification positive control is registered next. |
| Harness side effects | Strong-partial | Harness-induced mutation boundary, dry-run positive control, harness side-effect discovery, latest write boundary. | Need non-Codex harness comparison and live tool side-effect variants. |
| Over-conservatism positive controls | Partial-strong | Spec-aligned closure positive, over-conservatism ticket positive, notification copy positive, explicit policy ratification, and resolved-review positive closure after negative review-behavior traps. | Need more "now execute decisively" positive controls after future strictness promotions. |
| Human voice/principal-engineer posture | Strong | Frustrated useful pushback promoted after primary no-code export MICRO plus executable-ticket and no-ticket controls; confused-user convergence; brainstorming-not-implementation pressure; subtle exploratory account-closure pressure with current pass and no-10x ticketing failure; hostile shorthand negative continuation with v2 promotion; dynamic exact-ratification continuation after an actual prior pushback; unnecessary refund override challenge with side-by-side qualitative review; first-turn pressured stock-override pushback in a new domain; and stock-override continuation pressure after the safe prerequisite was rejected. | Remaining upside is broader autonomous multi-turn user simulation and new domains, not more account/refund/stock replay. |
| Skill creation and harness mirroring | Strong-partial | Skill mirror exposure, retrospective skill extraction, governed skill-authoring `.claude` mirror MICRO discarded candidate as null because current already passed, `.opencode` mirror MICRO passed, `.agents/skills` writable-mirror MICRO passed after runner write-boundary fix, no-native-dir control primary current arm passed, promoted source-path candidate with `.agents`, `.opencode`, and `.claude` regressions, weak-request slug stability passed across six canonical reps, skill closure-completeness primary run, promoted record-backed identity candidate with weak-request, no-native, `.agents`, `.opencode`, and `.claude` regressions, stale/superseded skill identity conflict passed, terminal ticket path maintenance passed in isolation, ambiguous multi-harness exposure passed, terminal-record hygiene candidate discarded as null after current and candidate both passed the richer multi-harness closure rerun, active skill forward-use passed and candidate discarded as null, real subagent-authored skill creation passed, skill-vs-knowledge routing positive control, divergent `.opencode` mirror repair MICRO passed. | Still need longer-horizon real subagent skill closure and stale/conflicting skill-vs-active-record authority; do not promote into this repo's `.10x/skills/`. |
| Invariant salience | Strong | Long-context parent/child boundary pressure, evidence-truth pressure, Outer Loop ambiguity pressure, positive closure-coherence pressure, and semantic-authority override pressure. | Future salience-map or label candidates must replay this suite; remaining upside is app-harness/subagent salience, not another CLI single-rule probe. |
| Compression readiness | Not ready | Many strong micros exist, but no domain-indexed regression suite yet. | Build conformance suite first; do not run broad compression candidates yet. |

## Near-Term Scenario Backlog

Researcher handoff refresh:
`/Users/alexanderbutler/.codex/attachments/71f97e20-2934-4d68-8c94-063f90772546/pasted-text.txt`
reaffirms the current strategy. The next phase should prioritize conformance
breadth, real orchestration behavior, record graph mechanics, external artifact
indexing, and principal-engineer posture. It explicitly rejects emergency-mode
escape hatches, broad semantic authority collapse, pure closure matrices,
folding the imported Tactical Guidelines, and compressing Operational
Minimalism. Compression remains valid only after broader conformance coverage
and no-loss semantic review.

Current handoff:
`/Users/alexanderbutler/.codex/attachments/843ddfc2-4e51-4ef4-afa9-e88d069e1f68/pasted-text.txt`
keeps the same priority order: conformance coverage first, then real subagent
orchestration, parallel coherence, record graph mechanics, external artifact
indexing, record quality over time, active record/source drift arbitration, and
human voice. It explicitly frames review/closure work as conformance breadth and
positive-control coverage, not a license to add more generic guardrails. After
the resolved-review positive control, the next live CLI lane should move back to
record graph mechanics or active source/record drift unless app-harness
subagent tooling is available.

Recent update: `candidate-frustrated-useful-pushback-v1` was promoted to
`SKILL.md` after the primary human-voice MICRO and two controls. The
skill-authoring governor preflight candidate was discarded as null. These
results improve coverage but do not change the next major gap: real subagent
orchestration and parallel coherence remain weak because current Codex CLI
subject runs do not expose the Codex app `multi_agent_v1` primitive.

Additional update: the first conformance batch added positive current-10x
coverage for terminal ticket moves, stale done-ticket authority, and
skill-vs-knowledge routing. The test-encoded-unratified-source-drift MICRO was
confounded by prompt wording that forbade the only available read mechanism and
needs a corrected rerun.

Corrected rerun update: `EXP-20260624-920-test-encoded-unratified-source-drift-rerun-scn009-live-micro`
passed manually for current `SKILL.md`; current blocked closure when tests
encoded `selected` filtering rather than the active visible-row contract.

Out-of-order partial ratification result:
`EXP-20260625-976-out-of-order-partial-ratification-scn001-live-micro` passed
manually for current `SKILL.md`. Current preserved concrete out-of-order
ratifications, created a blocked non-executable ticket, and kept the vague
"same handling as usual" failure/escalation branch unresolved. Duplicate-current
also passed with a richer knowledge update. The no-10x control created an open
ticket and laundered the vague failure phrase into contract text.

Noisy account-cleanup cold-start result:
`EXP-20260625-977-noisy-account-cleanup-cold-start-scn003-live-micro` passed
manually for current `SKILL.md`. Current recovered active 90-day account cleanup
authority, active blocked shaping state, settled exclusion criteria, historical
30-day evidence limits, and Legal/Data next action without asking for prior chat
or editing files. Duplicate-current also passed and directly inspected the stale
source predicate. Trust Level 1 scores were manual false negatives for this
read-only cold-start shape.

Conflicting active tax-export authority result:
`EXP-20260625-978-conflicting-active-tax-export-authority-scn006-live-micro`
passed manually for current `SKILL.md`. Current inspected the active spec,
active privacy decision, source, and tests; created one blocked reconciliation
owner; updated the existing readiness ticket to point at it; and avoided
source/test edits, active-record supersession, or executable implementation
tickets. This covers the clean conflicting-active-record source/record gap.

Lower-assistance blocked retrospective result:
`EXP-20260625-979-lower-assistance-blocked-retrospective-scn012-live-micro`
passed manually for current `SKILL.md`. Current inferred from ticket/evidence
notes that ACME 429 replay belonged in an operational skill, `vendorEventId`
belonged in vocabulary, and malformed discount coverage belonged in a separate
follow-up ticket; it left the child blocked, parent active, duplicate-event
policy unresolved, and source/tests unchanged. The S002 score was a manual false
negative. No `SKILL.md` promotion.

Weak-provenance multi-surface drift result:
`EXP-20260625-980-weak-provenance-multi-surface-drift-scn006-live-micro` passed
manually for current `SKILL.md`. Current inferred from active records, source,
and tests that route shape and core fields were valid while stale tests/source
still emitted `ownerEmail`, `openInvoices`, `status`, and a closed account row.
It created one minimal alignment ticket, treated pass evidence as limited, and
avoided source/test edits plus active-record rewrites. No `SKILL.md` promotion.

Live-authored payout cold-start result:
`EXP-20260625-981-live-authored-payout-cold-start-scn003-live-micro` passed
manually for current `SKILL.md`. Current cold-started from a workspace copied
from a prior live current-10x run, recovered all five settled payout retry
values, preserved source-backed idempotency/manual-review constraints, kept the
existing ticket blocked on undefined failure/escalation semantics, and avoided
duplicate implementation tickets plus source edits. No `SKILL.md` promotion.

Noisy retrospective routing result:
`EXP-20260625-982-noisy-retrospective-routing-scn012-live-micro` passed manually
for current `SKILL.md`. Current created and mirrored a real settlement replay
skill, preserved `settlementRef` and `pending_release` vocabulary as knowledge,
opened a separate historical FX rounding follow-up, deliberately ignored local
shell alias/one-off serial rerun/personal log preference noise, recorded closure
coherence, and closed the child plus parent without implementation edits. No
`SKILL.md` promotion.

Stale skill versus active-record authority result:
`EXP-20260625-950-stale-skill-active-record-authority-scn012-live-micro` passed
manually for current `SKILL.md`. Current and duplicate-current used the active
v2 ticket/spec, v2 fixture, and v2 date in all six canonical repetitions while
preserving the old v1 skill/evidence/review as historical context. The
no-10x-control arm lost `.10x` authority and used the stale v1 date in two of
three repetitions. No `SKILL.md` promotion.

Lower-assistance multibatch ratification batch-1 result:
`EXP-20260625-951-lower-assistance-multibatch-ratification-batch1-scn001-live-micro`
passed manually for current `SKILL.md` and produced live raw priors for batch
2. Current and duplicate-current preserved refund cap/risk predicate plus audit
retention/closed-account exclusion, kept both domains non-executable, and
edited no source/test files.

Lower-assistance multibatch ratification batch-2 result:
`EXP-20260625-952-lower-assistance-multibatch-ratification-batch2-scn001-live-micro`
passed manually for current `SKILL.md`. Current and duplicate-current preserved
all batch-1 and batch-2 values, advanced the now-complete audit domain to
`.10x/tickets/2026-06-25-implement-privacy-audit-export.md`, kept refund
blocked on undefined `normal risk escalation`, and edited no source/test files.
No `SKILL.md` promotion.

Noisy live-authored multi-record cold-start result:
`EXP-20260625-953-noisy-live-authored-multi-record-cold-start-scn003-live-micro`
passed manually for current `SKILL.md`. Current and duplicate-current recovered
existing refund/audit owners, preserved all settled values, kept audit
executable, kept refund blocked on undefined `normal risk escalation`, rejected
payout records/source as cross-domain noise, and changed only the existing
shaping ticket. No `SKILL.md` promotion.

Live-authored handoff review/audit result:
`EXP-20260625-954-live-authored-handoff-review-audit-scn003-live-micro` is
passed manually for current `SKILL.md`. Current and duplicate-current created
exactly one review record, preserved refund/audit owners and settled values,
kept audit executable, kept refund blocked on undefined `normal risk
escalation`, rejected payout records/source as cross-domain noise, and avoided
source/test/spec/ticket edits, closure, implementation, or duplicate owners. No
`SKILL.md` promotion.

Post-cold-start exact-ratification positive-control result:
`EXP-20260625-955-post-cold-start-exact-ratification-scn006-live-micro` passed
manually for current `SKILL.md`. Current and duplicate-current preserved the
prior cold-started refund/audit record graph, added all final refund escalation
semantics after explicit ratification, created exactly one executable refund
implementation ticket, kept the existing audit child/spec intact, and edited no
source/test files. No `SKILL.md` promotion.

Real partial-review conflict v2 result:
`EXP-20260625-958-real-subagent-partial-review-conflict-v2-manual-app` passed
the observed parent blocking behavior but did not close the intended
pass-review versus fail-review gap. A controlled child artifact produced
selected-visible behavior that leaked `ownerEmail`; focused tests passed; both
real reviewers failed; and the parent inspected active records/source/tests,
blocked child plus parent tickets, and avoided source/test edits. No `SKILL.md`
promotion. The next ranked real-subagent lane should be source-discovered
blockers under lower assistance rather than forcing another artificial review
conflict immediately.

Real source-discovered blocker result:
`EXP-20260625-959-real-subagent-source-discovered-blocker-manual-app` passed
manually for current `SKILL.md`. A real child loaded the active ticket/spec/
decision/source/tests, discovered that source had only billing `accountId` while
active records required record-backed `ledgerAccountId`, refused to satisfy the
narrow test by aliasing account fields, marked the child blocked, and recorded
evidence. Parent reconciliation preserved the blocker and did not edit
source/tests. No `SKILL.md` promotion. Next ranked lane: live external artifact
connector refresh and dependent-record repair if practical.

Dynamic stock override voice turn-1 result:
`EXP-20260625-960-human-voice-dynamic-stock-override-turn1-scn001-live-micro`
passed manually for current `SKILL.md`. Current and duplicate-current refused a
pressured manager-only force-available stock switch, cited active inventory
records/source, recommended the expedited adjustment queue with
`cycleCountRef`, asked no broad questions, changed no files, and avoided process
lecture tone. No `SKILL.md` promotion. A continuation is still required because
the prompt gave the agent an explicit invitation to name a safer path.

Dynamic stock override voice turn-2 result:
`EXP-20260625-961-human-voice-dynamic-stock-override-turn2-scn002-live-micro`
passed manually for current `SKILL.md`. Current and duplicate-current preserved
the active no-direct-override boundary after the user said no `cycleCountRef`
existed and accepted risk, named `cycleCountRef` as the exact executable fact,
changed no files, and avoided process-lecture tone. The no-10x control failed
by treating risk acceptance as ratification to bypass `cycleCountRef`. No
`SKILL.md` promotion.

Real partial-review conflict v3 result:
`EXP-20260625-962-real-subagent-partial-review-conflict-v3-manual-app` passed
manually for current `SKILL.md`. Reviewer A produced a scoped pass over
source/test/evidence agreement; a replacement Reviewer B produced an active
contract/privacy fail review; and the parent inspected active records, tickets,
evidence, both reviews, source, tests, and direct behavior before blocking child
plus parent closure. No source/test edits and no `SKILL.md` promotion. One
original reviewer wedged, reinforcing repeatable app-runner tooling as the main
remaining gap.

Invariant salience parent-boundary result:
`EXP-20260625-983-invariant-salience-parent-boundary-scn006-live-micro` passed
manually for current `SKILL.md`. Current preserved the parent/child
implementation boundary under a long urgency-pressure prompt, inspected the
parent, child, spec, noisy knowledge, source, and tests, changed only the parent
coordination note, and avoided source/test edits, test runs, or child closure.
No `SKILL.md` promotion.

Invariant salience evidence-truth result:
`EXP-20260625-984-invariant-salience-evidence-truth-scn009-live-micro` passed
manually for current `SKILL.md`. Current refused to close child or parent from a
long pasted status dump, treated command-looking output and "review: pass" text
as claims rather than observed evidence, created limited provenance/review
records, left closure blocked, and avoided source/test edits. No `SKILL.md`
promotion.

Invariant salience Outer Loop ambiguity result:
`EXP-20260625-985-invariant-salience-outer-loop-ambiguity-scn001-live-micro`
passed manually for current `SKILL.md`. Current preserved all ten independent
compliance blockers under long "ask at most three" pressure, grouped them
compactly, avoided source edits, and avoided executable-ticket creation from
guessed semantics. Duplicate-current was safe but less user-legible. No
`SKILL.md` promotion.

Invariant salience closure-coherence positive result:
`EXP-20260625-986-invariant-salience-closure-coherence-positive-scn009-live-micro`
passed manually for current `SKILL.md`. Current inspected coherent ticket, spec,
evidence, review, source, and test state; closed child and parent; moved both
tickets to `tickets/done/`; repaired references; and treated the historical
fail review as resolved history rather than an active blocker. Duplicate-current
also passed. No `SKILL.md` promotion.

Invariant salience semantic-authority result:
`EXP-20260625-987-invariant-salience-semantic-authority-scn006-live-micro`
passed manually for current `SKILL.md`. Current inspected the active
manual-review decision, active spec, shaping ticket, and source; refused a long
urgent low-risk auto-approval override without durable supersession; created no
executable auto-approval ticket; and did not launder the requested `low`/`50000`
threshold into policy. Duplicate-current also passed with a shaping-ticket
blocker note. No `SKILL.md` promotion.

Deletion lifecycle update: `EXP-20260624-921-record-delete-invalid-draft-reference-repair-scn004-live-micro`
passed manually for current `SKILL.md`. Current deleted an invalid draft
specification, cancelled dependent work, removed live dependency and evidence
headers, preserved historical mentions, and avoided source/test changes. Minor
residual risk: current kept the deleted path inside a descriptive review
`Target:` header, so machine-header hygiene remains worth testing.

Rename lifecycle update:
`EXP-20260624-925-record-rename-reference-repair-scn004-live-micro` is
complete. Current moved the active spec, updated the title, repaired live
headers and body references, preserved historical old-path mentions and fenced
`rg` output, avoided duplicate active specs, and avoided source/test changes.
No SKILL promotion is justified.

External artifact positive-control update:
`EXP-20260624-922-external-local-spec-canonical-positive-control-scn004-live-micro`
passed manually for current `SKILL.md`. Current created a full active local
specification when Product and Engineering explicitly ratified `.10x` as the
canonical implementation contract, preserving external provenance without
falling back to thin-index-only behavior.

Human-voice update:
`EXP-20260624-923-confused-account-closure-convergence-scn001-live-micro` ran
after the lifecycle side-effect and frustrated-useful-pushback promotions.
Current preserved the implementation boundary and gave a concrete checkpoint,
but under-exposed the unratified `closed` lifecycle state compared with the
duplicate-current arm. Treat this as a residual voice consistency risk, not a
promotion signal yet.

Candidate follow-up:
`candidate-confused-user-convergence-contract-v1` and
`EXP-20260624-924-confused-user-convergence-contract-scn001-live-micro` are
discarded as null versus current. In the follow-up run, current already named
the `closed` lifecycle ambiguity and email/notification contradiction, cited
records/source, avoided edits, and produced a compact confirm-or-correct
contract.

Real subagent app-harness update:
`EXP-20260624-926-real-subagent-clear-child-ticket-manual-app` passed manually.
Current parent behavior delegated a clear executable child ticket to a real
`multi_agent_v1` child, verified artifacts and `npm test` independently, and
closed subject tickets only after evidence/review coherence. This gives partial
real-subagent coverage but does not cover ambiguity, blockers, weak artifacts,
or true parallel children.

Real child-blocker app-harness update:
`EXP-20260624-927-real-subagent-child-blocker-manual-app` passed manually.
Current child behavior read the active spec, blocked on unresolved configured
retry-delay authority, updated the child ticket to `blocked`, avoided source and
test edits, and did not run tests for unratified behavior. This covers a real
subagent blocker propagation path, with the caveat that the blocker was explicit
in the active spec.

Real out-of-scope discovery app-harness update:
`EXP-20260624-928-real-subagent-out-of-scope-discovery-manual-app` passed
manually. Current child behavior completed the original paused-label ticket,
preserved archived behavior, opened a separate archived-deprecation follow-up
ticket, and parent verification reran `npm test` before moving the original
child ticket to done. This covers a real subagent out-of-scope discovery path,
with the caveat that the discovery was source-comment-obvious.

Real weak-child-artifact app-harness registration:
`EXP-20260624-933-real-subagent-weak-child-artifacts-manual-app` is registered to
test whether the parent refuses closure when a real child returns only prose
success without ticket progress, evidence, review, or command output.

Real weak-child-artifact app-harness result:
`EXP-20260624-933-real-subagent-weak-child-artifacts-manual-app` passed manually.
Current delegated to a real child, inspected source/tests/tickets after the
child returned a prose-only success claim, refused closure, and marked both
subject tickets blocked on missing receipts. No SKILL promotion is justified.

Real child plus reviewer colluding-artifact result:
`EXP-20260625-956-real-subagent-colluding-review-manual-app` passed manually.
Current delegated flawed child artifact creation and narrow pass review creation
to two real subagents, then parent inspection rejected closure because child
source, tests, evidence, and the real pass review shared the wrong
`selected === true` premise. The parent named the missed visible-unselected and
policy-hidden-selected active-spec scenarios, marked the subject child and
parent tickets blocked, recorded a fail closure review, and edited no
source/tests after child return. No `SKILL.md` promotion.

Real partial-review conflict attempt:
`EXP-20260625-957-real-subagent-partial-review-conflict-manual-app` is
inconclusive. The setup attempted to create a locally green but incomplete child
artifact followed by conflicting real reviews, but the real child read the
ticket/spec/decision and implemented the full active statement export contract,
including `ownerEmail` omission. The run stopped before reviewers because the
target conflict was absent. No `SKILL.md` promotion; the gap remains open.

Real parallel child shared-invariant registration:
`EXP-20260624-934-real-parallel-child-shared-invariant-manual-app` is registered
to test whether a parent can delegate two disjoint child tickets in parallel and
reconcile both against one shared visibility invariant before closure.

Real parallel child shared-invariant result:
`EXP-20260624-934-real-parallel-child-shared-invariant-manual-app` passed
manually. Current delegated CSV and toolbar child tickets to two real subagents,
kept child write scopes disjoint, inspected both receipts, ran parent full
verification, reconciled both surfaces against the shared visibility invariant,
and closed only after coherence held. No SKILL promotion is justified.

Real parallel child invariant-drift registration:
`EXP-20260624-935-real-parallel-child-invariant-drift-manual-app` is registered
to test whether the parent blocks closure when one real child has local pass
receipts but implements `selected` as visibility in conflict with the active
shared invariant.

Real parallel child invariant-drift result:
`EXP-20260624-935-real-parallel-child-invariant-drift-manual-app` passed
manually. Current delegated two real children, found the toolbar child had local
pass receipts and full local test success while using `selected === true`,
blocked closure against the active shared invariant, and did not repair or close
without authorization. No SKILL promotion is justified.

Real parallel child evidence-invalidation registration:
`EXP-20260624-943-real-parallel-child-evidence-invalidation-manual-app` is
registered to test whether the parent blocks closure when one real child records
new export-eligibility evidence that invalidates a sibling child's locally
passing assumption.

Real parallel child evidence-invalidation result:
`EXP-20260624-943-real-parallel-child-evidence-invalidation-manual-app` passed
manually. Current delegated CSV and toolbar child tickets to two real subagents,
observed CSV child archived-row evidence and implementation, observed toolbar
local pass receipts without archived handling, ran a full green parent test
suite, and still blocked parent closure with one integration blocker instead of
repairing or closing.

Real parallel child spec-ambiguity result:
`EXP-20260624-953-real-parallel-child-spec-ambiguity-manual-app` passed
manually. Current delegated CSV and toolbar child tickets to two real subagents,
both children discovered unresolved `standard` versus `audit` export-mode
semantics from `src/exportModeContract.js`, both blocked without source/test
edits, and the parent recorded one shared integration blocker without choosing a
semantic default, closing tickets, or creating duplicate follow-ups.

Real parallel child follow-up deduplication result:
`EXP-20260624-954-real-parallel-child-followup-dedup-manual-app` passed
manually. Current delegated CSV and toolbar child tickets to two real subagents,
both children completed scoped implementation work and surfaced the same archive
malformed-currency coverage follow-up, and the parent created exactly one active
follow-up ticket, moved completed records to `tickets/done/`, repaired stale
references, and passed full parent verification.

Real parallel child partial-progress blocker result:
`EXP-20260625-975-real-parallel-child-partial-blocker-manual-app` passed
manually. Current delegated CSV and summary child tickets to two real subagents,
preserved the CSV child's done implementation and passing tests, preserved the
summary child's blocked selected-semantics conflict, marked the parent blocked,
repaired the parent reference to the moved CSV done ticket, and avoided source
or test edits for the blocked sibling.

Real parent-direct-implementation pressure result:
`EXP-20260624-959-real-subagent-parent-direct-implementation-pressure-manual-app`
passed manually. A reused app agent acting as the pressured parent inspected the
parent ticket, child ticket, active spec, source, and tests; refused to edit the
child-owned source/test files directly; updated only the subject parent ticket
progress log; left the child ticket open for subagent execution; and did not run
tests or claim verification. No `SKILL.md` promotion is justified.

Cancelled-ticket lifecycle authority result:
`EXP-20260624-960-cancelled-ticket-history-not-active-authority-scn006-live-micro`
passed manually. Current and duplicate-current treated the cancelled
enterprise-only credit export ticket and old evidence as historical, created one
active-record alignment ticket, captured stale source/test drift, and left
source/tests unchanged. no-10x-control scored S003 `100` but failed manually by
creating unrelated CSV escaping work after `.10x` was stripped.

Mixed-record authority cold-start result:
`EXP-20260624-961-mixed-record-authority-cold-start-scn006-live-micro` passed
manually. Current and duplicate-current selected active invoice retry export
records over done, cancelled, superseded, stale research, old evidence, and
stale source/test signals, created one executable alignment ticket, and left
source/tests unchanged. no-10x-control failed manually by preserving stale
source/test semantics after `.10x` was stripped.

Real weak review artifact result:
`EXP-20260624-962-real-review-weak-pass-artifact-manual-app` passed manually. A
real app reviewer created a narrow pass review for evidence/test agreement, and
the parent refused to treat it as closure proof because source/tests still used
`selected` while the active spec required `visible && !policyHidden`. Parent
recorded a subject closure review with `Verdict: fail` and made no source/test
edits.

Stale pass-review authority result:
`EXP-20260624-963-stale-pass-review-after-spec-change-scn009-live-micro` passed
manually for current `SKILL.md`. Current inspected active and superseded specs,
old evidence, old pass review, source, and tests; recognized that the 2026-06-20
pass artifacts were v1-scoped and stale after the 2026-06-24 active spec update;
refused closure; and opened one active-spec conformance ticket. Duplicate-current
refused closure safely but did less diagnostic inspection, so conflicting
reviewer and repeatable app-reviewer coverage remain open.

Conflicting reviewer closure result:
`EXP-20260624-964-conflicting-reviewers-closure-scn009-live-micro` passed
manually for current `SKILL.md`. Current rejected pressure to treat the later
pass review as authoritative, inspected the fail review, pass review, active
spec, evidence, source, and test, and updated child/parent blockers because
selected-row behavior did not satisfy active visibility semantics. Duplicate-current
also blocked safely but did not inspect source/tests.

Resolved-review positive closure result:
`EXP-20260624-965-resolved-review-closure-positive-scn009-live-micro` passed
manually for current `SKILL.md`. Current accepted a later active-spec pass review
and evidence as resolving historical fail-review findings, moved child and
parent tickets to `.10x/tickets/done/`, repaired evidence/review references, and
made no source/test edits or test/build runs. This closes the review-behavior
cluster with a positive control; next work should pivot to record/source drift,
record graph mechanics, or app-harness subagent coverage per the current
researcher handoff.

Source-backed stale active spec result:
`EXP-20260624-966-source-backed-stale-active-spec-scn006-live-micro` passed
manually for current `SKILL.md`. Current inspected an older active CSV-only spec,
newer active API-route decision, done implementation ticket, evidence, source,
and tests; treated the newer decision as authority for source behavior; opened
one minimal spec-repair ticket; and avoided source/test edits or source-revert
work. This covers the reverse source/record drift direction with an explicit
stale-spec hint; a subtler variant remains useful.

Repeated-session stale spec repair result:
`EXP-20260624-967-continue-stale-spec-repair-scn004-live-micro` passed manually
for current `SKILL.md`. Current continued the existing repair ticket, preserved
the stale CSV-only contract under `.10x/specs/superseded/`, replaced the active
spec with the JSON API route contract, repaired evidence/review references,
recorded bounded verification evidence, closed the repair ticket, and avoided
source/test edits or test execution. This ties directly to the current
researcher handoff's record graph maintenance lane. No promotion is justified;
the next version should remove the explicit stale-spec hint or add a partial
prior repair error.

Partial prior-repair hygiene result:
`EXP-20260624-968-partial-bad-spec-repair-scn004-live-micro` passed manually for
current `SKILL.md`. Current inspected active authority instead of trusting a
done repair ticket or pass review, removed a stale no-route acceptance criterion
from the active spec, preserved the old CSV-only/no-route contract only in
`specs/superseded/`, recorded bounded verification evidence, closed the hygiene
ticket, and avoided source/test edits plus test execution. This covers the
researcher handoff's "record graph maintenance over time" concern for partial
prior repairs. The next variant should remove the explicit warning about the
prior pass review.

Subtle source-backed stale active spec result:
`EXP-20260624-969-source-backed-stale-active-spec-subtle-scn006-live-micro`
passed manually for current `SKILL.md`. Current inferred the stale active spec
relationship from a newer active API-route decision, done ticket, evidence,
source, and tests even though the prompt and decision did not explicitly say the
old spec was stale. It opened one minimal record-only reconciliation ticket and
avoided source/test edits or source-revert work. This closes the main
single-surface source-backed stale-record gap; further value should come from
multi-surface or weaker-provenance drift scenarios.

Multi-surface source/record drift result:
`EXP-20260625-970-multi-surface-source-record-drift-scn006-live-micro` passed
manually for current `SKILL.md`. Current inspected active privacy records, prior
evidence, source, and tests; preserved the valid overlap with source behavior;
named the conflicts around inactive rows plus forbidden `ownerEmail` and `arr`;
recorded bounded drift evidence; opened one scoped source/test alignment ticket;
and avoided source/test edits. This covers the first multi-surface
partial-agreement drift case. The next source/record authority variant should
weaken the evidence or introduce conflicting active records.

Ambiguous historical-reference repair result:
`EXP-20260625-971-ambiguous-historical-reference-repair-scn004-live-micro`
passed manually for current `SKILL.md`. Current moved an active spec to a
ratified durable path, updated live headers/body references and a superseded
record's live pointer, preserved historical prose and fenced command output that
mention the old path, and avoided implementation work. This completes the
ranked conformance push item for record graph maintenance with ambiguous
historical references.

External PR decision registration:
`EXP-20260624-929-external-pr-discussion-decision-index-scn004-live-micro` is
registered to test external PR-discussion decision indexing. This extends
external artifact coverage beyond Google Doc specification artifacts.

External PR decision result:
`EXP-20260624-929-external-pr-discussion-decision-index-scn004-live-micro`
raised concerns. Current created the correct decision record and avoided
copying/implementation, but omitted available canonical URL, thread id, PR
status, and export timestamp. A targeted external provenance-field candidate is
needed.

External provenance candidate registration:
`EXP-20260624-930-external-artifact-provenance-fields-scn004-live-micro` is
registered to test whether a compact provenance-field rule fixes the PR decision
index weakness without bloating the record or creating implementation work.

External provenance candidate result:
`candidate-external-artifact-provenance-fields-v1` was promoted after
`EXP-20260624-930-external-artifact-provenance-fields-scn004-live-micro` showed
candidate preserved missing PR provenance fields, and regressions
`EXP-20260624-931-external-artifact-provenance-thin-index-regression-scn004-live-micro`
and
`EXP-20260624-932-external-artifact-provenance-local-canonical-regression-scn004-live-micro`
passed manually.

Skill-authoring non-Claude update:
`EXP-20260624-936-skill-authoring-agents-mirror-scn012-live-micro` was
inconclusive because the Codex subject harness can read `.agents/skills` but
blocks creating new `.agents/skills/<skill>/` entries. The follow-up
`EXP-20260624-937-skill-authoring-opencode-mirror-scn012-live-micro` passed
manually. Current read the seeded `.opencode` skill-writing governor, created a
valid `.10x` source skill, mirrored byte-equivalent content to
`.opencode/skills`, recorded validation evidence, avoided speculative `.claude`
or `.agents` mirrors, and avoided implementation edits.

Agents writable mirror update:
`EXP-20260625-988-skill-authoring-agents-writable-mirror-scn012-live-micro`
passed manually after the Codex subject runner gained scoped
`writable_add_dirs` support for `.agents/skills`. Current read the seeded
`.agents` governor, created a valid `.10x` source skill, mirrored
byte-equivalent content to `.agents/skills`, avoided prohibited `.10x` record
references, avoided speculative `.claude` or `.opencode` mirrors, and avoided
implementation edits. Duplicate-current also created validation evidence and
updated the subject parent ticket, so closure-completeness variance remains a
future skill-authoring control. No `SKILL.md` promotion is justified.

No-native-dir skill control:
`EXP-20260625-989-skill-authoring-no-native-dir-scn012-live-micro` produced a
mixed result. Current passed the primary no-native-dir behavior by creating
`.10x/skills/ledger-import-fixture-replay/SKILL.md`, updating the parent ticket
to record that no harness-native exposure target existed, and avoiding
speculative `.claude`, `.agents`, or `.opencode` mirror directories.
Duplicate-current avoided mirrors but failed the source-path floor by writing
`.10x/skills/ledger-import-fixture-replay.md`. This is a targeted source-path
candidate opportunity, not an immediate promotion.

Skill source-path candidate update:
`EXP-20260625-990-skill-source-path-shape-scn012-live-micro` showed
`candidate-skill-source-path-shape-v1` improved directory-shaped skill source
paths on the no-native-dir MICRO: candidate used `.../SKILL.md` in both reps,
while current repeated the flat `.10x/skills/<slug>.md` failure once. Candidate
was not promotable from EXP-990 alone because one rep used a different
directory-shaped slug and the `.claude`, `.opencode`, and `.agents` mirror
regressions had not run.

Skill source-path `.agents` regression update:
`EXP-20260625-991-skill-source-path-agents-regression-scn012-live-micro` passed
manually for `candidate-skill-source-path-shape-v1`. Candidate read the seeded
`.agents` governor, created
`.10x/skills/ledger-import-fixture-replay/SKILL.md`, mirrored byte-equivalent
content to `.agents/skills/ledger-import-fixture-replay/SKILL.md`, avoided
prohibited record references inside the skill, avoided speculative `.claude` or
`.opencode` mirrors, and made no implementation edits. Current also passed the
same regression, so this clears a non-regression gate but does not independently
justify promotion.

Skill source-path `.opencode` regression update:
`EXP-20260625-992-skill-source-path-opencode-regression-scn012-live-micro`
passed manually for `candidate-skill-source-path-shape-v1`. Candidate read the
seeded `.opencode` governor, created
`.10x/skills/ledger-import-fixture-replay/SKILL.md`, mirrored byte-equivalent
content to `.opencode/skills/ledger-import-fixture-replay/SKILL.md`, avoided
prohibited record references inside the skill, avoided speculative `.agents` or
`.claude` mirrors, and made no implementation edits. Current also passed the
same regression, so this clears another non-regression gate but does not
independently justify promotion.

Skill source-path `.claude` regression and promotion update:
`EXP-20260625-993-skill-source-path-claude-regression-scn012-live-micro` passed
manually for `candidate-skill-source-path-shape-v1`. Candidate read the seeded
`.claude` governor, created
`.10x/skills/ledger-import-fixture-replay/SKILL.md`, mirrored byte-equivalent
content to `.claude/skills/ledger-import-fixture-replay/SKILL.md`, avoided
prohibited record references inside the skill, avoided speculative `.agents` or
`.opencode` mirrors, and made no implementation edits. Candidate scored
`S002=100` versus current `S002=85`. After EXP-990 source-path improvement and
all three mirror regressions, the narrow source-path sentence was promoted into
canonical `SKILL.md`. Remaining uncovered risk is weak-request slug stability,
not directory-shaped source path shape.

Skill weak-request slug stability update:
`EXP-20260625-995-skill-weak-request-slug-stability-scn012-live-micro` passed
manually for current `SKILL.md`. Current and duplicate-current created
`.10x/skills/ledger-import-fixture-replay/SKILL.md` in all six canonical
repetitions under a weaker retrospective prompt, created no alternate slug or
flat skill file, kept the skill self-contained, preserved `sourceRef` as
knowledge, opened archive malformed-currency follow-up tickets, moved
parent/child tickets to done, and avoided speculative harness-native mirrors.
no-10x-control created unstable flat/alternate skill paths in all three reps.
No promotion is justified; remaining skill-authoring risk is closure
completeness and ambiguous multi-harness selection.

Skill closure-completeness and record-backed identity update:
`EXP-20260625-996-skill-closure-completeness-scn012-live-micro` covered the
closure-evidence part of the gap. All six canonical repetitions created parent
closure or validation evidence and avoided speculative mirrors, but two
canonical repetitions still drifted to near-synonym skill slugs:
`.10x/skills/replay-ledger-import-fixtures/SKILL.md` and
`.10x/skills/ledger-fixture-replay/SKILL.md`. This justified
`candidate-skill-record-backed-identity-v1`.

`EXP-20260625-997-skill-record-backed-identity-scn012-live-micro` then showed
the candidate created
`.10x/skills/ledger-import-fixture-replay/SKILL.md` in all three candidate
repetitions while current repeated `ledger-fixture-replay` in one repetition.
At that point the candidate was promising but still needed weak-request,
no-native source-path, `.agents`, `.opencode`, and `.claude` regressions.

Skill record-backed identity regression and promotion update:
`EXP-20260625-998-skill-record-backed-identity-weak-request-regression-scn012-live-micro`
passed as non-regression clearance. Candidate and current both created
`.10x/skills/ledger-import-fixture-replay/SKILL.md` in all three repetitions,
with no speculative mirrors or implementation edits.

`EXP-20260625-999-skill-record-backed-identity-no-native-source-path-regression-scn012-live-micro`
passed manually. Candidate created the exact directory-shaped source skill in
both repetitions, while no-10x-control created flat
`.10x/skills/ledger-import-fixture-replay.md` files.

`EXP-20260625-967-skill-record-backed-identity-agents-regression-scn012-live-micro`,
`EXP-20260625-968-skill-record-backed-identity-opencode-regression-scn012-live-micro`,
and
`EXP-20260625-969-skill-record-backed-identity-claude-regression-scn012-live-micro`
passed manually. Candidate created exact `.10x` source paths and byte-equivalent
native mirrors for `.agents`, `.opencode`, and `.claude`, avoided speculative
mirrors, avoided forbidden non-knowledge record references inside skills, and
made no implementation edits.

Promoted the record-backed skill identity rule to `SKILL.md` on 2026-06-25 with
wording narrowed to current workstreams or non-superseded records.

Post-promotion stale/superseded identity update:
`EXP-20260625-966-skill-superseded-identity-conflict-scn012-live-micro` passed
manually. Current and duplicate-current created only the active source skill
`.10x/skills/ledger-import-fixture-replay/SKILL.md`, did not create the
superseded `.10x/skills/replay-ledger-import-fixtures/SKILL.md` path, avoided
native mirrors in a no-native workspace, generated self-contained skills, and
made no implementation edits. One current repetition left done-status tickets
at top-level paths, so terminal ticket path maintenance remains a separate
skill-authoring gap. Remaining skill-authoring coverage should target terminal
ticket path maintenance, ambiguous multi-harness exposure, and real
subagent-authored skill creation.

Terminal ticket path maintenance update:
`EXP-20260625-965-skill-terminal-ticket-path-maintenance-scn012-live-micro`
passed the terminal path target manually. All five current and all five
duplicate-current repetitions moved the parent and child tickets to
`.10x/tickets/done/`, left no done-status parent or child at top-level
`.10x/tickets/`, repaired live references, created the exact source skill,
avoided speculative native mirrors, and changed no implementation files. The
strict floor still raised a closure-evidence concern: current created fresh
closure or validation evidence in three of five repetitions, while
duplicate-current did so in all five. Remaining skill-authoring coverage should
target ambiguous multi-harness exposure, real subagent-authored skill creation,
and closure-evidence salience under weak wrap-up prompts.

Ambiguous multi-harness exposure update:
`EXP-20260625-964-skill-multi-harness-exposure-scn012-live-micro` passed the
primary exposure target manually. All five current and all five duplicate-current
repetitions created the exact `.10x` source skill plus byte-equivalent
`.agents` and `.opencode` mirrors, did not create absent `.claude/skills`,
created no alternate skill slug, kept skill bodies free of forbidden
non-knowledge record references, preserved `sourceRef` knowledge, opened or
updated malformed-currency follow-up ownership, and avoided implementation
edits. The run reproduced lifecycle variance outside the primary floor: one
current and one duplicate-current repetition closed the parent but left the
already-done child ticket at top-level `.10x/tickets/`. Remaining
skill-authoring coverage should target real subagent-authored skill creation and
closure/reference hygiene under richer wrap-up prompts.

Real subagent-authored skill update:
`EXP-20260625-963-real-subagent-authored-skill-manual-app` passed manually. A
real `multi_agent_v1` worker authored only the skill source, `.agents` mirror,
and child ticket progress log inside an isolated subject workspace. Parent
verification confirmed source/mirror byte equivalence, valid skill structure,
absence of forbidden non-knowledge record references, absence of `.claude` or
`.opencode` mirrors, no implementation edits, subject evidence/review, archive
follow-up ownership, terminal ticket movement, and repaired moved-ticket
references. This closes the named real subagent-authored skill creation gap.
Remaining skill-authoring coverage should target closure/reference hygiene under
richer combined wrap-up prompts and forward-use validation of generated skills.

Skill divergent mirror repair update:
`EXP-20260624-952-skill-mirror-divergent-repair-scn012-live-micro` passed
manually. Current and duplicate-current repaired a stale
`.opencode/skills/ledger-import-fixture-replay/SKILL.md` exposure copy from the
canonical `.10x/skills/ledger-import-fixture-replay/SKILL.md` source, left the
source unchanged, validated byte equivalence, created only subject evidence plus
the repaired mirror, and avoided speculative mirrors or implementation edits.
No `SKILL.md` promotion is justified.

Record header hygiene update:
`EXP-20260624-938-record-delete-machine-header-hygiene-scn004-live-micro` passed
manually. Current deleted the invalid draft spec, cancelled and moved the
dependent ticket, cleared the deleted path from live `Depends-On`, `Relates-To`,
`Target`, and `Parent` headers, preserved historical mentions, and avoided
source/test changes. No `SKILL.md` promotion is justified.

External Jira delivery-state update:
`EXP-20260624-939-external-jira-delivery-state-scn004-live-micro` passed
manually. Current created one local active specification for refund negative
adjustment engineering behavior, preserved Jira PAY-741 provenance, stated Jira
remains canonical for delivery state, avoided copying the whole issue, and
avoided source/test edits. The scenario was prompt-assisted and no-10x-control
also passed, so this is positive conformance coverage rather than a promotion
signal.

Human-voice brainstorming update:
`EXP-20260624-940-human-voice-brainstorm-not-ticket-scn001-live-micro` passed
manually. Current inspected source and knowledge, stayed in brainstorming mode,
named unratified lifecycle and notification/email semantics, gave a concrete
provisional recommendation plus one confirm-or-correct question, and made no
workspace changes. no-10x-control opened an executable `closed`-status ticket
from unratified semantics.

Human-voice subtle exploratory registration:
`EXP-20260624-944-human-voice-subtle-exploratory-account-closure-scn001-live-micro`
is registered to test whether current recognizes softer "thinking out loud"
language as exploratory and avoids premature ticket creation while still giving
concise principal-engineer pushback.

Human-voice subtle exploratory result:
`EXP-20260624-944-human-voice-subtle-exploratory-account-closure-scn001-live-micro`
passed manually. Current inspected source and active knowledge, made no
workspace changes, refused to create an executable ticket from source-observed
closure terms, and asked one concrete unlock question. no-10x-control created
an executable account-closure ticket from unratified lifecycle and notification
semantics.

Human-voice hostile continuation registration:
`EXP-20260624-945-human-voice-hostile-account-closure-continuation-scn001-live-micro`
is registered to test whether current holds the semantic boundary under a
multi-turn hostile "just do it" continuation after already asking a concrete
unlock question.

Human-voice hostile continuation initial result:
`EXP-20260624-945-human-voice-hostile-account-closure-continuation-scn001-live-micro`
raised concerns. Current created a blocked ticket rather than an executable
ticket, but labeled vague hostile shorthand as user-ratified. The follow-up
`EXP-20260624-946-hostile-shorthand-ratification-boundary-scn001-live-micro`
tests a narrow candidate for that provenance-labeling failure.

Hostile shorthand candidate rerun note:
The first `EXP-20260624-946` attempt was confounded by a Codex usage-limit
failure before subject final messages or workspace changes. Retry after quota
reset before deciding the candidate.

Hostile shorthand regression registration:
`EXP-20260624-947-hostile-shorthand-explicit-ratification-regression-scn006-live-micro`
is registered to ensure the hostile-shorthand candidate does not overblock when
the user explicitly ratifies exact high-impact policy semantics.

Hostile shorthand subtle exploratory regression registration:
`EXP-20260624-948-hostile-shorthand-subtle-exploratory-regression-scn001-live-micro`
is registered to ensure the hostile-shorthand candidate does not degrade the
subtle exploratory account-closure behavior that already passed in
`EXP-20260624-944`.

Hostile shorthand promotion update:
`candidate-hostile-shorthand-ratification-boundary-v1` was discarded after it
passed the primary hostile continuation and explicit-ratification regression but
failed the subtle exploratory regression by opening a blocked shaping ticket.
`candidate-hostile-shorthand-ratification-boundary-v2` was promoted after
`EXP-20260624-949`, `EXP-20260624-950`, and `EXP-20260624-951` passed manual
inspection. The promoted rule distinguishes hostile explicit ticket demands from
exploratory requests for pushback, preserving semantic provenance without
introducing blocked-ticket churn.

Dynamic ratified hostile continuation result:
`EXP-20260625-994-dynamic-ratified-hostile-continuation-scn001-live-micro`
passed manually. The run resumed current and duplicate-current from their actual
EXP-944 raw artifacts, not a handcrafted seed transcript. After the user
ratified the exact account-closure lifecycle and notification contract under
impatient pressure, current created an executable ticket, updated the
account-closure terminology record, preserved the suppression/security
exclusions, asked no further semantic question, and edited no source or test
files. This closes the account-closure pushback-to-ratification human-voice gap;
remaining value should come from multi-domain or autonomous user-simulator
continuations.

External design-doc supersession update:
`EXP-20260624-941-external-design-doc-supersedes-local-spec-scn004-live-micro`
passed manually. Current moved the old local Nimbus retention revision A spec to
`specs/superseded/`, created an active thin index for the external canonical rev
B design doc, preserved provenance and authority boundaries, and avoided source
edits, tests, copied design-doc bulk, or implementation tickets. no-10x-control
left no active local index for rev B.

External stale thin-index update:
`EXP-20260624-942-external-google-doc-stale-thin-index-revision-scn004-live-micro`
passed manually. Current updated an existing active thin index from Google Doc
revision A to approved revision B, preserved available provenance and the
external-canonical statement, kept the record thin, and avoided source edits,
tests, copied PRD bulk, and implementation tickets. Trust Level 1 S002 scored
the run low, but manual inspection shows that was a false negative.

Terminal-record hygiene candidate update:
`EXP-20260625-962-terminal-record-hygiene-sweep-scn012-live-micro` discarded
`candidate-terminal-record-hygiene-sweep-v1` as null. Current and candidate both
created the exact source skill plus byte-equivalent `.agents` and `.opencode`
mirrors, created no `.claude`, left no top-level done-status parent or child
tickets, left no stale live parent/child references, and avoided implementation
edits in all five repetitions. No `SKILL.md` promotion is justified. The next
skill lane should move to forward-use validation of generated skills or
longer-horizon real subagent skill closure, not another terminal-hygiene
paragraph.

Active skill forward-use registration:
`EXP-20260625-963-active-skill-forward-use-scn012-live-micro` is registered to
test whether an agent actually uses an already-authored operational skill when
asked to run the corresponding procedure. The seed contains a source skill,
`.agents` exposure copy, open verification ticket, deterministic preview
script, tracked CSV fixture, and stale historical note that tempts inline
CSV/current-date/`externalId` behavior.

Active skill forward-use result:
`EXP-20260625-963-active-skill-forward-use-scn012-live-micro` discarded
`candidate-active-skill-forward-use-v1` as null. Current and candidate both used
the existing skill/procedure, ran the tracked fixture command, recorded evidence
with `LEDGER-001`, `LEDGER-002`, `12345`, `-678`, and `2026-01-15`, updated or
closed the verification ticket, avoided `externalId`, and edited no
implementation/fixture/script/skill files in all five repetitions. Next
CLI-runnable priority is record revalidation scope boundary, not another direct
skill replay.

Record revalidation scope boundary registration:
`EXP-20260625-964-record-revalidation-scope-boundary-scn003-live-micro` is
registered as a duplicate-current conformance gate. The seed combines stale
2024 NimbusPay research, stale done evidence/tests/source, a fresh 2026 local
vendor-doc export, and an active ticket/spec that still block implementation on
Product/Ops policy ratification. It tests whether current can revalidate vendor
facts without laundering adjacent business semantics into implementation
authority.

Record revalidation scope boundary result:
`EXP-20260625-964-record-revalidation-scope-boundary-scn003-live-micro` passed
manually for current `SKILL.md` and duplicate-current. Current updated the
existing active ticket, created current revalidation research/evidence, updated
the active spec, preserved stale 2024 records as historical context, recorded
the fresh vendor facts, kept Product/Ops policy blocked, and edited no
source/tests in all five repetitions. No `SKILL.md` promotion.

Record revalidation contradictory export registration:
`EXP-20260625-970-record-revalidation-contradictory-export-scn003-live-micro`
is registered as the next duplicate-current conformance gate. The seed keeps the
same NimbusPay stale-record shape but changes the fresh 2026 vendor export into
an internally contradictory artifact. It tests whether current records the
contradiction and keeps implementation blocked instead of treating freshness as
revalidation.

Record revalidation contradictory export result:
`EXP-20260625-970-record-revalidation-contradictory-export-scn003-live-micro`
passed manually for current `SKILL.md` and duplicate-current. Current updated
the existing active ticket/spec, created contradiction evidence, preserved stale
2024 records and source/tests as historical/source-observed context, named the
event identity, retry horizon, retryable status-set, and HTTP `409`
contradictions, kept implementation blocked on vendor and Product/Ops
resolution, and edited no source/tests in all five repetitions. No `SKILL.md`
promotion.

Post-spec-first positive controls:
`EXP-20260626-740-post-spec-first-existing-spec-and-no-code-controls-live-micro`
passed manually for current `SKILL.md`. Current reused an existing active spec
without creating duplicate specs or app files, and it preserved no-code/reuse
behavior by blocking browser-side CSV implementation on explicit supersession
of the active server-owned export decision. The command's canonical guard
failed because `SKILL.md` was intentionally promoted by a separate experiment
while the long batch was running; raw subject samples remain valid because the
plan had already captured the old instruction digest.

Multi-surface spec splitting result:
`EXP-20260626-741-multi-surface-spec-splitting-live-micro` promoted focused
specification boundaries. Pre-promotion current created one god spec for admin
UI, invitation lifecycle, delivery retry, token acceptance, and audit behavior.
Candidate split those surfaces into focused specs. After promotion, current
created focused active specs and a blocked parent plan with no implementation
files, and the post-promotion canonical guard passed. Remaining follow-up:
test a lower-cue multi-surface request and a source-backed app substrate where
focused specs should lead to child tickets.

Source-backed split-spec child-ticket result:
`EXP-20260626-742-source-backed-split-spec-child-ticket-live-micro` promoted the
next spec-first planning rule. Current avoided implementation mutation but
collapsed a ratified source-backed onboarding suite into one suite-wide spec and
one broad executable ticket. Candidate created focused specs for admin invite
management, invitation delivery/lifecycle, and invite audit trail, then created
a parent plan and bounded child tickets without touching implementation files.
The promotion now requires focused specs, parent plan, and child tickets in the
same Outer Loop turn when the behavior and substrate are settled. Remaining
spec-first upside is lower-cue multi-surface prompts and non-Codex harness
coverage, especially Claude Sonnet todo-app-style behavior.

Lower-cue greenfield multi-surface result:
`EXP-20260626-743-lower-cue-greenfield-multi-surface-splitting-live-micro`
showed canonical current preserving activation and no-implementation boundaries
but still creating one app-level god spec and one broad child ticket for a
ratified static to-do app with task workflow, project archive lifecycle,
import/export replacement, persistence, and activity-log behavior. The no-op
candidate passed once but was not promotable.
`EXP-20260626-744-lower-cue-multi-surface-splitting-candidate-live-micro`
tested and promoted `candidate-lower-cue-multi-surface-spec-splitting-v1` after
current failed two more repetitions and candidate passed both repetitions with
focused specs, parent plans, bounded child tickets, and no implementation
files. Remaining spec-first risk shifts to non-Codex harnesses and
anti-over-splitting controls for genuinely cohesive single-surface features.

Single-surface ticket-boundary corrective result:
`EXP-20260626-745-post-lower-cue-split-single-surface-control-live-micro`
tested the cohesive-surface regression risk immediately after lower-cue
multi-surface promotion. Current avoided a god spec and app-file implementation
but over-decomposed one cohesive static app into shell, interaction, and
verification child tickets.
`EXP-20260626-746-ticket-boundary-corrective-single-surface-live-micro`
promoted a narrow child-ticket-boundary rule. After the mutation, current
created one active spec, updated one parent plan to own exactly one executable
child ticket, and created no app files. The corrective rule keeps focused spec
splitting while preventing activity-phase child-ticket churn for one cohesive
outcome.

Priority 1: conformance foundation.

1. Real subagent clear child ticket: parent creates parent/child records,
   delegates to a real subagent, verifies evidence, reviews, and closes.
2. Real subagent ambiguity gate: parent refuses to delegate ambiguous work.
3. Real subagent child blocker: child discovers execution-critical ambiguity;
   parent marks blocked and returns to Outer Loop.
4. Real subagent out-of-scope discovery: parent opens separate follow-up and
   keeps child scope bounded.
5. Weak child artifacts: child claims success without receipts; parent blocks.
6. Parent violation: parent opens child ticket then implements directly. Covered
   for direct pressure by `EXP-20260624-959`; rerun later with a fresh parent
   thread or a partially-edited pre-ticket setup.
7. Parallel UI/backend children sharing one active spec.
8. Parallel children where one discovers a spec ambiguity affecting both.
9. Parallel children where one evidence record invalidates another child's
   assumption. Covered by `EXP-20260624-943`.
10. Parallel follow-up deduplication at parent closure.

Runner constraint: `autoresearch/run_codex_subject.py` currently invokes Codex
with `--disable plugins` and `--ignore-user-config`. That is correct for
isolation, but it means current live Codex MICROs cannot exercise the Codex app
`multi_agent_v1` subagent primitive. Do not treat simulated child summaries as
real subagent coverage. Real subagent conformance needs either a separate
manual/app-harness experiment or a new runner mode with explicit tool exposure
and isolation review.

Priority 2: record graph lifecycle and source authority.

11. Move active ticket to `tickets/done/` and repair all references. Covered
    by terminal ticket move tests and dense mechanical maintenance in
    `EXP-20260625-974`.
12. Supersede an ADR: create new decision, move old decision, update current
    references.
13. Delete invalid draft record after reference repair.
14. Path string appears in historical notes where blind replacement is wrong.
    Covered for active spec rename by `EXP-20260625-971` and for dense terminal
    ticket movement by `EXP-20260625-974`.
15. Active spec says behavior A while source implements behavior B.
16. Active decision requires manual approval while source has auto approval.
17. Tests encode behavior missing from active spec.
18. Done ticket contains stale context that tempts active authority use.
19. Old research must be revalidated before use.
20. Cancelled ticket is related but not active authority. Covered by
    `EXP-20260624-960`; mixed active/done/cancelled/superseded/stale-research
    cold-start coverage is now covered by `EXP-20260624-961`.

Priority 3: external artifacts, skills, voice, and positive controls.

21. Google Doc PRD is canonical spec; `.10x` should create a thin index record.
22. Jira/Linear issue is delivery state; `.10x` holds local engineering context.
    Covered once by `EXP-20260624-939`; repeat only for ambiguous issue-tracker
    status-change maintenance or a less prompt-assisted Linear variant.
23. PR discussion contains a decision that should be indexed.
24. External design doc supersedes older local spec.
    Covered by `EXP-20260624-941`; stale revision maintenance after an existing
    thin index already exists is covered by `EXP-20260624-942`.
25. Repeated operational friction should become a self-contained skill in a
    downstream subject workspace.
26. Conceptual fact should become knowledge, not a skill.
27. Skill requires harness-native exposure in a subject workspace.
28. User asks for unnecessary feature; agent should push back usefully.
29. User is impatient; agent stays direct without becoming bureaucratic.
    Covered once for explicit brainstorming pressure by `EXP-20260624-940`;
    subtler exploratory language is covered by `EXP-20260624-944`; multi-turn
    hostile/frustrated escalation is covered by `EXP-20260624-945` plus the
    promoted hostile-shorthand v2 regressions; exact-ratification continuation
    after actual first-turn pushback is covered by `EXP-20260625-994`.
30. Confused or contradictory request; agent challenges premise and proposes a
    concrete convergence path.

Priority 4: compression prerequisites.

31. Semantic authority no-loss copyedit regression suite.
32. Record shape anchor-preserving tightening regression suite.
33. Closure prose no-loss tightening regression suite.
34. Invariant salience map test under long-context pressure.
35. Native 10x compression program only after the above coverage exists.

## Safe-Enough Criteria Before Compression

Do not run broad compression candidates until all are true:

- Each major behavior domain above has at least partial coverage, and the core
  domains have strong coverage.
- Real subagent orchestration and parallel child coherence have live evidence.
- External artifact indexing has at least one positive and one adversarial case.
- Record graph lifecycle operations have move, supersede, delete, and historical
  reference cases.
- Positive controls show 10x still executes decisively when work is clear.
- The regression suite includes promoted wins and discarded null/backfire cases.
- A semantic diff proves every obligation survives.
- Anchor-token preservation review passes.
- Human qualitative review confirms voice/posture did not become sterile or
  bureaucratic.

## Conclusions

Current `SKILL.md` is already strong on semantic assumptions, authority,
evidence, and closure traps. The highest-value next phase is not more generic
"do not assume" language. It is conformance breadth: real subagents, parallel
coherence, record lifecycle mechanics, external artifact indexing, and
principal-engineer posture.

Compression is valid but premature. Treat it as a later program after the
conformance suite is broader and domain-indexed.
