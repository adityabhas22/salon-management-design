import asyncio
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import AsyncSessionLocal
from sqlalchemy import text

async def check_service_category_references():
    async with AsyncSessionLocal() as session:
        try:
            # Check if there are any services referencing service categories
            result = await session.execute(text("""
                SELECT s.id, s.name, sc.id as category_id, sc.name as category_name
                FROM services s
                JOIN service_categories sc ON s.category_id = sc.id
            """))
            
            references = result.fetchall()
            
            if references:
                print("Services referencing service categories:")
                for ref in references:
                    print(f"- Service ID {ref[0]} ({ref[1]}) references Category ID {ref[2]} ({ref[3]})")
            else:
                print("No services are referencing service categories.")
                
            # Check if there's a foreign key constraint
            result = await session.execute(text("""
                SELECT tc.constraint_name, tc.table_name, kcu.column_name, 
                       ccu.table_name AS foreign_table_name,
                       ccu.column_name AS foreign_column_name 
                FROM information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
                  AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY' 
                  AND tc.table_name = 'services'
                  AND kcu.column_name = 'category_id'
            """))
            
            constraints = result.fetchall()
            
            if constraints:
                print("\nForeign key constraints:")
                for constraint in constraints:
                    print(f"- Constraint {constraint[0]}: {constraint[1]}.{constraint[2]} references {constraint[3]}.{constraint[4]}")
            else:
                print("\nNo foreign key constraints found for services.category_id.")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_service_category_references()) 