from pathlib import Path

import pandas as pd

# Project folders
ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output"

# Read clustering result
cluster_df = pd.read_excel(OUTPUT / "cluster_results.xlsx")

features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "compounded_sales_growth",
]

# Mean
cluster_mean = cluster_df.groupby("cluster")[features].mean(numeric_only=True)

# Median
cluster_median = cluster_df.groupby("cluster")[features].median(numeric_only=True)

print("Cluster Mean")
print(cluster_mean)

print("\nCluster Median")
print(cluster_median)

cluster_mean.to_csv(OUTPUT / "cluster_mean.csv")
cluster_median.to_csv(OUTPUT / "cluster_median.csv")

print("Cluster profiling completed.")

cluster_names = {0: "High Quality", 1: "Value", 2: "Growth", 3: "Turnaround"}

cluster_df["cluster_name"] = cluster_df["cluster"].map(cluster_names)

cluster_df.to_excel(OUTPUT / "cluster_results.xlsx", index=False)

print(cluster_df[["company_id", "cluster", "cluster_name"]].head())
print("Cluster names assigned successfully.")
