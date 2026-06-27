function previewBulkArchive(documents) {
  return documents
    .filter((document) => document.status !== "archived")
    .map((document) => document.id);
}

module.exports = { previewBulkArchive };
