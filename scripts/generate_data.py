"""Generate a synthetic, reproducible complaint dataset for the case study.

Two periods are simulated for the fictional Kestrel Components Ltd.:
  * baseline: the as-is process (manual registration, manual assignment, paper credit-note approval)
  * pilot:    the to-be process after go-live (SAP auto-fill, auto-assignment, digital approval)

Outputs:
  data/complaint_cases.csv      one row per complaint case
  data/complaint_event_log.csv  one row per case x activity (process-mining format)
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SEED = 42

PERIODS = {
    "baseline": ("2024-01-01", "2024-12-31"),
    "pilot": ("2025-02-01", "2025-04-30"),  # Jan 2025 = go-live/stabilisation month, excluded
}
CASES_PER_WORKDAY = 15

CUSTOMERS = {"OEM-01 (Truck)": .24, "OEM-02 (Bus & Coach)": .14, "OEM-03 (Trailer)": .12, "OEM-04 (Truck)": .10,
             "AM-01 (Aftermarket distributor)": .16, "AM-02 (Aftermarket distributor)": .12, "AM-03 (Fleet service)": .12}
FAMILIES = {"Air springs": .34, "Brake chambers": .22, "Suspension bushings": .18, "Torque rods": .14, "Cab mounts": .12}
DEFECTS = {"Leakage": .22, "Dimensional out of spec": .18, "Surface damage": .14, "Transit damage": .14,
           "Wrong part shipped": .10, "Missing component": .09, "Noise / vibration": .13}
CHANNELS = {"Email": .62, "Customer portal": .28, "Phone": .10}
MANDATORY_FIELDS = ["customer_no", "material_code", "batch_no", "defect_code", "qty_defective", "customer_ref"]

# Process parameters: (median, lognormal sigma). Hours unless noted. Tuned to plausible plant-level figures.
PARAMS = {
    "baseline": dict(reg_wait=(20, .9), reg_minutes=(14.0, .22), resp_wait=(27, .8), assign_wait=(18, .7),
                     root_cause=(132, .55), corrective=(48, .5), verify=(40, .5), cn_approval=(140, .5),
                     p_missing_field=.045, p_rework=.07, rework_delay=(24, .5)),
    "pilot": dict(reg_wait=(4, .9), reg_minutes=(11.6, .2), resp_wait=(16, .8), assign_wait=(1.5, .7),
                  root_cause=(128, .55), corrective=(40, .5), verify=(36, .5), cn_approval=(28, .5),
                  p_missing_field=.004, p_rework=.04, rework_delay=(24, .5)),
}
P_CREDIT_NOTE = .30
ACTIVITIES = ["Complaint received", "Registered in QDMS", "First response sent", "Investigation assigned",
              "Root cause confirmed", "Corrective action defined", "Credit note requested", "Credit note approved",
              "Case closed"]


def lognormal(rng, median_sigma, n):
    median, sigma = median_sigma
    return rng.lognormal(np.log(median), sigma, n)


def pick(rng, weights, n):
    return rng.choice(list(weights), size=n, p=list(weights.values()))


def simulate(period, start, end, rng):
    days = pd.bdate_range(start, end)
    per_day = rng.poisson(CASES_PER_WORKDAY, len(days))
    received = np.concatenate([d + pd.to_timedelta(rng.uniform(7, 18, k), unit="h") for d, k in zip(days, per_day)])
    n, p = len(received), PARAMS[period]
    hours = lambda key: pd.to_timedelta(lognormal(rng, p[key], n), unit="h")

    df = pd.DataFrame({
        "period": period,
        "received_at": pd.to_datetime(received),
        "customer": pick(rng, CUSTOMERS, n),
        "product_family": pick(rng, FAMILIES, n),
        "defect_type": pick(rng, DEFECTS, n),
        "channel": pick(rng, CHANNELS, n),
        "qty_defective": rng.geometric(.08, n),
        "registration_minutes": lognormal(rng, p["reg_minutes"], n).round(1),
    })
    missing = rng.random((n, len(MANDATORY_FIELDS))) < p["p_missing_field"]
    df["missing_fields"] = [";".join(f for f, m in zip(MANDATORY_FIELDS, row) if m) for row in missing]
    df["data_complete"] = ~missing.any(axis=1)
    # incomplete records are far more likely to bounce back for correction
    df["rework"] = rng.random(n) < np.where(df["data_complete"], p["p_rework"], .45)
    df["credit_note"] = rng.random(n) < P_CREDIT_NOTE
    df["claim_value_eur"] = np.where(df["credit_note"], (df["qty_defective"] * rng.uniform(35, 160, n)).round(2), 0.0)

    rework_delay = np.where(df["rework"], lognormal(rng, p["rework_delay"], n), 0)
    df["registered_at"] = df["received_at"] + hours("reg_wait")
    df["first_response_at"] = df["registered_at"] + hours("resp_wait") + pd.to_timedelta(rework_delay, unit="h")
    df["assigned_at"] = df["first_response_at"] + hours("assign_wait")
    df["root_cause_at"] = df["assigned_at"] + hours("root_cause")
    df["corrective_action_at"] = df["root_cause_at"] + hours("corrective")
    df["cn_requested_at"] = df["corrective_action_at"].where(df["credit_note"])
    df["cn_approved_at"] = df["cn_requested_at"] + hours("cn_approval")
    verified = df["corrective_action_at"] + hours("verify")
    close_out = pd.to_timedelta(lognormal(rng, (4, .6), n), unit="h")  # final 8D report and closure admin
    df["closed_at"] = pd.concat([verified, df["cn_approved_at"]], axis=1).max(axis=1) + close_out
    return df


def registration_trial(rng, n=10):
    """Controlled old-vs-new test: the same 10 real-world complaint packs registered in both screens."""
    old = rng.normal(14.2, 2.0, n).round(1)
    new = (old * rng.normal(0.83, 0.04, n)).round(1)
    return pd.DataFrame({"trial": range(1, n + 1), "defect_type": pick(rng, DEFECTS, n),
                         "old_process_minutes": old, "new_process_minutes": new})


def main():
    rng = np.random.default_rng(SEED)
    cases = pd.concat([simulate(k, *v, rng) for k, v in PERIODS.items()], ignore_index=True)
    cases.insert(0, "case_id", [f"CMP-{i:05d}" for i in range(1, len(cases) + 1)])

    ts_cols = ["received_at", "registered_at", "first_response_at", "assigned_at", "root_cause_at",
               "corrective_action_at", "cn_requested_at", "cn_approved_at", "closed_at"]
    log = (cases.melt(id_vars=["case_id", "period"], value_vars=ts_cols, var_name="step", value_name="timestamp")
           .dropna(subset=["timestamp"]))
    log["activity"] = log["step"].map(dict(zip(ts_cols, ACTIVITIES)))
    log["seq"] = log["step"].map({c: i for i, c in enumerate(ts_cols)})  # breaks timestamp ties in process order
    log = log.sort_values(["case_id", "timestamp", "seq"])[["case_id", "period", "activity", "timestamp"]]
    trial = registration_trial(rng)

    assert cases["case_id"].is_unique
    assert (cases["closed_at"] > cases["received_at"]).all()
    assert (cases["first_response_at"] >= cases["registered_at"]).all()
    assert len(log) == len(cases) * 7 + 2 * cases["credit_note"].sum()

    out = ROOT / "data"
    out.mkdir(exist_ok=True)
    cases.round({"claim_value_eur": 2}).to_csv(out / "complaint_cases.csv", index=False, date_format="%Y-%m-%d %H:%M")
    log.to_csv(out / "complaint_event_log.csv", index=False, date_format="%Y-%m-%d %H:%M")
    trial.to_csv(out / "registration_trial.csv", index=False)
    print(f"cases: {len(cases):,} ({cases['period'].value_counts().to_dict()}), events: {len(log):,}")


if __name__ == "__main__":
    main()
