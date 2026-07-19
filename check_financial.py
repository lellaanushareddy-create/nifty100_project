import pandas as pd

file = "data/raw/financial_ratios.xlsx"

for i in range(6):
    df = pd.read_excel(file, header=i)
    print("\nHEADER =", i)
    print(df.columns.tolist())