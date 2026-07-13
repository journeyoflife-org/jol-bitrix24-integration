"""Centralised application settings loaded from environment / .env file.

Deployment model: Bitrix24 Enterprise On-Premise on JOL's own Proxmox
infrastructure.  All data stays within JOL-controlled EU infrastructure;
no third-country transfers for the CRM processor.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Settings:
    """Immutable configuration for the integration service.

    Infrastructure context
    ----------------------
    * Bitrix24 **Enterprise On-Premise** running on JOL Proxmox cluster.
    * Integration service and Bitrix24 share the same network segment.
    * All PII remains on JOL-controlled infrastructure within the EU.
    """

    # Bitrix24 Enterprise On-Premise (self-hosted base URL, not SaaS)
    bitrix24_base_url: str = ""  # e.g. https://crm.journeyoflife.org
    bitrix24_client_id: str = ""
    bitrix24_client_secret: str = ""
    bitrix24_redirect_uri: str = ""

    # TLS verification (on-prem: may use internal CA)
    bitrix24_tls_verify: bool = True
    bitrix24_tls_ca_bundle: str = ""  # path to custom CA bundle

    # Webhooks
    bitrix24_webhook_secret: str = ""
    bitrix24_webhook_url: str = ""

    # Token rotation
    token_rotation_interval_days: int = 90
    token_encryption_key: str = ""

    # Sync
    sync_interval_minutes: int = 15
    sync_batch_size: int = 100
    sync_conflict_strategy: str = "manual_review"

    # Logging
    log_level: str = "INFO"
    audit_log_path: str = "/var/log/jol-bitrix24/audit.log"
    pii_logging_enabled: bool = False

    # Database
    database_url: str = ""

    # Environment tag (dev / staging / prod)
    environment: str = "dev"

    @classmethod
    def from_env(cls, env_file: str | Path | None = None) -> Settings:
        """Build settings from environment variables, optionally loading a .env file."""
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        return cls(
            bitrix24_base_url=os.getenv("BITRIX24_BASE_URL", ""),
            bitrix24_client_id=os.getenv("BITRIX24_CLIENT_ID", ""),
            bitrix24_client_secret=os.getenv("BITRIX24_CLIENT_SECRET", ""),
            bitrix24_redirect_uri=os.getenv("BITRIX24_REDIRECT_URI", ""),
            bitrix24_tls_verify=os.getenv("BITRIX24_TLS_VERIFY", "true").lower()
            in ("true", "1", "yes"),
            bitrix24_tls_ca_bundle=os.getenv("BITRIX24_TLS_CA_BUNDLE", ""),
            bitrix24_webhook_secret=os.getenv("BITRIX24_WEBHOOK_SECRET", ""),
            bitrix24_webhook_url=os.getenv("BITRIX24_WEBHOOK_URL", ""),
            token_rotation_interval_days=int(os.getenv("TOKEN_ROTATION_INTERVAL_DAYS", "90")),
            token_encryption_key=os.getenv("TOKEN_ENCRYPTION_KEY", ""),
            sync_interval_minutes=int(os.getenv("SYNC_INTERVAL_MINUTES", "15")),
            sync_batch_size=int(os.getenv("SYNC_BATCH_SIZE", "100")),
            sync_conflict_strategy=os.getenv("SYNC_CONFLICT_STRATEGY", "manual_review"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            audit_log_path=os.getenv("AUDIT_LOG_PATH", "/var/log/jol-bitrix24/audit.log"),
            pii_logging_enabled=os.getenv("PII_LOGGING_ENABLED", "false").lower()
            in ("true", "1", "yes"),
            database_url=os.getenv("DATABASE_URL", ""),
            environment=os.getenv("ENVIRONMENT", "dev"),
        )

    def validate(self) -> list[str]:
        """Validate critical settings.  Returns a list of warning messages.

        Raises no exceptions — callers decide how to handle warnings
        (e.g. log-and-continue in dev, fail-fast in prod).
        """
        warnings: list[str] = []

        if self.bitrix24_base_url and not self.bitrix24_base_url.startswith("https://"):
            warnings.append(
                "bitrix24_base_url should use HTTPS " f"(got: {self.bitrix24_base_url!r})"
            )

        if not self.token_encryption_key:
            warnings.append(
                "token_encryption_key is empty — " "Fernet encryption will fail at runtime"
            )

        if self.pii_logging_enabled:
            warnings.append(
                "pii_logging_enabled is True — this may violate "
                "GDPR Art. 5 data-minimisation in production"
            )

        if not self.bitrix24_webhook_secret:
            warnings.append(
                "bitrix24_webhook_secret is empty — "
                "webhook signature verification will reject all events"
            )

        for w in warnings:
            logger.warning("Config validation: %s", w)

        return warnings
