@echo off
echo Verifying Fleetwise Ports Configuration
echo =========================================
echo.

echo Expected Configuration:
echo   Port 3000: Frontend (React/Vite)
echo   Port 8001: Reflex Backend (WebSocket)
echo   Port 8000: Flask API (REST)
echo.

echo Port 3000 (Frontend):
netstat -ano | findstr :3000 | findstr LISTENING
if errorlevel 1 echo   Not listening
echo.

echo Port 8001 (Reflex Backend - WebSocket):
netstat -ano | findstr :8001 | findstr LISTENING
if errorlevel 1 echo   Not listening
echo.

echo Port 8000 (Flask API - REST):
netstat -ano | findstr :8000 | findstr LISTENING
if errorlevel 1 echo   Not listening
echo.

echo.
echo WebSocket Test:
echo   Expected: ws://127.0.0.1:8001/_event
echo   (NOT ws://127.0.0.1:8000/_event)
echo.

pause