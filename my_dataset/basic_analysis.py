import pandas as pd 
import numpy as ny

df = pd.read_csv("/home/vijayditya/defi-metrics/my_dataset/1/solana_2020-04-09_2025-06-14.csv")



#print(df.columns[-1])

df.columns = ['day', 'open', 'high', 'low', 'close', 'volume', 'market_cap']



df['day'] = pd.to_datetime(df['day'], format='%d/%m/%Y')


df= df.sort_values("day")

df['avg_price'] = (df['high'] + df['low']) / 2
df['volume_usd'] = df['volume']
df['tvl_usd'] = df['market_cap']

# print(df.head(10))
# print(df['high'].max())
print(df['market_cap'].describe())
