#!/usr/bin/env python3
"""
CRUD Operations Test Script for Fleetwise
Tests all Create, Read, Update, Delete operations
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000/api"
AUTH_EMAIL = "admin@fleetwise.com"
AUTH_PASSWORD = "admin123"

def get_token():
    """Get authentication token"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": AUTH_EMAIL, "password": AUTH_PASSWORD}
    )
    if response.status_code == 200:
        return response.json()["token"]
    raise Exception(f"Authentication failed: {response.text}")

def get_headers(token):
    """Get request headers with auth token"""
    return {"Authorization": f"Bearer {token}"}

def test_create_driver(token):
    """Test CREATE operation"""
    print("\n✓ Testing CREATE operation...")
    headers = get_headers(token)
    
    driver_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": f"john.doe.{datetime.now().timestamp()}@fleetwise.com",
        "phone": "+1-555-0123",
        "license_number": f"DL{datetime.now().timestamp()}",
        "license_expiry": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
        "status": "active"
    }
    
    response = requests.post(f"{BASE_URL}/drivers", json=driver_data, headers=headers)
    if response.status_code == 201:
        driver_id = response.json()["id"]
        print(f"  ✓ Driver created successfully (ID: {driver_id})")
        return driver_id
    else:
        print(f"  ✗ Failed to create driver: {response.text}")
        return None

def test_read_drivers(token):
    """Test READ operation"""
    print("\n✓ Testing READ operation...")
    headers = get_headers(token)
    
    response = requests.get(f"{BASE_URL}/drivers", headers=headers)
    if response.status_code == 200:
        drivers = response.json()
        print(f"  ✓ Retrieved {len(drivers)} drivers")
        return drivers
    else:
        print(f"  ✗ Failed to read drivers: {response.text}")
        return []

def test_read_single_driver(token, driver_id):
    """Test READ single driver"""
    print(f"\n✓ Testing READ single driver (ID: {driver_id})...")
    headers = get_headers(token)
    
    response = requests.get(f"{BASE_URL}/drivers/{driver_id}", headers=headers)
    if response.status_code == 200:
        driver = response.json()
        print(f"  ✓ Retrieved driver: {driver['first_name']} {driver['last_name']}")
        return driver
    else:
        print(f"  ✗ Failed to read driver: {response.text}")
        return None

def test_update_driver(token, driver_id):
    """Test UPDATE operation"""
    print(f"\n✓ Testing UPDATE operation (ID: {driver_id})...")
    headers = get_headers(token)
    
    update_data = {
        "phone": "+1-555-9999",
        "status": "inactive"
    }
    
    response = requests.put(f"{BASE_URL}/drivers/{driver_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        print(f"  ✓ Driver updated successfully")
        return True
    else:
        print(f"  ✗ Failed to update driver: {response.text}")
        return False

def test_delete_driver(token, driver_id):
    """Test DELETE operation"""
    print(f"\n✓ Testing DELETE operation (ID: {driver_id})...")
    headers = get_headers(token)
    
    response = requests.delete(f"{BASE_URL}/drivers/{driver_id}", headers=headers)
    if response.status_code == 200:
        print(f"  ✓ Driver deleted successfully")
        return True
    else:
        print(f"  ✗ Failed to delete driver: {response.text}")
        return False

def main():
    """Run all CRUD tests"""
    print("=" * 60)
    print("  Fleetwise CRUD Operations Test")
    print("=" * 60)
    
    try:
        # Get authentication token
        print("\n→ Authenticating...")
        token = get_token()
        print("  ✓ Authentication successful")
        
        # Test CREATE
        driver_id = test_create_driver(token)
        if not driver_id:
            print("\n✗ CREATE test failed, stopping tests")
            return
        
        # Test READ all
        test_read_drivers(token)
        
        # Test READ single
        test_read_single_driver(token, driver_id)
        
        # Test UPDATE
        if not test_update_driver(token, driver_id):
            print("\n✗ UPDATE test failed")
            return
        
        # Verify update
        driver = test_read_single_driver(token, driver_id)
        if driver and driver["status"] == "inactive":
            print("  ✓ Update verified: status changed to inactive")
        
        # Test DELETE
        if not test_delete_driver(token, driver_id):
            print("\n✗ DELETE test failed")
            return
        
        # Verify deletion
        response = requests.get(f"{BASE_URL}/drivers/{driver_id}", headers=get_headers(token))
        if response.status_code == 404:
            print("  ✓ Deletion verified: driver not found")
        
        print("\n" + "=" * 60)
        print("  ✓ All CRUD operations passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    main()
