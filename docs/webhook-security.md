# Webhook Security

> **Status:** TEMPLATE — requires security team review.

## Signature Verification

All incoming Bitrix24 webhook callbacks are verified using **HMAC-SHA256**.

### Flow

1. Bitrix24 signs the webhook payload with the shared secret.
2. The integration service computes HMAC-SHA256 over the raw body.
3. The computed signature is compared using constant-time comparison (`hmac.compare_digest`).
4. Mismatched or missing signatures are rejected and audit-logged.

### Configuration

| Parameter | Source | Description |
|-----------|--------|-------------|
| `BITRIX24_WEBHOOK_SECRET` | Environment (encrypted) | Shared HMAC key |
| `X-Bitrix-Signature` | HTTP header | Signature from Bitrix24 |

## Replay Protection

Webhooks include a `ts` (timestamp) field. Events older than 5 minutes are rejected.

## Rate Limiting

Incoming webhooks are rate-limited to 100 requests/minute per source IP.

## Failure Handling

| Scenario | Response | Audit Event |
|----------|----------|-------------|
| Missing signature | HTTP 401 | `webhook_received` / `signature_verification_failed` |
| Invalid signature | HTTP 401 | `webhook_received` / `signature_verification_failed` |
| Unknown event type | HTTP 400 | `webhook_received` / `unknown_event_type` |
| Handler exception | HTTP 500 | `webhook_received` / `handler_exception` |
| Success | HTTP 200 | `webhook_received` / `success` |
