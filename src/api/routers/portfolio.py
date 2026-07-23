from fastapi import APIRouter
import sqlite3

router = APIRouter()

DB_PATH = "db/nifty100.db"


@router.get("/portfolio/stats")
def get_portfolio_stats():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_companies,
            AVG(roe_percentage) AS avg_roe,
            AVG(roce_percentage) AS avg_roce
        FROM companies
    """)

    data = dict(cursor.fetchone())

    conn.close()

    return data