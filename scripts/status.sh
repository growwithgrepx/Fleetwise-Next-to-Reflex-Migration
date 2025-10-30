#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo ""
echo "Fleetwise Service Status"
echo "========================"
echo ""

check_port() {
    local PORT=$1
    if command -v lsof &> /dev/null; then
        lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1
    elif command -v netstat &> /dev/null; then
        netstat -ano 2>/dev/null | grep ":$PORT" | grep "LISTENING" >/dev/null 2>&1
    else
        return 1
    fi
}

get_pid() {
    local PORT=$1
    if command -v lsof &> /dev/null; then
        lsof -Pi :$PORT -sTCP:LISTEN -t 2>/dev/null || true
    elif command -v netstat &> /dev/null; then
        netstat -ano 2>/dev/null | grep ":$PORT" | grep "LISTENING" | awk '{print $5}' | head -1 || true
    fi
}

echo "[Backend API - Port 8000]"
if check_port 8000; then
    PID=$(get_pid 8000)
    echo "  [*] Running (PID: $PID)"
    if [ -f "logs/backend.pid" ]; then
        SAVED_PID=$(cat logs/backend.pid)
        if [ "$PID" = "$SAVED_PID" ]; then
            echo "  [*] PID matches saved PID"
        else
            echo "  [!] PID mismatch"
        fi
    fi
else
    echo "  [X] Not running"
fi

echo ""

echo "[Reflex Backend - Port 8001]"
if check_port 8001; then
    PID=$(get_pid 8001)
    echo "  [*] Running (PID: $PID)"
else
    echo "  [X] Not running"
fi

echo ""

echo "[Frontend UI - Port 3000]"
if check_port 3000; then
    PID=$(get_pid 3000)
    echo "  [*] Running (PID: $PID)"
    if [ -f "logs/reflex.pid" ]; then
        SAVED_PID=$(cat logs/reflex.pid)
        if [ "$PID" = "$SAVED_PID" ]; then
            echo "  [*] PID matches saved PID"
        else
            echo "  [!] PID mismatch"
        fi
    fi
else
    echo "  [X] Not running"
fi

echo ""
echo "========================"
BACKEND_OK=false
FRONTEND_OK=false

if check_port 8000; then
    BACKEND_OK=true
fi
if check_port 3000; then
    FRONTEND_OK=true
fi

if [ "$BACKEND_OK" = true ] && [ "$FRONTEND_OK" = true ]; then
    echo "[*] All services running"
    echo ""
    echo "Access:"
    echo "  Backend:  http://127.0.0.1:8000"
    echo "  Frontend: http://localhost:3000"
elif [ "$BACKEND_OK" = true ]; then
    echo "[!] Backend running, but frontend is down"
elif [ "$FRONTEND_OK" = true ]; then
    echo "[!] Frontend running, but backend is down"
else
    echo "[X] No services running"
    echo "  Start: scripts/start.sh"
fi

echo "========================"
echo ""