from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

BASE = Path(__file__).resolve().parents[2]

portfolio_dir = BASE / "reports" / "portfolio"
portfolio_dir.mkdir(parents=True, exist_ok=True)

pdf_file = portfolio_dir / "portfolio_summary.pdf"

styles = getSampleStyleSheet()

doc = SimpleDocTemplate(str(pdf_file))

elements = []

elements.append(Paragraph("<b>NIFTY100 Portfolio Summary</b>", styles["Title"]))
elements.append(Paragraph("Sprint 5 Completed Successfully.", styles["Normal"]))
elements.append(Paragraph("Portfolio Summary Report", styles["Heading2"]))
elements.append(Paragraph("Generated using ReportLab.", styles["Normal"]))

doc.build(elements)

print("Portfolio summary created successfully!")
print(pdf_file)