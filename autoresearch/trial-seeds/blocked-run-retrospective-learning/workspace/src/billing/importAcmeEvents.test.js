import { importAcmeEvents } from "./importAcmeEvents.js";

it("preserves vendor event identifiers", () => {
  expect(
    importAcmeEvents([
      { vendorEventId: "evt_acme_001", invoiceId: "inv_001", amountCents: 1200 }
    ])
  ).toEqual([
    { vendorEventId: "evt_acme_001", invoiceId: "inv_001", amountCents: 1200 }
  ]);
});
