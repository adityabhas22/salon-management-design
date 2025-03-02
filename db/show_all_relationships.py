import asyncio
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from my_salon_app.app.database import AsyncSessionLocal
from sqlalchemy import text

async def get_all_tables():
    """Get a list of all tables in the database"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        return [row[0] for row in result.fetchall()]

async def get_table_columns(table_name):
    """Get all columns for a specific table"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(text(f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """))
        return result.fetchall()

async def get_foreign_keys(table_name):
    """Get all foreign keys for a specific table"""
    async with AsyncSessionLocal() as session:
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
        return result.fetchall()

async def get_referenced_by(table_name):
    """Get all tables that reference this table"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(text(f"""
            SELECT
                tc.table_name AS referencing_table,
                kcu.column_name AS referencing_column,
                ccu.column_name AS referenced_column
            FROM
                information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
                  AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY' AND ccu.table_name = '{table_name}'
        """))
        return result.fetchall()

async def show_all_relationships():
    """Show all tables and their relationships"""
    try:
        tables = await get_all_tables()
        
        if not tables:
            print("No tables found in the database.")
            return
        
        print(f"Found {len(tables)} tables in the database:")
        print("=" * 80)
        
        # Store relationships for visualization
        relationships = []
        
        for table_name in tables:
            print(f"\n📋 TABLE: {table_name}")
            print("-" * 80)
            
            # Get and display columns
            columns = await get_table_columns(table_name)
            if columns:
                print(f"{'Column':<20} {'Type':<20} {'Nullable':<10} {'Default':<20}")
                print("-" * 70)
                for column in columns:
                    print(f"{column[0]:<20} {column[1]:<20} {column[2]:<10} {str(column[3] or ''):<20}")
            else:
                print("No columns found for this table.")
            
            # Get and display foreign keys (outgoing relationships)
            foreign_keys = await get_foreign_keys(table_name)
            if foreign_keys:
                print("\n🔑 Foreign Keys (This table references):")
                for fk in foreign_keys:
                    print(f"  - {table_name}.{fk[1]} → {fk[2]}.{fk[3]} (Constraint: {fk[0]})")
                    relationships.append((table_name, fk[2], fk[1], fk[3]))
            else:
                print("\n🔑 Foreign Keys: None")
            
            # Get and display tables that reference this table (incoming relationships)
            referenced_by = await get_referenced_by(table_name)
            if referenced_by:
                print("\n🔄 Referenced By (Tables that reference this table):")
                for ref in referenced_by:
                    print(f"  - {ref[0]}.{ref[1]} → {table_name}.{ref[2]}")
            else:
                print("\n🔄 Referenced By: None")
        
        # Print a summary of all relationships
        print("\n\n" + "=" * 80)
        print("SUMMARY OF ALL RELATIONSHIPS")
        print("=" * 80)
        
        if relationships:
            for source, target, source_col, target_col in relationships:
                print(f"{source}.{source_col} → {target}.{target_col}")
        else:
            print("No relationships found between tables.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(show_all_relationships()) 