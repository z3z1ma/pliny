import { mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PACKAGE_ROOT = dirname(fileURLToPath(import.meta.url));
const PLUGIN_ID = "open-loom-playbooks";

const PLAYBOOK_MACRO_PREAMBLE = `The user explicitly invoked this Loom Playbook as an optional workflow macro.

Use it as a workflow lens only after Core Loom routing has identified the owning surface or after the operator has deliberately selected this lens. Preserve Core surface ownership, ticket shaping, evidence, audit, and ticket-owned Ralph worker/review discipline. Do not treat this Playbook as automatic first-action activation from ordinary natural-language task text.`;

function posixPath(path) {
  return path.split("\\").join("/");
}

function directoryExists(directory) {
  return statSync(directory, { throwIfNoEntry: false })?.isDirectory() === true;
}

function fileExists(file) {
  return statSync(file, { throwIfNoEntry: false })?.isFile() === true;
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

function surfaceOptions(options = {}) {
  return {
    rootDir: resolve(String(options.rootDir || PACKAGE_ROOT)),
  };
}

function readSkillDocuments(options = {}) {
  const { rootDir } = surfaceOptions(options);
  const skillRoot = join(rootDir, "playbooks");
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
        content: md.content,
      };
    });
}

export function readSkillFiles(options = {}) {
  return readSkillDocuments(options).map(({ content: _content, ...skill }) => skill);
}

function macroDescription(skill) {
  return skill.description;
}

function macroBody(skill) {
  return `${PLAYBOOK_MACRO_PREAMBLE}\n\n${skill.content}`;
}

export function readPlaybookMacroCatalog(options = {}) {
  return readSkillDocuments(options).map((skill) => ({
    name: skill.name,
    source: skill.path,
    description: macroDescription(skill),
    body: macroBody(skill),
  }));
}

export function readPlaybookCommands(options = {}) {
  return Object.fromEntries(readPlaybookMacroCatalog(options).map((macro) => [macro.name, {
    description: macro.description,
    template: macro.body,
  }]));
}

function tomlMultilineLiteralString(value) {
  if (value.includes("'''")) {
    throw new Error("Gemini command TOML literal strings cannot contain triple single quotes.");
  }

  return `'''\n${value}\n'''`;
}

export function toGeminiCommandToml(macro) {
  return `description = ${JSON.stringify(macro.description)}\nprompt = ${tomlMultilineLiteralString(macro.body)}\n`;
}

export function writeGeminiCommandFiles(options = {}) {
  const surfaces = surfaceOptions(options);
  const commandRoot = join(surfaces.rootDir, "commands");
  mkdirSync(commandRoot, { recursive: true });

  return readPlaybookMacroCatalog(surfaces).map((macro) => {
    const path = join(commandRoot, `${macro.name}.toml`);
    writeFileSync(path, toGeminiCommandToml(macro), "utf8");
    return posixPath(relative(surfaces.rootDir, path));
  });
}

export function configureOpenCode(config, options = {}) {
  const surfaces = surfaceOptions(options);
  const commands = readPlaybookCommands(surfaces);

  if (Object.keys(commands).length > 0) {
    config.command ??= {};
    for (const [name, command] of Object.entries(commands)) {
      config.command[name] ??= command;
    }
  }

  return config;
}

export function inspectPlaybookMacroCatalog(options = {}) {
  const skills = readSkillFiles(options);
  const macros = readPlaybookMacroCatalog(options);
  const missingMacros = skills
    .filter((skill) => !macros.some((macro) => macro.name === skill.name && macro.source === skill.path))
    .map((skill) => skill.name);
  const explicitDescriptionPrefixFailures = macros
    .filter((macro) => macro.description.includes("Explicit optional workflow macro for"))
    .map((macro) => ({ name: macro.name, description: macro.description }));

  return {
    ok: missingMacros.length === 0 && explicitDescriptionPrefixFailures.length === 0,
    result: "derived from skills as explicit optional workflow macros",
    count: macros.length,
    items: macros.map((macro) => ({
      name: macro.name,
      source: macro.source,
      description: macro.description,
    })),
    missingMacros,
    explicitDescriptionPrefixFailures,
  };
}

