from django.core.management.base import BaseCommand
from django.db import connection
from api.models import Comment, Issue, Contributor, Project
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Cleans all data from the database while preserving the structure'

    def handle(self, *args, **options):
        self.stdout.write('Cleaning database...')
        
        # Define models in order of deletion (respecting foreign key dependencies)
        models_to_clean = [
            Comment,    # Depends on Issue and Contributor
            Issue,      # Depends on Project and Contributor
            Contributor, # Depends on Project and User
            Project,    # Depends on User
            User        # Base model
        ]
        
        # Disable foreign key checks temporarily for SQLite
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys = OFF;')
            
            # Delete all data from each model
            for model in models_to_clean:
                try:
                    model.objects.all().delete()
                    self.stdout.write(f'Cleaned {model.__name__} table')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Could not clean {model.__name__}: {str(e)}'))
            
            # Re-enable foreign key checks
            cursor.execute('PRAGMA foreign_keys = ON;')
        
        self.stdout.write(self.style.SUCCESS('Database cleaned successfully!')) 