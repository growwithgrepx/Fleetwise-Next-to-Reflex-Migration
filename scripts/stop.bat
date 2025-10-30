@echo off
setlocal enabledelayedexpansion

if not exist "logs" mkdir logs

set LOGFILE=logs\stop.log
type nul > %LOGFILE%

echo [%date% %time%] Stopping Fleetwise Application >> %LOGFILE%
echo.
echo Stopping Fleetwise Application
echo.

echo [1/4] Attempting graceful shutdown...
taskkill /FI "WindowTitle eq Fleetwise-Frontend*" >nul 2>&1
taskkill /FI "WindowTitle eq Fleetwise-Backend*" >nul 2>&1
timeout /t 3 /nobreak >nul

echo.
echo [2/4] Checking for remaining processes...
set FORCE_KILL_NEEDED=0

taskkill /F /IM reflex.exe >nul 2>&1
if not errorlevel 1 set FORCE_KILL_NEEDED=1

taskkill /F /IM node.exe >nul 2>&1
if not errorlevel 1 set FORCE_KILL_NEEDED=1

if exist logs\backend.pid del logs\backend.pid
if exist logs\reflex.pid del logs\reflex.pid

if %FORCE_KILL_NEEDED%==1 (
    echo [OK] Force kill was necessary
) else (
    echo [OK] Graceful shutdown successful
)

echo.
echo [3/4] Force cleaning service ports...
for %%P in (3000 8000 8001) do (
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%P ^| findstr LISTENING 2^>nul') do (
        taskkill /F /PID %%a >nul 2>&1
    )
)
echo [OK] Ports cleaned

echo.
echo [4/4] Verifying shutdown...
timeout /t 2 /nobreak >nul

set PORTS_CLEAR=1
for %%P in (3000 8000 8001) do (
    netstat -an | findstr :%%P | findstr LISTENING >nul 2>&1
    if not errorlevel 1 set PORTS_CLEAR=0
)

if %PORTS_CLEAR%==1 (
    echo [OK] All services stopped
) else (
    echo [WARNING] Some ports may still be in use
)

echo.
echo Fleetwise has been STOPPED
echo.
pause