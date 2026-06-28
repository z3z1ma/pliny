Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Target: README.md
Verdict: pass

# README Context And Workflow Refinement Review

## Target

README changes requested after the public-launch polish commit, especially
context terminology, subagent wording, richer record example, removal of the RAG
section, and workflow augmentation framing.

## Findings

- Pass: "Project memory" was replaced with "project context" for the `.10x/`
  substrate while preserving natural language like "remembering" where it is
  not naming the system.
- Pass: The subagent row now names the black-box handoff problem more directly.
- Pass: The richer record example better demonstrates 10x's typed context model:
  authority, provenance, source limits, unresolved semantics, and follow-up
  ownership.
- Pass: The RAG/vector/context-window section was removed, reducing conceptual
  distraction.
- Pass: The workflow section now frames 10x as an augmentation layer under
  existing AI coding workflows rather than a replacement.
- Pass: The Superpowers context informs one table row and the FAQ without
  creating a direct comparison section.
- Minor residual risk: The richer record example adds length. This is acceptable
  because it sells a central differentiator that the prior thin ADR example
  undersold.

## Verdict

Pass. The README now better represents 10x as a layered project context and
authority system rather than just durable notes.

## Residual Risk

Future README compression should preserve the rich-record example or replace it
with an equally context-rich artifact; reverting to a thin ADR would weaken the
product story.
