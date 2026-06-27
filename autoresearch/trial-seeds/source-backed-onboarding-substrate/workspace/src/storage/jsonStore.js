import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname } from "node:path";

export const defaultStatePath = "data/onboarding-state.json";

export async function readState(path = defaultStatePath) {
  try {
    return JSON.parse(await readFile(path, "utf8"));
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
    return { invites: [], members: [], audit: [], outbox: [] };
  }
}

export async function writeState(state, path = defaultStatePath) {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, JSON.stringify(state, null, 2) + "\n", "utf8");
}
