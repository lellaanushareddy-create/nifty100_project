import pandas as pd
import sqlite3

print("Reading Excel...")

df = pd.read_excel("data/raw/financial_ratios.xlsx")

print("Excel loaded:", df.shape)

df = df.replace(["none", "None", "NULL", "null", ""], 0)
df = df.fillna(0)

conn = sqlite3.connect("db/nifty100.db")
df.to_sql("financial_data", conn, if_exists="replace", index=False)

conn.close()

print("Clean data stored successfully!")