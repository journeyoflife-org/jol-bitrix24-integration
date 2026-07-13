"""Conflict resolution strategies for bidirectional sync.

When both JOL and Bitrix24 have modified the same record since the
last sync, a conflict arises.  This module provides deterministic,
auditable resolution strategies.

Strategies
----------
* ``last_write_wins`` — most recent ``DATE_MODIFY`` wins.
* ``jol_wins``        — JOL is the system of record.
* ``bitrix24_wins``   — Bitrix24 is the system of record.
* ``manual_review``   — flag for human review; no automatic merge.

All resolutions are audit-logged for data integrity evidence.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

logger = logging.getLogger(__name__)


class ConflictStrategy(StrEnum):
    """Supported conflict resolution strategies."""

    LAST_WRITE_WINS = "last_write_wins"
    JOL_WINS = "jol_wins"
    BITRIX24_WINS = "bitrix24_wins"
    MANUAL_REVIEW = "manual_review"


class ConflictRecord:
    """Represents a detected conflict between JOL and Bitrix24 versions of a record."""

    def __init__(
        self,
        entity_type: str,
        entity_id: str,
        jol_version: dict[str, Any],
        bitrix24_version: dict[str, Any],
        jol_modified: datetime,
        bitrix24_modified: datetime,
    ) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.jol_version = jol_version
        self.bitrix24_version = bitrix24_version
        self.jol_modified = jol_modified
        self.bitrix24_modified = bitrix24_modified
        self.resolved = False
        self.resolution: str | None = None
        self.resolved_at: datetime | None = None

    def to_audit_dict(self) -> dict[str, Any]:
        """Return a PII-safe summary for audit logging."""
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "jol_modified": self.jol_modified.isoformat(),
            "bitrix24_modified": self.bitrix24_modified.isoformat(),
            "resolved": self.resolved,
            "resolution": self.resolution,
        }


def resolve_conflict(
    conflict: ConflictRecord,
    strategy: ConflictStrategy,
) -> dict[str, Any] | None:
    """Apply the chosen strategy and return the winning version.

    Returns
    -------
    dict or None
        The winning record version, or ``None`` for ``manual_review``.
    """
    if strategy == ConflictStrategy.LAST_WRITE_WINS:
        if conflict.jol_modified >= conflict.bitrix24_modified:
            winner = conflict.jol_version
            conflict.resolution = "jol_wins_by_timestamp"
        else:
            winner = conflict.bitrix24_version
            conflict.resolution = "bitrix24_wins_by_timestamp"

    elif strategy == ConflictStrategy.JOL_WINS:
        winner = conflict.jol_version
        conflict.resolution = "jol_wins_policy"

    elif strategy == ConflictStrategy.BITRIX24_WINS:
        winner = conflict.bitrix24_version
        conflict.resolution = "bitrix24_wins_policy"

    elif strategy == ConflictStrategy.MANUAL_REVIEW:
        conflict.resolution = None
        logger.info(
            "Conflict flagged for manual review: %s/%s",
            conflict.entity_type,
            conflict.entity_id,
        )
        return None

    else:
        raise ValueError(f"Unknown conflict strategy: {strategy}")

    conflict.resolved = True
    conflict.resolved_at = datetime.now(UTC)
    return winner
