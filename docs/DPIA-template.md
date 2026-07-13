# Data Protection Impact Assessment (DPIA) Template

> **⚠️ TEMPLATE — This document must be completed and approved by the DPO before production deployment.**

## 1. Processing Description

| Field | Value |
|-------|-------|
| **Project** | JOL-Bitrix24 CRM Integration |
| **Controller** | Journey Of Life |
| **Processor** | Journey Of Life (internal) |
| **Sub-processor** | Bitrix24 Enterprise On-Premise (self-hosted on JOL Proxmox) |
| **Data subjects** | ~400,000 religious institution contacts across 27 EU countries |
| **Data categories** | Name, email, phone, address, organisational affiliation |
| **Legal basis** | [TO BE DETERMINED — legitimate interest / consent / contract] |

## 2. Necessity and Proportionality

- [ ] Purpose limitation documented
- [ ] Data minimisation verified (only required fields synced)
- [ ] Retention periods defined
- [ ] Data subject rights process documented

## 3. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Unauthorised access to CRM data | Low | High | OAuth2 + encrypted tokens + on-premise infrastructure |
| Data breach via API | Low | High | Least-privilege scopes + TLS + audit logging |
| Forged webhook events | Low | Medium | HMAC-SHA256 signature verification |
| Token compromise | Low | High | 90-day rotation + Fernet encryption at rest |
| Cross-border data transfer | Very Low | High | On-premise — no transfer outside JOL EU infrastructure |

## 4. Safeguards

- [ ] Encryption at rest (tokens)
- [ ] Encryption in transit (TLS)
- [ ] Access controls (RBAC)
- [ ] Audit logging (PII-safe)
- [ ] Incident response playbook
- [ ] DPA with Bitrix24 (N/A — self-hosted on JOL infrastructure)

## 5. Sign-off

| Role | Name | Date | Status |
|------|------|------|--------|
| DPO | [TO BE ASSIGNED] | — | Pending |
| CISO | [TO BE ASSIGNED] | — | Pending |
| Engineering Lead | [TO BE ASSIGNED] | — | Pending |
