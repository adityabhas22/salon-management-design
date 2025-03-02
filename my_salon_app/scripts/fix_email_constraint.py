import asyncio
import os
from sqlalchemy import text
from app.database import AsyncSessionLocal

async def fix_email_constraint():
    """Fix the email constraint in the customers table."""
    print("Fixing email constraint in customers table...")
    
    async with AsyncSessionLocal() as session:
        try:
            # Execute raw SQL to alter the table
            await session.execute(text("ALTER TABLE customers ALTER COLUMN email DROP NOT NULL;"))
            await session.commit()
            print("✅ Successfully made email column nullable")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(fix_email_constraint()) 