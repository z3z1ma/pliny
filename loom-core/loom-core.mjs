import { readdirSync, readFileSync, statSync } from "node:fs";
import { basename, dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PACKAGE_ROOT = dirname(fileURLToPath(import.meta.url));
const PLUGIN_ID = "open-loom-core";
const BOOTSTRAP_MARKER = "loom-core-using-loom-bootstrap";
const USING_LOOM_REFERENCE_ORDER = [
  "how-loom-thinks.md",
  "activation-discipline.md",
  "directory-structure.md",
  "shaping-with-humans.md",
  "delegating-to-workers.md",
  "proving-the-work.md",
  "staying-safe.md",
];
const TRIGGER_DESCRIPTION_PREFIXES = ["Always activate", "Use when", "Use before", "Use after"];
const ACTIVATION_REQUIRED_PHRASES = [
  "Activation Discipline",
  "If you think there is even a 1% chance a skill might apply, you ABSOLUTELY MUST",
  "IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE",
  "before responding",
  "before asking clarifying questions",
  "before code exploration",
  "before quick checks",
  "before editing files",
  "before creating tickets",
  "before launching Ralph",
  "this is simple",
  "this is just a small change",
  "I need more context first",
  "I'll create the ticket after",
  "I'll ask the worker directly",
  "evidence can wait",
  "audit is overkill",
  "I'll just do this one thing first",
];
const bootstrapCache = new Map();

function posixPath(path) {
  return path.split("\\").join("/");
}

function directoryExists(directory) {
  return statSync(directory, { throwIfNoEntry: false })?.isDirectory() === true;
}

function fileExists(file) {
  return statSync(file, { throwIfNoEntry: false })?.isFile() === true;
}

function markdownFilesIn(directory, { recursive = false } = {}) {
  if (!directoryExists(directory)) return [];

  const result = [];
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory() && recursive) {
      result.push(...markdownFilesIn(path, { recursive }));
      continue;
    }
    if (entry.isFile() && entry.name.endsWith(".md")) result.push(path);
  }

  return result.sort((a, b) => a.localeCompare(b));
}

function readMarkdownDocument(file) {
  const text = readFileSync(file, "utf8").trimEnd();
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!match) return { data: {}, content: text };

  const data = {};
  for (const line of match[1].split(/\r?\n/)) {
    const scalar = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!scalar) continue;
    const value = scalar[2].trim().replace(/^["']|["']$/g, "");
    data[scalar[1]] = value;
  }

  return {
    data,
    content: text.slice(match[0].length).trim(),
  };
}

function pushUnique(array, value) {
  if (!array.includes(value)) array.push(value);
}

function surfaceOptions(options = {}) {
  return {
    rootDir: resolve(String(options.rootDir || PACKAGE_ROOT)),
    usingLoom: options.usingLoom !== false,
    skills: options.skills !== false,
    agents: options.agents !== false,
  };
}

export function readOrderedUsingLoomFiles(options = {}) {
  const { rootDir } = surfaceOptions(options);
  const skillPath = join(rootDir, "skills", "using-loom", "SKILL.md");
  const referencesDir = join(rootDir, "skills", "using-loom", "references");
  const referenceOrder = new Map(USING_LOOM_REFERENCE_ORDER.map((name, index) => [name, index]));
  const references = markdownFilesIn(referencesDir).sort((a, b) => {
    const aOrder = referenceOrder.get(basename(a)) ?? Number.MAX_SAFE_INTEGER;
    const bOrder = referenceOrder.get(basename(b)) ?? Number.MAX_SAFE_INTEGER;
    if (aOrder !== bOrder) return aOrder - bOrder;
    return a.localeCompare(b);
  });
  const files = fileExists(skillPath) ? [skillPath, ...references] : references;
  return files.map((path) => ({
    path: posixPath(relative(rootDir, path)),
    absolutePath: path,
    text: readFileSync(path, "utf8").trimEnd(),
  }));
}

