from pathlib import Path
import pandas as pd
import numpy as np

# Project folders
ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output"

# Read clustering result
cluster_df = pd.read_excel(OUTPUT / "cluster_results.xlsx")

# Features to check
features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "compounded_sales_growth"
]

# Convert columns to numeric
for feature in features:
    if feature in cluster_df.columns:
        cluster_df[feature] = pd.to_numeric(
            cluster_df[feature],
            errors="coerce"
        )

# Fill missing broad_sector
cluster_df["broad_sector"] = cluster_df["broad_sector"].fillna("Unknown")

# Outlier detection using Z-score
cluster_df["outlier"] = False

for feature in features:

    if feature not in cluster_df.columns:
        continue

    mean = cluster_df.groupby("broad_sector")[feature].transform(lambda x: x.mean())
    std = cluster_df.groupby("broad_sector")[feature].transform(lambda x: x.std())

    zscore = (cluster_df[feature] - mean) / std

    cluster_df[f"{feature}_zscore"] = zscore

    cluster_df.loc[zscore.abs() > 3, "outlier"] = True

# Save report
report = OUTPUT / "outlier_report.csv"
cluster_df.to_csv(report, index=False)

print(cluster_df[["company_id", "outlier"]].head())

print(f"\nOutlier report saved to: {report}")
print("Outlier detection completed successfully.")