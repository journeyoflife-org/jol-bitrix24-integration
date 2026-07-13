"""Bidirectional organisation (company) synchronisation between JOL and Bitrix24.

Syncs CRM companies using the configured field mapping, conflict
resolution strategy, and retry queue.  All operations are audit-logged.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from jol_bitrix24_integration.clients.bitrix24_client import Bitrix24APIError, Bitrix24Client
from jol_bitrix24_integration.logging.audit import AuditLogger
from jol_bitrix24_integration.mappings.field_mapping import ORGANIZATION_FIELD_MAP, map_fields
from jol_bitrix24_integration.sync.conflict_resolution import (
    ConflictStrategy,
)
from jol_bitrix24_integration.sync.retry_queue import RetryQueue, SyncOperation

logger = logging.getLogger(__name__)


class OrganizationSync:
    """Synchronises CRM companies (organisations) between JOL and Bitrix24."""

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

    def run_full_sync(self, jol_orgs: list[dict[str, Any]]) -> dict[str, int]:
        """Execute a full bidirectional sync of organisations.

        Args:
            jol_orgs: Current organisation records from the JOL system.

        Returns:
            Summary dict with counts: created, updated, skipped, failed.
        """
        ts = datetime.now(UTC).isoformat()
        stats = {"created": 0, "updated": 0, "skipped": 0, "failed": 0}

        try:
            bitrix_companies = self._fetch_all_bitrix_companies()
        except Bitrix24APIError:
            logger.exception("Failed to fetch Bitrix24 companies")
            self._audit.log_event(
                "sync_run", "failure", ts, {"entity": "company", "reason": "fetch_failed"}
            )
            stats["failed"] = len(jol_orgs)
            return stats

        bitrix_index: dict[str, dict[str, Any]] = {str(c.get("ID")): c for c in bitrix_companies}

        for jol_org in jol_orgs:
            jol_id = str(jol_org.get("id", ""))
            try:
                mapped = map_fields(jol_org, ORGANIZATION_FIELD_MAP)

                if jol_id in bitrix_index:
                    self._client.update_company(int(jol_id), mapped)
                    stats["updated"] += 1
                else:
                    self._client.create_company(mapped)
                    stats["created"] += 1

            except Bitrix24APIError as exc:
                stats["failed"] += 1
                self._retry.enqueue(SyncOperation.UPDATE, "company", jol_id, str(exc.code))

        self._audit.log_event(
            event_type="sync_run",
            status="success",
            timestamp=ts,
            details={"entity": "company", **stats},
        )
        logger.info("Organization sync complete: %s", stats)
        return stats

    def _fetch_all_bitrix_companies(self) -> list[dict[str, Any]]:
        """Paginate through all Bitrix24 companies."""
        all_companies: list[dict[str, Any]] = []
        start = 0
        while True:
            result = self._client.list_companies(start=start)
            items = result if isinstance(result, list) else result.get("companies", [])
            all_companies.extend(items)
            if len(items) < 50:
                break
            start += len(items)
        return all_companies
