import os
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veteranmeet.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    email = 'admin@gmail.com'
    password = 'admin123'
    
    user = User.objects.filter(email=email).first()
    if user:
        print(f"DEBUG: Found existing user {email}. Updating permissions...")
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        print(f"DEBUG: Status for {email} -> is_staff: {user.is_staff}, is_superuser: {user.is_superuser}, is_active: {user.is_active}")
        print(f"Superuser {email} reset to password 'admin123'.")
        return
    
    try:
        print(f"DEBUG: Creating new superuser {email}...")
        User.objects.create_superuser(
            email=email, 
            password=password,
            username='admin_main',
            first_name='Admin',
            last_name='User'
        )
        print(f"Superuser {email} created successfully.")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == '__main__':
    create_superuser()
