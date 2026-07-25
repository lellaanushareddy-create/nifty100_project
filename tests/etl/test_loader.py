import os


def test_data_folder_exists():
    assert os.path.exists("data/raw")


def test_excel_files_exist():
    files = [f for f in os.listdir("data/raw") if f.endswith(".xlsx")]
    assert len(files) > 0


def test_companies_file():
    assert os.path.exists("data/raw/companies.xlsx")


def test_balancesheet_file():
    assert os.path.exists("data/raw/balancesheet.xlsx")


def test_cashflow_file():
    assert os.path.exists("data/raw/cashflow.xlsx")


def test_profitandloss_file():
    assert os.path.exists("data/raw/profitandloss.xlsx")


def test_analysis_file():
    assert os.path.exists("data/raw/analysis.xlsx")


def test_financial_ratios_file():
    assert os.path.exists("data/raw/financial_ratios.xlsx")


def test_peer_groups_file():
    assert os.path.exists("data/raw/peer_groups.xlsx")


def test_documents_file():
    assert os.path.exists("data/raw/documents.xlsx")
