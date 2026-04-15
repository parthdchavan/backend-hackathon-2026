#!/usr/bin/env python3
"""
Verify PostgreSQL connection and check/create objections table
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import engine, Base
from app.models import Objection
from sqlalchemy import inspect, text

def verify_connection():
    print("🔍 Verifying PostgreSQL connection...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL!")
            print(f"   Version: {version[:50]}...")
            return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def check_table():
    print("\n🔍 Checking if 'objections' table exists...")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if 'objections' in tables:
        print("✅ Table 'objections' already exists!")
        
        # Get column info
        columns = inspector.get_columns('objections')
        print("\n📋 Table Schema:")
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            print(f"   - {col['name']:20} {str(col['type']):20} {nullable}")
        
        # Count records
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM objections"))
            count = result.fetchone()[0]
            print(f"\n📊 Total records: {count}")
        
        return True
    else:
        print("⚠️  Table 'objections' does not exist")
        return False

def create_table():
    print("\n🔨 Creating 'objections' table...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Table created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create table: {e}")
        return False

def main():
    print("=" * 70)
    print("PostgreSQL Database Verification")
    print("=" * 70)
    
    # Step 1: Verify connection
    if not verify_connection():
        print("\n❌ Cannot proceed without database connection")
        return
    
    # Step 2: Check if table exists
    table_exists = check_table()
    
    # Step 3: Create table if needed
    if not table_exists:
        response = input("\n❓ Would you like to create the table? (yes/no): ")
        if response.lower() in ['yes', 'y']:
            create_table()
            check_table()  # Verify creation
        else:
            print("⏭️  Skipping table creation")
    
    print("\n" + "=" * 70)
    print("✅ Verification complete!")
    print("=" * 70)
    print("\n💡 Your application is now configured to use PostgreSQL")
    print("   Start the backend: cd backend && uvicorn app.main:app --reload")

if __name__ == "__main__":
    main()
