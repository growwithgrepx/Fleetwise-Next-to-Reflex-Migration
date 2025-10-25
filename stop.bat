@echo off
REM =============================================================================
REM Fleetwise - Production-Grade Shutdown Script (Windows)
REM =============================================================================
REM Description: Gracefully terminates all Fleetwise services
REM Author: DevOps Team
REM Last Modified: 2025-10-25
REM =============================================================================

setlocal enabledelayedexpansion

REM Create logs directory
if not exist "logs" mkdir logs

REM Set log file with timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_%datetime:~8,2%-%datetime:~10,2%-%datetime:~12,2%
set LOGFILE=logs\stop_%TIMESTAMP%.log

echo [%date% %time%] ======================================== >> %LOGFILE%
echo [%date% %time%] Stopping Fleetwise Application >> %LOGFILE%
echo [%date% %time%] ======================================== >> %LOGFILE%

echo.
echo ========================================
echo   Fleetwise Application Shutdown
echo ========================================
echo.
echo [INFO] Initiating graceful shutdown...
echo [INFO] Log file: %LOGFILE%
echo.

REM Step 1: Terminate Reflex processes (frontend + backend)
echo [1/4] Stopping Reflex processes...
echo [%date% %time%] Terminating Reflex processes >> %LOGFILE%

taskkill /FI "WindowTitle eq Fleetwise-Frontend*" /F >nul 2>&1
taskkill /FI "IMAGENAME eq reflex.exe" /F >nul 2>&1

REM Kill Node.js processes spawned by Reflex
for /f "tokens=2" %%a in ('tasklist ^| findstr "node.exe"') do (
    echo   Terminating Node.js process %%a
    echo [%date% %time%] Killing Node.js PID %%a >> %LOGFILE%
    taskkill /F /PID %%a >nul 2>&1
)

echo [OK] Reflex processes terminated

REM Step 2: Terminate Flask backend
echo.
echo [2/4] Stopping Flask backend...
echo [%date% %time%] Terminating Flask backend >> %LOGFILE%

taskkill /FI "WindowTitle eq Fleetwise-Backend*" /F >nul 2>&1

REM Kill Python processes on port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo   Terminating Flask process %%a
    echo [%date% %time%] Killing Flask PID %%a on port 8000 >> %LOGFILE%
    taskkill /F /PID %%a >nul 2>&1
)

echo [OK] Flask backend terminated

REM Step 3: Clean all service ports
echo.
echo [3/4] Cleaning service ports (3000, 8000, 8001)...
echo [%date% %time%] Cleaning ports >> %LOGFILE%

for %%P in (3000 8000 8001) do (
    echo   Checking port %%P...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%P ^| findstr LISTENING') do (
        set PID=%%a
        if !PID! NEQ 0 (
            echo     Force killing remaining process !PID! on port %%P
            echo [%date% %time%] Force killing PID !PID! on port %%P >> %LOGFILE%
            taskkill /F /PID !PID! >nul 2>&1
        )
    )
)

echo [OK] Ports cleaned

REM Step 4: Verify all processes stopped
echo.
echo [4/4] Verifying shutdown...
echo [%date% %time%] Verifying shutdown >> %LOGFILE%

timeout /t 2 /nobreak >nul

set PORTS_CLEAR=1
for %%P in (3000 8000 8001) do (
    netstat -an | findstr :%%P | findstr LISTENING >nul 2>&1
    if not errorlevel 1 (
        echo [WARNING] Port %%P still in use
        echo [%date% %time%] WARNING: Port %%P still listening >> %LOGFILE%
        set PORTS_CLEAR=0
    )
)

if %PORTS_CLEAR%==1 (
    echo [OK] All services stopped, ports released
    echo [%date% %time%] Shutdown completed successfully >> %LOGFILE%
) else (
    echo [WARNING] Some ports may still be in use
    echo [%date% %time%] Shutdown completed with warnings >> %LOGFILE%
)

echo.
echo ========================================
echo   Fleetwise has been STOPPED
echo ========================================
echo.
echo [%date% %time%] ======================================== >> %LOGFILE%
echo.

pause
