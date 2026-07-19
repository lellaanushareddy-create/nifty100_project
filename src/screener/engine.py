import pandas as pd
import yaml


def load_config(config_file="screener_config.yaml"):
    with open(config_file, "r") as file:
        return yaml.safe_load(file)


def apply_filters(df):
    config = load_config()
    filters = config["filters"]

    if "return_on_equity_pct" in df.columns:
        df = df[df["return_on_equity_pct"] >= filters["roe_min"]]

    if "debt_to_equity" in df.columns:
        df = df[df["debt_to_equity"] <= filters["debt_to_equity_max"]]

    if "net_profit_margin_pct" in df.columns:
        df = df[df["net_profit_margin_pct"] >= filters["net_profit_min"]]

    df["composite_quality_score"] = (
        df.select_dtypes(include="number")
        .fillna(0)
        .sum(axis=1)
    )

    return df.sort_values(
        by="composite_quality_score",
        ascending=False
    )


PRESETS = {
    "quality_compounder": {
        "roe_min": 15,
        "debt_to_equity_max": 1.0,
        "fcf_positive": True,
        "revenue_cagr_5y_min": 10,
    },
    "value_pick": {
        "pe_max": 20,
        "pb_max": 3,
        "debt_to_equity_max": 2,
        "dividend_yield_min": 1,
    },
    "growth_accelerator": {
        "pat_cagr_5y_min": 20,
        "revenue_cagr_5y_min": 15,
        "debt_to_equity_max": 2,
    },
    "dividend_champion": {
        "dividend_yield_min": 2,
        "dividend_payout_max": 80,
        "fcf_positive": True,
    },
    "debt_free_blue_chip": {
        "debt_to_equity_max": 0,
        "roe_min": 12,
        "revenue_min": 5000,
    },
    "turnaround_watch": {
        "revenue_cagr_3y_min": 10,
        "fcf_positive": True,
    },
}


if __name__ == "__main__":
    print("Day 16 Presets Added Successfully")