# API Testing Procedures

This document explains how to test the DNA Center Cisco application API endpoints.

## Prerequisites

1. Python 3.8 or higher
2. Required packages installed (`pip install -r requirements.txt`)
3. MongoDB running (can be installed using [install_mongodb.sh](file://c:\Users\ssilva\college\IST105-Assignment9\install_mongodb.sh))
4. Django development server

## Test Procedures

### 1. Automated API Tests

There are two automated test scripts available:

#### Basic API Test (`test_api.py`)

This script tests if the endpoints are accessible and return the expected HTTP status codes.

#### Comprehensive API Test (`test_api_comprehensive.py`)

This script tests the actual functionality of each endpoint by checking the content of the responses.

### 2. Running the Tests

#### Method 1: Using the Batch Script (Windows)

```cmd
run_api_tests.bat
```

This will:
1. Start the Django development server
2. Run the comprehensive API tests
3. Stop the server after testing

#### Method 2: Manual Testing

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. In another terminal, run either test script:
   ```bash
   # For basic tests
   python test_api.py
   
   # For comprehensive tests
   python test_api_comprehensive.py
   ```

### 3. Manual Browser Testing

You can also test the API endpoints manually by visiting these URLs in your browser:

1. Home page: http://localhost:8000/
2. Authentication: http://localhost:8000/authenticate/
3. Device list: http://localhost:8000/devices/
4. Interface form: http://localhost:8000/interfaces/
5. Logs: http://localhost:8000/logs/

### 4. Expected Results

All tests should pass when the application is working correctly. Some tests might show warnings for content checking but still pass if the pages load correctly.

## Troubleshooting

1. If tests fail with connection errors, make sure the Django server is running
2. If MongoDB tests fail, make sure MongoDB is installed and running
3. If authentication tests fail, check the DNA Center credentials in [dnac_config.py](file://c:\Users\ssilva\college\IST105-Assignment9\dna_center_cisco\dnac_config.py)

## Test Descriptions

### Index Page Test
- Verifies that the main page loads correctly

### Authentication Test
- Tests the authentication with DNA Center
- Should display either a token or an error message

### Device List Test
- Tests retrieving the list of network devices
- Connects to the DNA Center sandbox

### Interfaces Form Test
- Tests the interface to select a device for viewing interfaces

### Logs Test
- Tests the MongoDB integration by displaying logs
- Shows actions performed by the application

### Interfaces POST Test
- Tests submitting a device IP to retrieve interfaces
- Handles both valid and invalid IP addresses