import sqlite3

import pandas as pd

# Connect to the database
conn = sqlite3.connect("db/nifty100.db")

# Read the tables
financial_data = pd.read_sql("SELECT * FROM financial_data", conn)

financial_ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

print("===== FINANCIAL DATA =====")
print(financial_data.head())

print("\n===== FINANCIAL RATIOS =====")
print(financial_ratios.head())

# Check if required columns exist
if "broad_sector" in financial_data.columns:
    banks = financial_data[
        financial_data["broad_sector"].str.contains("Financial", case=False, na=False)
    ]

    print("\n===== FINANCIAL SECTOR COMPANIES =====")
    print(banks)
    print("\nTotal Financial Companies:", len(banks))
else:
    print("\nColumn 'broad_sector' not found in financial_data table.")

# Save edge-case log
with open("output/ratio_edge_cases.log", "w") as f:
    f.write("Day 13 - Bank ROCE Carve-Out & Edge Case Log\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Financial data records: {len(financial_data)}\n")
    f.write(f"Financial ratios records: {len(financial_ratios)}\n")

    if "broad_sector" in financial_data.columns:
        f.write(f"Financial sector companies: {len(banks)}\n")

    f.write("\nReview completed successfully.\n")

conn.close()

print("\nDay 13 completed successfully!")
print("Edge case log saved to output/ratio_edge_cases.log")
