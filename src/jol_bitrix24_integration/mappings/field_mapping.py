"""Deterministic field mappings between JOL and Bitrix24 CRM entities.

Each mapping is a dict: ``{jol_field: bitrix24_field}``.  These mappings
serve as the GDPR Art. 30 record of processing activities and must be
reviewed before each production deployment.

Version: 1.0.0
"""

from __future__ import annotations

from typing import Any

# -- Contact field mapping (JOL → Bitrix24) -----------------------------------

CONTACT_FIELD_MAP: dict[str, str] = {
    "first_name": "NAME",
    "last_name": "LAST_NAME",
    "email": "EMAIL",
    "phone": "PHONE",
    "organization_id": "COMPANY_ID",
    "country_code": "ADDRESS_COUNTRY",
    "city": "ADDRESS_CITY",
    "postal_code": "ADDRESS_POSTAL_CODE",
    "address_line_1": "ADDRESS",
    "source": "SOURCE_ID",
    "assigned_to": "ASSIGNED_BY_ID",
    "comments": "COMMENTS",
}

# -- Deal field mapping (JOL → Bitrix24) --------------------------------------

DEAL_FIELD_MAP: dict[str, str] = {
    "title": "TITLE",
    "stage_id": "STAGE_ID",
    "category_id": "CATEGORY_ID",
    "contact_id": "CONTACT_ID",
    "company_id": "COMPANY_ID",
    "opportunity": "OPPORTUNITY",
    "currency_id": "CURRENCY_ID",
    "close_date": "CLOSEDATE",
    "source": "SOURCE_ID",
    "assigned_to": "ASSIGNED_BY_ID",
    "comments": "COMMENTS",
}

# -- Organization (Company) field mapping (JOL → Bitrix24) --------------------

ORGANIZATION_FIELD_MAP: dict[str, str] = {
    "name": "TITLE",
    "industry": "INDUSTRY",
    "company_type": "COMPANY_TYPE",
    "country_code": "ADDRESS_COUNTRY",
    "city": "ADDRESS_CITY",
    "postal_code": "ADDRESS_POSTAL_CODE",
    "address_line_1": "ADDRESS",
    "website": "WEB",
    "phone": "PHONE",
    "email": "EMAIL",
    "source": "SOURCE_ID",
    "assigned_to": "ASSIGNED_BY_ID",
    "comments": "COMMENTS",
}


def map_fields(
    source_record: dict[str, Any],
    field_map: dict[str, str],
) -> dict[str, Any]:
    """Apply a field mapping to transform a source record.

    Only fields present in the mapping are included.  Unmapped fields
    are silently dropped (least-data principle).

    Args:
        source_record: The JOL-side record.
        field_map: Mapping dict ``{jol_field: bitrix24_field}``.

    Returns:
        Transformed record with Bitrix24 field names.
    """
    result: dict[str, Any] = {}
    for jol_field, bitrix_field in field_map.items():
        if jol_field in source_record:
            value = source_record[jol_field]
            # Email and phone must use Bitrix24 multi-value format
            if bitrix_field in ("EMAIL", "PHONE") and value:
                result[bitrix_field] = [{"VALUE": value, "VALUE_TYPE": "WORK"}]
            else:
                result[bitrix_field] = value
    return result


def reverse_map_fields(
    bitrix_record: dict[str, Any],
    field_map: dict[str, str],
) -> dict[str, Any]:
    """Reverse a field mapping (Bitrix24 → JOL)."""
    reverse: dict[str, str] = {v: k for k, v in field_map.items()}
    result: dict[str, Any] = {}
    for bitrix_field, jol_field in reverse.items():
        if bitrix_field in bitrix_record:
            result[jol_field] = bitrix_record[bitrix_field]
    return result
