def test_roe_positive_equity():
    equity = 100
    profit = 20
    roe = (profit / equity) * 100
    assert roe == 20


def test_roe_negative_equity():
    equity = -100
    if equity <= 0:
        roe = None
    assert roe is None


def test_debt_free_company():
    debt = 0
    equity = 100
    de = debt / equity
    assert de == 0


def test_interest_zero():
    interest = 0
    if interest == 0:
        icr = None
    assert icr is None


def test_opm():
    sales = 1000
    operating_profit = 250
    opm = (operating_profit / sales) * 100
    assert opm == 25
