from pathlib import Path

import pandas as pd
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

BASE = Path(__file__).resolve().parents[2]

input_file = BASE / "output" / "company_summary.csv"
output_dir = BASE / "reports" / "tearsheets"

output_dir.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()

if not input_file.exists():
    print("company_summary.csv not found.")
    exit()

companies = pd.read_csv(input_file)

if "company_name" not in companies.columns:
    companies["company_name"] = companies.iloc[:, 0]

generated = 0
skipped = []

for _, row in companies.iterrows():
    company = str(row["company_name"]).strip()

    if company == "" or company.lower() == "nan":
        skipped.append(company)
        continue

    pdf_file = output_dir / f"{company}_tearsheet.pdf"

    doc = SimpleDocTemplate(str(pdf_file))
    elements = [
        Paragraph(f"<b>{company}</b>", styles["Title"]),
        Paragraph("Batch Tearsheet Generated Successfully", styles["Heading2"]),
        Paragraph("Generated using ReportLab.", styles["BodyText"]),
    ]

    doc.build(elements)
    generated += 1

pd.DataFrame({"Skipped": skipped}).to_csv(
    BASE / "output" / "skipped_tearsheets.csv", index=False
)

print(f"Generated {generated} tear sheets.")
print(f"Skipped {len(skipped)} companies.")
print(f"Output folder: {output_dir}")
