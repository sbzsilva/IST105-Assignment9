@echo off
REM API Test Runner Script for Windows
REM This script starts the Django development server and runs the API tests

echo 🚀 Starting API Test Procedure
echo ============================

REM Check if we're in the right directory
if not exist "manage.py" (
    echo ❌ Error: manage.py not found. Please run this script from the project root directory.
    exit /b 1
)

REM Check if required packages are installed
echo 🔍 Checking dependencies...
python -c "import django" 2>nul
if %errorlevel% neq 0 (
    echo Installing requirements...
    pip install -r requirements.txt
)

REM Start Django development server in the background
echo 🔧 Starting Django development server...
start "Django Server" /min cmd /c "python manage.py runserver 8000"
echo Waiting for server to start...

REM Give Django some time to start
timeout /t 10 /nobreak >nul

REM Check if server is running
curl -s http://localhost:8000 >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Django server failed to start
    exit /b 1
)

echo ✅ Django server is running

REM Run the API tests
echo 🧪 Running API tests...
python test_api.py

REM Capture test results
set TEST_RESULT=%errorlevel%

REM Show final result
echo.
echo 🏁 Test Procedure Complete
echo ==========================
if %TEST_RESULT% equ 0 (
    echo ✅ All tests completed successfully
) else (
    echo ❌ Some tests failed
)

exit /b %TEST_RESULT%