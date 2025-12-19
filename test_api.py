#!/usr/bin/env python
import requests
import json
from datetime import datetime, timedelta

BASE_URL = 'http://127.0.0.1:8000/api'

def test_api():
    """Test all API endpoints"""
    print("Testing VeteranMeet API...")
    
    # Test user registration
    print("\n1. Testing user registration...")
    register_data = {
        'email': 'test@example.com',
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'testpass123',
        'password_confirm': 'testpass123',
        'is_veteran': True
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/register/', json=register_data)
        if response.status_code == 201:
            print("[OK] Registration successful")
            tokens = response.json()
            access_token = tokens['access']
            headers = {'Authorization': f'Bearer {access_token}'}
        else:
            print(f"[ERROR] Registration failed: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to server. Make sure Django server is running on port 8000")
        return
    
    # Test login
    print("\n2. Testing login...")
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    
    response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
    if response.status_code == 200:
        print("[OK] Login successful")
    else:
        print(f"[ERROR] Login failed: {response.text}")
    
    # Test profile
    print("\n3. Testing profile...")
    response = requests.get(f'{BASE_URL}/auth/profile/', headers=headers)
    if response.status_code == 200:
        print("[OK] Profile retrieved successfully")
    else:
        print(f"[ERROR] Profile retrieval failed: {response.text}")
    
    # Test creating an event
    print("\n4. Testing event creation...")
    event_data = {
        'title': 'Test Event',
        'description': 'A test event for veterans',
        'location': 'Test Location',
        'date_time': (datetime.now() + timedelta(days=7)).isoformat(),
        'max_participants': 20
    }
    
    response = requests.post(f'{BASE_URL}/events/', json=event_data, headers=headers)
    if response.status_code == 201:
        print("[OK] Event created successfully")
        event_id = response.json()['id']
    else:
        print(f"[ERROR] Event creation failed: {response.text}")
        event_id = None
    
    # Test creating a post
    print("\n5. Testing post creation...")
    post_data = {
        'content': 'This is a test post from the API test script!'
    }
    
    response = requests.post(f'{BASE_URL}/posts/', json=post_data, headers=headers)
    if response.status_code == 201:
        print("[OK] Post created successfully")
        post_id = response.json()['id']
    else:
        print(f"[ERROR] Post creation failed: {response.text}")
        post_id = None
    
    # Test getting notifications
    print("\n6. Testing notifications...")
    response = requests.get(f'{BASE_URL}/notifications/', headers=headers)
    if response.status_code == 200:
        print("[OK] Notifications retrieved successfully")
    else:
        print(f"[ERROR] Notifications retrieval failed: {response.text}")
    
    print("\n[OK] API testing completed!")
    print("\nAvailable endpoints:")
    print("- POST /api/auth/register/ - User registration")
    print("- POST /api/auth/login/ - User login")
    print("- GET/PUT /api/auth/profile/ - User profile")
    print("- GET /api/auth/users/ - List users")
    print("- GET/POST /api/events/ - Events")
    print("- GET/POST /api/posts/ - Posts")
    print("- GET /api/notifications/ - Notifications")

if __name__ == '__main__':
    test_api()