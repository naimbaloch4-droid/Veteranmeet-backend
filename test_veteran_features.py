import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_veteran_features():
    # First, login to get token
    login_data = {
        'email': 'admin@example.com',
        'password': 'admin123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
        if response.status_code == 200:
            token = response.json()['access']
            headers = {'Authorization': f'Bearer {token}'}
            print("✓ Login successful")
        else:
            print("✗ Login failed")
            return
    except:
        print("✗ Server not running or login endpoint not available")
        return

    # Test Veteran Hub
    print("\n=== VETERAN HUB TESTS ===")
    try:
        response = requests.get(f'{BASE_URL}/hub/dashboard/', headers=headers)
        print(f"Dashboard: {response.status_code}")
        
        response = requests.get(f'{BASE_URL}/hub/stats/', headers=headers)
        print(f"User Stats: {response.status_code}")
        
        response = requests.get(f'{BASE_URL}/hub/announcements/', headers=headers)
        print(f"Announcements: {response.status_code}")
    except Exception as e:
        print(f"✗ Hub tests failed: {e}")

    # Test Chat
    print("\n=== CHAT TESTS ===")
    try:
        response = requests.get(f'{BASE_URL}/chat/rooms/', headers=headers)
        print(f"Chat Rooms: {response.status_code}")
        
        response = requests.get(f'{BASE_URL}/chat/messages/', headers=headers)
        print(f"Chat Messages: {response.status_code}")
    except Exception as e:
        print(f"✗ Chat tests failed: {e}")

    # Test Support Groups
    print("\n=== SUPPORT GROUPS TESTS ===")
    try:
        # Create a support group
        group_data = {
            'name': 'PTSD Support',
            'description': 'Support group for veterans dealing with PTSD',
            'topic': 'Mental Health',
            'privacy_level': 'public'
        }
        response = requests.post(f'{BASE_URL}/support-groups/groups/', json=group_data, headers=headers)
        print(f"Create Group: {response.status_code}")
        
        response = requests.get(f'{BASE_URL}/support-groups/groups/', headers=headers)
        print(f"List Groups: {response.status_code}")
    except Exception as e:
        print(f"✗ Support Groups tests failed: {e}")

    # Test Resources
    print("\n=== RESOURCES TESTS ===")
    try:
        response = requests.get(f'{BASE_URL}/resources/categories/', headers=headers)
        print(f"Resource Categories: {response.status_code}")
        
        response = requests.get(f'{BASE_URL}/resources/resources/', headers=headers)
        print(f"Resources: {response.status_code}")
        
        # Create a resource
        if response.status_code == 200:
            categories = requests.get(f'{BASE_URL}/resources/categories/', headers=headers).json()
            if categories:
                resource_data = {
                    'title': 'VA Medical Center',
                    'description': 'Full-service medical center for veterans',
                    'url': 'https://www.va.gov',
                    'location': 'Washington, DC',
                    'category': categories[0]['id']
                }
                response = requests.post(f'{BASE_URL}/resources/resources/', json=resource_data, headers=headers)
                print(f"Create Resource: {response.status_code}")
    except Exception as e:
        print(f"✗ Resources tests failed: {e}")

    print("\n=== ALL TESTS COMPLETED ===")

if __name__ == '__main__':
    test_veteran_features()