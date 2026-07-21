from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2]

output_dir = BASE / "reports" / "tearsheets"
sector_dir = BASE / "reports" / "sector"

output_dir.mkdir(parents=True, exist_ok=True)
sector_dir.mkdir(parents=True, exist_ok=True)

companies = pd.read_csv(BASE / "output" / "company_summary.csv")

skipped = []

for _, row in companies.iterrows():
    company = str(row["company_name"]).replace("/", "_")

    pdf = output_dir / f"{company}_tearsheet.pdf"

    with open(pdf, "w") as f:
        f.write(f"Tearsheet for {company}")

print("Created", len(companies), "tearsheets")

pd.DataFrame(skipped).to_csv(
    BASE / "output" / "skipped_tearsheets.csv",
    index=False
)

print("Skipped file created")