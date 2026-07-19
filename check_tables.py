import os
import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"
EXCEL_FOLDER = "data/raw"

conn = sqlite3.connect(DB_PATH)

# These Excel files have their column names on the SECOND row
header1_files = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
]

for file in os.listdir(EXCEL_FOLDER):

    if not file.endswith(".xlsx"):
        continue

    table_name = os.path.splitext(file)[0]
    file_path = os.path.join(EXCEL_FOLDER, file)

    print(f"\nImporting {file} -> {table_name}")

    # Read Excel
    if table_name in header1_files:
        df = pd.read_excel(file_path, header=1)
    else:
        df = pd.read_excel(file_path, header=0)

    # Remove empty rows and columns
    df.dropna(how="all", inplace=True)
    df.dropna(axis=1, how="all", inplace=True)

    # Clean column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print(df.columns.tolist())

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False,
    )

    print(f"Imported {len(df)} rows")

conn.close()

print("\nDone!")