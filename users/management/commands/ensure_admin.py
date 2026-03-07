import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Ensures the admin user is active, a superuser and staff. Reads ADMIN_EMAIL and ADMIN_PASSWORD from env.'

    def handle(self, *args, **options):
        User = get_user_model()

        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')

        if not admin_email:
            self.stdout.write(self.style.WARNING(
                'ADMIN_EMAIL env variable not set — skipping ensure_admin.'
            ))
            return

        try:
            user = User.objects.get(email=admin_email)
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

            if admin_password:
                user.set_password(admin_password)
                changed.append('password')

            if changed:
                user.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Admin user "{admin_email}" updated: {", ".join(changed)}'
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'Admin user "{admin_email}" is already active and healthy — no changes needed.'
                ))

        except User.DoesNotExist:
            # Create a brand new admin if one doesn't exist yet
            if not admin_password:
                self.stdout.write(self.style.ERROR(
                    f'No user found with email "{admin_email}" and ADMIN_PASSWORD is not set — cannot create admin.'
                ))
                return

            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                first_name='Admin',
                last_name='User',
            )
            self.stdout.write(self.style.SUCCESS(
                f'Superuser created: {admin_email}'
            ))
