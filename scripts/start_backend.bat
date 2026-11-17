@echo off
title CropScan Backend
cd /d "%~dp0..\webapp\backend"
echo.
echo  CropScan backend starting...
echo  Visit: http://localhost:8000/health
echo.
"%~dp0..\.venv\Scripts\python.exe" -m uvicorn main:app --reload
pause
