"""Unit tests for webhook signature verification."""

from __future__ import annotations

import hashlib
import hmac

from jol_bitrix24_integration.webhooks.signature_verification import verify_signature


class TestSignatureVerification:
    """Tests for HMAC-SHA256 webhook signature verification."""

    SECRET = "test-webhook-secret-key"

    def _sign(self, payload: bytes) -> str:
        return hmac.new(
            key=self.SECRET.encode(),
            msg=payload,
            digestmod=hashlib.sha256,
        ).hexdigest()

    def test_valid_signature(self) -> None:
        payload = b'{"event":"ONCRMCONTACTADD","data":{}}'
        sig = self._sign(payload)
        assert verify_signature(payload, sig, self.SECRET) is True

    def test_invalid_signature(self) -> None:
        payload = b'{"event":"ONCRMCONTACTADD","data":{}}'
        assert verify_signature(payload, "deadbeef" * 8, self.SECRET) is False

    def test_missing_signature_header(self) -> None:
        assert verify_signature(b"{}", None, self.SECRET) is False

    def test_empty_webhook_secret(self) -> None:
        payload = b'{"event":"test"}'
        sig = self._sign(payload)
        assert verify_signature(payload, sig, "") is False

    def test_tampered_payload(self) -> None:
        original = b'{"event":"ONCRMCONTACTADD","data":{}}'
        sig = self._sign(original)
        tampered = b'{"event":"ONCRMCONTACTDELETE","data":{}}'
        assert verify_signature(tampered, sig, self.SECRET) is False
