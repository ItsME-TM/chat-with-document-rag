@echo off
title AI Document Hub Launcher

echo Starting AI Document Q&A System...
echo.

:: 1. Start Python AI Service
echo [1/3] Starting Python AI Service on port 8000...
start "Python AI Service" cmd /k "cd ai-service && uvicorn main:app --reload --port 8000"

:: 2. Start .NET API Service
echo [2/3] Starting .NET API Service on port 5000...
start ".NET API Service" cmd /k "cd dotnet-api && dotnet run"

:: 3. Start Frontend Web Server
echo [3/3] Starting Frontend Web Server on port 3000...
start "Frontend Web Server" cmd /k "cd frontend && python -m http.server 3000"

echo.
echo All services are starting in separate windows.
echo Frontend: http://localhost:3000
echo.
pause