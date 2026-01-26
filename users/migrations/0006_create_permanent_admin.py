from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_admin_user(apps, schema_editor):
    # Use the model from the apps registry to ensure compatibility
    User = apps.get_model('users', 'User')
    Profile = apps.get_model('users', 'Profile')
    
    email = 'admin@gmail.com'
    if not User.objects.filter(email=email).exists():
        admin = User.objects.create(
            email=email,
            username='admin_permanent',
            password=make_password('admin123'),
            is_staff=True,
            is_superuser=True,
            first_name='Admin',
            last_name='User',
            is_active=True,
            is_veteran=True
        )
        # Ensure a profile is created for the admin
        Profile.objects.get_or_create(user=admin)
        print(f"Permanent Admin {email} created successfully.")

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_star_giver_alter_star_unique_together'),
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]
