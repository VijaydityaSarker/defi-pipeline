import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL   
import os
from dotenv import load_dotenv


df = pd.read_csv("/home/vijayditya/defi-metrics/my_dataset/1/solana_2020-04-09_2025-06-14.csv")
df.columns = ['day', 'open', 'high', 'low', 'close', 'volume', 'market_cap']
df['day'] = pd.to_datetime(df['day'], format='%d/%m/%Y')
df = df.sort_values('day')
df['avg_price'] = (df['high'] + df['low']) / 2
df['volume_usd'] = df['volume']
df['tvl_usd'] = df['market_cap']
df['base_amount'] = df['volume_usd'] / df['avg_price']
df['quote_amount'] = df['volume_usd']


# --- 2. Prepare tables ---

# tvl_snapshots table
tvl_df = df[['day', 'tvl_usd']].copy()
tvl_df.rename(columns={'day': 'snapped_at'}, inplace=True)
tvl_df['protocol'] = 'solana_network'
tvl_df['chain'] = 'solana'


# trades table
trades_df = df[['day', 'base_amount', 'quote_amount']].copy()
trades_df.rename(columns={'day': 'traded_at'}, inplace=True)
trades_df['chain'] = 'solana'
trades_df['dex'] = 'simulated'
trades_df['base_symbol'] = 'SOL'
trades_df['quote_symbol'] = 'USD'
trades_df['fee_bps'] = 25
trades_df['tx_hash'] = None 

load_dotenv()  # ensure .env is loaded

db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),      # e.g. postgres.<project-ref>
    password=os.getenv("DB_PASSWORD"),  # raw; SQLAlchemy will escape safely
    host=os.getenv("DB_HOST"),          # e.g. aws-1-eu-west-1.pooler.supabase.com
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "postgres"),
    query={"sslmode": "require"},       # Supabase requires SSL
)

engine = create_engine(db_url)

# quick probe before inserts
with engine.connect() as conn:
    print("✅ Connected to:", conn.exec_driver_sql("select version()").scalar())


tvl_df.to_sql('tvl_snapshots', con=engine, if_exists='append', index=False)
trades_df.to_sql('trades', con=engine, if_exists='append', index=False)

print("✅ Loaded Solana dataset into Supabase tables successfully!")