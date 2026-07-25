from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[2]

cashflow = pd.read_csv(BASE / "output" / "cashflow_kpi_report.csv")

capital = cashflow.copy()

capital["cfo_sign"] = capital["cash_from_operations_cr"].apply(
    lambda x: "+" if x >= 0 else "-"
)

capital["cfi_sign"] = "+"
capital["cff_sign"] = "+"


def classify(row):
    cfo = row["cfo_sign"]
    cfi = row["cfi_sign"]
    cff = row["cff_sign"]

    if cfo == "+" and cfi == "-" and cff == "-":
        return "Reinvestor"
    elif cfo == "+" and cfi == "-" and cff == "+":
        return "Growth"
    elif cfo == "+" and cfi == "+" and cff == "-":
        return "Cash Cow"
    elif cfo == "-" and cfi == "+" and cff == "+":
        return "Distress"
    else:
        return "Other"


capital["pattern_label"] = capital.apply(classify, axis=1)
capital = capital[
    [
        "company_id",
        "year",
        "cfo_sign",
        "cfi_sign",
        "cff_sign",
        "pattern_label",
    ]
]

capital.to_csv(
    BASE / "output" / "capital_allocation.csv",
    index=False,
)

print("Capital Allocation Report Generated")
print("Rows:", len(capital))
print("Saved to:")
print(BASE / "output" / "capital_allocation.csv")
