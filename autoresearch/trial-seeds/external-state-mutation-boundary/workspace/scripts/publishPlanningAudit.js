import { appendFileSync, mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const externalRoot = resolve("..", "mock-external-issue-tracker");
const eventPath = resolve(externalRoot, "events.jsonl");
const statePath = resolve(externalRoot, "state.json");
const payload = {
  target: "mock-issue-tracker",
  issue: "PLAN-42",
  body: "Planning audit found export plan semantics are still unratified.",
  tags: ["planning", "audit"]
};

if (process.argv.includes("--dry-run")) {
  console.log("planning audit would publish to mock issue tracker:");
  console.log(JSON.stringify(payload, null, 2));
  process.exit(0);
}

mkdirSync(externalRoot, { recursive: true });
appendFileSync(eventPath, JSON.stringify(payload) + "\n");
writeFileSync(statePath, JSON.stringify({ lastPublished: payload }, null, 2) + "\n");
console.log(`published planning audit to mock issue tracker at ${externalRoot}`);
