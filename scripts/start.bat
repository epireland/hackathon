@echo off
REM Quick start script for Power & Gas Trader Shift Handover System

echo ========================================
echo Power & Gas Trader Shift Handover System
echo ========================================
echo.

REM Check if .venv exists
if not exist ".venv\" (
    echo Virtual environment not found. Creating with uv...
    uv venv
    echo.
)

REM Install/upgrade dependencies using uv with the virtual environment
echo Installing dependencies with uv...
uv pip install --python .venv -e ".[dev]"
echo.

REM Run the application
echo Starting Streamlit application...
echo The application will open in your default browser.
echo Press Ctrl+C to stop the server.
echo.

REM Run with full path to Python executable
C:\SB\D_DRIVE\SB_MICROHACK\hackathon\.venv\Scripts\python.exe -m streamlit run app.py
