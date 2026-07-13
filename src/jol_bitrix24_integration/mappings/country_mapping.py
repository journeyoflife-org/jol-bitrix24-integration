"""Country code mappings — ISO 3166-1 alpha-2 ↔ Bitrix24 country names.

Bitrix24 uses full country names; JOL uses ISO codes.  This mapping
ensures consistent representation across the 27 EU member states plus
common partner countries.
"""

from __future__ import annotations

# EU-27 member states (ISO 3166-1 alpha-2 → Bitrix24 display name)
EU27_COUNTRY_MAP: dict[str, str] = {
    "AT": "Austria",
    "BE": "Belgium",
    "BG": "Bulgaria",
    "HR": "Croatia",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "EE": "Estonia",
    "FI": "Finland",
    "FR": "France",
    "DE": "Germany",
    "GR": "Greece",
    "HU": "Hungary",
    "IE": "Ireland",
    "IT": "Italy",
    "LV": "Latvia",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MT": "Malta",
    "NL": "Netherlands",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "ES": "Spain",
    "SE": "Sweden",
}

# Reverse mapping (display name → ISO code)
REVERSE_COUNTRY_MAP: dict[str, str] = {v: k for k, v in EU27_COUNTRY_MAP.items()}

# Extended map for common partner countries
EXTENDED_COUNTRY_MAP: dict[str, str] = {
    **EU27_COUNTRY_MAP,
    "GB": "United Kingdom",
    "CH": "Switzerland",
    "NO": "Norway",
    "US": "United States",
    "CA": "Canada",
}


def iso_to_bitrix24(iso_code: str) -> str:
    """Convert an ISO 3166-1 alpha-2 code to Bitrix24 country name."""
    return EXTENDED_COUNTRY_MAP.get(iso_code.upper(), iso_code)


def bitrix24_to_iso(country_name: str) -> str:
    """Convert a Bitrix24 country name to ISO 3166-1 alpha-2."""
    reverse = {v: k for k, v in EXTENDED_COUNTRY_MAP.items()}
    return reverse.get(country_name, country_name)
