from src.nlp.parser import extract_percentage, extract_years

samples = [
    "Sales growth 18% over 5 Years",
    "Profit CAGR 25.4% over 10 Years",
    "ROE is 21%",
    "No percentage here"
]

for text in samples:
    print(f"Text: {text}")
    print("Percentage:", extract_percentage(text))
    print("Years:", extract_years(text))
    print("-" * 40)