import { omegaBillingBadge } from "./omegaBillingStatus";

describe("omegaBillingBadge", () => {
  it("labels paid invoices as settled", () => {
    expect(omegaBillingBadge({ id: "inv_1", status: "paid" })).toBe("Settled");
  });

  it("labels past due invoices as needing action", () => {
    expect(omegaBillingBadge({ id: "inv_2", status: "past_due" })).toBe(
      "Action needed",
    );
  });
});
