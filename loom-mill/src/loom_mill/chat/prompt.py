from __future__ import annotations

from loom_mill.chat.session import ChatContext, ChatSession


def build_prompt(
    session: ChatSession,
    new_message: str,
    document_content: str | None,
    context: ChatContext | None,
) -> str:
    """Build full prompt with system context, history, document, context, and message."""
    parts = []
    parts.append("You are a Loom Weaver helping the operator shape records in the Design Room.")
    parts.append("You may edit files in .loom/ as needed. Your edits will appear live in the editor.")

    if document_content:
        parts.append(f"\nCurrent document ({session.document_path}):\n```\n{document_content}\n```")

    if session.messages:
        parts.append("\nConversation so far:")
        for message in session.messages:
            parts.append(f"{message.role.capitalize()}: {message.content}")

    if context:
        parts.append(f"\nThe operator has highlighted text from {context.path}, lines {context.line_range}:")
        parts.append(f"> {context.selected_text}")

    parts.append(f"\nOperator: {new_message}")
    return "\n".join(parts)
