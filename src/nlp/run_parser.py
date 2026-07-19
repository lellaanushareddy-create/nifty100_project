import pandas as pd
from src.nlp.analyzer import analyze_text


def main():
    # Path to Excel file
    file_path = "data/raw/analysis.xlsx"

    # Read Excel
    df = pd.read_excel(file_path,header=1)


    # Show available columns
    print("Columns found:")
    print(df.columns.tolist())
    print("-" * 60)

    # Columns to parse
    columns_to_parse = [
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe",
    ]

    # Check that required columns exist
    for col in columns_to_parse:
        if col not in df.columns:
            print(f"Error: '{col}' column not found.")
            return

    # Parse each column
    for col in columns_to_parse:
        df[col + "_parsed"] = (
            df[col]
            .astype(str)
            .apply(analyze_text)
        )

    # Print first 10 rows
    print(df.head(10))

    # Save output
    output_path = "output/parsed_analysis.xlsx"
    df.to_excel(output_path, index=False)

    print("\nParsing completed successfully!")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()