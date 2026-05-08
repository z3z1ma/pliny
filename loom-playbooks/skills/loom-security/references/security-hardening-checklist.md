# Security Hardening Checklist

Use this reference when `loom-security` is active. It adapts concrete hardening
patterns into Loom routing: security facts still belong in specs, tickets,
evidence, critique, research, and constitution decisions.

## Boundary Tiers

### Always Do

- Validate external input at system boundaries: routes, form handlers, webhooks,
  uploads, environment loading, and third-party response parsing.
- Parameterize database queries. Never concatenate user input into SQL, NoSQL
  filters, shell commands, or filesystem paths.
- Encode or escape output. Do not bypass framework escaping for user content.
- Use HTTPS for external communication.
- Hash passwords with a current password-hashing algorithm such as bcrypt, scrypt,
  or argon2. Never store plaintext passwords.
- Use httpOnly, secure, sameSite cookies for sessions when cookie sessions are used.
- Configure security headers such as CSP, HSTS, X-Frame-Options, and
  X-Content-Type-Options when applicable.
- Run the project's dependency audit or security scan before release when a package
  ecosystem supports it.

### Ask First Or Route To Owner Records

Ask the operator or route to a spec/plan/ticket/constitution decision before:

- adding or changing authentication flows
- changing authorization, permissions, roles, or tenant boundaries
- storing new categories of sensitive data
- changing CORS, CSP, cookie, or rate-limit policy
- adding file uploads, webhooks, callbacks, or external service integrations
- changing encryption, token, or secret-management behavior
- accepting security risk or deferring a medium/high vulnerability

### Never Do In Loom Artifacts

- Never copy secrets, tokens, private keys, passwords, full payment data, or
  sensitive personal data into Loom records, packets, memory, examples, or evidence.
- Never log sensitive data as evidence.
- Never treat client-side validation as a security boundary.
- Never disable security headers for convenience without ticket-owned accepted risk.
- Never use `eval`, unsafe HTML insertion, or external script loading with
  untrusted data unless a spec and security critique explicitly justify it.
- Never expose stack traces or internal error details to users.

## Threat And Asset Questions

Before changing security-sensitive code, answer:

- What asset is protected: identity, money, PII, private content, availability,
  admin capability, integrity, or secrets?
- Who are the actors: anonymous user, authenticated user, admin, service account,
  webhook sender, browser page, dependency, or internal job?
- Where are the trust boundaries: browser to server, public API to internal code,
  app to database, app to third-party service, build system to package registry?
- What input crosses the boundary?
- What authorization decision is required after authentication?
- What failure should be visible to users, and what must stay internal?
- What evidence will show the mitigation works without exposing sensitive data?

## Common Vulnerability Areas

### Injection

Check for:

- SQL or NoSQL strings built from user input
- shell commands with unescaped input
- path traversal through filenames or archive contents
- template or expression evaluation with user content

Expected mitigation:

- parameterized queries, ORM safe APIs, allowlists, typed schemas, and path
  normalization with containment checks.

### Authentication

Check for:

- plaintext or weak password storage
- tokens without expiration
- session fixation or weak cookie flags
- password reset tokens that do not expire or can be reused
- missing rate limits on login or reset flows

Expected mitigation:

- strong password hashing, token expiry and rotation, httpOnly/secure/sameSite
  cookies, rate limiting, and audit evidence.

### Authorization

Check for:

- endpoints that check authentication but not ownership or permissions
- tenant ID or user ID accepted from the client as authority
- admin actions without role checks
- object lookup before permission filtering

Expected mitigation:

- server-side permission checks close to the protected resource, scoped queries,
  and tests for cross-user or cross-tenant access.

### Cross-Site Scripting

Check for:

- raw HTML rendering of user content
- unsafe markdown or rich text rendering
- third-party content inserted into the DOM
- weak CSP or unsafe inline scripts

Expected mitigation:

- framework escaping, sanitization when HTML is required, safe markdown pipeline,
  and CSP appropriate to the app.

### Sensitive Data Exposure

Check for:

- password hashes, reset tokens, API tokens, internal flags, or PII returned in API responses
- sensitive data in logs, analytics, crash reports, evidence, screenshots, or test fixtures
- overly broad export or admin endpoints

Expected mitigation:

- response shaping, redaction, least-privilege data access, and sanitized evidence.

### Security Misconfiguration

Check for:

- wildcard CORS origins with credentials
- missing security headers
- debug routes or stack traces in production
- default credentials
- overly broad storage bucket or file permissions

Expected mitigation:

- environment-aware config, strict defaults, deploy checks, and release evidence.

## Input Validation Patterns

Validate at the boundary, then let internal code trust the validated type or shape.

Boundary validation should name:

- required and optional fields
- minimum and maximum lengths
- enum values
- default values
- date/time format and timezone assumptions
- numeric ranges
- file size and allowed content types
- reject/strip behavior for unknown fields

Third-party API responses are external input. Validate them before use in logic,
rendering, storage, or agent decision-making.

## Dependency Vulnerability Triage

For each advisory or audit finding, record:

- severity and confidence
- affected package and version
- runtime dependency or dev-only dependency
- reachable production path or not reachable
- exploit preconditions in this deployment
- fixed version or workaround availability
- replacement feasibility if no fix exists
- owner, target date, review date, or accepted-risk rationale

Decision shape:

- critical/high and reachable: fix immediately or block release.
- critical/high but not reachable: fix soon, document why not blocking.
- moderate and production-reachable: fix in the next release cycle.
- dev-only or low risk: track with owner and review date.

No vulnerability should be deferred with only "low risk" prose. The ticket owns
the risk disposition.

## File Upload Safety

For upload handlers, check:

- allowlisted MIME types and extensions
- maximum size
- storage path containment
- antivirus or scanning requirement when applicable
- magic-byte validation when the file type matters
- no direct serving of untrusted files without safe content type and disposition
- authentication and authorization around upload and download

## Rate Limiting And Abuse

Consider rate limits for:

- login, password reset, magic link, invite, and token exchange
- public search or expensive endpoints
- file upload and export
- webhook replay and external callbacks
- admin or destructive actions

Record limits and exceptions in specs or tickets when behavior matters to users.

## Secrets Management

Expected project hygiene:

- real `.env` files are ignored
- `.env.example` contains placeholders only
- private keys, certificates, and local secrets are ignored
- commits and staged diffs are checked when secret exposure risk exists
- rotation is handled by the project's secret-management process, not Loom

Loom may record sanitized facts: exposure observed, rotation required, rotation
completed, or value intentionally omitted. It must not store the value.

## Security Review Checklist

Authentication:

- passwords hashed with a modern algorithm and appropriate cost
- tokens expire and rotate where required
- session cookies are httpOnly, secure, and sameSite when applicable
- auth endpoints have rate limits

Authorization:

- every protected endpoint checks permissions
- users can access only their resources or authorized tenants
- admin actions require admin verification
- object lookup and permission filtering cannot be bypassed

Input and output:

- user input validated at boundaries
- database queries parameterized
- output encoded or sanitized
- file uploads restricted and contained

Data:

- no secrets in source, records, logs, evidence, or responses
- sensitive fields excluded from public API responses
- PII handling is explicit where applicable

Infrastructure:

- security headers configured where applicable
- CORS restricted to known origins
- dependencies audited and triaged
- error responses hide internals

## Evidence To Preserve

Good security evidence can include:

- sanitized scan or audit output
- focused test proving unauthorized access is denied
- before/after configuration diff
- dependency audit plus triage notes
- redacted log excerpt showing attempted exploit blocked
- browser/network observation proving headers or cookie flags

Do not preserve raw secrets, full tokens, private customer data, or unredacted PII.