export function readSkillFiles(options = {}) {
  const { rootDir } = surfaceOptions(options);
  const skillRoot = join(rootDir, "skills");
  if (!directoryExists(skillRoot)) return [];

  return readdirSync(skillRoot)
    .map((name) => ({ name, path: join(skillRoot, name, "SKILL.md") }))
    .filter((entry) => fileExists(entry.path))
    .sort((a, b) => a.name.localeCompare(b.name))
    .map((entry) => {
      const md = readMarkdownDocument(entry.path);
      return {
        directory: entry.name,
        path: posixPath(relative(rootDir, entry.path)),
        name: md.data.name || entry.name,
        description: md.data.description || "",
      };
    });
}

export function readAgentFiles(options = {}) {
  const { rootDir } = surfaceOptions(options);
  const agentRoot = join(rootDir, "agents");
  return markdownFilesIn(agentRoot).map((path) => {
    const md = readMarkdownDocument(path);
    return {
      path: posixPath(relative(rootDir, path)),
      name: md.data.name || basename(path, ".md"),
      description: md.data.description || "",
      content: md.content,
    };
  });
}

export function readLoomWeaverAgent(options = {}) {
  return readAgentFiles(options).find((agent) => agent.name === "loom-weaver") || null;
}

export function readCodexLoomWeaverAgent(options = {}) {
  const { rootDir } = surfaceOptions(options);
  const agentPath = join(rootDir, "codex", "agents", "loom-weaver.toml");
  if (!fileExists(agentPath)) return null;
  const text = readFileSync(agentPath, "utf8").trimEnd();
  const developerInstructionsMatch = text.match(/developer_instructions\s*=\s*"""([\s\S]*)"""\s*$/);
  const developerInstructions = developerInstructionsMatch
    ? developerInstructionsMatch[1].replace(/^\r?\n/, "").trimEnd()
    : "";
  return {
    path: posixPath(relative(rootDir, agentPath)),
    text,
    developerInstructions,
  };
}

export function configureOpenCode(config, options = {}) {
  const surfaces = surfaceOptions(options);

  if (surfaces.skills) {
    const skillRoot = join(surfaces.rootDir, "skills");
    if (readSkillFiles(surfaces).length > 0) {
      config.skills ??= {};
      config.skills.paths ??= [];
      pushUnique(config.skills.paths, skillRoot);
    }
  }

  if (surfaces.agents) {
    const loomWeaver = readLoomWeaverAgent(surfaces);
    if (loomWeaver) {
      config.agent ??= {};
      config.agent["loom-weaver"] ??= {
        description: loomWeaver.description,
        mode: "all",
        prompt: loomWeaver.content,
        permission: {
          read: "allow",
          glob: "allow",
          grep: "allow",
          edit: {
            "*": "deny",
            ".loom/**": "allow",
          },
          bash: "ask",
          task: "deny",
          skill: "allow",
          question: "allow",
        },
      };
    }
  }

  return config;
}

export function getUsingLoomBootstrapContent(options = {}) {
  const surfaces = surfaceOptions(options);
  if (!surfaces.usingLoom) return null;

  const cacheKey = surfaces.rootDir;
  if (bootstrapCache.has(cacheKey)) return bootstrapCache.get(cacheKey);

  const files = readOrderedUsingLoomFiles(surfaces);
  if (files.length === 0) {
    bootstrapCache.set(cacheKey, null);
    return null;
  }

  const sections = files.map((reference) => {
    const content = reference.path.endsWith("/SKILL.md")
      ? readMarkdownDocument(reference.absolutePath).content
      : reference.text;
    return `# Source: ${reference.path}\n\n${content}`;
  }).join("\n\n");

  const bootstrap = `<EXTREMELY_IMPORTANT>\n${BOOTSTRAP_MARKER}\nYou have Loom.\n\nIMPORTANT: The using-loom skill content and ordered references are included below. They are ALREADY LOADED - you are currently following them. Do NOT use the skill tool to load \"using-loom\" again just to satisfy session start.\n\nFor every other relevant Loom skill, use OpenCode's native \`skill\` tool. Skill invocation comes before clarifying questions, code exploration, quick checks, edits, ticket creation, Ralph launches, evidence claims, audit claims, or closure.\n\n${sections}\n</EXTREMELY_IMPORTANT>`;

  bootstrapCache.set(cacheKey, bootstrap);
  return bootstrap;
}

