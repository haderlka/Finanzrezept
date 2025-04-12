# finanzrezept - German Personal Finance Manager

A Django-based personal finance management system designed specifically for the German market.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Apply database migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to access the application.

## Development

This project uses:
- Django 5.0.2
- Bootstrap 5 for frontend
- PostgreSQL for database (recommended) 