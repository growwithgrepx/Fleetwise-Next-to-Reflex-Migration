@echo off
setlocal enabledelayedexpansion

if not exist "logs" mkdir logs

set LOGFILE=logs\start.log
set BACKEND_LOG=logs\backend.log
set REFLEX_LOG=logs\reflex.log

type nul > %LOGFILE%
type nul > %BACKEND_LOG%
type nul > %REFLEX_LOG%

echo [%date% %time%] Starting Fleetwise Application >> %LOGFILE%
echo.
echo Starting Fleetwise Application
echo.

echo [1/6] Verifying prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed
    pause
    exit /b 1
)
echo [OK] Python installed

echo.
echo [2/6] Cleaning ports...
for %%P in (3000 8000 8001) do (
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%P ^| findstr LISTENING 2^>nul') do (
        taskkill /F /PID %%a >nul 2>&1
    )
)
taskkill /F /IM reflex.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
echo [OK] Ports cleaned

echo.
echo [3/6] Verifying port availability...
timeout /t 3 /nobreak >nul
set PORT_ERROR=0
for %%P in (3000 8000 8001) do (
    netstat -an | findstr :%%P | findstr LISTENING >nul 2>&1
    if not errorlevel 1 set PORT_ERROR=1
)
if %PORT_ERROR%==1 (
    echo [ERROR] Ports still occupied
    pause
    exit /b 1
)
echo [OK] All ports available

echo.
echo [4/6] Starting Flask backend (port 8000)...
start "Fleetwise-Backend" /MIN cmd /c "python backend\app.py > %BACKEND_LOG% 2>&1"
timeout /t 5 /nobreak >nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo %%a > logs\backend.pid
    echo [OK] Backend running (PID: %%a)
    goto backend_done
)
echo [ERROR] Backend failed to start
pause
exit /b 1
:backend_done

echo.
echo [5/6] Starting Reflex frontend (ports 3000, 8001)...
start "Fleetwise-Frontend" /MIN cmd /c "reflex run > %REFLEX_LOG% 2>&1"
timeout /t 20 /nobreak >nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    echo %%a > logs\reflex.pid
    echo [OK] Frontend running (PID: %%a)
    goto frontend_done
)
echo [ERROR] Frontend failed to start
pause
exit /b 1
:frontend_done

echo.
echo [6/6] Startup complete!
echo.
echo Fleetwise is READY!
echo.
echo   Backend API:     http://127.0.0.1:8000
echo   Reflex Backend:  http://127.0.0.1:8001  
echo   Frontend UI:     http://localhost:3000
echo.
echo   Login: admin@fleetwise.com / admin123
echo.
echo Management:
echo   scripts\stop.bat    - Stop all services
echo   scripts\restart.bat - Restart services
echo   scripts\logs.bat    - Tail logs
echo.

choice /C YN /M "Open browser now" /T 5 /D Y >nul 2>&1
if errorlevel 1 start http://localhost:3000

echo.
pause