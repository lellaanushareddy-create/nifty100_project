import os
import re
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import pandas as pd

DB_PATH = Path.cwd() / "db" / "nifty100.db"

print("=" * 50)
print("Current Working Directory:", os.getcwd())
print("Database Path:", DB_PATH)
print("Database Exists:", DB_PATH.exists())
print("=" * 50)


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


with get_connection() as conn:
    cursor = conn.execute("PRAGMA table_info(financial_ratios)")
    print(cursor.fetchall())

    cursor = conn.execute("PRAGMA table_info(market_cap)")
    print(cursor.fetchall())

with get_connection() as conn:
    print("\nProfit and Loss Table Columns:")
    print(pd.read_sql_query("PRAGMA table_info(profitandloss)", conn))

if __name__ == "__main__":
    with get_connection() as conn:
        print(pd.read_sql_query("PRAGMA table_info(profitandloss)", conn))


def _table_has_column(table, column):
    with get_connection() as conn:
        cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    return column in cols


def parse_year(raw):
    """Normalize a year value into a 4-digit int.
    Handles plain ints, '2020', 'Mar 2020', 'Dec-13', etc."""
    if raw is None:
        return None
    if isinstance(raw, (int, float)):
        return int(raw)
    s = str(raw).strip()
    m = re.search(r"(\d{4})", s)
    if m:
        return int(m.group(1))
    m = re.search(r"-(\d{2})$", s)
    if m:
        yy = int(m.group(1))
        return 2000 + yy if yy < 70 else 1900 + yy
    return None


def _read_table(table):
    with get_connection() as conn:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    if "year" in df.columns:
        df["year"] = df["year"].apply(parse_year)
    return df


# ---------------------------------------------------------------------
# SHARED HELPERS
# ---------------------------------------------------------------------
def get_available_years():
    """Return available years safely."""

    with get_connection() as conn:
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';", conn
        )

        if "market_cap" not in tables["name"].tolist():
            return [2024, 2023, 2022, 2021, 2020, 2019]

        df = pd.read_sql_query(
            "SELECT DISTINCT year FROM market_cap ORDER BY year DESC", conn
        )

    if df.empty:
        return [2024, 2023, 2022, 2021, 2020, 2019]

    return df["year"].astype(int).tolist()


def _revenue_cagr(pnl_df, company_id, end_year, span=5):
    print("Columns:", pnl_df.columns.tolist())
    print(pnl_df.head())

    # Check if company_id column exists
    if "company_id" not in pnl_df.columns:
        print("ERROR: 'company_id' column not found!")
        return None

    rows = pnl_df[pnl_df["company_id"] == company_id].copy()

    # Convert year to numeric
    rows["year"] = pd.to_numeric(rows["year"], errors="coerce")

    end_row = rows[rows["year"] == end_year]
    start_row = rows[rows["year"] == (end_year - span)]

    if end_row.empty or start_row.empty:
        return None

    end_sales = pd.to_numeric(end_row["sales"], errors="coerce").iloc[0]
    start_sales = pd.to_numeric(start_row["sales"], errors="coerce").iloc[0]

    if pd.isna(end_sales) or pd.isna(start_sales):
        return None

    if start_sales <= 0:
        return None

    return ((end_sales / start_sales) ** (1 / span) - 1) * 100


def _roce_series(company_id):
    """Yearly ROCE% = operating_profit / capital_employed, where
    capital_employed = equity_capital + reserves + borrowings
    (i.e. total_liabilities minus other_liabilities)."""
    pnl = _read_table("profitandloss")
    bs = _read_table("balancesheet")
    pnl_c = pnl[pnl["company_id"] == company_id][["year", "operating_profit"]]
    bs_c = bs[bs["company_id"] == company_id].copy()
    bs_c["capital_employed"] = (
        bs_c["equity_capital"] + bs_c["reserves"] + bs_c["borrowings"]
    )
    merged = pnl_c.merge(bs_c[["year", "capital_employed"]], on="year", how="inner")
    merged = merged[merged["capital_employed"] > 0]
    merged["roce"] = merged["operating_profit"] / merged["capital_employed"] * 100
    return merged[["year", "roce"]].sort_values("year")


# ---------------------------------------------------------------------
# HOME SCREEN QUERIES
# ---------------------------------------------------------------------


