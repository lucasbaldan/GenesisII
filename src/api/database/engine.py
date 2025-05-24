from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from dotenv import load_dotenv
import os

load_dotenv()

# Create the SQLAlchemy engine using the SQL_URL environment variable

engine = create_async_engine(os.getenv("SQL_URL"))

async def get_session_engine():
    async with AsyncSession(engine) as session:
        yield session