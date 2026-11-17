@echo off
title CropScan Frontend
cd /d "%~dp0..\webapp\frontend"
echo.
echo  Serving frontend at http://localhost:3000
echo  Open your browser to http://localhost:3000
echo.
"%~dp0..\.venv\Scripts\python.exe" -m http.server 3000
pause
