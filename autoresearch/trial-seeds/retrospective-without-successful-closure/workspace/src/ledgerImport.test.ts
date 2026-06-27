import { previewLedgerImport } from "./ledgerImport";

describe("previewLedgerImport", () => {
  it("uses sourceRef and frozen posting dates in preview output", () => {
    expect(
      previewLedgerImport([
        { sourceRef: "bank-feed-001", amountCents: 1250, postedAt: "2026-01-15" },
      ]),
    ).toEqual(["bank-feed-001:1250:2026-01-15"]);
  });
});
