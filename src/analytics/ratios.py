def net_profit_margin(net_profit, sales):
    if sales == 0:
        return None
    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit, sales):
    if sales == 0:
        return None
    return (operating_profit / sales) * 100


def roe(net_profit, equity_capital, reserves):
    total_equity = equity_capital + reserves
    if total_equity <= 0:
        return None
    return (net_profit / total_equity) * 100


def roce(ebit, equity_capital, reserves, borrowings):
    capital_employed = equity_capital + reserves + borrowings
    if capital_employed <= 0:
        return None
    return (ebit / capital_employed) * 100


def roa(net_profit, total_assets):
    if total_assets == 0:
        return None
    return (net_profit / total_assets) * 100

def debt_to_equity(borrowings, equity_capital, reserves):
    if borrowings == 0:
        return 0

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return borrowings / total_equity


def high_leverage_flag(de_ratio, broad_sector):
    if de_ratio is None:
        return False

    return de_ratio > 5 and broad_sector != "Financials"


def interest_coverage_ratio(operating_profit, other_income, interest):
    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def icr_label(icr):
    if icr is None:
        return "Debt Free"
    return ""


def icr_warning_flag(icr):
    if icr is None:
        return False

    return icr < 1.5


def net_debt(borrowings, investments):
    return borrowings - investments


def asset_turnover(sales, total_assets):
    if total_assets == 0:
        return None

    return sales / total_assets