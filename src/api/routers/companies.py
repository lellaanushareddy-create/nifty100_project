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