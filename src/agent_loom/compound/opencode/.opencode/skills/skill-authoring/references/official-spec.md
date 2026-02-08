# Skill Specification (Practical Summary)

Source: https://agentskills.io/home

## SKILL.md File Structure

Every Skill requires a `SKILL.md` file with YAML frontmatter followed by Markdown instructions.

### Basic Format

```markdown
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for the agent.

## Examples
Show concrete examples of using this Skill.
```

## Required Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill name using lowercase letters, numbers, and hyphens only (max 64 characters). Should match the directory name. |
| `description` | Yes | What the Skill does and when to use it (max 1024 characters). The runtime uses this for skill discovery. |
| `allowed-tools` | No | Tools the agent can use without asking permission when this Skill is active. Example: `Read, Grep, Glob` |
| `model` | No | Specific model to use when this Skill is active (e.g., `openai/gpt-5.3-codex`). Defaults to the conversation's model. |

## Skill Locations & Priority

```
Enterprise (highest priority) → Personal → Project → Plugin (lowest priority)
```

| Type | Path | Applies to |
|------|------|-----------|
| **Enterprise** | See managed settings | All users in organization |
| **Personal** | `~/.opencode/skills/` | You, across all projects |
| **Project** | `.opencode/skills/` | Anyone working in repository |
| **Plugin** | Bundled with plugins | Anyone with plugin installed |

## How Skills Work

1. **Discovery**: Most runtimes index skill `name` and `description` for discovery
2. **Activation**: When your request matches a Skill's description, the runtime may ask for confirmation
3. **Execution**: The agent follows the Skill's instructions and loads referenced files

**Key Principle**: Skills are **runtime-invoked** — the runtime decides which Skills to suggest/activate based on your request.

## Progressive Disclosure Pattern

Keep `SKILL.md` under 500 lines by linking to supporting files:

```
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

### Example SKILL.md with References

```markdown
---
name: pdf-processing
description: Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction. Requires pypdf and pdfplumber packages.
allowed-tools: Read, Bash(python:*)
---

# PDF Processing

## Quick start

Extract text:
```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For form filling, see [FORMS.md](FORMS.md).
For detailed API reference, see [REFERENCE.md](REFERENCE.md).

## Requirements

Packages must be installed:
```bash
pip install pypdf pdfplumber
```
```

## Restricting Tool Access

```yaml
---
name: reading-files-safely
description: Read files without making changes. Use when you need read-only file access.
allowed-tools: Read, Grep, Glob
---
```

Benefits:
- Read-only Skills that shouldn't modify files
- Limited scope for specific tasks
- Security-sensitive workflows

## Writing Effective Descriptions

The `description` field enables Skill discovery and should include both what the Skill does and when to use it.

**Always write in third person.** The description is injected into the system prompt.

- **Good:** "Processes Excel files and generates reports"
- **Avoid:** "I can help you process Excel files"
- **Avoid:** "You can use this to process Excel files"

**Be specific and include key terms:**

```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Avoid vague descriptions:**

```yaml
description: Helps with documents  # Too vague!
```

## Complete Example: Commit Message Generator

```markdown
---
name: generating-commit-messages
description: Generates clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes.
---

# Generating Commit Messages

## Instructions

1. Run `git diff --staged` to see changes
2. I'll suggest a commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components

## Best practices

- Use present tense
- Explain what and why, not how
```

## Complete Example: Code Explanation Skill

```markdown
---
name: explaining-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

# Explaining Code

When explaining code, always include:

1. **Start with an analogy**: Compare the code to something from everyday life
2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
3. **Walk through the code**: Explain step-by-step what happens
4. **Highlight a gotcha**: What's a common misconception?

Keep explanations conversational. For complex concepts, use multiple analogies.
```

## Distribution

- **Project Skills**: Commit `.opencode/skills/` to version control
- **Plugins**: Add `skills/` directory to plugin with Skill folders
- **Enterprise**: Deploy organization-wide through managed settings
