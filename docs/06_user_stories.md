# 06 · User Stories

Each story traces to a functional requirement ([BRD](05_requirements_brd.md)) and to UAT test cases ([UAT plan](07_uat_plan.md)). Acceptance criteria are written in Gherkin so they can be tested directly.

---

### US-01 · Customer data from SAP · FR-01 · Must
**As a** Customer Quality engineer **I want** customer details filled from SAP when I enter the customer number **so that** I don't re-key data that already exists.

```gherkin
Scenario: Valid customer number
  Given I am creating a new complaint
  When I enter customer number "100245"
  Then customer name, country, account manager and customer type are filled from SAP
  And those fields are read-only

Scenario: Invalid customer number
  When I enter customer number "999999" that does not exist in SAP
  Then I see "Customer not found in SAP" and the record cannot be saved
```

### US-02 · Material data from SAP · FR-02 · Must
**As a** CQ engineer **I want** material details filled and validated from the material code **so that** wrong or obsolete part numbers are caught at intake.

```gherkin
Scenario: Valid material
  When I enter material code "AS-4410-22"
  Then description, product family "Air springs" and plant are filled from SAP

Scenario: Obsolete material
  When I enter a material code with SAP status "obsolete"
  Then I see a warning and must confirm before continuing
```

### US-03 · Mandatory fields · FR-03 · Must
**As a** CQ team lead **I want** complaints to be saved only when mandatory fields are complete **so that** records do not come back for correction.

```gherkin
Scenario: Missing batch number
  Given all mandatory fields are complete except batch number
  When I click Save
  Then the record is not saved and the batch field is highlighted with "Batch number required"
```

### US-04 · Standard defect codes · FR-04 · Must
**As a** quality analyst **I want** defects selected from a standard catalogue **so that** I can run Pareto analysis without cleaning free text.

```gherkin
Scenario: Picklist filtered by product family
  Given product family is "Brake chambers"
  When I open the defect code list
  Then I only see defect codes valid for "Brake chambers"
```

### US-05 · Duplicate warning · FR-05 · Should
**As a** CQ engineer **I want** a warning if the complaint already exists **so that** two engineers don't investigate the same issue.

```gherkin
Scenario: Same customer reference
  Given complaint CMP-01200 exists for customer "100245" with reference "QN-55871"
  When I register a new complaint with the same customer and reference
  Then I see "Possible duplicate of CMP-01200" with options Link or Continue
```

### US-06 · Automatic assignment · FR-06 · Must
**As a** CQ team lead **I want** investigations assigned automatically by product family **so that** cases don't wait for me to allocate them.

```gherkin
Scenario: Mapped product family
  Given the ownership matrix maps "Air springs" to Assembly Line 2
  When the first response is logged for an "Air springs" complaint
  Then the investigation is assigned to the Assembly Line 2 owner and engineer

Scenario: Unmapped product family
  When the product family has no owner in the matrix
  Then the case goes to the team lead queue
```

### US-07 · First-response escalation · FR-07 · Must
**As a** CQ team lead **I want** to be alerted before a first response becomes late **so that** we meet the customer's 1.5-day expectation.

```gherkin
Scenario: Reminder and escalation
  Given a complaint received at 09:00 on Monday with no first response
  When it is 09:00 on Tuesday
  Then the assigned engineer receives a reminder e-mail
  When it is 21:00 on Tuesday
  Then the team lead receives an escalation e-mail
```

### US-08 · 8D stage gates · FR-08 · Must
**As a** Head of Quality **I want** each 8D stage completed before the next starts **so that** closures are evidence-based and audit-ready.

```gherkin
Scenario: Root cause not verified
  Given a case in stage D4 with "Root cause verified" empty
  When I try to move to D5
  Then I see "Verify root cause before defining corrective actions"
```

### US-09 · Overdue action alerts · FR-09 · Should
**As a** manufacturing department owner **I want** to be told when a corrective action is overdue **so that** I can act before the customer chases.

```gherkin
Scenario: Action passes due date
  Given a corrective action due yesterday that is still open
  Then the action owner and department owner receive an overdue notification each morning until it is updated
```

### US-10 · Digital credit-note approval · FR-10, NFR-02 · Must
**As a** CQ engineer **I want** to request a credit note inside the case and have it routed to the right approver **so that** it is approved without printing and chasing signatures.

```gherkin
Scenario: Low-value credit note
  When I request a credit note of €1,500
  Then it is routed to the team lead only

Scenario: High-value credit note
  When I request a credit note of €4,800
  Then it is routed to the Quality Manager, then the Finance Controller

Scenario: Rejection
  When an approver rejects a request
  Then a comment is mandatory and the request returns to me
```

### US-11 · Approval audit trail · FR-11 · Must
**As an** internal auditor **I want** every approval decision recorded and locked **so that** I can evidence control during IATF and customer audits.

```gherkin
Scenario: Decision recorded
  When an approver approves a credit note
  Then approver, timestamp, decision and comment are stored
  And no user role can edit or delete that entry
```

### US-12 · Hand-off to SAP FI · FR-12 · Must
**As a** Finance clerk **I want** approved credit notes in a structured daily file **so that** I post them in SAP without re-keying from scans.

```gherkin
Scenario: Daily file
  Given two credit notes were approved today
  When the daily hand-off file is generated
  Then it contains two rows with customer number, amount with dot decimal, complaint ID and cost centre
```

### US-13 · Weekly KPI extract · FR-13 · Should
**As the** Head of Quality **I want** a weekly KPI extract generated automatically **so that** the CEO report uses one consistent set of numbers.

```gherkin
Scenario: Figures reconcile
  When the weekly extract runs on Monday 07:00
  Then complaints received, first-response and closure performance match the case list for the previous week
```

### US-14 · Attachments · FR-14 · Should
**As a** CQ engineer **I want** to attach photos and customer documents **so that** evidence is stored with the case, not in my inbox.

```gherkin
Scenario: Attach photos
  When I attach three photos of up to 10 MB each
  Then all three are stored on the case and visible to the assigned engineer
```
