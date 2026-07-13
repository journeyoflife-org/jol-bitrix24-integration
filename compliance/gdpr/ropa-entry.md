# Records of Processing Activities (ROPA)

> **⚠️ TEMPLATE — Must be completed per GDPR Art. 30 before production use.**

## Processing Activity: CRM Data Synchronisation

| Field | Value |
|-------|-------|
| **Controller** | Journey Of Life |
| **DPO** | [TO BE ASSIGNED] |
| **Purpose** | Synchronise contact, deal, and organisation data between JOL platform and Bitrix24 CRM |
| **Legal basis** | [TO BE DETERMINED] |
| **Data subjects** | Contacts at ~400,000 religious institutions across 27 EU countries |
| **Data categories** | Name, email, phone, address, organisational affiliation, deal/opportunity data |
| **Recipients** | Internal JOL teams (role-based access) |
| **International transfers** | None — all processing on JOL EU infrastructure |
| **Retention periods** | [TO BE DEFINED — e.g., active + 2 years after last interaction] |
| **Technical measures** | Encryption at rest, TLS in transit, PII-safe logging, audit trail |
| **Organisational measures** | RBAC, DPA review, DPIA, incident playbook |

## Processing Activity: Audit Logging

| Field | Value |
|-------|-------|
| **Purpose** | Compliance evidence collection for GDPR Art. 28 |
| **Data categories** | Event types, timestamps, entity IDs (no PII values) |
| **Retention** | 2 years |
| **Technical measures** | Append-only log, access restricted to compliance team |
