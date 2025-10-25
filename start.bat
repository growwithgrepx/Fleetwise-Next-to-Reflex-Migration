@echo off
REM =============================================================================
REM Fleetwise - Startup Script with Port Cleanup (Windows)
REM =============================================================================

setlocal enabledelayedexpansion

REM Create logs directory
if not exist "logs" mkdir logs

REM Use fixed log names (overwrite previous run)
set LOGFILE=logs\start.log
set BACKEND_LOG=logs\backend.log
set REFLEX_LOG=logs\reflex.log

REM Clear previous logs
type nul > %LOGFILE%
type nul > %BACKEND_LOG%
type nul > %REFLEX_LOG%

echo [%date% %time%] ======================================== >> %LOGFILE%
echo [%date% %time%] Starting Fleetwise Application >> %LOGFILE%
echo [%date% %time%] ======================================== >> %LOGFILE%

echo.
echo ========================================
echo   Fleetwise Application Startup
echo ========================================
echo.
echo [INFO] Initializing startup sequence...
echo [INFO] Log file: %LOGFILE%
echo.

REM Step 1: Verify Prerequisites
echo [1/6] Verifying prerequisites...
echo [%date% %time%] Checking Python installation >> %LOGFILE%

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo [%date% %time%] ERROR: Python not found >> %LOGFILE%
    pause
    exit /b 1
)
echo [OK] Python installed

echo   Checking Python dependencies...
python -c "import flask_cors" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Missing dependencies. Installing...
    echo [%date% %time%] Installing Python dependencies >> %LOGFILE%
    python -m pip install -q flask flask-cors flask-sqlalchemy pyjwt werkzeug requests reflex
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        echo [%date% %time%] ERROR: pip install failed >> %LOGFILE%
        echo Run manually: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
)

REM Step 2: Force Clean ALL Orphaned Processes
echo.
echo [2/6] Force cleaning orphaned processes on ports 3000, 8000, 8001...
echo [%date% %time%] Force cleaning ports >> %LOGFILE%

for %%P in (3000 8000 8001) do (
    echo   Checking port %%P...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%P ^| findstr LISTENING 2^>nul') do (
        set PID=%%a
        if !PID! NEQ 0 (
            echo     Force killing process !PID! on port %%P
            echo [%date% %time%] Force killing PID !PID! on port %%P >> %LOGFILE%
            taskkill /F /PID !PID! >nul 2>&1
        )
    )
)

REM Also kill reflex and node processes by name
taskkill /F /IM reflex.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1

echo [OK] Ports cleaned

REM Step 3: Verify Port Availability
echo.
echo [3/6] Verifying port availability...
echo [%date% %time%] Verifying ports >> %LOGFILE%

timeout /t 3 /nobreak >nul

set PORT_ERROR=0
for %%P in (3000 8000 8001) do (
    netstat -an | findstr :%%P | findstr LISTENING >nul 2>&1
    if not errorlevel 1 (
        echo [ERROR] Port %%P still in use after cleanup!
        echo [%date% %time%] ERROR: Port %%P still in use >> %LOGFILE%
        set PORT_ERROR=1
    )
)

if %PORT_ERROR%==1 (
    echo [ERROR] Cannot start - ports still occupied
    pause
    exit /b 1
)

echo [OK] All ports available

REM Step 4: Start Flask Backend
echo.
echo [4/6] Starting Flask backend (port 8000)...
echo [%date% %time%] Starting Flask backend >> %LOGFILE%

start "Fleetwise-Backend" /MIN cmd /c "python backend\app.py > %BACKEND_LOG% 2>&1"

echo   Waiting for backend initialization...
timeout /t 5 /nobreak >nul

netstat -an | findstr :8000 | findstr LISTENING >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Backend failed to start on port 8000
    echo [%date% %time%] ERROR: Backend startup failed >> %LOGFILE%
    echo.
    echo Backend error log:
    type %BACKEND_LOG%
    echo.
    echo Full log: %BACKEND_LOG%
    pause
    exit /b 1
)

REM Save backend PID
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo %%a > logs\backend.pid
    echo [OK] Backend running on http://127.0.0.1:8000 (PID: %%a)
    echo [%date% %time%] Backend started successfully (PID: %%a) >> %LOGFILE%
    goto backend_done
)
:backend_done

REM Step 5: Start Reflex Frontend
echo.
echo [5/6] Starting Reflex frontend (ports 3000, 8001)...
echo [%date% %time%] Starting Reflex frontend >> %LOGFILE%

start "Fleetwise-Frontend" /MIN cmd /c "reflex run > %REFLEX_LOG% 2>&1"

echo   Waiting for frontend compilation (20 seconds)...
timeout /t 20 /nobreak >nul

REM Verify both Reflex ports
netstat -an | findstr :3000 | findstr LISTENING >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Frontend failed to start on port 3000
    echo [%date% %time%] ERROR: Frontend startup failed >> %LOGFILE%
    echo.
    echo Frontend error log:
    type %REFLEX_LOG%
    echo.
    echo Full log: %REFLEX_LOG%
    pause
    exit /b 1
)

REM Save frontend PID
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    echo %%a > logs\reflex.pid
    echo [OK] Frontend running on http://localhost:3000 (PID: %%a)
    echo [%date% %time%] Frontend started successfully (PID: %%a) >> %LOGFILE%
    goto frontend_done
)
:frontend_done

netstat -an | findstr :8001 | findstr LISTENING >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Reflex backend (port 8001) not detected
    echo [%date% %time%] WARNING: Port 8001 not listening >> %LOGFILE%
) else (
    echo [OK] Reflex backend running on http://127.0.0.1:8001
)

REM Step 6: Final Status
echo.
echo [6/6] Startup complete!
echo [%date% %time%] ======================================== >> %LOGFILE%
echo [%date% %time%] Startup completed successfully >> %LOGFILE%
echo [%date% %time%] ======================================== >> %LOGFILE%

echo.
echo ========================================
echo   Fleetwise is READY!
echo ========================================
echo.
echo   Services:
echo     [*] Backend API:     http://127.0.0.1:8000
echo     [*] Reflex Backend:  http://127.0.0.1:8001  
echo     [*] Frontend UI:     http://localhost:3000
echo.
echo   Login:
echo     Email:    admin@fleetwise.com
echo     Password: admin123
echo.
echo   Management:
echo     stop.bat    - Stop all services
echo     restart.bat - Restart services
echo     status.bat  - Check service status
echo.
echo   Logs:
echo     %LOGFILE%
echo     %BACKEND_LOG%
echo     %REFLEX_LOG%
echo.

REM Open browser
choice /C YN /M "Open browser now" /T 5 /D Y >nul 2>&1
if errorlevel 1 (
    start http://localhost:3000
    echo [INFO] Browser opened
)

echo.
echo [INFO] Services running in background windows
echo [INFO] Run stop.bat to terminate all services
echo.
pause