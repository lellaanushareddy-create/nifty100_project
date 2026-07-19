from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)


def test_normal_cagr():
    value, flag = calculate_cagr(100, 200, 5)
    assert flag is None
    assert value is not None


def test_decline_to_loss():
    value, flag = calculate_cagr(100, -50, 5)
    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_turnaround():
    value, flag = calculate_cagr(-100, 50, 5)
    assert value is None
    assert flag == "TURNAROUND"


def test_both_negative():
    value, flag = calculate_cagr(-100, -50, 5)
    assert value is None
    assert flag == "BOTH_NEGATIVE"


def test_zero_base():
    value, flag = calculate_cagr(0, 100, 5)
    assert value is None
    assert flag == "ZERO_BASE"


def test_insufficient_data():
    value, flag = calculate_cagr(100, 200, 0)
    assert value is None
    assert flag == "INSUFFICIENT_DATA"


def test_revenue():
    value, flag = revenue_cagr(100, 200, 5)
    assert flag is None


def test_pat():
    value, flag = pat_cagr(50, 100, 3)
    assert flag is None


def test_eps():
    value, flag = eps_cagr(10, 20, 10)
    assert flag is None


def test_same_values():
    value, flag = calculate_cagr(100, 100, 5)
    assert value == 0.0
    assert flag is None