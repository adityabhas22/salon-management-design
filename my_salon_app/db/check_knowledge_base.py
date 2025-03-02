import asyncio
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import AsyncSessionLocal
from sqlalchemy import text

async def check_knowledge_base_schema():
    async with AsyncSessionLocal() as session:
        try:
            # Check if knowledge_base table exists
            result = await session.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'knowledge_base'
                )
            """))
            exists = result.scalar()
            
            if exists:
                print("✅ knowledge_base table exists")
                
                # Check columns
                result = await session.execute(text("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'knowledge_base'
                """))
                columns = result.fetchall()
                print("Columns in knowledge_base table:")
                for column in columns:
                    print(f"- {column[0]} ({column[1]})")
            else:
                print("❌ knowledge_base table does not exist")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_knowledge_base_schema()) 