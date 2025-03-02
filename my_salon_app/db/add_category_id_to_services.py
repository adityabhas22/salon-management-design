import asyncio
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import AsyncSessionLocal
from sqlalchemy import text

async def add_category_id_to_services():
    async with AsyncSessionLocal() as session:
        try:
            # Check if category_id column exists in services table
            result = await session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'services' AND column_name = 'category_id'
            """))
            
            if not result.fetchone():
                print("Adding category_id column to services table...")
                await session.execute(text("""
                    ALTER TABLE services 
                    ADD COLUMN category_id INTEGER NULL
                """))
                
                # Add foreign key constraint
                print("Adding foreign key constraint to services table...")
                await session.execute(text("""
                    ALTER TABLE services
                    ADD CONSTRAINT fk_services_category
                    FOREIGN KEY (category_id)
                    REFERENCES service_categories(id)
                """))
                
                print("✅ Added category_id column to services table")
            else:
                print("✅ category_id column already exists in services table")
            
            # Commit the changes
            await session.commit()
            print("✅ All changes committed successfully")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(add_category_id_to_services()) 