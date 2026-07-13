"""Webhook request handler — verify, parse, and dispatch events.

The handler is the single entry point for all incoming Bitrix24
webhook HTTP requests.  It enforces:

1. Signature verification (reject forged callbacks).
2. Event type validation (reject unknown events).
3. Dispatch to the appropriate sync handler.
4. Audit logging of every received event.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from jol_bitrix24_integration.logging.audit import AuditLogger
from jol_bitrix24_integration.webhooks.events import (
    Bitrix24EventType,
    is_known_event,
)
from jol_bitrix24_integration.webhooks.signature_verification import verify_signature

logger = logging.getLogger(__name__)

# Type alias for handler callbacks.
EventHandler = Callable[[dict[str, Any]], None]


class WebhookDispatcher:
    """Verifies and dispatches incoming Bitrix24 webhook payloads.

    Security controls
    -----------------
    * Every request is signature-verified before processing.
    * Unknown event types are logged and rejected.
    * All events are audit-logged regardless of outcome.
    """

    def __init__(
        self,
        webhook_secret: str,
        audit_logger: AuditLogger,
    ) -> None:
        self._secret = webhook_secret
        self._audit = audit_logger
        self._handlers: dict[str, EventHandler] = {}

    def register(self, event_type: Bitrix24EventType, handler: EventHandler) -> None:
        """Register a handler for a specific event type."""
        self._handlers[event_type.value] = handler
        logger.debug("Registered handler for event: %s", event_type.value)

    def handle_request(self, raw_body: bytes, signature_header: str | None) -> bool:
        """Process an incoming webhook request.

        Args:
            raw_body: Raw HTTP request body.
            signature_header: ``X-Bitrix-Signature`` header value.

        Returns:
            ``True`` if the event was processed, ``False`` if rejected.
        """
        ts = datetime.now(UTC).isoformat()

        # Step 1 — signature verification
        if not verify_signature(raw_body, signature_header, self._secret):
            self._audit.log_event(
                event_type="webhook_received",
                status="failure",
                timestamp=ts,
                details={"reason": "signature_verification_failed"},
            )
            return False

        # Step 2 — parse payload
        try:
            payload = json.loads(raw_body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._audit.log_event(
                event_type="webhook_received",
                status="failure",
                timestamp=ts,
                details={"reason": "invalid_json"},
            )
            logger.warning("Webhook payload is not valid JSON")
            return False

        # Step 3 — validate event type
        event_value: str = payload.get("event", "")
        if not is_known_event(event_value):
            self._audit.log_event(
                event_type="webhook_received",
                status="failure",
                timestamp=ts,
                details={"reason": "unknown_event_type", "event": event_value},
            )
            logger.warning("Unknown webhook event type: %s", event_value)
            return False

        # Step 4 — dispatch
        handler = self._handlers.get(event_value.upper())
        if handler is None:
            logger.info("No handler registered for event: %s", event_value)
            return True  # event is valid but unhandled — still acknowledge

        try:
            handler(payload.get("data", {}))
            self._audit.log_event(
                event_type="webhook_received",
                status="success",
                timestamp=ts,
                details={"event": event_value},
            )
            return True
        except Exception:  # noqa: BLE001 — catch-all intentional for audit logging
            self._audit.log_event(
                event_type="webhook_received",
                status="failure",
                timestamp=ts,
                details={"event": event_value, "reason": "handler_exception"},
            )
            logger.exception("Handler raised exception for event: %s", event_value)
            return False
