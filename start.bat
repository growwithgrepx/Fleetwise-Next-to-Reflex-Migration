@echo off
REM Fleetwise Startup Script for Windows

echo ========================================
echo   Starting Fleetwise Application
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "backend\app.py" (
    echo Error: backend\app.py not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

if not exist "app\app.py" (
    echo Error: app\app.py not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Start Flask backend in a new window
echo Starting Flask backend on port 8000...
start "Fleetwise Backend" cmd /k "python -m backend.app"

REM Wait for backend to initialize
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Test if backend is running
curl -s http://127.0.0.1:8000/health >nul 2>&1
if errorlevel 1 (
    echo Warning: Backend may not have started correctly
    echo Check the Backend window for errors
) else (
    echo Backend is running on http://127.0.0.1:8000
)

REM Start Reflex frontend in a new window
echo.
echo Starting Reflex frontend on port 3000...
start "Fleetwise Frontend" cmd /k "reflex run"

REM Wait for frontend to compile
echo Waiting for frontend to compile...
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo   Fleetwise is starting!
echo ========================================
echo.
echo   Backend:  http://127.0.0.1:8000
echo   Frontend: http://localhost:3000
echo.
echo   Login credentials:
echo     Email:    admin@fleetwise.com
echo     Password: admin123
echo.
echo   Two command windows have been opened:
echo     1. Fleetwise Backend (Flask)
echo     2. Fleetwise Frontend (Reflex)
echo.
echo   Close those windows to stop the servers
echo.
echo Press any key to open the app in your browser...
pause >nul

REM Open browser
start http://localhost:3000

echo.
echo Browser opened. You can close this window now.
pause