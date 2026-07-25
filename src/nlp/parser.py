import re

import pandas as pd


def extract_percentage(text):
    """
    Extract first percentage value from text.
    Example:
    'Sales growth 18% over 5 Years'
    -> 18
    """
    if pd.isna(text):
        return None

    text = str(text)

    match = re.search(r"(\d+(\.\d+)?)\s*%", text)

    if match:
        return float(match.group(1))

    return None


def extract_years(text):
    """
    Extract year value.
    Example:
    '18% over 5 Years'
    -> 5
    """
    if pd.isna(text):
        return None

    text = str(text)

    match = re.search(r"(\d+)\s*Years?", text, re.IGNORECASE)

    if match:
        return int(match.group(1))

    return None
