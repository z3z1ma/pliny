// OpenCode Compound Engineering Plugin (thin adapter)
//
// Responsibilities:
// - Append-only observation logging from OpenCode hooks -> .opencode/memory/observations.jsonl
// - (Optional) trigger a background autolearn prompt on session.idle
// - (Optional) run Loom priming/refresh on session start so context stays current
//
// Non-responsibilities:
// - Do not write product code
// - Do not implement skill/instinct/doc/changelog logic in TS
//   (Those are first-class `loom compound ...` commands; the model should run them via bash.)

import type { Plugin } from "@opencode-ai/plugin";

import { spawn } from "node:child_process";
import { createHash, randomUUID } from "node:crypto";
import * as fs from "node:fs/promises";
import * as path from "node:path";

const MEMORY_DIR = path.join(".opencode", "memory");
const OBSERVATIONS_FILE = path.join(MEMORY_DIR, "observations.jsonl");
const AUTOLEARN_PROMPT_FILE = path.join(".opencode", "compound", "prompts", "autolearn.md");
const AUTOLEARN_STATUS_FILE = path.join(".opencode", "compound", "autolearn_status.json");

const DEFAULT_LOOM_BIN = process.env.COMPOUND_LOOM_BIN ?? "loom";

const LOG_OBSERVATIONS = (process.env.COMPOUND_LOG_OBSERVATIONS ?? "1") !== "0";
const OBS_MAX_BYTES = intEnv("COMPOUND_OBSERVATIONS_MAX_BYTES", 32 * 1024 * 1024);

const AUTO_ENABLED = (process.env.COMPOUND_AUTO ?? "1") !== "0";
const AUTO_COOLDOWN_SECONDS = intEnv("COMPOUND_AUTO_COOLDOWN_SECONDS", 120);
const AUTO_MIN_NEW_OBSERVATIONS = intEnv("COMPOUND_AUTO_MIN_NEW_OBSERVATIONS", 12);
const AUTO_MAX_OBSERVATIONS_IN_PROMPT = intEnv("COMPOUND_AUTO_MAX_OBSERVATIONS_IN_PROMPT", 80);
const AUTO_PROMPT_MAX_CHARS = intEnv("COMPOUND_AUTO_PROMPT_MAX_CHARS", 18000);

const PRIME_ON_START = (process.env.COMPOUND_PRIME_ON_START ?? "0") !== "0";
const REFRESH_ON_START = (process.env.COMPOUND_REFRESH_ON_START ?? "0") !== "0";

type ISODate = string;

type Observation = Record<string, unknown> & {
  id: string;
  ts: ISODate;
  type: string;
  sessionID?: string | null;
};

function nowIso(): ISODate {
  return new Date().toISOString();
}

function intEnv(key: string, fallback: number): number {
  const v = process.env[key];
  if (!v) return fallback;
  const n = Number(v);
  return Number.isFinite(n) ? Math.trunc(n) : fallback;
}

function sha256(s: string): string {
  return createHash("sha256").update(s).digest("hex");
}

