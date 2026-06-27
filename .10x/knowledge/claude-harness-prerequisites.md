Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Claude Harness Prerequisites

## Context

Claude-backed autoresearch runs may depend on the operator's work-paid Claude
access and associated AWS SSO state.

## Convention

Before running Claude Code as a FULL harness target, confirm that the required
AWS SSO session is active. If it is not active, run the appropriate `aws sso
login` command for the operator's environment before invoking Claude.

The exact AWS profile/account is not yet specified in project records. Future
Claude runner work should fail with a clear prerequisite error rather than
recording credentials, guessing a profile, or embedding sensitive values.

## Related Context

- `.10x/specs/10x-autoresearch-loop.md`
- `.10x/decisions/autoresearch-live-trial-scientist-inspection.md`
