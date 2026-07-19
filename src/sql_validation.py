import sqlite3

conn = sqlite3.connect("nifty100.db")
cursor = conn.cursor()

tables = [
    "companies",
    "balancesheet",
    "cashflow",
    "profitandloss",
    "stock_prices",
    "market_cap",
    "financial_ratios"
]

print("=== ROW COUNTS ===")

for table in tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table}: {count}")
    except Exception as e:
        print(f"{table}: ERROR")

conn.close()