---
id: evidence:critique-closure-gate-validation
kind: evidence
status: recorded
created_at: 2026-05-02T22:16:05Z
updated_at: 2026-05-02T22:31:08Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:critgate2
  packet:
    - packet:ralph-ticket-critgate2-20260502T221504Z
  critique:
    - critique:critique-closure-gate-review
    - critique:critique-closure-gate-rereview
external_refs: {}
---

# Summary

Observation-first validation for mandatory/recommended critique closure-gate
wording in the Loom bootstrap references.

# Procedure

- Checked source fingerprint before editing.
- Captured before-state searches for required, mandatory, recommended,
  explicitly deferred, deferred, `not_required`, and closure-blocking wording.
- Updated targeted bootstrap references and ticket state.
- Captured after-state searches over the same reference and ticket paths.
- Ran `git diff --check`.
- Parent reconciled ticket claim status vocabulary, packet lifecycle status, and
  evidence shape before mandatory critique.
- After oracle finding `critique:critique-closure-gate-review#FIND-001`, repaired
  wording to require a `final` critique record with explicit verdict before
  closure.

# Source Fingerprint Check

Command:

```bash
git status --short && git rev-parse HEAD
```

Result:

```text
 M .loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md
?? .loom/packets/ralph/20260502T221504Z-ticket-critgate2-iter-01.md
52cc82e344dd82d1fb37a584f59ce8c3f20f5a8e
```

Interpretation: `HEAD` matched the packet source fingerprint. The dirty paths
were the scoped ticket and packet setup surfaces for this Ralph iteration.

# Before Observation

Command:

```bash
for pattern in 'required critique' 'mandatory critique' 'recommended critique' 'explicitly deferred' 'deferred' 'not_required' 'blocks `closed`' 'blocks closure' 'block closure'; do
  printf '\n### %s\n' "$pattern"
  rg -n -i "$pattern" \
    "skills/loom-bootstrap/references/07-validation-and-honesty.md" \
    "skills/loom-bootstrap/references/05-critique-and-wiki.md" \
    ".loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md" || true
done
```

Result:

```text
### required critique
skills/loom-bootstrap/references/07-validation-and-honesty.md:15:- required critique has happened or is explicitly deferred
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:32:that says required critique has happened or is explicitly deferred, which can
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:112:Required critique profiles:

### mandatory critique
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:26:Tighten bootstrap closure wording so mandatory critique cannot be read as
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:37:Closure discipline should fail closed for mandatory critique while still allowing
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:43:  mandatory critique from recommended critique.
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:54:- ACC-001: Mandatory critique clearly blocks closure until completed and required
skills/loom-bootstrap/references/05-critique-and-wiki.md:90:- mandatory critique blocks `closed` until the required review exists and every
skills/loom-bootstrap/references/07-validation-and-honesty.md:128:- mandatory critique blocks closure until open medium/high findings have

### recommended critique
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:33:blur mandatory and recommended critique policies.
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:38:ticket-owned rationale for recommended critique disposition.
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:43:  mandatory critique from recommended critique.
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:45:- Keep recommended critique disposition flexible where policy allows it.
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:56:- ACC-002: Recommended critique can be completed, deferred, or not required only
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:92:Bounded iteration: mandatory/recommended critique closure gate wording.
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:101:Expected: before/after searches for required/mandatory/recommended critique closure
skills/loom-bootstrap/references/05-critique-and-wiki.md:96:- recommended critique requires a recorded ticket-owned disposition status before
skills/loom-bootstrap/references/07-validation-and-honesty.md:127:- recommended critique needs a recorded ticket-owned disposition status before closure

### explicitly deferred
skills/loom-bootstrap/references/07-validation-and-honesty.md:15:- required critique has happened or is explicitly deferred
skills/loom-bootstrap/references/07-validation-and-honesty.md:16:- wiki follow-through has happened or is explicitly deferred
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:32:that says required critique has happened or is explicitly deferred, which can

### deferred
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:32:that says required critique has happened or is explicitly deferred, which can
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:56:- ACC-002: Recommended critique can be completed, deferred, or not required only
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:126:Not deferred.
skills/loom-bootstrap/references/07-validation-and-honesty.md:15:- required critique has happened or is explicitly deferred
skills/loom-bootstrap/references/07-validation-and-honesty.md:16:- wiki follow-through has happened or is explicitly deferred
skills/loom-bootstrap/references/05-critique-and-wiki.md:97:  closure: `completed`, `deferred`, or `not_required` with rationale
skills/loom-bootstrap/references/05-critique-and-wiki.md:191:  deferred, not required, or blocking
skills/loom-bootstrap/references/05-critique-and-wiki.md:225:A retrospective is a named workflow — not a new record kind and not a new directory. It assimilates what was learned during a ticket, initiative, or recent work slice into the existing owner layers, then the owning ticket or initiative records what was promoted, deferred, not required, or still blocking:

### not_required
skills/loom-bootstrap/references/05-critique-and-wiki.md:97:  closure: `completed`, `deferred`, or `not_required` with rationale

### blocks `closed`
skills/loom-bootstrap/references/05-critique-and-wiki.md:90:- mandatory critique blocks `closed` until the required review exists and every

### blocks closure
skills/loom-bootstrap/references/07-validation-and-honesty.md:128:- mandatory critique blocks closure until open medium/high findings have
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:54:- ACC-001: Mandatory critique clearly blocks closure until completed and required

### block closure
skills/loom-bootstrap/references/05-critique-and-wiki.md:95:  and do not block closure merely because of severity.
skills/loom-bootstrap/references/05-critique-and-wiki.md:98:- optional critique does not block closure unless a ticket, spec, plan, or human
```

