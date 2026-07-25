from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE = Path(__file__).resolve().parents[2]

output_file = BASE / "output" / "sample_tearsheet.pdf"

styles = getSampleStyleSheet()

doc = SimpleDocTemplate(str(output_file))

elements = []

# ---------------- Header ----------------

header = Table([["TCS (TCS.NS)"]], colWidths=[520])

header.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), colors.navy),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 18),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ]
    )
)

elements.append(header)
elements.append(Spacer(1, 20))

# ---------------- KPI Tiles ----------------

kpi_table = Table(
    [
        ["Revenue", "Net Profit", "ROE"],
        ["₹25,000 Cr", "₹4,500 Cr", "24%"],
        ["ROCE", "EPS", "Debt/Equity"],
        ["31%", "₹95", "0.18"],
    ],
    colWidths=[170, 170, 170],
)

kpi_table.setStyle(
    TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("BACKGROUND", (0, 0), (-1, -1), colors.beige),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]
    )
)

elements.append(kpi_table)
elements.append(Spacer(1, 20))

# ---------------- Sample Text ----------------

elements.append(
    Paragraph(
        "<b>Day 33 PDF Tearsheet Template</b>",
        styles["Heading2"],
    )
)

elements.append(
    Paragraph(
        "This is a sample PDF tearsheet. Revenue charts, ROE/ROCE charts, "
        "balance sheet, cash flow waterfall, pros & cons, and capital "
        "allocation badge will be added in the next steps.",
        styles["BodyText"],
    )
)

# ---------------- Build PDF ----------------

doc.build(elements)

print("PDF created successfully!")
print(output_file)
