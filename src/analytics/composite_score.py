import pandas as pd


def calculate_composite_score(df):
    score = pd.Series(0, index=df.index)

    if "return_on_equity_pct" in df.columns:
        score += df["return_on_equity_pct"].fillna(0) * 0.15

    if "roce_pct" in df.columns:
        score += df["roce_pct"].fillna(0) * 0.10

    if "net_profit_margin_pct" in df.columns:
        score += df["net_profit_margin_pct"].fillna(0) * 0.10

    if "fcf_cagr_5y_pct" in df.columns:
        score += df["fcf_cagr_5y_pct"].fillna(0) * 0.15

    if "cfo_pat_ratio_pct" in df.columns:
        score += df["cfo_pat_ratio_pct"].fillna(0) * 0.10

    if "revenue_cagr_5y_pct" in df.columns:
        score += df["revenue_cagr_5y_pct"].fillna(0) * 0.10

    if "pat_cagr_5y_pct" in df.columns:
        score += df["pat_cagr_5y_pct"].fillna(0) * 0.10

    if "interest_coverage_ratio" in df.columns:
        score += df["interest_coverage_ratio"].fillna(0) * 0.05

    if "debt_to_equity_ratio" in df.columns:
        score += (1 / (1 + df["debt_to_equity_ratio"].fillna(0))) * 10

    df["composite_score"] = score.round(2)

    return df.sort_values(by="composite_score", ascending=False)


if __name__ == "__main__":
    print("Day 17 Composite Score Ready")