def get_home_kpis(year):
    try:
        fr = _read_table("financial_ratios")
        fr_y = fr[fr["year"] == year]

        with get_connection() as conn:
            mc = pd.read_sql_query(
                "SELECT * FROM market_cap WHERE year = ?", conn, params=(year,)
            )

            total_companies = pd.read_sql_query(
                "SELECT COUNT(*) AS n FROM companies", conn
            )["n"].iloc[0]

        return {
            "avg_roe": fr_y["return_on_equity_pct"].mean() if not fr_y.empty else None,
            "median_pe": mc["pe_ratio"].median() if not mc.empty else None,
            "median_de": fr_y["debt_to_equity"].median() if not fr_y.empty else None,
            "total_companies": int(total_companies),
            "median_rev_cagr": None,
            "debt_free_count": 0,
        }

    except Exception as e:
        print("KPI Error:", e)
        return {
            "avg_roe": None,
            "median_pe": None,
            "median_de": None,
            "total_companies": 0,
            "median_rev_cagr": None,
            "debt_free_count": 0,
        }


def get_sector_breakdown():
    with get_connection() as conn:
        df = pd.read_sql_query(
            """
            SELECT
                broad_sector AS sector,
                COUNT(*) AS company_count
            FROM sectors
            GROUP BY broad_sector
            ORDER BY company_count DESC
        """,
            conn,
        )
    return df


def get_top5_quality_companies(year):
    fr = _read_table("financial_ratios")
    fr_y = fr[fr["year"] == year].copy()

    with get_connection() as conn:
        companies = pd.read_sql_query(
            """
            SELECT
                id AS company_id,
                company_name
            FROM companies
        """,
            conn,
        )

        sectors = pd.read_sql_query(
            """
            SELECT
                company_id,
                broad_sector AS sector
            FROM sectors
        """,
            conn,
        )

    # Make sure company_id columns match
    fr_y["company_id"] = fr_y["company_id"].astype(str).str.strip()
    companies["company_id"] = companies["company_id"].astype(str).str.strip()
    sectors["company_id"] = sectors["company_id"].astype(str).str.strip()

    if fr_y.empty:
        return pd.DataFrame(columns=["company_name", "sector", "quality_score"])

    if _table_has_column("financial_ratios", "composite_quality_score"):
        fr_y["quality_score"] = fr_y["composite_quality_score"]
    else:

        def norm(s):
            s = s.fillna(0)
            rng = s.max() - s.min()
            return (s - s.min()) / rng if rng else s * 0

        fr_y["quality_score"] = (
            norm(fr_y["return_on_equity_pct"]) * 0.3
            + norm(fr_y["net_profit_margin_pct"]) * 0.3
            + norm(-fr_y["debt_to_equity"]) * 0.2
            + norm(fr_y["free_cash_flow_cr"]) * 0.2
        ) * 100

    merged = fr_y.merge(companies, on="company_id", how="left").merge(
        sectors, on="company_id", how="left"
    )

    top5 = merged.sort_values("quality_score", ascending=False).head(5)

    return top5[["company_name", "sector", "quality_score"]]


# ---------------------------------------------------------------------
# COMPANY PROFILE SCREEN QUERIES
# ---------------------------------------------------------------------


def search_companies(query):
    """List of (ticker, company_name) matching the search text."""
    like = f"%{query}%"
    with get_connection() as conn:
        df = pd.read_sql_query(
            """
            SELECT id AS ticker, company_name AS name
            FROM companies
            WHERE id LIKE ? OR company_name LIKE ?
            ORDER BY company_name
            """,
            conn,
            params=(like, like),
        )
    return list(df.itertuples(index=False, name=None))


def get_company_card(ticker):
    """Dict with company name, sector, sub-sector, NSE ticker, about text
    — or None if the ticker isn't found."""
    with get_connection() as conn:
        df = pd.read_sql_query(
            """
            SELECT c.company_name AS company_name,
                   s.broad_sector AS sector,
                   s.sub_sector AS sub_sector,
                   c.id AS nse_ticker,
                   c.about_company AS about
            FROM companies c
            LEFT JOIN sectors s ON s.company_id = c.id
            WHERE c.id = ?
            """,
            conn,
            params=(ticker,),
        )
    if df.empty:
        return None
    return df.iloc[0].to_dict()