export function inspectLoomPlaybooksBundle(options = {}) {
  const surfaces = surfaceOptions(options);
  const skills = readSkillFiles(surfaces);
  const macros = inspectPlaybookMacroCatalog(surfaces);
  const config = configureOpenCode({}, surfaces);
  const commands = config.command ?? {};
  const skillRoot = join(surfaces.rootDir, "playbooks");
  const playbookSkillPaths = (config.skills?.paths ?? []).filter((skillPath) => resolve(skillPath) === skillRoot);
  const missingCommands = readPlaybookMacroCatalog(surfaces)
    .filter((macro) => commands[macro.name]?.template !== macro.body || commands[macro.name]?.description !== macro.description)
    .map((macro) => macro.name);

  return {
    usingLoom: {
      result: "not registered by this playbook package",
      files: [],
    },
    skills: {
      result: "source corpus only; not registered through config.skills.paths",
      registeredPlaybookSkillPaths: playbookSkillPaths,
      items: skills,
    },
    commands: {
      ok: missingCommands.length === 0 && playbookSkillPaths.length === 0,
      result: "registered through config.command from explicit macro catalog",
      count: Object.keys(commands).length,
      items: Object.entries(commands).map(([name, command]) => ({
        name,
        description: command.description,
        hasTemplate: typeof command.template === "string" && command.template.length > 0,
      })),
      missingCommands,
      registeredPlaybookSkillPaths: playbookSkillPaths,
    },
    macros,
  };
}

export const inspectLoomBundle = inspectLoomPlaybooksBundle;

export async function server(_input = {}, options = {}) {
  return {
    config(config) {
      configureOpenCode(config, options || {});
    },
  };
}

export default {
  id: PLUGIN_ID,
  server,
};

if (process.argv[1] === fileURLToPath(import.meta.url) && process.argv.includes("--write-gemini-commands")) {
  const written = writeGeminiCommandFiles();
  console.log(JSON.stringify({ written: written.length, files: written }, null, 2));
} else if (process.argv[1] === fileURLToPath(import.meta.url) && process.argv.includes("--smoke")) {
  const inspection = inspectLoomPlaybooksBundle();
  const config = configureOpenCode({});
  const beforeCommandCount = Object.keys(config.command ?? {}).length;
  configureOpenCode(config);
  const ok = inspection.commands.ok && inspection.macros.ok;

  console.log(JSON.stringify({
    ok,
    pluginId: PLUGIN_ID,
    usingLoomReferenceCount: inspection.usingLoom.files.length,
    instructionCount: config.instructions?.length ?? 0,
    doesNotPreloadCoreDoctrine: (config.instructions?.length ?? 0) === 0,
    skillCount: inspection.skills.items.length,
    commandCount: inspection.commands.count,
    commandRegistrationResult: inspection.commands.result,
    commandChecks: {
      ok: inspection.commands.ok,
      missingCommands: inspection.commands.missingCommands,
      registeredPlaybookSkillPaths: inspection.commands.registeredPlaybookSkillPaths,
    },
    commandEntriesAreDeduped: Object.keys(config.command ?? {}).length === beforeCommandCount,
    macroCount: inspection.macros.count,
    macrosResult: inspection.macros.result,
    macroChecks: {
      ok: inspection.macros.ok,
      missingMacros: inspection.macros.missingMacros,
      explicitDescriptionPrefixFailures: inspection.macros.explicitDescriptionPrefixFailures,
    },
    registeredPlaybookSkillPaths: inspection.skills.registeredPlaybookSkillPaths,
    playbookSkillPathsRegistered: inspection.skills.registeredPlaybookSkillPaths.length > 0,
    usingLoomResult: inspection.usingLoom.result,
    skillsResult: inspection.skills.result,
  }, null, 2));
  if (!ok) process.exitCode = 1;
}
