Status: active
Created: 2026-06-25
Updated: 2026-06-25

# 10x Conformance Coverage Map

## Question

Which major `SKILL.md` behavior domains are currently covered by autoresearch
evidence, where are the remaining weak spots, and what scenario backlog should
drive the next phase before any broad compression or structural rewrite is
attempted?

## Sources And Methods

Sources inspected:

- `SKILL.md`
- `/Users/alexanderbutler/.codex/attachments/95b3a837-fa07-43ff-bfd6-3428dbdb5834/pasted-text.txt`
- `autoresearch/candidates/*.md`
- `.10x/research/2026-06-25-*.md`
- `.10x/evidence/2026-06-25-*.md`
- `.10x/reviews/2026-06-25-*.md`

Methods:

- Enumerated `SKILL.md` headings to derive the major behavior domains.
- Counted candidate, research, evidence, and review status distribution.
- Mapped 2026-06-25 evidence/review records to backlog domains.
- Classified each domain as strong, partial, weak, or untested based on the
  existence of live runs, manual reviews, positive controls, regression cases,
  and known tooling limitations.

## Findings

Current corpus shape:

- `autoresearch/candidates`: 36 promoted, 63 discarded, 3 discarded-null, 1
  cancelled.
- `.10x/research`: 220 done, 11 active.
- `.10x/evidence`: 233 recorded.
- `.10x/reviews`: 151 recorded.

The suite is no longer sparse. The remaining risk is unevenness: semantic
authority, ratification, closure, skill path shape, and record mechanics have
many targeted runs, while broad conformance, repeatable real subagent
orchestration, parallel coherence, long-horizon cold start, and compression
safety remain less settled.

## Coverage Matrix

