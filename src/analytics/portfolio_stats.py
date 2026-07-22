from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output"

df = pd.read_excel(OUTPUT / "cluster_results.xlsx")

features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "compounded_sales_growth"
]

# Convert all feature columns to numeric
for col in features:
    df[col] = pd.to_numeric(df[col], errors="coerce")

stats = pd.DataFrame({
    "P10": df[features].quantile(0.10, numeric_only=True),
    "P25": df[features].quantile(0.25, numeric_only=True),
    "P50": df[features].quantile(0.50, numeric_only=True),
    "P75": df[features].quantile(0.75, numeric_only=True),
    "P90": df[features].quantile(0.90, numeric_only=True),
    "Mean": df[features].mean(numeric_only=True),
    "Std": df[features].std(numeric_only=True)
})

report = OUTPUT / "portfolio_stats.csv"
stats.to_csv(report)

print(stats)
print(f"\nPortfolio statistics saved to: {report}")
print("Portfolio statistics completed successfully.")