CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT
    sector TEXT
);

CREATE TABLE IF NOT EXISTS financial_ratios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT,
    roe REAL,
    roa REAL,
    debt_to_equity REAL,
    pe_ratio REAL
);