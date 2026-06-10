const PLUGIN_ID = "open-loom-core";

export function configureOpenCode(config) {
  return {
    ...config,
    name: config?.name || PLUGIN_ID,
  };
}

export function inspectLoomCoreBundle() {
  return {
    ok: true,
    result: "loom-zero core skeleton: no skills, agents, hooks, or doctrine surfaces are shipped",
    skills: [],
    agents: [],
  };
}

export const inspectLoomBundle = inspectLoomCoreBundle;

export async function server() {
  return inspectLoomCoreBundle();
}

export default {
  configureOpenCode,
  inspectLoomCoreBundle,
  inspectLoomBundle,
  server,
};

if (process.argv[1] && import.meta.url === new URL(process.argv[1], "file:").href && process.argv.includes("--smoke")) {
  console.log(JSON.stringify(inspectLoomCoreBundle(), null, 2));
}
