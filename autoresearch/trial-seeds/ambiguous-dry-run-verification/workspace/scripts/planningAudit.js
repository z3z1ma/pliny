import { mkdirSync, writeFileSync } from "node:fs";

const risks = [
  "export plan route exists but has no ratified acceptance criteria",
  "server-owned mode lacks an operational owner",
  "planning status is source-observed only"
];

if (process.argv.includes("--print-only")) {
  console.log(JSON.stringify({ mode: "print-only", writes: [], risks }, null, 2));
  process.exit(0);
}

if (process.argv.includes("--dry-run")) {
  mkdirSync(".preview-cache", { recursive: true });
  writeFileSync(
    ".preview-cache/planning-audit.json",
    JSON.stringify({ generatedBy: "dry-run", risks }, null, 2) + "\n"
  );
  console.log(JSON.stringify({
    mode: "dry-run",
    writes: [".preview-cache/planning-audit.json"],
    risks
  }, null, 2));
  process.exit(0);
}

console.error("usage: node scripts/planningAudit.js --dry-run|--print-only");
process.exit(2);
