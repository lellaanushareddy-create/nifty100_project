from pathlib import Path
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

BASE = Path(__file__).resolve().parents[2]

input_file = BASE / "output" / "company_summary.csv"
output_dir = BASE / "reports" / "sector"
output_dir.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()

if not input_file.exists():
    print("company_summary.csv not found.")
    exit()

df = pd.read_csv(input_file)

# Find sector column
if "sector" in df.columns:
    sector_col = "sector"
elif "broad_sector" in df.columns:
    sector_col = "broad_sector"
else:
    print("Sector report skipped.")
    print("Reason: company_summary.csv has no sector column.")
    exit()

# Find company column
if "company_name" in df.columns:
    company_col = "company_name"
elif "company_id" in df.columns:
    company_col = "company_id"
else:
    company_col = df.columns[0]

for sector in sorted(df[sector_col].dropna().unique()):

    sector_df = df[df[sector_col] == sector]

    pdf_file = output_dir / f"{sector}_report.pdf"

    doc = SimpleDocTemplate(str(pdf_file))
    elements = []

    elements.append(
        Paragraph(f"<b>Sector Report : {sector}</b>", styles["Title"])
    )

    elements.append(
        Paragraph(f"Total Companies : {len(sector_df)}", styles["Heading2"])
    )

    data = [["Company"]]

    for company in sector_df[company_col]:
        data.append([str(company)])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))

    elements.append(table)

    doc.build(elements)

print("Sector reports generated successfully.")
print("Location:", output_dir)