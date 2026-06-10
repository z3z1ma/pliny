const PLUGIN_ID = "open-loom-playbooks";

export function configureOpenCode(config) {
  return {
    ...config,
    name: config?.name || PLUGIN_ID,
  };
}

export function readPlaybookMacroCatalog() {
  return [];
}

export function readSkillFiles() {
  return [];
}

export function readPlaybookCommands() {
  return [];
}

export function inspectLoomPlaybooksBundle() {
  return {
    ok: true,
    result: "loom-zero playbooks skeleton: no playbooks or generated commands are shipped",
    playbooks: [],
    commands: [],
  };
}

export const inspectLoomBundle = inspectLoomPlaybooksBundle;

export async function server() {
  return inspectLoomPlaybooksBundle();
}

export default {
  configureOpenCode,
  readPlaybookMacroCatalog,
  readSkillFiles,
  readPlaybookCommands,
  inspectLoomPlaybooksBundle,
  inspectLoomBundle,
  server,
};

if (process.argv[1] && import.meta.url === new URL(process.argv[1], "file:").href && process.argv.includes("--smoke")) {
  console.log(JSON.stringify(inspectLoomPlaybooksBundle(), null, 2));
}
