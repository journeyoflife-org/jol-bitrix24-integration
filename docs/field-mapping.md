# Field Mapping

> **Version:** 1.0.0 · **Status:** TEMPLATE — requires legal review for GDPR Art. 30 compliance.

## Contact Fields (JOL → Bitrix24)

| JOL Field | Bitrix24 Field | Type | Notes |
|-----------|---------------|------|-------|
| `first_name` | `NAME` | string | |
| `last_name` | `LAST_NAME` | string | |
| `email` | `EMAIL` | multi-value | WORK type |
| `phone` | `PHONE` | multi-value | WORK type |
| `organization_id` | `COMPANY_ID` | integer | FK to company |
| `country_code` | `ADDRESS_COUNTRY` | string | ISO → display name |
| `city` | `ADDRESS_CITY` | string | |
| `postal_code` | `ADDRESS_POSTAL_CODE` | string | |
| `address_line_1` | `ADDRESS` | string | |
| `source` | `SOURCE_ID` | string | |
| `assigned_to` | `ASSIGNED_BY_ID` | integer | User ID |
| `comments` | `COMMENTS` | text | |

## Deal Fields (JOL → Bitrix24)

| JOL Field | Bitrix24 Field | Type | Notes |
|-----------|---------------|------|-------|
| `title` | `TITLE` | string | |
| `stage_id` | `STAGE_ID` | string | Pipeline stage |
| `category_id` | `CATEGORY_ID` | integer | |
| `contact_id` | `CONTACT_ID` | integer | FK to contact |
| `company_id` | `COMPANY_ID` | integer | FK to company |
| `opportunity` | `OPPORTUNITY` | decimal | |
| `currency_id` | `CURRENCY_ID` | string | ISO currency |
| `close_date` | `CLOSEDATE` | date | |
| `source` | `SOURCE_ID` | string | |
| `assigned_to` | `ASSIGNED_BY_ID` | integer | User ID |
| `comments` | `COMMENTS` | text | |

## Organization Fields (JOL → Bitrix24)

| JOL Field | Bitrix24 Field | Type | Notes |
|-----------|---------------|------|-------|
| `name` | `TITLE` | string | |
| `industry` | `INDUSTRY` | string | |
| `company_type` | `COMPANY_TYPE` | string | |
| `country_code` | `ADDRESS_COUNTRY` | string | ISO → display name |
| `city` | `ADDRESS_CITY` | string | |
| `postal_code` | `ADDRESS_POSTAL_CODE` | string | |
| `address_line_1` | `ADDRESS` | string | |
| `website` | `WEB` | string | |
| `phone` | `PHONE` | multi-value | WORK type |
| `email` | `EMAIL` | multi-value | WORK type |
| `source` | `SOURCE_ID` | string | |
| `assigned_to` | `ASSIGNED_BY_ID` | integer | User ID |
| `comments` | `COMMENTS` | text | |

## GDPR Art. 30 Note

This mapping document serves as part of the Records of Processing Activities
(ROPA) required under GDPR Article 30. It must be reviewed and approved by the
Data Protection Officer before each production deployment.
