from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

df = pd.read_excel(OUTPUT / "cluster_results.xlsx")

features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct"
]

corr = df[features].corr()

plt.figure(figsize=(6, 5))
plt.imshow(corr, interpolation="nearest")
plt.colorbar()

plt.xticks(range(len(features)), features, rotation=45)
plt.yticks(range(len(features)), features)

for i in range(len(features)):
    for j in range(len(features)):
        plt.text(j, i, f"{corr.iloc[i, j]:.2f}",
                 ha="center", va="center")

plt.tight_layout()
plt.savefig(REPORTS / "correlation_heatmap.png")
plt.close()

print("Correlation heatmap saved successfully.")