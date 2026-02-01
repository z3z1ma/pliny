// OpenCode Compound Engineering Plugin
// - Adds deterministic workflow tools (plan/work/review/compound support)
// - Maintains AGENTS.md / LOOM_ROADMAP.md managed blocks (changelog lives in LOOM_ROADMAP.md)
// - Automatically logs observations from tool/hooks
// - Automatically runs a post-turn "learn" pass to create/update instincts + skills
//
// Drop into: .opencode/plugins/compound_engineering.ts
//
// NOTE: This plugin intentionally only writes "memory files" (skills + docs + memos + changelog + instincts).
// It does NOT write product code. If you want code-writing automation, that's your own terrible decision.

import type { Plugin } from "@opencode-ai/plugin";
import { tool } from "@opencode-ai/plugin";

import { spawn } from "node:child_process";
import { randomUUID, createHash } from "node:crypto";
import * as fs from "node:fs/promises";
import * as path from "node:path";

// -----------------------------
// Config
// -----------------------------

const SKILLS_DIR = ".opencode/skills";
const CLAUDE_SKILLS_DIR = ".claude/skills";

const MEMORY_DIR = ".opencode/memory";
const OBSERVATIONS_FILE = path.join(MEMORY_DIR, "observations.jsonl");
const INSTINCTS_FILE = path.join(MEMORY_DIR, "instincts.json");
const INSTINCTS_MD = path.join(MEMORY_DIR, "INSTINCTS.md");

const COMPOUND_DIR = ".opencode/compound";
const STATE_FILE = path.join(COMPOUND_DIR, "state.json");
const PROMPTS_DIR = path.join(COMPOUND_DIR, "prompts");
const AUTOLEARN_PROMPT_FILE = path.join(PROMPTS_DIR, "autolearn.md");

const DEFAULT_LOOM_BIN = process.env.COMPOUND_LOOM_BIN ?? "loom";

const MIRROR_CLAUDE = (process.env.COMPOUND_MIRROR_CLAUDE ?? "1") !== "0";

// Auto-learning defaults: conservative enough to not DDOS your model, aggressive enough to compound.
const AUTO_ENABLED = (process.env.COMPOUND_AUTO ?? "1") !== "0";
const AUTO_COOLDOWN_SECONDS = intEnv("COMPOUND_AUTO_COOLDOWN_SECONDS", 120); // minimum time between runs
const AUTO_MIN_NEW_OBSERVATIONS = intEnv("COMPOUND_AUTO_MIN_NEW_OBSERVATIONS", 12);
const AUTO_MAX_OBSERVATIONS_IN_PROMPT = intEnv("COMPOUND_AUTO_MAX_OBSERVATIONS_IN_PROMPT", 80);
const AUTO_MAX_SKILLS_PER_RUN = intEnv("COMPOUND_AUTO_MAX_SKILLS_PER_RUN", 3);
const AUTO_MAX_INSTINCT_UPDATES_PER_RUN = intEnv("COMPOUND_AUTO_MAX_INSTINCT_UPDATES_PER_RUN", 8);
const AUTO_PROMPT_MAX_CHARS = intEnv("COMPOUND_AUTO_PROMPT_MAX_CHARS", 18000);

const CHANGELOG_MAX_ENTRIES = intEnv("COMPOUND_CHANGELOG_MAX_ENTRIES", 120);
const CHANGELOG_DEDUPE_WINDOW = intEnv("COMPOUND_CHANGELOG_DEDUPE_WINDOW", 20);

const DOC_BLOCK_MAX_CHARS = intEnv("COMPOUND_DOC_BLOCK_MAX_CHARS", 5000);

const LOG_OBSERVATIONS = (process.env.COMPOUND_LOG_OBSERVATIONS ?? "1") !== "0";
const OBS_MAX_BYTES = intEnv("COMPOUND_OBSERVATIONS_MAX_BYTES", 32 * 1024 * 1024); // 32MB

const SKILL_NAME_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/; // per OpenCode skills docs

// -----------------------------
// Types
// -----------------------------

type ISODate = string;

type PluginState = {
  version: 2;
  lastCommand?: { name: string; at: ISODate; sessionID?: string | null };
  autolearn?: {
    lastRunAt?: ISODate;
    lastRunSessionID?: string | null;
    lastObservationCount?: number;
    lastObservationHash?: string;
  };
};

type SkillSpec = {
  name: string; // kebab-case directory name
  description: string;
  body: string; // markdown body (plugin wraps it in a managed block)
  license?: string;
  compatibility?: string;
  tags?: string[];
  metadata?: Record<string, string>;
};

type SkillUpdateSpec = {
  name: string;
  description?: string;
  body: string;
  license?: string;
  compatibility?: string;
  tags?: string[];
  metadata?: Record<string, string>;
};

type Instinct = {
  id: string; // kebab-case
  title: string;
  trigger: string;
  action: string;
  tags?: string[];
  confidence: number; // 0..1
  status: "active" | "deprecated";
  skill?: string; // linked skill name if promoted
  notes?: string;
  created_at: ISODate;
  updated_at: ISODate;
  evidence: Array<{ ts: ISODate; sessionID?: string | null; note?: string }>;
};

type InstinctStore = {
  version: 1;
  instincts: Instinct[];
};

type InstinctCreateSpec = {
  id: string;
  title: string;
  trigger: string;
  action: string;
  tags?: string[];
  confidence?: number;
  skill?: string;
  notes?: string;
  evidence_note?: string;
};

type InstinctUpdateSpec = {
  id: string;
  title?: string;
  trigger?: string;
  action?: string;
  tags?: string[];
  confidence?: number;
  confidence_delta?: number;
  status?: "active" | "deprecated";
  skill?: string | null;
  notes?: string | null;
  evidence_note?: string;
};

type MemosAddSpec = {
  title: string;
  body: string;
  tags?: string[];
  scopes?: string[]; // raw scope strings, eg "command:workflows:plan" or "file:src/foo.ts"
  command?: string; // convenience: stored as scope command:<value>
  ticket?: string; // convenience: stored as scope ticket:<id>
  visibility?: string; // shared|personal|ephemeral (optional)
};

type DocBlockUpsertSpec = {
  file: string; // repo-root-relative (eg "AGENTS.md")
  id: string; // compound managed block id (eg "roadmap-ai-notes")
  content: string;
};

type CompoundSpecV1 = {
  schema_version: 1;
  skills?: {
    create?: SkillSpec[];
    update?: SkillUpdateSpec[];
    deprecate?: Array<{ name: string; reason: string; replacement?: string }>;
  };
  docs?: { sync?: boolean; blocks?: { upsert?: DocBlockUpsertSpec[] } };
  memos?: { add?: MemosAddSpec[] };
  changelog?: { note?: string };
};

type CompoundSpecV2 = {
  schema_version: 2;
  auto?: { reason?: string; sessionID?: string | null };
  skills?: CompoundSpecV1["skills"];
  docs?: CompoundSpecV1["docs"];
  memos?: CompoundSpecV1["memos"];
  changelog?: CompoundSpecV1["changelog"];
  instincts?: {
    create?: InstinctCreateSpec[];
    update?: InstinctUpdateSpec[];
  };
};

type CompoundSpec = CompoundSpecV1 | CompoundSpecV2;

type Observation = Record<string, unknown> & {
  id: string;
  ts: ISODate;
  type: string;
  sessionID?: string | null;
};

// -----------------------------
// Tiny helpers
// -----------------------------

function nowIso(): ISODate {
  return new Date().toISOString();
}

function intEnv(key: string, fallback: number): number {
  const v = process.env[key];
  if (!v) return fallback;
  const n = Number(v);
  return Number.isFinite(n) ? Math.trunc(n) : fallback;
}

function clamp(n: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, n));
}

function normalizeNewlines(s: string): string {
  return s.replace(/\r\n/g, "\n");
}

