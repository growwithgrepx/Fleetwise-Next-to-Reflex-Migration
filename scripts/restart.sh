#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p logs

LOGFILE="logs/restart.log"
> "$LOGFILE"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE"
}

log "Restarting Fleetwise Application"

echo ""
echo "Restarting Fleetwise Application"
echo ""

echo "[PHASE 1: Stopping Services]"
echo ""
log "Phase 1: Stopping services"

if [ -f "scripts/stop.sh" ]; then
    bash scripts/stop.sh
else
    echo "[ERROR] scripts/stop.sh not found"
    exit 1
fi

echo ""
log "Phase 1 complete"

echo "Waiting 3 seconds before restart..."
sleep 3

MAX_RETRIES=3
RETRY_COUNT=0
PORTS_READY=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ] && [ "$PORTS_READY" = false ]; do
    PORTS_READY=true
    for PORT in 3000 8000 8001; do
        if command -v lsof &> /dev/null; then
            if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
                PORTS_READY=false
                PIDS=$(lsof -ti:$PORT 2>/dev/null || true)
                if [ -n "$PIDS" ]; then
                    for PID in $PIDS; do
                        kill -9 $PID 2>/dev/null || true
                    done
                fi
            fi
        fi
    done
    
    if [ "$PORTS_READY" = false ]; then
        RETRY_COUNT=$((RETRY_COUNT+1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            sleep 2
        fi
    fi
done

if [ "$PORTS_READY" = false ]; then
    echo "[ERROR] Cannot restart - ports still occupied"
    log "Restart failed - ports blocked"
    exit 1
fi

echo "[OK] All ports available"

echo ""
echo "[PHASE 2: Starting Services]"
echo ""
log "Phase 2: Starting services"

if [ -f "scripts/start.sh" ]; then
    bash scripts/start.sh
else
    echo "[ERROR] scripts/start.sh not found"
    exit 1
fi

log "Phase 2 complete"

echo ""
echo "Restart COMPLETE!"
echo ""

log "Restart completed successfully"