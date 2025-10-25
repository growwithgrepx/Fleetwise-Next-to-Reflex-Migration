#!/bin/bash

# Fleetwise Startup Script
# This script starts both the Flask backend and Reflex frontend

set -e  # Exit on error

echo "========================================"
echo "  Starting Fleetwise Application"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if required files exist
if [ ! -f "backend/app.py" ]; then
    echo -e "${RED}Error: backend/app.py not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

if [ ! -f "app/app.py" ]; then
    echo -e "${RED}Error: app/app.py not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Function to cleanup background processes on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down servers...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        echo "  ✓ Backend stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        echo "  ✓ Frontend stopped"
    fi
    echo -e "${GREEN}Cleanup complete${NC}"
    exit 0
}

# Register cleanup function to run on script exit
trap cleanup EXIT INT TERM

# Check if backend is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}Warning: Port 8000 is already in use${NC}"
    echo "Another Flask backend may be running. Press Ctrl+C to exit or wait to continue..."
    sleep 3
fi

# Check if frontend is already running
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}Warning: Port 3000 is already in use${NC}"
    echo "Another Reflex frontend may be running. Press Ctrl+C to exit or wait to continue..."
    sleep 3
fi

# Start Flask backend
echo "Starting Flask backend on port 8000..."
python3 -m backend.app > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}Error: Backend failed to start${NC}"
    echo "Check backend.log for details:"
    tail -20 backend.log
    exit 1
fi

# Test backend health
if curl -s http://127.0.0.1:8000/health > /dev/null; then
    echo -e "${GREEN}✓ Backend is running on http://127.0.0.1:8000${NC}"
else
    echo -e "${RED}Error: Backend is not responding${NC}"
    exit 1
fi

# Start Reflex frontend
echo ""
echo "Starting Reflex frontend on port 3000..."
reflex run > frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
echo "Waiting for frontend to compile..."
sleep 10

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}Error: Frontend failed to start${NC}"
    echo "Check frontend.log for details:"
    tail -20 frontend.log
    exit 1
fi

echo -e "${GREEN}✓ Frontend is starting...${NC}"
echo ""
echo "========================================"
echo -e "  ${GREEN}✓ Fleetwise is running!${NC}"
echo "========================================"
echo ""
echo "  Backend:  http://127.0.0.1:8000"
echo "  Frontend: http://localhost:3000"
echo ""
echo "  Login credentials:"
echo "    Email:    admin@fleetwise.com"
echo "    Password: admin123"
echo ""
echo "  Press Ctrl+C to stop all servers"
echo ""
echo "  Logs are being written to:"
echo "    - backend.log"
echo "    - frontend.log"
echo ""

# Keep script running and show logs
tail -f backend.log frontend.log