import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(os.getenv("MY_DB_URL"))

with engine.connect() as conn:
    print("✅ Connected:", conn.exec_driver_sql("select current_database();").scalar())