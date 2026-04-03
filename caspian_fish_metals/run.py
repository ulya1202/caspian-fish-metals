#!/usr/bin/env python3
"""
Entry point for the Caspian Sea fish heavy metals analysis.

Run from the project root:
    python run.py
"""
import os
import sys
import numpy as np

# make sure imports resolve from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import OUTPUT_DIR, SEED
from data.compile import compile
from analysis.descriptive import descriptive_table
from analysis.kruskal import normality_check, kruskal_tests
from analysis.health_risk import eu_comparison, compute_thq
from figures.plots import generate_all

np.random.seed(SEED)


def main():
    print("Caspian Sea Fish Heavy Metals")
    print("=" * 45)

    # 1. compile dataset
    df = compile()
    csv_path = os.path.join(OUTPUT_DIR, "dataset.csv")
    df.to_csv(csv_path, index=False)

    print(f"\nDataset : {len(df)} observations")
    print(f"Sources : {df['paper_id'].nunique()}")
    print(f"Species : {df['species'].nunique()}")
    print(f"Metals  : {df['metal'].nunique()}")
    print(f"Verification: {df['verification'].value_counts().to_dict()}")

    # 2. normality check (justifies nonparametric tests)
    normality_check(df)

    # 3. descriptive stats -> Table 1
    descriptive_table(df)

    # 4. Kruskal-Wallis -> Table 2
    kruskal_tests(df)

    # 5. EU comparison
    eu_comparison(df)

    # 6. health risk assessment -> Table 4
    compute_thq(df)

    # 7. figures 1-4
    generate_all(df)

    print(f"\nAll outputs in: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
