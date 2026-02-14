@echo off
echo ========================================
echo SCM Supply Chain Management System
echo ========================================
echo.

echo Starting Backend Server...
start "SCM Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "SCM Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Services started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo ========================================
pause
