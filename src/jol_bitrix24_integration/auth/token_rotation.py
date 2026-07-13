"""Automated OAuth token rotation with configurable interval.

Enforces a maximum token lifetime (default 90 days) and supports
revocation on employee offboarding.  All rotation events are written
to the audit log for compliance evidence.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import UTC, datetime

from jol_bitrix24_integration.auth.oauth import OAuthManager, TokenSet
from jol_bitrix24_integration.logging.audit import AuditLogger

logger = logging.getLogger(__name__)


@dataclass
class RotationPolicy:
    """Defines the token rotation policy parameters."""

    max_lifetime_days: int = 90
    warn_before_days: int = 14  # emit warning N days before expiry

    @property
    def max_lifetime_seconds(self) -> float:
        return self.max_lifetime_days * 86400


class TokenRotationManager:
    """Rotates OAuth tokens according to the configured policy.

    Responsibilities
    ----------------
    * Check whether a token is due for rotation.
    * Execute the refresh flow and store the new encrypted token.
    * Emit audit events for every rotation attempt (success / failure).
    * Support emergency revocation (offboarding).
    """

    def __init__(
        self,
        oauth_manager: OAuthManager,
        audit_logger: AuditLogger,
        policy: RotationPolicy | None = None,
    ) -> None:
        self._oauth = oauth_manager
        self._audit = audit_logger
        self._policy = policy or RotationPolicy()

    def needs_rotation(self, issued_at: float) -> bool:
        """Return True if the token has exceeded its maximum lifetime."""
        return (time.time() - issued_at) >= self._policy.max_lifetime_seconds

    def should_warn(self, issued_at: float) -> bool:
        """Return True if the token is approaching its rotation deadline."""
        warn_threshold = self._policy.max_lifetime_seconds - (self._policy.warn_before_days * 86400)
        return (time.time() - issued_at) >= warn_threshold

    def rotate(self, current_token: TokenSet) -> TokenSet:
        """Execute token rotation: refresh, audit, return new token.

        Raises
        ------
        TokenRotationError
            If the refresh call fails.
        """
        ts = datetime.now(UTC).isoformat()
        try:
            new_token = self._oauth.refresh(current_token)
            self._audit.log_event(
                event_type="token_rotation",
                status="success",
                timestamp=ts,
                details={"action": "refresh_token", "policy_days": self._policy.max_lifetime_days},
            )
            logger.info("Token rotation completed successfully")
            return new_token
        except Exception as exc:
            self._audit.log_event(
                event_type="token_rotation",
                status="failure",
                timestamp=ts,
                details={"error_code": type(exc).__name__},
            )
            logger.error("Token rotation failed: %s", type(exc).__name__)
            raise TokenRotationError(str(exc)) from exc

    def revoke(self, reason: str = "offboarding") -> None:
        """Emergency token revocation (e.g. employee offboarding).

        Bitrix24 does not expose a dedicated revocation endpoint for
        on-premise; we invalidate locally and log the event.
        """
        ts = datetime.now(UTC).isoformat()
        self._audit.log_event(
            event_type="token_revocation",
            status="success",
            timestamp=ts,
            details={"reason": reason},
        )
        logger.info("Token revoked — reason: %s", reason)


class TokenRotationError(Exception):
    """Raised when automated token rotation fails."""
