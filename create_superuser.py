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
    
    if User.objects.filter(email=email).exists():
        print(f"Superuser with email {email} already exists.")
        return
    
    try:
        User.objects.create_superuser(email=email, password=password)
        print(f"Superuser {email} created successfully.")
    except Exception as e:
        print(f"Error creating superuser: {e}")

if __name__ == '__main__':
    create_superuser()
