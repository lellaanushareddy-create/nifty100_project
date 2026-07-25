import pytest

# assuming your functions are imported like this:
# from your_module import normalize_year, normalize_ticker


def normalize_year(year):
    return str(year).strip()


def normalize_ticker(ticker):
    return str(ticker).upper().strip()


# -------------------------
# 20 TEST CASES: normalize_ticker
# -------------------------
@pytest.mark.parametrize(
    "input_val, expected",
    [
        ("aapl", "AAPL"),
        ("goog", "GOOG"),
        (" msft ", "MSFT"),
        ("TsLa", "TSLA"),
        ("infy", "INFY"),
        (" tcs", "TCS"),
        ("wipRo ", "WIPRO"),
        ("reliance", "RELIANCE"),
        ("hdfc", "HDFC"),
        (" icici ", "ICICI"),
        ("sbIN", "SBIN"),
        ("baJaj", "BAJAJ"),
        ("maruti", "MARUTI"),
        ("nvdA", "NVDA"),
        ("amzn", "AMZN"),
        (" meta ", "META"),
        ("  ibm", "IBM"),
        ("oracle ", "ORACLE"),
        ("intel", "INTEL"),
        ("salesforce", "SALESFORCE"),
    ],
)
def test_normalize_ticker(input_val, expected):
    assert normalize_ticker(input_val) == expected


# -------------------------
# 15 TEST CASES: normalize_year
# -------------------------
@pytest.mark.parametrize(
    "input_val, expected",
    [
        (2020, "2020"),
        ("2021", "2021"),
        (" 2022 ", "2022"),
        (1999, "1999"),
        ("2000", "2000"),
        (" 2010", "2010"),
        ("2015 ", "2015"),
        (0, "0"),
        (1, "1"),
        ("-2020", "-2020"),
        ("2023", "2023"),
        (" 1995 ", "1995"),
        (2024, "2024"),
        ("  1980  ", "1980"),
        ("3000", "3000"),
    ],
)
def test_normalize_year(input_val, expected):
    assert normalize_year(input_val) == expected
