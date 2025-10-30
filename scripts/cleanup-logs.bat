@echo off
setlocal enabledelayedexpansion

echo.
echo Fleetwise Log Cleanup
echo ====================
echo.

if not exist "logs" (
    echo [INFO] No logs directory found
    pause
    exit /b 0
)

echo [INFO] Removing logs older than 24 hours...

powershell -Command "Get-ChildItem -Path 'logs\*.log' | Where-Object { $_.LastWriteTime -lt (Get-Date).AddHours(-24) } | Remove-Item -Force"

echo [OK] Cleanup complete

set /a count=0
for %%f in (logs\*.log) do set /a count+=1

echo [INFO] Current log files: %count%

echo.
pause