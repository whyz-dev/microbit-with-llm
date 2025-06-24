@echo off
setlocal

set VENV_DIR=.venv

if not exist %VENV_DIR%\Scripts\activate.bat (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)
call %VENV_DIR%\Scripts\activate.bat

echo Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Running main.py...
python main.py

endlocal
pause
