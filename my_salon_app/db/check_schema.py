import asyncio
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import AsyncSessionLocal
from sqlalchemy import text

async def check_schema():
    async with AsyncSessionLocal() as session:
        try:
            # Check services table columns
            result = await session.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'services'
            """))
            services_columns = result.fetchall()
            print('Services table columns:')
            for column in services_columns:
                print(f'- {column[0]} ({column[1]})')
            
            # Check if duration_minutes exists
            result = await session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'services' AND column_name = 'duration_minutes'
            """))
            if result.fetchone():
                print("\n✅ duration_minutes column exists in services table")
            else:
                print("\n❌ duration_minutes column MISSING from services table")
            
            # Check promotions table columns
            result = await session.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'promotions'
            """))
            promotions_columns = result.fetchall()
            print('\nPromotions table columns:')
            for column in promotions_columns:
                print(f'- {column[0]} ({column[1]})')
            
            # Check if start_date exists
            result = await session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'promotions' AND column_name = 'start_date'
            """))
            if result.fetchone():
                print("\n✅ start_date column exists in promotions table")
            else:
                print("\n❌ start_date column MISSING from promotions table")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_schema()) 