export type PricingException = {
  accountId: string;
  ownerEmail: string;
  exceptionType: string;
  amountCents: number;
  reason: string;
  status: "pending" | "approved" | "rejected";
};

export function listApprovedPricingExceptions(
  exceptions: PricingException[],
): PricingException[] {
  return exceptions.filter((exception) => exception.status === "approved");
}
