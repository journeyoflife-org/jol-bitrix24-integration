"""OAuth2 authorization-code flow for Bitrix24 Enterprise On-Premise.

Handles token acquisition, refresh, and secure storage.  Tokens are
encrypted at rest using Fernet symmetric encryption.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from typing import Any

import requests
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)


# noinspection PyMissingConstructor
@dataclass
class TokenSet:
    """Represents an OAuth2 token pair with expiry metadata."""

    access_token: str
    refresh_token: str
    expires_at: float  # Unix timestamp
    scope: str = ""

    @property
    def is_expired(self) -> bool:
        return time.time() >= (self.expires_at - 60)  # 60-second safety margin


class OAuthManager:
    """Manages the OAuth2 lifecycle for Bitrix24 Enterprise On-Premise.

    Security controls
    -----------------
    * Tokens encrypted at rest (Fernet / AES-128-CBC).
    * Tokens never logged (PII-safe logging policy).
    * Refresh tokens are single-use; old tokens invalidated on rotation.
    """

    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        encryption_key: str,
        *,
        tls_verify: bool = True,
        tls_ca_bundle: str = "",
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._fernet = Fernet(
            encryption_key.encode() if isinstance(encryption_key, str) else encryption_key
        )
        self._tls_verify = tls_ca_bundle if (tls_verify and tls_ca_bundle) else tls_verify

    # -- Public API ------------------------------------------------------------

    def get_authorization_url(self) -> str:
        """Return the URL the user must visit to grant OAuth access."""
        return (
            f"{self._base_url}/oauth/authorize/"
            f"?client_id={self._client_id}"
            f"&redirect_uri={self._redirect_uri}"
            f"&response_type=code"
            f"&scope=crm"
        )

    def exchange_code(self, authorization_code: str) -> TokenSet:
        """Exchange an authorization code for an access + refresh token pair."""
        resp = requests.post(
            f"{self._base_url}/oauth/token/",
            data={
                "grant_type": "authorization_code",
                "code": authorization_code,
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "redirect_uri": self._redirect_uri,
            },
            verify=self._tls_verify,
            timeout=15,
        )
        resp.raise_for_status()
        return self._parse_token_response(resp.json())

    def refresh(self, token_set: TokenSet) -> TokenSet:
        """Use the refresh token to obtain a new token pair.

        The old refresh token is invalidated server-side by Bitrix24.
        """
        resp = requests.post(
            f"{self._base_url}/oauth/token/",
            data={
                "grant_type": "refresh_token",
                "refresh_token": token_set.refresh_token,
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            },
            verify=self._tls_verify,
            timeout=15,
        )
        resp.raise_for_status()
        logger.info("OAuth token refreshed successfully")
        return self._parse_token_response(resp.json())

    # -- Secure storage --------------------------------------------------------

    def encrypt_token(self, token_set: TokenSet) -> bytes:
        """Encrypt a token set for storage at rest."""
        payload = json.dumps(
            {
                "access_token": token_set.access_token,
                "refresh_token": token_set.refresh_token,
                "expires_at": token_set.expires_at,
                "scope": token_set.scope,
            }
        )
        return self._fernet.encrypt(payload.encode())

    def decrypt_token(self, encrypted: bytes) -> TokenSet:
        """Decrypt a stored token set."""
        payload = json.loads(self._fernet.decrypt(encrypted).decode())
        return TokenSet(**payload)

    # -- Internal --------------------------------------------------------------

    @staticmethod
    def _parse_token_response(data: dict[str, Any]) -> TokenSet:
        """Parse the Bitrix24 token endpoint response into a TokenSet."""
        return TokenSet(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_at=time.time() + data.get("expires_in", 3600),
            scope=data.get("scope", "crm"),
        )
