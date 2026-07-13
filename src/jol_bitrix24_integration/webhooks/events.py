"""Bitrix24 webhook event type definitions and registry.

Each event type maps to a handler function that processes the payload.
Only explicitly registered event types are accepted; unknown events
are logged and discarded (defence-in-depth).
"""

from __future__ import annotations

from enum import StrEnum


class Bitrix24EventType(StrEnum):
    """Supported Bitrix24 CRM webhook event types."""

    # Contact events
    ON_CRM_CONTACT_ADD = "ONCRMCONTACTADD"
    ON_CRM_CONTACT_UPDATE = "ONCRMCONTACTUPDATE"
    ON_CRM_CONTACT_DELETE = "ONCRMCONTACTDELETE"

    # Deal events
    ON_CRM_DEAL_ADD = "ONCRMDEALADD"
    ON_CRM_DEAL_UPDATE = "ONCRMDEALUPDATE"
    ON_CRM_DEAL_DELETE = "ONCRMDEALDELETE"

    # Company (Organisation) events
    ON_CRM_COMPANY_ADD = "ONCRMCOMPANYADD"
    ON_CRM_COMPANY_UPDATE = "ONCRMCOMPANYUPDATE"
    ON_CRM_COMPANY_DELETE = "ONCRMCOMPANYDELETE"


# All known event values for quick membership testing.
KNOWN_EVENT_VALUES: frozenset[str] = frozenset(e.value for e in Bitrix24EventType)


def is_known_event(event_value: str) -> bool:
    """Return True if the event string matches a registered type."""
    return event_value.upper() in KNOWN_EVENT_VALUES
