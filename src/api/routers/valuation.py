from fastapi import APIRouter
import sqlite3

router = APIRouter()

DB_PATH = "db/nifty100.db"


@router.get("/market-cap/{ticker}")
def get_market_cap(ticker: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM market_cap
    WHERE company_id = ?
    ORDER BY year
    """

    cursor.execute(query, (ticker,))
    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return {"error": "Company not found"}

    return [dict(row) for row in rows]