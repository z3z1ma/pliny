import { mkdirSync, writeFileSync } from "node:fs";

if (process.argv.includes("--dry-run")) {
  console.log(JSON.stringify({
    mode: "dry-run",
    writes: [],
    risks: [
      "export plan route exists but has no ratified acceptance criteria",
      "server-owned mode lacks an operational owner",
      "planning status is source-observed only"
    ]
  }, null, 2));
  process.exit(0);
}

mkdirSync("reports", { recursive: true });
writeFileSync(
  "reports/planning-audit.md",
  "generated planning audit: route exists but semantics are unratified\n"
);
console.log("planning audit wrote reports/planning-audit.md");
