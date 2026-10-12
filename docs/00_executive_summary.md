# 00 · Executive Summary

**Customer complaint handling redesign — Kestrel Components Ltd. (fictional)** · Pilot review, May 2025

## Situation

The Customer Quality team handles about 3,900 OEM and aftermarket complaints a year. In 2024, first responses averaged around three days against a customer expectation of 1.5, a quarter of records were incomplete at registration, and paper credit-note approval held cases open for about a week. Two key OEM accounts raised response time in their supplier reviews.

## What we found

- **Data was entered twice.** Engineers re-keyed customer and part data already held in SAP, and QDMS did not enforce mandatory fields — so records came back for correction.
- **Cases waited for people, not work.** Apart from the engineering investigation, the longest waits were paper credit-note approval, the gap between receipt and first response, and waiting for the team lead to assign an owner.
- **Problems were seen too late.** No SLA timer, and KPIs were compiled manually once a week.

## What we changed

SAP master-data look-ups and mandatory fields at registration; automatic assignment by product family; first-response SLA alerts; 8D stage gates; digital, value-based credit-note approval with an audit trail and a hand-off file to SAP Finance; an automated weekly KPI extract. No new system was bought — QDMS was reconfigured and connected to SAP. Delivered with 14 functional requirements, 25 UAT test cases (5 defects found and fixed before go-live) and role-based training.

## Results (pilot Feb–Apr 2025 vs 2024)

<!-- RESULTS:START -->
Synthetic data: 3,855 baseline complaints (Jan-Dec 2024) vs 968 pilot complaints (Feb-Apr 2025).

| KPI | Unit | Baseline | Pilot | Change | Target | Target met |
|---|---|---|---|---|---|---|
| Registration effort (median) | min | 14.2 | 11.6 | -18% | -15% vs baseline | Yes |
| Received to registered (median) | hours | 20.3 | 4.0 | -80% | - | - |
| First response time (mean) | days | 3.0 | 1.2 | -60% | <= 1.5 | Yes |
| First response within 1.5 days | % | 22.1 | 71.6 | +49.5 pp | - | - |
| Closure time (mean) | days | 16.1 | 11.4 | -29% | <= 14 | Yes |
| Closed within 14 days | % | 40.5 | 78.1 | +37.6 pp | - | - |
| Data completeness at registration | % | 76.0 | 97.4 | +21.4 pp | >= 95% | Yes |
| Rework rate (records sent back) | % | 16.3 | 6.6 | -9.7 pp | <= 5% | No |
| Credit-note approval cycle (median) | days | 5.7 | 1.1 | -81% | <= 2 | Yes |

**Controlled registration trial (10 paired complaints):** 14.6 -> 12.0 min on average, **17.3% faster** (95% CI of saving: 2.0-3.0 min per complaint).

**Estimated capacity released:** ~762 hours per year (~0.5 FTE) - see [benefit case](../outputs/benefit_case.csv) for assumptions.
<!-- RESULTS:END -->

## What still needs work

1. **Rework is down sharply but still above the 5% target.** Next step: add a rework reason code to see why complete records are still sent back; a batch look-up from the delivery note is the leading candidate fix.
2. **The investigation phase did not get faster.** Time from assignment to confirmed root cause is unchanged; the next improvement cycle should target Manufacturing's investigation capacity and standard RCA templates.
3. **Mean first response meets target, but more than a quarter of cases are still late.** Proposed: report the % within 1.5 days as the primary KPI and set a 90% goal.

## Recommendation

Adopt the redesigned process as standard work under the QMS, keep the weekly KPI review, and approve phase 2 (customer-portal intake and batch capture) for H2 2025.
