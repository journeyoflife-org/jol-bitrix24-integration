"""Structured audit logger for compliance evidence collection.

Writes immutable, append-only audit events to a dedicated log file.
These logs serve as evidence for GDPR Art. 28 / Art. 30 compliance
reviews and must never contain PII values.
"""

from __future__ import annotations

import json
import logging
import os
import stat
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class AuditLogger:
    """Append-only audit logger for compliance evidence.

    Each event is a single JSON line containing:
    * ``event_type``  — category (e.g. ``token_rotation``, ``sync_run``)
    * ``status``      — ``success`` or ``failure``
    * ``timestamp``   — ISO-8601 UTC
    * ``details``     — non-PII metadata only

    PII values (names, emails, phone numbers) are **never** written.
    """

    def __init__(self, log_path: str | Path) -> None:
        self._path = Path(log_path)
        self._ensure_log_directory()

    def log_event(
        self,
        event_type: str,
        status: str,
        timestamp: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Append a single audit event.

        Args:
            event_type: Category identifier (e.g. ``sync_run``, ``token_rotation``).
            status: ``"success"`` or ``"failure"``.
            timestamp: ISO-8601 string; defaults to current UTC time.
            details: Arbitrary metadata — must NOT contain PII.
        """
        if timestamp is None:
            timestamp = datetime.now(UTC).isoformat()

        record = {
            "event_type": event_type,
            "status": status,
            "timestamp": timestamp,
            "details": details or {},
        }

        try:
            with open(self._path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError:
            logger.exception("Failed to write audit event to %s", self._path)

    def read_events(
        self,
        event_type: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Read recent audit events, optionally filtered by type.

        Returns the most recent *limit* events in descending order.
        """
        if not self._path.exists():
            return []

        events: list[dict[str, Any]] = []
        with open(self._path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event_type and record.get("event_type") != event_type:
                    continue
                events.append(record)

        return events[-limit:]

    def _ensure_log_directory(self) -> None:
        """Create the parent directory for the audit log if it doesn't exist.

        Sets restrictive permissions (0o750 for directory, 0o640 for log file)
        to protect compliance evidence from unauthorised access.
        """
        self._path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(self._path.parent, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)
        except OSError:
            logger.debug("Could not set audit directory permissions on %s", self._path.parent)
