"""Before/after analysis of the complaint process redesign.

Reads data/*.csv (from generate_data.py) and writes:
  outputs/kpi_summary.csv, outputs/step_waiting_times.csv, outputs/benefit_case.csv, outputs/results.json
  dashboard/data.js  (consumed by dashboard/index.html)
  generated result blocks inside README.md, docs/00_executive_summary.md and docs/01_project_brief.md
"""
import json
from pathlib import Path

import pandas as pd

from docblocks import md_table, replace_block
from generate_data import ACTIVITIES

ROOT = Path(__file__).resolve().parents[1]
T_CRIT_DF9 = 2.262  # two-sided 95% t critical value for 10 paired trials (df = 9)

BENEFIT_ASSUMPTIONS = {
    "rework_minutes_per_case": 25,        # re-open record, chase customer/SAP data, correct, re-notify
    "paper_credit_note_minutes": 18,      # print, collect wet signatures, scan, re-upload
    "digital_credit_note_minutes": 3,     # review and approve in workflow
    "manual_report_hours_per_week": 3,   # weekly CEO KPI pack compiled by hand in Excel
    "reporting_weeks_per_year": 48,
    "productive_hours_per_fte": 1650,
}

# name, unit, target (as text), check(value, baseline) -> met?, metric(group)
KPIS = [
    ("Registration effort (median)", "min", "-15% vs baseline", lambda v, b: v <= .85 * b,
     lambda g: g["registration_minutes"].median()),
    ("Received to registered (median)", "hours", "-", None, lambda g: g["reg_wait_h"].median()),
    ("First response time (mean)", "days", "<= 1.5", lambda v, b: v <= 1.5, lambda g: g["first_response_d"].mean()),
    ("First response within 1.5 days", "%", "-", None, lambda g: 100 * (g["first_response_d"] <= 1.5).mean()),
    ("Closure time (mean)", "days", "<= 14", lambda v, b: v <= 14, lambda g: g["closure_d"].mean()),
    ("Closed within 14 days", "%", "-", None, lambda g: 100 * (g["closure_d"] <= 14).mean()),
    ("Data completeness at registration", "%", ">= 95%", lambda v, b: v >= 95, lambda g: 100 * g["data_complete"].mean()),
    ("Rework rate (records sent back)", "%", "<= 5%", lambda v, b: v <= 5, lambda g: 100 * g["rework"].mean()),
    ("Credit-note approval cycle (median)", "days", "<= 2", lambda v, b: v <= 2, lambda g: g["cn_cycle_d"].median()),
]


def load_cases():
    path = ROOT / "data/complaint_cases.csv"
    cases = pd.read_csv(path, parse_dates=[c for c in pd.read_csv(path, nrows=0).columns if c.endswith("_at")])
    span = lambda a, b: (cases[b] - cases[a]).dt.total_seconds()
    cases["reg_wait_h"] = span("received_at", "registered_at") / 3600
    cases["first_response_d"] = span("received_at", "first_response_at") / 86400
    cases["closure_d"] = span("received_at", "closed_at") / 86400
    cases["cn_cycle_d"] = span("cn_requested_at", "cn_approved_at") / 86400
    return cases


def kpi_table(cases):
    groups = dict(tuple(cases.groupby("period")))
    rows = []
    for name, unit, target, check, metric in KPIS:
        # Round first so the change shown on a card matches the two values printed next to it.
        base, pilot = round(metric(groups["baseline"]), 1), round(metric(groups["pilot"]), 1)
        rows.append({"KPI": name, "Unit": unit, "Baseline": base, "Pilot": pilot,
                     "Change": f"{pilot - base:+.1f} pp" if unit == "%" else f"{(pilot - base) / base:+.0%}",
                     "Target": target,
                     "Target met": "-" if check is None else ("Yes" if check(pilot, base) else "No")})
    return pd.DataFrame(rows)


def step_waits():
    log = pd.read_csv(ROOT / "data/complaint_event_log.csv", parse_dates=["timestamp"])
    log["seq"] = log["activity"].map({a: i for i, a in enumerate(ACTIVITIES)})
    log = log.sort_values(["case_id", "timestamp", "seq"])
    nxt = log.groupby("case_id")[["activity", "timestamp"]].shift(-1)
    log["transition"] = log["activity"] + " -> " + nxt["activity"]
    log["wait_h"] = (nxt["timestamp"] - log["timestamp"]).dt.total_seconds() / 3600
    t = log.dropna(subset=["transition"])
    t = t[t["transition"] != "Corrective action defined -> Credit note requested"]  # same event, zero wait
    out = (t.groupby(["transition", "period"])["wait_h"].agg(["median", "count"]).unstack("period"))
    out.columns = [f"{stat}_{period}" for stat, period in out.columns]
    out["seq"] = t.groupby("transition")["seq"].min()
    out = out.sort_values(["seq", "count_baseline"], ascending=[True, False]).drop(columns="seq")
    return out.reset_index().round(1)


