import pandas as pd
import sqlite3

# Connect database
conn = sqlite3.connect("db/nifty100.db")

# Read tables
financial_df = pd.read_sql("SELECT * FROM financial_ratios", conn)
peer_df = pd.read_excel("data/raw/peer_groups.xlsx")

# Merge using company_id
merged_df = financial_df.merge(
    peer_df,
    on="company_id",
    how="left"
)

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "eps_cagr_5yr",
    "interest_coverage",
    "asset_turnover"

]

results = []

for group in merged_df["peer_group_name"].dropna().unique():

    group_df = merged_df[
        merged_df["peer_group_name"] == group
    ].copy()

    for metric in metrics:

        if metric not in group_df.columns:
            print(f"{metric} not found")
            continue

        group_df["percentile_rank"] = group_df[metric].rank(pct=True)

        if metric == "debt_to_equity":
            group_df["percentile_rank"] = 1 - group_df["percentile_rank"]

        for _, row in group_df.iterrows():

            results.append({
                "company_id": row["company_id"],
                "peer_group_name": group,
                "metric": metric,
                "value": row[metric],
                "percentile_rank": row["percentile_rank"],
                "year": row["year"]
            })

result_df = pd.DataFrame(results)

result_df.to_sql(
    "peer_percentiles",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Peer percentile rankings generated successfully!")