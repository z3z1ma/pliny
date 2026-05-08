---
name: loom-security
description: "Route security-sensitive work before implementation. Use when authentication, authorization, user input, secrets, sensitive data, uploads, webhooks, external integrations, dependency vulnerabilities, trust boundaries, or hardening need threat-aware evidence and critique."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-security

Security work fails when risk is treated as ordinary implementation detail.

This playbook coordinates threat-aware scoping, remediation, evidence, and review
without storing secrets or creating a second security ledger.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- security-sensitive intake and risk classification
- threat, reachability, and vulnerability triage
- safe handling of secrets and sensitive observations in Loom records
- remediation routing through specs, plans, tickets, evidence, and critique
- dependency and external-integration hardening posture

## What This Workflow Does Not Own

- secret values, credentials, tokens, private keys, or passwords
- durable policy or security principle changes; use constitution decisions
- intended security behavior; use specs
- live remediation state and accepted risk; use tickets
- observed scan or audit output; use evidence after sanitization
- final review verdicts; use critique

## Use This Skill When

- work touches authentication, authorization, sessions, permissions, or identity
- user input, uploads, webhooks, external callbacks, or external integrations are in scope
- secrets, sensitive data, privacy boundaries, logging, or error leakage matter
- dependency vulnerabilities, advisories, or hardening requests appear
- CORS, CSP, cookies, tokens, encryption, rate limits, or data exposure are discussed

## Do Not Use This Skill When

- the change has no plausible security or trust-boundary impact
- the only need is a final review of an already scoped diff; use critique
- secret handling requires incident response outside Loom; record only sanitized facts
- the request asks to weaken protections without explicit owner-approved rationale

## Default Procedure

1. Identify assets, actors, trust boundaries, data sensitivity, entry points, and
   existing security expectations before changing code or records.
2. Stop and ask or route outward when the work changes auth model, permissions,
   sensitive-data handling, upload policy, CORS/security headers, cryptography,
   secret exposure, or accepted risk.
3. For vulnerabilities, triage reachability, affected runtime path, severity,
   exploitability, dependency type, fix availability, and deferral risk.
4. Route threat analysis, tradeoffs, and rejected mitigations to research. Route
   intended security behavior to specs.
5. Use plans for multi-step remediation, staged rollout, migration, or compatibility
   work. Use tickets for bounded remediation and accepted-risk disposition.
6. Gather evidence from tests, scans, dependency output, configuration review,
   before/after observations, or reproduction steps. Sanitize before preserving.
7. Run critique with a security profile before closure for security-sensitive work,
   and disposition every medium/high finding in the ticket.
8. Promote durable hardening lessons to retrospective, wiki, research, spec, or
   constitution only when the owning layer should keep them.

## Handling Secrets

Never copy secret values into Loom records, tickets, evidence, packets, memory, or
examples. Record only sanitized facts such as "token exposure was observed" or
"credential rotation was required", plus non-sensitive provenance when useful.

Use the project's normal non-Loom secret-management and incident procedures for
the value itself.

## Common Rationalizations

- **Rationalization:** "This is just a small auth tweak."
  **Reality:** Auth, authorization, sessions, and permissions are security-sensitive even when the diff is small.
- **Rationalization:** "The scanner says low severity, so no ticket detail is needed."
  **Reality:** Reachability, runtime exposure, fix availability, and accepted risk still need ticket-owned disposition.
- **Rationalization:** "I need to paste the token to prove the issue."
  **Reality:** Loom records may capture the fact of exposure, not the secret value.
- **Rationalization:** "Security review can happen after merge."
  **Reality:** Security-sensitive work needs critique disposition before closure unless the ticket explicitly accepts the risk.

## Red Flags

- secret or sensitive personal data appears in Loom records or evidence
- external input is trusted because it came from a known integration
- auth or permission changes lack explicit intended behavior
- vulnerability deferral has no owner, review date, or accepted-risk rationale
- scan output is preserved without reachability or relevance analysis
- medium/high security findings are hidden in handoff prose instead of ticket dispositions

## Verification

- [ ] Assets, trust boundaries, data sensitivity, and entry points are explicit.
- [ ] Secrets are redacted or omitted from Loom artifacts.
- [ ] Intended security behavior is spec-owned when downstream work depends on it.
- [ ] Evidence supports the remediation, triage, or accepted-risk claim and is sanitized.
- [ ] Security critique and ticket-owned finding dispositions are closure-compatible.

## Done Means

- the security-sensitive scope is explicit and owner-routed
- remediation or accepted risk is ticket-owned
- evidence is sanitized and proportional to the claim
- critique disposition is complete enough for the risk class
- no Loom artifact became a secret store or shadow security ledger

## Read In This Order

Read immediately for security-sensitive work:

1. `references/security-hardening-checklist.md` for boundary tiers, vulnerability
   areas, dependency triage, secrets hygiene, and review checklist.
2. the core `loom-records` trust-boundary guidance when source material or evidence
   may contain sensitive data.
3. the core `loom-research` skill for threat analysis, vulnerability triage, and
   rejected mitigations.
4. the core `loom-specs` skill for intended auth, permission, validation, or data
   handling behavior.

Then read conditionally:

5. the core `loom-plans`, `loom-tickets`, and `loom-ralph` skills for remediation
   execution.
6. the core `loom-evidence` and `loom-critique` skills for sanitized proof and
   security review.
7. `skills/loom-migration/SKILL.md` when remediation requires replacement,
   deprecation, rollout, or removal.
