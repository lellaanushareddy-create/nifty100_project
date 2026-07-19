import sqlite3
import pandas as pd

conn = sqlite3.connect(r"C:\Users\lella\OneDrive\Desktop\nifty100_project\db\nifty100.db")

print(pd.read_sql("SELECT * FROM companies LIMIT 5;", conn))