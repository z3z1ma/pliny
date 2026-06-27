function createStockAdjustmentRequest({
  sku,
  targetAvailableQuantity,
  cycleCountRef,
  reason,
  expedite = false,
}) {
  if (!sku) {
    throw new Error("sku is required");
  }
  if (!cycleCountRef) {
    return {
      status: "incomplete",
      blocker: "cycleCountRef required before availability changes",
      sku,
      targetAvailableQuantity,
      reason,
      expedite,
    };
  }
  return {
    status: expedite ? "urgent-review" : "queued",
    sku,
    targetAvailableQuantity,
    cycleCountRef,
    reason,
    expedite,
  };
}

module.exports = { createStockAdjustmentRequest };
