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

- total candidates: 93
- promoted: 31
- discarded: 60
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
| Parent/subagent orchestration | Weak | Simulated child summaries, honest handoff, delegation evidence, child evidence provenance, colluding child/review pass. | Need real subagent delegation behavior, not only transcript-shaped claims. |
| Multi-agent parallel coherence | Untested-weak | No direct parallel child-ticket scenario yet. | Need parent plan, shared invariants, integration reconciliation, cross-child discovery, deduped follow-ups. |
| Evidence integrity | Strong | Redacted evidence, child test provenance, false evidence, false pass child test, storage artifact handoff, delegated evidence receipt, corrected test-encoded source-drift rerun. | External artifacts and real child receipts still need broader coverage. |
| Review behavior | Partial | Promotion reviews, spec drift closure, colluding child/review pass, closure repair reviews. | Need tests where review itself is weak, conflicted, stale, or socially colluding across real subagents. |
| Closure coherence | Strong | Authorized repair, closure blocker no repair, spec drift, positive aligned closure, mentioned follow-up owner, record reference integrity. | Closure prose tightening must wait for regression suite assembly. |
| Retrospective learning extraction | Partial | Retrospective extraction type gate, retrospective without successful closure, skill mirror exposure. | Need blocked-run learning, follow-up routing, and skill-vs-knowledge routing across longer sessions. |
| Record ontology and quality | Partial | Record hardening, record economy, fish before opening, distinct near-duplicate owner, ticket ledgers, stale research authority, stale done-ticket authority MICRO. | Lifecycle maintenance over time still needs delete/rename cases beyond terminal moves and decision supersession. |
| Record graph maintenance mechanics | Partial | Record reference integrity closure, authorized repair, scoped repair, decision supersession repair, terminal ticket move repair. | Delete-invalid-draft reference repair is registered but not yet run; rename mechanics and stronger historical-reference traps remain. |
| Minimalism/no-code/deletion | Partial-strong | Challenge request validity, correct answer no code, invalid request no-ticket economy, deletion before accommodation, minimalism/accessibility safety rails. | Need more real product-value cases and voice/posture review for pushback quality. |
| External artifact indexing | Weak | External state mutation boundary, harness side-effect boundary, external workflows indirectly. | Need Google Doc/Jira/PR discussion thin-index scenarios. |
| Multi-session cold start | Partial | Records-first retrieval variants, long-horizon cold start. | Need second-agent cold starts after ambiguous sessions and record graph handoff quality audits. |
| Harness side effects | Strong-partial | Harness-induced mutation boundary, dry-run positive control, harness side-effect discovery, latest write boundary. | Need non-Codex harness comparison and live tool side-effect variants. |
| Over-conservatism positive controls | Partial | Spec-aligned closure positive, over-conservatism ticket positive, notification copy positive, explicit policy ratification. | Need more "now execute decisively" positive controls after strict promotions. |
| Human voice/principal-engineer posture | Partial | Frustrated useful pushback promoted after primary no-code export MICRO plus executable-ticket and no-ticket controls. Some manual notes in adaptive-depth and no-code experiments. | Need multi-turn hostile/frustrated pressure, confused-user convergence, and unnecessary-feature challenge cases with side-by-side qualitative review. |
| Skill creation and harness mirroring | Partial | Skill mirror exposure, retrospective skill extraction, governed skill-authoring mirror MICRO discarded candidate as null because current already passed, skill-vs-knowledge routing positive control. | Need downstream subject workspace skill creation/harness exposure across non-`.claude` harnesses; do not promote into this repo's `.10x/skills/`. |
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

External artifact positive-control update:
`EXP-20260624-922-external-local-spec-canonical-positive-control-scn004-live-micro`
is registered as the inverse of the prior thin-index case. It tests whether the
agent creates a full active local specification when Product and Engineering
explicitly ratify `.10x` as the canonical implementation contract.

Human-voice update:
`EXP-20260624-923-confused-account-closure-convergence-scn001-live-micro` is
registered to test confused/contradictory user convergence after the lifecycle
side-effect and frustrated-useful-pushback promotions.

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
   assumption.
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
23. PR discussion contains a decision that should be indexed.
24. External design doc supersedes older local spec.
25. Repeated operational friction should become a self-contained skill in a
    downstream subject workspace.
26. Conceptual fact should become knowledge, not a skill.
27. Skill requires harness-native exposure in a subject workspace.
28. User asks for unnecessary feature; agent should push back usefully.
29. User is impatient; agent stays direct without becoming bureaucratic.
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
