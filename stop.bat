@echo off
REM =============================================================================
REM Fleetwise - Graceful Shutdown Script (Windows)
REM =============================================================================

setlocal enabledelayedexpansion

REM Create logs directory
if not exist "logs" mkdir logs

REM Use fixed log name (overwrite previous run)
set LOGFILE=logs\stop.log
type nul > %LOGFILE%

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

REM Step 1: Graceful Stop - Try normal termination first
echo [1/4] Attempting graceful shutdown...
echo [%date% %time%] Attempting graceful shutdown >> %LOGFILE%

taskkill /FI "WindowTitle eq Fleetwise-Frontend*" >nul 2>&1
taskkill /FI "WindowTitle eq Fleetwise-Backend*" >nul 2>&1

echo   Waiting 3 seconds for graceful shutdown...
timeout /t 3 /nobreak >nul

REM Step 2: Check if processes stopped, force kill if needed
echo.
echo [2/4] Checking for remaining processes...
echo [%date% %time%] Checking for remaining processes >> %LOGFILE%

set FORCE_KILL_NEEDED=0

REM Force kill reflex and node processes
taskkill /F /IM reflex.exe >nul 2>&1
if not errorlevel 1 (
    echo   Force killed Reflex processes
    echo [%date% %time%] Force killed Reflex >> %LOGFILE%
    set FORCE_KILL_NEEDED=1
)

taskkill /F /IM node.exe >nul 2>&1
if not errorlevel 1 (
    echo   Force killed Node.js processes
    echo [%date% %time%] Force killed Node.js >> %LOGFILE%
    set FORCE_KILL_NEEDED=1
)

REM Delete PID files
if exist logs\backend.pid del logs\backend.pid
if exist logs\reflex.pid del logs\reflex.pid

if %FORCE_KILL_NEEDED%==1 (
    echo [OK] Force kill was necessary
) else (
    echo [OK] Graceful shutdown successful
)

REM Step 3: Force Clean ALL Service Ports
echo.
echo [3/4] Force cleaning service ports (3000, 8000, 8001)...
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

echo [OK] Ports cleaned

REM Step 4: Verify All Processes Stopped
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
    echo   Run stop.bat again or manually check with: netstat -ano ^| findstr :3000
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