#!/usr/bin/env python3
"""
Test script to verify API documentation is working
"""

import requests
import webbrowser
import time

BASE_URL = "http://localhost:5100"

def test_documentation():
    """Test if documentation endpoints are accessible"""
    endpoints = {
        'Swagger UI': f"{BASE_URL}/api/docs/",
        'ReDoc': f"{BASE_URL}/api/redoc/",
        'OpenAPI Schema': f"{BASE_URL}/api/schema/"
    }
    
    print("🔍 Testing API Documentation Endpoints")
    print("=" * 50)
    
    for name, url in endpoints.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: {response.status_code} - Available at {url}")
            else:
                print(f"❌ {name}: {response.status_code} - Failed")
        except requests.exceptions.RequestException as e:
            print(f"❌ {name}: Connection failed - {e}")
    
    # Test home endpoint for documentation links
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            data = response.json()
            if 'documentation' in data:
                print(f"\n✅ Home endpoint includes documentation links:")
                for doc_type, path in data['documentation'].items():
                    print(f"   {doc_type}: {BASE_URL}{path}")
            else:
                print(f"\n❌ Home endpoint missing documentation links")
        else:
            print(f"\n❌ Home endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"\n❌ Home endpoint error: {e}")

def open_documentation():
    """Open documentation in browser"""
    print(f"\n🌐 Opening Swagger UI in browser...")
    try:
        webbrowser.open(f"{BASE_URL}/api/docs/")
        print("✅ Browser opened successfully")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")

def main():
    print("📚 API Documentation Tester")
    print("Make sure your Django server is running on port 5100")
    print()
    
    # Test endpoints
    test_documentation()
    
    # Ask if user wants to open browser
    print(f"\n🤔 Would you like to open the Swagger UI in your browser? (y/n): ", end="")
    if input().lower() == 'y':
        open_documentation()
    
    print(f"\n📖 Documentation URLs:")
    print(f"   Swagger UI: {BASE_URL}/api/docs/")
    print(f"   ReDoc:      {BASE_URL}/api/redoc/")
    print(f"   Schema:     {BASE_URL}/api/schema/")

if __name__ == "__main__":
    main()