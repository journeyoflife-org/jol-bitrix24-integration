# Contributing

Thank you for contributing to the JOL-Bitrix24 integration.

## Development Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Code Standards

- **Python 3.11+** required
- **Black** for formatting (`black src/ tests/`)
- **Ruff** for linting (`ruff check src/ tests/`)
- **mypy** for type checking (`mypy src/`)
- All functions must have docstrings
- Type hints required on all public APIs

## Security Requirements

- **Never log PII** — use the `PIISafeFilter` and `redact_dict()` from `logging/pii_safe_logging.py`
- **Never commit secrets** — pre-commit hook `detect-private-key` will block
- **Audit-log all operations** — use `AuditLogger` for every state change
- **Least-privilege** — only request the minimum required API scopes

## Compliance Requirements

When changing sync logic, field mappings, or data processing:

1. Update `docs/field-mapping.md` if fields change
2. Update `compliance/gdpr/ropa-entry.md` if data categories change
3. Update `compliance/risk/controls-matrix.md` if controls change
4. Flag compliance docs as templates requiring legal review

## Pull Request Process

1. Fork and branch from `main`
2. Write tests for new functionality
3. Ensure `pytest`, `ruff`, `black`, and `mypy` all pass
4. Open a PR — use the PR template
5. Security-sensitive changes require security team review
6. Compliance-sensitive changes require DPO/compliance team review

## Code Owners

See `.github/CODEOWNERS` for the complete mapping.