function rewriteRepoAbsolutePaths(root: string, text: string): string {
  const t = normalizeNewlines(String(text ?? ""));

  const rootAbs = path.resolve(String(root ?? "")).replace(/[\\/]+$/, "");
  if (!rootAbs) return t;

  const rootPosix = rootAbs.replace(/\\/g, "/");
  const rootWin = rootAbs.replace(/\//g, "\\");

  // Only rewrite paths that are clearly within this repo root.
  return t.split(rootPosix + "/").join("").split(rootWin + "\\").join("");
}

function sha256(s: string): string {
  return createHash("sha256").update(s).digest("hex");
}

function safeFilenameComponent(input: string, fallback = "unknown"): string {
  const s = String(input ?? "").trim();
  if (!s) return fallback;
  const cleaned = s.replace(/[^A-Za-z0-9_-]/g, "_").slice(0, 80);
  return cleaned || fallback;
}

async function tuiToast(client: any, message: string, variant: "success" | "error" | "info" = "info") {
  try {
    await client.tui.showToast({ body: { message, variant } });
  } catch {}
}

async function pathExists(p: string): Promise<boolean> {
  try {
    await fs.stat(p);
    return true;
  } catch {
    return false;
  }
}

async function ensureDir(p: string): Promise<void> {
  await fs.mkdir(p, { recursive: true });
}

async function atomicWrite(filePath: string, content: string): Promise<void> {
  const dir = path.dirname(filePath);
  await ensureDir(dir);
  const tmp = `${filePath}.tmp.${randomUUID()}`;
  await fs.writeFile(tmp, content, "utf8");
  await fs.rename(tmp, filePath);
}

async function resolveWriteRoot(sessionRoot: string): Promise<string> {
  const override = String(process.env.COMPOUND_ROOT ?? "").trim();
  if (override) return path.resolve(override);

  // Fallback: infer repo root via git common dir (works in worktrees).
  try {
    const res = await runProcess({ cmd: "git", args: ["rev-parse", "--git-common-dir"] }, sessionRoot, 8000);
    const out = String(res.stdout ?? "").trim();
    if (!out) return sessionRoot;

    const commonDir = path.resolve(sessionRoot, out);
    const commonPosix = commonDir.replace(/\\/g, "/");

    // Normal repo: .../.git
    if (path.basename(commonDir) === ".git") return path.dirname(commonDir);

    // Worktree common dir: .../.git/worktrees/<name>
    const m = commonPosix.match(/^(.*)\/\.git(?:\/|$)/);
    if (m && m[1]) return m[1];
  } catch {}

  return sessionRoot;
}

// -----------------------------
// Managed blocks
// -----------------------------

function blockMarkers(id: string): { begin: string; end: string } {
  return {
    begin: `<!-- BEGIN:compound:${id} -->`,
    end: `<!-- END:compound:${id} -->`,
  };
}

function managedBlock(begin: string, end: string, inner: string): string {
  const body = normalizeNewlines(inner).trimEnd();
  return `${begin}\n${body}\n${end}`;
}

function upsertManagedBlock(doc: string, id: string, inner: string): string {
  const markers = blockMarkers(id);
  const begin = markers.begin;
  const end = markers.end;

  const block = managedBlock(begin, end, inner);

  const b = doc.indexOf(begin);
  const e = doc.indexOf(end);

  if (b !== -1 && e !== -1 && e > b) {
    const before = doc.slice(0, b);
    const after = doc.slice(e + end.length);
    return (before + block + after).trimEnd() + "\n";
  }

  // Missing: append at end with spacing.
  const trimmed = doc.trimEnd();
  return `${trimmed}\n\n${block}\n`;
}

function removeManagedBlock(doc: string, id: string): string {
  const markers = blockMarkers(id);
  const b = doc.indexOf(markers.begin);
  const e = doc.indexOf(markers.end);
  if (b === -1 || e === -1 || e <= b) return doc;

  const before = doc.slice(0, b).trimEnd();
  const after = doc.slice(e + markers.end.length).trimStart();
  const joined = before && after ? `${before}\n\n${after}` : before || after;
  return joined.trimEnd() + "\n";
}

function readManagedBlockInner(doc: string, id: string): string {
  const markers = blockMarkers(id);
  const b = doc.indexOf(markers.begin);
  const e = doc.indexOf(markers.end);
  if (b === -1 || e === -1 || e <= b) return "";
  return doc.slice(b + markers.begin.length, e).trim();
}

function isPlaceholderBlock(inner: string): boolean {
  const t = normalizeNewlines(String(inner ?? "")).trim();
  if (!t) return true;
  if (t === "(autogenerated)") return true;
  if (/^\(auto\-generated\)$/i.test(t)) return true;
  if (/^\-\s*_\(none/i.test(t)) return true;
  return false;
}

function upsertManagedBlockPreservingNonPlaceholder(doc: string, id: string, inner: string): string {
  const existing = readManagedBlockInner(doc, id);
  if (existing && !isPlaceholderBlock(existing)) return doc;
  return upsertManagedBlock(doc, id, inner);
}

// -----------------------------
// Bootstrap / skeleton docs
// -----------------------------

function agentsSkeleton(): string {
  return normalizeNewlines(`# AGENTS

This file is included in the agent’s context. It should be committed.

The plugin maintains some **AI-managed blocks** below. Anything outside those blocks is yours.

## Workflow

Use the commands in \`.opencode/commands\`:

- \`/workflows:plan\` → tickets + plan
- \`/workflows:work\` → implement in a worktree
- \`/workflows:review\` → review and adjust tickets
- \`/workflows:compound\` → extract learnings into skills + memos + docs

## AI-managed blocks

${blockMarkers("agents-ai-behavior").begin}
(autogenerated)
${blockMarkers("agents-ai-behavior").end}

 ${blockMarkers("workflow-commands").begin}
(autogenerated)
 ${blockMarkers("workflow-commands").end}

 ${blockMarkers("loom-core-context").begin}
(autogenerated)
 ${blockMarkers("loom-core-context").end}

 ${blockMarkers("instincts-index").begin}
(autogenerated)
 ${blockMarkers("instincts-index").end}

${blockMarkers("rules-index").begin}
(autogenerated)
${blockMarkers("rules-index").end}
`);
}

function roadmapSkeleton(): string {
  return normalizeNewlines(`# LOOM_ROADMAP

High-level direction and priorities.

This is an evolving, empirical compass. Keep it short and stable.

 ${blockMarkers("roadmap-backlog").begin}
(autogenerated)
 ${blockMarkers("roadmap-backlog").end}

${blockMarkers("roadmap-ai-notes").begin}
(autogenerated)
${blockMarkers("roadmap-ai-notes").end}

## Changelog (AI-first)

This log is optimized for *agents*, not humans.
It tracks changes to skills, instincts, and core context files.

It is intentionally bounded. Do not write entries like "no changes".

 ${blockMarkers("changelog-entries").begin}
(autogenerated)
 ${blockMarkers("changelog-entries").end}
`);
}

async function ensureBootstrap(root: string): Promise<void> {
  await ensureDir(path.join(root, ".opencode", "commands"));
  await ensureDir(path.join(root, ".opencode", "plugins"));
  await ensureDir(path.join(root, SKILLS_DIR));
  await ensureDir(path.join(root, COMPOUND_DIR));
  await ensureDir(path.join(root, PROMPTS_DIR));
  await ensureDir(path.join(root, MEMORY_DIR));

  // Default prompt template
  const promptExists = await pathExists(path.join(root, AUTOLEARN_PROMPT_FILE));
  if (!promptExists) {
    await atomicWrite(path.join(root, AUTOLEARN_PROMPT_FILE), defaultAutolearnPrompt());
  }

  // Docs skeletons
  const agentsPath = path.join(root, "AGENTS.md");
  if (!(await pathExists(agentsPath))) await atomicWrite(agentsPath, agentsSkeleton());

  const roadmapPath = path.join(root, "LOOM_ROADMAP.md");
  if (!(await pathExists(roadmapPath))) await atomicWrite(roadmapPath, roadmapSkeleton());

  // Instinct store scaffold
  const instinctsPath = path.join(root, INSTINCTS_FILE);
  if (!(await pathExists(instinctsPath))) {
    const init: InstinctStore = { version: 1, instincts: [] };
    await atomicWrite(instinctsPath, JSON.stringify(init, null, 2) + "\n");
  }

  // Instincts markdown (AI-managed)
  const instinctsMdPath = path.join(root, INSTINCTS_MD);
  if (!(await pathExists(instinctsMdPath))) {
    await atomicWrite(
      instinctsMdPath,
      normalizeNewlines(`# INSTINCTS

This is the *fast index* of the current instinct set.
The source of truth is \`${INSTINCTS_FILE}\`.

${blockMarkers("instincts-md").begin}
(autogenerated)
${blockMarkers("instincts-md").end}
`)
    );
  }

  // Local state file (intentionally not precious)
  const statePath = path.join(root, STATE_FILE);
  if (!(await pathExists(statePath))) {
    const init: PluginState = { version: 2 };
    await atomicWrite(statePath, JSON.stringify(init, null, 2) + "\n");
  }

  // Gitignore for noisy, potentially sensitive runtime artifacts
  const memIgnore = path.join(root, MEMORY_DIR, ".gitignore");
  const memStatus = await _ensure_lines_in_file({
    dest: memIgnore,
    requiredLines: ["observations.jsonl", "observations.jsonl.*.bak", "autolearn_failures/"],
  });
  void memStatus;

  const compoundIgnore = path.join(root, COMPOUND_DIR, ".gitignore");
  const compStatus = await _ensure_lines_in_file({
    dest: compoundIgnore,
    requiredLines: ["state.json", "*.tmp.*"],
  });
  void compStatus;
}

async function _ensure_lines_in_file(opts: { dest: string; requiredLines: string[] }): Promise<"wrote" | "skipped"> {
  const dest = opts.dest;
  const required = opts.requiredLines.map((l) => String(l).trim()).filter(Boolean);
  let existing = "";
  try {
    existing = await fs.readFile(dest, "utf8");
  } catch {
    existing = "";
  }

  const existingLines = new Set(normalizeNewlines(existing).split("\n").map((l) => l.trim()).filter(Boolean));
  const missing = required.filter((l) => !existingLines.has(l));
  if (!missing.length && existing) return "skipped";
  if (!missing.length && !existing) {
    await atomicWrite(dest, required.join("\n") + "\n");
    return "wrote";
  }
  const next = (existing ? existing.trimEnd() + "\n" : "") + missing.join("\n") + "\n";
  await atomicWrite(dest, next);
  return "wrote";
}

function extractSessionID(resp: any): string {
  const r = resp?.data ?? resp;
  const id = r?.id ?? r?.data?.id ?? r?.session?.id ?? r?.data?.session?.id;
  return typeof id === "string" ? id : "";
}

async function forkEphemeralSession(client: any, activeSessionID: string): Promise<string> {
  if (!activeSessionID) return "";

  // Prefer a fork, since it preserves message history.
  try {
    const forkFn = client?.session?.fork;
    if (typeof forkFn === "function") {
      const resp = await forkFn({ path: { id: activeSessionID }, body: {} });
      const id = extractSessionID(resp);
      if (id) return id;
    }
  } catch {}

  // Fallback: create a child session (may not inherit full message history, but avoids polluting the active chat).
  try {
    const resp = await client.session.create({ body: { parentID: activeSessionID, title: "compound-autolearn" } });
    const id = extractSessionID(resp);
    if (id) return id;
  } catch {}

  return "";
}

// -----------------------------
// State
// -----------------------------

async function loadState(root: string): Promise<PluginState> {
  try {
    const raw = await fs.readFile(path.join(root, STATE_FILE), "utf8");
    const parsed = JSON.parse(raw) as PluginState;
    if (parsed?.version === 2) return parsed;
  } catch {}
  return { version: 2 };
}

async function saveState(root: string, state: PluginState): Promise<void> {
  await atomicWrite(path.join(root, STATE_FILE), JSON.stringify(state, null, 2) + "\n");
}

// -----------------------------
// Observations
// -----------------------------

const SECRET_KEY_RE = /(pass(word)?|secret|token|api[_-]?key|auth(orization)?|cookie|session|private[_-]?key)/i;
const SECRET_VALUE_RE = [
  /\bghp_[A-Za-z0-9]{20,}\b/g, // GitHub classic
  /\bgithub_pat_[A-Za-z0-9_]{20,}\b/g, // GitHub fine-grained
  /\bsk-[A-Za-z0-9]{16,}\b/g, // common API key prefix
  /\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b/g, // JWT
  /(Authorization\s*:\s*Bearer)\s+[^\s"']+/gi,
  /(Bearer)\s+[^\s"']+/gi,
  /-----BEGIN[\s\S]{0,2000}?-----END[^-]*-----/g,
];

function scrubString(s: string): string {
  let out = String(s ?? "");
  for (const re of SECRET_VALUE_RE) {
    out = out.replace(re, (m, p1) => (p1 ? `${p1} [REDACTED]` : "[REDACTED]"));
  }
  return out;
}

function sanitizeObservationArgs(toolName: string, args: any): any {
  if (!args || typeof args !== "object") return args;

  // For shell-like tools, never persist the raw command.
  if (/bash|shell/i.test(toolName)) {
    const cmd = typeof (args as any)?.command === "string" ? String((args as any).command) : "";
    return {
      redacted: true,
      command_len: cmd.length,
      command_sha256: cmd ? sha256(cmd) : "",
    };
  }

  const cloned: any = Array.isArray(args) ? [...args] : { ...args };

  const dropTextField = (k: string) => {
    if (!(k in cloned)) return;
    const v = cloned[k];
    if (typeof v === "string") {
      cloned[`${k}_len`] = v.length;
      cloned[`${k}_sha256`] = sha256(v);
      cloned[k] = "[REDACTED]";
      return;
    }
    if (v && typeof v === "object") {
      const raw = JSON.stringify(v);
      cloned[`${k}_len`] = raw.length;
      cloned[`${k}_sha256`] = sha256(raw);
      cloned[k] = "[REDACTED]";
    }
  };

  if (/write|edit/i.test(toolName)) {
    ["content", "new_content", "old_content", "patch", "text"].forEach(dropTextField);
  }

  const scrub = (v: any, key: string, depth: number): any => {
    if (depth > 4) return "{…}";
    if (SECRET_KEY_RE.test(key)) return "[REDACTED]";
    if (typeof v === "string") return scrubString(v);
    if (Array.isArray(v)) {
      return v.slice(0, 50).map((x) => scrub(x, key, depth + 1));
    }
    if (v && typeof v === "object") {
      const out: any = {};
      for (const [k, vv] of Object.entries(v)) {
        if (SECRET_KEY_RE.test(k)) {
          out[k] = "[REDACTED]";
        } else {
          out[k] = scrub(vv, k, depth + 1);
        }
      }
      return out;
    }
    return v;
  };

  return scrub(cloned, "args", 0);
}

async function appendObservation(root: string, obs: Observation): Promise<void> {
  if (!LOG_OBSERVATIONS) return;

  const filePath = path.join(root, OBSERVATIONS_FILE);
  await ensureDir(path.dirname(filePath));

  // Soft-rotate if huge.
  try {
    const st = await fs.stat(filePath);
    if (st.size > OBS_MAX_BYTES) {
      const rotated = `${filePath}.${Date.now()}.bak`;
      await fs.rename(filePath, rotated);
    }
  } catch {}

  await fs.appendFile(filePath, JSON.stringify(obs) + "\n", "utf8");
}

async function readObservationsTail(root: string, maxLines: number): Promise<Observation[]> {
  const filePath = path.join(root, OBSERVATIONS_FILE);
  if (!(await pathExists(filePath))) return [];
  const raw = await fs.readFile(filePath, "utf8");
  const lines = raw.trimEnd().split("\n");
  const slice = lines.slice(Math.max(0, lines.length - maxLines));
  const out: Observation[] = [];
  for (const line of slice) {
    try {
      out.push(JSON.parse(line));
    } catch {}
  }
  return out;
}

async function countObservations(root: string): Promise<{ count: number; tailHash: string }> {
  const filePath = path.join(root, OBSERVATIONS_FILE);
  if (!(await pathExists(filePath))) return { count: 0, tailHash: "" };
  const raw = await fs.readFile(filePath, "utf8");
  const lines = raw.trimEnd().split("\n");
  const tail = lines.slice(Math.max(0, lines.length - 200)).join("\n");
  return { count: lines.filter(Boolean).length, tailHash: sha256(tail) };
}

// -----------------------------
// Instincts
// -----------------------------

function validateKebab(name: string, label: string): void {
  if (!name || typeof name !== "string") throw new Error(`${label} must be a string`);
  if (name.length < 1 || name.length > 64) throw new Error(`${label} must be 1-64 chars`);
  if (!SKILL_NAME_RE.test(name)) throw new Error(`${label} must match ${SKILL_NAME_RE.toString()}`);
}

async function loadInstincts(root: string): Promise<InstinctStore> {
  const filePath = path.join(root, INSTINCTS_FILE);
  try {
    const raw = await fs.readFile(filePath, "utf8");
    const parsed = JSON.parse(raw) as InstinctStore;
    if (parsed?.version === 1 && Array.isArray(parsed.instincts)) return parsed;
  } catch {}
  return { version: 1, instincts: [] };
}

async function saveInstincts(root: string, store: InstinctStore): Promise<void> {
  await atomicWrite(path.join(root, INSTINCTS_FILE), JSON.stringify(store, null, 2) + "\n");
  await syncInstinctsMarkdown(root, store);
}

function renderInstinctsIndex(instincts: Instinct[], max = 25): string {
  const active = instincts
    .filter((i) => i.status === "active")
    .sort((a: any, b: any) => (b.confidence ?? 0) - (a.confidence ?? 0))
    .slice(0, max);

  if (!active.length) return "- _(none yet)_";

  return active
    .map((i) => {
      const tags = i.tags?.length ? ` [${i.tags.join(", ")}]` : "";
      const skill = i.skill ? ` → skill: \`${i.skill}\`` : "";
      return `- **${i.id}** (${Math.round(i.confidence * 100)}%)${tags}${skill}\n  - Trigger: ${oneLine(i.trigger)}\n  - Action: ${oneLine(i.action)}`;
    })
    .join("\n");
}

function oneLine(s: string, max = 200): string {
  const t = normalizeNewlines(String(s ?? "")).replace(/\s+/g, " ").trim();
  return t.length > max ? t.slice(0, max) + "…" : t;
}

async function syncInstinctsMarkdown(root: string, store: InstinctStore): Promise<void> {
  const mdPath = path.join(root, INSTINCTS_MD);
  let md = "";
  try {
    md = await fs.readFile(mdPath, "utf8");
  } catch {
    md = normalizeNewlines(`# INSTINCTS

${blockMarkers("instincts-md").begin}
(autogenerated)
${blockMarkers("instincts-md").end}
`);
  }

  const inner = [
    "## Active instincts (top confidence)",
    "",
    renderInstinctsIndex(store.instincts, 40),
    "",
    "## Notes",
    "",
    "- Instincts are the *pre-skill* layer: small, repeatable heuristics.",
    "- When an instinct proves useful across sessions, promote it into a Skill.",
  ].join("\n");

  md = upsertManagedBlock(md, "instincts-md", inner);
  await atomicWrite(mdPath, md);
}

function applyInstinctChanges(store: InstinctStore, changes?: CompoundSpecV2["instincts"], sessionID?: string | null): { created: number; updated: number } {
  let created = 0;
  let updated = 0;
  if (!changes) return { created, updated };

  const byId = new Map(store.instincts.map((i) => [i.id, i]));

  for (const c of changes.create ?? []) {
    validateKebab(c.id, "instinct.id");
    const existing = byId.get(c.id);
    if (existing) continue;

    const ts = nowIso();
    const inst: Instinct = {
      id: c.id,
      title: c.title?.trim() || c.id,
      trigger: c.trigger?.trim() || "",
      action: c.action?.trim() || "",
      tags: c.tags ?? [],
      confidence: clamp(c.confidence ?? 0.5, 0, 1),
      status: "active",
      skill: c.skill,
      notes: c.notes ?? undefined,
      created_at: ts,
      updated_at: ts,
      evidence: [{ ts, sessionID: sessionID ?? null, note: c.evidence_note }],
    };
    store.instincts.push(inst);
    byId.set(inst.id, inst);
    created++;
  }

  for (const u of changes.update ?? []) {
    validateKebab(u.id, "instinct.id");
    const inst = byId.get(u.id);
    if (!inst) continue;

    if (typeof u.title === "string") inst.title = u.title;
    if (typeof u.trigger === "string") inst.trigger = u.trigger;
    if (typeof u.action === "string") inst.action = u.action;
    if (Array.isArray(u.tags)) inst.tags = u.tags;
    if (typeof u.status === "string") inst.status = u.status;
    if ("skill" in u) inst.skill = u.skill ?? undefined;
    if ("notes" in u) inst.notes = u.notes ?? undefined;

    if (typeof u.confidence_delta === "number") {
      inst.confidence = clamp((inst.confidence ?? 0.5) + u.confidence_delta, 0, 1);
    }
    if (typeof u.confidence === "number") {
      inst.confidence = clamp(u.confidence, 0, 1);
    }

    if (u.evidence_note) {
      inst.evidence.push({ ts: nowIso(), sessionID: sessionID ?? null, note: u.evidence_note });
    }

    inst.updated_at = nowIso();
    updated++;
  }

  return { created, updated };
}

// -----------------------------
// Skills
// -----------------------------

function nonEmptyLineCount(s: string): number {
  return normalizeNewlines(s)
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean).length;
}

function looksLikeDiffOrPatch(s: string): boolean {
  const t = normalizeNewlines(s);
  if (/^```diff\b/m.test(t)) return true;
  if (/^\+\+\+\s+\S+/m.test(t) && /^---\s+\S+/m.test(t)) return true;
  if (/^@@\s+[-+0-9, ]+\s+@@/m.test(t)) return true;
  return false;
}

function looksLikePartialSkillBodyUpdate(existingBody: string, nextBody: string): boolean {
  const oldBody = normalizeNewlines(existingBody).trim();
  const newBody = normalizeNewlines(nextBody).trim();
  if (!oldBody) return false;
  if (!newBody) return true;

  if (looksLikeDiffOrPatch(newBody)) return true;

  // Heuristic guardrail: block obvious "snippet" updates that would truncate the managed body.
  const oldLen = oldBody.length;
  const newLen = newBody.length;
  const oldLines = nonEmptyLineCount(oldBody);
  const newLines = nonEmptyLineCount(newBody);
  if (oldLen > 250 && newLen < 250) return true;
  if (oldLines >= 12 && newLines < 8) return true;
  if (newLen < oldLen * 0.3 && newLines < 20) return true;

  return false;
}

type ParsedFrontmatter = {
  name?: string;
  description?: string;
  license?: string;
  compatibility?: string;
  metadata?: Record<string, string>;
};

function parseFrontmatter(md: string): { fm: ParsedFrontmatter; body: string; manualNotes: string } {
  const text = normalizeNewlines(md);
  if (!text.startsWith("---\n")) {
    return { fm: {}, body: text.trim(), manualNotes: "" };
  }
  const end = text.indexOf("\n---\n", 4);
  if (end === -1) return { fm: {}, body: text.trim(), manualNotes: "" };

  const fmRaw = text.slice(4, end).trim();
  const rest = text.slice(end + "\n---\n".length);

  // Extremely small YAML parser (just what we need).
  const fm: ParsedFrontmatter = {};
  let inMetadata = false;
  const metadata: Record<string, string> = {};

  for (const line of fmRaw.split("\n")) {
    const l = line.trimEnd();
    if (!l.trim()) continue;
    if (/^\s*metadata\s*:\s*$/.test(l)) {
      inMetadata = true;
      continue;
    }
    if (inMetadata) {
      const m = l.match(/^\s+([a-zA-Z0-9_\-]+)\s*:\s*"?(.+?)"?\s*$/);
      if (m) metadata[m[1]] = m[2].replace(/\\"/g, '"');
      continue;
    }
    const m = l.match(/^([a-zA-Z0-9_\-]+)\s*:\s*(.+)\s*$/);
    if (!m) continue;
    const key = m[1];
    const val = m[2].trim().replace(/^"(.+)"$/, "$1");
    if (key === "name") fm.name = val;
    if (key === "description") fm.description = val;
    if (key === "license") fm.license = val;
    if (key === "compatibility") fm.compatibility = val;
  }

  fm.metadata = Object.keys(metadata).length ? metadata : undefined;

  // Body is the managed block content; manual notes is whatever after it.
  const markers = blockMarkers("skill-managed");
  const b = rest.indexOf(markers.begin);
  const e = rest.indexOf(markers.end);
  let body = rest.trim();
  let manualNotes = "";
  if (b !== -1 && e !== -1 && e > b) {
    body = rest.slice(b + markers.begin.length, e).trim();
    manualNotes = rest.slice(e + markers.end.length).trim();
  } else {
    // Back-compat: older skills may not have managed markers, but do have a "## Manual notes" section.
    const re = /(^|\n)##\s+manual\s+notes\b/i;
    const m = re.exec(rest);
    if (m && typeof m.index === "number") {
      let idx = m.index;
      if (rest[idx] === "\n") idx += 1; // start at the heading, not the preceding newline
      body = rest.slice(0, idx).trim();
      manualNotes = rest.slice(idx).trim();
    }
  }
  return { fm, body, manualNotes };
}

function buildSkillMarkdown(opts: {
  name: string;
  description: string;
  body: string;
  license?: string;
  compatibility?: string;
  metadata?: Record<string, string>;
  version: number;
  createdAt?: ISODate;
  updatedAt?: ISODate;
  tags?: string[];
  manualNotes?: string | null;
}): string {
  const license = opts.license ?? "MIT";
  const compatibility = opts.compatibility ?? "opencode,claude";
  const createdAt = opts.createdAt ?? nowIso();
  const updatedAt = opts.updatedAt ?? nowIso();

  const metadata: Record<string, string> = {
    created_at: createdAt,
    updated_at: updatedAt,
    version: String(opts.version),
    ...(opts.tags && opts.tags.length ? { tags: opts.tags.join(",") } : {}),
    ...(opts.metadata ?? {}),
  };

  const fmLines = [
    "---",
    `name: ${opts.name}`,
    `description: ${opts.description}`,
    `license: ${license}`,
    `compatibility: ${compatibility}`,
    "metadata:",
    ...Object.entries(metadata).map(([k, v]) => `  ${k}: "${String(v).replace(/"/g, '\\"')}"`),
    "---",
    "",
  ].join("\n");

  const markers = blockMarkers("skill-managed");
  const managed = managedBlock(markers.begin, markers.end, opts.body.trim());

  const placeholder = [
    "## Manual notes",
    "",
    "_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._",
    "",
  ].join("\n");

  const tail = opts.manualNotes && opts.manualNotes.trim().length ? normalizeNewlines(opts.manualNotes).trimEnd() + "\n" : placeholder;

  return fmLines + managed + "\n\n" + tail;
}

async function scanSkills(
  root: string
): Promise<Array<{ name: string; description: string; path: string; version?: string; managedBody?: string }>> {
  const dir = path.join(root, SKILLS_DIR);
  if (!(await pathExists(dir))) return [];
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const out: Array<{ name: string; description: string; path: string; version?: string; managedBody?: string }> = [];

  for (const ent of entries) {
    if (!ent.isDirectory()) continue;
    const name = ent.name;
    const skillPathAbs = path.join(dir, name, "SKILL.md");
    if (!(await pathExists(skillPathAbs))) continue;
    try {
      const raw = await fs.readFile(skillPathAbs, "utf8");
      const { fm, body } = parseFrontmatter(raw);
      if (!fm.name || !fm.description) continue;
      const rel = path.relative(root, skillPathAbs).replace(/\\/g, "/");
      out.push({ name: fm.name, description: fm.description, path: rel, version: fm.metadata?.version, managedBody: body });
    } catch {}
  }
  return out.sort((a: any, b: any) => a.name.localeCompare(b.name));
}

async function syncClaudeSkillsMirror(root: string): Promise<{ synced: number }> {
  if (!MIRROR_CLAUDE) return { synced: 0 };

  const skills = await scanSkills(root);
  let synced = 0;
  for (const s of skills) {
    const srcPath = path.join(root, s.path);
    const dstPath = path.join(root, CLAUDE_SKILLS_DIR, s.name, "SKILL.md");
    const raw = await safeReadFile(srcPath, "");
    if (!raw) continue;

    const existing = await safeReadFile(dstPath, "");
    if (existing === raw) continue;

    await ensureDir(path.dirname(dstPath));
    await atomicWrite(dstPath, raw);
    synced += 1;
  }
  return { synced };
}

async function writeOrUpdateSkill(root: string, input: SkillSpec | (SkillUpdateSpec & { description: string })): Promise<{ action: "created" | "updated"; path: string }> {
  validateKebab(input.name, "skill.name");
  if (!input.description?.trim()) throw new Error("skill.description required");
  const sanitizedBody = rewriteRepoAbsolutePaths(root, input.body);
  if (!sanitizedBody?.trim()) throw new Error("skill.body required");

  const skillDir = path.join(root, SKILLS_DIR, input.name);
  const skillPath = path.join(skillDir, "SKILL.md");

  const exists = await pathExists(skillPath);
  let nextVersion = 1;
  let createdAt = nowIso();
  let manualNotes: string | null = null;
  let existingFm: ParsedFrontmatter = {};
  let existingBody: string | null = null;

  if (exists) {
    const raw = await fs.readFile(skillPath, "utf8");
    const parsed = parseFrontmatter(raw);
    existingFm = parsed.fm;
    existingBody = parsed.body;
    const curV = Number(parsed.fm.metadata?.version ?? "1");
    nextVersion = Number.isFinite(curV) ? curV + 1 : 2;
    createdAt = parsed.fm.metadata?.created_at ?? createdAt;
    manualNotes = parsed.manualNotes;
  }

  if (exists && existingBody && looksLikePartialSkillBodyUpdate(existingBody, sanitizedBody)) {
    throw new Error(
      "skill.update.body must be the full managed body (complete replacement), not a snippet/diff. Re-emit the entire managed body with your edits applied."
    );
  }

  const tags = input.tags ?? (existingFm.metadata?.tags ? existingFm.metadata.tags.split(",").map((t) => t.trim()).filter(Boolean) : undefined);
  const mergedMeta = { ...(existingFm.metadata ?? {}), ...(input.metadata ?? {}) };

  const md = buildSkillMarkdown({
    name: input.name,
    description: input.description.trim(),
    body: sanitizedBody.trim(),
    license: input.license ?? existingFm.license,
    compatibility: input.compatibility ?? existingFm.compatibility,
    version: nextVersion,
    createdAt,
    updatedAt: nowIso(),
    tags,
    metadata: mergedMeta,
    manualNotes,
  });

  await ensureDir(skillDir);
  await atomicWrite(skillPath, md);

  if (MIRROR_CLAUDE) {
    const claudeDir = path.join(root, CLAUDE_SKILLS_DIR, input.name);
    const claudePath = path.join(claudeDir, "SKILL.md");
    await ensureDir(claudeDir);
    await atomicWrite(claudePath, md);
  }

  return { action: exists ? "updated" : "created", path: skillPath };
}

async function deprecateSkill(root: string, name: string, reason: string, replacement?: string): Promise<void> {
  validateKebab(name, "skill.name");
  const skillPath = path.join(root, SKILLS_DIR, name, "SKILL.md");
  if (!(await pathExists(skillPath))) return;

  const raw = await fs.readFile(skillPath, "utf8");
  const parsed = parseFrontmatter(raw);
  const body = parsed.body;

  const deprecation = [
    "> **Deprecated**",
    `> Reason: ${oneLine(reason, 400)}`,
    ...(replacement ? [`> Replacement: \`${replacement}\``] : []),
    "",
  ].join("\n");

  const newBody = deprecation + body;
  await writeOrUpdateSkill(root, {
    name,
    description: parsed.fm.description ?? `Deprecated skill: ${name}`,
    body: newBody,
    license: parsed.fm.license,
    compatibility: parsed.fm.compatibility,
    metadata: parsed.fm.metadata,
  });
}

// -----------------------------
// CLI runner (loom + subsystem aliases)
// -----------------------------

type CommandSpec = { cmd: string; args: string[] };

async function runProcess(spec: CommandSpec, cwd: string, timeoutMs = 120000): Promise<{ code: number; stdout: string; stderr: string }> {
  return await new Promise((resolve) => {
    const child = spawn(spec.cmd, spec.args, { cwd, env: process.env });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (d: any) => (stdout += d.toString()));
    child.stderr.on("data", (d: any) => (stderr += d.toString()));

    const t = setTimeout(() => {
      try {
        child.kill("SIGKILL");
      } catch {}
      resolve({ code: 124, stdout, stderr: stderr + "\n(timeout)" });
    }, timeoutMs);

    child.on("close", (code: any) => {
      clearTimeout(t);
      resolve({ code: code ?? 1, stdout, stderr });
    });
  });
}

