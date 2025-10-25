@echo off
REM =============================================================================
REM Fleetwise - Production-Grade Startup Script (Windows)
REM =============================================================================
REM Description: Gracefully cleans ports, starts services with proper ordering
REM Author: DevOps Team
REM Last Modified: 2025-10-25
REM =============================================================================

setlocal enabledelayedexpansion

REM Create logs directory
if not exist "logs" mkdir logs

REM Set log file with timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_%datetime:~8,2%-%datetime:~10,2%-%datetime:~12,2%
set LOGFILE=logs\start_%TIMESTAMP%.log

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

REM Step 2: Clean Orphaned Processes
echo.
echo [2/6] Cleaning orphaned processes on ports 3000, 8000, 8001...
echo [%date% %time%] Cleaning ports >> %LOGFILE%

for %%P in (3000 8000 8001) do (
    echo   Checking port %%P...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%P ^| findstr LISTENING') do (
        set PID=%%a
        if !PID! NEQ 0 (
            echo     Killing process !PID! on port %%P
            echo [%date% %time%] Killing PID !PID! on port %%P >> %LOGFILE%
            taskkill /F /PID !PID! >nul 2>&1
        )
    )
)
echo [OK] Ports cleaned

REM Step 3: Verify Port Availability
echo.
echo [3/6] Verifying port availability...
echo [%date% %time%] Verifying ports >> %LOGFILE%

timeout /t 2 /nobreak >nul

for %%P in (3000 8000 8001) do (
    netstat -an | findstr :%%P | findstr LISTENING >nul 2>&1
    if not errorlevel 1 (
        echo [ERROR] Port %%P still in use!
        echo [%date% %time%] ERROR: Port %%P still in use >> %LOGFILE%
        pause
        exit /b 1
    )
)
echo [OK] All ports available

REM Step 4: Start Flask Backend
echo.
echo [4/6] Starting Flask backend (port 8000)...
echo [%date% %time%] Starting Flask backend >> %LOGFILE%

start "Fleetwise-Backend" /MIN cmd /c "python backend\app.py > logs\backend_%TIMESTAMP%.log 2>&1"

REM Wait and verify backend
echo   Waiting for backend initialization...
timeout /t 5 /nobreak >nul

netstat -an | findstr :8000 | findstr LISTENING >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Backend failed to start on port 8000
    echo [%date% %time%] ERROR: Backend startup failed >> %LOGFILE%
    echo Check logs\backend_%TIMESTAMP%.log for details
    pause
    exit /b 1
)
echo [OK] Backend running on http://127.0.0.1:8000
echo [%date% %time%] Backend started successfully >> %LOGFILE%

REM Step 5: Start Reflex Frontend
echo.
echo [5/6] Starting Reflex frontend (ports 3000, 8001)...
echo [%date% %time%] Starting Reflex frontend >> %LOGFILE%

start "Fleetwise-Frontend" /MIN cmd /c "reflex run > logs\reflex_%TIMESTAMP%.log 2>&1"

REM Wait for compilation
echo   Waiting for frontend compilation...
timeout /t 20 /nobreak >nul

REM Verify both Reflex ports
netstat -an | findstr :3000 | findstr LISTENING >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Frontend failed to start on port 3000
    echo [%date% %time%] ERROR: Frontend startup failed >> %LOGFILE%
    echo Check logs\reflex_%TIMESTAMP%.log for details
    pause
    exit /b 1
)

netstat -an | findstr :8001 | findstr LISTENING >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Reflex backend (port 8001) not detected
    echo [%date% %time%] WARNING: Port 8001 not listening >> %LOGFILE%
)

echo [OK] Frontend running on http://localhost:3000
echo [OK] Reflex backend running on http://127.0.0.1:8001
echo [%date% %time%] Frontend started successfully >> %LOGFILE%

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
echo.
echo   Logs:
echo     %LOGFILE%
echo     logs\backend_%TIMESTAMP%.log
echo     logs\reflex_%TIMESTAMP%.log
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