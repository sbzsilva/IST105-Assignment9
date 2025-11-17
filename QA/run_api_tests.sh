#!/bin/bash

# API Test Runner Script
# This script starts the Django development server and runs the API tests

echo "🚀 Starting API Test Procedure"
echo "============================"

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the project root directory."
    exit 1
fi

# Check if required packages are installed
echo "🔍 Checking dependencies..."
if ! python3 -c "import django" 2>/dev/null; then
    echo " Django not found. Installing requirements..."
    pip install -r requirements.txt
fi

# Start Django development server in the background
echo "🔧 Starting Django development server..."
python3 manage.py runserver 8000 &
DJANGO_PID=$!

# Give Django some time to start
echo "⏳ Waiting for server to start..."
sleep 10

# Check if server is running
if ! curl -s http://localhost:8000 >/dev/null; then
    echo "❌ Error: Django server failed to start"
    kill $DJANGO_PID 2>/dev/null
    exit 1
fi

echo "✅ Django server is running"

# Run the API tests
echo "🧪 Running API tests..."
python3 test_api.py

# Capture test results
TEST_RESULT=$?

# Stop Django server
echo "🛑 Stopping Django server..."
kill $DJANGO_PID

# Wait a moment for the process to terminate
sleep 2

# Show final result
echo ""
echo "🏁 Test Procedure Complete"
echo "=========================="
if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ All tests completed successfully"
else
    echo "❌ Some tests failed"
fi

exit $TEST_RESULT