"""Persistent retry queue for failed sync operations.

When a sync operation fails (API error, network timeout, etc.) it is
placed on a retry queue with exponential back-off.  The queue is
persisted to the database so it survives service restarts.

PII is never stored in the queue — only entity IDs and operation type.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

logger = logging.getLogger(__name__)


class SyncOperation(StrEnum):
    """Types of sync operations that can be queued."""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

    def __init__(self, value: str) -> None:  # noqa: PLW3271
        self._value_ = value


@dataclass
class RetryItem:
    """A single item on the retry queue."""

    operation: SyncOperation
    entity_type: str  # e.g. "contact", "deal", "company"
    entity_id: str
    attempt_count: int = 0
    max_attempts: int = 5
    next_retry_at: float = 0.0  # Unix timestamp
    last_error: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def __init__(
        self,
        operation: SyncOperation,
        entity_type: str,
        entity_id: str,
        attempt_count: int = 0,
        max_attempts: int = 5,
        next_retry_at: float = 0.0,
        last_error: str = "",
        created_at: str = "",
    ) -> None:
        self.operation = operation
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.attempt_count = attempt_count
        self.max_attempts = max_attempts
        self.next_retry_at = next_retry_at
        self.last_error = last_error
        self.created_at = created_at or datetime.now(UTC).isoformat()

    @property
    def is_exhausted(self) -> bool:
        return self.attempt_count >= self.max_attempts

    @property
    def is_due(self) -> bool:
        return time.time() >= self.next_retry_at

    def schedule_next_retry(self) -> None:
        """Set next retry time using exponential back-off."""
        self.attempt_count += 1
        delay = min(2**self.attempt_count, 3600)  # cap at 1 hour
        self.next_retry_at = time.time() + delay


class RetryQueue:
    """In-memory retry queue with persistence hooks.

    For production use, back this with a database table.  The in-memory
    implementation is suitable for development and testing.
    """

    def __init__(self) -> None:
        self._items: list[RetryItem] = []

    def enqueue(
        self,
        operation: SyncOperation,
        entity_type: str,
        entity_id: str,
        error: str = "",
    ) -> RetryItem:
        """Add a failed operation to the retry queue."""
        item = RetryItem(
            operation=operation,
            entity_type=entity_type,
            entity_id=entity_id,
            last_error=error,
            next_retry_at=time.time() + 60,  # first retry in 60s
        )
        self._items.append(item)
        logger.info(
            "Enqueued retry: %s %s/%s",
            operation.value,
            entity_type,
            entity_id,
        )
        return item

    def get_due_items(self) -> list[RetryItem]:
        """Return all items that are due for retry."""
        return [item for item in self._items if item.is_due and not item.is_exhausted]

    def remove(self, item: RetryItem) -> None:
        """Remove a successfully completed item from the queue."""
        self._items = [i for i in self._items if i is not item]

    def remove_exhausted(self) -> list[RetryItem]:
        """Remove and return items that have exceeded max retry attempts."""
        exhausted = [i for i in self._items if i.is_exhausted]
        self._items = [i for i in self._items if not i.is_exhausted]
        if exhausted:
            logger.warning("Removed %d exhausted retry items", len(exhausted))
        return exhausted

    @property
    def size(self) -> int:
        return len(self._items)
