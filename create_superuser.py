import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softdesk.settings')
django.setup()

from users.models import User

# Create superuser
User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123',
    birth_date=datetime.strptime('1990-01-01', '%Y-%m-%d').date()
) 