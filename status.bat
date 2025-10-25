@echo off
REM =============================================================================
REM Fleetwise - Service Status Check Script (Windows)
REM =============================================================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   Fleetwise Service Status
echo ========================================
echo.

REM Check Backend (Port 8000)
echo [Backend API - Port 8000]
netstat -an | findstr :8000 | findstr LISTENING >nul 2>&1
if %ERRORLEVEL%==0 (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
        echo   [*] Running (PID: %%a^)
        if exist logs\backend.pid (
            set /p SAVED_PID=<logs\backend.pid
            if "%%a"=="!SAVED_PID!" (
                echo   [*] PID matches saved PID
            ) else (
                echo   [!] PID mismatch (saved: !SAVED_PID!, actual: %%a^)
            )
        )
        goto backend_done
    )
) else (
    echo   [X] Not running
)
:backend_done

echo.

REM Check Reflex Backend (Port 8001)
echo [Reflex Backend - Port 8001]
netstat -an | findstr :8001 | findstr LISTENING >nul 2>&1
if %ERRORLEVEL%==0 (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001 ^| findstr LISTENING') do (
        echo   [*] Running (PID: %%a^)
        goto reflex_backend_done
    )
) else (
    echo   [X] Not running
)
:reflex_backend_done

echo.

REM Check Frontend (Port 3000)
echo [Frontend UI - Port 3000]
netstat -an | findstr :3000 | findstr LISTENING >nul 2>&1
if %ERRORLEVEL%==0 (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
        echo   [*] Running (PID: %%a^)
        if exist logs\reflex.pid (
            set /p SAVED_PID=<logs\reflex.pid
            if "%%a"=="!SAVED_PID!" (
                echo   [*] PID matches saved PID
            ) else (
                echo   [!] PID mismatch (saved: !SAVED_PID!, actual: %%a^)
            )
        )
        goto frontend_done
    )
) else (
    echo   [X] Not running
)
:frontend_done

echo.

REM Overall Status
echo ========================================
set BACKEND_OK=0
set FRONTEND_OK=0

netstat -an | findstr :8000 | findstr LISTENING >nul 2>&1
if %ERRORLEVEL%==0 set BACKEND_OK=1

netstat -an | findstr :3000 | findstr LISTENING >nul 2>&1
if %ERRORLEVEL%==0 set FRONTEND_OK=1

if %BACKEND_OK%==1 if %FRONTEND_OK%==1 (
    echo [*] All services running
    echo.
    echo Access URLs:
    echo   Backend:  http://127.0.0.1:8000
    echo   Frontend: http://localhost:3000
) else if %BACKEND_OK%==1 (
    echo [!] Backend running, but frontend is down
    echo   Start frontend: reflex run
) else if %FRONTEND_OK%==1 (
    echo [!] Frontend running, but backend is down
    echo   Start backend: python backend\app.py
) else (
    echo [X] No services running
    echo   Start all: start.bat
)

echo ========================================
echo.