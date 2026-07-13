"""Application entry point and FastAPI app factory."""

from __future__ import annotations

import logging

from jol_bitrix24_integration.config import Settings

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> None:
    """Initialise the integration service.

    Args:
        settings: Application settings.  Loaded from environment when *None*.
    """
    if settings is None:
        settings = Settings.from_env()

    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger.info("JOL-Bitrix24 integration starting (env=%s)", settings.environment)


if __name__ == "__main__":
    create_app()
