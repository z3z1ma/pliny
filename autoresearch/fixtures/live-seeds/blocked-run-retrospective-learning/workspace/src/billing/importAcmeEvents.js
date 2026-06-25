export function importAcmeEvents(events) {
  return events.map((event) => ({
    vendorEventId: event.vendorEventId,
    invoiceId: event.invoiceId,
    amountCents: event.amountCents
  }));
}
