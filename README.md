# Customer Complaint Handling — Process Redesign
### A Business Analysis case study: from as-is mapping to UAT sign-off and measured benefits

**Author:** Oguzkagan Ilhan · Industrial Engineer · [LinkedIn](https://www.linkedin.com/in/oguzkagan-ilhan-29620085)
**Interactive dashboard:** [`dashboard/index.html`](dashboard/index.html) (published via GitHub Pages)

> **About this case study.** Kestrel Components Ltd., its people, customers and all data in this repository are **fictional and synthetic**. The project is a reconstruction of a complaint-workflow redesign I led as Customer Quality Team Lead at an automotive components manufacturer — defining SAP-linked data requirements with IT, testing revisions, training users and measuring the new process against the old one. Company details and figures have been replaced so the methodology can be shown in full; every number below is computed from the generated data by the scripts in this repo.

## The problem

A six-engineer Customer Quality team registers ~3,900 complaints a year from truck, bus and trailer OEMs and aftermarket distributors. Engineers re-keyed customer and part data from e-mails and SAP, records were often incomplete, first responses missed the customer's 1.5-day expectation, and credit notes were approved on paper. → [Project brief](docs/01_project_brief.md)

## Approach

| BA phase | What I did | Artefact |
|---|---|---|
| Define | Problem statement, SMART objectives, scope, assumptions, constraints | [01 Project brief](docs/01_project_brief.md) |
| Engage | Stakeholder register, power/interest grid, RACI | [02 Stakeholder analysis](docs/02_stakeholder_analysis.md) |
| Analyse as-is | Swimlane map, step analysis by waste type, 5 Whys, fishbone, event-log baseline | [03 As-is process](docs/03_as_is_process.md) |
| Design to-be | Target process, change rationale, gap analysis | [04 To-be process](docs/04_to_be_process.md) |
| Specify | Business / functional / non-functional / data requirements, MoSCoW, traceability matrix | [05 BRD](docs/05_requirements_brd.md) |
| Refine | 14 user stories with Gherkin acceptance criteria | [06 User stories](docs/06_user_stories.md) |
| Validate | UAT plan, 25 test cases, defect log, controlled old-vs-new trial, sign-off | [07 UAT](docs/07_uat_plan.md) · [test pack (xlsx)](uat/uat_test_cases.xlsx) |
| Deliver & embed | Rollout, training, ADKAR change plan, benefits tracking | [08 Rollout & change](docs/08_rollout_and_change.md) |
| Report | One-page summary for the sponsor | [00 Executive summary](docs/00_executive_summary.md) |

## Headline results

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

**Estimated capacity released:** ~762 hours per year (~0.5 FTE) - see [benefit case](outputs/benefit_case.csv) for assumptions.
<!-- RESULTS:END -->

Not everything hit target — rework is still above 5% and the engineering investigation itself did not speed up. Both are carried into the [next improvement cycle](docs/00_executive_summary.md#what-still-needs-work).

## Skills demonstrated

- **Requirements elicitation & documentation** — workshops, process walk-throughs, BRD with business, functional, non-functional and field-level data requirements
- **Process modelling** — BPMN-style swimlanes (as-is / to-be), waste analysis, gap analysis
- **Agile artefacts** — user stories with Gherkin acceptance criteria, MoSCoW prioritisation, end-to-end traceability (BR → FR → US → TC, checked automatically)
- **Testing** — UAT planning, entry/exit criteria, test cases, defect triage, controlled trial with confidence interval
- **Data analysis** — process-mining-style event-log analysis in Python/pandas, KPI definition, benefit case with explicit assumptions
- **Stakeholder & change management** — RACI, power/interest mapping, ADKAR, training and communication plans
- **Domain** — customer quality, 8D, SAP master data (customer / material), credit-note controls, IATF 16949 record-keeping

## How to run

```bash
pip install -r requirements.txt
./run.sh          # generate data -> analyse -> build UAT pack; updates outputs/, dashboard/data.js and the result tables in the docs
```

Open `dashboard/index.html` in a browser to view the dashboard locally.

## Repository structure

```
├── docs/                    BA artefacts 00–08 (Markdown + Mermaid diagrams)
├── data/                    synthetic complaint cases, event log, registration trial (generated)
├── outputs/                 KPI summary, step waiting times, benefit case, results.json (generated)
├── uat/uat_test_cases.xlsx  UAT test pack: summary, test cases, defect log (generated)
├── dashboard/               static before/after dashboard (index.html + generated data.js)
├── scripts/
│   ├── generate_data.py     seeded synthetic data for baseline (2024) and pilot (Feb–Apr 2025)
│   ├── analyse.py           KPIs, step waits, trial statistics, benefit case, doc tables
│   ├── build_uat.py         UAT workbook + traceability check against the BRD
│   └── docblocks.py         writes generated tables into the Markdown docs
└── run.sh
```

## Modelling notes

- Durations are in calendar hours (no working-time calendar), as most OEM response expectations are calendar-based.
- Baseline = all complaints received Jan–Dec 2024; pilot = Feb–Apr 2025. January 2025 is excluded as the go-live stabilisation month.
- Process parameters in `generate_data.py` were set to plausible plant-level values; change the seed or parameters to see how the conclusions hold.
