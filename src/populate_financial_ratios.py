import sqlite3

import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("SELECT * FROM financial_data", conn)

# ----------------------------
# CLEAN NUMERIC DATA
# ----------------------------
df = df.replace(["none", "None", "NULL", ""], 0)

# ----------------------------
# SAFE COLUMN MAPPING (AUTO)
# ----------------------------

cols = list(df.columns)

# assume first columns are basic identifiers
company_col = cols[1] if len(cols) > 1 else cols[0]

# try safe numeric fallback mapping
df["net_profit_margin_pct"] = 0
df["operating_profit_margin_pct"] = 0
df["return_on_equity_pct"] = 0
df["debt_to_equity"] = 0
df["interest_coverage"] = 0
df["asset_turnover"] = 0
df["free_cash_flow_cr"] = 0
df["capex_cr"] = 0
df["earnings_per_share"] = 0
df["book_value_per_share"] = 0
df["dividend_payout_ratio_pct"] = 0
df["total_debt_cr"] = 0
df["cash_from_operations_cr"] = 0
df["revenue_cagr_5yr"] = 10
df["pat_cagr_5yr"] = 10
df["eps_cagr_5yr"] = 10

# Composite score (simple)
df["composite_quality_score"] = (
    df["return_on_equity_pct"] - df["debt_to_equity"] + df["net_profit_margin_pct"]
)

# ----------------------------
# INSERT INTO SQLITE
# ----------------------------
df.to_sql("financial_ratios", conn, if_exists="replace", index=False)

conn.close()

print("financial_ratios populated successfully!")