export function injectUsingLoomBootstrap(output, options = {}) {
  const bootstrap = getUsingLoomBootstrapContent(options);
  if (!bootstrap || !output?.messages?.length) return output;

  const firstUser = output.messages.find((message) => message.info?.role === "user" || message.role === "user");
  if (!firstUser) return output;
  firstUser.parts ??= [];
  if (firstUser.parts.some((part) => part.type === "text" && part.text.includes(BOOTSTRAP_MARKER))) {
    return output;
  }

  const ref = firstUser.parts[0] || {};
  firstUser.parts.unshift({ ...ref, type: "text", text: bootstrap });
  return output;
}

export function inspectActivationDiscipline(options = {}) {
  const surfaces = surfaceOptions(options);
  const usingLoomReferences = readOrderedUsingLoomFiles(surfaces);
  const combinedDoctrine = usingLoomReferences.map((reference) => reference.text).join("\n");
  const lowerDoctrine = combinedDoctrine.toLowerCase();
  const missingPhrases = ACTIVATION_REQUIRED_PHRASES.filter(
    (phrase) => !lowerDoctrine.includes(phrase.toLowerCase()),
  );
  const triggerDescriptionFailures = readSkillFiles(surfaces)
    .filter((skill) => !TRIGGER_DESCRIPTION_PREFIXES.some((prefix) => skill.description.startsWith(prefix)))
    .map((skill) => ({ name: skill.name, description: skill.description }));
  const hasActivationReference = usingLoomReferences.some(
    (reference) => reference.path === "skills/using-loom/references/activation-discipline.md",
  );

  return {
    ok: hasActivationReference && missingPhrases.length === 0 && triggerDescriptionFailures.length === 0,
    hasActivationReference,
    requiredPhraseCount: ACTIVATION_REQUIRED_PHRASES.length,
    missingPhrases,
    triggerDescriptionPrefixes: TRIGGER_DESCRIPTION_PREFIXES,
    triggerDescriptionFailures,
  };
}

export function inspectLoomCoreBundle(options = {}) {
  const surfaces = surfaceOptions(options);
  const usingLoomReferences = readOrderedUsingLoomFiles(surfaces);
  const skills = readSkillFiles(surfaces);
  const agents = readAgentFiles(surfaces);
  const loomWeaverAgent = readLoomWeaverAgent(surfaces);
  const codexLoomWeaverAgent = readCodexLoomWeaverAgent(surfaces);
  const activation = inspectActivationDiscipline(surfaces);
  const bootstrap = getUsingLoomBootstrapContent(surfaces);

  return {
    usingLoom: {
      result: "injected into the first user message through experimental.chat.messages.transform as stripped using-Loom doctrine and ordered references",
      files: usingLoomReferences.map((reference) => reference.path),
    },
    bootstrap: {
      result: "cached first-user-message injection",
      marker: BOOTSTRAP_MARKER,
      hasContent: Boolean(bootstrap),
    },
    activation,
    skills: {
      result: "registered through config.skills.paths",
      path: directoryExists(join(surfaces.rootDir, "skills")) ? join(surfaces.rootDir, "skills") : undefined,
      items: skills,
    },
    agents: {
      result: "registered with OpenCode config.agent when available",
      path: directoryExists(join(surfaces.rootDir, "agents")) ? join(surfaces.rootDir, "agents") : undefined,
      items: agents.map((agent) => ({
        path: agent.path,
        name: agent.name,
        description: agent.description,
      })),
    },
    loomWeaver: {
      agentPath: loomWeaverAgent?.path,
      codexAgentPath: codexLoomWeaverAgent?.path,
      codexAgentHasDeveloperInstructions: Boolean(codexLoomWeaverAgent?.text.includes("developer_instructions")),
      codexAgentHasWriteBoundary: Boolean(codexLoomWeaverAgent?.text.includes("Write only inside `.loom/`")),
      codexAgentPromptMatchesAgent: Boolean(
        loomWeaverAgent && codexLoomWeaverAgent?.developerInstructions === loomWeaverAgent.content,
      ),
    },
  };
}

