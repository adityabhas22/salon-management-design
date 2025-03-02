import asyncio
import sys
import os
import argparse

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import AsyncSessionLocal
from sqlalchemy import text

async def check_table_schema(table_name):
    async with AsyncSessionLocal() as session:
        try:
            # Check if table exists
            result = await session.execute(text(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = '{table_name}'
                )
            """))
            exists = result.scalar()
            
            if not exists:
                print(f"❌ Table '{table_name}' does not exist")
                return
            
            # Get table columns
            result = await session.execute(text(f"""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
            """))
            
            columns = result.fetchall()
            
            if columns:
                print(f"Table '{table_name}' schema:")
                print(f"{'Column':<20} {'Type':<20} {'Nullable':<10} {'Default':<20}")
                print("-" * 70)
                for column in columns:
                    print(f"{column[0]:<20} {column[1]:<20} {column[2]:<10} {str(column[3] or ''):<20}")
            else:
                print(f"No columns found for table '{table_name}'")
                
            # Get foreign keys
            result = await session.execute(text(f"""
                SELECT
                    tc.constraint_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM
                    information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                      AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                      ON ccu.constraint_name = tc.constraint_name
                      AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = '{table_name}'
            """))
            
            foreign_keys = result.fetchall()
            
            if foreign_keys:
                print("\nForeign Keys:")
                for fk in foreign_keys:
                    print(f"- {fk[1]} -> {fk[2]}.{fk[3]} (Constraint: {fk[0]})")
            else:
                print("\nNo foreign keys found")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check database table schema')
    parser.add_argument('table_name', help='Name of the table to check')
    args = parser.parse_args()
    
    asyncio.run(check_table_schema(args.table_name)) 