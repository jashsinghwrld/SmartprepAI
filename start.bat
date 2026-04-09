@echo off
setlocal EnableDelayedExpansion
title SmartPrepAI Launcher

echo =========================================
echo   SmartPrepAI - Automated Initialization
echo =========================================
echo.

REM ---------------------------------------------------------
REM PHASE 5: PATH FIXES (Ensure accurate CWD regardless of launch method)
REM ---------------------------------------------------------
cd /d "%~dp0"

REM ---------------------------------------------------------
REM PHASE 6: FAILSAFE HANDLING (Python & Node checks)
REM ---------------------------------------------------------
echo [System Check] Validating dependencies...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to PATH. 
    echo Please install Python 3.10+ and try again.
    pause
    exit /b
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not added to PATH. 
    echo Please install Node.js and try again.
    pause
    exit /b
)
echo [System Check] Passed!
echo.

set "FRONTEND_PATH=%~dp0frontend"
echo Using frontend: !FRONTEND_PATH!
echo Using backend: %~dp0backend
echo.

REM ---------------------------------------------------------
REM PHASE 0: CLEANUP STALE PROCESSES
REM ---------------------------------------------------------
echo [Cleanup] Neutralizing any old frontend/backend processes...
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1

REM ---------------------------------------------------------
REM ZERO MANUAL SETUP: API KEY CHECK
REM ---------------------------------------------------------
if not exist "backend\.env" (
    echo GEMINI_API_KEY=your_gemini_key_here>backend\.env
)

findstr /C:"your_gemini_key_here" "backend\.env" >nul 2>&1
if %errorlevel% == 0 (
    echo ========================================================
    echo   GEMINI API KEY REQUIRED
    echo ========================================================
    echo The AI engine requires a Google Gemini API key to function.
    set /p API_KEY="Please paste your API key here (or press Enter to skip): "
    
    if not "!API_KEY!" == "" (
        echo GEMINI_API_KEY=!API_KEY!>backend\.env
        echo Key successfully saved to backend\.env!
    ) else (
        echo Skipping API config. Note: Generating AI questions will fail.
    )
    echo.
)

REM ---------------------------------------------------------
REM PHASE 1: BACKEND AUTOMATION
REM ---------------------------------------------------------
echo [1/3] Setting up Backend...
if not exist "backend" (
    echo [ERROR] 'backend' generic folder not found in %CD%.
    pause
    exit /b
)

cd backend

if not exist "venv\" (
    echo Creating isolated Python virtual environment...
    python -m venv venv
)

echo Activating environment and confirming dependencies...
call venv\Scripts\activate.bat
REM Install quietly to prevent cluttering the main launch terminal
pip install -r requirements.txt >nul 2>&1

netstat -ano | findstr :8000 >nul 2>&1
if %errorlevel% == 0 (
    echo [WARNING] Port 8000 is currently busy! The backend connection may fail.
)

echo Starting Backend Server...
start "SmartPrepAI Backend (FastAPI)" cmd /k "call venv\Scripts\activate.bat && uvicorn main:app --reload --port 8000"

cd ..

REM ---------------------------------------------------------
REM PHASE 3: SMART HANDLING
REM ---------------------------------------------------------
echo [2/3] Waiting for Backend to boot (4 seconds)...
timeout /t 4 /nobreak >nul

REM ---------------------------------------------------------
REM PHASE 2: FRONTEND AUTOMATION
REM ---------------------------------------------------------
echo [3/3] Setting up Frontend Framework...
if not exist "%~dp0frontend" (
    echo [ERROR] 'frontend' generic folder not found.
    pause
    exit /b
)

cd /d "%~dp0frontend"

if not exist "node_modules\" (
    echo Initializing workspace dependencies. This may take a minute...
    call npm install
)

echo Running frontend from /frontend
echo Ensure Vite launches seamlessly on Port 5173
start "SmartPrepAI Frontend (Vite)" /D "%~dp0frontend" cmd /k "npm run dev"

cd /d "%~dp0"
echo.

REM ---------------------------------------------------------
REM PHASE 3: SMART HANDLING (AUTO BROWSER)
REM ---------------------------------------------------------
echo =========================================
echo   SmartPrepAI initialization complete!
echo   Launching main application locally...
echo =========================================

REM Wait a tiny bit for vite to serve
timeout /t 2 /nobreak >nul
start http://localhost:5173

pause