def get_company_latest_kpis(ticker):
    """Dict of the 6 KPI tiles (ROE, ROCE, Net Margin, D/E, Revenue CAGR
    5yr, FCF) using the most recent year available for this company."""
    fr = _read_table("financial_ratios")
    fr_c = fr[fr["company_id"] == ticker]
    if fr_c.empty:
        return None

    latest_year = int(fr_c["year"].max())
    latest = fr_c[fr_c["year"] == latest_year].iloc[0]

    with get_connection() as conn:
        comp = pd.read_sql_query(
            "SELECT roce_percentage FROM companies WHERE id = ?", conn, params=(ticker,)
        )
    roce = comp["roce_percentage"].iloc[0] if not comp.empty else None

    pnl = _read_table("profitandloss")
    rev_cagr = _revenue_cagr(pnl, ticker, latest_year)

    return {
        "roe": latest.get("return_on_equity_pct"),
        "roce": roce,
        "net_margin": latest.get("net_profit_margin_pct"),
        "de": latest.get("debt_to_equity"),
        "rev_cagr_5yr": rev_cagr,
        "fcf": latest.get("free_cash_flow_cr"),
    }


def get_company_financials_10yr(ticker):
    pnl = _read_table("profitandloss")

    if pnl.empty:
        return pd.DataFrame(columns=["year", "revenue", "net_profit"])

    df = (
        pnl[pnl["company_id"] == ticker][["year", "sales", "net_profit"]]
        .rename(columns={"sales": "revenue"})
        .copy()
    )

    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    return df.dropna(subset=["year"]).sort_values("year").tail(10)


def get_company_roe_roce_10yr(ticker):
    fr = _read_table("financial_ratios")

    roe = fr[fr["company_id"] == ticker][["year", "return_on_equity_pct"]].rename(
        columns={"return_on_equity_pct": "roe"}
    )

    roce = _roce_series(ticker)

    df = roe.merge(roce, on="year", how="outer").sort_values("year")

    return df.dropna(subset=["year"]).tail(10)


def get_pros_cons(company_id):
    with get_connection() as conn:
        df = pd.read_sql_query(
            """
            SELECT pros, cons
            FROM prosandcons
            WHERE company_id = ?
            """,
            conn,
            params=(company_id,),
        )

    if df.empty:
        return [], []

    pros = df["pros"].dropna().tolist()
    cons = df["cons"].dropna().tolist()

    return pros, cons


def get_screener_data(year):
    fr = _read_table("financial_ratios")
    fr = fr[fr["year"] == int(year)]

    with get_connection() as conn:
        companies = pd.read_sql_query("SELECT id, company_name FROM companies", conn)

        sectors = pd.read_sql_query(
            "SELECT company_id, broad_sector FROM sectors", conn
        )

        market = pd.read_sql_query(
            "SELECT company_id, year, pe_ratio, pb_ratio FROM market_cap", conn
        )

    market["year"] = market["year"].astype(int)

    df = (
        fr.merge(companies, left_on="company_id", right_on="id", how="left")
        .merge(sectors, on="company_id", how="left")
        .merge(market, on=["company_id", "year"], how="left")
    )

    return df.rename(columns={"broad_sector": "sector"})


def get_peer_groups():
    with get_connection() as conn:
        df = pd.read_sql_query(
            """
        SELECT DISTINCT peer_group
        FROM peer_groups
        ORDER BY peer_group_name
        """,
            conn,
        )

    return df["peer_group_name"].tolist()


def get_peer_groups():
    with get_connection() as conn:
        df = pd.read_sql_query(
            """
            SELECT DISTINCT peer_group_name
            FROM peer_groups
            ORDER BY peer_group_name
        """,
            conn,
        )

    return df["peer_group_name"].tolist()


def get_peer_metrics(group, year):
    fr = _read_table("financial_ratios")
    fr = fr[fr["year"] == int(year)]

    with get_connection() as conn:
        companies = pd.read_sql_query("SELECT id, company_name FROM companies", conn)

        peers = pd.read_sql_query(
            "SELECT peer_group_name, company_id FROM peer_groups", conn
        )

        market = pd.read_sql_query(
            "SELECT company_id, year, pe_ratio, pb_ratio FROM market_cap", conn
        )

    market["year"] = market["year"].astype(int)

    df = (
        peers.merge(companies, left_on="company_id", right_on="id")
        .merge(fr, on="company_id")
        .merge(market, on=["company_id", "year"], how="left")
    )

    df = df[df["peer_group_name"] == group]

    return df[
        [
            "company_name",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "pe_ratio",
            "pb_ratio",
        ]
    ]


