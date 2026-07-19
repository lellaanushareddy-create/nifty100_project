import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

try:
    # Display available tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables in database:")
    for table in tables:
        print(table[0])

    print("\nFirst 5 rows from financial_ratios:")

    # Fetch first 5 rows
    cursor.execute("SELECT * FROM financial_ratios LIMIT 5;")
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No data found in financial_ratios.")

except sqlite3.Error as e:
    print("Database Error:", e)

finally:
    conn.close()