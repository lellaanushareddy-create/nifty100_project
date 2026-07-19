import pandas as pd
import os

def export_to_excel():
    os.makedirs("output", exist_ok=True)

    df = pd.DataFrame({
        "Company": ["Sample Company"],
        "Composite Score": [85.5]
    })

    output_file = "output/screener_output.xlsx"

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Composite Score", index=False)

    print(f"Results exported to {output_file}")

if __name__ == "__main__":
    export_to_excel()