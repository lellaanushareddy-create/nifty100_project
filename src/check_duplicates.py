import sqlite3

conn = sqlite3.connect("nifty100.db")
cursor = conn.cursor()

tables = [
    "companies",
    "balancesheet",
    "cashflow",
    "profitandloss"
]

for table in tables:
    cursor.execute(f"""
    SELECT COUNT(*) -
    COUNT(DISTINCT rowid)
    FROM {table}
    """)

    duplicates = cursor.fetchone()[0]
    print(f"{table}: {duplicates}")

conn.close()