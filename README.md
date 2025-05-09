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

7. Database Management:
```bash
# Clean all data from the database (preserves structure)
python manage.py clean_db
```

## Project Structure

- `softdesk/` - Main project directory
- `api/` - API application directory
- `users/` - User management application directory


## Testing with Postman

To test the API endpoints using Postman:

1. Download and install [Postman](https://www.postman.com/downloads/) if you haven't already.

2. Import the Postman collection:
   - Open Postman
   - Click on "Import" button in the top left
   - Select the `postman_collection.json` file from the project root directory
   - Click "Import"

3. The collection will be imported with all the necessary endpoints and example requests.

4. Before making requests, make sure the development server is running (`python manage.py runserver`).

5. For authenticated endpoints, you'll need to:
   - First login using the `/api/token/` endpoint
   - The token will be set to the `token` global variable to be used in the requests in the "Authorization" tab with the format: `Bearer your_access_token` 