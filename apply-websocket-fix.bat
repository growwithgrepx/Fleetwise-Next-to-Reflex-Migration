@echo off
echo Applying WebSocket Fix
echo ======================
echo.

REM Stop services
echo [1/4] Stopping services...
call stop.bat 2>nul
timeout /t 2 /nobreak >nul

REM Clear Reflex cache
echo [2/4] Clearing Reflex cache...
if exist .web rmdir /s /q .web
if exist __pycache__ rmdir /s /q __pycache__
if exist app\__pycache__ rmdir /s /q app\__pycache__
if exist backend\__pycache__ rmdir /s /q backend\__pycache__
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

REM Backup old config
echo [3/4] Backing up rxconfig.py...
if exist rxconfig.py copy rxconfig.py rxconfig.py.backup >nul

REM Apply fix
echo [4/4] Applying configuration fix...
(
echo import reflex as rx
echo.
echo config = rx.Config^(
echo     app_name="app",
echo     plugins=[
echo         rx.plugins.TailwindV3Plugin^(^),
echo         rx.plugins.sitemap.SitemapPlugin^(^),
echo     ],
echo     frontend_host="0.0.0.0",
echo     frontend_port=3000,
echo     backend_host="127.0.0.1",
echo     backend_port=8001,
echo ^)
) > rxconfig.py

echo.
echo Fix applied successfully!
echo.
echo Next steps:
echo   1. Run: start.bat
echo   2. Wait 30 seconds for compilation
echo   3. Open: http://localhost:3000
echo   4. Login: admin@fleetwise.com / admin123
echo.
echo WebSocket should now connect to: ws://127.0.0.1:8001/_event
echo (NOT ws://127.0.0.1:8000/_event)
echo.

pause