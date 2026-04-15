#!/usr/bin/env python3
"""
View data from PostgreSQL objections table
Usage: python view_postgres_data.py
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__) / "backend"))

from backend.app.database import engine
from sqlalchemy import text

def view_data():
    print("=" * 80)
    print("PostgreSQL - Objections Table Data")
    print("=" * 80)
    
    try:
        with engine.connect() as conn:
            # Count records
            result = conn.execute(text("SELECT COUNT(*) FROM objections"))
            count = result.fetchone()[0]
            print(f"\n📊 Total Records: {count}\n")
            
            if count == 0:
                print("No objections found. Create one through the UI!")
                return
            
            # Fetch all records
            result = conn.execute(text("""
                SELECT id, objection_text, response, category, severity, created_at 
                FROM objections 
                ORDER BY created_at DESC
            """))
            
            records = result.fetchall()
            
            print("=" * 80)
            for i, record in enumerate(records, 1):
                print(f"\n[Record #{i}]")
                print(f"  ID:         {record[0]}")
                print(f"  Objection:  {record[1][:100]}{'...' if len(record[1]) > 100 else ''}")
                print(f"  Response:   {record[2][:100]}{'...' if len(record[2]) > 100 else ''}")
                print(f"  Category:   {record[3]}")
                print(f"  Severity:   {record[4]}")
                print(f"  Created:    {record[5]}")
                print("-" * 80)
            
            print("\n✅ Data retrieved successfully from PostgreSQL!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    view_data()
