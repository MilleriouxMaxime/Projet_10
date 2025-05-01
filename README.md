# SoftDesk API

This is a Django REST Framework API project for SoftDesk.

## Setup Instructions

1. Install pipenv if you haven't already:
```bash
pip install pipenv
```

2. Install dependencies:
```bash
pipenv install
```

3. Activate the virtual environment:
```bash
pipenv shell
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
# Method 1: Using the provided script
python create_superuser.py

# Method 2: Using Django shell
python manage.py shell
>>> from users.models import User
>>> from datetime import datetime
>>> User.objects.create_superuser(
...     username='admin',
...     email='admin@example.com',
...     password='admin123',
...     birth_date=datetime.strptime('1990-01-01', '%Y-%m-%d').date()
... )
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

- `softdesk/` - Main project directory
- `api/` - API application directory
- `users/` - User management application directory
- `docs/` - Project documentation

## API Documentation

API documentation will be available at `/api/docs/` once the server is running. 