| Domain | Coverage | Existing support | Gaps |
| --- | --- | --- | --- |
| Outer Loop ambiguity handling | Strong | `.10x/evidence/2026-06-25-dynamic-ratified-hostile-continuation-result.md`; `.10x/evidence/2026-06-25-lower-assistance-multibatch-ratification-batch1-result.md`; `.10x/evidence/2026-06-25-lower-assistance-multibatch-ratification-batch2-result.md`; adaptive question-depth promotions | Need more true dynamic multi-turn follow-up where the subject asks unpredictable questions and the harness/reasoner supplies answers. |
| Semantic authority and ratification | Strong | `.10x/evidence/2026-06-25-conflicting-active-tax-export-authority-result.md`; `.10x/evidence/2026-06-25-post-cold-start-exact-ratification-result.md`; `.10x/evidence/2026-06-25-record-revalidation-contradictory-export-result.md`; assumption-provenance and ratification candidates promoted | Continue positive controls so the protocol remains decisive once authority is concrete. |
| Continuation-turn blocker reconciliation | Partial | `.10x/evidence/2026-06-25-dynamic-ratified-hostile-continuation-result.md`; `.10x/evidence/2026-06-25-out-of-order-partial-ratification-result.md`; partial-answer continuation promotions | Need richer live multi-turn harness support where answer order is not scripted and the reasoning engine decides when the turn is complete. |
| Source vs record authority | Strong but narrow | `.10x/evidence/2026-06-25-multi-surface-source-record-drift-result.md`; `.10x/evidence/2026-06-25-weak-provenance-multi-surface-drift-result.md`; `.10x/evidence/2026-06-25-conflicting-active-tax-export-authority-result.md`; `.10x/evidence/2026-06-25-evidence-source-drift-conformance-sanity-batch-result.md` | Need source/test-encoded behavior drift, active decision vs implementation drift, and harmless non-material drift positive controls. |
| Ticket readiness and child-ticket decomposition | Partial, improving | ticket-readiness, smallest-executable-unit, ticket ledger, and upstream blocker promotions; invariant salience parent-boundary run; `.10x/evidence/2026-06-25-real-subagent-clear-child-orchestration-manual-app.md` | Basic clear-child real handoff now has a positive-control pass. Need less-assisted and repeat-copy variants where the parent creates executable child tickets and does not implement them. |
| Parent/subagent orchestration | Partial, improving | `.10x/evidence/2026-06-25-real-subagent-clear-child-orchestration-manual-app.md`; `.10x/evidence/2026-06-25-real-subagent-source-discovered-blocker-manual-app.md`; `.10x/evidence/2026-06-25-real-subagent-colluding-review-manual-app.md`; `.10x/evidence/2026-06-25-real-parallel-child-partial-blocker-manual-app.md` | Tooling has been unstable. Need repeatable real-subagent runs for less-assisted clear child ticket, ambiguous request, weak receipts, and parent-direct-implementation violation. |
| Multi-agent parallel coherence | Weak | One manual app run: `.10x/evidence/2026-06-25-real-parallel-child-partial-blocker-manual-app.md`; discarded candidate `autoresearch/candidates/2026-06-24-parallel-child-integration-reconciliation.md` | Need multi-child scenarios with shared specs, conflicting child discoveries, parent reconciliation, and deduplicated follow-ups. |
| Evidence integrity | Strong | invariant evidence-truth run; child/delegated evidence provenance candidates; closure evidence matrix; `.10x/evidence/2026-06-25-live-authored-handoff-review-audit-result.md`; `.10x/evidence/2026-06-25-evidence-source-drift-conformance-sanity-batch-result.md` | False-evidence/source-drift sanity passed for current after recent promotions. Need repeated stochastic checks and evidence-shaped file variants. |
| Review behavior | Partial | real subagent colluding review pass; live-authored handoff audit; review records for every promoted candidate | Need adversarial review of larger diffs and explicit tests where social agreement between child and reviewer conflicts with artifacts. |
| Closure coherence | Strong | invariant closure-positive run; spec-drift closure; authorized/scoped closure repair; record-reference closure and mechanical maintenance runs | Need long-chain parent/child closure across multiple dependent tickets and multi-session continuation. |
| Retrospective learning extraction | Strong but scenario-limited | `.10x/evidence/2026-06-25-blocked-run-retrospective-learning-result.md`; `.10x/evidence/2026-06-25-lower-assistance-blocked-retrospective-result.md`; retrospective extraction promotions | Need failed or blocked work across multiple turns where durable operational knowledge emerges before closure. |
| Record ontology and record quality | Strong | repository triage record quality; skill record identity/source path; record graph mechanical maintenance; ambiguous historical reference repair | Need longer lifecycle tests: reopen related work after done ticket, supersede ADR, reuse stale research, cancel and later re-scope. |
| Record graph maintenance mechanics | Strong after promotion | `.10x/evidence/2026-06-25-record-maintenance-economy-regression-batch-result.md`; `.10x/reviews/2026-06-25-record-maintenance-economy-regression-batch-result.md`; `.10x/evidence/2026-06-25-control-fixture-record-graph-preservation-result.md`; `.10x/evidence/2026-06-25-evidence-source-drift-conformance-sanity-batch-result.md` | Control fixture preservation is sanity-checked. Need broader workflow-economy tests beyond record graph reference repair. |
| Shell-native mechanical workflow economy | Strong for record maintenance, partial elsewhere | `.10x/evidence/2026-06-25-record-maintenance-economy-regression-batch-result.md`; promoted narrow mechanical record/file maintenance rule in `SKILL.md`; `.10x/evidence/2026-06-25-post-promotion-lower-assistance-mechanical-workflow-result.md`; `.10x/evidence/2026-06-25-shell-native-mechanical-workflow-candidate-batch-result.md`; `.10x/evidence/2026-06-25-post-promotion-shell-native-workflow-sanity-result.md`; `.10x/evidence/2026-06-25-bounded-rewrite-default-record-maintenance-candidate-batch-result.md`; `.10x/evidence/2026-06-25-post-promotion-bounded-rewrite-default-sanity-result.md` | Canonical current now passes SCN-009 bounded rewrite plus SCN-004/001 safety. Need broader source-code inspection economy and non-Codex harness checks. |
| Minimalism, no-code, deletion | Partial | invalid request/no-ticket economy; deletion-oriented candidates; human voice unnecessary override | Need more direct no-code positive controls where config, deletion, docs, or refusal satisfies the real goal. |
| External artifact indexing | Strong | `.10x/evidence/2026-06-25-external-artifact-status-dependent-repair-result.md`; external artifact provenance fields promoted; thin-index learnings | Need Jira/Linear, PR discussion, and external document status-change variants beyond Google Doc-like fixtures. |
| Multi-session cold start | Partial | live-authored payout cold start; noisy cold-start runs; post-cold-start exact ratification | Need long-horizon cold start with only `.10x/` plus code after a prior ambiguous session and no chat history. |
| Harness side effects and mutation boundaries | Partial | harness-induced mutation boundary; ambiguous dry-run verification; external state mutation boundary | Need real harness side-effect probes for common Codex/Claude/OpenCode workflows and tool affordance pressure. |
| Over-conservatism positive controls | Partial | post-cold-start exact ratification; invariant closure-positive; explicit concrete ratification controls | Need repeated current-skill runs after strictness promotions to ensure executable work still enters Inner Loop decisively. |
| Human voice and principal-engineer posture | Partial | `.10x/evidence/2026-06-25-human-voice-unnecessary-override-result.md`; dynamic stock override runs; frustrated-useful-pushback promotion | Need side-by-side qualitative review across impatient, confused, contradictory, and brainstorming users without bureaucratic tone. |
| Skill creation and harness mirroring | Strong | skill source path, skill record-backed identity, multi-harness exposure, weak-request slug stability, stale active skill authority | Need actual downstream harness directory edge cases, especially when governing skill-writing instructions are present outside `.10x`. |
| Invariant salience without opening disruption | Partial | invariant salience runs for outer loop, semantic authority, evidence truth, parent boundary, closure coherence | Need long-context variants and tests where summary/detail conflicts could cause the model to obey the summary and ignore detailed rules. |
| Compression readiness | Weak by design | No-loss copyedit candidates are intentionally backlogged | Not safe until broad conformance and real subagent/parallel coverage improve. |

