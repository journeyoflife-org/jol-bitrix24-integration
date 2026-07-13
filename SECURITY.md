# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes (current development) |

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

Email: **security@journeyoflife.org**

Include:
- Description of the vulnerability
- Steps to reproduce (no PII)
- Potential impact assessment

We will acknowledge receipt within **24 hours** and provide an initial
assessment within **72 hours**.

## Security Controls

This project implements the following security controls:

1. **OAuth token encryption at rest** — Fernet (AES-128-CBC)
2. **90-day automated token rotation** with audit trail
3. **HMAC-SHA256 webhook signature verification** — prevents forged callbacks
4. **PII-safe logging** — personal data is never written to logs
5. **Least-privilege API scopes** — only `crm` scope requested
6. **TLS verification** — all API traffic encrypted in transit
7. **Pre-commit hooks** — `detect-private-key` prevents accidental secret commits
8. **CodeQL analysis** — automated SAST on every PR
9. **Qodana analysis** — JetBrains static analysis on every PR

## Compliance

This integration processes personal data under GDPR. See:
- `compliance/dpa/bitrix24-dpa-status.md` — DPA status
- `compliance/gdpr/ropa-entry.md` — Records of Processing Activities
- `compliance/risk/risk-register.md` — Risk register
- `docs/incident-playbook.md` — Incident response playbook

## Incident Response

See `docs/incident-playbook.md` for the full incident response procedure.