async function resolveLoomRoot(root: string): Promise<CommandSpec> {
  const candidates = [DEFAULT_LOOM_BIN, "agent-loom", "loom"];
  for (const c of candidates) {
    const r = await runProcess({ cmd: c, args: ["--help"] }, root, 8000);
    if (r.code === 0) return { cmd: c, args: [] };
  }
  return { cmd: DEFAULT_LOOM_BIN, args: [] };
}

async function resolveTicketCli(root: string): Promise<CommandSpec> {
  const loom = await resolveLoomRoot(root);
  const viaLoom = await runProcess({ cmd: loom.cmd, args: [...loom.args, "ticket", "--help"] }, root, 8000);
  if (viaLoom.code === 0) return { cmd: loom.cmd, args: [...loom.args, "ticket"] };

  const alias = "agent-loom-ticket";
  const viaAlias = await runProcess({ cmd: alias, args: ["--help"] }, root, 8000);
  if (viaAlias.code === 0) return { cmd: alias, args: [] };

  return { cmd: loom.cmd, args: [...loom.args, "ticket"] };
}

async function resolveMemoryCli(root: string): Promise<CommandSpec> {
  const loom = await resolveLoomRoot(root);
  const viaLoom = await runProcess({ cmd: loom.cmd, args: [...loom.args, "memory", "--help"] }, root, 8000);
  if (viaLoom.code === 0) return { cmd: loom.cmd, args: [...loom.args, "memory"] };

  const alias = "agent-loom-memory";
  const viaAlias = await runProcess({ cmd: alias, args: ["--help"] }, root, 8000);
  if (viaAlias.code === 0) return { cmd: alias, args: [] };

  return { cmd: loom.cmd, args: [...loom.args, "memory"] };
}

