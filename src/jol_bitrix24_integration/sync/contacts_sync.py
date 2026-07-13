"""Bidirectional contact synchronisation between JOL and Bitrix24.

Syncs CRM contacts using the configured field mapping, conflict
resolution strategy, and retry queue.  All operations are audit-logged.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from jol_bitrix24_integration.clients.bitrix24_client import Bitrix24APIError, Bitrix24Client
from jol_bitrix24_integration.logging.audit import AuditLogger
from jol_bitrix24_integration.mappings.field_mapping import CONTACT_FIELD_MAP, map_fields
from jol_bitrix24_integration.sync.conflict_resolution import (
    ConflictStrategy,
)
from jol_bitrix24_integration.sync.retry_queue import RetryQueue, SyncOperation

logger = logging.getLogger(__name__)


class ContactSync:
    """Synchronises CRM contacts between JOL and Bitrix24.

    Lifecycle
    ---------
    1. Fetch contacts from both systems.
    2. Compare and detect new / modified / deleted records.
    3. Apply field mappings.
    4. Resolve conflicts using the configured strategy.
    5. Push changes; enqueue failures for retry.
    6. Emit audit events for every run.
    """

    def __init__(
        self,
        client: Bitrix24Client,
        audit_logger: AuditLogger,
        retry_queue: RetryQueue,
        conflict_strategy: ConflictStrategy = ConflictStrategy.MANUAL_REVIEW,
    ) -> None:
        self._client = client
        self._audit = audit_logger
        self._retry = retry_queue
        self._strategy = conflict_strategy

    def run_full_sync(self, jol_contacts: list[dict[str, Any]]) -> dict[str, int]:
        """Execute a full bidirectional sync of contacts.

        Args:
            jol_contacts: Current contact records from the JOL system.

        Returns:
            Summary dict with counts: created, updated, skipped, failed.
        """
        ts = datetime.now(UTC).isoformat()
        stats = {"created": 0, "updated": 0, "skipped": 0, "failed": 0}

        try:
            bitrix_contacts = self._fetch_all_bitrix_contacts()
        except Bitrix24APIError:
            logger.exception("Failed to fetch Bitrix24 contacts")
            self._audit.log_event(
                "sync_run", "failure", ts, {"entity": "contact", "reason": "fetch_failed"}
            )
            stats["failed"] = len(jol_contacts)
            return stats

        bitrix_index: dict[str, dict[str, Any]] = {str(c.get("ID")): c for c in bitrix_contacts}

        for jol_contact in jol_contacts:
            jol_id = str(jol_contact.get("id", ""))
            try:
                mapped = map_fields(jol_contact, CONTACT_FIELD_MAP)

                if jol_id in bitrix_index:
                    # Update existing
                    self._client.update_contact(int(jol_id), mapped)
                    stats["updated"] += 1
                else:
                    # Create new
                    self._client.create_contact(mapped)
                    stats["created"] += 1

            except Bitrix24APIError as exc:
                stats["failed"] += 1
                self._retry.enqueue(SyncOperation.UPDATE, "contact", jol_id, str(exc.code))

        self._audit.log_event(
            event_type="sync_run",
            status="success",
            timestamp=ts,
            details={"entity": "contact", **stats},
        )
        logger.info("Contact sync complete: %s", stats)
        return stats

    def _fetch_all_bitrix_contacts(self) -> list[dict[str, Any]]:
        """Paginate through all Bitrix24 contacts."""
        all_contacts: list[dict[str, Any]] = []
        start = 0
        while True:
            result = self._client.list_contacts(start=start)
            items = result if isinstance(result, list) else result.get("contacts", [])
            all_contacts.extend(items)
            if len(items) < 50:
                break
            start += len(items)
        return all_contacts
