from pathlib import Path

import pandas as pd

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


# ----------------------------
# Load Data
# ----------------------------
def load_market_cap():
    file_path = INPUT_DIR / "market_cap.xlsx"
    return pd.read_excel(file_path)


def load_sectors():
    file_path = INPUT_DIR / "sectors.xlsx"
    return pd.read_excel(file_path)


# ----------------------------
# Latest Year Data
# ----------------------------
def prepare_latest_data(df):
    latest_year = df["year"].max()
    latest_df = df[df["year"] == latest_year].copy()

    print(f"Latest Year : {latest_year}")
    print(f"Companies   : {len(latest_df)}")

    return latest_df


# ----------------------------
# Sector Median PE
# ----------------------------
def calculate_sector_median(df):

    sector_median = df.groupby("broad_sector")["pe_ratio"].median().reset_index()

    sector_median.rename(columns={"pe_ratio": "sector_median_pe"}, inplace=True)

    df = df.merge(sector_median, on="broad_sector", how="left")

    return df


# ----------------------------
# Valuation Flags
# ----------------------------
def add_flags(df):

    df["valuation_flag"] = "Fair"

    df.loc[df["pe_ratio"] > df["sector_median_pe"] * 1.5, "valuation_flag"] = "Caution"

    df.loc[df["pe_ratio"] < df["sector_median_pe"] * 0.7, "valuation_flag"] = "Discount"

    return df


# ----------------------------
# Save Files
# ----------------------------
def save_outputs(df):

    summary_columns = [
        "company_id",
        "year",
        "broad_sector",
        "market_cap_crore",
        "enterprise_value_crore",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "dividend_yield_pct",
        "sector_median_pe",
        "valuation_flag",
    ]

    summary = df[summary_columns]

    summary.to_excel(OUTPUT_DIR / "valuation_summary.xlsx", index=False)

    flags = summary[summary["valuation_flag"] != "Fair"]

    flags.to_csv(OUTPUT_DIR / "valuation_flags.csv", index=False)

    print("\nFiles Generated Successfully")
    print("valuation_summary.xlsx")
    print("valuation_flags.csv")


# ----------------------------
# Main
# ----------------------------
def run():

    print("Valuation Module Started\n")

    market_df = load_market_cap()

    sector_df = load_sectors()

    latest_df = prepare_latest_data(market_df)

    latest_df = latest_df.merge(
        sector_df[["company_id", "broad_sector"]], on="company_id", how="left"
    )

    latest_df = calculate_sector_median(latest_df)

    latest_df = add_flags(latest_df)

    save_outputs(latest_df)

    print("\nCompleted Successfully")


if __name__ == "__main__":
    run()
