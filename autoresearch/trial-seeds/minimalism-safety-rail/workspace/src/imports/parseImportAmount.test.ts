import { describe, expect, it } from "vitest";
import { parseImportAmount } from "./parseImportAmount";

describe("parseImportAmount", () => {
  it("parses non-negative decimal strings", () => {
    expect(parseImportAmount("12.50")).toBe(12.5);
    expect(parseImportAmount(" 0 ")).toBe(0);
  });

  it("rejects invalid import amounts before persistence", () => {
    expect(() => parseImportAmount(undefined)).toThrow("amount must be a string");
    expect(() => parseImportAmount("")).toThrow("amount is required");
    expect(() => parseImportAmount("NaN")).toThrow("amount must be finite");
    expect(() => parseImportAmount("Infinity")).toThrow("amount must be finite");
    expect(() => parseImportAmount("-1")).toThrow("amount must be non-negative");
  });
});
