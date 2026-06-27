const rows = [
  {
    customer_id: "cus_123",
    account_name: "Northwind, Inc.",
    exception_reason: "Enterprise renewal",
    requested_discount_pct: 18,
    status: "pending_review",
    requested_by: "maria@example.com",
    created_at: "2026-06-20"
  }
];

export function usePricingExceptions() {
  return {
    rows,
    visibleRows: rows,
    isLoading: false
  };
}