# =====================================================
# TREND ANALYSIS
# =====================================================


def get_company_list():
    with get_connection() as conn:
        return pd.read_sql_query(
            """
            SELECT
                id,
                company_name
            FROM companies
            ORDER BY company_name
        """,
            conn,
        )


def get_company_trends(company_id):

    pnl = _read_table("profitandloss")
    fr = _read_table("financial_ratios")

    print("P&L Columns:", pnl.columns.tolist())
    print("FR Columns:", fr.columns.tolist())

    if "company_id" not in pnl.columns:
        raise Exception(
            f"'company_id' not found in profitandloss table.\nColumns: {pnl.columns.tolist()}"
        )

    if "company_id" not in fr.columns:
        raise Exception(
            f"'company_id' not found in financial_ratios table.\nColumns: {fr.columns.tolist()}"
        )

    pnl = pnl[pnl["company_id"] == company_id][["year", "sales", "net_profit", "eps"]]

    fr = fr[fr["company_id"] == company_id][
        [
            "year",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
        ]
    ]

    pnl = pnl.rename(
        columns={"sales": "Revenue", "net_profit": "Net Profit", "eps": "EPS"}
    )

    fr = fr.rename(
        columns={
            "return_on_equity_pct": "ROE",
            "net_profit_margin_pct": "Net Margin",
            "debt_to_equity": "Debt to Equity",
            "free_cash_flow_cr": "Free Cash Flow",
        }
    )

    return pnl.merge(fr, on="year", how="outer").sort_values("year")


def get_sector_list():
    with get_connection() as conn:
        df = pd.read_sql_query(
            """
            SELECT DISTINCT broad_sector
            FROM sectors
            ORDER BY broad_sector
        """,
            conn,
        )

    return df


def get_sector_data(sector):
    with get_connection() as conn:

        query = """
        SELECT
            c.company_name,
            s.broad_sector,
            s.sub_sector,

            p.year,

            p.sales AS Revenue,

            f.return_on_equity_pct AS ROE,

            m.market_cap_crore AS MarketCap

        FROM companies c

        INNER JOIN sectors s
            ON c.id = s.company_id

        LEFT JOIN profitandloss p
            ON c.id = p.company_id

        LEFT JOIN financial_ratios f
        ON c.id = f.company_id
        AND CAST(SUBSTR(p.year, -4) AS INTEGER) = CAST(SUBSTR(f.year, -4) AS INTEGER)

        LEFT JOIN market_cap m
         ON c.id = m.company_id
         AND CAST(SUBSTR(p.year, -4) AS INTEGER) = m.year
        WHERE s.broad_sector = ?
        """

        df = pd.read_sql_query(query, conn, params=(sector,))

    if df.empty:
        return df

    # Extract year
    df["year"] = df["year"].astype(str).str.extract(r"(\d{4})")[0]

    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    # Convert numeric columns
    df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")
    df["ROE"] = pd.to_numeric(df["ROE"], errors="coerce")
    df["MarketCap"] = pd.to_numeric(df["MarketCap"], errors="coerce")

    # Remove rows without year
    df = df.dropna(subset=["year"])

    # Keep latest record of each company
    df = (
        df.sort_values("year")
        .drop_duplicates(subset="company_name", keep="last")
        .reset_index(drop=True)
    )

    return df


def get_capital_data():
    with get_connection() as conn:
        query = """
        SELECT
            c.company_name,
            s.broad_sector,

            CASE
                WHEN a.roe >= 20 THEN 'High ROE'
                WHEN a.roe >= 15 THEN 'Quality Compounder'
                WHEN a.roe >= 10 THEN 'Steady Performer'
                WHEN a.roe >= 5 THEN 'Average'
                ELSE 'Turnaround'
            END AS capital_pattern

        FROM companies c
        LEFT JOIN sectors s
            ON c.id = s.company_id
        LEFT JOIN analysis a
            ON c.id = a.company_id
        """
        return pd.read_sql_query(query, conn)
