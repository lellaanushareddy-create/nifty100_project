import sqlite3
import pandas as pd
import os

# Create db folder if it doesn't exist
os.makedirs("db", exist_ok=True)

# Create/connect to database
conn = sqlite3.connect("db/nifty100.db")

# Read Excel files and save as SQLite tables
files = {
    "companies": "data/raw/companies.xlsx",
    "financial_ratios": "data/raw/financial_ratios.xlsx",
    "balancesheet": "data/raw/balancesheet.xlsx",
    "cashflow": "data/raw/cashflow.xlsx",
    "profitandloss": "data/raw/profitandloss.xlsx",
    "market_cap": "data/raw/market_cap.xlsx",
    "peer_groups": "data/raw/peer_groups.xlsx",
    "sectors": "data/raw/sectors.xlsx",
    "stock_prices": "data/raw/stock_prices.xlsx"
}

for table_name, file_path in files.items():
    print(f"Loading {file_path}...")
    df = pd.read_excel(file_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)

conn.close()

print("✅ Database created successfully: db/nifty100.db")