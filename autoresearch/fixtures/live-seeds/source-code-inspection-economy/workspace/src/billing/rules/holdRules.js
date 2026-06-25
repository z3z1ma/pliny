export function isBlockedInvoice(invoice) {
  return Boolean(invoice.manualHold || invoice.disputeId);
}
