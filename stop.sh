#!/bin/bash
###############################################################################
# Fleetwise - Production-Grade Shutdown Script (Unix/Linux/macOS)
###############################################################################
# Description: Gracefully terminates all Fleetwise services
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
LOGFILE="logs/stop_${TIMESTAMP}.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE"
}

log "========================================"
log "Stopping Fleetwise Application"
log "========================================"

echo ""
echo "========================================"
echo "  Fleetwise Application Shutdown"
echo "========================================"
echo ""
echo -e "${BLUE}[INFO]${NC} Initiating graceful shutdown..."
echo -e "${BLUE}[INFO]${NC} Log file: $LOGFILE"
echo ""

# Step 1: Stop processes from PID files
echo -e "${BLUE}[1/4]${NC} Stopping services from PID files..."
log "Stopping services from PID files"

if [ -f "logs/reflex.pid" ]; then
    REFLEX_PID=$(cat logs/reflex.pid)
    if kill -0 $REFLEX_PID 2>/dev/null; then
        echo "  Stopping Reflex (PID: $REFLEX_PID)..."
        log "Killing Reflex PID $REFLEX_PID"
        kill -TERM $REFLEX_PID 2>/dev/null || true
        sleep 2
        # Force kill if still running
        if kill -0 $REFLEX_PID 2>/dev/null; then
            kill -9 $REFLEX_PID 2>/dev/null || true
        fi
    fi
    rm -f logs/reflex.pid
fi

if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo "  Stopping Backend (PID: $BACKEND_PID)..."
        log "Killing Backend PID $BACKEND_PID"
        kill -TERM $BACKEND_PID 2>/dev/null || true
        sleep 2
        # Force kill if still running
        if kill -0 $BACKEND_PID 2>/dev/null; then
            kill -9 $BACKEND_PID 2>/dev/null || true
        fi
    fi
    rm -f logs/backend.pid
fi

echo -e "${GREEN}[OK]${NC} PID file services stopped"

# Step 2: Terminate any remaining Reflex/Node processes
echo ""
echo -e "${BLUE}[2/4]${NC} Stopping remaining Reflex/Node processes..."
log "Terminating Reflex/Node processes"

if command -v pkill &> /dev/null; then
    pkill -f "reflex run" 2>/dev/null || true
    pkill -f "react-router" 2>/dev/null || true
    pkill -f "node.*vite" 2>/dev/null || true
    echo -e "${GREEN}[OK]${NC} Reflex processes terminated"
else
    echo -e "${YELLOW}[WARNING]${NC} pkill not available, skipping"
fi

# Step 3: Clean all service ports
echo ""
echo -e "${BLUE}[3/4]${NC} Cleaning service ports (3000, 8000, 8001)..."
log "Cleaning ports"

for PORT in 3000 8000 8001; do
    echo "  Checking port $PORT..."
    if command -v lsof &> /dev/null; then
        PIDS=$(lsof -ti:$PORT 2>/dev/null || true)
    elif command -v fuser &> /dev/null; then
        PIDS=$(fuser $PORT/tcp 2>/dev/null | tr -s ' ' '\n' || true)
    else
        echo -e "${YELLOW}[WARNING]${NC} Cannot check port $PORT (lsof/fuser not available)"
        continue
    fi
    
    if [ -n "$PIDS" ]; then
        for PID in $PIDS; do
            if [ -n "$PID" ] && [ "$PID" != "" ]; then
                echo "    Force killing process $PID on port $PORT"
                log "Force killing PID $PID on port $PORT"
                kill -9 $PID 2>/dev/null || true
            fi
        done
    fi
done

echo -e "${GREEN}[OK]${NC} Ports cleaned"

# Step 4: Verify all processes stopped
echo ""
echo -e "${BLUE}[4/4]${NC} Verifying shutdown..."
log "Verifying shutdown"

sleep 2

PORTS_CLEAR=true
for PORT in 3000 8000 8001; do
    if command -v lsof &> /dev/null; then
        if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo -e "${YELLOW}[WARNING]${NC} Port $PORT still in use"
            log "WARNING: Port $PORT still listening"
            PORTS_CLEAR=false
        fi
    fi
done

if [ "$PORTS_CLEAR" = true ]; then
    echo -e "${GREEN}[OK]${NC} All services stopped, ports released"
    log "Shutdown completed successfully"
else
    echo -e "${YELLOW}[WARNING]${NC} Some ports may still be in use"
    log "Shutdown completed with warnings"
fi

echo ""
echo "========================================"
echo -e "  ${GREEN}Fleetwise has been STOPPED${NC}"
echo "========================================"
echo ""
log "========================================"
