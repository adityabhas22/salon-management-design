import asyncio
from sqlalchemy import text
from app.database import AsyncSessionLocal

async def list_tables():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = result.fetchall()
            print('Tables in database:')
            for table in tables:
                print(f'- {table[0]}')
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(list_tables()) 