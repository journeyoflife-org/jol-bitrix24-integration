# Controls Matrix

> **⚠️ TEMPLATE — Maps security controls to audit requirements.**

## Technical Controls

| Control | Implementation | Test Evidence | Status |
|---------|---------------|---------------|--------|
| OAuth token encryption at rest | Fernet (AES-128-CBC) in `auth/oauth.py` | Unit tests | Implemented |
| 90-day token rotation | `auth/token_rotation.py` with `RotationPolicy` | Unit tests | Implemented |
| Webhook signature verification | HMAC-SHA256 in `webhooks/signature_verification.py` | Unit tests | Implemented |
| PII-safe logging | `logging/pii_safe_logging.py` filter | Security tests | Implemented |
| Least-privilege API scopes | Only `crm` scope in `clients/bitrix24_client.py` | Code review | Implemented |
| TLS verification | Configurable in `Bitrix24Client.__init__` | Unit tests | Implemented |
| Audit trail | Append-only JSON log in `logging/audit.py` | Integration tests | Implemented |
| Conflict resolution | Deterministic strategies in `sync/conflict_resolution.py` | Unit tests | Implemented |
| Retry with back-off | `sync/retry_queue.py` | Unit tests | Implemented |
| Pre-commit security checks | `detect-private-key` hook | CI pipeline | Implemented |

## Organisational Controls

| Control | Implementation | Status |
|---------|---------------|--------|
| DPA assessment | `compliance/dpa/bitrix24-dpa-status.md` | Pending legal review |
| DPIA | `docs/DPIA-template.md` | Pending DPO completion |
| ROPA entry | `compliance/gdpr/ropa-entry.md` | Pending DPO approval |
| Incident playbook | `docs/incident-playbook.md` | Draft |
| Access reviews | `compliance/audit/access-review-log.md` | Pending |
| Token rotation runbook | `docs/runbook-token-rotation.md` | Draft |
| Field mapping documentation | `docs/field-mapping.md` | Draft |
