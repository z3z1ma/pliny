export function parseImportAmount(input: unknown): number {
  if (typeof input !== "string") {
    throw new TypeError("amount must be a string");
  }

  const trimmed = input.trim();
  if (trimmed.length === 0) {
    throw new TypeError("amount is required");
  }

  const amount = Number(trimmed);
  if (!Number.isFinite(amount)) {
    throw new TypeError("amount must be finite");
  }

  if (amount < 0) {
    throw new RangeError("amount must be non-negative");
  }

  return amount;
}
