Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Vendor Tax Export Privacy Minimization

## Context

Privacy reviewed the vendor tax export after the active specification was
written. The active specification still asks for full `taxId`, while the
current source and tests now export only `taxLast4`.

The review was documented as a decision but did not explicitly supersede
`.10x/specs/vendor-tax-export.md`.

## Decision

Vendor tax export artifacts must not expose full `taxId` until Finance and
Privacy reconcile the active specification with the privacy decision.

Current implementation work may preserve `taxLast4` as the source-observed
privacy-minimized behavior, but no executable ticket may declare the export
production-ready while the active spec still requires full `taxId`.

## Alternatives Considered

- Keep full `taxId`: rejected by Privacy as overexposure unless Finance provides
  a narrower transfer and retention control.
- Treat `taxLast4` source behavior as automatically superseding the spec:
  rejected because the active specification was not moved to superseded or
  replaced.
- Delete the tax identifier from the export entirely: rejected because Finance
  still needs some reconciliation key.

## Consequences

The next safe work item is a record reconciliation owner that resolves the
active spec/decision conflict. Do not edit source/tests or open an executable
implementation ticket until the active record set has one coherent authority.
