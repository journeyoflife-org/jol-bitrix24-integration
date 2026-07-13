# Data Retention Policy

> **⚠️ TEMPLATE — Requires legal review and DPO approval.**

## CRM Record Retention

| Data Category | Active Period | Archive Period | Deletion |
|--------------|--------------|----------------|----------|
| Contact records | Duration of relationship | 2 years post-relationship | Permanent deletion |
| Deal records | Duration of deal + 1 year | 2 years post-deal | Permanent deletion |
| Organisation records | Duration of relationship | 2 years post-relationship | Permanent deletion |

## Operational Data Retention

| Data Category | Retention | Deletion |
|--------------|-----------|----------|
| Audit logs | 2 years | Permanent deletion |
| Sync state (database) | Current state only | Overwritten on each cycle |
| Retry queue | Until resolved or max retries | Automatic purge |
| OAuth tokens | Until rotated (max 90 days) | Encrypted; overwritten |
| Application logs | 90 days | Automatic rotation |

## Deletion Process

1. Automated purge jobs run monthly.
2. Deletion events are audit-logged (entity_type + entity_id only).
3. Soft-delete → 30-day grace period → hard-delete.

## Data Subject Requests

- **Right to erasure (Art. 17):** Requests processed within 30 days.
- **Right to access (Art. 15):** Data export provided within 30 days.
- **Right to portability (Art. 20):** Machine-readable export within 30 days.

Process: [TO BE DOCUMENTED]
