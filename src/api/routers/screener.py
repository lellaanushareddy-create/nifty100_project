from fastapi import APIRouter, Query
import sqlite3

router = APIRouter()

DB_PATH = "db/nifty100.db"


@router.get("/screener")
def get_screener(
    min_roe: float | None = Query(None),
    max_de: float | None = Query(None),
    min_fcf: float | None = Query(None),
    sector: str | None = Query(None),
    min_rev_cagr_5yr: float | None = Query(None),
    min_pat_cagr_5yr: float | None = Query(None),
    max_pe: float | None = Query(None),
):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
        SELECT *
        FROM financial_ratios
        WHERE 1=1
    """

    params = []

    if min_roe is not None:
        query += " AND return_on_equity_pct >= ?"
        params.append(min_roe)

    if max_de is not None:
        query += " AND debt_to_equity <= ?"
        params.append(max_de)

    if min_fcf is not None:
        query += " AND free_cash_flow_cr >= ?"
        params.append(min_fcf)

    if min_rev_cagr_5yr is not None:
        query += " AND revenue_cagr_5yr >= ?"
        params.append(min_rev_cagr_5yr)

    if min_pat_cagr_5yr is not None:
        query += " AND pat_cagr_5yr >= ?"
        params.append(min_pat_cagr_5yr)

    if max_pe is not None:
        query += " AND price_to_earnings <= ?"
        params.append(max_pe)

    cursor.execute(query, params)

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return data