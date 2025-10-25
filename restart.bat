@echo off
REM =============================================================================
REM Fleetwise - Restart Script with Port Cleanup (Windows)
REM =============================================================================

setlocal enabledelayedexpansion

REM Create logs directory
if not exist "logs" mkdir logs

REM Use fixed log name (overwrite previous run)
set LOGFILE=logs\restart.log
type nul > %LOGFILE%

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

REM Call stop.bat
if exist stop.bat (
    call stop.bat
) else (
    echo [ERROR] stop.bat not found
    pause
    exit /b 1
)

echo.
echo [%date% %time%] Phase 1 complete - services stopped >> %LOGFILE%

REM Wait and verify ports are free
echo Waiting 3 seconds before restart...
timeout /t 3 /nobreak >nul

REM Verify ports are free with retry
set MAX_RETRIES=3
set RETRY_COUNT=0
set PORTS_READY=0

:check_ports_loop
if %RETRY_COUNT% GEQ %MAX_RETRIES% goto ports_check_done

set PORTS_READY=1
for %%P in (3000 8000 8001) do (
    netstat -an | findstr :%%P | findstr LISTENING >nul 2>&1
    if not errorlevel 1 (
        echo [WARNING] Port %%P still in use (attempt %RETRY_COUNT%/%MAX_RETRIES%)
        echo [%date% %time%] WARNING: Port %%P still in use (retry %RETRY_COUNT%) >> %LOGFILE%
        set PORTS_READY=0
        
        REM Force kill process on this port
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
    echo [ERROR] Cannot restart - ports still occupied after %MAX_RETRIES% attempts
    echo [%date% %time%] Restart failed - ports blocked >> %LOGFILE%
    pause
    exit /b 1
)

echo [OK] All ports available

REM Phase 2: Startup
echo.
echo ========================================
echo   PHASE 2: Starting Services
echo ========================================
echo.
echo [%date% %time%] Phase 2: Starting services >> %LOGFILE%

REM Call start.bat
if exist start.bat (
    call start.bat
) else (
    echo [ERROR] start.bat not found
    pause
    exit /b 1
)

echo [%date% %time%] Phase 2 complete - services started >> %LOGFILE%

REM Final Status
echo.
echo ========================================
echo   Restart COMPLETE!
echo ========================================
echo.

echo [%date% %time%] ======================================== >> %LOGFILE%
echo [%date% %time%] Restart completed successfully >> %LOGFILE%
echo [%date% %time%] ======================================== >> %LOGFILE%

echo [INFO] Services restarted successfully
echo.
pause