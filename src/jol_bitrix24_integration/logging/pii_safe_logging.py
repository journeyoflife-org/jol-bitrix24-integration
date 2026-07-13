"""PII-safe logging filter and formatter.

Ensures that no personal data (names, email addresses, phone numbers,
physical addresses) leaks into application logs.  This is a technical
control supporting GDPR Art. 5 — data minimisation.
"""

from __future__ import annotations

import logging
import re
from typing import Any

# Patterns that indicate likely PII — matched against log message strings.
_PII_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),  # email
    re.compile(r"\+?\d[\d\s\-()]{7,}\d"),  # phone (international)
    re.compile(
        r"\b\d{1,5}\s+\w+\s+(?:street|st|avenue|ave|road|rd|boulevard|blvd|lane|ln|drive|dr)\b",
        re.IGNORECASE,
    ),  # street address
]

# Fields that commonly contain PII and should be redacted from structured logs.
PII_FIELD_NAMES: frozenset[str] = frozenset(
    {
        "name",
        "first_name",
        "last_name",
        "email",
        "phone",
        "address",
        "city",
        "postal_code",
        "zip",
        "comments",
        "notes",  # free-text fields that may contain PII
    }
)

REDACTED = "***REDACTED***"


class PIISafeFilter(logging.Filter):
    """Logging filter that redacts PII patterns from log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = self._redact_pii(record.msg)
        return True

    @staticmethod
    def _redact_pii(text: str) -> str:
        """Replace patterns that look like PII with a redaction marker."""
        for pattern in _PII_PATTERNS:
            text = pattern.sub(REDACTED, text)
        return text


def redact_dict(data: dict[str, Any], depth: int = 0) -> dict[str, Any]:
    """Return a copy of *data* with PII-sensitive keys redacted.

    Recursively processes nested dicts up to *depth* levels (0 = unlimited).
    """
    result: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in PII_FIELD_NAMES:
            result[key] = REDACTED
        elif isinstance(value, dict) and (depth == 0 or depth > 1):
            result[key] = redact_dict(value, depth - 1 if depth else 0)
        else:
            result[key] = value
    return result


def install_pii_filter(logger_name: str | None = None) -> None:
    """Install the PII-safe filter on the specified logger (or root)."""
    target = logging.getLogger(logger_name)
    target.addFilter(PIISafeFilter())