# After Observation

Command: same as the before observation.

Result:

```text
skills/loom-bootstrap/references/07-validation-and-honesty.md:15:- required critique gate is satisfied by the policy that applies to this work:
skills/loom-bootstrap/references/07-validation-and-honesty.md:18:  - every open medium/high finding from a required critique has a ticket-owned
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:34:that says required critique has happened or is explicitly deferred, which can
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:101:Required critique profiles: `closure-honesty`, `operator-clarity`, and
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:124:Required critique profiles:

### mandatory critique
skills/loom-bootstrap/references/07-validation-and-honesty.md:16:  - mandatory critique has happened before closure; deferral or `not_required`
skills/loom-bootstrap/references/07-validation-and-honesty.md:17:    does not satisfy a mandatory critique gate
skills/loom-bootstrap/references/07-validation-and-honesty.md:136:- mandatory critique blocks closure until the required review exists and every
skills/loom-bootstrap/references/05-critique-and-wiki.md:90:- mandatory critique blocks `closed` until the required review exists. It cannot
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:28:Tighten bootstrap closure wording so mandatory critique cannot be read as
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:39:Closure discipline should fail closed for mandatory critique while still allowing
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:45:  mandatory critique from recommended critique.
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:56:- ACC-001: Mandatory critique clearly blocks closure until completed and required

### recommended critique
skills/loom-bootstrap/references/05-critique-and-wiki.md:97:- recommended critique requires a recorded ticket-owned disposition status before
skills/loom-bootstrap/references/07-validation-and-honesty.md:21:  - recommended critique has a recorded ticket-owned disposition before closure:
skills/loom-bootstrap/references/07-validation-and-honesty.md:140:- recommended critique needs a recorded ticket-owned disposition status before
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:35:blur mandatory and recommended critique policies.
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:40:ticket-owned rationale for recommended critique disposition.
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:45:  mandatory critique from recommended critique.
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:47:- Keep recommended critique disposition flexible where policy allows it.
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:58:- ACC-002: Recommended critique can be completed, deferred, or not required only
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:99:Bounded iteration: mandatory/recommended critique closure gate wording landed;

### explicitly deferred
skills/loom-bootstrap/references/07-validation-and-honesty.md:25:- wiki follow-through has happened or is explicitly deferred
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:34:that says required critique has happened or is explicitly deferred, which can

### deferred
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:34:that says required critique has happened or is explicitly deferred, which can
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:58:- ACC-002: Recommended critique can be completed, deferred, or not required only
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:113:  deferred, deferred, `not_required`, and closure-blocking wording
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:138:Not deferred.
skills/loom-bootstrap/references/07-validation-and-honesty.md:22:    `completed`, `deferred`, or `not_required` with rationale
skills/loom-bootstrap/references/07-validation-and-honesty.md:25:- wiki follow-through has happened or is explicitly deferred
skills/loom-bootstrap/references/07-validation-and-honesty.md:141:  closure: `completed`, `deferred`, or `not_required` with rationale
skills/loom-bootstrap/references/05-critique-and-wiki.md:98:  closure: `completed`, `deferred`, or `not_required` with ticket-owned rationale
skills/loom-bootstrap/references/05-critique-and-wiki.md:192:  deferred, not required, or blocking
skills/loom-bootstrap/references/05-critique-and-wiki.md:226:A retrospective is a named workflow — not a new record kind and not a new directory. It assimilates what was learned during a ticket, initiative, or recent work slice into the existing owner layers, then the owning ticket or initiative records what was promoted, deferred, not required, or still blocking:

### not_required
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:113:  deferred, deferred, `not_required`, and closure-blocking wording
skills/loom-bootstrap/references/05-critique-and-wiki.md:91:  be satisfied by deferral or `not_required` before closure. After the review
skills/loom-bootstrap/references/05-critique-and-wiki.md:98:  closure: `completed`, `deferred`, or `not_required` with ticket-owned rationale
skills/loom-bootstrap/references/07-validation-and-honesty.md:16:  - mandatory critique has happened before closure; deferral or `not_required`
skills/loom-bootstrap/references/07-validation-and-honesty.md:22:    `completed`, `deferred`, or `not_required` with rationale
skills/loom-bootstrap/references/07-validation-and-honesty.md:139:  critique cannot be satisfied by deferral or `not_required`
skills/loom-bootstrap/references/07-validation-and-honesty.md:141:  closure: `completed`, `deferred`, or `not_required` with rationale

### blocks `closed`
skills/loom-bootstrap/references/05-critique-and-wiki.md:90:- mandatory critique blocks `closed` until the required review exists. It cannot

### blocks closure
skills/loom-bootstrap/references/07-validation-and-honesty.md:136:- mandatory critique blocks closure until the required review exists and every
.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md:56:- ACC-001: Mandatory critique clearly blocks closure until completed and required

### block closure
skills/loom-bootstrap/references/07-validation-and-honesty.md:23:  - optional critique does not block closure unless a ticket, spec, plan, or
skills/loom-bootstrap/references/07-validation-and-honesty.md:142:- optional critique does not block closure unless a ticket, spec, plan, or human
skills/loom-bootstrap/references/05-critique-and-wiki.md:96:  and do not block closure merely because of severity.
skills/loom-bootstrap/references/05-critique-and-wiki.md:99:- optional critique does not block closure unless a ticket, spec, plan, or human
```