async function resolveWorkspaceCli(root: string): Promise<CommandSpec> {
  const loom = await resolveLoomRoot(root);
  const viaLoom = await runProcess({ cmd: loom.cmd, args: [...loom.args, "workspace", "--help"] }, root, 8000);
  if (viaLoom.code === 0) return { cmd: loom.cmd, args: [...loom.args, "workspace"] };

  const alias = "agent-loom-workspace";
  const viaAlias = await runProcess({ cmd: alias, args: ["--help"] }, root, 8000);
  if (viaAlias.code === 0) return { cmd: alias, args: [] };

  return { cmd: loom.cmd, args: [...loom.args, "workspace"] };
}

// -----------------------------
// Git summary (used in autolearn prompt and status)
// -----------------------------

async function gitSummary(root: string): Promise<{ ok: boolean; changedFiles: string[]; diffStat: string }> {
  const status = await runProcess({ cmd: "git", args: ["status", "--porcelain"] }, root, 20000);
  if (status.code !== 0) return { ok: false, changedFiles: [], diffStat: "" };

  const changedFiles = status.stdout
    .split("\n")
    .map((l: any) => l.trim())
    .filter(Boolean)
    .map((l: any) => l.slice(3).trim());

  const diffStatRes = await runProcess({ cmd: "git", args: ["diff", "--stat"] }, root, 20000);
  const diffStat = diffStatRes.code === 0 ? diffStatRes.stdout.trim() : "";

  return { ok: true, changedFiles, diffStat };
}

