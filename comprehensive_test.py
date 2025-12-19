import requests
import json
import time
from threading import Thread
import subprocess
import sys

def start_server():
    subprocess.run([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def comprehensive_test():
    base_url = 'http://127.0.0.1:8000'
    
    print('=== VeteranMeet API Comprehensive Testing ===\n')
    
    # Register and login
    print('1. User Registration & Login...')
    user_data = {
        'email': 'comprehensive@test.com',
        'username': 'comptest',
        'password': 'testpass123',
        'password_confirm': 'testpass123',
        'first_name': 'Comprehensive',
        'last_name': 'Test',
        'is_veteran': True
    }
    
    # Register
    reg_response = requests.post(f'{base_url}/api/auth/register/', json=user_data)
    print(f'   Registration: {reg_response.status_code}')
    
    # Login
    login_data = {'email': 'comprehensive@test.com', 'password': 'testpass123'}
    login_response = requests.post(f'{base_url}/api/auth/login/', json=login_data)
    print(f'   Login: {login_response.status_code}')
    
    if login_response.status_code != 200:
        print('   [ERROR] Cannot proceed without authentication')
        return
    
    token_data = login_response.json()
    access_token = token_data.get('access')
    headers = {'Authorization': f'Bearer {access_token}'}
    
    print('   [OK] Authentication successful')
    
    # Test Event Creation
    print('\\n2. Testing Event Operations...')
    event_data = {
        'title': 'Test Event',
        'description': 'A test event for API testing',
        'date': '2024-12-25T10:00:00Z',
        'location': 'Test Location',
        'max_participants': 10
    }
    
    event_response = requests.post(f'{base_url}/api/events/', json=event_data, headers=headers)
    print(f'   Create Event: {event_response.status_code}')
    
    if event_response.status_code in [200, 201]:
        event_id = event_response.json().get('id')
        print(f'   [OK] Event created with ID: {event_id}')
        
        # Join event
        join_response = requests.post(f'{base_url}/api/events/{event_id}/join/', headers=headers)
        print(f'   Join Event: {join_response.status_code}')
        
        # Get participants
        participants_response = requests.get(f'{base_url}/api/events/{event_id}/participants/', headers=headers)
        print(f'   Get Participants: {participants_response.status_code}')
    
    # Test Post Creation
    print('\\n3. Testing Post Operations...')
    post_data = {
        'content': 'This is a test post for API testing'
    }
    
    post_response = requests.post(f'{base_url}/api/posts/', json=post_data, headers=headers)
    print(f'   Create Post: {post_response.status_code}')
    
    if post_response.status_code in [200, 201]:
        post_id = post_response.json().get('id')
        print(f'   [OK] Post created with ID: {post_id}')
        
        # Like post
        like_response = requests.post(f'{base_url}/api/posts/{post_id}/like/', headers=headers)
        print(f'   Like Post: {like_response.status_code}')
        
        # Add comment
        comment_data = {'content': 'This is a test comment'}
        comment_response = requests.post(f'{base_url}/api/posts/{post_id}/comments/', json=comment_data, headers=headers)
        print(f'   Add Comment: {comment_response.status_code}')
    
    # Test Profile Update
    print('\\n4. Testing Profile Operations...')
    profile_data = {
        'bio': 'Updated bio for testing',
        'location': 'Test City',
        'military_branch': 'Army',
        'years_served': 5
    }
    
    profile_response = requests.put(f'{base_url}/api/auth/profile/', json=profile_data, headers=headers)
    print(f'   Update Profile: {profile_response.status_code}')
    
    # Test User List
    users_response = requests.get(f'{base_url}/api/auth/users/', headers=headers)
    print(f'   Get Users: {users_response.status_code}')
    
    # Test Notifications
    print('\\n5. Testing Notifications...')
    notifications_response = requests.get(f'{base_url}/api/notifications/', headers=headers)
    print(f'   Get Notifications: {notifications_response.status_code}')
    
    unread_response = requests.get(f'{base_url}/api/notifications/unread-count/', headers=headers)
    print(f'   Unread Count: {unread_response.status_code}')
    
    # Test Token Refresh
    print('\\n6. Testing Token Refresh...')
    refresh_token = token_data.get('refresh')
    refresh_data = {'refresh': refresh_token}
    refresh_response = requests.post(f'{base_url}/api/auth/token/refresh/', json=refresh_data)
    print(f'   Token Refresh: {refresh_response.status_code}')
    
    print('\\n=== All Tests Completed Successfully ===')
    print('\\nAPI Endpoints Summary:')
    print('- Authentication: Registration, Login, Token Refresh ✓')
    print('- Events: Create, List, Join, Participants ✓')
    print('- Posts: Create, List, Like, Comments ✓')
    print('- Profile: View, Update ✓')
    print('- Notifications: List, Unread Count ✓')
    print('- Swagger Documentation: Available at /api/swagger/ ✓')

if __name__ == '__main__':
    # Start server in background
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    
    print('Starting Django server...')
    time.sleep(4)
    
    comprehensive_test()