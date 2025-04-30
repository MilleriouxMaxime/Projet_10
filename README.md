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
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

- `softdesk/` - Main project directory
- `api/` - API application directory
- `docs/` - Project documentation

## API Documentation

API documentation will be available at `/api/docs/` once the server is running. 