// -----------------------------
// Docs sync
// -----------------------------

async function scanRules(root: string): Promise<Array<{ name: string; path: string }>> {
  const rulesDir = path.join(root, ".opencode", "rules");
  if (!(await pathExists(rulesDir))) return [];
  const entries = await fs.readdir(rulesDir, { withFileTypes: true });
  return entries
    .filter((e: any) => e.isFile() && e.name.toLowerCase().endsWith(".md"))
    .map((e: any) => ({ name: e.name, path: path.join(".opencode", "rules", e.name) }))
    .sort((a: any, b: any) => a.name.localeCompare(b.name));
}

function renderAgentsAiBehavior(): string {
  return normalizeNewlines(`# Compound Engineering Baseline

This block is maintained by the compound plugin.

**Core loop:** Plan → Work → Review → Compound → Repeat.

**Memory model:**
- **Observations** are logged automatically from tool calls and session events.
- **Instincts** are small heuristics extracted from observations.
- **Skills** are durable procedural memory (directory + SKILL.md) and are the primary compounding mechanism.

**Non-negotiables:**
- Keep skills small, specific, and triggerable from the \`description\`.
- Prefer updating an existing skill over creating a near-duplicate.
- Never put secrets into skills, memos, or observations.
- The plugin may auto-create/update skills. Humans should occasionally prune duplicates.

**Where things live:**
- Skills: \`${SKILLS_DIR}/<name>/SKILL.md\`
- Instincts: \`${INSTINCTS_FILE}\` (index at \`${INSTINCTS_MD}\`)
- Observations: \`${OBSERVATIONS_FILE}\` (gitignored by default)

**Core docs:**
- \`AGENTS.md\` (behavior + always-on context)
- \`LOOM_ROADMAP.md\` (direction + backlog + changelog)
`);
}

function renderWorkflowCommands(): string {
  return normalizeNewlines(`- \`/workflows:plan\` - Create tickets + plan (uses memory recall)
- \`/workflows:work\` - Create/manage worktree (workspace) and implement
- \`/workflows:review\` - Review changes and update tickets
- \`/workflows:compound\` - Extract learnings into skills + memory + docs
`);
}

function renderLoomCoreContext(): string {
  return normalizeNewlines(`# Loom always-on context (second-order compression)

This block is intentionally *small and stable*. Only update it when a principle has proven durable.

- First-order: observations → instincts → skills.
- Second-order: compress skills/instincts/patterns into a few fundamentals that are always-on.
- Prefer agent-native primitives: ticket, memory, workspace, team.
- Governance loop: Plan → Work → Review → Compound → Repeat.

@LOOM_ROADMAP.md
`);
}

function renderSkillsIndex(skills: Array<{ name: string; description: string; path: string; version?: string }>): string {
  if (!skills.length) return "- _(none yet)_";
  return skills
    .map((s) => `- **${s.name}**${s.version ? ` (v${s.version})` : ""}: ${s.description}\n  - ${s.path.replace(/\\/g, "/")}`)
    .join("\n");
}

async function renderRoadmapBacklog(root: string): Promise<string> {
  // Best-effort: use loom ticket list. If not available, leave placeholder.
  const ticket = await resolveTicketCli(root);
  const res = await runProcess({ cmd: ticket.cmd, args: [...ticket.args, "list"] }, root, 25000);
  if (res.code !== 0) {
    return "- _(loom ticket not available or repo not initialized)_";
  }
  // Just include raw output; it's already intended as a human-readable backlog.
  const lines = normalizeNewlines(res.stdout).trim().split("\n").slice(0, 60);
  return lines.length ? lines.map((l: any) => `- ${l}`).join("\n") : "- _(no tickets)_";
}

function defaultRoadmapCompass(): string {
  return normalizeNewlines(`## Compass

- Direction: _(fill in)_
- Themes: _(fill in)_
- Next focus (1-3): _(fill in)_
- Guardrails: keep memory changes meaningful; avoid churn; prefer compounding.
`);
}

async function syncDocs(root: string): Promise<void> {
  await ensureBootstrap(root);

  // AGENTS.md
  const agentsPath = path.join(root, "AGENTS.md");
  let agents = await fs.readFile(agentsPath, "utf8");

  // Drop legacy blocks to keep AGENTS small.
  agents = removeManagedBlock(agents, "skills-index");

  const rules = await scanRules(root);
  const instincts = await loadInstincts(root);

  agents = upsertManagedBlock(agents, "agents-ai-behavior", renderAgentsAiBehavior());
  agents = upsertManagedBlock(agents, "workflow-commands", renderWorkflowCommands());
  agents = upsertManagedBlockPreservingNonPlaceholder(agents, "loom-core-context", renderLoomCoreContext());
  agents = upsertManagedBlock(agents, "instincts-index", renderInstinctsIndex(instincts.instincts, 20));
  agents = upsertManagedBlock(
    agents,
    "rules-index",
    rules.length ? rules.map((r) => `- ${r.name}: ${r.path}`).join("\n") : "- _(none)_"
  );
  await atomicWrite(agentsPath, agents);

  // LOOM_ROADMAP.md
  const roadmapPath = path.join(root, "LOOM_ROADMAP.md");
  let roadmap = await fs.readFile(roadmapPath, "utf8");
  roadmap = upsertManagedBlock(roadmap, "roadmap-backlog", await renderRoadmapBacklog(root));
  roadmap = upsertManagedBlockPreservingNonPlaceholder(roadmap, "roadmap-ai-notes", defaultRoadmapCompass());
  await atomicWrite(roadmapPath, roadmap);

  // INSTINCTS.md already kept in sync by saveInstincts(). But make sure it exists and has current content.
  await syncInstinctsMarkdown(root, instincts);
}

// -----------------------------
// Changelog
// -----------------------------

function isTrivialChangelogNote(note: string): boolean {
  const t = oneLine(String(note ?? "").toLowerCase(), 400);
  if (!t) return true;

  const trivial = [
    "no changes",
    "no change",
    "noop",
    "no-op",
    "none",
    "n/a",
    "nothing",
    "(none)",
    "no updates",
    "no significant changes",
  ];
  if (trivial.includes(t)) return true;
  if (/(^|\b)(no changes|no change|no updates|no significant changes)(\b|$)/.test(t)) return true;

  return false;
}

function stripChangelogTimestamp(entryLine: string): string {
  // Example: "- 2026-01-30T12:34:56.000Z skills: foo(created)"
  const l = oneLine(String(entryLine ?? ""), 800);
  return l.replace(/^\-\s+\d{4}-\d{2}-\d{2}T[^\s]+\s+/, "").trim();
}

