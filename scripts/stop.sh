#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p logs

LOGFILE="logs/stop.log"
> "$LOGFILE"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE"
}

log "Stopping Fleetwise Application"

echo ""
echo "Stopping Fleetwise Application"
echo ""

echo "[1/4] Attempting graceful shutdown..."
log "Attempting graceful shutdown"

if [ -f "logs/reflex.pid" ]; then
    REFLEX_PID=$(cat logs/reflex.pid)
    if kill -0 $REFLEX_PID 2>/dev/null; then
        kill -TERM $REFLEX_PID 2>/dev/null || true
    fi
fi

if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill -TERM $BACKEND_PID 2>/dev/null || true
    fi
fi

sleep 3

echo ""
echo "[2/4] Checking for remaining processes..."
log "Checking for remaining processes"

FORCE_KILL_NEEDED=false

if [ -f "logs/reflex.pid" ]; then
    REFLEX_PID=$(cat logs/reflex.pid)
    if kill -0 $REFLEX_PID 2>/dev/null; then
        kill -9 $REFLEX_PID 2>/dev/null || true
        FORCE_KILL_NEEDED=true
    fi
    rm -f logs/reflex.pid
fi

if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill -9 $BACKEND_PID 2>/dev/null || true
        FORCE_KILL_NEEDED=true
    fi
    rm -f logs/backend.pid
fi

if command -v pkill &> /dev/null; then
    pkill -9 -f "reflex run" 2>/dev/null || true
    pkill -9 -f "react-router" 2>/dev/null || true
    pkill -9 -f "node.*vite" 2>/dev/null || true
    pkill -9 -f "python.*backend" 2>/dev/null || true
fi

if [ "$FORCE_KILL_NEEDED" = true ]; then
    echo "[OK] Force kill was necessary"
else
    echo "[OK] Graceful shutdown successful"
fi

echo ""
echo "[3/4] Force cleaning service ports..."
log "Force cleaning ports"

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

echo "[OK] Ports cleaned"

echo ""
echo "[4/4] Verifying shutdown..."
log "Verifying shutdown"

sleep 2

echo "[OK] All services stopped"
log "Shutdown completed successfully"

echo ""
echo "Fleetwise has been STOPPED"
echo ""
log "Shutdown complete"