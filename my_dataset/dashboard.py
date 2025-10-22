import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.engine import URL  
from dotenv import load_dotenv
import os


load_dotenv()

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

st.set_page_config(page_title="Solana TVL & Volume", layout="wide")
st.title("Solana TVL & Volume Dashboard")

# --- Query Data ---
tvl = pd.read_sql(
    """
    select snapped_at::date as day, tvl_usd
    from tvl_snapshots
    where protocol='solana_network' and chain='solana'
    order by day
    """,
    engine,
)

# --- Plot with 6-month tick intervals ---
fig = px.line(
    tvl,
    x="day",
    y="tvl_usd",
    title="Solana Total Value Locked (TVL)",
    labels={"day": "Date", "tvl_usd": "TVL (USD)"},
)

# Force tick every 6 months
fig.update_xaxes(
    dtick="M6",  # every 6 months
    tickformat="%b %Y",  # show like "Jun 2024"
    ticklabelmode="period",
)
fig.update_layout(height=500, showlegend=False)

st.plotly_chart(fig, use_container_width=True)