async function appendChangelog(root: string, line: string): Promise<void> {
  await ensureBootstrap(root);
  const p = path.join(root, "LOOM_ROADMAP.md");
  let doc = await fs.readFile(p, "utf8");

  const markers = blockMarkers("changelog-entries");
  const safeLine = rewriteRepoAbsolutePaths(root, oneLine(line, 400));
  if (isTrivialChangelogNote(safeLine)) return;

  const entry = `- ${nowIso()} ${safeLine}`;

  const b = doc.indexOf(markers.begin);
  const e = doc.indexOf(markers.end);
  if (b !== -1 && e !== -1 && e > b) {
    const inside = doc.slice(b + markers.begin.length, e).trim();
    const lines = inside ? inside.split("\n").filter(Boolean) : [];

    // Dedupe against the recent window (ignore timestamps).
    const newSig = stripChangelogTimestamp(entry).toLowerCase();
    const recentSigs = lines
      .slice(0, CHANGELOG_DEDUPE_WINDOW)
      .map((l: any) => stripChangelogTimestamp(l).toLowerCase())
      .filter(Boolean);
    if (recentSigs.includes(newSig)) return;

    lines.unshift(entry);
    const inner = lines.slice(0, CHANGELOG_MAX_ENTRIES).join("\n");
    doc = upsertManagedBlock(doc, "changelog-entries", inner);
  } else {
    doc = upsertManagedBlock(doc, "changelog-entries", entry);
  }

  await atomicWrite(p, doc);
}

// -----------------------------
// Apply CompoundSpec
// -----------------------------

function coerceSpec(obj: any): CompoundSpec {
  if (!obj || typeof obj !== "object") throw new Error("spec must be an object");
  const v = obj.schema_version ?? 1;
  if (v !== 1 && v !== 2) throw new Error("unsupported schema_version");
  obj.schema_version = v;
  return obj as CompoundSpec;
}

async function applySpec(root: string, spec: CompoundSpec, mode: "auto" | "manual" = "manual"): Promise<{ skills: Array<{ name: string; action: string }>; instincts: { created: number; updated: number } }> {
  await ensureBootstrap(root);

  const results: Array<{ name: string; action: string }> = [];
  const autoSessionID =
    spec.schema_version === 2 ? (spec as CompoundSpecV2).auto?.sessionID ?? null : null;
  const skillLimit = mode === "auto" ? AUTO_MAX_SKILLS_PER_RUN : Number.MAX_SAFE_INTEGER;
  const memoLimit = mode === "auto" ? 6 : Number.MAX_SAFE_INTEGER;
  const instinctLimit = mode === "auto" ? AUTO_MAX_INSTINCT_UPDATES_PER_RUN : Number.MAX_SAFE_INTEGER;

  const docBlockLimit = mode === "auto" ? 3 : Number.MAX_SAFE_INTEGER;
  let docBlocksApplied = 0;
  let memosAttempted = 0;

  const allowedDocBlocks: Record<string, Set<string>> = {
    "AGENTS.md": new Set(["loom-core-context"]),
    "LOOM_ROADMAP.md": new Set(["roadmap-ai-notes"]),
  };

  const applyDocBlockUpsert = async (u: DocBlockUpsertSpec): Promise<void> => {
    const file = String(u?.file ?? "").trim().replace(/\\/g, "/");
    const id = String(u?.id ?? "").trim();
    let content = normalizeNewlines(String(u?.content ?? "")).trim();
    if (!file || !id || !content) return;

    if (content.length > DOC_BLOCK_MAX_CHARS) {
      content = content.slice(0, DOC_BLOCK_MAX_CHARS).trimEnd() + "\n";
    }
    content = rewriteRepoAbsolutePaths(root, content);

    if (file.startsWith("/") || file.includes("..")) {
      throw new Error(`doc.blocks.upsert.file must be repo-relative (got: ${file})`);
    }
    if (!(file in allowedDocBlocks) || !allowedDocBlocks[file]?.has(id)) {
      throw new Error(`doc.blocks.upsert target not allowed: ${file}#${id}`);
    }

    const abs = path.resolve(root, file);
    const rel = path.relative(root, abs);
    if (!rel || rel.startsWith("..") || path.isAbsolute(rel)) {
      throw new Error(`doc.blocks.upsert.file escapes repo root: ${file}`);
    }

    const existing = await safeReadFile(abs, "");
    const updated = upsertManagedBlock(existing || "", id, content);
    if (updated !== existing) {
      await atomicWrite(abs, updated);
      docBlocksApplied += 1;
    }
  };

  // Skills
  if (spec.skills?.create) {
    for (const s of spec.skills.create.slice(0, skillLimit)) {
      try {
        const r = await writeOrUpdateSkill(root, s);
        results.push({ name: s.name, action: r.action });
      } catch (e) {
        if (mode !== "auto") throw e;
        const msg = e instanceof Error ? `${e.name}: ${e.message}` : String(e);
        await recordAutolearnFailure(root, autoSessionID, `skill.create failed (${s.name}): ${msg}`);
      }
    }
  }
  if (spec.skills?.update) {
    for (const u of spec.skills.update.slice(0, skillLimit)) {
      // Need existing description if not provided
      const skillPath = path.join(root, SKILLS_DIR, u.name, "SKILL.md");
      let description = u.description;
      if (!description && (await pathExists(skillPath))) {
        const raw = await fs.readFile(skillPath, "utf8");
        const parsed = parseFrontmatter(raw);
        description = parsed.fm.description ?? `Skill: ${u.name}`;
      }
      if (!description) description = `Skill: ${u.name}`;
      try {
        const r = await writeOrUpdateSkill(root, { ...u, description });
        results.push({ name: u.name, action: r.action });
      } catch (e) {
        if (mode !== "auto") throw e;
        const msg = e instanceof Error ? `${e.name}: ${e.message}` : String(e);
        await recordAutolearnFailure(root, autoSessionID, `skill.update failed (${u.name}): ${msg}`);
      }
    }
  }
  if (spec.skills?.deprecate) {
    for (const d of spec.skills.deprecate) {
      await deprecateSkill(root, d.name, d.reason, d.replacement);
      results.push({ name: d.name, action: "deprecated" });
    }
  }

  // Instincts (v2 only)
  let instinctDelta = { created: 0, updated: 0 };
  if (spec.schema_version === 2) {
    const store = await loadInstincts(root);
    const rawChanges = (spec as CompoundSpecV2).instincts;
    const limitedChanges = rawChanges
      ? {
          create: rawChanges.create?.slice(0, instinctLimit),
          update: rawChanges.update?.slice(0, instinctLimit),
        }
      : undefined;
    instinctDelta = applyInstinctChanges(store, limitedChanges, (spec as CompoundSpecV2).auto?.sessionID ?? null);
    if (instinctDelta.created || instinctDelta.updated) {
      await saveInstincts(root, store);
    }
  }

  // Memory notes (optional, best-effort)
  if (spec.memos?.add?.length) {
    const mem = await resolveMemoryCli(root);
    for (const m of spec.memos.add.slice(0, memoLimit)) {
      // loom memory add --title ... --body ... --tag ... --scope ...
      const args = [...mem.args, "add", "--title", m.title, "--body", m.body];

      for (const t of m.tags ?? []) {
        if (String(t).trim()) args.push("--tag", String(t).trim());
      }

      for (const s of m.scopes ?? []) {
        if (String(s).trim()) args.push("--scope", String(s).trim());
      }

      if (m.command) args.push("--scope", `command:${m.command}`);
      if (m.ticket) {
        const safe = String(m.ticket).replace(/[^A-Za-z0-9_-]/g, "");
        if (safe) args.push("--tag", `ticket_${safe}`);
      }
      if (m.visibility) args.push("--visibility", String(m.visibility));

      await runProcess({ cmd: mem.cmd, args }, root, 30000);
      memosAttempted += 1;
    }
  }

  // Targeted doc block updates (bounded allowlist)
  if (spec.docs?.blocks?.upsert?.length) {
    for (const u of spec.docs.blocks.upsert.slice(0, docBlockLimit)) {
      try {
        await applyDocBlockUpsert(u);
      } catch (e) {
        if (mode !== "auto") throw e;
        const msg = e instanceof Error ? `${e.name}: ${e.message}` : String(e);
        await recordAutolearnFailure(root, autoSessionID, `docs.blocks.upsert failed: ${msg}`);
      }
    }
  }

  // Docs sync
  if (spec.docs?.sync) {
    await syncDocs(root);
  }

  // Changelog note
  const note = spec.changelog?.note;
  const usableNote = note && note.trim() && !isTrivialChangelogNote(note.trim()) ? note.trim() : "";

  const significantChanges =
    results.length > 0 ||
    instinctDelta.created > 0 ||
    instinctDelta.updated > 0 ||
    docBlocksApplied > 0 ||
    memosAttempted > 0;

  if (!significantChanges) {
    // Even if the model emits a note, avoid log spam.
    return { skills: results, instincts: instinctDelta };
  }

  if (usableNote) {
    await appendChangelog(root, usableNote);
  } else {
    const summary = [
      results.length ? `skills: ${results.map((r) => `${r.name}(${r.action})`).join(", ")}` : null,
      instinctDelta.created || instinctDelta.updated ? `instincts: +${instinctDelta.created}/~${instinctDelta.updated}` : null,
      docBlocksApplied > 0 ? `docs: blocks=${docBlocksApplied}` : null,
      memosAttempted > 0 ? `memos: +${memosAttempted}` : null,
    ].filter(Boolean).join(" | ");
    if (summary) await appendChangelog(root, summary);
  }

  return { skills: results, instincts: instinctDelta };
}

// -----------------------------
// Auto-learn (session.idle)
// -----------------------------

