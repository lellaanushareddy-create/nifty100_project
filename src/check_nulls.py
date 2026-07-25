import sqlite3

import pandas as pd

conn = sqlite3.connect("nifty100.db")

tables = ["companies", "balancesheet", "cashflow", "profitandloss"]

for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}", conn)

    print(f"\n{table}")
    print(df.isnull().sum())

conn.close()
