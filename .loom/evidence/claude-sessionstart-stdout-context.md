---
id: evidence:claude-sessionstart-stdout-context
kind: evidence
status: recorded
created_at: 2026-04-26T02:59:44Z
updated_at: 2026-04-26T05:15:49Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:q7h1d05q
    - ticket:cldrel01
  research:
    - research:loom-install-distribution-methods
  evidence:
    - evidence:claude-plugin-hybrid
external_refs:
  claude_docs:
    - https://code.claude.com/docs/en/hooks
    - https://code.claude.com/docs/en/plugins
    - https://code.claude.com/docs/en/plugins-reference
  inspiration:
    - https://github.com/obra/superpowers
---

# Summary

Observed that a Claude plugin `SessionStart` command hook can print small raw
text to stdout and have that text visible to Claude in the same session. Full-rule
validation did **not** support replacing the earlier Claude sync/guard prototype
with a simple monolithic hook-context loader: Claude exposed the 44.5 KB Loom rule
corpus as a persisted hook-output preview, not as fully queryable same-session
context. A follow-up validation found plugin-root static files were not loaded by
native plugin context, while 26-chunk structured `SessionStart`
`additionalContext` and seven-command per-rule raw stdout candidates exposed the
full rule corpus. The repository plugin now implements the simpler per-rule raw
stdout shape, and local startup validation observed all seven rule files visible
without preview/truncation.

This evidence was gathered after inspecting `obra/superpowers`, which uses a
Claude plugin hook on `startup|clear|compact` to emit context at session start.
The observation challenges the earlier assumption that hook-delivered context was
not viable for Loom's Claude plugin simplification.

# Procedure

- Cloned `https://github.com/obra/superpowers` into
  `/tmp/loom-superpowers.ug453Z/superpowers` with `git clone --depth 1`.
- Inspected `hooks/hooks.json`, `hooks/run-hook.cmd`, `hooks/session-start`,
  `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json`.
- Re-fetched current Claude hook and plugin docs.
- Created a temporary Claude plugin under `/tmp/loom-claude-cat-probe/plugin` with:
  - `.claude-plugin/plugin.json`
  - `hooks/hooks.json`
  - `rules/01-probe.md`
- The temporary hook used:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "cat \"${CLAUDE_PLUGIN_ROOT}\"/rules/*.md",
            "async": false
          }
        ]
      }
    ]
  }
}
```

- The temporary rule file contained a unique `CLAUDE_HOOK_CAT_PROBE` marker.
- Ran `claude plugin validate /tmp/loom-claude-cat-probe/plugin`.
- Ran a one-turn Claude probe from `/tmp/loom-claude-cat-probe/project` with
  `--plugin-dir /tmp/loom-claude-cat-probe/plugin` and asked whether the marker
  was visible in loaded context.

# Artifacts

Superpowers hook shape:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start",
            "async": false
          }
        ]
      }
    ]
  }
}
```

Superpowers `hooks/session-start` emits structured Claude context output:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "..."
  }
}
```

Claude docs extraction from `https://code.claude.com/docs/en/hooks` reported:

```text
SessionStart matcher values:
- startup - new session
- resume - --resume, --continue, or /resume
- clear - /clear
- compact - auto or manual compaction

For SessionStart, any text the hook script prints to stdout is added as context
for Claude.
```

Temporary probe plugin validation:

```text
Validating plugin manifest: /tmp/loom-claude-cat-probe/plugin/.claude-plugin/plugin.json

Warning: author information not provided
Validation passed with warnings
```

Claude runtime probe result:

```json
{"probe_visible": true, "source": "SessionStart stdout"}
```

The command result reported:

```text
Runtime: Claude Code 2.1.119
Session: ef3865eb-9cd2-400b-98c9-a460f2702ddb
Cost: 0.25121750000000004 USD
Cache creation input tokens: 40078
```

## Full-rule candidate validation on repository plugin

Candidate 1 temporarily changed `hooks/hooks.json` to the simple raw stdout
shape:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "cat \"${CLAUDE_PLUGIN_ROOT}\"/rules/*.md",
            "async": false
          }
        ]
      }
    ]
  }
}
```

Structural validation command:

```bash
claude plugin validate .
```

Result:

```text
Validating marketplace manifest: /Users/alexanderbutler/code_projects/personal/agent-loom/.claude-plugin/marketplace.json

