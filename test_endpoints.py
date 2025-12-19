import requests
import json
import time
from threading import Thread
import subprocess
import sys

def start_server():
    subprocess.run([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def test_api():
    base_url = 'http://127.0.0.1:8000'
    
    print('=== VeteranMeet API Testing ===\n')
    
    # Test API root
    print('1. Testing API Root...')
    try:
        response = requests.get(f'{base_url}/api/')
        print(f'   Status: {response.status_code}')
        if response.status_code == 200:
            print('   [OK] API Root accessible')
        else:
            print('   [FAIL] API Root failed')
    except Exception as e:
        print(f'   [ERROR] API Root error: {e}')
    
    # Test Swagger
    print('\n2. Testing Swagger UI...')
    try:
        response = requests.get(f'{base_url}/api/swagger/')
        print(f'   Status: {response.status_code}')
        if response.status_code == 200:
            print('   [OK] Swagger UI accessible')
        else:
            print('   [FAIL] Swagger UI failed')
    except Exception as e:
        print(f'   [ERROR] Swagger error: {e}')
    
    # Test user registration
    print('\n3. Testing User Registration...')
    try:
        user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'is_veteran': True
        }
        response = requests.post(f'{base_url}/api/auth/register/', json=user_data)
        print(f'   Status: {response.status_code}')
        if response.status_code in [200, 201]:
            print('   [OK] Registration successful')
        else:
            print(f'   [FAIL] Registration failed: {response.text[:100]}')
    except Exception as e:
        print(f'   [ERROR] Registration error: {e}')
    
    # Test user login
    print('\n4. Testing User Login...')
    access_token = None
    try:
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        response = requests.post(f'{base_url}/api/auth/login/', json=login_data)
        print(f'   Status: {response.status_code}')
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access')
            print('   [OK] Login successful, token obtained')
        else:
            print(f'   [FAIL] Login failed: {response.text[:100]}')
    except Exception as e:
        print(f'   [ERROR] Login error: {e}')
    
    if access_token:
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Test events endpoint
        print('\n5. Testing Events Endpoint...')
        try:
            response = requests.get(f'{base_url}/api/events/', headers=headers)
            print(f'   Status: {response.status_code}')
            if response.status_code == 200:
                print('   [OK] Events endpoint accessible')
            else:
                print('   [FAIL] Events endpoint failed')
        except Exception as e:
            print(f'   [ERROR] Events error: {e}')
        
        # Test posts endpoint
        print('\n6. Testing Posts Endpoint...')
        try:
            response = requests.get(f'{base_url}/api/posts/', headers=headers)
            print(f'   Status: {response.status_code}')
            if response.status_code == 200:
                print('   [OK] Posts endpoint accessible')
            else:
                print('   [FAIL] Posts endpoint failed')
        except Exception as e:
            print(f'   [ERROR] Posts error: {e}')
        
        # Test notifications endpoint
        print('\n7. Testing Notifications Endpoint...')
        try:
            response = requests.get(f'{base_url}/api/notifications/', headers=headers)
            print(f'   Status: {response.status_code}')
            if response.status_code == 200:
                print('   [OK] Notifications endpoint accessible')
            else:
                print('   [FAIL] Notifications endpoint failed')
        except Exception as e:
            print(f'   [ERROR] Notifications error: {e}')
    
    print('\n=== Testing Complete ===')

if __name__ == '__main__':
    # Start server in background
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    
    print('Starting Django server...')
    time.sleep(4)  # Wait for server to start
    
    test_api()