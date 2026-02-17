---
id: 20260217014327-render-hotspot-splits-should-preserve-stable-import-seams-c17b2fc7
title: Render hotspot splits should preserve stable import seams
visibility: shared
status: active
created_at: "2026-02-17T01:43:27Z"
updated_at: "2026-02-17T01:43:27Z"
---

When decomposing large text-rendering modules in Loom Workspace, keep the public render module as a stable shim and move heavy implementation into a dedicated module. This preserves call-site contracts while enabling focused evolution of renderer logic and guardrail tracking.

Related: [[[[20260217014327-workspace-render-9e742bde|workspace render]]]] [[[[20260217014327-stable-seams-ad413357|stable seams]]]] [[[[20260217014327-hotspot-decomposition-f86be33a|hotspot decomposition]]]]
