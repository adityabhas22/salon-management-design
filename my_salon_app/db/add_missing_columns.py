import asyncio
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import AsyncSessionLocal
from sqlalchemy import text

async def add_missing_columns():
    async with AsyncSessionLocal() as session:
        try:
            # Check if duration_minutes column exists in services table
            result = await session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'services' AND column_name = 'duration_minutes'
            """))
            
            if not result.fetchone():
                print("Adding duration_minutes column to services table...")
                await session.execute(text("""
                    ALTER TABLE services 
                    ADD COLUMN duration_minutes INTEGER NOT NULL DEFAULT 60
                """))
                print("✅ Added duration_minutes column to services table")
            else:
                print("✅ duration_minutes column already exists in services table")
            
            # Check if start_date column exists in promotions table
            result = await session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'promotions' AND column_name = 'start_date'
            """))
            
            if not result.fetchone():
                print("Adding start_date column to promotions table...")
                await session.execute(text("""
                    ALTER TABLE promotions 
                    ADD COLUMN start_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                """))
                print("✅ Added start_date column to promotions table")
            else:
                print("✅ start_date column already exists in promotions table")
            
            # Check if category column exists in knowledge_base table
            result = await session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'knowledge_base' AND column_name = 'category'
            """))
            
            if not result.fetchone():
                print("Adding category column to knowledge_base table...")
                await session.execute(text("""
                    ALTER TABLE knowledge_base 
                    ADD COLUMN category VARCHAR NULL
                """))
                print("✅ Added category column to knowledge_base table")
            else:
                print("✅ category column already exists in knowledge_base table")
            
            # Commit the changes
            await session.commit()
            print("✅ All changes committed successfully")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(add_missing_columns()) 