function defaultAutolearnPrompt(): string {
  return normalizeNewlines(`# Background Autolearn Prompt (Compound Engineering)

You are a background "learning" agent for an agentic coding system.

Your job is to propose **memory updates** from the recent activity:
- **Instincts**: small heuristics (trigger → action), with confidence.
- **Skills**: durable procedural memory stored under .opencode/skills/<name>/SKILL.md.
- **Docs**: keep AGENTS.md and LOOM_ROADMAP.md consistent.

Focus:
- Prioritize *second-order compression*: distill stable fundamentals into always-on context (AGENTS.md).

Rules:
- ONLY propose changes to: skills, instincts, memory notes, AGENTS.md, LOOM_ROADMAP.md.
- Do NOT propose changes to product code.
- Prefer updating an existing skill over creating a duplicate.
- Skills must be specific, not generic. The description should clearly indicate when to use it.
- Keep bodies short and checklist-like when possible.
- Do not write changelog entries like "no changes".

Output format:
- Output **only** valid JSON (no code fences, no commentary).
- Use this schema (CompoundSpec v2):

{
  "schema_version": 2,
  "auto": { "reason": "why", "sessionID": "ses_..." },
  "instincts": {
    "create": [ { "id": "...", "title": "...", "trigger": "...", "action": "...", "confidence": 0.6 } ],
    "update": [ { "id": "...", "confidence_delta": 0.1, "evidence_note": "..." } ]
  },
  "skills": {
    "create": [ { "name": "...", "description": "...", "body": "..." } ],
    "update": [ { "name": "...", "body": "...", "description": "..." } ]
  },
  "docs": {
    "sync": true,
    "blocks": {
      "upsert": [
        { "file": "AGENTS.md", "id": "loom-core-context", "content": "always-on context..." },
        { "file": "LOOM_ROADMAP.md", "id": "roadmap-ai-notes", "content": "empirical compass..." }
      ]
    }
  },
  "changelog": { "note": "short AI-first memory delta" }
}

Constraints:
- Max skills per run: ${AUTO_MAX_SKILLS_PER_RUN}
- Max instinct updates per run: ${AUTO_MAX_INSTINCT_UPDATES_PER_RUN}

Skill update rule (MANDATORY):
- For skills.update[], body MUST be the entire, final managed body for the skill.
- Do NOT output snippets, diffs, or partial sections. Re-emit the whole managed body with your edits applied.
- Start from the existing skill managed bodies provided in the prompt context.

Path rule (MANDATORY):
- Whenever you reference repository files or directories in any markdown you output, use repo-root-relative paths (no absolute paths).
- Example good: src/app.py, .opencode/skills/foo/SKILL.md
- Example bad: <ABSOLUTE_PATH>/src/app.py

Docs blocks guidance:
- Update AGENTS.md/loom-core-context only when a principle has stabilized.
- Update LOOM_ROADMAP.md/roadmap-ai-notes as a compass: themes, direction, near-term focus.
- Keep both blocks short. Prefer bullets.
`);
}

function extractJsonObject(text: string): any | null {
  const s = text.trim();
  // Try direct parse first.
  try {
    return JSON.parse(s);
  } catch {}
  // Otherwise, best-effort: first {...last}
  const first = s.indexOf("{");
  const last = s.lastIndexOf("}");
  if (first === -1 || last === -1 || last <= first) return null;
  try {
    return JSON.parse(s.slice(first, last + 1));
  } catch {
    return null;
  }
}

let autolearnInFlight = false;

async function autoLearnIfNeeded(
  sessionRoot: string,
  writeRoot: string,
  client: any,
  sessionID: string | null | undefined,
  reason = "session.idle"
): Promise<void> {
  if (!AUTO_ENABLED) return;
  if (autolearnInFlight) return;

  autolearnInFlight = true;
  try {
    const state = await loadState(sessionRoot);
    if (!sessionID) return;
    const last = state.autolearn?.lastRunAt ? Date.parse(state.autolearn.lastRunAt) : 0;
    const now = Date.now();
    if (last && now - last < AUTO_COOLDOWN_SECONDS * 1000) return;

    const obsCount = await countObservations(sessionRoot);
    const lastCount = state.autolearn?.lastObservationCount ?? 0;
    const newObs = obsCount.count - lastCount;

    // If events are noisy, prefer hash change as signal.
    const hashChanged = obsCount.tailHash && obsCount.tailHash !== state.autolearn?.lastObservationHash;

    if (newObs < AUTO_MIN_NEW_OBSERVATIONS && !hashChanged) return;

    const recentObs = await readObservationsTail(sessionRoot, AUTO_MAX_OBSERVATIONS_IN_PROMPT);
    const instincts = await loadInstincts(writeRoot);
    const skills = await scanSkills(writeRoot);
    const g = await gitSummary(sessionRoot);

    const promptTemplate = await safeReadFile(
      path.join(writeRoot, AUTOLEARN_PROMPT_FILE),
      defaultAutolearnPrompt()
    );

    const skillsContext = skills
      .slice(0, 25)
      .map((s) => {
        const body = s.managedBody?.trim() ?? "";
        return [`-- skill: ${s.name}`, `description: ${s.description}`, "managed_body:", body || "(empty)", "-- end skill"].join("\n");
      })
      .join("\n\n");

    const context = normalizeNewlines(`
## AUTOLEARN CONTEXT
session_id: ${sessionID ?? "unknown"}
reason: ${reason}
time: ${nowIso()}

### Git summary
changed_files: ${g.ok ? g.changedFiles.length : "n/a"}
diffstat:
${g.diffStat || "(none)"}

### Existing skills (managed bodies)
${skillsContext || "(none)"}

### Existing instincts (top)
${renderInstinctsIndex(instincts.instincts, 20)}

### Recent observations (most recent last)
${recentObs
  .map((o) => {
    const t = String(o.type ?? "");
    const toolName = o["tool"] ? ` tool=${String(o["tool"])}` : "";
    const cmdName = o["command"] ? ` command=${String(o["command"])}` : "";
    const msg = o["summary"] ? ` summary=${String(o["summary"])}` : "";
    return `- ${o.ts} ${t}${toolName}${cmdName}${msg}`;
  })
  .join("\n")}
`).trim() + "\n";

    const finalPrompt = truncate(
      promptTemplate.trim() + "\n\n" + context,
      AUTO_PROMPT_MAX_CHARS
    );

    // Ask the model for a CompoundSpec v2 in an ephemeral forked session so the gigantic
    // autolearn prompt doesn't pollute the user's active chat.
    const ephemeralSessionID = await forkEphemeralSession(client, sessionID);
    if (!ephemeralSessionID) {
      await recordAutolearnFailure(sessionRoot, sessionID, "failed to create ephemeral autolearn session");
      await tuiToast(client, "Compound autolearn failed (could not create background session)", "error");
      return;
    }

    let resp: any;
    try {
      resp = await client.session.prompt({
        path: { id: ephemeralSessionID },
        body: {
          // Use read-only agent if available; it's fine if ignored.
          agent: "plan",
          parts: [{ type: "text", text: finalPrompt }],
        },
      });
    } finally {
      // Best-effort: keep autolearn invisible by deleting the fork.
      try {
        await client.session.delete({ path: { id: ephemeralSessionID } });
      } catch {}
    }

    const text = extractTextFromMessage(resp);
    const parsed = extractJsonObject(text);
    if (!parsed) {
      await recordAutolearnFailure(sessionRoot, sessionID, text);
      await tuiToast(client, "Compound autolearn failed (invalid JSON spec)", "error");
      return;
    }

    const spec = coerceSpec(parsed);
    // Force safety rails in auto mode:
    if (spec.schema_version === 2) {
      (spec as CompoundSpecV2).auto = { reason, sessionID: sessionID ?? null };
    }

    // Apply spec (memory only)
    const applyRes = await applySpec(writeRoot, spec, "auto");

    // Always sync docs after autolearn, to keep indexes fresh.
    await syncDocs(writeRoot);
    await syncClaudeSkillsMirror(writeRoot);

    // Notify only on meaningful changes.
    try {
      const skillChanges = Array.isArray((applyRes as any)?.skills) ? (applyRes as any).skills.length : 0;
      const instinctsCreated = Number((applyRes as any)?.instincts?.created ?? 0);
      const instinctsUpdated = Number((applyRes as any)?.instincts?.updated ?? 0);
      if (skillChanges > 0 || instinctsCreated > 0 || instinctsUpdated > 0) {
        const bits: string[] = [];
        if (skillChanges > 0) bits.push(`skills=${skillChanges}`);
        if (instinctsCreated + instinctsUpdated > 0)
          bits.push(`instincts=+${instinctsCreated}/~${instinctsUpdated}`);
        await tuiToast(client, `Compound autolearn applied (${bits.join(" ")})`, "success");
      }
    } catch {}

    state.autolearn = {
      lastRunAt: nowIso(),
      lastRunSessionID: sessionID ?? null,
      lastObservationCount: obsCount.count,
      lastObservationHash: obsCount.tailHash,
    };
    await saveState(sessionRoot, state);
  } catch (e) {
    // Keep it quiet, but leave breadcrumbs for debugging.
    try {
      const msg = e instanceof Error ? `${e.name}: ${e.message}\n${e.stack ?? ""}` : String(e);
      await recordAutolearnFailure(sessionRoot, sessionID, msg);
      await tuiToast(client, "Compound autolearn failed", "error");
    } catch {}
  } finally {
    autolearnInFlight = false;
  }
}

async function safeReadFile(p: string, fallback: string): Promise<string> {
  try {
    return await fs.readFile(p, "utf8");
  } catch {
    return fallback;
  }
}

function truncate(s: string, maxChars: number): string {
  if (s.length <= maxChars) return s;
  return s.slice(0, Math.max(0, maxChars - 200)) + `\n\n(…truncated, len=${s.length})\n`;
}

function extractTextFromMessage(resp: any): string {
  // OpenCode SDK tends to return { data: { parts: [...] } } or just the message object.
  const msg = resp?.data ?? resp;
  const parts = msg?.parts ?? msg?.message?.parts ?? [];
  if (!Array.isArray(parts)) return String(msg?.content ?? "");
  return parts
    .map((p: any) => (p?.type === "text" ? String(p.text ?? "") : ""))
    .join("\n")
    .trim();
}

