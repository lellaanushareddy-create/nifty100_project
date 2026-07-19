import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

# Read SQL schema file
with open("db/schema.sql", "r") as f:
    sql_script = f.read()

# Execute SQL script
cursor.executescript(sql_script)

# Save changes
conn.commit()

# Close connection
conn.close()

print("Database tables created successfully.")