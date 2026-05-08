import { readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PACKAGE_ROOT = dirname(fileURLToPath(import.meta.url));
const PLUGIN_ID = "open-loom-playbooks";

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

function pushUnique(array, value) {
  if (!array.includes(value)) array.push(value);
}

function surfaceOptions(options = {}) {
  return {
    rootDir: resolve(String(options.rootDir || PACKAGE_ROOT)),
    skills: options.skills !== false,
  };
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

  return config;
}

export function inspectLoomPlaybooksBundle(options = {}) {
  const surfaces = surfaceOptions(options);
  const skills = readSkillFiles(surfaces);

  return {
    usingLoom: {
      result: "not registered by this playbook package",
      files: [],
    },
    skills: {
      result: "registered through config.skills.paths",
      path: directoryExists(join(surfaces.rootDir, "skills")) ? join(surfaces.rootDir, "skills") : undefined,
      items: skills,
    },
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

if (process.argv[1] === fileURLToPath(import.meta.url) && process.argv.includes("--smoke")) {
  const inspection = inspectLoomPlaybooksBundle();
  const config = configureOpenCode({});
  const beforeSkillPathCount = config.skills?.paths?.length ?? 0;
  configureOpenCode(config);

  console.log(JSON.stringify({
    ok: true,
    pluginId: PLUGIN_ID,
    usingLoomReferenceCount: inspection.usingLoom.files.length,
    instructionCount: config.instructions?.length ?? 0,
    doesNotPreloadCoreDoctrine: (config.instructions?.length ?? 0) === 0,
    skillCount: inspection.skills.items.length,
    skillPath: config.skills?.paths?.[0],
    skillPathsAreDeduped: (config.skills?.paths?.length ?? 0) === beforeSkillPathCount,
    usingLoomResult: inspection.usingLoom.result,
    skillsResult: inspection.skills.result,
  }, null, 2));
}
