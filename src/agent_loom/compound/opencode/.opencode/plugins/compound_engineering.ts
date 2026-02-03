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
const AUTO_MAX_DOC_BLOCKS_PER_RUN = intEnv("COMPOUND_AUTO_MAX_DOC_BLOCKS_PER_RUN", 3);
const AUTO_MAX_MEMOS_PER_RUN = intEnv("COMPOUND_AUTO_MAX_MEMOS_PER_RUN", 4);
const AUTO_MAX_TOOL_CALLS_PER_RUN = intEnv("COMPOUND_AUTO_MAX_TOOL_CALLS_PER_RUN", 18);
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
    lastOutcome?: "noop" | "applied" | "error";
    lastError?: string;
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

type InstinctChanges = {
  create?: InstinctCreateSpec[];
  update?: InstinctUpdateSpec[];
};

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
// Install checks (scaffolding lives in Python)
// -----------------------------

function _required_install_paths(): string[] {
  // These should be installed via `loom compound init` (Python).
  return [
    "AGENTS.md",
    "LOOM_ROADMAP.md",
    path.join(".opencode", "commands", "workflows:plan.md"),
    path.join(".opencode", "compound", "prompts", "autolearn.md"),
    path.join(".opencode", "memory", ".gitignore"),
    path.join(".opencode", "compound", ".gitignore"),
  ].map((p) => p.replace(/\\/g, "/"));
}

async function checkInstalled(root: string): Promise<{ ok: boolean; missing: string[] }> {
  const missing: string[] = [];
  for (const rel of _required_install_paths()) {
    const abs = path.join(root, rel);
    if (!(await pathExists(abs))) missing.push(rel);
  }
  return { ok: missing.length === 0, missing: missing.sort((a, b) => a.localeCompare(b)) };
}

function _install_hint(): string {
  return "Run: loom compound init --dest .";
}

async function requireInstalled(root: string): Promise<void> {
  const st = await checkInstalled(root);
  if (st.ok) return;
  const list = st.missing.map((p) => `- ${p}`).join("\n");
  throw new Error(`compound scaffolding is not installed (missing required files):\n${list}\n\n${_install_hint()}`);
}

function extractSessionID(resp: any): string {
  const r = resp?.data ?? resp;
  const id = r?.id ?? r?.data?.id ?? r?.session?.id ?? r?.data?.session?.id;
  return typeof id === "string" ? id : "";
}