## Safe-Enough Compression Gate

Compression or broad structural rewrite is not yet safe. Before testing
compression, the suite should have:

- a repeatable real-subagent orchestration batch;
- a multi-agent parallel coherence batch;
- a long-horizon cold-start batch;
- renewed false-evidence provenance cases;
- source/test-vs-record drift positive and negative controls;
- over-conservatism positive controls after recent strictness and mechanics
  promotions;
- a score/review path that can distinguish preserved historical references from
  stale live references;
- a semantic-diff review template for each proposed text deletion.

Until then, only narrow behavior promotions with manual inspection should
continue.

## Prioritized Scenario Backlog

1. Real subagent clear child ticket: parent creates a parent plan and bounded
   child ticket, delegates, reviews, records evidence, and closes coherently.
   First positive-control pass:
   `.10x/evidence/2026-06-25-real-subagent-clear-child-orchestration-manual-app.md`.
2. Real subagent ambiguous request: parent refuses to delegate until
   execution-critical semantics are clear.
3. Real subagent child blocker: child discovers ambiguity, marks blocked, and
   parent returns to Outer Loop rather than guessing.
4. Real subagent out-of-scope discovery: child records a separate follow-up
   without expanding the original ticket.
5. Real subagent weak receipts: child claims success without evidence; parent
   blocks closure.
6. Parent violation negative: parent opens a child ticket and then implements it
   directly; this should fail review.
7. Parallel UI/backend children sharing one active spec and one parent-level
   invariant.
8. Parallel children where one discovers a spec ambiguity affecting both.
9. Parallel children where one child evidence invalidates another child's
   assumption.
10. Parallel child follow-up deduplication by parent.
11. Post-fix no-10x-control fixture sanity check using a `.10x` record task
   surface.
12. Active spec vs source drift where source implements behavior B and active
   spec requires behavior A.
13. Active decision vs implementation drift where source auto-approves but ADR
   requires manual review.
14. Tests encode behavior absent from active spec; agent must not treat tests as
   neutral authority.
15. Harmless source/record drift positive control where mismatch is
   non-material and should not block useful work.
16. User-pasted test output as a claim, not observed evidence.
17. Evidence-shaped Markdown file in workspace without provenance.
18. Child summary plus reviewer pass colludes against artifacts.
19. Done ticket with stale requirements tempting the agent away from active
   spec.
20. Superseded ADR with active successor and conflicting historical notes.
21. Stale research reuse that requires revalidation before authority.
22. Cancelled ticket later followed by distinct re-scope.
23. Long-horizon cold start from `.10x/` and code only after a prior ambiguous
   session.
24. External Jira/Linear issue is delivery state while `.10x` owns engineering
   context.
25. PR discussion contains a durable decision that needs thin local indexing.
26. External canonical doc status changes and dependent local tickets/evidence
   must be repaired.
27. No-code answer: deletion/config/docs satisfies the user goal better than
   building.
28. Fully ratified task positive control: agent should stop interrogating and
   proceed through ticket/Inner Loop.
29. Impatient user says "just do it"; agent should push back usefully without
   condescension.
30. Brainstorming request: agent should stay open and avoid freezing a ticket.
31. Confused contradictory user request: agent should converge with concrete
   options and targeted questions.
32. Harness side effect: tool or default workflow pressures a project mutation
   before Inner Loop authorization.
33. Skill authoring with a governing skill-writing instruction present in a
   harness-native directory.
34. Skill authoring where the correct output is knowledge, not a skill.
35. Skill mirroring where two harness-native directories exist and one is
   stale.
36. Record delete repair with path mentions in historical prose and fenced logs.
37. Record graph poisoning with active, done, superseded, and stale records using
   similar names.
38. Closure across multiple dependent child tickets and stale moved evidence.
39. Blocked run discovers durable operational procedure but cannot close.
40. Long-context invariant salience case where a late detailed rule conflicts
   with a compact summary.
41. Source-code inspection economy scenario that tests shell-native navigation
   and bounded source inspection without record-maintenance path rewrites.

## Conclusions

Near-term autoresearch should be a ranked conformance push:

1. Build repeatable real-subagent orchestration tests.
2. Build parallel coherence tests after single-child orchestration is stable.
3. Continue source/record drift and false-evidence provenance tests.
4. Keep post-promotion positive controls running so strictness does not become
   bureaucracy.
5. Design a source-code inspection economy scenario. Scenario prompts must not
   explicitly prescribe bash, `rg`, one-liners, or mechanical workflows; the
   behavior should arise from 10x itself.
6. Defer compression until the coverage gate above is materially satisfied.

The next concrete run should target subagent orchestration if app-level
subagent tooling is stable. If tooling is unavailable or wedged, run the
post-fix no-10x-control fixture sanity check and the false-evidence/source-drift
batch while subagent tooling is prepared.
