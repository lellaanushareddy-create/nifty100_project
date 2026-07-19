import pandas as pd
import os

# Normalize Year
def normalize_year(year):
    return str(year).strip()

# Normalize Ticker
def normalize_ticker(ticker):
    return str(ticker).upper().strip()

# Data folder path
data_folder = "data/raw"

# Read all Excel files
files = [f for f in os.listdir(data_folder) if f.endswith(".xlsx")]

if not files:
    print("No Excel files found!")

else:

    for file in files:

        file_path = os.path.join(
            data_folder,
            file
        )

        try:

            df = pd.read_excel(
                file_path
            )

            # Normalize year
            if "year" in df.columns:

                df["year"] = (
                    df["year"]
                    .apply(
                        normalize_year
                    )
                )

            # Normalize ticker
            if "ticker" in df.columns:

                df["ticker"] = (
                    df["ticker"]
                    .apply(
                        normalize_ticker
                    )
                )

            print("\n=================")
            print(f"Loaded: {file}")
            print(
                f"Rows: {len(df)}"
            )

            print(
                f"Columns: {len(df.columns)}"
            )

            print(
                df.columns.tolist()
            )

            print(
                df.head()
            )

        except Exception as e:

            print(
                f"Error reading {file}: {e}"
            )

print("\nData ingestion complete.")