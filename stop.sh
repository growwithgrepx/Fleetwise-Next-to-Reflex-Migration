#!/bin/bash
###############################################################################
# Fleetwise - Graceful Shutdown Script (Unix/Linux/macOS)
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
LOGFILE="logs/stop.log"
> "$LOGFILE"

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

# Step 1: Graceful Stop - Try SIGTERM first
echo -e "${BLUE}[1/4]${NC} Attempting graceful shutdown..."
log "Attempting graceful shutdown"

if [ -f "logs/reflex.pid" ]; then
    REFLEX_PID=$(cat logs/reflex.pid)
    if kill -0 $REFLEX_PID 2>/dev/null; then
        echo "  Stopping Reflex (PID: $REFLEX_PID) gracefully..."
        log "Sending SIGTERM to Reflex PID $REFLEX_PID"
        kill -TERM $REFLEX_PID 2>/dev/null || true
    fi
fi

if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo "  Stopping Backend (PID: $BACKEND_PID) gracefully..."
        log "Sending SIGTERM to Backend PID $BACKEND_PID"
        kill -TERM $BACKEND_PID 2>/dev/null || true
    fi
fi

echo "  Waiting 3 seconds for graceful shutdown..."
sleep 3

# Step 2: Check if processes stopped, force kill if needed
echo ""
echo -e "${BLUE}[2/4]${NC} Checking for remaining processes..."
log "Checking for remaining processes"

FORCE_KILL_NEEDED=false

if [ -f "logs/reflex.pid" ]; then
    REFLEX_PID=$(cat logs/reflex.pid)
    if kill -0 $REFLEX_PID 2>/dev/null; then
        echo "  Reflex still running, force killing..."
        log "Force killing Reflex PID $REFLEX_PID"
        kill -9 $REFLEX_PID 2>/dev/null || true
        FORCE_KILL_NEEDED=true
    fi
    rm -f logs/reflex.pid
fi

if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo "  Backend still running, force killing..."
        log "Force killing Backend PID $BACKEND_PID"
        kill -9 $BACKEND_PID 2>/dev/null || true
        FORCE_KILL_NEEDED=true
    fi
    rm -f logs/backend.pid
fi

# Kill any remaining reflex/node processes by name
if command -v pkill &> /dev/null; then
    pkill -9 -f "reflex run" 2>/dev/null || true
    pkill -9 -f "react-router" 2>/dev/null || true
    pkill -9 -f "node.*vite" 2>/dev/null || true
fi

if [ "$FORCE_KILL_NEEDED" = true ]; then
    echo -e "${YELLOW}[OK]${NC} Force kill was necessary"
else
    echo -e "${GREEN}[OK]${NC} Graceful shutdown successful"
fi

# Step 3: Force Clean ALL Service Ports
echo ""
echo -e "${BLUE}[3/4]${NC} Force cleaning service ports (3000, 8000, 8001)..."
log "Force cleaning ports"

for PORT in 3000 8000 8001; do
    echo "  Checking port $PORT..."
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
                echo "    Force killing process $PID on port $PORT"
                log "Force killing PID $PID on port $PORT"
                kill -9 $PID 2>/dev/null || true
            fi
        done
    fi
done

echo -e "${GREEN}[OK]${NC} Ports cleaned"

# Step 4: Verify All Processes Stopped
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
    echo "  Run ./stop.sh again or manually check with: lsof -ti:3000,8000,8001"
    log "Shutdown completed with warnings"
fi

echo ""
echo "========================================"
echo -e "  ${GREEN}Fleetwise has been STOPPED${NC}"
echo "========================================"
echo ""
log "========================================"