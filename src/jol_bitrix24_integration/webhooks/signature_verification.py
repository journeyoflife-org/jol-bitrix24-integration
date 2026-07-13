"""HMAC-SHA256 signature verification for Bitrix24 webhook callbacks.

Prevents forged callbacks by validating the ``X-Bitrix-Signature``
header against the shared webhook secret.  This is a critical security
control — without it an attacker could inject fake CRM events.
"""

from __future__ import annotations

import hashlib
import hmac
import logging

logger = logging.getLogger(__name__)


def verify_signature(
    payload: bytes,
    signature_header: str | None,
    webhook_secret: str,
) -> bool:
    """Verify the HMAC-SHA256 signature of a Bitrix24 webhook payload.

    Args:
        payload: Raw request body bytes.
        signature_header: Value of the ``X-Bitrix-Signature`` header.
        webhook_secret: Shared secret configured in Bitrix24 and this service.

    Returns:
        ``True`` if the signature is valid, ``False`` otherwise.
    """
    if not signature_header:
        logger.warning("Webhook received without signature header — rejected")
        return False

    if not webhook_secret:
        logger.error("Webhook secret is not configured — cannot verify signatures")
        return False

    expected = hmac.new(
        key=webhook_secret.encode("utf-8"),
        msg=payload,
        digestmod=hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, signature_header):
        logger.warning("Webhook signature mismatch — forged callback rejected")
        return False

    logger.debug("Webhook signature verified successfully")
    return True


class WebhookVerificationError(Exception):
    """Raised when a webhook payload fails signature verification."""
