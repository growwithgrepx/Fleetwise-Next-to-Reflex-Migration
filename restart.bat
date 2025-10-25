@echo off
REM =============================================================================
REM Fleetwise - Production-Grade Restart Script (Windows)
REM =============================================================================
REM Description: Stops and restarts all Fleetwise services
REM Author: DevOps Team
REM Last Modified: 2025-10-25
REM =============================================================================

setlocal enabledelayedexpansion

REM Create logs directory
if not exist "logs" mkdir logs

REM Set log file with timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_%datetime:~8,2%-%datetime:~10,2%-%datetime:~12,2%
set LOGFILE=logs\restart_%TIMESTAMP%.log

echo [%date% %time%] ======================================== >> %LOGFILE%
echo [%date% %time%] Restarting Fleetwise Application >> %LOGFILE%
echo [%date% %time%] ======================================== >> %LOGFILE%

echo.
echo ========================================
echo   Fleetwise Application Restart
echo ========================================
echo.
echo [INFO] Initiating restart sequence...
echo [INFO] Log file: %LOGFILE%
echo.

REM Phase 1: Graceful Shutdown
echo ========================================
echo   PHASE 1: Stopping Services
echo ========================================
echo.
echo [%date% %time%] Phase 1: Stopping services >> %LOGFILE%

REM Terminate all Fleetwise processes
echo [1/3] Stopping Reflex frontend...
taskkill /FI "WindowTitle eq Fleetwise-Frontend*" /F >nul 2>&1
taskkill /FI "IMAGENAME eq reflex.exe" /F >nul 2>&1

REM Kill Node.js processes
for /f "tokens=2" %%a in ('tasklist ^| findstr "node.exe"') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo [OK] Reflex stopped

echo.
echo [2/3] Stopping Flask backend...
taskkill /FI "WindowTitle eq Fleetwise-Backend*" /F >nul 2>&1

REM Clean ports
for %%P in (3000 8000 8001) do (
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%P ^| findstr LISTENING') do (
        taskkill /F /PID %%a >nul 2>&1
    )
)
echo [OK] Backend stopped

echo.
echo [3/3] Cleaning ports...
timeout /t 3 /nobreak >nul

REM Verify ports are free
set PORTS_READY=1
for %%P in (3000 8000 8001) do (
    netstat -an | findstr :%%P | findstr LISTENING >nul 2>&1
    if not errorlevel 1 (
        echo [ERROR] Port %%P still in use!
        echo [%date% %time%] ERROR: Port %%P not freed >> %LOGFILE%
        set PORTS_READY=0
    )
)

if %PORTS_READY%==0 (
    echo [ERROR] Cannot restart - ports still occupied
    echo [%date% %time%] Restart failed - ports blocked >> %LOGFILE%
    pause
    exit /b 1
)
echo [OK] All ports available

echo [%date% %time%] Phase 1 complete - services stopped >> %LOGFILE%

REM Phase 2: Startup
echo.
echo ========================================
echo   PHASE 2: Starting Services
echo ========================================
echo.
echo [%date% %time%] Phase 2: Starting services >> %LOGFILE%

echo [1/2] Starting Flask backend...
echo [%date% %time%] Starting Flask backend >> %LOGFILE%
start "Fleetwise-Backend" /MIN cmd /c "python backend\app.py > logs\backend_%TIMESTAMP%.log 2>&1"

echo   Waiting for backend initialization...
timeout /t 5 /nobreak >nul

netstat -an | findstr :8000 | findstr LISTENING >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Backend failed to start
    echo [%date% %time%] ERROR: Backend startup failed >> %LOGFILE%
    pause
    exit /b 1
)
echo [OK] Backend running

echo.
echo [2/2] Starting Reflex frontend...
echo [%date% %time%] Starting Reflex frontend >> %LOGFILE%
start "Fleetwise-Frontend" /MIN cmd /c "reflex run > logs\reflex_%TIMESTAMP%.log 2>&1"

echo   Waiting for frontend compilation...
timeout /t 20 /nobreak >nul

netstat -an | findstr :3000 | findstr LISTENING >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Frontend failed to start
    echo [%date% %time%] ERROR: Frontend startup failed >> %LOGFILE%
    pause
    exit /b 1
)
echo [OK] Frontend running

echo [%date% %time%] Phase 2 complete - services started >> %LOGFILE%

REM Final Status
echo.
echo ========================================
echo   Restart COMPLETE!
echo ========================================
echo.
echo   Services:
echo     [*] Backend API:     http://127.0.0.1:8000
echo     [*] Reflex Backend:  http://127.0.0.1:8001
echo     [*] Frontend UI:     http://localhost:3000
echo.
echo   Logs:
echo     %LOGFILE%
echo     logs\backend_%TIMESTAMP%.log
echo     logs\reflex_%TIMESTAMP%.log
echo.
echo [%date% %time%] ======================================== >> %LOGFILE%
echo [%date% %time%] Restart completed successfully >> %LOGFILE%
echo [%date% %time%] ======================================== >> %LOGFILE%

REM Open browser
choice /C YN /M "Open browser now" /T 5 /D Y >nul 2>&1
if errorlevel 1 (
    start http://localhost:3000
    echo [INFO] Browser opened
)

echo.
pause
