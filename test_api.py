#!/usr/bin/env python3
"""
Simple API test script to verify the Django backend is working
"""

import requests
import json

BASE_URL = "http://localhost:5100"

def test_home():
    """Test the home endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Home endpoint: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Home endpoint failed: {e}")
        return False

def test_signup():
    """Test user signup"""
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "phone": "+1234567890",
        "role": "Employee",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/users/signup/", json=user_data)
        print(f"✅ Signup: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Signup failed: {e}")
        return False

def test_login():
    """Test user login"""
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/users/login/", json=login_data)
        if response.status_code == 200:
            token = response.json().get('token')
            print(f"✅ Login: {response.status_code} - Token received")
            return token
        else:
            print(f"❌ Login failed: {response.status_code} - {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return None

def test_protected_endpoint(token):
    """Test a protected endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/requests/", headers=headers)
        print(f"✅ Protected endpoint: {response.status_code} - {len(response.json().get('data', []))} requests")
        return True
    except Exception as e:
        print(f"❌ Protected endpoint failed: {e}")
        return False

def test_request_crud(token):
    """Test request CRUD operations"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a test request
    request_data = {
        "amount": 1500.00,
        "currency": "USD",
        "approver_id": "123e4567-e89b-12d3-a456-426614174000",  # Dummy UUID
        "purpose": "Test request for CRUD operations",
        "description": "Testing create, edit, and delete functionality"
    }
    
    try:
        # Create request
        response = requests.post(f"{BASE_URL}/api/requests/", json=request_data, headers=headers)
        if response.status_code == 201:
            request_id = response.json().get('id')
            print(f"✅ Request created: {request_id}")
            
            # Edit request (should work for pending requests)
            edit_data = {
                "amount": 2000.00,
                "purpose": "Updated test request"
            }
            response = requests.put(f"{BASE_URL}/api/requests/{request_id}/", json=edit_data, headers=headers)
            if response.status_code == 200:
                print("✅ Request edited successfully")
            else:
                print(f"⚠️ Request edit failed: {response.status_code}")
            
            # Delete request (should work for pending requests)
            response = requests.delete(f"{BASE_URL}/api/requests/{request_id}/", headers=headers)
            if response.status_code == 204:
                print("✅ Request deleted successfully")
            else:
                print(f"⚠️ Request delete failed: {response.status_code}")
                
        else:
            print(f"⚠️ Request creation failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request CRUD test failed: {e}")

def main():
    print("🧪 Testing Django API endpoints")
    print("=" * 40)
    
    # Test home
    if not test_home():
        print("❌ Basic connectivity failed. Is the server running?")
        return
    
    # Test signup
    test_signup()  # May fail if user already exists, that's ok
    
    # Test login
    token = test_login()
    if not token:
        print("❌ Authentication failed. Cannot test protected endpoints.")
        return
    
    # Test protected endpoint
    test_protected_endpoint(token)
    
    # Test request CRUD operations
    test_request_crud(token)
    
    print("\n🎉 API testing completed!")
    print("💡 Note: Some tests may fail if data already exists, which is normal.")

if __name__ == "__main__":
    main()