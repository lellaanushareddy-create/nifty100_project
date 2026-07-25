import os

import pandas as pd

# Load Excel files
companies = pd.read_excel("data/raw/companies.xlsx")
balancesheet = pd.read_excel("data/raw/balancesheet.xlsx")
cashflow = pd.read_excel("data/raw/cashflow.xlsx")
profitandloss = pd.read_excel("data/raw/profitandloss.xlsx")
stock_prices = pd.read_excel("data/raw/stock_prices.xlsx")

financial_ratios = pd.read_excel("data/raw/financial_ratios.xlsx")
market_cap = pd.read_excel("data/raw/market_cap.xlsx")
peer_groups = pd.read_excel("data/raw/peer_groups.xlsx")
sectors = pd.read_excel("data/raw/sectors.xlsx")

# Store validation issues
validation_errors = []


# Validation function
def validate(df, table_name):

    # Null check
    for col in df.columns:

        null_count = df[col].isnull().sum()

        if null_count > 0:

            validation_errors.append([table_name, "Null Check", col, null_count])

    # Duplicate check
    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:

        validation_errors.append(
            [table_name, "Duplicate Check", "all_columns", duplicate_count]
        )


# Run validation
validate(companies, "companies")
validate(balancesheet, "balancesheet")
validate(cashflow, "cashflow")
validate(profitandloss, "profitandloss")
validate(stock_prices, "stock_prices")

validate(financial_ratios, "financial_ratios")
validate(market_cap, "market_cap")
validate(peer_groups, "peer_groups")
validate(sectors, "sectors")


# Unique company_id check
if "company_id" in companies.columns:

    if companies["company_id"].nunique() != len(companies):

        validation_errors.append(
            ["companies", "Unique Check", "company_id", "duplicate ids"]
        )


# Create output folder
os.makedirs("output", exist_ok=True)


# Create report
report = pd.DataFrame(validation_errors, columns=["Table", "Rule", "Column", "Issue"])

# Save CSV
report.to_csv("output/validation_failures.csv", index=False)

print("Validation completed")
print(report)
