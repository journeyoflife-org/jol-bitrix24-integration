# Data Flow

> **Status:** TEMPLATE — requires review before production use.

## Sync Cycle (Bidirectional)

```
JOL Platform                    Integration Service              Bitrix24 On-Prem
    │                                  │                                │
    │──1. Fetch JOL records───────────▶│                                │
    │                                  │──2. Fetch Bitrix24 records────▶│
    │                                  │◀─3. Return records─────────────│
    │                                  │                                │
    │                                  │  4. Apply field mappings       │
    │                                  │  5. Detect conflicts           │
    │                                  │  6. Resolve conflicts          │
    │                                  │                                │
    │                                  │──7. Push updates──────────────▶│
    │◀─8. Push updates────────────────│                                │
    │                                  │                                │
    │                                  │  9. Audit log sync results     │
```

## Webhook Flow (Event-Driven)

```
Bitrix24 On-Prem                Integration Service              JOL Platform
    │                                  │                                │
    │──1. CRM event occurs────────────▶│                                │
    │  (signed with HMAC-SHA256)       │                                │
    │                                  │  2. Verify signature           │
    │                                  │  3. Validate event type        │
    │                                  │  4. Dispatch to handler        │
    │                                  │──5. Update JOL───────────────▶│
    │                                  │                                │
    │                                  │  6. Audit log event            │
```

## Data Residency

All data remains on JOL-controlled infrastructure within the EU:
- Bitrix24 Enterprise On-Premise VMs on Proxmox
- Integration service containers on same network segment
- PostgreSQL database on JOL infrastructure
- Audit logs stored locally with 2-year retention
