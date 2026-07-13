# Incident Playbook

> **Status:** TEMPLATE — requires security team review and approval.

## Scope

This playbook covers security incidents specific to the JOL-Bitrix24 integration:
- Token compromise
- Webhook forgery attempts
- Data breach involving CRM records
- Unauthorised API access

## Incident Response Steps

### 1. Token Compromise

| Step | Action | Owner |
|------|--------|-------|
| 1 | Revoke the compromised token immediately | On-call engineer |
| 2 | Rotate the encryption key | Security team |
| 3 | Audit all API calls since last known-good state | Security team |
| 4 | Generate new OAuth tokens | On-call engineer |
| 5 | Write incident report | Incident commander |

### 2. Webhook Forgery

| Step | Action | Owner |
|------|--------|-------|
| 1 | Block the source IP at the firewall | Infrastructure team |
| 2 | Rotate the webhook secret | On-call engineer |
| 3 | Review audit log for successful forgeries | Security team |
| 4 | Update Bitrix24 webhook configuration | On-call engineer |

### 3. Data Breach (CRM Records)

| Step | Action | Owner |
|------|--------|-------|
| 1 | Isolate the affected system | Infrastructure team |
| 2 | Determine scope of data exposure | Security team + DPO |
| 3 | Notify supervisory authority within 72 hours (GDPR Art. 33) | DPO |
| 4 | Notify affected data subjects (GDPR Art. 34) | DPO |
| 5 | Preserve forensic evidence | Security team |

## Contact

- **DPO:** [TO BE ASSIGNED — legal review required]
- **On-call engineer:** See PagerDuty rotation
- **Security team:** security@journeyoflife.org