export const inspectLoomBundle = inspectLoomCoreBundle;

export async function server(_input = {}, options = {}) {
  return {
    config(config) {
      configureOpenCode(config, options || {});
    },
    "experimental.chat.messages.transform": async (_input, output) => {
      injectUsingLoomBootstrap(output, options || {});
    },
  };
}

export default {
  id: PLUGIN_ID,
  server,
};

if (process.argv[1] === fileURLToPath(import.meta.url) && process.argv.includes("--smoke")) {
  const inspection = inspectLoomCoreBundle();
  const config = configureOpenCode({});
  const loomWeaverConfig = config.agent?.["loom-weaver"];
  const codexLoomWeaverAgent = readCodexLoomWeaverAgent();
  const beforeSkillPathCount = config.skills?.paths?.length ?? 0;
  configureOpenCode(config);
  const plugin = await server({}, {});
  const transform = plugin["experimental.chat.messages.transform"];
  const output = { messages: [{ info: { role: "user" }, parts: [{ type: "text", text: "hello" }] }] };
  await transform({}, output);
  await transform({}, output);
  const bootstrapPartCount = output.messages[0].parts.filter(
    (part) => part.type === "text" && part.text.includes(BOOTSTRAP_MARKER),
  ).length;
  const ok = inspection.activation.ok
    && inspection.bootstrap.hasContent
    && bootstrapPartCount === 1
    && inspection.agents.items.some((agent) => agent.name === "loom-weaver")
    && codexLoomWeaverAgent?.text.includes('name = "loom-weaver"')
    && inspection.loomWeaver.codexAgentHasDeveloperInstructions
    && inspection.loomWeaver.codexAgentHasWriteBoundary
    && inspection.loomWeaver.codexAgentPromptMatchesAgent
    && loomWeaverConfig?.mode === "all"
    && Boolean(loomWeaverConfig?.prompt?.includes("Write only inside `.loom/`"));

  console.log(JSON.stringify({
    ok,
    pluginId: PLUGIN_ID,
    usingLoomFileCount: inspection.usingLoom.files.length,
    usingLoomFiles: inspection.usingLoom.files,
    firstUsingLoomFile: inspection.usingLoom.files[0],
    lastUsingLoomFile: inspection.usingLoom.files.at(-1),
    instructionCount: config.instructions?.length ?? 0,
    doesNotUseConfigInstructionsForBootstrap: (config.instructions?.length ?? 0) === 0,
    bootstrapInjectionPartCount: bootstrapPartCount,
    bootstrapInjectionIsDeduped: bootstrapPartCount === 1,
    skillCount: inspection.skills.items.length,
    skillPath: config.skills?.paths?.[0],
    skillPathsAreDeduped: (config.skills?.paths?.length ?? 0) === beforeSkillPathCount,
    agentCount: inspection.agents.items.length,
    agentNames: inspection.agents.items.map((agent) => agent.name),
    loomWeaverAgentPath: inspection.agents.items.find((agent) => agent.name === "loom-weaver")?.path,
    codexLoomWeaverAgentPath: inspection.loomWeaver.codexAgentPath,
    codexLoomWeaverHasDeveloperInstructions: inspection.loomWeaver.codexAgentHasDeveloperInstructions,
    codexLoomWeaverHasWriteBoundary: inspection.loomWeaver.codexAgentHasWriteBoundary,
    codexLoomWeaverPromptMatchesAgent: inspection.loomWeaver.codexAgentPromptMatchesAgent,
    loomWeaverOpenCodeMode: loomWeaverConfig?.mode,
    loomWeaverPromptHasWriteBoundary: Boolean(loomWeaverConfig?.prompt?.includes("Write only inside `.loom/`")),
    loomWeaverEditPermission: loomWeaverConfig?.permission?.edit,
    usingLoomResult: inspection.usingLoom.result,
    bootstrapResult: inspection.bootstrap.result,
    activationChecks: inspection.activation,
    skillsResult: inspection.skills.result,
    agentsResult: inspection.agents.result,
  }, null, 2));
  if (!ok) process.exitCode = 1;
}
