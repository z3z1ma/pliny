from __future__ import annotations

from .models import InteractionBlock, SessionPhase


def build_decision_prompt(context: str, recent_blocks: list[InteractionBlock], phase: SessionPhase) -> str:
    context_excerpt = context[-8000:] if context else "(no context yet)"
    history = format_block_history(recent_blocks)
    return f"""You are a shaping agent in a Loom session. Your job is to help the operator
shape their fuzzy intent into concrete Loom records (tickets, specs, plans, research).

## Current Phase: {phase.value}

## Internal Context Document
{context_excerpt}

## Recent Interaction History
{history}

## Your Task
Based on the context and history above, decide your SINGLE next action.
Output EXACTLY ONE structured ```action block and no other fenced blocks.

### If you need more information from the codebase
```action
type: explore
goal: <what to explore and why>
context_excerpt: <optional relevant context excerpt>
```

### If you need to ask the operator a question
```action
type: question
question: <one focused question>
options: <comma-separated options, or "open" for free text>
context_ref: <what part of the context this relates to>
```

### If you discovered something the operator should know
```action
type: observation
observation: <what you noticed>
evidence: <file paths, code snippets, or record refs that support this>
```

### If you are ready to propose a record
```action
type: propose
surface: <tickets|specs|plans|research>
title: <record title>
content: <full Markdown content of the proposed record>
```

### If you see multiple valid directions
```action
type: branch
branches: <branch_a_label> | <branch_b_label>
reasoning: <why these are materially different paths>
```

## Guidelines
- Ask ONE focused question at a time, not a list.
- Questions should narrow the design space, not gather information you could find yourself.
- Explore before asking when the repository, existing records, or context document can answer the question.
- Before proposing, verify you have enough context and the scope boundary is coherent.
- Proposals should be detailed, complete records rather than stubs.
- Observe contradictions, missing pieces, scope creep, and incoherence.
- If the operator gave a clear enough direction, propose records rather than asking more.
- Move toward proposing records as quickly as certainty allows.
"""


def format_block_history(blocks: list[InteractionBlock]) -> str:
    if not blocks:
        return "(no interaction blocks yet)"
    return "\n".join(_format_block(block) for block in blocks)


def _format_block(block: InteractionBlock) -> str:
    content = block.content
    if "text" in content:
        summary = content["text"]
    elif "question" in content:
        summary = content["question"]
    elif "observation" in content:
        summary = content["observation"]
    elif "title" in content:
        summary = f"{content.get('surface', 'record')}: {content['title']}"
    elif "summary" in content:
        summary = content["summary"]
    elif "goal" in content:
        summary = content["goal"]
    elif "branches" in content:
        summary = ", ".join(branch.get("label", "") for branch in content["branches"])
    else:
        summary = str(content)
    return f"- {block.type.value}: {_one_line(str(summary))}"


def _one_line(value: str, limit: int = 500) -> str:
    value = " ".join(value.split())
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."
