import { resolveInvoiceStatus } from "./invoiceStatus.js";

export function buildInvoiceStatusSummary(invoices, now = new Date()) {
  return invoices.map((invoice) => ({
    invoiceId: invoice.id,
    customerId: invoice.customerId,
    status: resolveInvoiceStatus(invoice, now)
  }));
}
