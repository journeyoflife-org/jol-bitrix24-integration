# Architecture

> **Deployment model:** Bitrix24 Enterprise On-Premise on JOL Proxmox infrastructure.

## System Overview

```
┌─────────────────────────────────────────────────────┐
│           JOL Proxmox Infrastructure (EU)           │
│                                                     │
│  ┌─────────────┐      ┌──────────────────────────┐ │
│  │  JOL Core   │─────▶│  jol-bitrix24-integration │ │
│  │  Platform   │◀─────│  (sync service)           │ │
│  └─────────────┘      └──────────┬───────────────┘ │
│                                   │ REST API        │
│                          ┌────────▼────────┐        │
│                          │   Bitrix24      │        │
│                          │  Enterprise     │        │
│                          │  On-Premise     │        │
│                          └─────────────────┘        │
└─────────────────────────────────────────────────────┘
```

## Components

| Component | Responsibility |
|-----------|---------------|
| `clients/bitrix24_client.py` | Bitrix24 REST API wrapper with TLS, retry, PII-safe logging |
| `auth/oauth.py` | OAuth2 authorization-code flow, token encryption at rest |
| `auth/token_rotation.py` | Automated 90-day token rotation with audit trail |
| `webhooks/handlers.py` | Webhook dispatcher with HMAC-SHA256 verification |
| `webhooks/signature_verification.py` | Signature validation for incoming callbacks |
| `sync/contacts_sync.py` | Bidirectional contact synchronisation |
| `sync/deals_sync.py` | Bidirectional deal synchronisation |
| `sync/organizations_sync.py` | Bidirectional company/organisation synchronisation |
| `sync/conflict_resolution.py` | Deterministic conflict resolution strategies |
| `sync/retry_queue.py` | Failed operation retry with exponential back-off |
| `mappings/field_mapping.py` | JOL ↔ Bitrix24 field translations |
| `mappings/country_mapping.py` | ISO 3166-1 ↔ Bitrix24 country names (EU-27) |
| `logging/audit.py` | Append-only audit log (compliance evidence) |
| `logging/pii_safe_logging.py` | PII redaction filter for application logs |

## Security Controls

1. **TLS verification** — all API traffic encrypted; internal CA support.
2. **OAuth tokens encrypted at rest** — Fernet (AES-128-CBC).
3. **Webhook signature verification** — HMAC-SHA256 on every callback.
4. **PII-safe logging** — no personal data in application or audit logs.
5. **Least-privilege scopes** — only `crm` scope requested.
6. **90-day token rotation** — automated with audit trail.
7. **On-premise infrastructure** — all data stays within JOL-controlled EU network.

## Data Flow

See [data-flow.md](data-flow.md) for detailed data flow diagrams.
