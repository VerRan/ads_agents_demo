#!/usr/bin/env python3
"""
Test script for the Ads Go Agent REST API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_comprehensive_analysis():
    """Test the comprehensive analysis endpoint"""
    print("\nTesting comprehensive analysis...")
    try:
        data = {
            "url": "https://www.kreadoai.com/",
            "analysis_type": "comprehensive",
            "language": "zh"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/analyze", json=data)
        print(f"Status: {response.status_code}")
        
        result = response.json()
        if result.get("status") == "success":
            print("✓ Comprehensive analysis successful")
            print(f"Analysis ID: {result['data'].get('analysis_id')}")
            return True
        else:
            print(f"✗ Analysis failed: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"Comprehensive analysis test failed: {e}")
        return False

def test_product_analysis():
    """Test the product analysis endpoint"""
    print("\nTesting product analysis...")
    try:
        data = {
            "query": "https://www.kreadoai.com/"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/analyze/product", json=data)
        print(f"Status: {response.status_code}")
        
        result = response.json()
        if result.get("status") == "success":
            print("✓ Product analysis successful")
            return True
        else:
            print(f"✗ Product analysis failed: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"Product analysis test failed: {e}")
        return False

def test_api_docs():
    """Test the API documentation endpoints"""
    print("\nTesting API documentation...")
    try:
        # Test JSON docs
        response = requests.get(f"{BASE_URL}/api/v1/docs")
        print(f"JSON Docs Status: {response.status_code}")
        
        result = response.json()
        json_success = "title" in result and "endpoints" in result
        
        # Test HTML docs
        html_response = requests.get(f"{BASE_URL}/docs")
        print(f"HTML Docs Status: {html_response.status_code}")
        
        html_success = html_response.status_code == 200 and "Ads Go Agent REST API" in html_response.text
        
        if json_success and html_success:
            print("✓ Both JSON and HTML API documentation accessible")
            print(f"  - JSON docs: {len(result.get('endpoints', {}))} endpoints documented")
            print(f"  - HTML docs: Interactive documentation available")
            return True
        else:
            print(f"✗ Documentation issues - JSON: {json_success}, HTML: {html_success}")
            return False
            
    except Exception as e:
        print(f"API docs test failed: {e}")
        return False

def test_batch_analysis():
    """Test the batch analysis endpoint"""
    print("\nTesting batch analysis...")
    try:
        data = {
            "urls": ["https://www.kreadoai.com/"],
            "analysis_types": ["product"]
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/analyze/batch", json=data)
        print(f"Status: {response.status_code}")
        
        result = response.json()
        if result.get("status") == "success":
            print("✓ Batch analysis successful")
            print(f"Total URLs processed: {result['data'].get('total_urls')}")
            return True
        else:
            print(f"✗ Batch analysis failed: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"Batch analysis test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Ads Go Agent REST API Test Suite")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("API Documentation", test_api_docs),
        ("Product Analysis", test_product_analysis),
        ("Batch Analysis", test_batch_analysis),
        # ("Comprehensive Analysis", test_comprehensive_analysis),  # This might take longer
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'=' * 20}")
        print(f"Running: {test_name}")
        print(f"{'=' * 20}")
        
        start_time = time.time()
        success = test_func()
        end_time = time.time()
        
        results.append({
            'name': test_name,
            'success': success,
            'duration': end_time - start_time
        })
        
        print(f"Duration: {end_time - start_time:.2f}s")
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    
    for result in results:
        status = "✓ PASS" if result['success'] else "✗ FAIL"
        print(f"{result['name']:<25} {status:<8} ({result['duration']:.2f}s)")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())