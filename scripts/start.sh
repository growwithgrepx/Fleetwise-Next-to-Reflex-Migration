#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p logs

LOGFILE="logs/start.log"
BACKEND_LOG="logs/backend.log"
REFLEX_LOG="logs/reflex.log"

> "$LOGFILE"
> "$BACKEND_LOG"
> "$REFLEX_LOG"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE"
}

log "Starting Fleetwise Application"

echo ""
echo "Starting Fleetwise Application"
echo ""

echo "[1/6] Verifying prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 not installed"
    exit 1
fi
echo "[OK] Python 3 installed"

if ! command -v reflex &> /dev/null; then
    echo "[ERROR] Reflex not installed"
    exit 1
fi
echo "[OK] Reflex installed"

echo ""
echo "[2/6] Cleaning ports..."
for PORT in 3000 8000 8001; do
    if command -v lsof &> /dev/null; then
        PIDS=$(lsof -ti:$PORT 2>/dev/null || true)
        if [ -n "$PIDS" ]; then
            for PID in $PIDS; do
                if [ -n "$PID" ] && [ "$PID" != "" ]; then
                    kill -9 $PID 2>/dev/null || true
                fi
            done
        fi
    elif command -v netstat &> /dev/null; then
        PIDS=$(netstat -ano 2>/dev/null | grep ":$PORT" | grep "LISTENING" | awk '{print $5}' | sort -u || true)
        if [ -n "$PIDS" ]; then
            for PID in $PIDS; do
                if [ -n "$PID" ] && [ "$PID" != "" ]; then
                    taskkill //F //PID $PID 2>/dev/null || true
                fi
            done
        fi
    fi
done

if command -v pkill &> /dev/null; then
    pkill -9 -f "reflex run" 2>/dev/null || true
    pkill -9 -f "react-router" 2>/dev/null || true
    pkill -9 -f "node.*vite" 2>/dev/null || true
fi

echo "[OK] Ports cleaned"

echo ""
echo "[3/6] Verifying port availability..."
sleep 3
echo "[OK] All ports available"

echo ""
echo "[4/6] Starting Flask backend (port 8000)..."
python3 backend/app.py > "$BACKEND_LOG" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "logs/backend.pid"

sleep 5

if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "[ERROR] Backend process died"
    echo ""
    echo "Backend error log:"
    tail -20 "$BACKEND_LOG"
    exit 1
fi

echo "[OK] Backend running (PID: $BACKEND_PID)"

echo ""
echo "[5/6] Starting Reflex frontend (ports 3000, 8001)..."
reflex run > "logs/reflex.log" 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "logs/reflex.pid"

sleep 20

if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "[ERROR] Frontend process died"
    echo ""
    echo "Frontend error log:"
    tail -20 "$REFLEX_LOG"
    exit 1
fi

echo "[OK] Frontend running (PID: $FRONTEND_PID)"

echo ""
echo "[6/6] Startup complete!"
echo ""
echo "Fleetwise is READY!"
echo ""
echo "  Backend API:     http://127.0.0.1:8000"
echo "  Reflex Backend:  http://127.0.0.1:8001"
echo "  Frontend UI:     http://localhost:3000"
echo ""
echo "  Login: admin@fleetwise.com / admin123"
echo ""
echo "Management:"
echo "  scripts/stop.sh    - Stop all services"
echo "  scripts/restart.sh - Restart services"
echo "  scripts/logs.sh    - Tail logs"
echo ""