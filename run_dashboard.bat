@echo off
echo Installing requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install requirements. Please check your internet connection or permissions.
    pause
    exit /b %errorlevel%
)

echo Running FastHTML dashboard...
python main.py
pause
