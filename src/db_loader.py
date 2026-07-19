import pandas as pd
import sqlite3
import os

# -------------------------------
# Database configuration
# -------------------------------
DB_PATH = "db/nifty100.db"
DATA_PATH = "data/raw"

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# Excel files to load
files = {
    "companies": "companies.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "cashflow": "cashflow.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "stock_prices": "stock_prices.xlsx",
    "market_cap": "market_cap.xlsx",
    "financial_ratios": "financial_ratios.xlsx",
    "peer_groups": "peer_groups.xlsx",
    "sectors": "sectors.xlsx",
    "analysis": "analysis.xlsx"
}

audit = []

for table, file in files.items():

    path = os.path.join(DATA_PATH, file)

    if not os.path.exists(path):
        print(f"File not found: {file}")
        continue

    print(f"Loading {file}...")

    # Companies file has a title row before the headers
    if table == "companies":
        df = pd.read_excel(path, header=1)
    else:
        df = pd.read_excel(path)

    # Clean column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Save into SQLite
    df.to_sql(
        table,
        conn,
        if_exists="replace",
        index=False
    )

    audit.append([table, len(df)])

    print(f"Loaded {table}: {len(df)} rows")

# Save audit report
os.makedirs("output", exist_ok=True)

audit_df = pd.DataFrame(
    audit,
    columns=["table_name", "row_count"]
)

audit_df.to_csv(
    "output/load_audit.csv",
    index=False
)

conn.close()

print("\nDatabase loading completed successfully.")