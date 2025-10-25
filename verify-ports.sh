#!/bin/bash

echo "Verifying Fleetwise Ports Configuration"
echo "========================================="
echo ""

echo "Expected Configuration:"
echo "  Port 3000: Frontend (React/Vite)"
echo "  Port 8001: Reflex Backend (WebSocket)"
echo "  Port 8000: Flask API (REST)"
echo ""

if command -v lsof &> /dev/null; then
    echo "Port 3000 (Frontend):"
    lsof -Pi :3000 -sTCP:LISTEN || echo "  Not listening"
    echo ""
    
    echo "Port 8001 (Reflex Backend - WebSocket):"
    lsof -Pi :8001 -sTCP:LISTEN || echo "  Not listening"
    echo ""
    
    echo "Port 8000 (Flask API - REST):"
    lsof -Pi :8000 -sTCP:LISTEN || echo "  Not listening"
    echo ""
else
    netstat -an | grep LISTEN | grep -E ":(3000|8000|8001)"
fi

echo ""
echo "WebSocket Test:"
echo "  Expected: ws://127.0.0.1:8001/_event"
echo "  (NOT ws://127.0.0.1:8000/_event)"