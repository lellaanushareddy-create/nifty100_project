import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

tables = [
    "companies",
    "balancesheet",
    "cashflow",
    "profitandloss"
]

report = []

for table in tables:
    df = pd.read_sql(
        f"SELECT * FROM {table}",
        conn
    )

    report.append([
        table,
        len(df),
        df.isnull().sum().sum()
    ])

report_df = pd.DataFrame(
    report,
    columns=[
        "table_name",
        "row_count",
        "null_count"
    ]
)

report_df.to_csv(
    "output/validation_report.csv",
    index=False
)

conn.close()

print("Validation report generated")