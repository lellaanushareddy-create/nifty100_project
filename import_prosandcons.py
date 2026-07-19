import sqlite3
import pandas as pd

# Read the excel
df = pd.read_excel("data/raw/prosandcons.xlsx")

# Rename columns
df.columns = [
    "id",
    "company_id",
    "pros",
    "cons"
]

# Connect database
conn = sqlite3.connect("db/nifty100.db")

# Replace table
df.to_sql(
    "prosandcons",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Imported successfully!")