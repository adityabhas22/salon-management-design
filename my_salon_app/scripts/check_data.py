import asyncio
import sys
import os
from sqlalchemy import text

# Add parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import AsyncSessionLocal

async def count_records():
    async with AsyncSessionLocal() as session:
        tables = [
            'customers', 
            'staff', 
            'services', 
            'appointments', 
            'feedback', 
            'promotions', 
            'knowledge_base'
        ]
        
        print('Current record counts:')
        for table in tables:
            try:
                result = await session.execute(text(f'SELECT COUNT(*) FROM {table}'))
                count = result.scalar()
                print(f'- {table}: {count}')
            except Exception as e:
                print(f'- {table}: Error - {str(e)}')

if __name__ == "__main__":
    asyncio.run(count_records()) 