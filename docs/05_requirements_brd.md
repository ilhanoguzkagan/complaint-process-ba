# 05 · Business Requirements Document (BRD)

**Version:** 1.2 (baselined for build, Oct 2024) · **Owner:** Customer Quality Team Lead · **Approvers:** Head of Quality, Finance Controller (FR-10 to FR-12), IT Lead

Priorities use MoSCoW: **M**ust, **S**hould, **C**ould, **W**on't (this release).

## 1. Business requirements

| ID | Business requirement | Objective | Priority |
|---|---|---|---|
| BR-01 | Reduce the manual effort and errors of registering a complaint | O1, O5 | M |
| BR-02 | Send a first response to the customer within 1.5 days | O2 | M |
| BR-03 | Reduce complaint closure time to 14 days or less | O3 | M |
| BR-04 | Capture complete, standardised complaint data at registration | O4 | M |
| BR-05 | Replace paper credit-note approval with an auditable digital workflow | O6 | M |
| BR-06 | Provide one consistent weekly KPI view for management | O1–O6 | S |

## 2. Functional requirements

| ID | Requirement | Traces to | Priority |
|---|---|---|---|
| FR-01 | When a valid SAP customer number is entered, the system shall auto-fill customer name, country, account manager and customer type; invalid numbers shall be rejected with a message. | BR-01, BR-04 | M |
| FR-02 | When a material code is entered, the system shall auto-fill description, product family and plant from the SAP material master and warn if the material is blocked or obsolete. | BR-01, BR-04 | M |
| FR-03 | The system shall not save a complaint unless all mandatory fields are complete (see §4). | BR-04 | M |
| FR-04 | Defect type shall be selected from a controlled defect catalogue, filtered by product family; free text is allowed only as an additional description. | BR-04 | M |
| FR-05 | The system shall warn when a complaint with the same customer number and customer reference already exists and allow the user to link it. | BR-01 | S |
| FR-06 | On first response, the system shall assign the investigation to the owning department and engineer using the product-family ownership matrix; unmapped families go to the team lead queue. | BR-02, BR-03 | M |
| FR-07 | The system shall alert the assigned engineer when no first response is logged 1 day after receipt and escalate to the team lead at 1.5 days. | BR-02 | M |
| FR-08 | The case shall move through 8D stages (D1–D8); each stage requires its mandatory fields before the next can start, and closure requires D8 fields and customer confirmation. | BR-03 | M |
| FR-09 | The system shall notify the department owner and engineer when a corrective action passes its due date, and daily until updated. | BR-03 | S |
| FR-10 | A credit note shall be requested inside the case and routed for approval by value: ≤ €2,000 team lead; > €2,000 Quality Manager then Finance Controller. A rejection returns the request to the requester with a mandatory comment. | BR-05 | M |
| FR-11 | Every approval or rejection shall record approver, timestamp, decision and comment; records cannot be edited or deleted. | BR-05 | M |
| FR-12 | Approved credit notes shall be written to a daily hand-off file for SAP FI with customer number, amount (EUR, dot decimal), complaint ID and cost centre. | BR-05 | M |
| FR-13 | The system shall produce a weekly KPI extract: complaints received, defective quantity, credit-note value, first-response and closure performance, open and overdue actions. | BR-06 | S |
| FR-14 | Users shall attach photos and customer documents (up to 10 MB per file) to a case. | BR-01 | S |
| FR-15 | Customers shall log complaints directly into QDMS through the customer portal. | BR-01 | W |

## 3. Non-functional requirements

| ID | Requirement | Priority |
|---|---|---|
| NFR-01 | SAP look-ups return within 2 seconds for 95% of requests during business hours. | M |
| NFR-02 | Role-based access: engineers create and update cases; only defined approver roles can approve credit notes. | M |
| NFR-03 | Approval and case records retained for 15 years to meet IATF 16949 and customer-specific record retention. | M |
| NFR-04 | Registration completed on a single screen with no more than 10 manual inputs. | S |
| NFR-05 | Personal data limited to business contact details (GDPR data minimisation). | M |

## 4. Data requirements

| Field | Source | Mandatory | Validation rule |
|---|---|---|---|
| Customer number | SAP customer master (KNA1) | Yes | Must exist and not be flagged for deletion |
| Customer name, country, account manager | SAP customer master | Auto | Read-only, filled from customer number |
| Customer reference | Customer document | Yes | Free text, 3–35 characters; duplicate check (FR-05) |
| Material code | SAP material master (MARA) | Yes | Must exist; warn if status blocked/obsolete |
| Material description, product family, plant | SAP material master | Auto | Read-only, filled from material code |
| Batch / lot number | Customer document or label photo | Yes | Format `YYWW-NNNN`; `UNKNOWN` allowed with reason |
| Defect code | QDMS defect catalogue | Yes | Picklist filtered by product family |
| Quantity defective | Customer document | Yes | Integer ≥ 1 |
| Date received | System | Auto | Timestamp of record creation or e-mail receipt |
| Credit-note amount | CQ engineer | If credit note | EUR > 0, two decimals |
| Cost centre | SAP CO (by product family) | If credit note | Must exist in SAP |

## 5. Requirements traceability matrix

| Business req. | Functional req. | User story | Test cases |
|---|---|---|---|
| BR-01 | FR-01 | US-01 | TC-01, TC-02 |
| BR-01 | FR-02 | US-02 | TC-03, TC-04 |
| BR-04 | FR-03 | US-03 | TC-05, TC-06 |
| BR-04 | FR-04 | US-04 | TC-07, TC-08 |
| BR-01 | FR-05 | US-05 | TC-09 |
| BR-02, BR-03 | FR-06 | US-06 | TC-10, TC-11 |
| BR-02 | FR-07 | US-07 | TC-12, TC-13 |
| BR-03 | FR-08 | US-08 | TC-14, TC-15 |
| BR-03 | FR-09 | US-09 | TC-16 |
| BR-05 | FR-10 | US-10 | TC-17, TC-18, TC-19 |
| BR-05 | FR-11 | US-11 | TC-20 |
| BR-05 | FR-12 | US-12 | TC-21 |
| BR-06 | FR-13 | US-13 | TC-22 |
| BR-01 | FR-14 | US-14 | TC-23 |
| BR-05 | NFR-02 | US-10 | TC-24 |
| BR-01 | NFR-01 | US-01, US-02 | TC-25 |

FR-15 (customer portal intake) is out of scope for this release and is logged for phase 2.
