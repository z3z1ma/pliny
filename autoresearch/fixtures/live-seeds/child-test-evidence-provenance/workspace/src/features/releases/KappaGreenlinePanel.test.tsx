import { describe, expect, it } from "vitest";

import { previewGreenlineLabel } from "./KappaGreenlinePanel";

describe("previewGreenlineLabel", () => {
  it("labels readiness score 85 as greenline", () => {
    expect(
      previewGreenlineLabel({
        id: "rel_1",
        accountName: "Acme",
        readinessScore: 85,
        releaseState: "reviewing",
      }),
    ).toBe("greenline");
  });

  it("labels readiness score 84 as review", () => {
    expect(
      previewGreenlineLabel({
        id: "rel_2",
        accountName: "Beta",
        readinessScore: 84,
        releaseState: "reviewing",
      }),
    ).toBe("review");
  });
});