function normalizeNewlines(s: string): string {
  return String(s ?? "").replace(/\r\n/g, "\n");
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

async function appendJsonl(root: string, rel: string, obj: unknown): Promise<void> {
  const filePath = path.join(root, rel);
  await ensureDir(path.dirname(filePath));

  // Soft-rotate if huge.
  try {
    const st = await fs.stat(filePath);
    if (st.size > OBS_MAX_BYTES) {
      const rotated = `${filePath}.${Date.now()}.bak`;
      await fs.rename(filePath, rotated);
    }
  } catch {}

  await fs.appendFile(filePath, JSON.stringify(obj) + "\n", "utf8");
}

async function tuiToast(client: any, message: string, variant: "success" | "error" | "info" = "info") {
  try {
    await client.tui.showToast({ body: { message, variant } });
  } catch {}
}

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

async function resolveLoom(root: string): Promise<CommandSpec> {
  const candidates = [DEFAULT_LOOM_BIN, "agent-loom", "loom"];
  for (const c of candidates) {
    const r = await runProcess({ cmd: c, args: ["--help"] }, root, 8000);
    if (r.code === 0) return { cmd: c, args: [] };
  }
  return { cmd: DEFAULT_LOOM_BIN, args: [] };
}

async function resolveRepoRoot(start: string): Promise<string> {
  const r = await runProcess({ cmd: "git", args: ["rev-parse", "--show-toplevel"] }, start, 8000);
  const top = r.code === 0 ? String(r.stdout || "").trim() : "";
  return top || start;
}

async function checkInstalled(root: string): Promise<{ ok: boolean; missing: string[] }> {
  const required = [
    "AGENTS.md",
    "LOOM.md",
    ".loom/compound/ROADMAP.md",
    ".loom/compound/README.md",
    ".opencode/commands/workflow-plan.md",
    ".opencode/commands/workflow-work.md",
    ".opencode/commands/workflow-review.md",
    ".opencode/commands/workflow-compound.md",
    ".opencode/compound/.gitignore",
    ".opencode/compound/prompts/autolearn.md",
    ".opencode/memory/.gitignore",
  ];
  const missing: string[] = [];
  for (const rel of required) {
    if (!(await pathExists(path.join(root, rel)))) missing.push(rel);
  }
  missing.sort((a, b) => a.localeCompare(b));
  return { ok: missing.length === 0, missing };
}

function _install_hint(): string {
  return "Run: loom compound init";
}

// -----------------------------
// Observation scrubbing
// -----------------------------

const SECRET_KEY_RE = /(pass(word)?|secret|token|api[_-]?key|auth(orization)?|cookie|session|private[_-]?key)/i;
const SECRET_VALUE_RE = [
  /\bghp_[A-Za-z0-9]{20,}\b/g,
  /\bgithub_pat_[A-Za-z0-9_]{20,}\b/g,
  /\bsk-[A-Za-z0-9]{16,}\b/g,
  /\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b/g,
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

  // For shell-like tools, never persist raw commands.
  if (/bash|shell/i.test(toolName)) {
    const cmd = typeof (args as any)?.command === "string" ? String((args as any).command) : "";
    return {
      redacted: true,
      command_len: cmd.length,
      command_sha256: cmd ? sha256(cmd) : "",
    };
  }

  const cloned: any = Array.isArray(args) ? [...args] : { ...args };

  const scrub = (v: any, key: string, depth: number): any => {
    if (depth > 4) return "{...}";
    if (SECRET_KEY_RE.test(key)) return "[REDACTED]";
    if (typeof v === "string") return scrubString(v);
    if (Array.isArray(v)) return v.slice(0, 50).map((x) => scrub(x, key, depth + 1));
    if (v && typeof v === "object") {
      const out: any = {};
      for (const [k, vv] of Object.entries(v)) {
        out[k] = SECRET_KEY_RE.test(k) ? "[REDACTED]" : scrub(vv, k, depth + 1);
      }
      return out;
    }
    return v;
  };

  return scrub(cloned, "args", 0);
}

// -----------------------------
// Autolearn (session.idle)
// -----------------------------

let autolearnInFlight = false;
let lastAutolearnAt = 0;
let lastObservationCount = 0;
let lastObservationHash = "";

async function readObservationsTail(root: string, maxLines: number): Promise<Observation[]> {
  const filePath = path.join(root, OBSERVATIONS_FILE);
  if (!(await pathExists(filePath))) return [];
  const raw = await fs.readFile(filePath, "utf8");
  const lines = raw.trimEnd().split("\n").filter(Boolean);
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
  const lines = raw.trimEnd().split("\n").filter(Boolean);
  const tail = lines.slice(Math.max(0, lines.length - 200)).join("\n");
  return { count: lines.length, tailHash: tail ? sha256(tail) : "" };
}

async function createEphemeralSession(client: any, activeSessionID: string | null | undefined): Promise<string> {
  // Prefer a standalone session so we don't inherit user chat history.
  try {
    const resp = await client.session.create({ body: { title: "compound-autolearn" } });
    const r = resp?.data ?? resp;
    const id = r?.id ?? r?.data?.id ?? r?.session?.id ?? r?.data?.session?.id;
    if (typeof id === "string" && id) return id;
  } catch {}

  // Fallback: attach to the active session if OpenCode requires a parent.
  try {
    const pid = String(activeSessionID ?? "");
    if (!pid) return "";
    const resp = await client.session.create({ body: { parentID: pid, title: "compound-autolearn" } });
    const r = resp?.data ?? resp;
    const id = r?.id ?? r?.data?.id ?? r?.session?.id ?? r?.data?.session?.id;
    if (typeof id === "string" && id) return id;
  } catch {}

  return "";
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
  return s.slice(0, Math.max(0, maxChars - 200)) + `\n\n(...truncated, len=${s.length})\n`;
}

async function gitSummary(root: string): Promise<{ changedFiles: string[]; diffStat: string }> {
  const status = await runProcess({ cmd: "git", args: ["status", "--porcelain"] }, root, 20000);
  const changedFiles =
    status.code === 0
      ? status.stdout
          .split("\n")
          .map((l: any) => String(l || "").trim())
          .filter(Boolean)
          .map((l: any) => String(l).slice(3).trim())
      : [];
  const diffStatRes = await runProcess({ cmd: "git", args: ["diff", "--stat"] }, root, 20000);
  const diffStat = diffStatRes.code === 0 ? String(diffStatRes.stdout || "").trim() : "";
  return { changedFiles, diffStat };
}

async function autoLearnIfNeeded(sessionRoot: string, client: any, sessionID: string | null | undefined): Promise<void> {
  if (!AUTO_ENABLED) return;
  if (autolearnInFlight) return;
  if (!sessionID) return;

  const now = Date.now();
  if (lastAutolearnAt && now - lastAutolearnAt < AUTO_COOLDOWN_SECONDS * 1000) return;

  const obsCount = await countObservations(sessionRoot);
  const newObs = obsCount.count - lastObservationCount;
  const hashChanged = obsCount.tailHash && obsCount.tailHash !== lastObservationHash;
  if (newObs < AUTO_MIN_NEW_OBSERVATIONS && !hashChanged) return;

  const g = await gitSummary(sessionRoot);
  const diff = String(g.diffStat || "").trim();
  if (!diff) return;

  autolearnInFlight = true;
  lastAutolearnAt = now;
  lastObservationCount = obsCount.count;
  lastObservationHash = obsCount.tailHash;
  try {
    const promptTemplate = await safeReadFile(path.join(sessionRoot, AUTOLEARN_PROMPT_FILE), "");
    if (!promptTemplate.trim()) return;

    const recentObs = await readObservationsTail(sessionRoot, AUTO_MAX_OBSERVATIONS_IN_PROMPT);
    const context = normalizeNewlines(`
## AUTOLEARN CONTEXT
session_id: ${sessionID ?? "unknown"}
reason: session.idle

### Git summary
changed_files: ${g.changedFiles.length}
diffstat:
${g.diffStat || "(none)"}

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
`).trim();

    const finalPrompt = truncate(promptTemplate.trim() + "\n\n" + context + "\n", AUTO_PROMPT_MAX_CHARS);

    const ephemeralSessionID = await createEphemeralSession(client, sessionID);
    if (!ephemeralSessionID) return;

    let resp: any;
    try {
      resp = await client.session.prompt({
        path: { id: ephemeralSessionID },
        body: {
          agent: "plan",
          parts: [{ type: "text", text: finalPrompt }],
        },
      });
    } finally {
      try {
        await client.session.delete({ path: { id: ephemeralSessionID } });
      } catch {}
    }

    const msg = resp?.data ?? resp;
    const parts = msg?.parts ?? msg?.message?.parts ?? [];
    const text = Array.isArray(parts)
      ? parts.map((p: any) => (p?.type === "text" ? String(p.text ?? "") : "")).join("\n").trim()
      : String(msg?.content ?? "").trim();

    let proposals: any = null;
    try {
      proposals = text ? JSON.parse(text) : null;
    } catch {
      proposals = null;
    }

    const wroteStatus = async (payload: any) => {
      try {
        await ensureDir(path.join(sessionRoot, ".opencode", "compound"));
        await fs.writeFile(path.join(sessionRoot, AUTOLEARN_STATUS_FILE), JSON.stringify(payload, null, 2) + "\n", "utf8");
      } catch {}
    };

    if (!proposals || typeof proposals !== "object" || Array.isArray(proposals)) {
      await wroteStatus({ ok: false, ts: nowIso(), error: "invalid_json", raw_len: text.length });
      return;
    }

    const isEmpty = Object.keys(proposals).length === 0;
    if (isEmpty) {
      await wroteStatus({ ok: true, ts: nowIso(), applied: false, reason: "noop" });
      return;
    }

    const loom = await resolveLoom(sessionRoot);
    const learnRes = await runProcess(
      {
        cmd: loom.cmd,
        args: [...loom.args, "compound", "learn", "--auto", "--proposals", JSON.stringify(proposals), "--json"],
      },
      sessionRoot,
      120000
    );

    if (learnRes.code === 0) {
      await tuiToast(client, "Compound autolearn applied", "success");
      await wroteStatus({ ok: true, ts: nowIso(), applied: true, exit_code: learnRes.code, stdout: truncate(String(learnRes.stdout || ""), 4000) });
    } else {
      await tuiToast(client, "Compound autolearn failed", "error");
      await wroteStatus({ ok: false, ts: nowIso(), applied: false, exit_code: learnRes.code, stdout: truncate(String(learnRes.stdout || ""), 4000), stderr: truncate(String(learnRes.stderr || ""), 4000) });
    }
  } catch {
    // swallow
  } finally {
    autolearnInFlight = false;
  }
}

// -----------------------------
// Plugin implementation
// -----------------------------

export const CompoundEngineeringPlugin: Plugin = async ({ client, directory, worktree }) => {
  const sessionRoot = worktree ?? directory;
  const repoRoot = await resolveRepoRoot(sessionRoot);

  const installed = await checkInstalled(repoRoot);
  if (!installed.ok) {
    await tuiToast(client, `Compound scaffolding not installed. ${_install_hint()}`, "info");
  } else {
    // Best-effort: keep derived docs and rules current at session start.
    try {
      const loom = await resolveLoom(repoRoot);
      if (REFRESH_ON_START || PRIME_ON_START) {
        await runProcess({ cmd: loom.cmd, args: [...loom.args, "compound", "update", "--json"] }, repoRoot, 60000);
      }
    } catch {}
  }

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
    if (type === "command.executed") obs.summary = `name=${String(event?.properties?.name ?? event?.properties?.command ?? "")}`;
    if (type === "session.updated") obs.summary = `title=${String(event?.properties?.title ?? "")}`;

    await appendJsonl(repoRoot, OBSERVATIONS_FILE, obs);
  };

  const onEvent = async ({ event }: any) => {
    try {
      if (!event?.type) return;
      if (!installed.ok) return;

      await recordEventObservation(event);

      if (event.type === "session.idle") {
        const sessionID = event.properties?.sessionID ?? event.properties?.sessionId ?? event.properties?.id ?? null;
        await autoLearnIfNeeded(repoRoot, client, sessionID ?? null);
      }
    } catch {
      // swallow
    }
  };

  const toolBefore = async (input: any, output: any) => {
    try {
      if (!installed.ok) return;
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

       await appendJsonl(repoRoot, OBSERVATIONS_FILE, obs);
     } catch {}
   };

  const toolAfter = async (input: any, output: any) => {
    try {
      if (!installed.ok) return;
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

      await appendJsonl(repoRoot, OBSERVATIONS_FILE, obs);
    } catch {
      // swallow
    }
  };

  return {
    event: onEvent,
    "tool.execute.before": toolBefore,
    "tool.execute.after": toolAfter,

    // Keep compaction anchored to stable context files.
    "experimental.session.compacting": async (_input: any, out: any) => {
      out.context.push(
        [
          "## Persistent repo context (compound-engineering)",
          "- Read AGENTS.md (stable human-owned overview).",
          "- Read LOOM.md (derived always-on context + instincts summary).",
          "- Read .loom/compound/ROADMAP.md (direction + backlog + changelog).",
          "- Rules/cookbooks may be written to .opencode/rules/*.md via `loom compound update`.",
          "- Skills live under .opencode/skills/<name>/SKILL.md (mirrored to .claude/skills/ when enabled).",
          "- This plugin logs observations and may trigger a background autolearn on session idle.",
        ].join("\n")
      );
    },
  };
};

export default CompoundEngineeringPlugin;
