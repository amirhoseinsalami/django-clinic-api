# Django Clinic API

A clinic management REST API built with Django and Django REST
Framework.

This project provides a backend system for managing patients, doctors,
appointments, payments, and reviews with authentication, role-based
permissions, database relationships, and API development best practices.

## Features

### Authentication & Users

-   Custom User model
-   JWT authentication
-   Access and refresh tokens
-   Patient, Doctor, and Admin roles
-   User profile management

### Doctors Management

-   Doctor profiles
-   Doctor specialities
-   Doctor listing and details
-   Doctor rating aggregation

### Appointment System

-   Create appointments
-   View appointments
-   Cancel appointments
-   Ownership permissions
-   Appointment time validation
-   Business rules for doctor and patient relationships

### Payment System

-   Payment model
-   Payment status management
-   Gateway callback structure

### Review System

-   Doctor reviews
-   Rating system
-   Appointment-based reviews

## Technology Stack

-   Python
-   Django
-   Django REST Framework
-   Simple JWT
-   PostgreSQL
-   SQLite (development)
-   Pytest
-   Docker
-   Docker Compose

Planned: - Gunicorn - Nginx - Redis - Celery - GitHub Actions CI/CD

## Project Structure

    clinic_backend/
    ├── accounts/
    ├── doctors/
    ├── appointments/
    ├── payments/
    ├── reviews/
    ├── common/
    ├── config/
    ├── Dockerfile
    ├── docker-compose.yml
    ├── docker-compose.prod.yml
    ├── nginx.conf
    ├── requirements.txt
    └── manage.py

## Installation

Clone the repository:

``` bash
git clone https://github.com/amirhoseinsalami/django-clinic-api.git
cd django-clinic-api
```

Create environment:

``` bash
python -m venv venv
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Create `.env` file:

``` env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=clinic
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

Run migrations:

``` bash
python manage.py migrate
```

Run server:

``` bash
python manage.py runserver
```

## Docker

Build:

``` bash
docker compose build
```

Run:

``` bash
docker compose up
```

Migration:

``` bash
docker compose exec web python manage.py migrate
```

## Testing

Run:

``` bash
pytest
```

## API Documentation

Swagger documentation is available at:

http://127.0.0.1:8000/api/docs/

## Main API Endpoints

Authentication:

    POST /api/accounts/register/
    POST /api/login/
    POST /api/token/refresh/
    GET /api/accounts/me/

Doctors:

    GET /api/doctors/
    GET /api/doctors/{id}/

Appointments:

    GET /api/appointments/
    POST /api/appointments/
    POST /api/appointments/{id}/cancel/

## Optimization Concepts

Implemented concepts:

-   select_related()
-   prefetch_related()
-   annotate()
-   aggregate queries
-   database indexes
-   transaction handling

## Security

Implemented:

-   JWT authentication
-   Password hashing
-   Permission control
-   Environment variables
-   Django ORM protection against SQL injection

## Future Improvements

-   Swagger/OpenAPI documentation
-   Redis caching
-   Celery background tasks
-   Appointment reminders
-   SMS/email notifications
-   Payment gateway integration
-   CI/CD pipeline
-   Production deployment

## Author

Amirhossein Salami

GitHub: https://github.com/amirhoseinsalami
