-- 1
SELECT COUNT(*) FROM companies;

-- 2
SELECT sector, COUNT(*) 
FROM companies
GROUP BY sector;

-- 3
SELECT ticker, company_name
FROM companies
LIMIT 10;

-- 4
SELECT COUNT(*) FROM balancesheet;

-- 5
SELECT COUNT(*) FROM profitandloss;

-- 6
SELECT COUNT(*) FROM cashflow;

-- 7
SELECT AVG(close_price)
FROM stock_prices;

-- 8
SELECT MAX(market_cap)
FROM market_cap;

-- 9
SELECT *
FROM financial_ratios
LIMIT 5;

-- 10
SELECT company_id, COUNT(*)
FROM stock_prices
GROUP BY company_id;