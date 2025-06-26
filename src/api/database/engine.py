from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from dotenv import load_dotenv
import os

load_dotenv()

# Create the SQLAlchemy engine using the SQL_URL environment variable

engine = create_async_engine(os.getenv("SQL_URL"))

# FAST_API
async def get_session_engine():
    async with AsyncSession(engine) as session:
        yield session

# OUTROS LUGARES DO PROJETO
@asynccontextmanager
async def get_session_engine_context():
    async with AsyncSession(engine) as session:
        yield session
