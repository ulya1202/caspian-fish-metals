"""
Table 1: Descriptive statistics per metal.
"""
import os
import pandas as pd
from config import OUTPUT_DIR


def descriptive_table(df):
    """Compute count, mean, SD, median, min, max for each metal."""
    stats = (df.groupby("metal")["conc"]
             .agg(N="count", Mean="mean", SD="std",
                  Median="median", Min="min", Max="max")
             .round(4))

    path = os.path.join(OUTPUT_DIR, "table1_descriptive.csv")
    stats.to_csv(path)

    print("\n── Table 1: Descriptive statistics ──")
    print(stats.to_string())
    return stats