✔ Validation passed
```

Same-session startup probe used the real repository plugin with project settings
only, no tools, a custom system prompt, and an empty temporary working directory
(`/tmp/loom-claude-empty-probe`) to avoid project Claude rules. The first probe
confirmed attribution to the startup hook but described the content as a preview:

```bash
claude -p --plugin-dir "/Users/alexanderbutler/code_projects/personal/agent-loom" --no-session-persistence --output-format json --max-budget-usd 1 --tools "" --setting-sources project --system-prompt "You are a probe. Answer only the requested JSON." "Reply with compact JSON only. This run uses a custom system prompt, project-only settings, an empty temporary working directory, and the repository plugin via --plugin-dir. Do you see Loom operating rules in your loaded context? Include keys loom_loaded, source, observed_rule_titles with two exact Loom rule titles, and note. Do not use tools."
```

Result excerpt:

```json
{
  "loom_loaded": true,
  "source": "SessionStart startup hook persisted-output (44.5KB file preview in system-reminder)",
  "observed_rule_titles": ["Mandatory Operating Sequence", "What Loom Optimizes For"],
  "note": "Loom protocol loaded via startup hook..."
}
```

The ordered full-rule probe failed to see later rule documents:

```bash
claude -p --plugin-dir "/Users/alexanderbutler/code_projects/personal/agent-loom" --no-session-persistence --output-format json --max-budget-usd 1 --tools "" --setting-sources project --system-prompt "You are a probe. Answer only the requested JSON." "Reply with compact JSON only. This run uses a custom system prompt, project-only settings, an empty temporary working directory, and the repository plugin via --plugin-dir. From loaded context only, list the Loom top-level rule document titles in order. Include keys loom_loaded, source, ordered_rule_titles, count, and late_rule_phrase with one short exact phrase from the validation/honesty rule. Do not use tools."
```

Result excerpt:

```json
{
  "loom_loaded": true,
  "source": "startup hook persisted output (44.5KB total, 2KB preview)",
  "ordered_rule_titles": ["Core Identity"],
  "count": 1,
  "late_rule_phrase": "not visible in preview - validation/honesty rule section truncated"
}
```

Candidate 2 temporarily changed the hook command to emit structured Claude hook
context rather than raw text:

```bash
python3 -c 'import glob,json,os,pathlib; root=os.environ["CLAUDE_PLUGIN_ROOT"]; paths=sorted(glob.glob(os.path.join(root,"rules","*.md"))); text="\n\n".join(pathlib.Path(p).read_text(encoding="utf-8") for p in paths); print(json.dumps({"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":text}}))'
```

Structural validation again passed:

```text
Validating marketplace manifest: /Users/alexanderbutler/code_projects/personal/agent-loom/.claude-plugin/marketplace.json

