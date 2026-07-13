# International Transfer Assessment

> **⚠️ TEMPLATE — Requires legal review.**

## Assessment: NOT REQUIRED

**Rationale:** Bitrix24 Enterprise On-Premise runs entirely on JOL's own
Proxmox infrastructure within the EU. No personal data is transferred to a
third country or international organisation.

### Infrastructure Location

| Component | Location | Country |
|-----------|----------|---------|
| Proxmox VE cluster | JOL data centre | [EU COUNTRY — TO BE SPECIFIED] |
| Bitrix24 Enterprise | VM on above cluster | Same |
| Integration service | Container on same network | Same |
| PostgreSQL database | VM on same cluster | Same |

### Bitrix24 Software Vendor (1C-Bitrix)

- [ ] Verify that Bitrix24 Enterprise On-Premise does not transmit telemetry data to 1C-Bitrix servers (Russia)
- [ ] Disable all outbound telemetry in Bitrix24 configuration
- [ ] Document findings in this assessment

### If Telemetry Cannot Be Disabled

If any data leaves JOL infrastructure to reach 1C-Bitrix servers:
- [ ] Assess transfer mechanism (SCCs, adequacy decision)
- [ ] Conduct Transfer Impact Assessment (TIA) per Schrems II
- [ ] Implement supplementary measures

## Review History

| Date | Reviewer | Outcome |
|------|----------|---------|
| — | — | Pending initial review |
