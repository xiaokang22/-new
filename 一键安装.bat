@echo off
chcp 65001 >nul
echo ================================
echo   ?????????? - ????
echo ================================
echo.

:: ??????? Git
echo [1/6] ?? Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ???? Git...
    curl -o git-installer.exe https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.1/Git-2.45.2-64-bit.exe
    git-installer.exe /VERYSILENT /NORESTART
    del git-installer.exe
    echo Git ????
    set PATH=%PATH%;C:\Program Files\Git\bin
) else (
    echo Git ??????
)

:: ?? Python
echo [2/6] ?? Python...
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
echo [3/6] ?? Node.js...
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

:: ????
echo [4/6] ????...
if exist "C:\Users\user\Desktop\loubang-project" (
    echo ????????????
) else (
    cd /d C:\Users\user\Desktop
    git clone https://github.com/xiaokang22/-new.git loubang-project
)

:: ??????
echo [5/6] ??????...
cd /d C:\Users\user\Desktop\loubang-project\backend
python -m venv venv
.\venv\Scripts\pip.exe install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

:: ??????
echo [6/6] ??????...
cd /d C:\Users\user\Desktop\loubang-project\frontend
call npm install

:: ??
echo.
echo ================================
echo   ???????
echo   ??"??.bat"????
echo ================================
pause
