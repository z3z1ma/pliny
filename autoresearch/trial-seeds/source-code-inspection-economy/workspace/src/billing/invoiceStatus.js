import { classifyAging } from "./rules/agingRules.js";
import { isBlockedInvoice } from "./rules/holdRules.js";

export const INVOICE_STATUS = {
  PAID: "paid",
  BLOCKED: "blocked",
  OVERDUE: "overdue",
  DUE_SOON: "due_soon",
  OPEN: "open"
};

export function resolveInvoiceStatus(invoice, now = new Date()) {
  if (invoice.paidAt) {
    return INVOICE_STATUS.PAID;
  }

  if (isBlockedInvoice(invoice)) {
    return INVOICE_STATUS.BLOCKED;
  }

  const aging = classifyAging(invoice, now);
  if (aging === "past_due") {
    return INVOICE_STATUS.OVERDUE;
  }

  if (aging === "due_soon") {
    return INVOICE_STATUS.DUE_SOON;
  }

  return INVOICE_STATUS.OPEN;
}
