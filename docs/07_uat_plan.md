# 07 · User Acceptance Testing (UAT) Plan & Results

Full test pack with steps, preconditions and expected results: [`uat/uat_test_cases.xlsx`](../uat/uat_test_cases.xlsx).

## Approach

- **Objective:** confirm the configured QDMS workflow, SAP look-ups and credit-note hand-off meet the [BRD](05_requirements_brd.md) before go-live.
- **Scope:** FR-01 to FR-14, NFR-01 and NFR-02. FR-15 is out of scope (phase 2). NFR-03 and NFR-05 are verified by configuration review with Internal Audit, not by test execution.
- **Environment:** QDMS test instance connected to the SAP QA client; anonymised copy of 2024 master data; test clock for SLA scenarios.
- **Test data:** 30 real 2024 complaint packs (e-mails, photos, customer 8D forms) re-registered in the new screens, plus edge-case records (obsolete material, unmapped product family, high-value credit note).
- **Testers:** four Customer Quality engineers, Finance clerk (TC-17 to TC-21), team lead; the BA facilitates and triages defects with IT daily.
- **Cycles:** Cycle 1 (2 weeks, Nov 2024) → fixes → Cycle 2 retest of failed cases plus regression of related cases (1 week, Dec 2024).

## Entry criteria

- BRD v1.2 signed off; test cases peer-reviewed and traced to requirements
- Build deployed to test with release notes; SAP QA look-up service available
- Test users created with production-like roles; test data loaded

## Exit criteria

- 100% of test cases executed; all Must requirements passed
- No open Critical or Major defects; Minor defects have an agreed fix date or workaround
- Controlled registration trial completed (old vs new screen, 10 paired complaints)
- Sign-off from Head of Quality, Finance Controller and IT Lead

## Defect severity

| Severity | Definition |
|---|---|
| Critical | Blocks a business process or corrupts data (e.g. Finance cannot post) — no workaround |
| Major | Requirement not met; workaround exists but is not acceptable for go-live |
| Minor | Cosmetic or low impact; does not affect data or process outcome |

## Results

<!-- UATSUMMARY:START -->
**25 test cases** executed over two cycles: 20 passed first time, 5 failed and passed on retest. **5 defects** raised (1 critical, 3 major, 1 minor), all fixed and retested before sign-off.
<!-- UATSUMMARY:END -->

### Test cases

<!-- TESTCASES:START -->
| Test ID | Title | Requirement | User story | Cycle 1 | Cycle 2 (retest) | Defect ID |
|---|---|---|---|---|---|---|
| TC-01 | Valid customer number auto-fills customer data | FR-01 | US-01 | Pass | - |  |
| TC-02 | Invalid customer number rejected | FR-01 | US-01 | Pass | - |  |
| TC-03 | Valid material code auto-fills material data | FR-02 | US-02 | Pass | - |  |
| TC-04 | Obsolete material triggers warning | FR-02 | US-02 | Fail | Pass | DEF-01 |
| TC-05 | Save blocked when batch number missing | FR-03 | US-03 | Pass | - |  |
| TC-06 | Save succeeds with all mandatory fields | FR-03 | US-03 | Pass | - |  |
| TC-07 | Defect picklist filtered by product family | FR-04 | US-04 | Fail | Pass | DEF-05 |
| TC-08 | Free text not accepted as defect code | FR-04 | US-04 | Pass | - |  |
| TC-09 | Duplicate customer reference warning | FR-05 | US-05 | Pass | - |  |
| TC-10 | Auto-assignment for mapped product family | FR-06 | US-06 | Pass | - |  |
| TC-11 | Unmapped product family goes to team lead queue | FR-06 | US-06 | Pass | - |  |
| TC-12 | Reminder at 1 day without first response | FR-07 | US-07 | Pass | - |  |
| TC-13 | Escalation at 1.5 days without first response | FR-07 | US-07 | Fail | Pass | DEF-02 |
| TC-14 | Cannot enter D5 without verified root cause | FR-08 | US-08 | Pass | - |  |
| TC-15 | Closure requires D8 fields and customer confirmation | FR-08 | US-08 | Pass | - |  |
| TC-16 | Overdue corrective action notification | FR-09 | US-09 | Pass | - |  |
| TC-17 | Credit note EUR 1,500 routed to team lead only | FR-10 | US-10 | Pass | - |  |
| TC-18 | Credit note EUR 4,800 routed to QM then Finance | FR-10 | US-10 | Pass | - |  |
| TC-19 | Rejected credit note returns with mandatory comment | FR-10 | US-10 | Pass | - |  |
| TC-20 | Approval audit trail recorded and locked | FR-11 | US-11 | Pass | - |  |
| TC-21 | Approved credit note in SAP hand-off file | FR-12 | US-12 | Fail | Pass | DEF-03 |
| TC-22 | Weekly KPI extract reconciles with case list | FR-13 | US-13 | Fail | Pass | DEF-04 |
| TC-23 | Attach three photos up to 10 MB | FR-14 | US-14 | Pass | - |  |
| TC-24 | Engineer role cannot approve credit notes | NFR-02 | US-10 | Pass | - |  |
| TC-25 | SAP look-up response time | NFR-01 | US-01, US-02 | Pass | - |  |
<!-- TESTCASES:END -->

### Defect log

<!-- DEFECTS:START -->
| Defect ID | Test ID | Description | Severity | Status |
|---|---|---|---|---|
| DEF-01 | TC-04 | Obsolete material accepted without warning (status field not mapped) | Major | Fixed - retest passed |
| DEF-02 | TC-13 | Escalation sent to original engineer's lead after reassignment | Major | Fixed - retest passed |
| DEF-03 | TC-21 | Hand-off file used comma decimal separator; SAP import rejected rows | Critical | Fixed - retest passed |
| DEF-04 | TC-22 | Reopened cases counted twice in weekly received volume | Major | Fixed - retest passed |
| DEF-05 | TC-07 | Two retired defect codes still shown for Brake chambers | Minor | Fixed - retest passed |
<!-- DEFECTS:END -->

### Controlled registration trial

Ten 2024 complaint packs were registered by the same engineers in the old screen and in the new screen (order alternated to limit learning effects). Results are computed in [`scripts/analyse.py`](../scripts/analyse.py) from [`data/registration_trial.csv`](../data/registration_trial.csv) and summarised in the [README](../README.md#headline-results).

## Sign-off

| Role | Name | Decision | Date |
|---|---|---|---|
| Head of Quality | (fictional) | Approved for go-live | 18 Dec 2024 |
| Finance Controller | (fictional) | Approved — FR-10 to FR-12 | 18 Dec 2024 |
| IT Lead | (fictional) | Approved | 19 Dec 2024 |
| Customer Quality Team Lead (BA) | (fictional) | Approved | 18 Dec 2024 |
