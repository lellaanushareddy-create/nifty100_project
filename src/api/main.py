from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import time

from .routers import (
    companies,
    documents,
    health,
    peers,
    portfolio,
    screener,
    sectors,
    valuation,
)

app = FastAPI(
    title="Nifty100 Analytics API",
    version="1.0.0",
    description="FastAPI backend for Nifty100 Analytics Project"
)


# SQLite connection
def get_connection():
    conn = sqlite3.connect("db/nifty100.db")
    return conn


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = round(time.time() - start, 4)

    print(
        f"{request.method} {request.url.path} "
        f"Status:{response.status_code} "
        f"Time:{process_time}s"
    )

    return response


# Include routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(companies.router, prefix="/api/v1")
app.include_router(screener.router, prefix="/api/v1")
app.include_router(sectors.router, prefix="/api/v1")
app.include_router(peers.router, prefix="/api/v1")
app.include_router(valuation.router, prefix="/api/v1")
app.include_router(portfolio.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Welcome to Nifty100 Analytics API",
        "version": "1.0.0"
    }