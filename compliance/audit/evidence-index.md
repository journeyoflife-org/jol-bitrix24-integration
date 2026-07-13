# Evidence Index

> **⚠️ TEMPLATE — Populated during development and operations.**

## Compliance Evidence Catalogue

| ID | Evidence | Location | Status |
|----|----------|----------|--------|
| E-001 | Field mapping documentation | `docs/field-mapping.md` | Draft |
| E-002 | Sync conflict resolution documentation | `docs/sync-conflict-resolution.md` | Draft |
| E-003 | Webhook security documentation | `docs/webhook-security.md` | Draft |
| E-004 | Token rotation runbook | `docs/runbook-token-rotation.md` | Draft |
| E-005 | Audit log samples | Generated at runtime | Pending |
| E-006 | PII-safe logging verification | `tests/security/test_pii_never_logged.py` | Implemented |
| E-007 | Signature verification tests | `tests/unit/test_signature_verification.py` | Implemented |
| E-008 | DPA status | `compliance/dpa/bitrix24-dpa-status.md` | Pending review |
| E-009 | DPIA | `docs/DPIA-template.md` | Pending completion |
| E-010 | Incident playbook | `docs/incident-playbook.md` | Draft |

## How to Use

This index is the single reference point for auditors. Each evidence item
links to the artefact that demonstrates the corresponding control.
