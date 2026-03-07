from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_admin_users(apps, schema_editor):
    User = apps.get_model('users', 'User')
    Profile = apps.get_model('users', 'Profile')

    admins = [
        {'email': 'admin1@gmail.com', 'username': 'admin1'},
        {'email': 'admin2@gmail.com', 'username': 'admin2'},
    ]

    for data in admins:
        if not User.objects.filter(email=data['email']).exists():
            user = User.objects.create(
                email=data['email'],
                username=data['username'],
                password=make_password('admin123'),
                is_staff=True,
                is_superuser=True,
                is_active=True,
                first_name='Admin',
                last_name='User',
                is_veteran=False,
            )
            Profile.objects.get_or_create(user=user)
            print(f"Admin created: {data['email']}")
        else:
            # Make sure existing user is active and a superuser
            user = User.objects.get(email=data['email'])
            updated = False
            if not user.is_active:
                user.is_active = True
                updated = True
            if not user.is_staff:
                user.is_staff = True
                updated = True
            if not user.is_superuser:
                user.is_superuser = True
                updated = True
            if updated:
                user.save()
                print(f"Admin updated: {data['email']}")
            else:
                print(f"Admin already exists and is healthy: {data['email']}")


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_options_alter_user_last_activity_and_more'),
    ]

    operations = [
        migrations.RunPython(create_admin_users, migrations.RunPython.noop),
    ]
