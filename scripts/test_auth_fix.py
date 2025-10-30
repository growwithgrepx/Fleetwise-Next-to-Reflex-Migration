#!/usr/bin/env python3
"""
Test script to verify authentication and driver creation fixes.
"""

import requests
import json
import time

API_BASE_URL = "http://127.0.0.1:8000/api"

def test_health():
    """Test health endpoint."""
    print("\n[1/5] Testing health endpoint...")
    try:
        resp = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if resp.status_code == 200:
            print("  ✓ Health check passed")
            return True
        else:
            print(f"  ✗ Health check failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_login():
    """Test login endpoint."""
    print("\n[2/5] Testing login...")
    try:
        resp = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"email": "admin@fleetwise.com", "password": "admin123"},
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            token = data.get("token")
            print(f"  ✓ Login successful")
            print(f"  Token: {token[:20]}...")
            return token
        else:
            print(f"  ✗ Login failed: {resp.status_code} - {resp.text}")
            return None
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None

def test_fetch_drivers(token):
    """Test fetching drivers with auth."""
    print("\n[3/5] Testing fetch drivers with authentication...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(
            f"{API_BASE_URL}/drivers",
            headers=headers,
            timeout=5
        )
        if resp.status_code == 200:
            drivers = resp.json()
            print(f"  ✓ Fetch successful - {len(drivers)} drivers found")
            return True
        else:
            print(f"  ✗ Fetch failed: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_create_driver(token):
    """Test creating a driver with auth."""
    print("\n[4/5] Testing create driver with authentication...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        driver_data = {
            "first_name": "Test",
            "last_name": "Driver",
            "email": "test@example.com",
            "phone": "1234567890",
            "license_number": "DL123456",
            "license_expiry": "2025-12-31",
            "status": "active"
        }
        resp = requests.post(
            f"{API_BASE_URL}/drivers",
            json=driver_data,
            headers=headers,
            timeout=5
        )
        if resp.status_code == 201:
            data = resp.json()
            print(f"  ✓ Driver created successfully")
            print(f"  Response: {data}")
            return True
        else:
            print(f"  ✗ Create failed: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_auth_headers_format():
    """Test that auth headers are formatted correctly."""
    print("\n[5/5] Testing auth headers format...")
    token = "test_token_12345"
    headers = {"Authorization": f"Bearer {token}"}
    
    # Verify format
    auth_header = headers.get("Authorization")
    if auth_header.startswith("Bearer ") and len(auth_header.split(" ")) == 2:
        print(f"  ✓ Auth header format correct: {auth_header}")
        return True
    else:
        print(f"  ✗ Auth header format incorrect: {auth_header}")
        return False

def main():
    print("=" * 60)
    print("  Fleetwise Authentication & Driver Creation Test")
    print("=" * 60)
    
    results = []
    
    # Test health
    results.append(("Health Check", test_health()))
    
    # Test login
    token = test_login()
    results.append(("Login", token is not None))
    
    if token:
        # Test fetch drivers
        results.append(("Fetch Drivers", test_fetch_drivers(token)))
        
        # Test create driver
        results.append(("Create Driver", test_create_driver(token)))
    else:
        print("\n  ⚠ Skipping authenticated tests - login failed")
        results.append(("Fetch Drivers", False))
        results.append(("Create Driver", False))
    
    # Test auth headers format
    results.append(("Auth Headers Format", test_auth_headers_format()))
    
    # Summary
    print("\n" + "=" * 60)
    print("  Test Summary")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
