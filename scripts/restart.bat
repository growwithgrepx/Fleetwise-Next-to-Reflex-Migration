@echo off
setlocal enabledelayedexpansion

if not exist "logs" mkdir logs

set LOGFILE=logs\restart.log
type nul > %LOGFILE%

echo [%date% %time%] Restarting Fleetwise Application >> %LOGFILE%
echo.
echo Restarting Fleetwise Application
echo.

echo [PHASE 1: Stopping Services]
echo.
if exist scripts\stop.bat (
    call scripts\stop.bat
) else (
    echo [ERROR] scripts\stop.bat not found
    pause
    exit /b 1
)

echo.
echo Waiting 3 seconds before restart...
timeout /t 3 /nobreak >nul

set MAX_RETRIES=3
set RETRY_COUNT=0
set PORTS_READY=0

:check_ports_loop
if %RETRY_COUNT% GEQ %MAX_RETRIES% goto ports_check_done

set PORTS_READY=1
for %%P in (3000 8000 8001) do (
    netstat -an | findstr :%%P | findstr LISTENING >nul 2>&1
    if not errorlevel 1 (
        set PORTS_READY=0
        for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%P ^| findstr LISTENING 2^>nul') do (
            taskkill /F /PID %%a >nul 2>&1
        )
    )
)

if %PORTS_READY%==0 (
    set /a RETRY_COUNT+=1
    if %RETRY_COUNT% LSS %MAX_RETRIES% (
        timeout /t 2 /nobreak >nul
        goto check_ports_loop
    )
)

:ports_check_done

if %PORTS_READY%==0 (
    echo [ERROR] Cannot restart - ports still occupied
    pause
    exit /b 1
)

echo [OK] All ports available

echo.
echo [PHASE 2: Starting Services]
echo.
if exist scripts\start.bat (
    call scripts\start.bat
) else (
    echo [ERROR] scripts\start.bat not found
    pause
    exit /b 1
)

echo.
echo Restart COMPLETE!
echo.
pause