@echo off
chcp 65001 >nul
echo ================================
echo   ?????????? - ?????
echo ================================
echo.

:: ?? Python
echo [1/5] ?? Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ???? Python 3.12...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
    echo Python ????
) else (
    echo Python ??????
)

:: ?? Node.js
echo [2/5] ?? Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ???? Node.js 20...
    curl -o node-installer.msi https://nodejs.org/dist/v20.18.0/node-v20.18.0-x64.msi
    msiexec /i node-installer.msi /quiet
    del node-installer.msi
    echo Node.js ????
) else (
    echo Node.js ??????
)

:: ????????
echo ????????...
timeout /t 5 /nobreak >nul

:: ??????
echo [3/5] ????????...
cd /d C:\Users\user\Desktop\loubang-project\backend
python -m venv venv
echo ????????????????...
.\venv\Scripts\pip.exe install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

:: ??????
echo [4/5] ??????...
cd /d C:\Users\user\Desktop\loubang-project\frontend
call npm install

:: ??
echo [5/5] ?????
echo.
echo ================================
echo   ?????
echo   ??"??.bat"????
echo ================================
pause
