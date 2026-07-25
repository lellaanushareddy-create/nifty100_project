def free_cash_flow(operating_activity, investing_activity):
    return operating_activity + investing_activity


def cfo_quality_score(cfo_list, pat_list):
    ratios = []

    for cfo, pat in zip(cfo_list, pat_list):
        if pat == 0:
            return None
        ratios.append(cfo / pat)

    avg_ratio = sum(ratios) / len(ratios)

    if avg_ratio > 1.0:
        return "High Quality"
    elif avg_ratio >= 0.5:
        return "Moderate"
    else:
        return "Accrual Risk"


def capex_intensity(investing_activity, sales):
    if sales == 0:
        return None

    intensity = abs(investing_activity) / sales * 100

    if intensity < 3:
        return "Asset Light"
    elif intensity <= 8:
        return "Moderate"
    else:
        return "Capital Intensive"


def fcf_conversion_rate(fcf, operating_profit):
    if operating_profit == 0:
        return None

    return (fcf / operating_profit) * 100


def capital_allocation_pattern(cfo, cfi, cff, cfo_pat_ratio=None):
    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    pattern = (cfo_sign, cfi_sign, cff_sign)

    if pattern == ("+", "-", "-"):
        if cfo_pat_ratio is not None and cfo_pat_ratio > 1.0:
            label = "Shareholder Returns"
        else:
            label = "Reinvestor"
    elif pattern == ("+", "+", "-"):
        label = "Liquidating Assets"
    elif pattern == ("-", "+", "+"):
        label = "Distress Signal"
    elif pattern == ("-", "-", "+"):
        label = "Growth Funded by Debt"
    elif pattern == ("+", "+", "+"):
        label = "Cash Accumulator"
    elif pattern == ("-", "-", "-"):
        label = "Pre-Revenue"
    elif pattern == ("+", "-", "+"):
        label = "Mixed"
    else:
        label = "Other"

    return {
        "cfo_sign": cfo_sign,
        "cfi_sign": cfi_sign,
        "cff_sign": cff_sign,
        "pattern_label": label,
    }