async function recordAutolearnFailure(root: string, sessionID: string | null | undefined, text: string): Promise<void> {
  const dir = path.join(root, MEMORY_DIR, "autolearn_failures");
  await ensureDir(dir);
  const safeID = safeFilenameComponent(sessionID ?? "", "unknown");
  const raw = String(text ?? "");
  const excerpt = scrubString(raw).slice(0, 4000);
  const payload = [
    `sessionID: ${safeID}`,
    `sha256: ${raw ? sha256(raw) : ""}`,
    "",
    excerpt || "(empty)",
  ].join("\n");
  const p = path.join(dir, `${Date.now()}_${safeID}.txt`);
  await atomicWrite(p, payload);
}

// -----------------------------
// Plugin implementation
// -----------------------------

export const CompoundEngineeringPlugin: Plugin = async ({ client, directory, worktree }) => {
  const sessionRoot = worktree ?? directory;
  const writeRoot = await resolveWriteRoot(sessionRoot);

  await ensureBootstrap(writeRoot);
  await syncDocs(writeRoot);
  await syncClaudeSkillsMirror(writeRoot);

  // Tools
  const compound_bootstrap = tool({
    description: "Create/update scaffolding (docs + dirs + prompts) for the compound engineering system.",
    parameters: {},
    execute: async () => {
      await ensureBootstrap(writeRoot);
      await syncDocs(writeRoot);
      return "compound_bootstrap complete";
    },
  });

  const compound_sync = tool({
    description: "Refresh AI-managed blocks in AGENTS.md / LOOM_ROADMAP.md and the instincts index.",
    parameters: {},
    execute: async () => {
      await syncDocs(writeRoot);
      return "compound_sync complete";
    },
  });

  const compound_status = tool({
    description: "Show compound system status: skills count, instincts count, observation count, last autolearn.",
    parameters: {},
    execute: async () => {
      const skills = await scanSkills(writeRoot);
      const instincts = await loadInstincts(writeRoot);
      const obs = await countObservations(sessionRoot);
      const state = await loadState(sessionRoot);
      const out = {
        skills: skills.length,
        instincts: instincts.instincts.length,
        observations: obs.count,
        autolearn: state.autolearn ?? {},
        mirror_claude: MIRROR_CLAUDE,
        auto_enabled: AUTO_ENABLED,
        write_root: writeRoot,
        session_root: sessionRoot,
      };
      return JSON.stringify(out, null, 2);
    },
  });

  const compound_git_summary = tool({
    description: "Get git status + diffstat for the current repo/worktree.",
    parameters: {},
    execute: async () => JSON.stringify(await gitSummary(sessionRoot), null, 2),
  });

  const compound_apply = tool({
    description: "Apply a CompoundSpec (JSON) to update skills/instincts/docs/memos/changelog. Writes memory files only.",
    parameters: { spec_json: { type: "string" } },
    execute: async ({ spec_json }: any) => {
      const parsed = JSON.parse(spec_json);
      const spec = coerceSpec(parsed);
      const r = await applySpec(writeRoot, spec, "manual");
      await syncDocs(writeRoot);
      await syncClaudeSkillsMirror(writeRoot);
      return JSON.stringify(r, null, 2);
    },
  });

  const compound_autolearn_now = tool({
    description: "Force an autolearn run now (same as session.idle background), using recent observations.",
    parameters: { sessionID: { type: "string", optional: true }, reason: { type: "string", optional: true } },
    execute: async ({ sessionID, reason }: any) => {
      await autoLearnIfNeeded(sessionRoot, writeRoot, client, sessionID ?? null, reason ?? "manual");
      return "autolearn triggered";
    },
  });

  const compound_observations_tail = tool({
    description: "Show the last N observation records (JSONL).",
    parameters: { n: { type: "number", optional: true } },
    execute: async ({ n }: any) => {
      const tail = await readObservationsTail(sessionRoot, Number(n ?? 30));
      return JSON.stringify(tail, null, 2);
    },
  });

  const compound_instincts = tool({
    description: "List instincts (top by confidence) from the instincts store.",
    parameters: { n: { type: "number", optional: true } },
    execute: async ({ n }: any) => {
      const store = await loadInstincts(writeRoot);
      const list = store.instincts
        .filter((i) => i.status === "active")
        .sort((a: any, b: any) => (b.confidence ?? 0) - (a.confidence ?? 0))
        .slice(0, Number(n ?? 30));
      return JSON.stringify(list, null, 2);
    },
  });

  // -------- Events + hooks --------

  const recordEventObservation = async (event: any) => {
    if (!LOG_OBSERVATIONS) return;

    const type = String(event?.type ?? "unknown");
    const sessionID = event?.properties?.sessionID ?? event?.properties?.sessionId ?? event?.properties?.id ?? null;

    const pick = (obj: any, keys: string[]) => {
      const out: any = {};
      for (const k of keys) if (k in (obj ?? {})) out[k] = obj[k];
      return out;
    };

    // Don't dump raw event.properties into logs. Some events can be huge or sensitive.
    const props = event?.properties;
    let safeProps: any = undefined;
    if (props && typeof props === "object") {
      if (type === "command.executed") {
        safeProps = {
          name: props.name ?? props.command,
          argv_count: Array.isArray(props.argv) ? props.argv.length : undefined,
        };
      } else if (type === "session.updated") {
        safeProps = pick(props, ["title", "id", "sessionID", "sessionId"]);
      } else if (type === "session.idle") {
        safeProps = pick(props, ["id", "sessionID", "sessionId"]);
      } else if (type === "lsp.client.diagnostics") {
        safeProps = {
          uri: props.uri ?? props.file ?? props.path,
          diagnostics_count: Array.isArray(props.diagnostics) ? props.diagnostics.length : undefined,
        };
      } else {
        safeProps = { keys: Object.keys(props).slice(0, 40) };
      }
    }

    const obs: Observation = {
      id: randomUUID(),
      ts: nowIso(),
      type,
      sessionID: sessionID ?? null,
    };

    if (safeProps) obs.properties = safeProps;

    // Basic summary to make the autolearn prompt smaller.
    if (type === "command.executed") obs.summary = `name=${String(event?.properties?.name ?? event?.properties?.command ?? "")}`;
    if (type === "session.updated") obs.summary = `title=${String(event?.properties?.title ?? "")}`;
    if (type === "lsp.client.diagnostics") obs.summary = "diagnostics";

    await appendObservation(sessionRoot, obs);
  };

  const onEvent = async ({ event }: any) => {
    try {
      if (!event?.type) return;

      // Always record (best-effort) for later pattern mining.
      await recordEventObservation(event);

      if (event.type === "command.executed") {
        const name = String(event.properties?.name ?? event.properties?.command ?? "");
        const sessionID = event.properties?.sessionID ?? event.properties?.sessionId ?? null;
        const state = await loadState(sessionRoot);
        state.lastCommand = { name, at: nowIso(), sessionID };
        await saveState(sessionRoot, state);
      }

      if (event.type === "session.idle") {
        const sessionID = event.properties?.sessionID ?? event.properties?.sessionId ?? event.properties?.id ?? null;
        await autoLearnIfNeeded(sessionRoot, writeRoot, client, sessionID ?? null, "session.idle");
      }
    } catch {
      // swallow
    }
  };

  // Tool hooks (more structured than event stream for observation logging)
  const toolAfter = async (input: any, output: any) => {
    try {
      if (!LOG_OBSERVATIONS) return;
      const toolName = String(input?.tool ?? input?.name ?? output?.tool ?? "unknown");
      const sessionID = input?.sessionID ?? input?.sessionId ?? null;
      const args = output?.args ?? input?.args ?? null;
      const ok = output?.ok ?? output?.success ?? null;

      const redactedArgs = sanitizeObservationArgs(toolName, args);
      const obs: Observation = {
        id: randomUUID(),
        ts: nowIso(),
        type: "tool.execute.after",
        sessionID,
        tool: toolName,
        ok,
        args: redactedArgs,
      };

      // Helpful single-line summary for pattern mining.
      try {
        const file = (redactedArgs as any)?.file_path ?? (redactedArgs as any)?.path ?? (redactedArgs as any)?.file;
        const bits: string[] = [];
        if (file) bits.push(`file=${String(file)}`);
        if (bits.length) (obs as any).summary = bits.join(" ");
      } catch {}

      await appendObservation(sessionRoot, obs);
    } catch {
      // swallow
    }
  };

  const toolBefore = async (input: any, output: any) => {
    try {
      if (!LOG_OBSERVATIONS) return;
      const toolName = String(input?.tool ?? input?.name ?? output?.tool ?? "unknown");
      const sessionID = input?.sessionID ?? input?.sessionId ?? null;
      const args = output?.args ?? input?.args ?? null;

      const redactedArgs = sanitizeObservationArgs(toolName, args);
      const obs: Observation = {
        id: randomUUID(),
        ts: nowIso(),
        type: "tool.execute.before",
        sessionID,
        tool: toolName,
        args: redactedArgs,
      };

      try {
        const file = (redactedArgs as any)?.file_path ?? (redactedArgs as any)?.path ?? (redactedArgs as any)?.file;
        const bits: string[] = [];
        if (file) bits.push(`file=${String(file)}`);
        if (bits.length) (obs as any).summary = bits.join(" ");
      } catch {}

      await appendObservation(sessionRoot, obs);
    } catch {}
  };

  return {
    event: onEvent,

    // Keep compaction anchored to the stable context files.
    "experimental.session.compacting": async (_input: any, out: any) => {
      out.context.push(
        [
          "## Persistent repo context (compound-engineering)",
          "- Read AGENTS.md (core behavior + links + skills + instincts).",
          "- Read LOOM_ROADMAP.md (direction + backlog + changelog).",
          "- Skills live under .opencode/skills/<name>/SKILL.md (mirrored to .claude/skills/ if enabled).",
          "- Instincts live under .opencode/memory/instincts.json (index in .opencode/memory/INSTINCTS.md).",
          "- This plugin auto-logs observations and auto-compounds memory when the session goes idle.",
        ].join("\n")
      );
    },

    // Hooks
    "tool.execute.before": toolBefore,
    "tool.execute.after": toolAfter,

    tool: {
      compound_bootstrap,
      compound_sync,
      compound_status,
      compound_git_summary,
      compound_apply,
      compound_autolearn_now,
      compound_observations_tail,
      compound_instincts,
    },
  };
};

export default CompoundEngineeringPlugin;
