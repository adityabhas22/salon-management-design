import asyncio
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import AsyncSessionLocal
from sqlalchemy import text

async def check_alembic_version():
    async with AsyncSessionLocal() as session:
        try:
            # Check if alembic_version table exists
            result = await session.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'alembic_version'
                )
            """))
            exists = result.scalar()
            
            if exists:
                print("✅ alembic_version table exists")
                
                # Check current version
                result = await session.execute(text("SELECT version_num FROM alembic_version"))
                version = result.scalar()
                print(f"Current version: {version}")
            else:
                print("❌ alembic_version table does not exist")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_alembic_version()) 