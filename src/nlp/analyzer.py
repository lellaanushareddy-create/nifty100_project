import pandas as pd
from src.nlp.parser import extract_percentage, extract_years


def analyze_text(text):
    """
    Analyze a text field and extract useful metrics.
    """

    return {
        "percentage": extract_percentage(text),
        "years": extract_years(text)
    }


if __name__ == "__main__":
    samples = [
        "Sales growth 18% over 5 Years",
        "Profit CAGR 25.4% over 10 Years",
        "ROE is 21%",
        "No percentage here"
    ]

    for sample in samples:
        print(sample)
        print(analyze_text(sample))
        print("-" * 40)