from fastapi import APIRouter
import sqlite3

router = APIRouter()

DB_PATH = "db/nifty100.db"


@router.get("/companies")
def get_companies():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            id,
            company_name,
            roe_percentage,
            roce_percentage
        FROM companies
        ORDER BY company_name
    """)

    companies = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return companies


@router.get("/companies/{ticker}")
def get_company(ticker: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM companies
        WHERE id = ?
    """, (ticker,))

    company = cursor.fetchone()
    conn.close()

    if company is None:
        return {"error": "Company not found"}

    return dict(company)

@router.get("/companies/{ticker}/pl")
def get_company_pl(
    ticker: str,
    from_year: int | None = None,
    to_year: int | None = None,
):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
    """

    params = [ticker]

    if from_year is not None:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year is not None:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year"

    cursor.execute(query, params)

    data = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return data

@router.get("/companies/{ticker}/bs")
def get_company_bs(
    ticker: str,
    from_year: int | None = None,
    to_year: int | None = None,
):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
        SELECT *
        FROM balancesheet
        WHERE company_id = ?
    """

    params = [ticker]

    if from_year is not None:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year is not None:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year"

    cursor.execute(query, params)

    data = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return data

@router.get("/companies/{ticker}/cashflow")
def get_company_cashflow(
    ticker: str,
    from_year: int | None = None,
    to_year: int | None = None,
):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
        SELECT *
        FROM cashflow
        WHERE company_id = ?
    """

    params = [ticker]

    if from_year is not None:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year is not None:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year"

    cursor.execute(query, params)

    data = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return data

@router.get("/companies/{ticker}/ratios")
def get_company_ratios(
    ticker: str,
    year: int | None = None,
):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
    """

    params = [ticker]

    if year is not None:
        query += " AND year = ?"
        params.append(year)

    query += " ORDER BY year"

    cursor.execute(query, params)

    data = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return data

from fastapi.responses import FileResponse
from pathlib import Path

@router.get("/companies/{ticker}/tearsheet")
def get_company_tearsheet(ticker: str):
    file_path = Path(f"output/tearsheets/{ticker}.pdf")

    if not file_path.exists():
        return {"error": "Tearsheet not found"}

    return FileResponse(
        path=file_path,
        filename=f"{ticker}.pdf",
        media_type="application/pdf"
    )

@router.get("/companies/{ticker}/peers/compare")
def compare_peers(ticker: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        net_profit_margin_pct,
        debt_to_equity,
        asset_turnover,
        earnings_per_share,
        free_cash_flow_cr,
        capex_cr,
        dividend_payout_ratio_pct
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year DESC
    """

    cursor.execute(query, (ticker,))
    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return {"error": "Company not found"}

    return [dict(row) for row in rows]