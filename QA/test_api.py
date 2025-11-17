#!/usr/bin/env python3
"""
API Test Script for DNA Center Cisco App

This script tests the main API endpoints of the Django application.
"""

import requests
import time
import os
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Configuration
BASE_URL = os.environ.get('APP_BASE_URL', 'http://localhost:8000')
HEADERS = {'User-Agent': 'API-Test-Script/1.0'}

def test_endpoint(url, method='GET', data=None, expected_status=200):
    """
    Test a specific endpoint
    
    Args:
        url (str): The endpoint URL to test
        method (str): HTTP method (GET, POST, etc.)
        data (dict): Data to send with POST requests
        expected_status (int): Expected HTTP status code
    
    Returns:
        dict: Test results
    """
    try:
        print(f"Testing {method} {url}...")
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=HEADERS, verify=False, timeout=30)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=HEADERS, data=data, verify=False, timeout=30)
        else:
            print(f"Unsupported method: {method}")
            return {'success': False, 'error': f'Unsupported method: {method}'}
        
        result = {
            'success': response.status_code == expected_status,
            'status_code': response.status_code,
            'expected_status': expected_status,
            'response_time': response.elapsed.total_seconds(),
            'content_type': response.headers.get('content-type', 'unknown')
        }
        
        if response.status_code != expected_status:
            result['error'] = f"Expected status {expected_status}, got {response.status_code}"
            print(f"  ❌ {result['error']}")
        else:
            print(f"  ✅ Success - Status: {response.status_code}, Time: {response.elapsed.total_seconds():.2f}s")
            
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Request failed: {str(e)}")
        return {'success': False, 'error': str(e)}
    except Exception as e:
        print(f"  ❌ Unexpected error: {str(e)}")
        return {'success': False, 'error': str(e)}

def main():
    """Main test function"""
    print("🧪 Starting API Tests for DNA Center Cisco App")
    print("=" * 50)
    
    # Test base URL accessibility
    print("\n1. Testing base URL accessibility:")
    results = []
    results.append(test_endpoint(f"{BASE_URL}/", expected_status=200))
    
    # Test authentication endpoint
    print("\n2. Testing authentication endpoint:")
    results.append(test_endpoint(f"{BASE_URL}/authenticate/", expected_status=200))
    
    # Wait a bit to avoid rate limiting
    time.sleep(2)
    
    # Test devices list endpoint
    print("\n3. Testing devices list endpoint:")
    results.append(test_endpoint(f"{BASE_URL}/devices/", expected_status=200))
    
    # Test interfaces form endpoint
    print("\n4. Testing interfaces form endpoint:")
    results.append(test_endpoint(f"{BASE_URL}/interfaces/", expected_status=200))
    
    # Test logs endpoint
    print("\n5. Testing logs endpoint:")
    results.append(test_endpoint(f"{BASE_URL}/logs/", expected_status=200))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for r in results if r.get('success', False))
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())