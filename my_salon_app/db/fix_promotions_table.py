import asyncio
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import AsyncSessionLocal
from sqlalchemy import text

async def fix_promotions_table():
    async with AsyncSessionLocal() as session:
        try:
            # Check if service_id column exists
            result = await session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'promotions' AND column_name = 'service_id'
            """))
            
            if not result.fetchone():
                print("Adding service_id column to promotions table...")
                await session.execute(text("""
                    ALTER TABLE promotions 
                    ADD COLUMN service_id INTEGER NULL
                """))
                
                # Add foreign key constraint
                print("Adding foreign key constraint to promotions table...")
                await session.execute(text("""
                    ALTER TABLE promotions
                    ADD CONSTRAINT fk_promotions_service
                    FOREIGN KEY (service_id)
                    REFERENCES services(id)
                """))
                
                print("✅ Added service_id column to promotions table")
            else:
                print("✅ service_id column already exists in promotions table")
            
            # Check if end_date column exists
            result = await session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'promotions' AND column_name = 'end_date'
            """))
            
            if not result.fetchone():
                print("Adding end_date column to promotions table...")
                await session.execute(text("""
                    ALTER TABLE promotions 
                    ADD COLUMN end_date TIMESTAMP WITH TIME ZONE NULL
                """))
                
                # Copy data from valid_till to end_date
                print("Copying data from valid_till to end_date...")
                await session.execute(text("""
                    UPDATE promotions
                    SET end_date = valid_till
                """))
                
                print("✅ Added end_date column to promotions table")
            else:
                print("✅ end_date column already exists in promotions table")
            
            # Commit the changes
            await session.commit()
            print("✅ All changes committed successfully")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(fix_promotions_table()) 