# Diff Check

Command:

```bash
git diff --check
```

Result: passed with no output.

# Parent Reconciliation Check

Observed at `2026-05-02T22:22:34Z` after parent reconciliation edits:

- `git diff --check`: passed with no output.
- Grep for noncanonical ticket claim statuses `implemented_pending_critique` and
  table status `satisfied` returned no matches in `ticket:critgate2`.
- Grep for `status: compiled` returned no matches in
  `packet:ralph-ticket-critgate2-20260502T221504Z`.
- Grep over targeted bootstrap references found mandatory critique deferral/
  `not_required` prohibitions and optional critique non-blocking wording in the
  expected files.

# Repair Validation Check

Observed at `2026-05-02T22:27:17Z` after repairing
`critique:critique-closure-gate-review#FIND-001`:

- `git diff --check`: passed with no output.
- Grep for `required review exists`, `review exists`, `has happened before
  closure`, and `final review exists` returned no matches in the targeted
  bootstrap references.
- Grep for `` `final` critique record``, `draft/stub review`, `explicit verdict`,
  and `ticket-owned disposition` found the expected mandatory critique closure
  wording in the targeted bootstrap references.

# Artifacts

- `skills/loom-bootstrap/references/07-validation-and-honesty.md`
- `skills/loom-bootstrap/references/05-critique-and-wiki.md`
- `.loom/tickets/20260502-critgate2-tighten-mandatory-critique-closure.md`
- `.loom/packets/ralph/20260502T221504Z-ticket-critgate2-iter-01.md`
- This evidence record.
- Before/after `rg` output recorded above.
- `git diff --check` output recorded above.

# Supports Claims

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-002`
- `ticket:critgate2#ACC-001`
- `ticket:critgate2#ACC-002`
- `ticket:critgate2#ACC-003`
- `ticket:critgate2#ACC-004`

# Challenges Claims

None - the observations did not challenge a scoped claim.

# Environment

Commit: `52cc82e344dd82d1fb37a584f59ce8c3f20f5a8e` plus the scoped uncommitted
`ticket:critgate2` diff.
Branch: `main`.
Runtime: Markdown corpus; no app runtime or automated test suite.
OS: macOS/Darwin.
Relevant config: repository-local Loom records and `skills/` product corpus.

# Validity

Valid for: the `ticket:critgate2` bootstrap reference changes, parent
reconciliation, and oracle re-review path at `2026-05-02T22:31:08Z`.
Recheck when: either bootstrap reference, the ticket, the evidence record, the
Ralph packet, or linked critique records change after acceptance.

# Limitations

- Does not establish `ticket:critgate2#ACC-005` by itself; final critique records
  own the oracle verdict.
- Does not validate unrelated critique-gate wording outside the targeted bootstrap
  references.
- Does not close the ticket or own the acceptance decision.

# Result

The targeted bootstrap references now distinguish mandatory, recommended, and
optional critique closure effects, and mandatory critique requires a `final`
critique record with explicit verdict before closure. The evidence supports the
implemented wording claims while leaving critique pass/fail and ticket closure to
the critique and ticket layers.

# Interpretation

- The ambiguous bootstrap line that allowed `required critique` to be
  `explicitly deferred` was replaced with a critique-gate policy split.
- Mandatory critique now blocks closure until a `final` critique record with
  explicit verdict is recorded and open medium/high findings have ticket-owned
  disposition; deferral, `not_required`, and draft/stub reviews are explicitly
  insufficient for mandatory critique.
- Recommended critique retains ticket-owned disposition flexibility through
  `completed`, `deferred`, or `not_required` with rationale.
- Optional critique remains non-blocking unless another owner or human gate made
  it required.

# Residual Risks

Oracle re-review passed with no findings, but evidence remains observational; the
ticket owns closure and the critique records own verdicts.

# Related Records

- `initiative:skills-corpus-template-grammar-safety-pass`
- `plan:skills-corpus-template-grammar-safety-pass`
- `ticket:critgate2`
- `packet:ralph-ticket-critgate2-20260502T221504Z`
- `critique:critique-closure-gate-review`
- `critique:critique-closure-gate-rereview`
