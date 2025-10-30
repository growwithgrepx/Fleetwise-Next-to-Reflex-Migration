#!/usr/bin/env python3
"""
WebSocket Connection Test for Fleetwise
Tests if Reflex backend WebSocket is accessible
"""

import socket
import sys

def test_port(host, port, service_name):
    """Test if a port is open and listening"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((host, port))
    sock.close()
    
    if result == 0:
        print(f"✓ {service_name} (port {port}): LISTENING")
        return True
    else:
        print(f"✗ {service_name} (port {port}): NOT LISTENING")
        return False

def main():
    print("=" * 60)
    print("  Fleetwise WebSocket Connection Test")
    print("=" * 60)
    print()
    
    print("Testing service ports...")
    print()
    
    flask_ok = test_port("127.0.0.1", 8000, "Flask API (REST)")
    reflex_ok = test_port("127.0.0.1", 8001, "Reflex Backend (WebSocket)")
    frontend_ok = test_port("127.0.0.1", 3000, "Frontend (React)")
    
    print()
    print("=" * 60)
    
    if flask_ok and reflex_ok and frontend_ok:
        print("✓ All services running correctly!")
        print()
        print("WebSocket Configuration:")
        print("  ✓ WebSocket: ws://127.0.0.1:8001/_event")
        print("  ✓ REST API:  http://127.0.0.1:8000/api")
        print("  ✓ Frontend:  http://localhost:3000")
        print()
        print("Test: Open http://localhost:3000 in browser")
        print("Expected: No WebSocket errors in console")
        sys.exit(0)
    else:
        print("✗ Some services are not running")
        print()
        if not flask_ok:
            print("  Start Flask: python backend/app.py")
        if not reflex_ok or not frontend_ok:
            print("  Start Reflex: reflex run")
        print()
        print("Or run: ./start.sh (Unix) or start.bat (Windows)")
        sys.exit(1)

if __name__ == "__main__":
    main()