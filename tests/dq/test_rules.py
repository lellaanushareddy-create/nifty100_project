import pandas as pd


def test_missing_value():
    df = pd.DataFrame({"name": ["A", None]})
    assert df["name"].isnull().sum() == 1


def test_duplicate_rows():
    df = pd.DataFrame({"id": [1, 1, 2]})
    assert df.duplicated().sum() == 1


def test_negative_value():
    df = pd.DataFrame({"sales": [100, -50]})
    assert (df["sales"] < 0).sum() == 1


def test_empty_dataframe():
    df = pd.DataFrame()
    assert df.empty


def test_column_exists():
    df = pd.DataFrame({"company": ["TCS"]})
    assert "company" in df.columns
