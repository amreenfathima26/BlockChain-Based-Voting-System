@echo off
echo ==========================================
echo STARTING SECURE VOTE SERVER
echo ==========================================

if not exist venv (
    echo Virtual environment not found! Please run 'setup_project.bat' first.
    pause
    exit /b
)

call venv\Scripts\activate
echo Virtual environment activated.

echo Starting server...
python run_public.py runserver

pause
