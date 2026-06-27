const visibleExceptions = [
  {
    id: "pex_001",
    accountName: "Northwind, Inc.",
    exceptionReason: "Expansion discount request",
    requestedDiscountPct: 18,
    status: "pending_review",
    arrImpactUsd: 240000,
    renewalDate: "2026-09-15"
  }
];

export function usePricingExceptions() {
  return {
    visibleExceptions
  };
}
