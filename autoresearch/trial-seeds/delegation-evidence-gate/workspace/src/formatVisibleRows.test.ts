import { formatVisibleRows } from "./formatVisibleRows";

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
