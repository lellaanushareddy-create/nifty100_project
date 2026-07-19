import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM financial_ratios LIMIT 3;")
rows = cursor.fetchall()

for r in rows:
    print(r)

conn.close()