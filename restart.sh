#!/bin/bash
###############################################################################
# Fleetwise - Restart Script with Port Cleanup (Unix/Linux/macOS)
###############################################################################

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Create logs directory
mkdir -p logs

# Use fixed log name (overwrite previous run)
LOGFILE="logs/restart.log"
> "$LOGFILE"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE"
}

log "========================================"
log "Restarting Fleetwise Application"
log "========================================"

echo ""
echo "========================================"
echo "  Fleetwise Application Restart"
echo "========================================"
echo ""
echo -e "${BLUE}[INFO]${NC} Initiating restart sequence..."
echo -e "${BLUE}[INFO]${NC} Log file: $LOGFILE"
echo ""

# Phase 1: Graceful Shutdown
echo "========================================"
echo "  PHASE 1: Stopping Services"
echo "========================================"
echo ""
log "Phase 1: Stopping services"

# Call stop.sh
if [ -f "./stop.sh" ]; then
    ./stop.sh
else
    echo -e "${RED}[ERROR]${NC} stop.sh not found"
    exit 1
fi

echo ""
log "Phase 1 complete - services stopped"

# Wait and verify ports are free
echo "Waiting 3 seconds before restart..."
sleep 3

# Verify ports are free with retry
MAX_RETRIES=3
RETRY_COUNT=0
PORTS_READY=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ] && [ "$PORTS_READY" = false ]; do
    PORTS_READY=true
    for PORT in 3000 8000 8001; do
        if command -v lsof &> /dev/null; then
            if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
                echo -e "${YELLOW}[WARNING]${NC} Port $PORT still in use (attempt $((RETRY_COUNT+1))/$MAX_RETRIES)"
                log "WARNING: Port $PORT still in use (retry $((RETRY_COUNT+1)))"
                PORTS_READY=false
                
                # Force kill process on this port
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
    echo -e "${RED}[ERROR]${NC} Cannot restart - ports still occupied after $MAX_RETRIES attempts"
    log "Restart failed - ports blocked"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} All ports available"

# Phase 2: Startup
echo ""
echo "========================================"
echo "  PHASE 2: Starting Services"
echo "========================================"
echo ""
log "Phase 2: Starting services"

# Call start.sh
if [ -f "./start.sh" ]; then
    ./start.sh
else
    echo -e "${RED}[ERROR]${NC} start.sh not found"
    exit 1
fi

log "Phase 2 complete - services started"

# Final Status
echo ""
echo "========================================"
echo -e "  ${GREEN}Restart COMPLETE!${NC}"
echo "========================================"
echo ""

log "========================================"
log "Restart completed successfully"
log "========================================"

echo -e "${BLUE}[INFO]${NC} Services restarted successfully"
echo ""