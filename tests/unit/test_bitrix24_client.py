"""Unit tests for Bitrix24 REST API client."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from jol_bitrix24_integration.clients.bitrix24_client import Bitrix24APIError, Bitrix24Client


class TestBitrix24Client:
    """Tests for the Bitrix24Client class."""

    def setup_method(self) -> None:
        self.client = Bitrix24Client(
            base_url="https://crm.journeyoflife.org",
            access_token="test-token-123",
        )

    def test_client_sets_authorization_header(self) -> None:
        assert self.client._session.headers["Authorization"] == "Bearer test-token-123"

    def test_client_base_url_no_trailing_slash(self) -> None:
        client = Bitrix24Client(
            base_url="https://crm.journeyoflife.org/",
            access_token="token",
        )
        assert client._base_url == "https://crm.journeyoflife.org"

    @patch("requests.Session.post")
    def test_get_contact_success(self, mock_post: MagicMock) -> None:
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"result": {"ID": 42, "NAME": "Test"}}
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = self.client.get_contact(42)
        assert result["ID"] == 42

    @patch("requests.Session.post")
    def test_api_error_raises_exception(self, mock_post: MagicMock) -> None:
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "error": "ACCESS_DENIED",
            "error_description": "Insufficient permissions",
        }
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        with pytest.raises(Bitrix24APIError) as exc_info:
            self.client.get_contact(1)
        assert exc_info.value.code == "ACCESS_DENIED"

    def test_tls_verify_disabled_logs_warning(self) -> None:
        """TLS verification disabled should produce a warning log."""
        client = Bitrix24Client(
            base_url="https://crm.test.local",
            access_token="token",
            tls_verify=False,
        )
        assert client._session.verify is False

    def test_custom_ca_bundle(self) -> None:
        client = Bitrix24Client(
            base_url="https://crm.test.local",
            access_token="token",
            tls_ca_bundle="/etc/ssl/certs/jol-ca.pem",
        )
        assert client._session.verify == "/etc/ssl/certs/jol-ca.pem"
