"""Unit tests for conflict resolution strategies."""

from __future__ import annotations

from datetime import UTC, datetime

from jol_bitrix24_integration.sync.conflict_resolution import (
    ConflictRecord,
    ConflictStrategy,
    resolve_conflict,
)


def _make_conflict(
    jol_modified: datetime,
    bitrix_modified: datetime,
) -> ConflictRecord:
    return ConflictRecord(
        entity_type="contact",
        entity_id="42",
        jol_version={"NAME": "JOL Version"},
        bitrix24_version={"NAME": "Bitrix24 Version"},
        jol_modified=jol_modified,
        bitrix24_modified=bitrix_modified,
    )


class TestConflictResolution:

    def test_last_write_wins_jol_newer(self) -> None:
        conflict = _make_conflict(
            jol_modified=datetime(2026, 7, 13, 12, 0, tzinfo=UTC),
            bitrix_modified=datetime(2026, 7, 13, 10, 0, tzinfo=UTC),
        )
        winner = resolve_conflict(conflict, ConflictStrategy.LAST_WRITE_WINS)
        assert winner == {"NAME": "JOL Version"}
        assert conflict.resolved is True

    def test_last_write_wins_bitrix_newer(self) -> None:
        conflict = _make_conflict(
            jol_modified=datetime(2026, 7, 13, 10, 0, tzinfo=UTC),
            bitrix_modified=datetime(2026, 7, 13, 12, 0, tzinfo=UTC),
        )
        winner = resolve_conflict(conflict, ConflictStrategy.LAST_WRITE_WINS)
        assert winner == {"NAME": "Bitrix24 Version"}

    def test_jol_wins_policy(self) -> None:
        conflict = _make_conflict(
            jol_modified=datetime(2026, 1, 1, tzinfo=UTC),
            bitrix_modified=datetime(2026, 7, 13, tzinfo=UTC),
        )
        winner = resolve_conflict(conflict, ConflictStrategy.JOL_WINS)
        assert winner == {"NAME": "JOL Version"}

    def test_bitrix24_wins_policy(self) -> None:
        conflict = _make_conflict(
            jol_modified=datetime(2026, 7, 13, tzinfo=UTC),
            bitrix_modified=datetime(2026, 1, 1, tzinfo=UTC),
        )
        winner = resolve_conflict(conflict, ConflictStrategy.BITRIX24_WINS)
        assert winner == {"NAME": "Bitrix24 Version"}

    def test_manual_review_returns_none(self) -> None:
        conflict = _make_conflict(
            jol_modified=datetime(2026, 7, 13, tzinfo=UTC),
            bitrix_modified=datetime(2026, 7, 13, tzinfo=UTC),
        )
        winner = resolve_conflict(conflict, ConflictStrategy.MANUAL_REVIEW)
        assert winner is None
        assert conflict.resolved is False
