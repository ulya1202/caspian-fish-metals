"""
Table 2: Kruskal-Wallis H tests by tissue category, species, and family.

Kruskal-Wallis chosen over parametric ANOVA because:
  - Shapiro-Wilk rejects normality for all priority metals
  - Group sizes are small and unequal
  - Levene test rejects homoscedasticity
"""
import os
import pandas as pd
from scipy.stats import kruskal, shapiro
from config import OUTPUT_DIR, TARGET_METALS


def normality_check(df):
    """Shapiro-Wilk test — justification for nonparametric approach."""
    print("\n── Normality check (Shapiro-Wilk) ──")
    for metal in TARGET_METALS:
        vals = df.loc[df["metal"] == metal, "conc"].values
        if len(vals) < 8:
            continue
        w, p = shapiro(vals)
        tag = "non-normal" if p < .05 else "normal"
        print(f"  {metal}: W = {w:.4f}, p = {p:.4f} -> {tag}")


def kruskal_tests(df, metals=None):
    """
    Run Kruskal-Wallis H for each metal across three grouping factors.
    Reports epsilon-squared as the effect-size measure.
    """
    if metals is None:
        metals = TARGET_METALS

    results = []
    print("\n── Table 2: Kruskal-Wallis H tests ──")

    for metal in metals:
        sub = df[df["metal"] == metal]
        N = len(sub)
        if N < 6:
            continue

        for factor, col in [("Tissue category", "tissue_cat"),
                            ("Species", "species"),
                            ("Family", "family")]:

            groups = [g["conc"].values
                      for _, g in sub.groupby(col) if len(g) >= 2]
            if len(groups) < 2:
                continue

            H, p = kruskal(*groups)
            k = len(groups)
            eps2 = H / (N - 1)
            label = ("large" if eps2 > 0.14
                     else "medium" if eps2 > 0.06 else "small")

            results.append({
                "Metal": metal, "Factor": factor,
                "H": round(H, 3), "df": k - 1,
                "p": round(p, 4), "eps2": round(eps2, 3),
                "effect": label, "N": N,
            })

            sig = "*" if p < .05 else ""
            print(f"  {metal:3s} x {factor:18s}: "
                  f"H({k-1}) = {H:7.3f}, p = {p:.4f}{sig}, "
                  f"eps2 = {eps2:.3f} ({label})")

    out = pd.DataFrame(results)
    out.to_csv(os.path.join(OUTPUT_DIR, "table2_kruskal.csv"), index=False)
    return out
