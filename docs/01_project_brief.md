# 01 · Project Brief

**Project:** Customer complaint handling — process redesign
**Organisation:** Kestrel Components Ltd. (fictional automotive suspension & brake components manufacturer, ~1,100 staff, OEM and aftermarket customers)
**Sponsor:** Head of Quality · **Business Analyst / Process Owner:** Customer Quality Team Lead · **Delivery partner:** IT (SAP & QDMS team)
**Timeline:** Discovery Jul 2024 → Design & build Sep–Dec 2024 → Go-live 13 Jan 2025 → Pilot measurement Feb–Apr 2025

## Background

Customer complaints from truck, bus and trailer OEMs and aftermarket distributors arrive by e-mail, customer portal and phone. A six-engineer Customer Quality team registers each complaint in the QDMS (quality document management system), sends a first response with containment actions, and leads an 8D investigation with Manufacturing. Where the customer is compensated, a credit note is raised and approved on paper before Finance posts it in SAP.

Complaint volume has grown to roughly 3,900 cases a year. OEM customers score suppliers on response speed, and two key accounts flagged slow first responses in their 2024 supplier reviews.

## Problem statement

> Registering a complaint takes too long and produces incomplete records, because engineers re-key customer and material data from e-mails and SAP by hand and the QDMS does not enforce mandatory fields. Incomplete records are sent back for correction, first responses miss the customer's 1.5-day expectation, and paper credit-note approval adds about a week before cases can close. Management reporting is compiled manually in Excel each week.

## Baseline (as-is, 2024)

<!-- BASELINE:START -->
Measured on 3,855 complaints received in 2024:

| KPI | Unit | Baseline | Target |
|---|---|---|---|
| Registration effort (median) | min | 14.2 | -15% vs baseline |
| Received to registered (median) | hours | 20.3 | - |
| First response time (mean) | days | 3.0 | <= 1.5 |
| First response within 1.5 days | % | 22.1 | - |
| Closure time (mean) | days | 16.1 | <= 14 |
| Closed within 14 days | % | 40.5 | - |
| Data completeness at registration | % | 76.0 | >= 95% |
| Rework rate (records sent back) | % | 16.3 | <= 5% |
| Credit-note approval cycle (median) | days | 5.7 | <= 2 |

Largest single wait in the as-is flow: **Credit note requested -> Credit note approved** (median 138.0 h).
<!-- BASELINE:END -->

## Business objectives

| # | Objective | Measure | Target |
|---|---|---|---|
| O1 | Cut the manual effort of registering a complaint | Median registration effort (min) | −15% vs baseline |
| O2 | Respond to customers within their expectation | Mean first-response time | ≤ 1.5 days |
| O3 | Close complaints faster | Mean closure time | ≤ 14 days |
| O4 | Capture complete, analysable data first time | Records with all mandatory fields | ≥ 95% |
| O5 | Stop records bouncing back for correction | Rework rate | ≤ 5% |
| O6 | Remove paper from credit-note approval | Median approval cycle | ≤ 2 days |

## Scope

| In scope | Out of scope |
|---|---|
| Complaint intake and registration in QDMS | Replacing QDMS with a new system |
| SAP customer-master and material-master look-ups (read only) | Changes to SAP FI posting logic |
| Assignment, first-response SLA and escalation | Supplier (incoming) complaint process |
| 8D stage gates in QDMS | Warranty claims from end users |
| Credit-note request and approval workflow + hand-off file to Finance | Customer portal redesign |
| Weekly KPI extract for management | BI platform / dashboards beyond the KPI extract |

## Assumptions

- SAP customer and material master data are accurate enough to be the single source for registration (validated on a 200-record sample during discovery).
- QDMS supports configurable mandatory fields, picklists and workflow; no custom development of the core product is needed.
- IT can provide a read-only SAP look-up service within the existing integration layer.
- Complaint volumes and mix in the pilot period are comparable to 2024.

## Constraints

- IT capacity: one QDMS configurator and one SAP integration developer, part-time (≈40%).
- No change to how Finance posts credit notes in SAP; the workflow must hand off, not post.
- IATF 16949 record-keeping: approval evidence must be retained and auditable.
- Go-live must avoid the December shipment peak.

## Success measures and governance

KPIs O1–O6 are tracked weekly from the QDMS extract and reviewed monthly at the Quality steering meeting (Head of Quality, Customer Quality Team Lead, IT lead, Finance controller). Benefits are reviewed formally at the end of the three-month pilot ([08 · Rollout & change](08_rollout_and_change.md)).
