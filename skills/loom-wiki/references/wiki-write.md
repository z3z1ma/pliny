# Wiki Write

Wiki write mode promotes accepted understanding into a durable page.

Use it when the source truth is settled enough that future agents should not
have to re-derive the explanation from tickets, critique, research, or chat.

## Goals

- promote accepted understanding into a durable page
- ground the page in accepted records and evidence
- prefer improving an existing page over forking a duplicate
- refuse policy, live execution, or behavior-contract drift into the wiki

## Procedure

1. Anchor the page.
   - Decide whether the target is a concept, workflow, reference, or atlas page.
   - Find existing pages first; prefer updating the right page over creating duplicates.
2. Gather accepted sources.
   - Read the canonical owners and evidence that ground the page.
   - Use critique and research where they sharpen the explanation.
   - Do not source the wiki from unsettled chat residue.
3. Decide whether a wiki packet is warranted.
   - If synthesis is non-trivial or the source set is wide, compile a wiki packet under `.loom/packets/wiki/`.
   - Otherwise write directly with the accepted source set in view.
4. Write or update the page.
   - Choose the proper page family.
   - Explain clearly, link related pages, and cite source records or evidence.
   - Make the page reusable by a future agent.
5. Reconnect the graph.
   - Add or update links from originating tickets, critiques, or plans when useful.
   - If a neighboring page should exist, note it without inventing a page prematurely.
6. Check truth boundaries.
   - If the page starts carrying behavior contract, policy authority, or live execution state, move that truth back into spec, constitution, or ticket and make the wiki refer to it.

## Required Output

- pages created or updated, with paths and IDs
- key claims promoted
- accepted sources used
- related pages or follow-up knowledge gaps
- recommended next owner layer or workflow route

## Guardrails

- Do not promote unsettled claims into the wiki.
- Do not let the wiki become the spec, constitution, or ticket.
- Avoid transcript residue; write durable explanation instead.
- Do not create duplicate pages because a page was not searched first.
