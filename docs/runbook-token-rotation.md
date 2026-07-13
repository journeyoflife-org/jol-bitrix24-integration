# Token Rotation Runbook

> **Status:** TEMPLATE — requires operational approval.

## Overview

OAuth tokens are rotated every **90 days** as required by the security policy.
Rotation is automated; this runbook covers manual intervention scenarios.

## Automated Rotation

1. The `TokenRotationManager` checks token age against the configured policy.
2. If the token is due for rotation, it calls the Bitrix24 refresh endpoint.
3. The new token is encrypted and stored; the old token is discarded.
4. An audit event is written: `token_rotation` / `success`.

## Manual Rotation

```bash
# Execute the rotation script
./scripts/rotate-oauth-token.sh

# Verify the new token was stored
python -c "from jol_bitrix24_integration.auth.oauth import OAuthManager; ..."
```

## Emergency Revocation (Offboarding)

```bash
# Revoke the current token
python -c "
from jol_bitrix24_integration.auth.token_rotation import TokenRotationManager
manager.revoke(current_token, reason='offboarding_user_xyz')
"
```

## Monitoring

- Warning alerts fire **14 days** before token expiry.
- Failed rotations trigger an immediate alert.
- All rotation events are in the audit log: `event_type=token_rotation`.

## Troubleshooting

| Issue | Check | Fix |
|-------|-------|-----|
| Rotation fails | Bitrix24 API reachable? | Check network/TLS |
| Token expired | `TOKEN_ROTATION_INTERVAL_DAYS` | Force manual rotation |
| Decryption fails | `TOKEN_ENCRYPTION_KEY` changed? | Restore from backup |
