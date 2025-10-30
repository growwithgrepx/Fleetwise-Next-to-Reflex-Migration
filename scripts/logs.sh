#!/bin/bash

cd "$(dirname "$0")/.."

echo ""
echo "Fleetwise Log Viewer"
echo "==================="
echo ""
echo "[1] Tail backend log"
echo "[2] Tail reflex log"
echo "[3] Tail all logs"
echo "[4] Show last 50 lines of backend"
echo "[5] Show last 50 lines of reflex"
echo "[6] Exit"
echo ""

read -p "Select option (1-6): " choice

case $choice in
    1)
        if [ -f "logs/backend.log" ]; then
            echo ""
            echo "Tailing backend.log (Ctrl+C to stop)..."
            echo ""
            tail -f -n 20 logs/backend.log
        else
            echo "[ERROR] logs/backend.log not found"
        fi
        ;;
    2)
        if [ -f "logs/reflex.log" ]; then
            echo ""
            echo "Tailing reflex.log (Ctrl+C to stop)..."
            echo ""
            tail -f -n 20 logs/reflex.log
        else
            echo "[ERROR] logs/reflex.log not found"
        fi
        ;;
    3)
        echo ""
        echo "Tailing all logs (Ctrl+C to stop)..."
        echo ""
        if command -v tmux &> /dev/null; then
            tmux new-session -d -s fleetwise-logs
            tmux split-window -h
            tmux send-keys -t 0 "tail -f logs/backend.log" C-m
            tmux send-keys -t 1 "tail -f logs/reflex.log" C-m
            tmux attach-session -t fleetwise-logs
        else
            echo "Backend log:" && tail -f -n 20 logs/backend.log &
            BACKEND_PID=$!
            echo "Reflex log:" && tail -f -n 20 logs/reflex.log &
            REFLEX_PID=$!
            wait
        fi
        ;;
    4)
        if [ -f "logs/backend.log" ]; then
            echo ""
            echo "Last 50 lines of backend.log:"
            echo ""
            tail -n 50 logs/backend.log
        else
            echo "[ERROR] logs/backend.log not found"
        fi
        ;;
    5)
        if [ -f "logs/reflex.log" ]; then
            echo ""
            echo "Last 50 lines of reflex.log:"
            echo ""
            tail -n 50 logs/reflex.log
        else
            echo "[ERROR] logs/reflex.log not found"
        fi
        ;;
    6)
        exit 0
        ;;
    *)
        echo "[ERROR] Invalid option"
        ;;
esac

echo ""