#!/usr/bin/env python3
"""
System integration test for ConvoSearch
"""
import sys
import os
import asyncio
import requests
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_services_health():
    """Test if all services are running and healthy"""
    print("Testing service health...")

    services = {
        "API": "http://localhost:8000/health",
        "ChromaDB": "http://localhost:8001/api/v1/heartbeat"
    }

    all_healthy = True
    for service, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service}: Healthy")
            else:
                print(f"❌ {service}: HTTP {response.status_code}")
                all_healthy = False
        except Exception as e:
            print(f"❌ {service}: Cannot connect - {e}")
            all_healthy = False

    return all_healthy


def test_api_endpoints():
    """Test key API endpoints"""
    print("\nTesting API endpoints...")

    base_url = "http://localhost:8000"
    tests = [
        ("GET", "/health", None),
        ("POST", "/api/query", {"question": "test question", "collection": "faq"}),
        ("POST", "/api/triage", {"message": "test message"}),
        ("GET", "/api/tickets", None)
    ]

    all_passed = True
    for method, endpoint, data in tests:
        try:
            url = base_url + endpoint
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, json=data, timeout=10)

            if response.status_code in [200, 201]:
                print(f"✅ {endpoint}: HTTP {response.status_code}")
            else:
                print(f"❌ {endpoint}: HTTP {response.status_code}")
                all_passed = False

        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")
            all_passed = False

    return all_passed


def test_web_interface():
    """Test web interface endpoints"""
    print("\nTesting web interface...")

    base_url = "http://localhost:8000"
    endpoints = ["/", "/chat", "/triage"]

    all_passed = True
    for endpoint in endpoints:
        try:
            response = requests.get(base_url + endpoint, timeout=10)
            if response.status_code == 200:
                print(f"✅ {endpoint}: HTTP {response.status_code}")
            else:
                print(f"❌ {endpoint}: HTTP {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")
            all_passed = False

    return all_passed


def main():
    print("🚀 ConvoSearch System Integration Test")
    print("=" * 50)

    # Wait a bit for services to start
    print("Waiting for services to start...")
    time.sleep(10)

    # Run tests
    health_ok = test_services_health()
    api_ok = test_api_endpoints()
    web_ok = test_web_interface()

    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"Services Health: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"API Endpoints: {'✅ PASS' if api_ok else '❌ FAIL'}")
    print(f"Web Interface: {'✅ PASS' if web_ok else '❌ FAIL'}")

    if all([health_ok, api_ok, web_ok]):
        print("\n🎉 ALL TESTS PASSED! ConvoSearch is working correctly.")
        print("\n🌐 Access your application at: http://localhost:8000")
    else:
        print("\n❌ SOME TESTS FAILED. Please check the logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main()