✔ Validation passed
```

The same ordered full-rule probe still saw only a preview/truncated subset:

```json
{
  "loom_loaded": true,
  "source": "sessionstart-hook-additionalContext",
  "ordered_rule_titles": [
    "Core Identity",
    "The Main Mental Model",
    "What Loom Optimizes For",
    "Mandatory Operating Sequence"
  ],
  "count": 4,
  "late_rule_phrase": "preview_truncated_at_2kb_of_44.5kb"
}
```

A second structured probe without the custom system prompt was stricter:

```json
{
  "loom_loaded": false,
  "source": "truncated_preview_only",
  "ordered_rule_titles": [],
  "count": 0,
  "late_rule_phrase": "unable_to_locate_validation_honesty_rule_in_truncated_preview",
  "note": "Preview shows 2KB of 44.5KB persisted output... but full rule document titles and validation/honesty rule content not visible in loaded context"
}
```

The repository hook/scripts/docs were restored after these probes because neither
raw stdout nor structured `hookSpecificOutput.additionalContext` satisfied the
packet's full-rule same-session requirement.

## Iteration 2 validation: native static context and chunked hook context

Packet: `packet:ralph-ticket-cldrel01-20260426T031800Z`.

Environment remained local `--plugin-dir` only, with real user Claude auth,
`--setting-sources project`, no tools, `--no-session-persistence`, empty
temporary working directories, and Claude Code 2.1.119 model reporting. The probe
did not mutate real Claude user config, product files, tickets, wiki, docs,
hooks, scripts, or the packet.

### Probe A: native plugin static context

Temporary shape:

- base: `/tmp/loom-claude-native-static.8pzTct`
- plugin root: `/tmp/loom-claude-native-static.8pzTct/plugin`
- empty project: `/tmp/loom-claude-native-static.8pzTct/project`
- plugin manifest: `.claude-plugin/plugin.json`
- static candidates generated from full ordered `rules/*.md`:
  - plugin-root `CLAUDE.md` with sentinel `LOOM_NATIVE_STATIC_CLAUDE_MD_SENTINEL_6D4F9A`
  - plugin-root `.claude/rules/loom.md` with sentinel `LOOM_NATIVE_STATIC_RULES_FILE_SENTINEL_B71C2E`
- generated corpus bytes: `45880`
- generated `CLAUDE.md` bytes: `45929`
- generated `.claude/rules/loom.md` bytes: `45930`

Creation command:

```bash
set -eu; BASE="$(mktemp -d /tmp/loom-claude-native-static.XXXXXX)"; PLUGIN="$BASE/plugin"; PROJECT="$BASE/project"; mkdir -p "$PLUGIN/.claude-plugin" "$PLUGIN/.claude/rules" "$PROJECT"; python3 - "$PLUGIN" <<'PY'
import json, sys
from pathlib import Path
repo=Path('/Users/alexanderbutler/code_projects/personal/agent-loom')
plugin=Path(sys.argv[1])
rules=[]
for p in sorted((repo/'rules').glob('*.md')):
    rules.append(f"<!-- SOURCE {p.name} -->\n" + p.read_text(encoding='utf-8'))
corpus="\n\n".join(rules)
manifest={"name":"loom-native-static-probe","version":"0.0.0-probe","description":"Temporary validation probe for plugin-bundled static Loom context.","author":{"name":"loom-validation-probe"}}
(plugin/'.claude-plugin'/'plugin.json').write_text(json.dumps(manifest, indent=2)+"\n", encoding='utf-8')
(plugin/'CLAUDE.md').write_text("# LOOM_NATIVE_STATIC_CLAUDE_MD_SENTINEL_6D4F9A\n\n"+corpus+"\n", encoding='utf-8')
(plugin/'.claude'/'rules'/'loom.md').write_text("# LOOM_NATIVE_STATIC_RULES_FILE_SENTINEL_B71C2E\n\n"+corpus+"\n", encoding='utf-8')
print(f"corpus_bytes={len(corpus.encode('utf-8'))}")
print(f"claude_md_bytes={(plugin/'CLAUDE.md').stat().st_size}")
print(f"rules_file_bytes={(plugin/'.claude'/'rules'/'loom.md').stat().st_size}")
PY
printf 'BASE=%s\nPLUGIN=%s\nPROJECT=%s\n' "$BASE" "$PLUGIN" "$PROJECT"
```

Creation result:

```text
corpus_bytes=45880
claude_md_bytes=45929
rules_file_bytes=45930
BASE=/tmp/loom-claude-native-static.8pzTct
PLUGIN=/tmp/loom-claude-native-static.8pzTct/plugin
PROJECT=/tmp/loom-claude-native-static.8pzTct/project
```

Validation command:

```bash
claude plugin validate "/tmp/loom-claude-native-static.8pzTct/plugin"
```

Validation result:

```text
Validating plugin manifest: /tmp/loom-claude-native-static.8pzTct/plugin/.claude-plugin/plugin.json

✔ Validation passed
```

Runtime probe command, run from
`/tmp/loom-claude-native-static.8pzTct/project`:

```bash
claude -p --plugin-dir "/tmp/loom-claude-native-static.8pzTct/plugin" --no-session-persistence --output-format json --max-budget-usd 1 --tools "" --setting-sources project --system-prompt "You are a validation probe. Use only loaded context; do not use tools. Answer only compact JSON." "From loaded context only, report whether plugin-bundled static Loom context is visible. Do not use tools. Return compact JSON with keys native_static_visible, visible_sources, sentinels_seen, early_rule, middle_rule, late_rule, confidence, note. sentinels_seen should mention any exact LOOM_NATIVE_STATIC_* sentinel visible. early_rule: exact title or phrase from 01-core-identity if visible. middle_rule: exact title or phrase from 04-ralph-inner-loop if visible. late_rule: exact title or phrase from 07-validation-and-honesty if visible."
```

Runtime result excerpt:

```json
{
  "native_static_visible": false,
  "visible_sources": ["system-reminder", "currentDate"],
  "sentinels_seen": [],
  "early_rule": null,
  "middle_rule": null,
  "late_rule": null,
  "confidence": "high",
  "note": "No Loom static context detected in loaded context"
}
```

Observed command metadata: duration `9732ms`; total cost `$0.008511`; session
`03041066-7159-4c22-8d7e-a651aa94f4e3`.

Conclusion: native plugin-bundled static context via plugin-root `CLAUDE.md` and
plugin-root `.claude/rules/loom.md` is not validated for `--plugin-dir` loading.
Neither sentinel nor early/middle/late rule content was visible.

### Probe B: chunked structured SessionStart additionalContext

Probe B ran because Probe A failed.

Temporary shape:

- base: `/tmp/loom-claude-chunked-hook.rjNNkY`
- plugin root: `/tmp/loom-claude-chunked-hook.rjNNkY/plugin`
- empty project: `/tmp/loom-claude-chunked-hook.rjNNkY/project`
- plugin manifest: `.claude-plugin/plugin.json`
- hook manifest: `hooks/hooks.json`
- hook helper: `hooks/emit-chunk.py`
- chunk files: `chunks/01.txt` through `chunks/26.txt`
- chunk sentinel format: `LOOM_CHUNKED_HOOK_SENTINEL_START chunk=NN/26`
- ordered corpus bytes: `45957`
- chunk count: `26`
- max chunk file bytes: `1889`
- first chunk bytes: `1889`
- last chunk bytes: `1046`

The candidate used 26 synchronous command hook entries, each printing one JSON
object with `hookSpecificOutput.hookEventName = "SessionStart"` and one
`additionalContext` chunk under the observed 2 KB preview threshold.

Creation command:

```bash
set -eu; BASE="$(mktemp -d /tmp/loom-claude-chunked-hook.XXXXXX)"; PLUGIN="$BASE/plugin"; PROJECT="$BASE/project"; mkdir -p "$PLUGIN/.claude-plugin" "$PLUGIN/hooks" "$PLUGIN/chunks" "$PROJECT"; python3 - "$PLUGIN" <<'PY'
import json, sys
from pathlib import Path
repo=Path('/Users/alexanderbutler/code_projects/personal/agent-loom')
plugin=Path(sys.argv[1])
parts=[]
for p in sorted((repo/'rules').glob('*.md')):
    parts.append(f"\n\n===== LOOM_RULE_FILE {p.name} =====\n" + p.read_text(encoding='utf-8'))
corpus="".join(parts).strip()+"\n"
max_bytes=1800
chunks=[]
cur=[]
cur_b=0
for ch in corpus:
    b=len(ch.encode('utf-8'))
    if cur and cur_b + b > max_bytes:
        chunks.append(''.join(cur)); cur=[ch]; cur_b=b
    else:
        cur.append(ch); cur_b += b
if cur:
    chunks.append(''.join(cur))
total=len(chunks)
for i, text in enumerate(chunks, 1):
    wrapped=(f"LOOM_CHUNKED_HOOK_SENTINEL_START chunk={i:02d}/{total:02d}\n" + text + f"\nLOOM_CHUNKED_HOOK_SENTINEL_END chunk={i:02d}/{total:02d}\n")
    (plugin/'chunks'/f'{i:02d}.txt').write_text(wrapped, encoding='utf-8')
manifest={"name":"loom-chunked-hook-probe","version":"0.0.0-probe","description":"Temporary validation probe for chunked SessionStart additionalContext.","author":{"name":"loom-validation-probe"}}
(plugin/'.claude-plugin'/'plugin.json').write_text(json.dumps(manifest, indent=2)+"\n", encoding='utf-8')
emit='''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
idx=sys.argv[1]
root=Path(os.environ["CLAUDE_PLUGIN_ROOT"])
text=(root/"chunks"/f"{int(idx):02d}.txt").read_text(encoding="utf-8")
print(json.dumps({"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":text}}))
'''
(plugin/'hooks'/'emit-chunk.py').write_text(emit, encoding='utf-8')
(plugin/'hooks'/'emit-chunk.py').chmod(0o755)
hooks=[{"type":"command","command":f"python3 \"${{CLAUDE_PLUGIN_ROOT}}/hooks/emit-chunk.py\" {i}","async":False,"timeout":10} for i in range(1,total+1)]
(plugin/'hooks'/'hooks.json').write_text(json.dumps({"description":"Temporary chunked hook context probe.","hooks":{"SessionStart":[{"matcher":"startup","hooks":hooks}]}}, indent=2)+"\n", encoding='utf-8')
print(f"corpus_bytes={len(corpus.encode('utf-8'))}")
print(f"chunk_count={total}")
print(f"max_chunk_file_bytes={max((plugin/'chunks'/f'{i:02d}.txt').stat().st_size for i in range(1,total+1))}")
print(f"first_chunk_bytes={(plugin/'chunks'/'01.txt').stat().st_size}")
print(f"last_chunk_bytes={(plugin/'chunks'/f'{total:02d}.txt').stat().st_size}")
PY
printf 'BASE=%s\nPLUGIN=%s\nPROJECT=%s\n' "$BASE" "$PLUGIN" "$PROJECT"
```

Creation result:

```text
corpus_bytes=45957
chunk_count=26
max_chunk_file_bytes=1889
first_chunk_bytes=1889
last_chunk_bytes=1046
BASE=/tmp/loom-claude-chunked-hook.rjNNkY
PLUGIN=/tmp/loom-claude-chunked-hook.rjNNkY/plugin
PROJECT=/tmp/loom-claude-chunked-hook.rjNNkY/project
```

Validation command:

```bash
claude plugin validate "/tmp/loom-claude-chunked-hook.rjNNkY/plugin"
```

Validation result:

```text
Validating plugin manifest: /tmp/loom-claude-chunked-hook.rjNNkY/plugin/.claude-plugin/plugin.json

✔ Validation passed
```

Runtime probe command, run from
`/tmp/loom-claude-chunked-hook.rjNNkY/project`:

```bash
claude -p --plugin-dir "/tmp/loom-claude-chunked-hook.rjNNkY/plugin" --no-session-persistence --output-format json --max-budget-usd 1 --tools "" --setting-sources project --system-prompt "You are a validation probe. Use only loaded context; do not use tools. Answer only compact JSON." "From loaded context only, report whether chunked SessionStart hook additionalContext made the full Loom rule corpus visible. Do not use tools. Return compact JSON with keys chunked_context_visible, source, chunk_sentinels_seen, early_rule_evidence, middle_rule_evidence, validation_honesty_evidence, missing_expected_content, confidence, note. chunk_sentinels_seen should include exact visible LOOM_CHUNKED_HOOK_SENTINEL_START examples for first, middle, and last chunks if visible. early_rule_evidence should quote or identify content from 01-core-identity. middle_rule_evidence should quote or identify content from 04-ralph-inner-loop. validation_honesty_evidence should quote or identify content from 07-validation-and-honesty."
```

Runtime result excerpt:

```json
{
  "chunked_context_visible": true,
  "source": "system-reminder SessionStart hook additionalContext",
  "chunk_sentinels_seen": {
    "first": "LOOM_CHUNKED_HOOK_SENTINEL_START chunk=01/26",
    "middle": "LOOM_CHUNKED_HOOK_SENTINEL_START chunk=13/26",
    "last": "LOOM_CHUNKED_HOOK_SENTINEL_START chunk=26/26"
  },
  "early_rule_evidence": {
    "file": "01-core-identity.md",
    "chunk": "01/26",
    "quote": "Loom is a mandatory operating protocol whenever Loom is present in the workspace. It is not decorative documentation and it is not a loose suggestion."
  },
  "middle_rule_evidence": {
    "file": "04-ralph-inner-loop.md",
    "chunk": "11/26",
    "quote": "Ralph is Loom's implementation loop. It exists to make execution reliable by using: fresh context, bounded packets, explicit scope, explicit write boundaries"
  },
  "validation_honesty_evidence": {
    "file": "07-validation-and-honesty.md",
    "chunks": ["24/26", "26/26"],
    "quote": "Loom is only useful if its records are truthful and its completion claims mean something. Work is done only when all relevant conditions are true"
  },
  "missing_expected_content": [],
  "confidence": 0.98,
  "note": "All 26 chunks present with clear sentinels. All 7 rule files visible..."
}
```

Observed command metadata: duration `25258ms`; total cost `$0.06996375`; session
`5aa78756-6d32-43d5-a647-d58aeccbc4a0`.

Conclusion: chunked structured `SessionStart` `additionalContext` is technically
viable in this local `--plugin-dir` startup probe. However, it required 26
synchronous hook command entries for the current full rule corpus, which is
materially more complex and brittle than the previously failed monolithic hook
candidate.

### Probe C: per-rule raw SessionStart stdout

Probe C tested the operator hypothesis that each Loom rule file is under Claude's
documented 10,000-character hook-output cap and can therefore be emitted as a
separate hook output instead of arbitrary 1.8 KB chunks.

Documentation and source support inspected before the probe:

- Claude hooks docs state hook output injected into context is capped at 10,000
  characters, and output above that limit is replaced with a saved-output preview.
- Local Claude Code source snapshot `/tmp/claudecodesource.G3zKWe` includes
  `MAX_HOOK_OUTPUT_LENGTH = 10000` in
  `src/utils/processUserInput/processUserInput.ts` for hook additional-context
  truncation.
- The same source snapshot shows matching hooks run concurrently in
  `src/utils/hooks.ts`, using `all(hookPromises)`, and `src/utils/generators.ts`
  documents that `all()` yields values as they come in. This means separate hook
  outputs can avoid the per-output cap but should not be assumed to preserve
  manifest order.

Temporary shape:

- base: `/tmp/loom-claude-per-rule-hook.0jCbp7`
- plugin root: `/tmp/loom-claude-per-rule-hook.0jCbp7/plugin`
- empty project: `/tmp/loom-claude-per-rule-hook.0jCbp7/project`
- hook manifest: seven `SessionStart` command hooks under matcher `startup`
- each hook emitted one rule with a source marker, using command shape:
  `printf '===== LOOM_RULE_FILE <file> =====\n'; cat "${CLAUDE_PLUGIN_ROOT}"/rules/<file>`

Per-rule sizes observed during probe setup:

```text
01-core-identity.md chars=5165 bytes=5171
02-truth-and-authority.md chars=7738 bytes=7738
03-outer-loop.md chars=5147 bytes=5149
04-ralph-inner-loop.md chars=9325 bytes=9335
05-critique-and-wiki.md chars=8269 bytes=8303
06-filesystem-and-tooling.md chars=5384 bytes=5384
07-validation-and-honesty.md chars=4508 bytes=4508
rule_count=7
```

Validation command:

```bash
claude plugin validate "/tmp/loom-claude-per-rule-hook.0jCbp7/plugin"
```

Validation result:

```text
Validating plugin manifest: /tmp/loom-claude-per-rule-hook.0jCbp7/plugin/.claude-plugin/plugin.json

✔ Validation passed
```

Runtime probe command, run from
`/tmp/loom-claude-per-rule-hook.0jCbp7/project`:

```bash
claude -p --plugin-dir "/tmp/loom-claude-per-rule-hook.0jCbp7/plugin" --no-session-persistence --output-format json --max-budget-usd 1 --tools "" --setting-sources project --system-prompt "You are a validation probe. Use only loaded context; do not use tools. Answer only compact JSON." "From loaded context only, report whether per-rule SessionStart hook stdout made all Loom rule files visible. Do not use tools. Return compact JSON with keys per_rule_context_visible, source, rule_files_seen, rule_count, early_rule_evidence, middle_rule_evidence, validation_honesty_evidence, any_preview_or_truncation, ordering_observation, confidence, note. rule_files_seen should list exact LOOM_RULE_FILE filenames visible. early_rule_evidence should quote content from 01-core-identity.md. middle_rule_evidence should quote content from 04-ralph-inner-loop.md. validation_honesty_evidence should quote content from 07-validation-and-honesty.md."
```

Runtime result excerpt:

```json
{
  "per_rule_context_visible": true,
  "source": "SessionStart hook stdout in system-reminder blocks",
  "rule_files_seen": [
    "01-core-identity.md",
    "02-truth-and-authority.md",
    "05-critique-and-wiki.md",
    "06-filesystem-and-tooling.md",
    "04-ralph-inner-loop.md",
    "03-outer-loop.md",
    "07-validation-and-honesty.md"
  ],
  "rule_count": 7,
  "any_preview_or_truncation": false,
  "ordering_observation": "Files loaded in non-sequential numerical order: 01, 02, 05, 06, 04, 03, 07",
  "confidence": "high",
  "note": "All 7 rule files fully visible with complete content, no truncation markers detected"
}
```

The same response quoted content from `01-core-identity.md`,
`04-ralph-inner-loop.md`, and `07-validation-and-honesty.md` without tools.

Observed command metadata: duration `22975ms`; total cost `$0.06120375`; session
`96eaa655-e267-48e6-a521-18ec84da2849`.

Conclusion: per-rule raw `SessionStart` stdout is technically viable in this
local startup probe and is materially simpler than the 26-command arbitrary
chunking candidate. It still needs a design decision before productization because
separate hooks run concurrently and the observed context order was non-sequential.

# Supports Claims

- Supports: Claude `SessionStart` hook stdout can add same-session context in
  Claude Code 2.1.119 when the output is small.
- Supports: a Claude plugin can locate bundled files through
  `${CLAUDE_PLUGIN_ROOT}` and emit their contents from a hook command.
- Supports: the `startup|clear|compact` matcher shape used by `superpowers` is
  accepted structurally by Claude plugin validation for a local plugin.
- Supports: the real repository plugin validates structurally when temporarily
  changed to either raw `cat` stdout or structured
  `hookSpecificOutput.additionalContext` emission.
- Supports: plugin-root `CLAUDE.md` and plugin-root `.claude/rules/loom.md`
  inside a local plugin directory validated structurally but were not loaded as
  model-visible context by `--plugin-dir` startup.
- Supports: 26 chunked structured `SessionStart` `additionalContext` outputs,
  each below the observed 2 KB preview threshold, were visible enough for Claude
  to quote early `01-core-identity`, middle `04-ralph-inner-loop`, and late
  `07-validation-and-honesty` content without tools.
- Supports: seven per-rule raw `SessionStart` stdout hook outputs, each below the
  documented 10,000-character hook-output cap, made the full Loom rule corpus
  visible in one local startup probe without preview/truncation.
- Supports: the repository plugin implementation of seven source-marked per-rule
  `SessionStart` stdout hooks validates structurally and made all seven rule files
  visible in same-session local `--plugin-dir` startup probing without
  preview/truncation.
- Supports: with the final staggered sleeps, `01-core-identity.md` appeared first
  in three repeated local startup ordering probes, while the remaining files still
  appeared in non-numeric order.

# Challenges Claims

- Challenges the earlier design assumption in `research:loom-install-distribution-methods`
  and `ticket:q7h1d05q` that hook-delivered context should remain rejected for
  Loom's Claude adapter without a fresh probe.
- Challenges the need for the current `scripts/claude-sync-rules.sh`,
  `scripts/claude-loom-restart-guard.sh`, and `scripts/claude-clean-rules.sh`
  stack if same-session hook context proves acceptable for Loom's rule-loading
  semantics.
- Challenges replacing the sync/guard stack now: full 44.5 KB rule-corpus output
  was exposed as a 2 KB persisted hook-output preview, and later rule files such
  as validation/honesty were not visible to the same-session probe.
- Challenges a native static-context simplification: plugin-bundled `CLAUDE.md`
  and `.claude/rules/loom.md` were not visible from an empty project when loaded
  through local `--plugin-dir`.
- Challenges a chunked-hook implementation on maintainability grounds: the
  validated candidate needed 26 synchronous hook commands for one rule corpus,
  making it sensitive to corpus growth, ordering, hook execution behavior, and
  Claude's undocumented aggregation/preview behavior.
- Challenges rejecting hook-context simplification solely because arbitrary
  chunking is too brittle: semantic per-rule outputs are simpler and worked in one
  local startup probe.
- Challenges assuming separate hook outputs preserve Loom rule order: the per-rule
  probe observed non-sequential context order.

# Environment

Commit: bac5544 plus local candidate edits during `ticket:cldrel01` validation
Branch: main
Runtime: Claude Code 2.1.119
OS: darwin
Relevant config: temporary plugin at `/tmp/loom-claude-cat-probe/plugin`; local
Claude run with real user auth and `--plugin-dir`; full-rule monolithic probes
used `/tmp/loom-claude-empty-probe`, project-only settings, no tools, and the
real repository plugin. Follow-up probes used
`/tmp/loom-claude-native-static.8pzTct`,
`/tmp/loom-claude-chunked-hook.rjNNkY`, and
`/tmp/loom-claude-per-rule-hook.0jCbp7`, each with empty temporary projects,
project-only settings, no tools, and local `--plugin-dir`.

# Validity

Valid for: local `--plugin-dir` Claude Code 2.1.119 behavior for one small raw
stdout `SessionStart` hook on the `startup` event, failed monolithic full-rule
startup probes using the real repository plugin, failed plugin-root static
context startup probe using a temporary plugin, and one successful 26-chunk
structured `SessionStart` `additionalContext` startup probe using a temporary
plugin, one successful seven-command per-rule raw stdout startup probe using a
temporary plugin, and repository-plugin implementation probes using local
`--plugin-dir` startup with project-only settings, no tools, and empty temporary
projects.

Recheck when: Claude changes hook-output preview behavior, changes plugin static
context loading semantics, splitting the corpus into smaller hook-context
segments, changing to installed marketplace plugin mode, testing `clear` or
`compact`, testing Windows, or preparing release docs.

# Limitations

- This did not test an installed marketplace plugin.
- This did not test `clear` or `compact`; it tested session startup.
- The final repository plugin implementation configures `startup|clear|compact`,
  but only `startup` was validated headlessly.
- Static native-context probing tested local `--plugin-dir` only; marketplace
  installation may differ.
- Full-rule startup probes tested concatenating all Loom rule files and showed the
  output was previewed/truncated rather than fully visible to the model.
- Chunked hook probing depended on model self-report from loaded context and did
  not independently inspect Claude's internal context representation.
- Chunked hook probing tested one generated 26-command implementation shape, not
  a polished product design, and did not measure startup latency across repeated
  runs.
- Per-rule hook probing depended on model self-report from loaded context and did
  not independently inspect Claude's internal context representation.
- Per-rule hook probing observed all rules but not numeric ordering; Claude Code
  source inspection suggests matching hooks run concurrently and yield as they
  complete.
- Final repeated repository startup probes observed `01-core-identity.md` first in
  three runs with staggered sleeps, but still observed non-numeric ordering for the
  remaining rule files. This is model-visible ordering evidence, not an
  independent inspection of Claude's internal context ordering.
- This did not prove hook context appears literally before every other context
  segment; it only proved Claude could see it in the same session.
- This did not prove token-cost or cache behavior is acceptable for the full Loom
  rules corpus; the failed full-rule probes reported 44.5 KB hook output and 2 KB
  preview behavior.
- Claude docs still recommend `CLAUDE.md` for static context, so adopting this
  pattern is a deliberate tradeoff rather than doc-preferred default.
- Superpowers uses structured JSON `hookSpecificOutput.additionalContext`; a
  structured full-rule candidate was also probed and still showed preview limits.

# Result

The raw `cat "${CLAUDE_PLUGIN_ROOT}"/rules/*.md` hook model remains feasible for
small marker context but is **not validated** for loading the full Loom rule
corpus. The monolithic structured `hookSpecificOutput.additionalContext` variant
also did not validate for the full corpus in the first full-rule probe.

Native plugin-bundled static context via plugin-root `CLAUDE.md` or
`.claude/rules/loom.md` is **not validated** for local `--plugin-dir` startup;
neither sentinel nor early/middle/late rule content was visible.

Chunked structured `SessionStart` `additionalContext` is **technically viable**
in one local startup probe: Claude reported first, middle, and last chunk
sentinels and quoted content from `01-core-identity.md`,
`04-ralph-inner-loop.md`, and `07-validation-and-honesty.md` without tools. The
candidate is not yet a product recommendation because it required 26 synchronous
hook commands and relies on behavior that is more complex than the sync/guard
model it might replace.

Per-rule raw `SessionStart` stdout is **technically viable** in one local startup
probe: Claude reported all seven rule files visible without preview/truncation and
quoted early, middle, and late rule content. This is simpler than arbitrary
chunking, but it exposed an ordering concern because the observed file order was
not numeric.

The repository Claude plugin now uses the per-rule raw `SessionStart` stdout
shape. Local implementation validation observed all seven rule files visible in
same-session startup context without preview/truncation. Repeated ordering probes
observed `01-core-identity.md` first after larger staggered sleeps, but did not
produce reliable overall numeric order; source markers remain necessary.

## Iteration 3 implementation validation: repository per-rule stdout hooks

Packet: `packet:ralph-ticket-cldrel01-20260426T050555Z`.

Implemented repository plugin shape:

- `hooks/hooks.json` has only a `SessionStart` hook group with matcher
  `startup|clear|compact`.
- The group has seven command hooks, one per top-level `rules/*.md` file.
- Each command emits `===== LOOM_RULE_FILE <filename> =====` and cats exactly one
  `${CLAUDE_PLUGIN_ROOT}/rules/<filename>` file.
- Commands after `01-core-identity.md` use increasing sleeps from `0.20` through
  `1.20` seconds. This is only a best-effort ordering nudge; Claude hook ordering
  is not guaranteed.
- The generated-rule scripts were removed from the product source:
  `scripts/claude-sync-rules.sh`, `scripts/claude-loom-restart-guard.sh`, and
  `scripts/claude-clean-rules.sh`.

Per-rule output size check, including source marker overhead:

```text
01-core-identity.md chars=5212 bytes=5218
02-truth-and-authority.md chars=7791 bytes=7791
03-outer-loop.md chars=5191 bytes=5193
04-ralph-inner-loop.md chars=9375 bytes=9385
05-critique-and-wiki.md chars=8320 bytes=8354
06-filesystem-and-tooling.md chars=5440 bytes=5440
07-validation-and-honesty.md chars=4564 bytes=4564
```

All seven outputs remained below Claude's documented 10,000-character hook-output
context cap.

Structural validation command:

```bash
claude plugin validate .
```

Result:

```text
Validating marketplace manifest: /Users/alexanderbutler/code_projects/personal/agent-loom/.claude-plugin/marketplace.json

✔ Validation passed
```

Same-session startup probe used the repository plugin with local `--plugin-dir`,
an empty temporary project, project-only settings, no tools, no session
persistence, and a custom probe system prompt. Command:

```bash
claude -p --plugin-dir "/Users/alexanderbutler/code_projects/personal/agent-loom" --no-session-persistence --output-format json --max-budget-usd 1 --tools "" --setting-sources project --system-prompt "You are a validation probe. Use only loaded context; do not use tools. Answer only compact JSON in your final text." "From loaded context only, report whether the repository plugin's per-rule SessionStart stdout made all Loom top-level rule files visible without preview/truncation. Do not use tools. Return compact JSON with keys per_rule_context_visible, source, rule_files_seen, rule_count, early_rule_evidence, middle_rule_evidence, validation_honesty_evidence, any_preview_or_truncation, first_visible_rule_file, confidence, note. rule_files_seen must list exact LOOM_RULE_FILE filenames visible. early_rule_evidence must quote content from 01-core-identity.md. middle_rule_evidence must quote content from 04-ralph-inner-loop.md. validation_honesty_evidence must quote content from 07-validation-and-honesty.md."
```

Runtime result excerpt:

```json
{
  "per_rule_context_visible": true,
  "source": "system-reminder SessionStart stdout blocks with LOOM_RULE_FILE headers",
  "rule_files_seen": [
    "01-core-identity.md",
    "02-truth-and-authority.md",
    "03-outer-loop.md",
    "04-ralph-inner-loop.md",
    "05-critique-and-wiki.md",
    "06-filesystem-and-tooling.md",
    "07-validation-and-honesty.md"
  ],
  "rule_count": 7,
  "any_preview_or_truncation": false,
  "first_visible_rule_file": "01-core-identity.md",
  "confidence": "high"
}
```

The response quoted content from `01-core-identity.md`,
`04-ralph-inner-loop.md`, and `07-validation-and-honesty.md` without using tools.
Observed command metadata: duration `28362ms`; total cost `$0.0624675`; session
`7f633cb9-1088-437f-8507-ee0aadc7fe5e`; model reported Claude Sonnet 4.5 with
`11438` cache creation input tokens.

Repeated startup ordering probe command shape:

```bash
for i in 1 2 3; do
  claude -p --plugin-dir "/Users/alexanderbutler/code_projects/personal/agent-loom" --no-session-persistence --output-format json --max-budget-usd 1 --tools "" --setting-sources project --system-prompt "You are a validation probe. Use only loaded context; do not use tools. Answer only compact JSON in your final text." "From loaded context only, inspect the visible LOOM_RULE_FILE source markers from SessionStart hook stdout. Do not use tools. Return compact JSON with keys first_visible_rule_file, ordered_rule_files_seen, rule_count, order_is_numeric, confidence, note. If exact complete order is not reliably visible, still report the first visible LOOM_RULE_FILE marker you can identify."
done
```

Observed ordering results with the final `0.20`-second stagger:

```text
run 1: first=01-core-identity.md; order=01,02,03,04,06,05,07; numeric=false
run 2: first=01-core-identity.md; order=01,05,04,03,02,06,07; numeric=false
run 3: first=01-core-identity.md; order=01,02,06,07,04,03,05; numeric=false
```

Interpretation: the stagger made `01-core-identity.md` appear first in these
three observed startup probes, but it did not make overall numeric order reliable.
The product docs therefore describe ordering as best effort and rely on source
markers for attribution.

Reference reconciliation check for deleted script names:

```text
hooks/hooks.json: no matches
INSTALL.md: no matches
examples/adapters/claude-plugin-install/README.md: no matches
README.md: no matches
ARCHITECTURE.md: no matches
rules/: no matches
skills/: no matches
commands/: no matches
```

Repository-wide search still finds historical or non-write-scope Loom references
in prior tickets, packets, research/wiki summaries, evidence, and critique. Those
records were not edited in this Ralph child iteration because the packet write
scope only allowed this evidence record among `.loom/` records.

# Interpretation

The simplest validated conclusion is narrower: `SessionStart` hook context can
carry small snippets, monolithic full-rule hook context currently appears as a
previewed hook output artifact, native plugin-root static files were not loaded,
chunked structured hook context can make the full corpus visible in one local
startup probe, and per-rule raw hook stdout can make the full corpus visible more
simply when every rule file remains below the documented per-output cap.

`ticket:cldrel01` replaced generated rule sync, restart guard, and cleanup with
the per-rule raw stdout hook design after implementation validation and mandatory
critique. This evidence supports that decision for local startup behavior; it
does not prove installed marketplace mode, Windows shell behavior, runtime
skill/command invocation, or headless `clear|compact` event behavior.

# Related Records

- `ticket:q7h1d05q`
- `ticket:cldrel01`
- `research:loom-install-distribution-methods`
- `evidence:claude-plugin-hybrid`
