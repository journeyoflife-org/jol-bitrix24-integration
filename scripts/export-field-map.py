#!/usr/bin/env python3
"""export-field-map.py — Export field mappings to CSV for compliance review.

Generates a CSV file from the field mapping definitions for inclusion
in GDPR Art. 30 Records of Processing Activities.

Usage:
    python scripts/export-field-map.py [--output field-mapping.csv]

Requires the package to be installed (pip install -e .).
"""

import csv
import sys
from pathlib import Path
from typing import IO

from jol_bitrix24_integration.mappings.field_mapping import (
    CONTACT_FIELD_MAP,
    DEAL_FIELD_MAP,
    ORGANIZATION_FIELD_MAP,
)


def export_mapping(
    entity_type: str,
    field_map: dict[str, str],
    writer: IO[str],
) -> None:
    """Write one entity type's mapping to the CSV writer."""
    for jol_field, bitrix24_field in sorted(field_map.items()):
        writer.writerow([entity_type, jol_field, bitrix24_field])


def main() -> None:
    if "--output" in sys.argv:
        output = Path(sys.argv[sys.argv.index("--output") + 1])
    else:
        output = Path("field-mapping.csv")

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Entity Type", "JOL Field", "Bitrix24 Field"])

        export_mapping("contact", CONTACT_FIELD_MAP, writer)
        export_mapping("deal", DEAL_FIELD_MAP, writer)
        export_mapping("organization", ORGANIZATION_FIELD_MAP, writer)

    print(f"Field mapping exported to: {output}")
    print(f"  Contacts:       {len(CONTACT_FIELD_MAP)} fields")
    print(f"  Deals:          {len(DEAL_FIELD_MAP)} fields")
    print(f"  Organizations:  {len(ORGANIZATION_FIELD_MAP)} fields")


if __name__ == "__main__":
    main()
