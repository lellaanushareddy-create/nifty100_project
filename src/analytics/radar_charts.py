import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Database Connection
# -------------------------------
DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

# -------------------------------
# Output Folder
# -------------------------------
OUTPUT_DIR = "reports/radar_charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------
# Load Tables
# -------------------------------
financial_data = pd.read_sql(
    "SELECT * FROM financial_data",
    conn
)

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

peer_percentiles = pd.read_sql(
    "SELECT * FROM peer_percentiles",
    conn
)

print("Financial Data :", financial_data.shape)
print("Financial Ratios :", financial_ratios.shape)
print("Peer Percentiles :", peer_percentiles.shape)

# -------------------------------
# Radar Metrics
# -------------------------------
metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "composite_quality_score"
]

# Keep only metrics that actually exist
metrics = [m for m in metrics if m in financial_ratios.columns]

print("Radar Metrics:", metrics)

# -------------------------------
# Merge company data
# -------------------------------
merged_df = financial_ratios.merge(
    financial_data[["company_id", "year"]],
    on=["company_id", "year"],
    how="left"
)

print("Merged Shape:", merged_df.shape)
# -----------------------------------------
# Radar Chart Function
# -----------------------------------------
def create_radar_chart(company_name, values):
    labels = metrics

    values = np.array(values, dtype=float)
    values = np.nan_to_num(values)

    # Close the polygon
    values = np.concatenate((values, [values[0]]))

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)

    ax.set_title(company_name, fontsize=14)

    filename = os.path.join(
        OUTPUT_DIR,
        f"{company_name.replace(' ', '_')}_radar.png"
    )

    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
# -----------------------------------------
# Generate Radar Charts
# -----------------------------------------

latest_data = (
    merged_df.sort_values("year")
    .groupby("company_id")
    .tail(1)
)

print(f"Generating radar charts for {len(latest_data)} companies...")

for _, row in latest_data.iterrows():

    company_name = row["company_id"]

    values = []

    for metric in metrics:
        if metric in latest_data.columns:
            values.append(row[metric])
        else:
            values.append(0)

    create_radar_chart(company_name, values)

print("Radar charts generated successfully!")
print(f"Saved in: {OUTPUT_DIR}")