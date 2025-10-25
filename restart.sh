#!/bin/bash
###############################################################################
# Fleetwise - Production-Grade Restart Script (Unix/Linux/macOS)
###############################################################################
# Description: Stops and restarts all Fleetwise services
# Author: DevOps Team
# Last Modified: 2025-10-25
###############################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create logs directory
mkdir -p logs

# Set log file with timestamp
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOGFILE="logs/restart_${TIMESTAMP}.log"

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

# Stop processes from PID files
echo -e "${BLUE}[1/3]${NC} Stopping Reflex frontend..."
if [ -f "logs/reflex.pid" ]; then
    REFLEX_PID=$(cat logs/reflex.pid)
    if kill -0 $REFLEX_PID 2>/dev/null; then
        kill -TERM $REFLEX_PID 2>/dev/null || true
        sleep 2
        kill -9 $REFLEX_PID 2>/dev/null || true
    fi
    rm -f logs/reflex.pid
fi
if command -v pkill &> /dev/null; then
    pkill -f "reflex run" 2>/dev/null || true
    pkill -f "react-router" 2>/dev/null || true
    pkill -f "node.*vite" 2>/dev/null || true
fi
echo -e "${GREEN}[OK]${NC} Reflex stopped"

echo ""
echo -e "${BLUE}[2/3]${NC} Stopping Flask backend..."
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill -TERM $BACKEND_PID 2>/dev/null || true
        sleep 2
        kill -9 $BACKEND_PID 2>/dev/null || true
    fi
    rm -f logs/backend.pid
fi
echo -e "${GREEN}[OK]${NC} Backend stopped"

echo ""
echo -e "${BLUE}[3/3]${NC} Cleaning ports..."
for PORT in 3000 8000 8001; do
    if command -v lsof &> /dev/null; then
        PIDS=$(lsof -ti:$PORT 2>/dev/null || true)
    elif command -v fuser &> /dev/null; then
        PIDS=$(fuser $PORT/tcp 2>/dev/null | tr -s ' ' '\n' || true)
    else
        continue
    fi
    
    if [ -n "$PIDS" ]; then
        for PID in $PIDS; do
            if [ -n "$PID" ] && [ "$PID" != "" ]; then
                kill -9 $PID 2>/dev/null || true
            fi
        done
    fi
done

sleep 3

# Verify ports are free
PORTS_READY=true
for PORT in 3000 8000 8001; do
    if command -v lsof &> /dev/null; then
        if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo -e "${RED}[ERROR]${NC} Port $PORT still in use!"
            log "ERROR: Port $PORT not freed"
            PORTS_READY=false
        fi
    fi
done

if [ "$PORTS_READY" = false ]; then
    echo -e "${RED}[ERROR]${NC} Cannot restart - ports still occupied"
    log "Restart failed - ports blocked"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} All ports available"
log "Phase 1 complete - services stopped"

# Phase 2: Startup
echo ""
echo "========================================"
echo "  PHASE 2: Starting Services"
echo "========================================"
echo ""
log "Phase 2: Starting services"

echo -e "${BLUE}[1/2]${NC} Starting Flask backend..."
log "Starting Flask backend"
python3 backend/app.py > "logs/backend_${TIMESTAMP}.log" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "logs/backend.pid"

echo "  Waiting for backend initialization..."
sleep 5

if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}[ERROR]${NC} Backend failed to start"
    log "ERROR: Backend startup failed"
    exit 1
fi

if command -v lsof &> /dev/null; then
    if ! lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}[ERROR]${NC} Backend not listening on port 8000"
        log "ERROR: Backend not responding"
        exit 1
    fi
fi

echo -e "${GREEN}[OK]${NC} Backend running"

echo ""
echo -e "${BLUE}[2/2]${NC} Starting Reflex frontend..."
log "Starting Reflex frontend"
reflex run > "logs/reflex_${TIMESTAMP}.log" 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "logs/reflex.pid"

echo "  Waiting for frontend compilation..."
sleep 15

if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}[ERROR]${NC} Frontend failed to start"
    log "ERROR: Frontend startup failed"
    exit 1
fi

if command -v lsof &> /dev/null; then
    if ! lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}[ERROR]${NC} Frontend not listening on port 3000"
        log "ERROR: Frontend not responding"
        exit 1
    fi
fi

echo -e "${GREEN}[OK]${NC} Frontend running"

log "Phase 2 complete - services started"

# Final Status
echo ""
echo "========================================"
echo -e "  ${GREEN}Restart COMPLETE!${NC}"
echo "========================================"
echo ""
echo "  Services:"
echo -e "    ${GREEN}[*]${NC} Backend API:     http://127.0.0.1:8000"
echo -e "    ${GREEN}[*]${NC} Reflex Backend:  http://127.0.0.1:8001"
echo -e "    ${GREEN}[*]${NC} Frontend UI:     http://localhost:3000"
echo ""
echo "  Logs:"
echo "    $LOGFILE"
echo "    logs/backend_${TIMESTAMP}.log"
echo "    logs/reflex_${TIMESTAMP}.log"
echo ""

log "========================================"
log "Restart completed successfully"
log "========================================"

echo -e "${BLUE}[INFO]${NC} Services restarted successfully"
echo ""
