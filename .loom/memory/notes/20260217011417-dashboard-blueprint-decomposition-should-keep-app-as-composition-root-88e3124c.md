---
id: 20260217011417-dashboard-blueprint-decomposition-should-keep-app-as-composition-root-88e3124c
title: Dashboard blueprint decomposition should keep app as composition root
visibility: shared
status: active
created_at: "2026-02-17T01:14:17Z"
updated_at: "2026-02-17T01:14:17Z"
---

In Loom Dashboard, the top-level app module should stay focused on app creation, error mapping, and blueprint registration. Route handlers should live in dedicated blueprint modules so endpoint concerns stay isolated and testable while preserving stable API contracts.

Related: [[[[20260217011417-dashboard-blueprints-9f9cff96|dashboard blueprints]]]] [[[[20260217011417-composition-root-8aee8fd3|composition root]]]] [[[[20260217011417-api-stability-2540dd53|api stability]]]]
