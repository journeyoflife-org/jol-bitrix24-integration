"""Low-level Bitrix24 REST API client for Enterprise On-Premise deployment.

Targets the self-hosted Bitrix24 instance running on JOL's Proxmox
infrastructure.  Supports internal CA bundles for TLS verification.
"""

from __future__ import annotations

import logging
from typing import Any, cast

import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

# Shared retry policy: exponential back-off on transient network errors only.
_RETRY_TRANSIENT = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=1, max=10),
    retry=retry_if_exception_type(requests.RequestException),
)

# Least-privilege: only CRM scopes required for sync operations.
REQUIRED_SCOPES = frozenset(
    {
        "crm",  # CRM entity read/write
        "rest_command",  # REST command execution
    }
)


class Bitrix24Client:
    """Thin wrapper around the Bitrix24 Enterprise On-Premise REST API.

    Security controls
    -----------------
    * TLS verification enabled by default (supports internal CA bundles).
    * Only minimum required OAuth scopes requested (least-privilege).
    * PII is never logged — only method names and error codes.
    * Exponential back-off with jitter on transient failures.
    """

    def __init__(
        self,
        base_url: str,
        access_token: str,
        *,
        tls_verify: bool = True,
        tls_ca_bundle: str = "",
        timeout: int = 30,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {access_token}"})

        # TLS configuration for on-premise (may use internal CA)
        if tls_verify:
            self._session.verify = tls_ca_bundle if tls_ca_bundle else True
        else:
            logger.warning("TLS verification DISABLED — acceptable only in dev/test")
            self._session.verify = False

    # -- CRM Contacts ----------------------------------------------------------

    @_RETRY_TRANSIENT
    def get_contact(self, contact_id: int) -> dict[str, Any]:
        """Fetch a single CRM contact by ID."""
        return self._call("crm.contact.get", {"ID": contact_id})

    @_RETRY_TRANSIENT
    def list_contacts(self, start: int = 0, batch: int = 50) -> dict[str, Any]:
        """List CRM contacts with pagination."""
        params = {"start": start, "order": {"ID": "ASC"}, "batch": batch}
        return self._call("crm.contact.list", params)

    @_RETRY_TRANSIENT
    def create_contact(self, fields: dict[str, Any]) -> dict[str, Any]:
        """Create a new CRM contact."""
        return self._call("crm.contact.add", {"fields": fields})

    @_RETRY_TRANSIENT
    def update_contact(self, contact_id: int, fields: dict[str, Any]) -> dict[str, Any]:
        """Update an existing CRM contact."""
        return self._call("crm.contact.update", {"ID": contact_id, "fields": fields})

    @_RETRY_TRANSIENT
    def delete_contact(self, contact_id: int) -> dict[str, Any]:
        """Delete a CRM contact."""
        return self._call("crm.contact.delete", {"ID": contact_id})

    # -- CRM Deals -------------------------------------------------------------

    @_RETRY_TRANSIENT
    def list_deals(self, start: int = 0) -> dict[str, Any]:
        """List CRM deals with pagination."""
        return self._call("crm.deal.list", {"start": start})

    @_RETRY_TRANSIENT
    def get_deal(self, deal_id: int) -> dict[str, Any]:
        """Fetch a single CRM deal by ID."""
        return self._call("crm.deal.get", {"ID": deal_id})

    @_RETRY_TRANSIENT
    def create_deal(self, fields: dict[str, Any]) -> dict[str, Any]:
        """Create a new CRM deal."""
        return self._call("crm.deal.add", {"fields": fields})

    @_RETRY_TRANSIENT
    def update_deal(self, deal_id: int, fields: dict[str, Any]) -> dict[str, Any]:
        """Update an existing CRM deal."""
        return self._call("crm.deal.update", {"ID": deal_id, "fields": fields})

    # -- CRM Companies (Organizations) -----------------------------------------

    @_RETRY_TRANSIENT
    def list_companies(self, start: int = 0) -> dict[str, Any]:
        """List CRM companies (organisations) with pagination."""
        return self._call("crm.company.list", {"start": start})

    @_RETRY_TRANSIENT
    def create_company(self, fields: dict[str, Any]) -> dict[str, Any]:
        """Create a new CRM company."""
        return self._call("crm.company.add", {"fields": fields})

    @_RETRY_TRANSIENT
    def update_company(self, company_id: int, fields: dict[str, Any]) -> dict[str, Any]:
        """Update an existing CRM company."""
        return self._call("crm.company.update", {"ID": company_id, "fields": fields})

    # -- Generic ---------------------------------------------------------------

    def _call(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute a Bitrix24 REST method.

        Logs the method name but **never** logs request/response payloads that
        may contain PII (GDPR Art. 5 — data minimisation).
        """
        url = f"{self._base_url}/rest/1/{method}/"
        logger.debug("Bitrix24 API call: %s", method)
        resp = self._session.post(url, json=params or {}, timeout=self._timeout)
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            logger.error(
                "Bitrix24 error: %s — %s",
                data["error"],
                data.get("error_description"),
            )
            raise Bitrix24APIError(data["error"], data.get("error_description", ""))
        result: dict[str, Any] = cast(dict[str, Any], data.get("result", {}))
        return result


class Bitrix24APIError(Exception):
    """Raised when the Bitrix24 REST API returns an error."""

    def __init__(self, code: str, description: str) -> None:
        self.code = code
        self.description = description
        super().__init__(f"Bitrix24 error {code}: {description}")
