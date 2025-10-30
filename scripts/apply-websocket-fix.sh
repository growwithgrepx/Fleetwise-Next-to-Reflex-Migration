#!/bin/bash

echo "Applying WebSocket Fix"
echo "======================"
echo ""

# Stop services
echo "[1/4] Stopping services..."
./stop.sh 2>/dev/null || true
sleep 2

# Clear Reflex cache
echo "[2/4] Clearing Reflex cache..."
rm -rf .web
rm -rf __pycache__
rm -rf app/__pycache__
rm -rf app/**/__pycache__
rm -rf backend/__pycache__

# Backup old config
echo "[3/4] Backing up rxconfig.py..."
if [ -f "rxconfig.py" ]; then
    cp rxconfig.py rxconfig.py.backup
fi

# Apply fix
echo "[4/4] Applying configuration fix..."
cat > rxconfig.py << 'EOF'
import reflex as rx

config = rx.Config(
    app_name="app",
    plugins=[
        rx.plugins.TailwindV3Plugin(),
        rx.plugins.sitemap.SitemapPlugin(),
    ],
    frontend_host="0.0.0.0",
    frontend_port=3000,
    backend_host="127.0.0.1",
    backend_port=8001,
)
EOF

echo ""
echo "Fix applied successfully!"
echo ""
echo "Next steps:"
echo "  1. Run: ./start.sh"
echo "  2. Wait 30 seconds for compilation"
echo "  3. Open: http://localhost:3000"
echo "  4. Login: admin@fleetwise.com / admin123"
echo ""
echo "WebSocket should now connect to: ws://127.0.0.1:8001/_event"
echo "(NOT ws://127.0.0.1:8000/_event)"
echo ""