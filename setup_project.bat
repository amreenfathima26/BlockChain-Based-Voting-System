@echo off
echo ==========================================
echo SECURE VOTE PROJECT SETUP
echo ==========================================

echo [1/4] Checking Python Installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.10+ and tick "Add to PATH".
    pause
    exit /b
)
echo Python found.

echo [2/4] Creating Virtual Environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo [3/4] Installing Dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

echo [4/4] Setting up Database...
python manage.py migrate

echo ==========================================
echo SETUP COMPLETE!
echo You can now run 'start_server.bat' to launch the application.
echo ==========================================
pause
