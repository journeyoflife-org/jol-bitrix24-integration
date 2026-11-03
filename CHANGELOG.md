# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- Adopted mise: mise.toml + mise.lock pin python 3.11.18/3.12.16 (SHA256 + GitHub attestations); CI lint/test/security-scan bootstrap the interpreter via pinned jdx/mise-action with a venv on PATH (was unpinned setup-python@v5). pip install -e .[dev], all check commands, and the PII/secret greps + pip-audit are unchanged; job names lint/test/security-scan preserved.
- Initial project scaffold with full directory structure
- Bitrix24 Enterprise On-Premise REST API client with TLS and retry
- OAuth2 authorization-code flow with Fernet token encryption at rest
- Automated 90-day token rotation with audit trail
- HMAC-SHA256 webhook signature verification
- Webhook event dispatcher with type validation
- Bidirectional sync engine for contacts, deals, and organisations
- Deterministic conflict resolution (last-write-wins, JOL-wins, Bitrix24-wins, manual-review)
- Retry queue with exponential back-off for failed sync operations
- JOL ↔ Bitrix24 field mappings for contacts, deals, and organisations
- ISO 3166-1 ↔ Bitrix24 country mappings for EU-27 member states
- Append-only audit logger for compliance evidence
- PII-safe logging filter (redacts email, phone, street address patterns)
- JSON schemas for webhook events and CRM records
- Operational scripts (token rotation, webhook validation, field map export, PII log scan)
- Compliance document templates (DPA, ROPA, DPIA, retention, risk register, controls matrix)
- GitHub Actions workflows (CI, compliance-check, CodeQL, Qodana)
- Pre-commit configuration (black, ruff, mypy, security hooks)
- Dependabot configuration for pip and GitHub Actions
