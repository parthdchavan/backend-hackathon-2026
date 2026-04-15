"""Test script to verify database storage is working correctly"""
import sys
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models import Objection
from datetime import datetime

def test_database():
    db = SessionLocal()
    
    # Test creating a record
    test_objection = Objection(
        objection_text="Test objection",
        response="Test response",
        category="Price",
        severity="High",
        embedding='[0.1, 0.2, 0.3]'
    )
    
    db.add(test_objection)
    db.commit()
    db.refresh(test_objection)
    
    print("✅ Test record created:")
    print(f"   ID: {test_objection.id}")
    print(f"   Objection: {test_objection.objection_text}")
    print(f"   Response: {test_objection.response}")
    print(f"   Category: {test_objection.category}")
    print(f"   Severity: {test_objection.severity}")
    print(f"   Embedding: {test_objection.embedding[:20]}...")
    print(f"   Created: {test_objection.created_at}")
    
    # Verify it's in the database
    all_records = db.query(Objection).all()
    print(f"\n✅ Total records in database: {len(all_records)}")
    
    # Clean up test record
    db.delete(test_objection)
    db.commit()
    print("✅ Test record deleted")
    
    db.close()

if __name__ == "__main__":
    test_database()
