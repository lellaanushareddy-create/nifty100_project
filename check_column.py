import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("PRAGMA table_info(prosandcons);", conn)

print(df[["name"]])

conn.close()