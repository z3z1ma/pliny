const assert = require("node:assert/strict");
const { test } = require("node:test");

const { previewBulkArchive } = require("./archivePreview");

test("returns inactive document ids only without mutating inputs", () => {
  const documents = [
    { id: "doc-active", status: "active" },
    { id: "doc-inactive", status: "inactive" },
    { id: "doc-archived", status: "archived" },
    { status: "inactive" },
  ];
  const snapshot = JSON.stringify(documents);

  assert.deepEqual(previewBulkArchive(documents), ["doc-inactive"]);
  assert.equal(JSON.stringify(documents), snapshot);
});
