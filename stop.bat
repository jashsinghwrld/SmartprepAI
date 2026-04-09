@echo off
title SmartPrepAI Shutdown Controller
echo =========================================
echo   Stopping SmartPrepAI Local Services
echo =========================================
echo.
REM ---------------------------------------------------------
REM PHASE 4: STOP SYSTEM
REM ---------------------------------------------------------
echo WARNING: Due to Windows sub-process constraints, this script mass-kills processes by name.
echo This will aggressively close ALL actively running Python (.exe) and Node (.exe) backgrounds.
echo If you have unrelated Python or Node projects running right now, press CTRL+C to cancel.
echo.
pause

echo.
echo Killing backend processes (uvicorn/python.exe)...
taskkill /F /IM python.exe /T

echo.
echo Killing frontend processes (node.exe)...
taskkill /F /IM node.exe /T

echo.
echo -----------------------------------------
echo SmartPrepAI stopped
echo -----------------------------------------
pause
