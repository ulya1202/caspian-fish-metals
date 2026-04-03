"""
Table 4: Target Hazard Quotient (THQ) and Hazard Index (HI).

Methodology follows US EPA (2000) risk assessment guidance.
Only edible white muscle tissue is used — caudal/red muscle,
organs, roe, and fin spines excluded from intake calculations.
"""
import os
import pandas as pd
from config import (OUTPUT_DIR, EU_LIMITS, RFD, SCENARIOS,
                    EXPOSURE_FREQ, EXPOSURE_DUR, BODY_WEIGHT, AVG_TIME)


def eu_comparison(df):
    """Compare edible muscle concentrations to EU Reg. 2023/915."""
    edible = df[df["edible"] == "yes"]
    print("\n── EU limit comparison (edible muscle) ──")

    for metal, limit in EU_LIMITS.items():
        sub = edible[edible["metal"] == metal]
        if sub.empty:
            continue
        mean_c = sub["conc"].mean()
        n_exc = (sub["conc"] > limit).sum()
        pct = n_exc / len(sub) * 100
        flag = "EXCEEDS" if mean_c > limit else "below"
        print(f"  {metal}: mean = {mean_c:.4f}, "
              f"EU limit = {limit}, {flag} "
              f"({n_exc}/{len(sub)} = {pct:.0f}% exceed)")


def compute_thq(df):
    """
    Calculate THQ per metal and HI under each consumption scenario.

    THQ = (EF * ED * FIR * C) / (RfD * BW * AT)

    where FIR is converted from g/day to kg/day.
    """
    edible = df[df["edible"] == "yes"]
    print("\n── Table 4: Health risk assessment ──")
    all_rows = []

    for label, fir_gday in SCENARIOS.items():
        print(f"\n  Scenario: {label}")
        fir_kgday = fir_gday / 1000
        hi = 0

        for metal, rfd in RFD.items():
            sub = edible[edible["metal"] == metal]
            if sub.empty:
                continue

            C = sub["conc"].mean()
            thq = ((EXPOSURE_FREQ * EXPOSURE_DUR * fir_kgday * C)
                   / (rfd * BODY_WEIGHT * AVG_TIME))
            hi += thq

            warn = " !" if thq > 1 else ""
            print(f"    {metal:4s}: C = {C:.4f}, THQ = {thq:.6f}{warn}")
            all_rows.append({
                "scenario": label, "metal": metal,
                "mean_conc": round(C, 4), "THQ": round(thq, 6),
            })

        all_rows.append({
            "scenario": label, "metal": "HI",
            "mean_conc": None, "THQ": round(hi, 4),
        })
        status = "< 1 (safe)" if hi < 1 else "> 1 (risk)"
        print(f"    HI = {hi:.4f}  {status}")

    out = pd.DataFrame(all_rows)
    out.to_csv(os.path.join(OUTPUT_DIR, "table4_hri.csv"), index=False)
    return out
