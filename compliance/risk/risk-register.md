# Risk Register

> **⚠️ TEMPLATE — Requires security team review.**

## Risk Register — JOL-Bitrix24 Integration

| ID | Risk | Likelihood | Impact | Risk Level | Mitigation | Owner |
|----|------|-----------|--------|------------|------------|-------|
| R-001 | OAuth token compromise | Low | High | Medium | 90-day rotation, Fernet encryption at rest, on-premise only | Engineering |
| R-002 | Forged webhook injection | Low | High | Medium | HMAC-SHA256 signature verification, replay protection | Engineering |
| R-003 | PII leakage via logs | Low | High | Medium | PII-safe filter, automated CI checks | Engineering |
| R-004 | Bitrix24 telemetry to Russia (1C-Bitrix) | Low | Critical | High | Disable telemetry, network egress controls | Infrastructure |
| R-005 | Sync data corruption | Low | Medium | Medium | Conflict resolution, audit trail, retry queue | Engineering |
| R-006 | Unauthorised internal access | Low | High | Medium | RBAC, access reviews, audit logging | Security |
| R-007 | DPA non-compliance | Very Low | High | Low | On-premise eliminates external processor; verify telemetry | Legal/DPO |
| R-008 | Token rotation failure | Medium | Medium | Medium | Automated alerts, manual runbook, 14-day warning | Engineering |

## Review Cadence

- Quarterly review by security team.
- Annual review by DPO.
- Ad-hoc review after any security incident.
