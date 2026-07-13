"""Integration test for full contact sync cycle (mocked Bitrix24 API)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from jol_bitrix24_integration.clients.bitrix24_client import Bitrix24Client
from jol_bitrix24_integration.logging.audit import AuditLogger
from jol_bitrix24_integration.sync.conflict_resolution import ConflictStrategy
from jol_bitrix24_integration.sync.contacts_sync import ContactSync
from jol_bitrix24_integration.sync.retry_queue import RetryQueue


class TestContactSyncIntegration:
    """End-to-end contact sync with mocked API calls."""

    @patch("requests.Session.post")
    def test_sync_creates_new_contacts(self, mock_post: MagicMock, tmp_path) -> None:
        # Mock Bitrix24 responses
        list_resp = MagicMock()
        list_resp.json.return_value = {"result": []}
        list_resp.raise_for_status = MagicMock()

        create_resp = MagicMock()
        create_resp.json.return_value = {"result": {"ID": 100}}
        create_resp.raise_for_status = MagicMock()

        mock_post.side_effect = [list_resp, create_resp, create_resp]

        client = Bitrix24Client("https://crm.test.local", "token")
        audit = AuditLogger(tmp_path / "audit.log")
        queue = RetryQueue()

        sync = ContactSync(client, audit, queue, ConflictStrategy.JOL_WINS)
        jol_contacts = [
            {"id": "1", "first_name": "Alice", "email": "alice@example.com"},
            {"id": "2", "first_name": "Bob", "email": "bob@example.com"},
        ]

        stats = sync.run_full_sync(jol_contacts)
        assert stats["created"] == 2
        assert stats["failed"] == 0

        # Verify audit log was written
        events = audit.read_events("sync_run")
        assert len(events) == 1
        assert events[0]["status"] == "success"
