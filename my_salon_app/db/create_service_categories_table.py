import asyncio
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import AsyncSessionLocal
from sqlalchemy import text

async def create_service_categories_table():
    async with AsyncSessionLocal() as session:
        try:
            # Check if service_categories table exists
            result = await session.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'service_categories'
                )
            """))
            exists = result.scalar()
            
            if exists:
                print("✅ service_categories table already exists")
                return
            
            # Create service_categories table
            print("Creating service_categories table...")
            await session.execute(text("""
                CREATE TABLE service_categories (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR NOT NULL UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """))
            
            # Add foreign key to services table if it exists
            result = await session.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'services'
                )
            """))
            services_exists = result.scalar()
            
            if services_exists:
                # Check if category_id column exists in services table
                result = await session.execute(text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.columns
                        WHERE table_name = 'services' AND column_name = 'category_id'
                    )
                """))
                column_exists = result.scalar()
                
                if column_exists:
                    # Add foreign key constraint
                    print("Adding foreign key constraint to services table...")
                    await session.execute(text("""
                        ALTER TABLE services
                        ADD CONSTRAINT fk_services_category
                        FOREIGN KEY (category_id)
                        REFERENCES service_categories(id)
                    """))
            
            await session.commit()
            print("✅ service_categories table created successfully")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(create_service_categories_table()) 