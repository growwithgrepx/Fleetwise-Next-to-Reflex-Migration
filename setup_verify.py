"""
Fleetwise Setup Verification Script
Run this to check if everything is configured correctly
"""

import os
import sys
import subprocess
import requests
from pathlib import Path


def print_header(text):
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def check_mark(passed):
    return "✓" if passed else "✗"


def test_file_exists(filepath):
    """Check if a file exists"""
    path = Path(filepath)
    exists = path.exists()
    size = path.stat().st_size if exists else 0
    print(
        f"  {check_mark(exists)} {filepath} {('(' + str(size) + ' bytes)' if exists else '(missing)')}"
    )
    return exists


def test_backend_running():
    """Check if Flask backend is running"""
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=2)
        if response.status_code == 200:
            print(f"  ✓ Backend is running on http://127.0.0.1:8000")
            return True
        else:
            print(f"  ✗ Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"  ✗ Backend is NOT running (connection refused)")
        print(f"     Start it with: python -m backend.app")
        return False
    except Exception as e:
        print(f"  ✗ Error checking backend: {e}")
        return False


def test_backend_auth():
    """Test backend authentication"""
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/auth/login",
            json={"email": "admin@fleetwise.com", "password": "admin123"},
            timeout=2,
        )
        if response.status_code == 200:
            data = response.json()
            if "token" in data:
                print(f"  ✓ Authentication working (token received)")
                return True
            else:
                print(f"  ✗ Authentication response missing token")
                return False
        else:
            print(f"  ✗ Authentication failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error testing authentication: {e}")
        return False


def test_database():
    """Check if database exists and has tables"""
    db_path = Path("backend/fleetwise.db")
    if not db_path.exists():
        print(f"  ✗ Database not found at {db_path}")
        print(f"     Create it by running: python -m backend.app")
        return False
    try:
        import sqlite3

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        table_names = [t[0] for t in tables]
        if "user" in table_names and "driver" in table_names:
            print(f"  ✓ Database exists with correct tables")
            cursor.execute("SELECT email FROM user WHERE email='admin@fleetwise.com'")
            admin = cursor.fetchone()
            if admin:
                print(f"  ✓ Admin user exists")
            else:
                print(f"  ✗ Admin user not found")
            conn.close()
            return True
        else:
            print(f"  ✗ Database missing required tables")
            print(f"     Found tables: {table_names}")
            conn.close()
            return False
    except Exception as e:
        print(f"  ✗ Error checking database: {e}")
        return False


def test_python_version():
    """Check Python version"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    if version.major == 3 and version.minor >= 10:
        print(f"  ✓ Python {version_str}")
        if version.minor == 10:
            print(f"    ⚠ Python 3.10 is deprecated, consider upgrading to 3.11+")
        return True
    else:
        print(f"  ✗ Python {version_str} (need 3.10+)")
        return False


def test_dependencies():
    """Check if required packages are installed"""
    required = {
        "flask": "flask",
        "reflex": "reflex",
        "requests": "requests",
        "flask_cors": "flask_cors",
        "flask_sqlalchemy": "flask_sqlalchemy",
        "pyjwt": "jwt",
    }
    all_installed = True
    for package_name, import_name in required.items():
        try:
            __import__(import_name)
            print(f"  ✓ {package_name}")
        except ImportError:
            print(f"  ✗ {package_name} (not installed)")
            all_installed = False
    return all_installed


def main():
    print_header("Fleetwise Setup Verification")
    results = {}
    print_header("1. Python Version")
    results["python"] = test_python_version()
    print_header("2. Dependencies")
    results["dependencies"] = test_dependencies()
    print_header("3. File Structure")
    required_files = [
        "requirements.txt",
        "rxconfig.py",
        "app/app.py",
        "app/states/base_state.py",
        "app/states/auth_state.py",
        "app/states/driver_state.py",
        "app/pages/login.py",
        "app/pages/drivers.py",
        "app/components/sidebar.py",
        "app/components/ui.py",
        "backend/app.py",
        "backend/models.py",
        "backend/config.py",
    ]
    files_ok = all((test_file_exists(f) for f in required_files))
    results["files"] = files_ok
    print_header("4. Database")
    results["database"] = test_database()
    print_header("5. Backend Server")
    results["backend"] = test_backend_running()
    if results["backend"]:
        print_header("6. Backend Authentication")
        results["auth"] = test_backend_auth()
    else:
        results["auth"] = False
    print_header("Summary")
    total_tests = len(results)
    passed_tests = sum(results.values())
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"  {symbol} {test_name.upper()}: {status}")
    print(f"\n  {passed_tests}/{total_tests} checks passed")
    if passed_tests == total_tests:
        print("""
  🎉 All checks passed! Your setup looks good.""")
        print("""
  Next steps:""")
        print("  1. Ensure backend is running: python -m backend.app")
        print("  2. Start frontend: reflex run")
        print("  3. Open browser: http://localhost:3000")
        print("  4. Login with: admin@fleetwise.com / admin123")
    else:
        print("""
  ⚠ Some checks failed. Please review the errors above.""")
        if not results.get("backend"):
            print("""
  → Start the backend first:""")
            print("     python -m backend.app")
        if not results.get("database"):
            print("""
  → Initialize the database:""")
            print("     python -m backend.app")
            print("     (This will create the database and admin user)")
        if not results.get("dependencies"):
            print("""
  → Install missing dependencies:""")
            print("     pip install -r requirements.txt")


if __name__ == "__main__":
    main()