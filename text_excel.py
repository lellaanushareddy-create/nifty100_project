import pandas as pd

df = pd.read_excel("data/raw/profitandloss.xlsx", header=None)

print(df.head(10))