import pandas as pd
from pathlib import Path

# ---------------------------------------
# Project Paths
# ---------------------------------------

ROOT = Path(__file__).resolve().parents[2]

DATA = ROOT / "data" / "raw"
OUTPUT = ROOT / "output"

OUTPUT.mkdir(exist_ok=True)

# ---------------------------------------
# Load Excel Files
# ---------------------------------------

financial = pd.read_excel(DATA / "financial_ratios.xlsx")
profit = pd.read_excel(DATA / "profitandloss.xlsx",header=1)
balance = pd.read_excel(DATA / "balancesheet.xlsx",header=1)
cashflow = pd.read_excel(DATA / "cashflow.xlsx",header=1)
companies = pd.read_excel(DATA / "companies.xlsx",header=1)

print("Financial Columns:", financial.columns.tolist())
print("Profit Columns:", profit.columns.tolist())
print("Balance Columns:", balance.columns.tolist())
print("Cashflow Columns:", cashflow.columns.tolist())

# ---------------------------------------
# Store Generated Pros & Cons
# ---------------------------------------

records = []

def add_record(company_id, rule_type, rule_id, text, confidence):
    if confidence >= 60:
        records.append({
            "company_id": company_id,
            "type": rule_type,
            "rule_id": rule_id,
            "text": text,
            "confidence_pct": confidence
        })

# Use March 2024 data (all companies)
latest_year = "Mar 2024"

latest = financial[financial["year"] == latest_year].copy()

print(f"Latest Year: {latest_year}")
print(f"Companies Found: {len(latest)}")

print("\nLatest Company IDs:")
print(latest["company_id"])

print("Companies Columns:")
print(companies.columns.tolist())

print(companies.head())
print("\nAll Years:")
print(financial["year"].value_counts())

# ---------------------------------------
# Generate Pros
# ---------------------------------------

for _, row in latest.iterrows():

    company = row["company_id"]

    if row["net_profit_margin_pct"] >= 15:
        add_record(company, "PRO", "P001",
                   "Strong net profit margin", 95)

    if row["return_on_equity_pct"] >= 15:
        add_record(company, "PRO", "P002",
                   "High Return on Equity", 95)

    if row["free_cash_flow_cr"] > 0:
        add_record(company, "PRO", "P003",
                   "Positive Free Cash Flow", 90)

    if row["asset_turnover"] >= 1:
        add_record(company, "PRO", "P004",
                   "Efficient asset utilization", 85)

    if row["operating_profit_margin_pct"] >= 15:
        add_record(company, "PRO", "P005",
                   "Healthy operating margin", 90)

    if row["earnings_per_share"] > 0:
        add_record(company, "PRO", "P006",
                   "Positive Earnings Per Share", 80)

# ---------------------------------------
# Generate Cons
# ---------------------------------------

for _, row in latest.iterrows():

    company = row["company_id"]

    if row["net_profit_margin_pct"] < 5:
        add_record(company, "CON", "C001",
                   "Low profit margin", 90)

    if row["return_on_equity_pct"] < 10:
        add_record(company, "CON", "C002",
                   "Weak Return on Equity", 90)

    if row["free_cash_flow_cr"] < 0:
        add_record(company, "CON", "C003",
                   "Negative Free Cash Flow", 95)

    if row["asset_turnover"] < 0.5:
        add_record(company, "CON", "C004",
                   "Poor asset utilization", 85)

    if row["operating_profit_margin_pct"] < 10:
        add_record(company, "CON", "C005",
                   "Low operating margin", 90)

    if row["earnings_per_share"] < 0:
        add_record(company, "CON", "C006",
                   "Negative Earnings Per Share", 90)

# ---------------------------------------
# Save Output
# ---------------------------------------

pros_cons = pd.DataFrame(records)

pros_cons.to_csv(
    OUTPUT / "pros_cons_report.csv",
    index=False
)

print()
print("Generated Records:", len(pros_cons))
print(pros_cons.head())

# ---------------------------------------
# Save Generated Pros & Cons
# ---------------------------------------

result = pd.DataFrame(records)

result.to_csv(OUTPUT / "pros_cons.csv", index=False)
result.to_excel(OUTPUT / "pros_cons.xlsx", index=False)

print("\nFiles Saved Successfully!")
print("CSV :", OUTPUT / "pros_cons.csv")
print("Excel :", OUTPUT / "pros_cons.xlsx")
print("Total Records:", len(result))


# -------------------------------
# CONS RULES
# -------------------------------

# Low Net Profit Margin
if row["net_profit_margin_pct"] < 8:
    add_record(company, "CON", "C001",
               "Low net profit margin", 90)

# Low ROE
if row["return_on_equity_pct"] < 12:
    add_record(company, "CON", "C002",
               "Low Return on Equity", 90)

# Negative Free Cash Flow
if row["free_cash_flow_cr"] < 0:
    add_record(company, "CON", "C003",
               "Negative Free Cash Flow", 95)

# High Debt
if row["debt_to_equity"] > 1:
    add_record(company, "CON", "C004",
               "High Debt to Equity", 90)

# Weak Operating Margin
if row["operating_profit_margin_pct"] < 10:
    add_record(company, "CON", "C005",
               "Weak operating margin", 85)
    

# ---------------------------------------
# Generate Company Summary
# ---------------------------------------

summary = []

for company_id in result["company_id"].unique():

    company_data = result[result["company_id"] == company_id]

    pros = company_data[company_data["type"] == "PRO"]["text"].tolist()
    cons = company_data[company_data["type"] == "CON"]["text"].tolist()

    if len(pros) >= 8 and len(cons) <= 2:
        recommendation = "BUY"
    elif len(pros) >= len(cons):
        recommendation = "HOLD"
    else:
        recommendation = "SELL"

    summary.append({
        "company_id": company_id,
        "pros_count": len(pros),
        "cons_count": len(cons),
        "pros": "; ".join(pros),
        "cons": "; ".join(cons),
        "recommendation": recommendation
    })

summary_df = pd.DataFrame(summary)

summary_df.to_csv(OUTPUT / "company_summary.csv", index=False)
summary_df.to_excel(OUTPUT / "company_summary.xlsx", index=False)

print("\nCompany Summary Generated!")
print(summary_df.head())

