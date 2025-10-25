#!/bin/bash
###############################################################################
# Fleetwise - Startup Script with Port Cleanup (Unix/Linux/macOS)
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

# Use fixed log names (overwrite previous run)
LOGFILE="logs/start.log"
BACKEND_LOG="logs/backend.log"
REFLEX_LOG="logs/reflex.log"

# Clear previous logs
> "$LOGFILE"
> "$BACKEND_LOG"
> "$REFLEX_LOG"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE"
}

log "========================================"
log "Starting Fleetwise Application"
log "========================================"

echo ""
echo "========================================"
echo "  Fleetwise Application Startup"
echo "========================================"
echo ""
echo -e "${BLUE}[INFO]${NC} Initializing startup sequence..."
echo -e "${BLUE}[INFO]${NC} Log file: $LOGFILE"
echo ""

# Step 1: Verify Prerequisites
echo -e "${BLUE}[1/6]${NC} Verifying prerequisites..."
log "Checking prerequisites"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 is not installed"
    log "ERROR: Python 3 not found"
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Python 3 installed"

# Check Python dependencies
echo "  Checking Python dependencies..."
if ! python3 -c "import flask_cors" 2>/dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} Missing dependencies. Installing..."
    log "Installing Python dependencies"
    python3 -m pip install -q flask flask-cors flask-sqlalchemy pyjwt werkzeug requests reflex
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR]${NC} Failed to install dependencies"
        log "ERROR: pip install failed"
        echo "Run manually: pip install -r requirements.txt"
        exit 1
    fi
    echo -e "${GREEN}[OK]${NC} Dependencies installed"
fi

if ! command -v reflex &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Reflex is not installed"
    log "ERROR: Reflex not found"
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Reflex installed"

# Step 2: Force Clean ALL Orphaned Processes
echo ""
echo -e "${BLUE}[2/6]${NC} Cleaning orphaned processes on ports 3000, 8000, 8001..."
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
                echo "    Killing process $PID on port $PORT"
                log "Force killing PID $PID on port $PORT"
                kill -9 $PID 2>/dev/null || true
            fi
        done
    fi
done

# Also kill any reflex/node processes by name
if command -v pkill &> /dev/null; then
    pkill -9 -f "reflex run" 2>/dev/null || true
    pkill -9 -f "react-router" 2>/dev/null || true
    pkill -9 -f "node.*vite" 2>/dev/null || true
fi

echo -e "${GREEN}[OK]${NC} Ports cleaned"

# Step 3: Verify Port Availability
echo ""
echo -e "${BLUE}[3/6]${NC} Verifying port availability..."
log "Verifying ports"

sleep 3

for PORT in 3000 8000 8001; do
    if command -v lsof &> /dev/null; then
        if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo -e "${RED}[ERROR]${NC} Port $PORT still in use after cleanup!"
            log "ERROR: Port $PORT still in use"
            exit 1
        fi
    fi
done
echo -e "${GREEN}[OK]${NC} All ports available"

# Step 4: Start Flask Backend
echo ""
echo -e "${BLUE}[4/6]${NC} Starting Flask backend (port 8000)..."
log "Starting Flask backend"

python3 backend/app.py > "$BACKEND_LOG" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "logs/backend.pid"

echo "  Waiting for backend initialization..."
sleep 5

# Verify backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}[ERROR]${NC} Backend process died"
    log "ERROR: Backend process died"
    echo ""
    echo "Backend error log:"
    tail -20 "$BACKEND_LOG"
    echo ""
    echo "Full log: $BACKEND_LOG"
    exit 1
fi

# Check if port 8000 is listening
if command -v lsof &> /dev/null; then
    if ! lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}[ERROR]${NC} Backend not listening on port 8000"
        log "ERROR: Backend startup failed"
        echo ""
        echo "Backend error log:"
        tail -20 "$BACKEND_LOG"
        echo ""
        echo "Full log: $BACKEND_LOG"
        exit 1
    fi
fi

echo -e "${GREEN}[OK]${NC} Backend running on http://127.0.0.1:8000"
log "Backend started successfully (PID: $BACKEND_PID)"

# Step 5: Start Reflex Frontend
echo ""
echo -e "${BLUE}[5/6]${NC} Starting Reflex frontend (ports 3000, 8001)..."
log "Starting Reflex frontend"

reflex run > "$REFLEX_LOG" 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "logs/reflex.pid"

echo "  Waiting for frontend compilation (20 seconds)..."
sleep 20

# Verify frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}[ERROR]${NC} Frontend process died"
    log "ERROR: Frontend process died"
    echo ""
    echo "Frontend error log:"
    tail -20 "$REFLEX_LOG"
    echo ""
    echo "Full log: $REFLEX_LOG"
    exit 1
fi

# Check if port 3000 is listening
if command -v lsof &> /dev/null; then
    if ! lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}[ERROR]${NC} Frontend not listening on port 3000"
        log "ERROR: Frontend startup failed"
        echo ""
        echo "Frontend error log:"
        tail -20 "$REFLEX_LOG"
        echo ""
        echo "Full log: $REFLEX_LOG"
        exit 1
    fi
    
    if ! lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}[WARNING]${NC} Reflex backend (port 8001) not detected"
        log "WARNING: Port 8001 not listening"
    fi
fi

echo -e "${GREEN}[OK]${NC} Frontend running on http://localhost:3000"
echo -e "${GREEN}[OK]${NC} Reflex backend running on http://127.0.0.1:8001"
log "Frontend started successfully (PID: $FRONTEND_PID)"

# Step 6: Final Status
echo ""
echo -e "${BLUE}[6/6]${NC} Startup complete!"
log "========================================"
log "Startup completed successfully"
log "========================================"

echo ""
echo "========================================"
echo -e "  ${GREEN}Fleetwise is READY!${NC}"
echo "========================================"
echo ""
echo "  Services:"
echo -e "    ${GREEN}[✓]${NC} Backend API:     http://127.0.0.1:8000"
echo -e "    ${GREEN}[✓]${NC} Reflex Backend:  http://127.0.0.1:8001"
echo -e "    ${GREEN}[✓]${NC} Frontend UI:     http://localhost:3000"
echo ""
echo "  Login:"
echo "    Email:    admin@fleetwise.com"
echo "    Password: admin123"
echo ""
echo "  Management:"
echo "    ./stop.sh    - Stop all services"
echo "    ./restart.sh - Restart services"
echo "    ./status.sh  - Check service status"
echo ""
echo "  Logs:"
echo "    $LOGFILE"
echo "    $BACKEND_LOG"
echo "    $REFLEX_LOG"
echo ""
echo "  PIDs saved to:"
echo "    logs/backend.pid ($BACKEND_PID)"
echo "    logs/reflex.pid ($FRONTEND_PID)"
echo ""
echo -e "${BLUE}[INFO]${NC} Services running in background"
echo -e "${BLUE}[INFO]${NC} Run ./stop.sh to terminate all services"
echo ""