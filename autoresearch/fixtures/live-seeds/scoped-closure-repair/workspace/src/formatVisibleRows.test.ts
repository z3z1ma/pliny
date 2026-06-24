import { formatVisibleRows, formatVisibleRowsCsv } from "./formatVisibleRows";

describe("formatVisibleRows", () => {
  it("formats visible rows only", () => {
    expect(
      formatVisibleRows([
        { customerId: "cus_1", accountName: "Acme", status: "visible" },
        { customerId: "cus_2", accountName: "Hidden Co", status: "hidden" },
      ]),
    ).toBe("cus_1: Acme");
  });
});

describe("formatVisibleRowsCsv", () => {
  it("writes the expected CSV header and visible rows", () => {
    expect(
      formatVisibleRowsCsv([
        { customerId: "cus_1", accountName: "Acme", status: "visible" },
      ]),
    ).toBe("customer_id,account_name,status\ncus_1,Acme,visible");
  });

  it("excludes hidden rows", () => {
    expect(
      formatVisibleRowsCsv([
        { customerId: "cus_1", accountName: "Acme", status: "visible" },
        { customerId: "cus_2", accountName: "Hidden Co", status: "hidden" },
      ]),
    ).toBe("customer_id,account_name,status\ncus_1,Acme,visible");
  });
});
