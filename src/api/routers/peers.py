from fastapi import APIRouter
import sqlite3

router = APIRouter()

DB_PATH = "db/nifty100.db"


@router.get("/peers/{group_name}")
def get_peer_group(group_name: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM peer_groups
    WHERE peer_group_name = ?
    ORDER BY company_id
    """

    cursor.execute(query, (group_name,))
    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    if not data:
        return {"error": "Peer group not found"}

    return data