def trial_summary():
    trial = pd.read_csv(ROOT / "data/registration_trial.csv")
    diff = trial["old_process_minutes"] - trial["new_process_minutes"]
    half_width = T_CRIT_DF9 * diff.std(ddof=1) / len(diff) ** .5
    assert len(trial) == 10 and (diff > 0).all()
    return trial, {
        "trials": len(trial),
        "old_mean_min": round(trial["old_process_minutes"].mean(), 1),
        "new_mean_min": round(trial["new_process_minutes"].mean(), 1),
        "pct_faster": round(100 * diff.mean() / trial["old_process_minutes"].mean(), 1),
        "saving_min_ci95": [round(diff.mean() - half_width, 1), round(diff.mean() + half_width, 1)],
    }


def benefit_case(cases):
    a = BENEFIT_ASSUMPTIONS
    base, pilot = cases[cases["period"] == "baseline"], cases[cases["period"] == "pilot"]
    annual_cases, annual_cn = len(base), int(base["credit_note"].sum())
    rows = [
        ("Faster registration", annual_cases,
         (base["registration_minutes"].mean() - pilot["registration_minutes"].mean()) * annual_cases / 60),
        ("Less rework", annual_cases,
         (base["rework"].mean() - pilot["rework"].mean()) * annual_cases * a["rework_minutes_per_case"] / 60),
        ("Digital credit-note approval", annual_cn,
         annual_cn * (a["paper_credit_note_minutes"] - a["digital_credit_note_minutes"]) / 60),
        ("Automated weekly KPI extract", a["reporting_weeks_per_year"],
         a["manual_report_hours_per_week"] * a["reporting_weeks_per_year"]),
    ]
    df = pd.DataFrame(rows, columns=["Benefit", "Annual volume", "Hours saved per year"]).round(0)
    df.loc[len(df)] = ["Total", "", df["Hours saved per year"].sum()]
    fte = df["Hours saved per year"].iloc[-1] / a["productive_hours_per_fte"]
    return df, round(fte, 1)


def monthly(cases):
    m = (cases.assign(month=cases["received_at"].dt.to_period("M").astype(str))
         .groupby(["month", "period"]).agg(cases=("case_id", "size"), first_response_d=("first_response_d", "mean"),
                                           closure_d=("closure_d", "mean"))
         .reset_index().round(2))
    return m


def main():
    cases = load_cases()
    kpis, waits = kpi_table(cases), step_waits()
    trial, trial_stats = trial_summary()
    benefits, fte = benefit_case(cases)
    trend = monthly(cases)

    # sanity: periods present, pilot improves every KPI where lower is better / higher is better
    assert set(cases["period"]) == {"baseline", "pilot"}
    assert kpis.set_index("KPI").loc["First response time (mean)", "Pilot"] < kpis.set_index("KPI").loc["First response time (mean)", "Baseline"]
    assert benefits["Hours saved per year"].iloc[-1] > 0

    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    kpis.to_csv(out / "kpi_summary.csv", index=False)
    waits.to_csv(out / "step_waiting_times.csv", index=False)
    benefits.to_csv(out / "benefit_case.csv", index=False)
    counts = cases["period"].value_counts().to_dict()
    results = {"case_counts": counts, "kpis": kpis.to_dict("records"), "trial": trial_stats,
               "benefit_assumptions": BENEFIT_ASSUMPTIONS, "benefits": benefits.to_dict("records"), "fte_equivalent": fte}
    (out / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))

    dashboard = {**results, "steps": waits.to_dict("records"), "monthly": trend.to_dict("records"),
                 "trial_rows": trial.to_dict("records")}
    (ROOT / "dashboard/data.js").write_text("window.DASHBOARD_DATA = " + json.dumps(dashboard, ensure_ascii=False) + ";\n")

    # generated doc blocks
    k = kpis.set_index("KPI")
    headline = (
        f"Synthetic data: {counts['baseline']:,} baseline complaints (Jan-Dec 2024) vs {counts['pilot']:,} pilot complaints "
        f"(Feb-Apr 2025).\n\n{md_table(kpis)}\n\n"
        f"**Controlled registration trial ({trial_stats['trials']} paired complaints):** {trial_stats['old_mean_min']} -> "
        f"{trial_stats['new_mean_min']} min on average, **{trial_stats['pct_faster']}% faster** "
        f"(95% CI of saving: {trial_stats['saving_min_ci95'][0]}-{trial_stats['saving_min_ci95'][1]} min per complaint).\n\n"
        f"**Estimated capacity released:** ~{benefits['Hours saved per year'].iloc[-1]:,.0f} hours per year "
        f"(~{fte} FTE) - see [benefit case](outputs/benefit_case.csv) for assumptions."
    )
    replace_block(ROOT / "README.md", "RESULTS", headline)
    replace_block(ROOT / "docs/00_executive_summary.md", "RESULTS",
                  headline.replace("(outputs/benefit_case.csv)", "(../outputs/benefit_case.csv)"))
    top = waits.sort_values("median_baseline", ascending=False).iloc[0]
    baseline = kpis[["KPI", "Unit", "Baseline", "Target"]]
    replace_block(ROOT / "docs/01_project_brief.md", "BASELINE",
                  f"Measured on {counts['baseline']:,} complaints received in 2024:\n\n{md_table(baseline)}\n\n"
                  f"Largest single wait in the as-is flow: **{top['transition']}** (median {top['median_baseline']} h).")
    print(kpis.to_string(index=False))
    print(trial_stats)
    print(benefits.to_string(index=False), f"\nFTE: {fte}")


if __name__ == "__main__":
    main()
