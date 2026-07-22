from fastapi import APIRouter
import sqlite3
from pathlib import Path
import time

router = APIRouter(tags=["Health"])

ROOT = Path(__file__).resolve().parents[3]
DB_PATH = ROOT / "db" / "nifty100.db"

start_time = time.time()


@router.get("/health")
def health():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = [
        "companies",
        "balancesheet",
        "cashflow",
        "profitandloss",
        "market_cap",
        "financial_ratios",
        "peer_groups",
        "sectors",
        "analysis",
        "prosandcons"
    ]

    row_counts = {}

    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_counts[table] = cursor.fetchone()[0]
        except:
            row_counts[table] = 0

    conn.close()

    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime_seconds": round(time.time() - start_time, 2),
        "db_row_counts": row_counts
    }