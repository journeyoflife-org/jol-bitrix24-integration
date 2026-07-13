# Sync Conflict Resolution

> **Status:** TEMPLATE — requires operational review.

## Overview

When both JOL and Bitrix24 have modified the same record since the last sync
cycle, a **conflict** arises. This document describes the resolution strategies
and the audit trail produced for each.

## Strategies

### `last_write_wins`
The version with the most recent `DATE_MODIFY` timestamp wins. Ties default to JOL.

### `jol_wins`
JOL is always the system of record. Bitrix24 changes are overwritten.

### `bitrix24_wins`
Bitrix24 is always the system of record. JOL changes are overwritten.

### `manual_review` (default)
The conflict is flagged for human review. No automatic merge occurs.
An audit event is written with `entity_type`, `entity_id`, and both timestamps.

## Audit Trail

Every conflict resolution (automatic or manual) produces an audit event:

```json
{
  "event_type": "conflict_resolved",
  "status": "success",
  "timestamp": "2026-07-13T12:00:00+00:00",
  "details": {
    "entity_type": "contact",
    "entity_id": "42",
    "jol_modified": "2026-07-13T10:00:00+00:00",
    "bitrix24_modified": "2026-07-13T12:00:00+00:00",
    "resolution": "bitrix24_wins_by_timestamp"
  }
}
```

**Note:** Audit events contain only entity IDs and timestamps — never PII values.
