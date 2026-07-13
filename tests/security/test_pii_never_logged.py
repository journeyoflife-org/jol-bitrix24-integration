"""Security test: verify PII never appears in log output."""

from __future__ import annotations

import io
import logging

from jol_bitrix24_integration.logging.pii_safe_logging import install_pii_filter


class TestPIINeverLogged:
    """Ensure personal data is never written to log output."""

    def test_log_output_contains_no_email(self) -> None:
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        logger = logging.getLogger("test_pii_security")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        install_pii_filter("test_pii_security")

        logger.info("Processing contact: user@example.com for sync")
        output = stream.getvalue()

        assert "user@example.com" not in output
        assert "***REDACTED***" in output

    def test_log_output_contains_no_phone(self) -> None:
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        logger = logging.getLogger("test_pii_phone")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        install_pii_filter("test_pii_phone")

        logger.info("Calling phone +49 30 12345678 for verification")
        output = stream.getvalue()

        assert "+49 30 12345678" not in output
