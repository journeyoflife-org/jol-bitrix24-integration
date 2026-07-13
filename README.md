# jol-bitrix24-integration

Integration layer between Journey Of Life and Bitrix24 CRM, enabling secure, GDPR-compliant bidirectional synchronisation of contacts, organisations, and deals at scale.

## Deployment Model

**Bitrix24 Enterprise On-Premise** running on JOL's own Proxmox infrastructure.
All data stays within JOL-controlled EU infrastructure — no third-country transfers.

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full system overview.

```
JOL Platform ←→ jol-bitrix24-integration ←→ Bitrix24 Enterprise (On-Premise)
```

## Security Controls

| Control | Implementation |
|---------|---------------|
| OAuth token encryption | Fernet (AES-128-CBC) at rest |
| Token rotation | Automated every 90 days |
| Webhook verification | HMAC-SHA256 signature on every callback |
| PII-safe logging | No personal data in application or audit logs |
| Least-privilege scopes | Only `crm` scope requested |
| TLS verification | Configurable; supports internal CA bundles |
| Audit trail | Append-only JSON audit log |

## Quick Start

```bash
# Clone
git clone https://github.com/journeyoflife-org/jol-bitrix24-integration.git
cd jol-bitrix24-integration

# Setup
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# Edit .env with your Bitrix24 Enterprise On-Premise credentials

# Run
python -m jol_bitrix24_integration.app

# Test
pytest
```

## Project Structure

```
src/jol_bitrix24_integration/
├── app.py                    # Application entry point
├── config.py                 # Centralised settings
├── clients/                  # Bitrix24 REST API client
├── auth/                     # OAuth2 flow + token rotation
├── webhooks/                 # Webhook dispatch + signature verification
├── sync/                     # Bidirectional sync engine (contacts, deals, organisations)
├── mappings/                 # Field + country mappings
├── logging/                  # Audit logger + PII-safe filter
└── schemas/                  # JSON schemas for validation
```

## Compliance

This project embeds GDPR compliance controls directly into the codebase:

- `compliance/` — DPA status, ROPA, retention policy, risk register (templates requiring legal review)
- `docs/DPIA-template.md` — Data Protection Impact Assessment template
- `docs/field-mapping.md` — Field mapping as GDPR Art. 30 evidence
- `scripts/pii-log-check.sh` — Automated PII leak detection in logs

> **⚠️ All compliance documents are templates. They require review and approval by your DPO before production use.**

## Licence

Apache License 2.0 — see [LICENSE](LICENSE).
