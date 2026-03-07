import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


ADMINS = [
    {
        'email':    os.environ.get('ADMIN_EMAIL',    'admin1@gmail.com'),
        'password': os.environ.get('ADMIN_PASSWORD', 'admin123'),
        'username': os.environ.get('ADMIN_USERNAME', 'admin1'),
    },
    {
        'email':    os.environ.get('ADMIN2_EMAIL',    'admin2@gmail.com'),
        'password': os.environ.get('ADMIN2_PASSWORD', 'admin123'),
        'username': os.environ.get('ADMIN2_USERNAME', 'admin2'),
    },
]


class Command(BaseCommand):
    help = 'Ensures all admin users are active superusers. Credentials read from env or use built-in defaults.'

    def handle(self, *args, **options):
        User = get_user_model()

        for admin in ADMINS:
            self._ensure(User, admin['email'], admin['password'], admin['username'])

    def _ensure(self, User, email, password, username):
        if not email or not password:
            self.stdout.write(self.style.WARNING(f'Skipping — no email/password for {username}'))
            return

        try:
            user = User.objects.get(email=email)
            changed = []

            if not user.is_active:
                user.is_active = True
                changed.append('is_active')
            if not user.is_staff:
                user.is_staff = True
                changed.append('is_staff')
            if not user.is_superuser:
                user.is_superuser = True
                changed.append('is_superuser')

            user.set_password(password)
            changed.append('password')

            user.save()

            if changed:
                self.stdout.write(self.style.SUCCESS(f'Admin "{email}" updated: {", ".join(changed)}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Admin "{email}" already healthy — no changes.'))

        except User.DoesNotExist:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Admin',
                last_name='User',
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser created: {email}'))
