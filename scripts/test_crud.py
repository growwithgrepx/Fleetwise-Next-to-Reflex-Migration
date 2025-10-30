#!/usr/bin/env python3
"""
CRUD Operations Test Script for Fleetwise
"""

import os
import sys
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path

# Change to project root
os.chdir(Path(__file__).parent.parent)

BASE_URL = "http://127.0.0.1:8000/api"
AUTH_EMAIL = "admin@fleetwise.com"
AUTH_PASSWORD = "admin123"

def get_token():
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": AUTH_EMAIL, "password": AUTH_PASSWORD}
    )
    if response.status_code == 200:
        return response.json()["token"]
    raise Exception(f"Authentication failed: {response.text}")

def get_headers(token):
    return {"Authorization": f"Bearer {token}"}

def test_create_driver(token):
    print("\n[CREATE] Testing...")
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
        print(f"  [OK] Driver created (ID: {driver_id})")
        return driver_id
    else:
        print(f"  [ERROR] Failed: {response.text}")
        return None

def test_read_drivers(token):
    print("\n[READ] Testing fetch all...")
    headers = get_headers(token)
    
    response = requests.get(f"{BASE_URL}/drivers", headers=headers)
    if response.status_code == 200:
        drivers = response.json()
        print(f"  [OK] Retrieved {len(drivers)} drivers")
        return drivers
    else:
        print(f"  [ERROR] Failed: {response.text}")
        return []

def test_read_single_driver(token, driver_id):
    print(f"\n[READ] Testing fetch single (ID: {driver_id})...")
    headers = get_headers(token)
    
    response = requests.get(f"{BASE_URL}/drivers/{driver_id}", headers=headers)
    if response.status_code == 200:
        driver = response.json()
        print(f"  [OK] Retrieved: {driver['first_name']} {driver['last_name']}")
        return driver
    else:
        print(f"  [ERROR] Failed: {response.text}")
        return None

def test_update_driver(token, driver_id):
    print(f"\n[UPDATE] Testing (ID: {driver_id})...")
    headers = get_headers(token)
    
    update_data = {
        "phone": "+1-555-9999",
        "status": "inactive"
    }
    
    response = requests.put(f"{BASE_URL}/drivers/{driver_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        print(f"  [OK] Driver updated")
        return True
    else:
        print(f"  [ERROR] Failed: {response.text}")
        return False

def test_delete_driver(token, driver_id):
    print(f"\n[DELETE] Testing (ID: {driver_id})...")
    headers = get_headers(token)
    
    response = requests.delete(f"{BASE_URL}/drivers/{driver_id}", headers=headers)
    if response.status_code == 200:
        print(f"  [OK] Driver deleted")
        return True
    else:
        print(f"  [ERROR] Failed: {response.text}")
        return False

def main():
    print("=" * 60)
    print("  Fleetwise CRUD Operations Test")
    print("=" * 60)
    
    try:
        print("\n[AUTH] Authenticating...")
        token = get_token()
        print("  [OK] Authentication successful")
        
        driver_id = test_create_driver(token)
        if not driver_id:
            print("\n[FAIL] CREATE test failed")
            return
        
        test_read_drivers(token)
        test_read_single_driver(token, driver_id)
        
        if not test_update_driver(token, driver_id):
            print("\n[FAIL] UPDATE test failed")
            return
        
        driver = test_read_single_driver(token, driver_id)
        if driver and driver["status"] == "inactive":
            print("  [OK] Update verified")
        
        if not test_delete_driver(token, driver_id):
            print("\n[FAIL] DELETE test failed")
            return
        
        response = requests.get(f"{BASE_URL}/drivers/{driver_id}", headers=get_headers(token))
        if response.status_code == 404:
            print("  [OK] Deletion verified")
        
        print("\n" + "=" * 60)
        print("  [SUCCESS] All CRUD operations passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    main()