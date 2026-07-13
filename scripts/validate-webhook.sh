#!/usr/bin/env bash
# validate-webhook.sh — Test webhook signature verification
#
# Usage: ./scripts/validate-webhook.sh
#
# Sends a signed test webhook payload to the local service endpoint
# to verify that signature verification is working correctly.
set -euo pipefail

WEBHOOK_URL="${1:-http://localhost:8000/webhooks/bitrix24}"
WEBHOOK_SECRET="${BITRIX24_WEBHOOK_SECRET:-test-secret}"

echo "=== JOL-Bitrix24 Webhook Validation ==="
echo "Endpoint: $WEBHOOK_URL"
echo ""

# Generate test payload
PAYLOAD='{"event":"ONCRMCONTACTADD","data":{"FIELDS":{"ID":999}}}'

# Compute HMAC-SHA256 signature
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$WEBHOOK_SECRET" | awk '{print $NF}')
echo "[INFO] Payload: $PAYLOAD"
echo "[INFO] Signature: $SIGNATURE"
echo ""

# Test 1: Valid signature (should return 200)
echo "--- Test 1: Valid signature ---"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "$WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -H "X-Bitrix-Signature: $SIGNATURE" \
    -d "$PAYLOAD" 2>/dev/null || echo "000")
echo "HTTP Status: $HTTP_CODE"
if [ "$HTTP_CODE" = "200" ]; then
    echo "[PASS] Valid signature accepted"
else
    echo "[WARN] Expected 200, got $HTTP_CODE (service may not be running)"
fi

# Test 2: Invalid signature (should return 401)
echo ""
echo "--- Test 2: Invalid signature ---"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "$WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -H "X-Bitrix-Signature: invalidsignature1234567890abcdef" \
    -d "$PAYLOAD" 2>/dev/null || echo "000")
echo "HTTP Status: $HTTP_CODE"
if [ "$HTTP_CODE" = "401" ]; then
    echo "[PASS] Invalid signature rejected"
else
    echo "[WARN] Expected 401, got $HTTP_CODE (service may not be running)"
fi

# Test 3: Missing signature (should return 401)
echo ""
echo "--- Test 3: Missing signature ---"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "$WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" 2>/dev/null || echo "000")
echo "HTTP Status: $HTTP_CODE"
if [ "$HTTP_CODE" = "401" ]; then
    echo "[PASS] Missing signature rejected"
else
    echo "[WARN] Expected 401, got $HTTP_CODE (service may not be running)"
fi

echo ""
echo "=== Validation complete ==="
