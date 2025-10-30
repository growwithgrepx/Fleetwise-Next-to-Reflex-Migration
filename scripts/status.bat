@echo off
setlocal enabledelayedexpansion

echo.
echo Fleetwise Service Status
echo ========================
echo.

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
                echo   [!] PID mismatch
            )
        )
        goto backend_done
    )
) else (
    echo   [X] Not running
)
:backend_done

echo.

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
                echo   [!] PID mismatch
            )
        )
        goto frontend_done
    )
) else (
    echo   [X] Not running
)
:frontend_done

echo.
echo ========================
set BACKEND_OK=0
set FRONTEND_OK=0

netstat -an | findstr :8000 | findstr LISTENING >nul 2>&1
if %ERRORLEVEL%==0 set BACKEND_OK=1

netstat -an | findstr :3000 | findstr LISTENING >nul 2>&1
if %ERRORLEVEL%==0 set FRONTEND_OK=1

if %BACKEND_OK%==1 if %FRONTEND_OK%==1 (
    echo [*] All services running
    echo.
    echo Access:
    echo   Backend:  http://127.0.0.1:8000
    echo   Frontend: http://localhost:3000
) else if %BACKEND_OK%==1 (
    echo [!] Backend running, but frontend is down
) else if %FRONTEND_OK%==1 (
    echo [!] Frontend running, but backend is down
) else (
    echo [X] No services running
    echo   Start: scripts\start.bat
)

echo ========================
echo.
pause