import asyncio
from sqlalchemy import text
from app.database import AsyncSessionLocal

async def test_connection():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(text('SELECT 1'))
            print("Database connection successful!")
            print(result.scalar())
        except Exception as e:
            print(f"Error connecting to database: {e}")
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(test_connection()) 