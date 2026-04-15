#!/bin/bash

echo "==================================="
echo "Quick Test - Sales Objection API"
echo "==================================="

# Test health endpoint
echo -e "\n1. Testing health endpoint..."
curl -s http://localhost:8000/health | python3 -m json.tool

# Test without auth (should fail)
echo -e "\n2. Testing without auth (should fail with 401)..."
curl -s -w "\nHTTP Status: %{http_code}\n" http://localhost:8000/objections/

# Test with auth
echo -e "\n3. Testing with auth (should succeed)..."
curl -s -H "Authorization: Bearer supersecret007" http://localhost:8000/objections/ | python3 -m json.tool

echo -e "\n==================================="
echo "Test complete!"
echo "==================================="
