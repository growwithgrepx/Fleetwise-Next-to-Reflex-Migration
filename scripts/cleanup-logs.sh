#!/bin/bash

cd "$(dirname "$0")/.."

echo ""
echo "Fleetwise Log Cleanup"
echo "===================="
echo ""

if [ ! -d "logs" ]; then
    echo "[INFO] No logs directory found"
    exit 0
fi

echo "[INFO] Removing logs older than 24 hours..."

find logs/ -name "*.log" -type f -mmin +1440 -delete 2>/dev/null

echo "[OK] Cleanup complete"

count=$(find logs/ -name "*.log" -type f 2>/dev/null | wc -l)
echo "[INFO] Current log files: $count"

echo ""