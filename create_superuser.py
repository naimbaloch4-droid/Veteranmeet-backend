import os
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veteranmeet.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def create_or_fix_superuser():
    email = 'admin@gmail.com'
    username = 'admin_main'
    password = 'admin123'
    
    # Try to find user by email OR username
    user = User.objects.filter(email=email).first() or User.objects.filter(username=username).first()
    
    if user:
        print(f"DEBUG: Found existing user {user.email}. Fixing permissions...")
        user.email = email
        user.username = username
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        print(f"SUCCESS: Admin account fixed. Log in with {email} / {password}")
    else:
        print(f"DEBUG: Creating brand new superuser {email}...")
        try:
            User.objects.create_superuser(
                email=email, 
                password=password,
                username=username,
                first_name='Admin',
                last_name='User'
            )
            print(f"SUCCESS: New superuser created. Log in with {email} / {password}")
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")

if __name__ == '__main__':
    create_or_fix_superuser()
