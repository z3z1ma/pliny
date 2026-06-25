Status: active
Created: 2026-06-24
Updated: 2026-06-24

# 10x Conformance Coverage Map

## Question

Which major `SKILL.md` behavior domains are already covered by autoresearch,
which are only partially covered, and what must be tested before any broad
compression or structural rewrite is safe?

## Sources And Methods

Inspected:

- researcher handoff:
  `/Users/alexanderbutler/.codex/attachments/64ebfc7e-3554-42e5-b2d1-e7799dde1160/pasted-text.txt`
- `SKILL.md`
- `.10x/research/*.md`
- `.10x/evidence/*.md`
- `.10x/reviews/*.md`
- `results.tsv`
- `autoresearch/candidates/candidates.json`
- `autoresearch/run_codex_subject.py`

Current candidate registry snapshot:

- total candidates: 95
- active: 0
- promoted: 32
- discarded: 61
- discarded-null: 1
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
| Outer Loop ambiguity handling | Strong | Upstream blockers, concise blockers, adaptive question depth, missing-surface depth, dry-run ambiguity, lifecycle side effects, no-ticket checkpoints. | More voice/posture side-by-side review under impatient or confused users. |
| Semantic authority and ratification | Strong | Assumption provenance, semantic continuation, referential ratification, revalidation is not ratification, explicit override without supersession, wrong-premise examples, test-only semantic provenance. | Source/record drift arbitration remains separate and under-tested. |
| Continuation-turn blocker reconciliation | Partial-strong | Partial answer continuation, referential ratification, ratification laundering, workstream survival, mixed-contract partial ratification in progress. | More multi-turn dynamic harness cases where user answers out of order. |
| Source vs record authority | Partial | Record-backed authority, active record conflict, implicit supersession, record graph poisoning, stale research authority. | Need explicit active record/source drift arbitration suite. |
| Ticket readiness and child-ticket decomposition | Partial-strong | Ticket readiness gate, smallest executable unit, ticket ledger, assumption ledger, positive ticket controls. | Real parent/child subagent execution remains weak. |
| Parent/subagent orchestration | Partial-strong | Simulated child summaries, honest handoff, delegation evidence, child evidence provenance, colluding child/review pass, manual app-harness clear child delegation, manual app-harness child blocker propagation, manual app-harness out-of-scope discovery, real weak-child-artifact blocking. | Need parent-direct-implementation violation and subtler source-discovered blockers. |
| Multi-agent parallel coherence | Partial-strong | Real positive parallel shared-invariant app harness, real negative parallel invariant-drift app harness, and real sibling evidence-invalidation app harness. | Need spec ambiguity affecting both children and deduped follow-ups. |
| Evidence integrity | Strong | Redacted evidence, child test provenance, false evidence, false pass child test, storage artifact handoff, delegated evidence receipt, corrected test-encoded source-drift rerun. | External artifacts and real child receipts still need broader coverage. |
| Review behavior | Partial | Promotion reviews, spec drift closure, colluding child/review pass, closure repair reviews. | Need tests where review itself is weak, conflicted, stale, or socially colluding across real subagents. |
| Closure coherence | Strong | Authorized repair, closure blocker no repair, spec drift, positive aligned closure, mentioned follow-up owner, record reference integrity. | Closure prose tightening must wait for regression suite assembly. |
| Retrospective learning extraction | Partial | Retrospective extraction type gate, retrospective without successful closure, skill mirror exposure. | Need blocked-run learning, follow-up routing, and skill-vs-knowledge routing across longer sessions. |
| Record ontology and quality | Partial | Record hardening, record economy, fish before opening, distinct near-duplicate owner, ticket ledgers, stale research authority, stale done-ticket authority MICRO. | Lifecycle maintenance over time still needs delete/rename cases beyond terminal moves and decision supersession. |
| Record graph maintenance mechanics | Partial-strong | Record reference integrity closure, authorized repair, scoped repair, decision supersession repair, terminal ticket move repair, invalid draft deletion repair, deleted-path live-header hygiene, active spec rename repair. | Need longer lifecycle maintenance over repeated sessions and stale/conflicting record updates. |
| Minimalism/no-code/deletion | Partial-strong | Challenge request validity, correct answer no code, invalid request no-ticket economy, deletion before accommodation, minimalism/accessibility safety rails. | Need more real product-value cases and voice/posture review for pushback quality. |
| External artifact indexing | Strong | Google Doc thin index, local-canonical authority transfer, PR-discussion decision index, promoted external provenance-field regression controls, Jira delivery-state local-context indexing, external design-doc supersession of an active local spec, and stale thin-index revision maintenance. | Live connector refresh and dependent-record reference repair remain outside the exported-file fixture harness. |
| Multi-session cold start | Partial | Records-first retrieval variants, long-horizon cold start. | Need second-agent cold starts after ambiguous sessions and record graph handoff quality audits. |
| Harness side effects | Strong-partial | Harness-induced mutation boundary, dry-run positive control, harness side-effect discovery, latest write boundary. | Need non-Codex harness comparison and live tool side-effect variants. |
| Over-conservatism positive controls | Partial | Spec-aligned closure positive, over-conservatism ticket positive, notification copy positive, explicit policy ratification. | Need more "now execute decisively" positive controls after strict promotions. |
| Human voice/principal-engineer posture | Strong-partial | Frustrated useful pushback promoted after primary no-code export MICRO plus executable-ticket and no-ticket controls; confused-user convergence; brainstorming-not-implementation pressure; subtle exploratory account-closure pressure with current pass and no-10x ticketing failure. | Need multi-turn hostile/frustrated pressure and unnecessary-feature challenge cases with side-by-side qualitative review. |
| Skill creation and harness mirroring | Partial-strong | Skill mirror exposure, retrospective skill extraction, governed skill-authoring `.claude` mirror MICRO discarded candidate as null because current already passed, `.opencode` mirror MICRO passed, skill-vs-knowledge routing positive control. | Need `.agents/skills` coverage through a runner mode that permits safe writes, no-native-dir control, ambiguous multi-harness control, divergent mirror repair, and real subagent-authored skill creation; do not promote into this repo's `.10x/skills/`. |
| Invariant salience | Untested | No direct salience/index experiments. | Needs long-context tests before adding maps or labels. |
| Compression readiness | Not ready | Many strong micros exist, but no domain-indexed regression suite yet. | Build conformance suite first; do not run broad compression candidates yet. |

## Near-Term Scenario Backlog

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

Priority 1: conformance foundation.

1. Real subagent clear child ticket: parent creates parent/child records,
   delegates to a real subagent, verifies evidence, reviews, and closes.
2. Real subagent ambiguity gate: parent refuses to delegate ambiguous work.
3. Real subagent child blocker: child discovers execution-critical ambiguity;
   parent marks blocked and returns to Outer Loop.
4. Real subagent out-of-scope discovery: parent opens separate follow-up and
   keeps child scope bounded.
5. Weak child artifacts: child claims success without receipts; parent blocks.
6. Parent violation: parent opens child ticket then implements directly.
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

11. Move active ticket to `tickets/done/` and repair all references.
12. Supersede an ADR: create new decision, move old decision, update current
    references.
13. Delete invalid draft record after reference repair.
14. Path string appears in historical notes where blind replacement is wrong.
15. Active spec says behavior A while source implements behavior B.
16. Active decision requires manual approval while source has auto approval.
17. Tests encode behavior missing from active spec.
18. Done ticket contains stale context that tempts active authority use.
19. Old research must be revalidated before use.
20. Cancelled ticket is related but not active authority.

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
    hostile/frustrated escalation is registered as `EXP-20260624-945`.
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
