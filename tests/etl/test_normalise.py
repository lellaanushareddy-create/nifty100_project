import os
import sys

sys.path.append(os.getcwd())

from src.loader import normalize_ticker, normalize_year


def test_normalize_year_int():
    assert normalize_year(2024) == "2024"


def test_normalize_year_string():
    assert normalize_year("2024") == "2024"


def test_normalize_year_spaces():
    assert normalize_year(" 2024 ") == "2024"


def test_normalize_year_float():
    assert normalize_year(2024.0) == "2024.0"


def test_normalize_year_none():
    assert normalize_year(None) == "None"


def test_normalize_ticker_lower():
    assert normalize_ticker("tcs") == "TCS"


def test_normalize_ticker_upper():
    assert normalize_ticker("INFY") == "INFY"


def test_normalize_ticker_spaces():
    assert normalize_ticker("  hdfc  ") == "HDFC"


def test_normalize_ticker_mixed():
    assert normalize_ticker("ReLiAnCe") == "RELIANCE"


def test_normalize_ticker_none():
    assert normalize_ticker(None) == "NONE"
