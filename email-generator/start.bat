@echo off
REM Email Template Generator - Windows launcher
cd /d "%~dp0"
echo Starting Email Template Generator...
py server.py
if %errorlevel% neq 0 python server.py
echo.
echo Server stopped. You can close this window.
pause
