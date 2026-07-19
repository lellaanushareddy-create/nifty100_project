import pandas as pd

df = pd.read_excel("data/raw/prosandcons.xlsx", header=1)

print(df.columns.tolist())
print(df.head())