# Ticket Readiness

A ticket is ready when the next governed route can proceed without chat history.

Readiness is route-neutral. A ready ticket might route to any canonical route
token in `skills/loom-records/references/route-vocabulary.md`, including
`ask_user`, `workspace_status`, `records_repair`, `research`, `spec`, `plan`,
`ticket`, `local_edit`, `ralph`, `debugging`, `spike`, `codemap`, `evidence`,
`critique`, `wiki`, `retrospective`, `acceptance_review`, `ship`, `continue`,
or `stop`.

Ralph-ready is stricter: the ticket must also make one bounded implementation
iteration, write boundary, likely verification posture, and expected output
contract legible enough for a fresh worker.

New tickets should normally start as `proposed`. Promote to `ready` only after
this checklist passes.

## Checklist

- the problem is clearly named
- why now is clearly named
- scope and non-goals are separated
- `change_class` and `risk_class` are set in frontmatter for new tickets and for
  tickets being materially updated for readiness, Ralph, critique, acceptance,
  reopening, or closure; normalize legacy tickets when touched or before
  governed execution or acceptance, without treating their prior absence as
  instant non-conformance
- acceptance criteria are concrete enough to guide behavior
- coverage names relevant spec acceptance IDs when the work implements or
  verifies a spec
- when no spec owns the acceptance contract, ticket-local acceptance criteria use
  stable `ACC-*` IDs in the ticket and downstream records cite them as
  `ticket:<token>#ACC-001`
- ticket-local `ACC-*` criteria are not used to redefine or replace a reusable
  spec-owned acceptance contract
- relevant upstream artifacts are linked
- the likely evidence path is visible
- critique risk class matches frontmatter `risk_class`; required profiles are
  explicit when review is expected
- the next route is explicit in `# Next Move / Next Route` or equivalent prose,
  using the shared route vocabulary: `local_edit`, `ralph`, `debugging`,
  `spike`, `codemap`, `critique`, `wiki`, `retrospective`, `evidence`,
  `research`, `spec`, `plan`, `ticket`, `acceptance_review`, `ship`,
  `ask_user`, `workspace_status`, `records_repair`, `continue`, or `stop`
- the ticket is small enough to fit one bounded iteration or a short sequence of
  clearly staged iterations

If several of those are missing, do not force Ralph, critique, wiki, or closure.
Refine the ticket first.

## Route Readiness

Use `# Route Readiness` or equivalent prose to make the route named in `# Next
Move / Next Route` specific without implying that every handoff is Ralph. Do not
use it as a second route-token selector or duplicate the allowed-token list.

Use `skills/loom-records/references/route-vocabulary.md` for route-token grammar;
do not use ticket lifecycle statuses such as `ready`, `active`,
`review_required`, or `complete_pending_acceptance` as next-route values.

- For `local_edit`, name the bounded edit and write boundary.
- For Ralph, keep the stricter Ralph-ready fields: bounded iteration, write
  boundary, likely verification posture, and expected output contract.
- For `debugging`, name the failing behavior, reproduction/evidence expectation,
  and root-cause or fix handoff boundary.
- For `spike` or `codemap`, name the research/evidence/wiki outputs the workflow
  should produce and any throwaway write boundary.
- For `critique`, name the review target, required profiles, and evidence to
  review.
- For wiki or retrospective work, name the explanation or lesson to promote and
  the owner records it should source.
- For evidence recording, name the claim references and observation procedure.
- For `acceptance_review`, name the evidence, critique disposition, and
  residual risks that the gate must evaluate.
- For `ship`, name the ticket/evidence/critique records to package and the
  external handoff surface without treating shipping as closure.
