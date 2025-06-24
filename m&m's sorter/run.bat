@echo off
setlocal

set VENV_DIR=.venv

if not exist %VENV_DIR%\Scripts\activate.bat (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)
call %VENV_DIR%\Scripts\activate.bat

:: 4. pip 최신화 및 패키지 설치
echo Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: 5. 스크립트 실행 (main.py 등)
echo Running main.py...
python main.py

endlocal
pause
