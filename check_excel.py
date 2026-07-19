import pandas as pd

file = "data/raw/financial_ratios.xlsx"

print("HEADER = 0")
df = pd.read_excel(file, header=0)
print(df.head())
print(df.columns.tolist())

print("\n" + "="*50)

print("HEADER = 1")
df = pd.read_excel(file, header=1)
print(df.head())
print(df.columns.tolist())