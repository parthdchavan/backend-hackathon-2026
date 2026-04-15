#!/usr/bin/env python3
"""
Test authentication for the API
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = "http://localhost:8000"
API_TOKEN = os.getenv("API_TOKEN", "supersecret007")

def test_without_token():
    """Test API call without token - should fail"""
    print("🔒 Testing without authentication token...")
    try:
        response = requests.get(f"{API_BASE}/objections/")
        if response.status_code == 401:
            print("✅ Correctly rejected: 401 Unauthorized")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_with_wrong_token():
    """Test API call with wrong token - should fail"""
    print("\n🔒 Testing with wrong token...")
    try:
        headers = {"Authorization": "Bearer wrongtoken123"}
        response = requests.get(f"{API_BASE}/objections/", headers=headers)
        if response.status_code == 401:
            print("✅ Correctly rejected: 401 Unauthorized")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_with_correct_token():
    """Test API call with correct token - should succeed"""
    print("\n🔓 Testing with correct token...")
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        response = requests.get(f"{API_BASE}/objections/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {len(data)} objections")
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_create_objection():
    """Test creating an objection with authentication"""
    print("\n📝 Testing create objection with authentication...")
    try:
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "objection_text": "This is a test objection for authentication"
        }
        response = requests.post(f"{API_BASE}/objections/", headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Created objection with ID: {result['id']}")
            print(f"   Category: {result['category']}")
            print(f"   Severity: {result['severity']}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("=" * 70)
    print("API Authentication Tests")
    print("=" * 70)
    print(f"API Base URL: {API_BASE}")
    print(f"API Token: {API_TOKEN}")
    print("=" * 70)
    
    # Check if server is running
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ Server is running\n")
        else:
            print("⚠️  Server responded but health check failed\n")
    except Exception as e:
        print(f"❌ Server is not running. Start it with:")
        print(f"   cd backend && uvicorn app.main:app --reload\n")
        return
    
    # Run tests
    test_without_token()
    test_with_wrong_token()
    test_with_correct_token()
    test_create_objection()
    
    print("\n" + "=" * 70)
    print("✅ Authentication tests complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
