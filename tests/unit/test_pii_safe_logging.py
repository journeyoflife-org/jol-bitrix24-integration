"""Unit tests for PII-safe logging."""

from __future__ import annotations

import logging

from jol_bitrix24_integration.logging.pii_safe_logging import (
    PIISafeFilter,
    redact_dict,
)


class TestPIISafeFilter:
    """Tests for PII redaction in log messages."""

    def setup_method(self) -> None:
        self.filter = PIISafeFilter()

    def test_redacts_email(self) -> None:
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="User email: john@example.com logged in",
            args=(),
            exc_info=None,
        )
        self.filter.filter(record)
        assert "john@example.com" not in str(record.msg)
        assert "***REDACTED***" in str(record.msg)

    def test_redacts_phone(self) -> None:
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Phone: +49 30 12345678 called",
            args=(),
            exc_info=None,
        )
        self.filter.filter(record)
        assert "+49 30 12345678" not in str(record.msg)


class TestRedactDict:
    """Tests for dict-level PII redaction."""

    def test_redacts_known_pii_fields(self) -> None:
        data = {"id": 42, "name": "Jane Doe", "email": "jane@example.com", "role": "admin"}
        result = redact_dict(data)
        assert result["id"] == 42
        assert result["role"] == "admin"
        assert result["name"] == "***REDACTED***"
        assert result["email"] == "***REDACTED***"

    def test_redacts_nested_pii(self) -> None:
        data = {"user": {"id": 1, "name": "Test", "email": "test@x.com"}}
        result = redact_dict(data)
        assert result["user"]["id"] == 1
        assert result["user"]["name"] == "***REDACTED***"
