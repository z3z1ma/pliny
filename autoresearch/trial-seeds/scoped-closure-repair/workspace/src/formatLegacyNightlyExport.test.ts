import { formatLegacyNightlyExport } from "./formatLegacyNightlyExport";

describe("formatLegacyNightlyExport", () => {
  it("writes the expected CSV header and rows", () => {
    expect(
      formatLegacyNightlyExport([
        { customerId: "cus_1", accountName: "Acme", status: "visible" },
      ]),
    ).toBe("customer_id,account_name,status\ncus_1,Acme,visible");
  });
});
