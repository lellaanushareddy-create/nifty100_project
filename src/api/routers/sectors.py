from fastapi import APIRouter
import sqlite3

router = APIRouter()

@router.get("/sectors/{sector}/companies")
def get_sector_companies(sector: str):
    conn = sqlite3.connect("db/nifty100.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT
        c.company_name,
        c.id AS ticker,
        s.broad_sector
    FROM companies c
    JOIN sectors s
        ON c.id = s.company_id
    WHERE s.broad_sector = ?
    ORDER BY c.company_name
    """

    cursor.execute(query, (sector,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"error": "Sector not found"}

    return [dict(row) for row in rows]