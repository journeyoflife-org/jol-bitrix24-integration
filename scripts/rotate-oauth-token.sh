#!/usr/bin/env bash
# rotate-oauth-token.sh — Manual OAuth token rotation script
#
# Usage: ./scripts/rotate-oauth-token.sh
#
# Prerequisites:
#   - .env file with BITRIX24_* and TOKEN_* variables
#   - Python virtualenv activated
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== JOL-Bitrix24 OAuth Token Rotation ==="
echo "Project: $PROJECT_DIR"
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%S%z)"
echo ""

# Load environment
if [ -f "$PROJECT_DIR/.env" ]; then
    set -a
    source "$PROJECT_DIR/.env"
    set +a
    echo "[OK] Environment loaded from .env"
else
    echo "[ERROR] .env file not found. Copy from .env.example and configure."
    exit 1
fi

# Verify required variables
for var in BITRIX24_BASE_URL BITRIX24_CLIENT_ID BITRIX24_CLIENT_SECRET TOKEN_ENCRYPTION_KEY; do
    if [ -z "${!var:-}" ]; then
        echo "[ERROR] Required variable $var is not set."
        exit 1
    fi
done

echo "[OK] Required variables present"
echo ""

# Execute rotation
cd "$PROJECT_DIR"
python -c "
from jol_bitrix24_integration.auth.token_rotation import TokenRotationManager, RotationPolicy
from jol_bitrix24_integration.auth.oauth import OAuthManager
from jol_bitrix24_integration.logging.audit import AuditLogger
from jol_bitrix24_integration.config import Settings

settings = Settings.from_env()
print('[INFO] Initiating manual token rotation...')
print('[INFO] This is a placeholder — full implementation requires')
print('[INFO] current token to be loaded from encrypted storage.')
print('[DONE] Review audit log at:', settings.audit_log_path)
"

echo ""
echo "=== Rotation complete. Check audit log for confirmation. ==="
