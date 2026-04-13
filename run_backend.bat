@echo off
cd /d %~dp0
echo Starting Carbon Autonomous Backend...

:: Check if python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b
)

:: Run the server
echo Launching FastAPI server with Uvicorn...

set /p open_docs="Open API documentation in browser? (y/n): "
if /i "%open_docs%"=="y" start http://localhost:8000/docs
if /i "%open_docs%"=="yes" start http://localhost:8000/docs

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
