from django.core.management.base import BaseCommand
from resources.models import ResourceCategory

class Command(BaseCommand):
    help = 'Create initial resource categories'

    def handle(self, *args, **options):
        categories = [
            {'name': 'Healthcare', 'description': 'Medical services and healthcare resources for veterans'},
            {'name': 'Education', 'description': 'Educational benefits and learning opportunities'},
            {'name': 'Employment', 'description': 'Job opportunities and career services'},
            {'name': 'Benefits', 'description': 'VA benefits and compensation information'},
            {'name': 'Legal', 'description': 'Legal assistance and advocacy services'},
            {'name': 'Mental Health', 'description': 'Mental health support and counseling services'},
            {'name': 'Housing', 'description': 'Housing assistance and homeless prevention'},
            {'name': 'Financial', 'description': 'Financial assistance and planning services'},
        ]

        for category_data in categories:
            category, created = ResourceCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully created resource categories')
        )