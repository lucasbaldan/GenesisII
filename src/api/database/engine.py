from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

load_dotenv()

# Create the SQLAlchemy engine using the SQL_URL environment variable

engine = create_engine(os.getenv("SQL_URL"))

def get_session_engine():
    print("CONECTADO AO BANCO DE PRODUÇÃO")
    with Session(engine) as session:
        yield session