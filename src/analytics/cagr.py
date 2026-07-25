from math import pow


def calculate_cagr(start, end, years):
    """
    Returns:
        (cagr_value, flag)

    Flags:
        None
        DECLINE_TO_LOSS
        TURNAROUND
        BOTH_NEGATIVE
        ZERO_BASE
        INSUFFICIENT_DATA
    """

    if years is None or years <= 0:
        return None, "INSUFFICIENT_DATA"

    if start == 0:
        return None, "ZERO_BASE"

    if start > 0 and end > 0:
        cagr = (pow(end / start, 1 / years) - 1) * 100
        return round(cagr, 2), None

    if start > 0 and end < 0:
        return None, "DECLINE_TO_LOSS"

    if start < 0 and end > 0:
        return None, "TURNAROUND"

    if start < 0 and end < 0:
        return None, "BOTH_NEGATIVE"

    return None, "INSUFFICIENT_DATA"


def revenue_cagr(start, end, years):
    return calculate_cagr(start, end, years)


def pat_cagr(start, end, years):
    return calculate_cagr(start, end, years)


def eps_cagr(start, end, years):
    return calculate_cagr(start, end, years)
