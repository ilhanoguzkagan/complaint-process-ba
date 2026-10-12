# 08 · Rollout, Training & Change Management

## Rollout plan

| Phase | Dates | What happens | Exit check |
|---|---|---|---|
| Readiness | 6–10 Jan 2025 | Ownership matrix published; defect catalogue loaded; approver roles set in QDMS | Go/no-go checklist signed by Head of Quality |
| Go-live | 13 Jan 2025 | All new complaints registered in the new screens; open cases stay in old flow until closed | First 50 cases spot-checked by BA |
| Hypercare | 13 Jan – 7 Feb 2025 | Daily 15-min stand-up with CQ team and IT; issue log; quick fixes | Issue log has no open high-priority items |
| Pilot measurement | 1 Feb – 30 Apr 2025 | KPIs tracked weekly against 2024 baseline | Benefits review at steering meeting |
| Handover | May 2025 | Process documented in QMS; KPI extract owned by team lead | Work instruction released under document control |

January is treated as a stabilisation month and excluded from the pilot comparison.

## Training plan

| Audience | Format | Duration | Content | Material |
|---|---|---|---|---|
| CQ engineers (6) | Hands-on session on test system + practice on 5 real cases | 2 h | New registration screen, mandatory fields, defect catalogue, 8D stage gates | Quick-reference card, work instruction |
| CQ team lead | 1:1 walkthrough | 1 h | Queue management, escalations, KPI extract | Work instruction |
| Manufacturing owners | Briefing at production meeting | 30 min | Ownership matrix, updating actions in QDMS, overdue alerts | One-page guide |
| Approvers (QM, Finance) | Short demo | 30 min | Approving / rejecting credit notes, audit trail | One-page guide |
| Finance clerk | Hands-on with hand-off file | 45 min | Importing the daily file into SAP FI | Step-by-step guide |

## Change management

The change is mostly to **how people work**, not just the system, so adoption was planned using the ADKAR model:

| ADKAR stage | Risk | Action |
|---|---|---|
| Awareness | Engineers see it as "more fields to fill in" | Shared the as-is pain points and baseline numbers in a team meeting |
| Desire | Manufacturing sees QDMS updates as extra admin | Agreed ownership matrix with department heads; alerts replace chasing e-mails |
| Knowledge | Mixed SAP familiarity across the team | Hands-on training on real cases; quick-reference card |
| Ability | Old habits (registering from inbox later in the day) | Hypercare stand-ups; SLA timer makes delays visible |
| Reinforcement | Drift back to e-mail updates | Weekly KPI review per engineer and per department; work instruction under QMS control |

## Communication plan

| Audience | Message | Channel | When |
|---|---|---|---|
| Whole CQ team | Why we change, what changes for you | Team meeting | Discovery and 2 weeks before go-live |
| Manufacturing heads | Ownership matrix and alerts | Production meeting | 3 weeks before go-live |
| Finance | New approval route and hand-off file | Workshop and e-mail | Design sign-off and go-live week |
| Key account managers | Faster responses; how to see case status | E-mail briefing | Go-live week |
| Steering group | Status, risks, KPIs | Monthly one-pager | Monthly |

## Benefits realisation tracking

| KPI | Owner | Source | Frequency | Target |
|---|---|---|---|---|
| Registration effort (median min) | CQ Team Lead | QDMS time-stamps + quarterly time study | Quarterly | −15% vs 2024 |
| First-response time (mean days) | CQ Team Lead | Weekly KPI extract | Weekly | ≤ 1.5 |
| Closure time (mean days) | CQ Team Lead | Weekly KPI extract | Weekly | ≤ 14 |
| Data completeness at registration | CQ Team Lead | Weekly KPI extract | Weekly | ≥ 95% |
| Rework rate | CQ Team Lead | QDMS "returned for correction" flag | Monthly | ≤ 5% |
| Credit-note approval cycle (median days) | Finance Controller | Approval audit trail | Monthly | ≤ 2 |

Pilot results against these targets are in the [executive summary](00_executive_summary.md). Targets not met are carried into the improvement backlog rather than re-baselined.
