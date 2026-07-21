@echo off
chcp 65001 >nul
echo ================================
echo   ?????????? - ?????
echo ================================
echo.

:: ?? Python
echo [1/4] ?? Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [??] ??? Python????? Python 3.12
    echo ????: https://www.python.org/downloads/
    pause
    exit /b
)
echo Python ???

:: ?? Node.js
echo [2/4] ?? Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [??] ??? Node.js????? Node.js 20
    echo ????: https://nodejs.org/
    pause
    exit /b
)
echo Node.js ???

:: ??????
echo [3/4] ??????...
cd /d C:\Users\user\Desktop\loubang-project\backend
python -m venv venv
.\venv\Scripts\pip.exe install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

:: ??????
echo [4/4] ??????...
cd /d C:\Users\user\Desktop\loubang-project\frontend
call npm install

echo.
echo ================================
echo   ???????"??.bat"????
echo ================================
pause
