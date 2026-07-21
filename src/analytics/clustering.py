from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[2]

output_dir = BASE / "output"
reports_dir = BASE / "reports"

reports_dir.mkdir(parents=True, exist_ok=True)

company_file = output_dir / "company_summary.csv"

df = pd.read_csv(company_file)

print("Company data loaded successfully!")
company_file = output_dir / "company_summary.csv"
valuation_file = output_dir / "valuation_summary.xlsx"
ratios_file = BASE / "data" / "raw" / "financial_ratios.xlsx"
growth_file = output_dir / "parsed_analysis.xlsx"
company_df = pd.read_csv(company_file)
valuation_df = pd.read_excel(valuation_file)
ratios_df = pd.read_excel(ratios_file)
growth_df = pd.read_excel(growth_file)
# Keep only latest year's ratios
ratios_df = (
    ratios_df.sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

# Select required columns
ratios_df = ratios_df[
    [
        "company_id",
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
    ]
]

growth_df = growth_df[
    [
        "company_id",
        "compounded_sales_growth",
    ]
]

# Merge all datasets
cluster_df = valuation_df.merge(
    ratios_df,
    on="company_id",
    how="left"
)

cluster_df = cluster_df.merge(
    growth_df,
    on="company_id",
    how="left"
)

print(cluster_df.shape)
print(cluster_df.head())

# Features for clustering
features = [
    "pe_ratio",
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "compounded_sales_growth",
]

cluster_data = cluster_df[features].copy()

# Convert growth column to numeric
cluster_data["compounded_sales_growth"] = (
    cluster_data["compounded_sales_growth"]
    .astype(str)
    .str.extract(r"(\d+\.?\d*)")[0]
)

cluster_data["compounded_sales_growth"] = pd.to_numeric(
    cluster_data["compounded_sales_growth"],
    errors="coerce"
)

# Fill missing values
cluster_data = cluster_data.fillna(cluster_data.median(numeric_only=True))

# Standardize features
scaler = StandardScaler()
scaled_data = scaler.fit_transform(cluster_data)

# Apply KMeans clustering
kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

cluster_df["cluster"] = kmeans.fit_predict(scaled_data)

print(cluster_df[["company_id", "cluster"]].head())

cluster_names = {
    0: "Stable",
    1: "Value",
    2: "Growth",
    3: "High Risk"
}

cluster_df["cluster_name"] = cluster_df["cluster"].map(cluster_names)

# Save clustering results
cluster_output = output_dir / "cluster_results.xlsx"
cluster_df.to_excel(cluster_output, index=False)

print(cluster_df[["company_id", "cluster", "cluster_name"]].head())
print(f"Cluster results saved to: {cluster_output}")

summary = (
    cluster_data.assign(cluster=cluster_df["cluster"])
    .groupby("cluster")
    .mean(numeric_only=True)
)

print(summary)