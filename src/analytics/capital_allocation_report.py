import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

capital = pd.read_csv(BASE / "output" / "capital_allocation.csv")

latest_year = capital["year"].max()

distribution = (
    capital[capital["year"] == latest_year]
    .groupby("pattern_label")
    .size()
    .reset_index(name="count")
)

distribution.to_csv(
    BASE / "output" / "capital_allocation_distribution.csv",
    index=False
)

pattern_changes = capital.sort_values(["company_id", "year"])

pattern_changes["previous_pattern"] = (
    pattern_changes.groupby("company_id")["pattern_label"].shift(1)
)

pattern_changes = pattern_changes[
    pattern_changes["pattern_label"] != pattern_changes["previous_pattern"]
]

pattern_changes.to_csv(
    BASE / "output" / "pattern_changes.csv",
    index=False
)

print("Saved:")
print(BASE / "output" / "capital_allocation_distribution.csv")
print(BASE / "output" / "pattern_changes.csv")