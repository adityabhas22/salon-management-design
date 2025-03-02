import asyncio
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import AsyncSessionLocal
from sqlalchemy import text

async def check_services_schema():
    async with AsyncSessionLocal() as session:
        try:
            # Check services table columns
            result = await session.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'services'
                ORDER BY ordinal_position
            """))
            services_columns = result.fetchall()
            print('Services table columns:')
            for column in services_columns:
                print(f'- {column[0]} ({column[1]})')
            
            # Check if category_id exists
            result = await session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'services' AND column_name = 'category_id'
            """))
            if result.fetchone():
                print("\n✅ category_id column exists in services table")
            else:
                print("\n❌ category_id column MISSING from services table")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_services_schema()) 