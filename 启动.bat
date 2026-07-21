@echo off
chcp 65001 >nul
echo ================================
echo   ?????????? ???...
echo ================================
echo.

:: ????
echo [1/2] ??????...
cd /d C:\Users\user\Desktop\loubang-project\backend
start "????" cmd /k ".\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"

:: ??????
timeout /t 3 /nobreak >nul

:: ????
echo [2/2] ??????...
cd /d C:\Users\user\Desktop\loubang-project\frontend
start "????" cmd /k "npm run dev"

:: ??????
timeout /t 3 /nobreak >nul

echo.
echo ================================
echo   ?????
echo   ?????: http://127.0.0.1:3000
echo ================================
echo.
pause
