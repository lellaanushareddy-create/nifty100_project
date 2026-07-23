from fastapi import APIRouter
import sqlite3

router = APIRouter()

DB_PATH = "db/nifty100.db"


@router.get("/documents")
def get_documents():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM annual_reports
    """)

    data = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return data