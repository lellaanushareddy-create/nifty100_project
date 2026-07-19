import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM financial_ratios;")
print(cursor.fetchone())

conn.close()