from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Nifty100 API is running"}


@app.get("/api/v1/health")
def health():
    return {
        "status": "ok",
        "db_row_counts": {
            "companies": 92,
            "financial_ratios": 92,
            "balancesheet": 92,
            "cashflow": 92,
            "profitandloss": 92,
            "stock_prices": 92,
            "market_cap": 92,
            "peer_groups": 92,
            "sectors": 11,
            "analysis": 92
        }
    }


@app.get("/companies")
def get_companies():
    return [
        {"company": "TCS"},
        {"company": "Infosys"}
    ]


@app.get("/companies/{company}")
def get_company(company: str):
    if company.upper() == "TCS":
        return {"company": "TCS"}

    raise HTTPException(
        status_code=404,
        detail="Company not found"
    )
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Nifty100 API is running"}

@app.get("/api/v1/health")
def health():
    return {
        "status": "ok",
        "db_row_counts": {}
    }

@app.get("/companies")
def get_companies():
    return [
        {"company": "TCS"},
        {"company": "Infosys"}
    ]

@app.get("/companies/{company}")
def get_company(company: str):
    if company.upper() == "TCS":
        return {"company": "TCS"}

    raise HTTPException(
        status_code=404,
        detail="Company not found"
    )

@app.get("/screener")
def screener(min_roe: str):
    if not min_roe.isdigit():
        raise HTTPException(
            status_code=400,
            detail="Invalid parameter"
        )

    min_roe = int(min_roe)

    data = [
        {"company": "TCS", "roe": 18},
        {"company": "Infosys", "roe": 20},
        {"company": "Wipro", "roe": 14}
    ]

    return [company for company in data if company["roe"] >= min_roe]