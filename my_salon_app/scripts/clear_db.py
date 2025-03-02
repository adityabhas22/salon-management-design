import asyncio
from sqlalchemy import text
from app.database import AsyncSessionLocal, engine
from app.models import Base

async def clear_database():
    # First drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("All tables dropped.")
        
        # Then recreate all tables
        await conn.run_sync(Base.metadata.create_all)
        print("All tables recreated.")
    
    print("Database cleared successfully!")

if __name__ == "__main__":
    asyncio.run(clear_database()) 