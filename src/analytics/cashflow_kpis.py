import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB = BASE_DIR / "db" / "nifty100.db"
OUTPUT = BASE_DIR / "output"

conn = sqlite3.connect(DB)

financial = pd.read_sql("SELECT * FROM financial_ratios", conn)
cashflow = pd.read_sql("SELECT * FROM cashflow", conn)
balance = pd.read_sql("SELECT * FROM balancesheet", conn)

financial["year"] = financial["year"].str.replace(" ", "-", regex=False)
financial["year"] = financial["year"].str.replace("2013", "13")
financial["year"] = financial["year"].str.replace("2014", "14")
financial["year"] = financial["year"].str.replace("2015", "15")
financial["year"] = financial["year"].str.replace("2016", "16")
financial["year"] = financial["year"].str.replace("2017", "17")
financial["year"] = financial["year"].str.replace("2018", "18")
financial["year"] = financial["year"].str.replace("2019", "19")
financial["year"] = financial["year"].str.replace("2020", "20")
financial["year"] = financial["year"].str.replace("2021", "21")
financial["year"] = financial["year"].str.replace("2022", "22")
financial["year"] = financial["year"].str.replace("2023", "23")
financial["year"] = financial["year"].str.replace("2024", "24")
cashflow["year"] = cashflow["year"].str.replace(" ", "-", regex=False)
cashflow["year"] = cashflow["year"].str.replace("2013", "13")
cashflow["year"] = cashflow["year"].str.replace("2014", "14")
cashflow["year"] = cashflow["year"].str.replace("2015", "15")
cashflow["year"] = cashflow["year"].str.replace("2016", "16")
cashflow["year"] = cashflow["year"].str.replace("2017", "17")
cashflow["year"] = cashflow["year"].str.replace("2018", "18")
cashflow["year"] = cashflow["year"].str.replace("2019", "19")
cashflow["year"] = cashflow["year"].str.replace("2020", "20")
cashflow["year"] = cashflow["year"].str.replace("2021", "21")
cashflow["year"] = cashflow["year"].str.replace("2022", "22")
cashflow["year"] = cashflow["year"].str.replace("2023", "23")
cashflow["year"] = cashflow["year"].str.replace("2024", "24")
cashflow["year"] = cashflow["year"].str.replace("2012", "12")
financial["year"] = financial["year"].str.replace("2012", "12")

print(financial.head())
print(cashflow.head())
print(balance.head())

financial = financial.drop_duplicates(subset=["company_id", "year"], keep="first")
cashflow = cashflow.drop_duplicates(subset=["company_id", "year"], keep="first")

# Merge financial ratios and cashflow
df = cashflow.merge(
    financial[
        [
            "company_id",
            "year",
            "cash_from_operations_cr"
        ]
    ],
    on=["company_id", "year"],
    how="left"
)

# CFO Quality Score
df["cfo_quality_score"] = (
    df["operating_activity"] /
    df["cash_from_operations_cr"]
)

# CFO Label
def label(score):
    if pd.isna(score):
        return "Unknown"
    elif score >= 1:
        return "Strong"
    elif score >= 0.7:
        return "Average"
    else:
        return "Weak"

df["cfo_quality_label"] = df["cfo_quality_score"].apply(label)

print("\nCash Flow KPI Report\n")

result = df[[
    "company_id",
    "year",
    "operating_activity",
    "cash_from_operations_cr",
    "cfo_quality_score",
    "cfo_quality_label"
]]

print(result.head(20).to_string(index=False))

OUTPUT.mkdir(exist_ok=True)

result.to_csv(OUTPUT / "cashflow_kpi_report.csv", index=False)

print("\nSaved:")
print(OUTPUT / "cashflow_kpi_report.csv")

conn.close()

