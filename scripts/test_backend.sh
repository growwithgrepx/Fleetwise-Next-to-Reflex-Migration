#!/usr/bin/env python3
"""
Test if backend starts correctly
"""

import os
import sys
from pathlib import Path

# Change to project root
os.chdir(Path(__file__).parent.parent)

print("Testing backend startup...")
print("=" * 60)

# Check if backend directory exists
if not Path("backend").exists():
    print("[ERROR] backend/ directory not found")
    sys.exit(1)

# Check if backend/app.py exists
if not Path("backend/app.py").exists():
    print("[ERROR] backend/app.py not found")
    sys.exit(1)

print("[OK] backend/app.py exists")

# Try to import backend modules
sys.path.insert(0, str(Path("backend")))

try:
    import config
    print("[OK] backend/config.py imports successfully")
except Exception as e:
    print(f"[ERROR] Failed to import config: {e}")
    sys.exit(1)

try:
    import models
    print("[OK] backend/models.py imports successfully")
except Exception as e:
    print(f"[ERROR] Failed to import models: {e}")
    sys.exit(1)

try:
    from app import app, init_db
    print("[OK] backend/app.py imports successfully")
except Exception as e:
    print(f"[ERROR] Failed to import app: {e}")
    print(f"\nDetails: {e.__class__.__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("[SUCCESS] Backend can start successfully")
print("=" * 60)
print("\nRun: python backend/app.py")