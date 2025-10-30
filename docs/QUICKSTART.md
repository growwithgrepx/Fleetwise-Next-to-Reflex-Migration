# Fleetwise Quick Start

## For Git Bash/MINGW64 Users (Windows)

### Initial Setup (One Time)

1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database:**
   ```bash
   python backend/app.py
   # Wait for "Running on http://0.0.0.0:8000"
   # Press Ctrl+C
   ```

### Start Application

**Option 1: Using Scripts (Recommended)**

From project root:
```bash
cd scripts
./start.sh
```

**Option 2: Manual Start (Two Terminals)**

Terminal 1 - Backend:
```bash
python backend/app.py
```

Terminal 2 - Frontend:
```bash
reflex run
```

### Access Application

- URL: http://localhost:3000
- Login: admin@fleetwise.com / admin123

### Stop Application

From scripts directory:
```bash
cd scripts
./stop.sh
```

Or press Ctrl+C in both terminals.

### Troubleshooting

**Backend fails to start:**
```bash
# Test backend
python scripts/test_backend.py

# If database missing
python backend/app.py
# Press Ctrl+C after it starts
```

**Check status:**
```bash
cd scripts
./status.sh
```

**View logs:**
```bash
cd scripts
./logs.sh
```

**Clean old logs:**
```bash
cd scripts
./cleanup-logs.sh
```

### Verification

```bash
cd scripts
python setup_verify.py
```

Expected: All checks pass

### Testing CRUD

```bash
cd scripts
python test_crud.py
```

Expected: All operations pass

## For PowerShell/CMD Users (Windows)

Use the `.bat` versions:
- `scripts\start.bat`
- `scripts\stop.bat`
- `scripts\status.bat`
- `scripts\logs.bat`

## Cloud Deployment

1. Copy `.env.example` to `.env`
2. Set:
   ```
   FRONTEND_HOST=0.0.0.0
   BACKEND_HOST=0.0.0.0
   API_HOST=0.0.0.0
   PORT=<your-cloud-port>
   ```
3. Deploy

## Notes

- Scripts work from `scripts/` directory but operate on parent project
- All logs go to `logs/` directory in project root
- Logs auto-cleanup after 24 hours
- Git Bash uses `netstat` instead of `lsof` on Windows