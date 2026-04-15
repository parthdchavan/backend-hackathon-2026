#!/usr/bin/env python3
"""
Script to view the objections database
Usage: python view_database.py
"""

import sqlite3
import os
from pathlib import Path

# Find the database file
db_paths = [
    "objections.db",
    "backend/objections.db",
    "./objections.db"
]

db_path = None
for path in db_paths:
    if os.path.exists(path):
        db_path = path
        break

if not db_path:
    print("❌ Database file not found!")
    print("\nThe database will be created when you:")
    print("1. Start the backend server: cd backend && uvicorn app.main:app --reload")
    print("2. Create your first objection through the UI")
    print("\nExpected location: ./objections.db or ./backend/objections.db")
    exit(1)

print(f"✅ Found database at: {db_path}\n")

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get table info
print("=" * 80)
print("TABLE: objections")
print("=" * 80)

# Show table schema
cursor.execute("PRAGMA table_info(objections)")
columns = cursor.fetchall()

print("\nTable Schema:")
print("-" * 80)
for col in columns:
    print(f"  {col[1]:20} {col[2]:15} {'PRIMARY KEY' if col[5] else ''} {'NOT NULL' if col[3] else 'NULL'}")

# Count records
cursor.execute("SELECT COUNT(*) FROM objections")
count = cursor.fetchone()[0]
print(f"\nTotal Records: {count}")

if count > 0:
    print("\n" + "=" * 80)
    print("RECORDS:")
    print("=" * 80)
    
    # Fetch all records
    cursor.execute("""
        SELECT id, objection_text, response, category, severity, created_at 
        FROM objections 
        ORDER BY created_at DESC
    """)
    
    records = cursor.fetchall()
    
    for i, record in enumerate(records, 1):
        print(f"\n[Record #{i}]")
        print(f"  ID:         {record[0]}")
        print(f"  Objection:  {record[1][:100]}{'...' if len(record[1]) > 100 else ''}")
        print(f"  Response:   {record[2][:100]}{'...' if len(record[2]) > 100 else ''}")
        print(f"  Category:   {record[3]}")
        print(f"  Severity:   {record[4]}")
        print(f"  Created:    {record[5]}")
        print("-" * 80)

conn.close()

print("\n💡 To view in SQLite browser:")
print(f"   sqlite3 {db_path}")
print("\n💡 To query manually:")
print(f"   sqlite3 {db_path} 'SELECT * FROM objections;'")