async function createEphemeralSession(client: any, activeSessionID: string | null | undefined): Promise<string> {
  // Prefer a standalone session so we don't inherit user chat history.
  try {
    const resp = await client.session.create({ body: { title: "compound-autolearn" } });
    const id = extractSessionID(resp);
    if (id) return id;
  } catch {}

  // Fallback: attach to the active session if OpenCode requires a parent.
  try {
    const pid = String(activeSessionID ?? "");
    if (!pid) return "";
    const resp = await client.session.create({ body: { parentID: pid, title: "compound-autolearn" } });
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

function applyInstinctChanges(store: InstinctStore, changes?: InstinctChanges, sessionID?: string | null): { created: number; updated: number } {
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
  await requireInstalled(root);

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
  await requireInstalled(root);
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
// Auto-learn (session.idle)
// -----------------------------

function defaultAutolearnPrompt(): string {
  return normalizeNewlines(`# Background Autolearn Prompt (Compound Engineering)

You are a background "learning" agent for an agentic coding system.

Your job is to apply **memory-only updates** from the recent activity:
- **Skills** (procedural memory) under .opencode/skills/<name>/SKILL.md
- **Instincts** (trigger -> action) in .opencode/memory/instincts.json
- **Docs blocks** in AGENTS.md and LOOM_ROADMAP.md (allowed blocks only)
- Optional: memory notes via the Loom CLI if you are explicitly instructed

You must NOT propose or write product code.

How to act:
- Prefer calling tools.
- If there are durable learnings, apply them using the granular tools below.
- If there is nothing worth persisting, do nothing.

Budget (hard caps):
- Max tool calls per run: ${AUTO_MAX_TOOL_CALLS_PER_RUN}
- Max skills per run: ${AUTO_MAX_SKILLS_PER_RUN}
- Max instinct updates per run: ${AUTO_MAX_INSTINCT_UPDATES_PER_RUN}
- Max doc-block upserts per run: ${AUTO_MAX_DOC_BLOCKS_PER_RUN}
- Max memos per run: ${AUTO_MAX_MEMOS_PER_RUN}

Tools to use:
- \`compound_skill_upsert\` (create/update a skill)
- \`compound_instinct_upsert\` (create/update an instinct)
- \`compound_docblock_upsert\` (AGENTS.md/loom-core-context or LOOM_ROADMAP.md/roadmap-ai-notes only)
- \`compound_memo_add\` (add a Loom memory note; use sparingly)
- \`compound_changelog_append\` (short AI-first memory delta)
- \`compound_sync\` (refresh indexes after you make changes)

Rules:
- Prefer updating an existing skill over creating a near-duplicate.
- Skills must be procedural and short.
- Use repo-root-relative paths in markdown.
- Do not write changelog notes like "no changes".

Response:
- If you made any changes, respond with a single line: APPLIED
- If you made no changes, respond with a single line: NOOP
`);
}

let autolearnInFlight = false;

type AutolearnBudget = {
  sessionID: string;
  reason: string;
  remaining_tool_calls: number;
  remaining_skill_ops: number;
  remaining_instinct_ops: number;
  remaining_doc_ops: number;
  remaining_memo_ops: number;
  writes: {
    tool_calls: number;
    skills: number;
    instincts: number;
    docs: number;
    memos: number;
    changelog: number;
  };
};

let activeAutolearn: AutolearnBudget | null = null;

function beginAutolearnBudget(sessionID: string, reason: string): void {
  activeAutolearn = {
    sessionID,
    reason,
    remaining_tool_calls: AUTO_MAX_TOOL_CALLS_PER_RUN,
    remaining_skill_ops: AUTO_MAX_SKILLS_PER_RUN,
    remaining_instinct_ops: AUTO_MAX_INSTINCT_UPDATES_PER_RUN,
    remaining_doc_ops: AUTO_MAX_DOC_BLOCKS_PER_RUN,
    remaining_memo_ops: AUTO_MAX_MEMOS_PER_RUN,
    writes: { tool_calls: 0, skills: 0, instincts: 0, docs: 0, memos: 0, changelog: 0 },
  };
}

function endAutolearnBudget(): AutolearnBudget | null {
  const b = activeAutolearn;
  activeAutolearn = null;
  return b;
}

function consumeAutolearnToolCall(): void {
  if (!activeAutolearn) return;
  if (activeAutolearn.remaining_tool_calls <= 0) throw new Error("autolearn tool-call budget exceeded");
  activeAutolearn.remaining_tool_calls -= 1;
  activeAutolearn.writes.tool_calls += 1;
}

function consumeAutolearnSkillOp(): void {
  if (!activeAutolearn) return;
  if (activeAutolearn.remaining_skill_ops <= 0) throw new Error("autolearn skill budget exceeded");
  activeAutolearn.remaining_skill_ops -= 1;
  activeAutolearn.writes.skills += 1;
}

function consumeAutolearnInstinctOp(): void {
  if (!activeAutolearn) return;
  if (activeAutolearn.remaining_instinct_ops <= 0) throw new Error("autolearn instinct budget exceeded");
  activeAutolearn.remaining_instinct_ops -= 1;
  activeAutolearn.writes.instincts += 1;
}

function consumeAutolearnDocOp(): void {
  if (!activeAutolearn) return;
  if (activeAutolearn.remaining_doc_ops <= 0) throw new Error("autolearn doc-block budget exceeded");
  activeAutolearn.remaining_doc_ops -= 1;
  activeAutolearn.writes.docs += 1;
}

function consumeAutolearnMemoOp(): void {
  if (!activeAutolearn) return;
  if (activeAutolearn.remaining_memo_ops <= 0) throw new Error("autolearn memo budget exceeded");
  activeAutolearn.remaining_memo_ops -= 1;
  activeAutolearn.writes.memos += 1;
}

function consumeAutolearnChangelogOp(): void {
  if (!activeAutolearn) return;
  activeAutolearn.writes.changelog += 1;
}

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
  let autolearnBudget: AutolearnBudget | null = null;
  try {
    const state = await loadState(sessionRoot);
    if (!sessionID) return;

    const lastCmdName = String(state.lastCommand?.name ?? "").trim();
    const lastCmdAt = state.lastCommand?.at ? Date.parse(state.lastCommand.at) : 0;
    const last = state.autolearn?.lastRunAt ? Date.parse(state.autolearn.lastRunAt) : 0;
    const now = Date.now();
    if (last && now - last < AUTO_COOLDOWN_SECONDS * 1000) return;

    if (reason === "session.idle") {
      if (!lastCmdAt || now - lastCmdAt > 10 * 60 * 1000) return;
      if (!lastCmdName) return;
      if (lastCmdName.startsWith("compound_")) return;
    }

    const obsCount = await countObservations(sessionRoot);
    const lastCount = state.autolearn?.lastObservationCount ?? 0;
    const newObs = obsCount.count - lastCount;
    const hashChanged = obsCount.tailHash && obsCount.tailHash !== state.autolearn?.lastObservationHash;
    if (newObs < AUTO_MIN_NEW_OBSERVATIONS && !hashChanged) return;

    const g = await gitSummary(sessionRoot);
    if (reason === "session.idle") {
      const diff = String(g.diffStat ?? "").trim();
      const looksLikeWorkflow = lastCmdName.startsWith("workflows:");
      if (!diff && !looksLikeWorkflow) return;
    }

    const recentObs = await readObservationsTail(sessionRoot, AUTO_MAX_OBSERVATIONS_IN_PROMPT);
    const instincts = await loadInstincts(writeRoot);
    const skills = await scanSkills(writeRoot);

    const promptTemplate = await safeReadFile(
      path.join(writeRoot, AUTOLEARN_PROMPT_FILE),
      defaultAutolearnPrompt()
    );

    const skillsIndex = skills
      .slice(0, 30)
      .map((s) => `- ${s.name}: ${oneLine(s.description ?? "", 120)}`)
      .join("\n");

    const skillsBodies = skills
      .slice(0, 8)
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

### Existing skills (index)
${skillsIndex || "- (none)"}

### Existing skills (managed bodies; limited)
${skillsBodies || "(none)"}

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

    const finalPrompt = truncate(promptTemplate.trim() + "\n\n" + context, AUTO_PROMPT_MAX_CHARS);

    const ephemeralSessionID = await createEphemeralSession(client, sessionID);
    if (!ephemeralSessionID) {
      await recordAutolearnFailure(sessionRoot, sessionID, "failed to create ephemeral autolearn session");
      await tuiToast(client, "Compound autolearn failed (could not create background session)", "error");
      return;
    }

    let resp: any;
    try {
      beginAutolearnBudget(sessionID, reason);
      resp = await client.session.prompt({
        path: { id: ephemeralSessionID },
        body: {
          agent: "plan",
          parts: [{ type: "text", text: finalPrompt }],
        },
      });
    } finally {
      autolearnBudget = endAutolearnBudget();
      try {
        await client.session.delete({ path: { id: ephemeralSessionID } });
      } catch {}
    }

    const text = extractTextFromMessage(resp);
    if (!text) await recordAutolearnFailure(sessionRoot, sessionID, "empty autolearn response");

    let outcome: "noop" | "applied" | "error" = "noop";
    const w = autolearnBudget?.writes ?? { tool_calls: 0, skills: 0, instincts: 0, docs: 0, memos: 0, changelog: 0 };
    const didWrite = w.skills + w.instincts + w.docs + w.memos + w.changelog > 0;
    if (didWrite) {
      await syncDocs(writeRoot);
      await syncClaudeSkillsMirror(writeRoot);
      outcome = "applied";
      try {
        const bits: string[] = [];
        if (w.skills) bits.push(`skills=${w.skills}`);
        if (w.instincts) bits.push(`instincts=${w.instincts}`);
        if (w.docs) bits.push(`docs=${w.docs}`);
        if (w.memos) bits.push(`memos=${w.memos}`);
        if (w.changelog) bits.push(`changelog=${w.changelog}`);
        if (bits.length) await tuiToast(client, `Compound autolearn applied (${bits.join(" ")})`, "success");
      } catch {}
    }

    const next: PluginState = {
      ...state,
      autolearn: {
        ...(state.autolearn ?? {}),
        lastRunAt: nowIso(),
        lastRunSessionID: sessionID ?? null,
        lastObservationCount: obsCount.count,
        lastObservationHash: obsCount.tailHash,
        lastOutcome: outcome,
        lastError: "",
      },
    };
    await saveState(sessionRoot, next);
  } catch (e) {
    try {
      const msg = e instanceof Error ? `${e.name}: ${e.message}\n${e.stack ?? ""}` : String(e);
      await recordAutolearnFailure(sessionRoot, sessionID, msg);
      const state = await loadState(sessionRoot);
      const next: PluginState = {
        ...state,
        autolearn: {
          ...(state.autolearn ?? {}),
          lastOutcome: "error",
          lastError: oneLine(msg, 800),
        },
      };
      await saveState(sessionRoot, next);
      await tuiToast(client, "Compound autolearn failed", "error");
    } catch {}
  } finally {
    endAutolearnBudget();
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

  let installed = await checkInstalled(writeRoot);
  if (!installed.ok) {
    await tuiToast(client, `Compound scaffolding not installed. ${_install_hint()}`, "info");
  } else {
    await syncDocs(writeRoot);
    await syncClaudeSkillsMirror(writeRoot);
  }

  // Tools
  const compound_bootstrap = tool({
    description: "Install/upgrade compound scaffolding (via `loom compound init`).",
    parameters: {},
    execute: async () => {
      const loom = await resolveLoomRoot(writeRoot);
      const res = await runProcess({ cmd: loom.cmd, args: [...loom.args, "compound", "init", "--dest", "."] }, writeRoot, 120000);
      if (res.code !== 0) {
        throw new Error(`compound_bootstrap failed (exit=${res.code})\n${(res.stderr || res.stdout || "").trim()}`);
      }

      installed = await checkInstalled(writeRoot);
      if (!installed.ok) {
        const list = installed.missing.map((p) => `- ${p}`).join("\n");
        throw new Error(`compound_bootstrap ran but scaffolding still missing:\n${list}`);
      }

      await syncDocs(writeRoot);
      await syncClaudeSkillsMirror(writeRoot);
      return "compound_bootstrap complete";
    },
  });

  const compound_sync = tool({
    description: "Refresh AI-managed blocks in AGENTS.md / LOOM_ROADMAP.md and the instincts index.",
    parameters: {},
    execute: async () => {
      await syncDocs(writeRoot);
      await syncClaudeSkillsMirror(writeRoot);
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

  const compound_skill_upsert = tool({
    description: "Create/update a skill (procedural memory).",
    parameters: {
      name: { type: "string" },
      description: { type: "string", optional: true },
      body: { type: "string" },
    },
    execute: async ({ name, description, body }: any) => {
      await requireInstalled(writeRoot);
      consumeAutolearnToolCall();

      const n = String(name ?? "").trim();
      const b = String(body ?? "");
      const d = String(description ?? "").trim();
      if (!n) throw new Error("skill.name is required");
      if (!b.trim()) throw new Error("skill.body is required");

      let desc = d;
      if (!desc) {
        const skillPath = path.join(writeRoot, SKILLS_DIR, n, "SKILL.md");
        if (await pathExists(skillPath)) {
          const raw = await fs.readFile(skillPath, "utf8");
          const parsed = parseFrontmatter(raw);
          desc = parsed.fm.description ?? "";
        }
      }
      if (!desc) desc = `Skill: ${n}`;

      const r = await writeOrUpdateSkill(writeRoot, { name: n, description: desc, body: b });
      consumeAutolearnSkillOp();
      await syncClaudeSkillsMirror(writeRoot);
      return JSON.stringify(r, null, 2);
    },
  });

  const compound_instinct_upsert = tool({
    description: "Create/update an instinct (trigger -> action heuristic).",
    parameters: {
      operation: { type: "string" },
      id: { type: "string" },
      title: { type: "string", optional: true },
      trigger: { type: "string", optional: true },
      action: { type: "string", optional: true },
      confidence: { type: "number", optional: true },
      confidence_delta: { type: "number", optional: true },
      evidence_note: { type: "string", optional: true },
    },
    execute: async (input: any) => {
      await requireInstalled(writeRoot);
      consumeAutolearnToolCall();

      const op = String(input?.operation ?? "").trim().toLowerCase();
      const id = String(input?.id ?? "").trim();
      if (!op || !["create", "update"].includes(op)) {
        throw new Error("operation must be 'create' or 'update'");
      }
      if (!id) throw new Error("id is required");

      const store = await loadInstincts(writeRoot);
      const sid = activeAutolearn?.sessionID ?? null;
      let delta = { created: 0, updated: 0 };
      if (op === "create") {
        const title = String(input?.title ?? "").trim();
        const trigger = String(input?.trigger ?? "").trim();
        const action = String(input?.action ?? "").trim();
        const confidence = Number(input?.confidence ?? NaN);
        if (!title || !trigger || !action) throw new Error("create requires title, trigger, action");
        if (!Number.isFinite(confidence)) throw new Error("create requires confidence (number)");
        delta = applyInstinctChanges(store, { create: [{ id, title, trigger, action, confidence }] }, sid);
      } else {
        const confidence_delta = input?.confidence_delta;
        const evidence_note = input?.evidence_note;
        delta = applyInstinctChanges(
          store,
          { update: [{ id, confidence_delta, evidence_note }] },
          sid
        );
      }

      if (delta.created || delta.updated) {
        await saveInstincts(writeRoot, store);
        consumeAutolearnInstinctOp();
      }
      return JSON.stringify(delta, null, 2);
    },
  });

  const compound_docblock_upsert = tool({
    description: "Upsert an allowed AI-managed doc block.",
    parameters: {
      file: { type: "string" },
      id: { type: "string" },
      content: { type: "string" },
    },
    execute: async ({ file, id, content }: any) => {
      await requireInstalled(writeRoot);
      consumeAutolearnToolCall();

      const f = String(file ?? "").trim().replace(/\\/g, "/");
      const blockID = String(id ?? "").trim();
      let c = normalizeNewlines(String(content ?? "")).trim();
      if (!f || !blockID || !c) throw new Error("file, id, and content are required");

      if (c.length > DOC_BLOCK_MAX_CHARS) {
        c = c.slice(0, DOC_BLOCK_MAX_CHARS).trimEnd() + "\n";
      }
      c = rewriteRepoAbsolutePaths(writeRoot, c);

      const allowed: Record<string, Set<string>> = {
        "AGENTS.md": new Set(["loom-core-context"]),
        "LOOM_ROADMAP.md": new Set(["roadmap-ai-notes"]),
      };
      if (!(f in allowed) || !allowed[f]?.has(blockID)) {
        throw new Error(`doc block not allowed: ${f}#${blockID}`);
      }
      if (f.startsWith("/") || f.includes("..")) throw new Error("file must be repo-relative");

      const abs = path.resolve(writeRoot, f);
      const rel = path.relative(writeRoot, abs);
      if (!rel || rel.startsWith("..") || path.isAbsolute(rel)) {
        throw new Error("file escapes repo root");
      }

      const existing = await safeReadFile(abs, "");
      const updated = upsertManagedBlock(existing || "", blockID, c);
      if (updated !== existing) {
        await atomicWrite(abs, updated);
        consumeAutolearnDocOp();
        return JSON.stringify({ ok: true, changed: true }, null, 2);
      }
      return JSON.stringify({ ok: true, changed: false }, null, 2);
    },
  });

  const compound_changelog_append = tool({
    description: "Append a short AI-first memory delta to LOOM_ROADMAP.md.",
    parameters: { note: { type: "string" } },
    execute: async ({ note }: any) => {
      await requireInstalled(writeRoot);
      consumeAutolearnToolCall();
      const n = String(note ?? "").trim();
      if (!n) throw new Error("note is required");
      if (isTrivialChangelogNote(n)) return "skipped";
      await appendChangelog(writeRoot, n);
      consumeAutolearnChangelogOp();
      return "ok";
    },
  });

  const compound_memo_add = tool({
    description: "Add a Loom memory note (use sparingly; scoped).",
    parameters: {
      title: { type: "string" },
      body: { type: "string" },
      tags: { type: "array", optional: true },
      scopes: { type: "array", optional: true },
      visibility: { type: "string", optional: true },
    },
    execute: async (input: any) => {
      await requireInstalled(writeRoot);
      consumeAutolearnToolCall();

      const title = String(input?.title ?? "").trim();
      const body = String(input?.body ?? "").trim();
      if (!title || !body) throw new Error("title and body are required");

      const mem = await resolveMemoryCli(writeRoot);
      const args = [...mem.args, "add", "--title", title, "--body", body];
      const tags = Array.isArray(input?.tags) ? input.tags : [];
      const scopes = Array.isArray(input?.scopes) ? input.scopes : [];
      for (const t of tags) {
        const s = String(t ?? "").trim();
        if (s) args.push("--tag", s);
      }
      for (const s0 of scopes) {
        const s = String(s0 ?? "").trim();
        if (s) args.push("--scope", s);
      }
      if (input?.visibility) args.push("--visibility", String(input.visibility));

      const res = await runProcess({ cmd: mem.cmd, args }, writeRoot, 30000);
      if (res.code !== 0) throw new Error(`loom memory add failed (exit=${res.code})`);
      consumeAutolearnMemoOp();
      return "ok";
    },
  });

  const compound_autolearn_now = tool({
    description: "Force an autolearn run now (same as session.idle background), using recent observations.",
    parameters: { sessionID: { type: "string", optional: true }, reason: { type: "string", optional: true } },
    execute: async ({ sessionID, reason }: any) => {
      await requireInstalled(writeRoot);
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
    if (!installed.ok) return;
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

      if (!installed.ok) return;

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
      compound_skill_upsert,
      compound_instinct_upsert,
      compound_docblock_upsert,
      compound_changelog_append,
      compound_memo_add,
      compound_autolearn_now,
      compound_observations_tail,
      compound_instincts,
    },
  };
};

export default CompoundEngineeringPlugin;
