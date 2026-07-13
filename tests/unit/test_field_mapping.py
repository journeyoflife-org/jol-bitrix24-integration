"""Unit tests for field mapping transformations."""

from __future__ import annotations

from jol_bitrix24_integration.mappings.field_mapping import (
    CONTACT_FIELD_MAP,
    DEAL_FIELD_MAP,
    ORGANIZATION_FIELD_MAP,
    map_fields,
    reverse_map_fields,
)


class TestFieldMapping:

    def test_contact_map_basic(self) -> None:
        jol = {"first_name": "Jane", "last_name": "Doe", "email": "jane@example.com"}
        mapped = map_fields(jol, CONTACT_FIELD_MAP)
        assert mapped["NAME"] == "Jane"
        assert mapped["LAST_NAME"] == "Doe"
        # Email uses multi-value format
        assert mapped["EMAIL"] == [{"VALUE": "jane@example.com", "VALUE_TYPE": "WORK"}]

    def test_unmapped_fields_dropped(self) -> None:
        jol = {"first_name": "Jane", "secret_field": "should_be_dropped"}
        mapped = map_fields(jol, CONTACT_FIELD_MAP)
        assert "secret_field" not in mapped

    def test_deal_map(self) -> None:
        jol = {"title": "Big Deal", "stage_id": "NEW", "opportunity": 50000}
        mapped = map_fields(jol, DEAL_FIELD_MAP)
        assert mapped["TITLE"] == "Big Deal"
        assert mapped["STAGE_ID"] == "NEW"

    def test_organization_map(self) -> None:
        jol = {"name": "ACME Corp", "website": "https://acme.com"}
        mapped = map_fields(jol, ORGANIZATION_FIELD_MAP)
        assert mapped["TITLE"] == "ACME Corp"
        assert mapped["WEB"] == "https://acme.com"

    def test_reverse_map(self) -> None:
        bitrix = {"NAME": "Jane", "LAST_NAME": "Doe"}
        reversed_ = reverse_map_fields(bitrix, CONTACT_FIELD_MAP)
        assert reversed_["first_name"] == "Jane"
        assert reversed_["last_name"] == "Doe"

    def test_empty_record(self) -> None:
        assert map_fields({}, CONTACT_FIELD_MAP) == {}
