export type Invoice = {
  invoiceId: string;
  accountId: string;
  amountDueCents: number;
  status: "paid" | "failed";
  failureCode?: string;
  daysSinceLastAttempt: number;
};

export function listFailedInvoices(invoices: readonly Invoice[]): Invoice[] {
  return invoices.filter((invoice) => invoice.status === "failed");
}
