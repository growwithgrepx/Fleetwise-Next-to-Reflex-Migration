# Fleetwise MVP

Fleet management application built with Python Reflex framework.

## Quick Start

### Prerequisites
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Start Application
```bash
# Terminal 1 - Backend
python backend/app.py

# Terminal 2 - Frontend
reflex run
```

### Access
- **URL**: http://localhost:3000
- **Login**: admin@fleetwise.com / admin123

## Scripts

All management scripts are in `scripts/` directory:

### Windows
- `scripts\start.bat` - Start all services
- `scripts\stop.bat` - Stop all services
- `scripts\restart.bat` - Restart all services
- `scripts\status.bat` - Check service status
- `scripts\logs.bat` - View application logs
- `scripts\cleanup-logs.bat` - Remove old logs (>24h)

### Linux/macOS
- `scripts/start.sh` - Start all services
- `scripts/stop.sh` - Stop all services
- `scripts/restart.sh` - Restart all services
- `scripts/status.sh` - Check service status
- `scripts/logs.sh` - View application logs
- `scripts/cleanup-logs.sh` - Remove old logs (>24h)

### Testing
- `scripts/setup_verify.py` - Verify setup
- `scripts/test_crud.py` - Test CRUD operations

## Configuration

### Local Development
Default configuration works out of the box.

### Cloud Deployment (render.com, etc.)
1. Copy `.env.example` to `.env`
2. Set environment variables:
   ```bash
   FRONTEND_HOST=0.0.0.0
   BACKEND_HOST=0.0.0.0
   API_HOST=0.0.0.0  # Important for cloud
   PORT=10000  # Or your cloud provider's port
   ```

## Architecture

```
Port 3000: Frontend (React/Reflex)
Port 8001: Reflex Backend (State Management)
Port 8000: Flask API (REST)
```

## Features

- JWT Authentication
- Driver CRUD operations
- Dark theme UI
- Responsive design
- Automated log rotation

## Log Management

Logs are stored in `logs/` directory:
- `backend.log` - Flask API logs
- `reflex.log` - Frontend logs
- `start.log`, `stop.log`, `restart.log` - Script logs

Logs older than 24 hours are automatically cleaned on restart.
Manual cleanup: `scripts/cleanup-logs.bat` or `scripts/cleanup-logs.sh`

## Troubleshooting

### Port Already in Use
Run: `scripts/stop.bat` or `scripts/stop.sh`

### Database Issues
```bash
rm backend/fleetwise.db
python backend/app.py
```

### Check Status
```bash
scripts/status.bat  # Windows
./scripts/status.sh # Linux/macOS
```

### View Logs
```bash
scripts/logs.bat    # Windows
./scripts/logs.sh   # Linux/macOS
```

## Development

### Project Structure
```
app/                    # Reflex frontend
  pages/               # Page components
  states/              # State management
  components/          # UI components
backend/               # Flask API
  app.py              # API server
  models.py           # Database models
  config.py           # Configuration
scripts/              # Management scripts
logs/                 # Application logs (auto-cleanup)
```

### Environment Variables
See `.env.example` for all available configuration options.

## Deployment

### Local
Use provided scripts in `scripts/` directory.

### Cloud (render.com, Railway, etc.)
1. Set environment variables
2. Start command: `reflex run --backend-only`
3. Web command: `python backend/app.py`

Or use Docker:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 3000 8000 8001
CMD ["reflex", "run"]
```

## Support

Run verification: `python scripts/setup_verify.py`
Check status: `scripts/status.bat` or `./scripts/status.sh`
View logs: `scripts/logs.bat` or `./scripts/logs.sh`