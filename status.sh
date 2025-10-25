#!/bin/bash
###############################################################################
# Fleetwise - Service Status Check Script (Unix/Linux/macOS)
###############################################################################

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo "========================================"
echo "  Fleetwise Service Status"
echo "========================================"
echo ""

# Check Backend (Port 8000)
echo -e "${BLUE}[Backend API - Port 8000]${NC}"
if command -v lsof &> /dev/null; then
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        PID=$(lsof -Pi :8000 -sTCP:LISTEN -t)
        echo -e "  ${GREEN}✓${NC} Running (PID: $PID)"
        if [ -f "logs/backend.pid" ]; then
            SAVED_PID=$(cat logs/backend.pid)
            if [ "$PID" = "$SAVED_PID" ]; then
                echo -e "  ${GREEN}✓${NC} PID matches saved PID"
            else
                echo -e "  ${YELLOW}⚠${NC} PID mismatch (saved: $SAVED_PID, actual: $PID)"
            fi
        fi
    else
        echo -e "  ${RED}✗${NC} Not running"
    fi
else
    echo -e "  ${YELLOW}⚠${NC} Cannot check (lsof not available)"
fi

echo ""

# Check Reflex Backend (Port 8001)
echo -e "${BLUE}[Reflex Backend - Port 8001]${NC}"
if command -v lsof &> /dev/null; then
    if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1; then
        PID=$(lsof -Pi :8001 -sTCP:LISTEN -t)
        echo -e "  ${GREEN}✓${NC} Running (PID: $PID)"
    else
        echo -e "  ${RED}✗${NC} Not running"
    fi
else
    echo -e "  ${YELLOW}⚠${NC} Cannot check (lsof not available)"
fi

echo ""

# Check Frontend (Port 3000)
echo -e "${BLUE}[Frontend UI - Port 3000]${NC}"
if command -v lsof &> /dev/null; then
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        PID=$(lsof -Pi :3000 -sTCP:LISTEN -t)
        echo -e "  ${GREEN}✓${NC} Running (PID: $PID)"
        if [ -f "logs/reflex.pid" ]; then
            SAVED_PID=$(cat logs/reflex.pid)
            if [ "$PID" = "$SAVED_PID" ]; then
                echo -e "  ${GREEN}✓${NC} PID matches saved PID"
            else
                echo -e "  ${YELLOW}⚠${NC} PID mismatch (saved: $SAVED_PID, actual: $PID)"
            fi
        fi
    else
        echo -e "  ${RED}✗${NC} Not running"
    fi
else
    echo -e "  ${YELLOW}⚠${NC} Cannot check (lsof not available)"
fi

echo ""

# Overall Status
echo "========================================"
BACKEND_OK=false
FRONTEND_OK=false

if command -v lsof &> /dev/null; then
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        BACKEND_OK=true
    fi
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        FRONTEND_OK=true
    fi
fi

if [ "$BACKEND_OK" = true ] && [ "$FRONTEND_OK" = true ]; then
    echo -e "${GREEN}✓ All services running${NC}"
    echo ""
    echo "Access URLs:"
    echo "  Backend:  http://127.0.0.1:8000"
    echo "  Frontend: http://localhost:3000"
elif [ "$BACKEND_OK" = true ]; then
    echo -e "${YELLOW}⚠ Backend running, but frontend is down${NC}"
    echo "  Start frontend: reflex run"
elif [ "$FRONTEND_OK" = true ]; then
    echo -e "${YELLOW}⚠ Frontend running, but backend is down${NC}"
    echo "  Start backend: python backend/app.py"
else
    echo -e "${RED}✗ No services running${NC}"
    echo "  Start all: ./start.sh"
fi

echo "========================================"
echo ""