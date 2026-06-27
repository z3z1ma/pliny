export type OmegaInvoice = {
  id: string;
  status: "paid" | "past_due" | "disputed";
};

export function omegaBillingBadge(invoice: OmegaInvoice): string {
  if (invoice.status === "paid") return "Settled";
  if (invoice.status === "past_due") return "Action needed";
  return "Under review";
}
