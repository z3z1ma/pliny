---
id: evidence:readme-bootstrap-authority-validation
kind: evidence
status: recorded
created_at: 2026-05-02T16:40:06Z
updated_at: 2026-05-02T16:40:06Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:yk89awl5
  packet:
    - packet:ralph-ticket-yk89awl5-20260502T163744Z
external_refs: {}
---

# Summary

Structural validation for the README alignment that routes bounded implementation
through Ralph with a Ralph packet and states that workflow skills coordinate
existing owner-layer routes without creating ledgers.

# Procedure

- Edited only the README route/workflow wording plus the owning ticket and this
  evidence record within the Ralph child write scope.
- Ran `git diff --check` from repository root after the README edits.
- Searched `README.md` for `Bounded implementation`, `Ralph`, `packet`,
  `workflow skills`, `Workflow skills`, `ledgers`, and `do not create ledgers`.
- Manually compared the edited README passages against:
  - `skills/loom-bootstrap/references/02-truth-and-authority.md` lines 70-73;
  - `skills/loom-bootstrap/references/04-ralph-inner-loop.md` lines 52-87;
  - `skills/loom-records/references/packet-frontmatter.md` lines 5-11 and 87-95;
  - `skills/loom-records/references/naming-and-ids.md` lines 96-110.

# Artifacts

- `git diff --check` outcome: passed with no output.
- Targeted README search outcome: key changed hits included:
  - `README.md:241`: `| Bounded implementation pass | Ralph with a Ralph packet |`
  - `README.md:244`: bug-fix narrative now says `a Ralph packet for the implementation pass`.
  - `README.md:354`: example sequence now says `Compile a Ralph packet for one implementation pass`.
  - `README.md:382`: `Workflow skills coordinate routes through existing owner layers. They do not create ledgers or new owner layers.`
  - `README.md:389`, `392`, `404`, `407`, `410`: workflow examples use `Ralph packet` for implementation routing/scope.
- Manual comparison outcome:
  - README route table now matches `naming-and-ids.md` route ownership: implementation goes through Ralph, while packets remain bounded contracts.
  - README workflow wording now matches `truth-and-authority.md`: workflow skills coordinate work across owner layers and do not create new truth layers.
  - README inner-loop and packet sections still preserve packet sibling grammar: critique and wiki may reuse packet discipline without becoming Ralph-governed; packets are support artifacts, not project truth owners.

# Supports Claims

- `ticket:yk89awl5#ACC-001`
- `ticket:yk89awl5#ACC-002`
- `ticket:yk89awl5#ACC-003`
- `ticket:yk89awl5#ACC-004`
- `initiative:skills-corpus-perfection-council-followup#OBJ-004`

# Challenges Claims

None.

# Environment

Commit: `57f19fbf5eafede98d179978e14b736c0068bb69`
Branch: `main`
Runtime: Markdown-only structural validation
OS: Darwin
Relevant config: no build/test runtime; validation used file inspection, targeted search, and `git diff --check`.

# Validity

Valid for: README alignment diff in the current working tree against commit `57f19fbf5eafede98d179978e14b736c0068bb69`.
Recheck when: README, bootstrap route/authority doctrine, packet-frontmatter grammar, or naming-and-IDs route ownership changes before acceptance.

# Limitations

- This evidence is structural and manual; it does not include oracle critique.
- It does not prove the README is maximally clear to all operators, only that the inspected passages align with the cited bootstrap and packet grammar.
- It does not close the ticket because mandatory oracle critique remains pending.

# Result

README public framing now sends bounded implementation through Ralph with a Ralph
packet, keeps packets as support contracts rather than route/truth owners, and
states that workflow skills coordinate existing owner-layer routes without
creating ledgers.

# Interpretation

The observed README text supports moving `ticket:yk89awl5` to `review_required`
for mandatory oracle critique. It does not by itself satisfy `ticket:yk89awl5#ACC-005`.

# Related Records

- `ticket:yk89awl5`
- `packet:ralph-ticket-yk89awl5-20260502T163744Z`
- `initiative:skills-corpus-perfection-council-followup#OBJ-004`
