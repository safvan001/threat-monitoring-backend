# Threat Monitoring & Alert Management Backend

## Project Overview

A Django REST Framework backend application for threat monitoring and alert management. The system ingests security events, automatically creates alerts for high-severity incidents, and provides role-based access control for managing alerts. The application uses JWT authentication, implements rate limiting, and includes comprehensive logging for critical operations.

## Tech Stack

- Backend: Python, Django
- API Framework: Django REST Framework (DRF)
- Authentication: JWT (SimpleJWT)
- Database: SQLite
- Filtering: django-filter
- Rate Limiting: DRF Throttling
- Logging: Python logging module
- Containerization: Docker & Docker Compose

## Features Implemented

### Core Features

- **Event Ingestion API**: Admin-only endpoint for creating security events with validation
- **Automatic Alert Creation**: Alerts are automatically generated for events with High (3) or Critical (4) severity
- **Alert Listing API**: Paginated endpoint to view all alerts with filtering capabilities
- **Alert Status Management**: Admin-only endpoint to update alert status (Open, Acknowledged, Resolved)
- **Input Validation**: Comprehensive validation using DRF serializers
- **SQL Injection Prevention**: All database operations use Django ORM
- **Permission Checks**: Role-based access control enforced at the view level

### Optional / Bonus Features

- **JWT Authentication**: Token-based authentication with access and refresh tokens
- **Rate Limiting**: Basic throttling using DRF throttling classes (20 requests/min for anonymous, 100 requests/min for authenticated users)
- **Logging**: Critical actions are logged:
  - Event creation
  - Automatic alert creation
  - Alert status updates
- **Docker Support**: Dockerfile and docker-compose.yml for containerized deployment
- **Deployment Documentation**: Simple deployment steps for AWS EC2

## User Roles & Access Control

The system implements two user roles:

- **Admin**: 
  - Can create events via the event ingestion API
  - Can view all alerts
  - Can update alert status

- **Analyst**: 
  - Can only view alerts (read-only access)

Users are created through Django Admin interface. There is no signup API endpoint.

## Setup Instructions (Local)

### Prerequisites

- Python 3.11 or higher
- pip

### Installation Steps

1. **Create a virtual environment**:
```bash
python -m venv venv
```

2. **Activate the virtual environment**:
   - On Windows: `venv\Scripts\activate`
   - On Linux/Mac: `source venv/bin/activate`

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Create environment file**:
   - Copy `.env.example` to `.env` (if available) or create a `.env` file with the following variables:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Run migrations**:
```bash
python manage.py migrate
```

6. **Create a superuser**:
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin user. You can also create regular users (Analysts) via Django Admin.

7. **Run the development server**:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## Authentication (JWT)

The application uses JWT (JSON Web Tokens) for authentication. All API endpoints (except token endpoints) require authentication.

### Obtaining Tokens

**Get Access Token**:
```bash
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

Response:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Refresh Access Token**:
```bash
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

### Using Tokens

Include the access token in the Authorization header for all authenticated requests:
```
Authorization: Bearer <access_token>
```

**Token Lifetime**:
- Access Token: 60 minutes
- Refresh Token: 1 day

## API Endpoints Summary

### Authentication
- `POST /api/token/` - Obtain JWT access and refresh tokens
- `POST /api/token/refresh/` - Refresh access token

### Events
- `POST /api/events/create-event/` - Create a new event (Admin only)
  - Required fields: `source`, `event_type`, `severity`, `description`
  - Severity values: 1 (Low), 2 (Medium), 3 (High), 4 (Critical)

### Alerts
- `GET /api/alerts/list-alerts/` - List all alerts with pagination (Authenticated users)
  - Supports filtering by `status` and `severity` query parameters
- `PATCH /api/alerts/update-alert/<id>/` - Update alert status (Admin only)
  - Allowed status values: 1 (Open), 2 (Acknowledged), 3 (Resolved)

### Admin
- `/admin/` - Django admin interface for user and data management


## Filtering & Pagination

### Filtering

The alert listing endpoint supports filtering using query parameters:

- `status`: Filter by alert status (1=Open, 2=Acknowledged, 3=Resolved)
- `severity`: Filter by event severity (1=Low, 2=Medium, 3=High, 4=Critical)

Example:
```
GET /api/alerts/list-alerts/?status=1&severity=3
```

This returns all open alerts for high-severity events.

### Pagination

All list endpoints use pagination with a default page size of 10 items. Use the `page` query parameter to navigate:

```
GET /api/alerts/list-alerts/?page=2
```

Response includes pagination metadata:
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/alerts/list-alerts/?page=3",
    "previous": "http://localhost:8000/api/alerts/list-alerts/?page=1",
    "results": [...]
}
```

## Logging

Critical actions are logged to the console with structured messages:

- **Event Creation**: Logged at INFO level with event ID and severity
- **Automatic Alert Creation**: Logged at WARNING level with alert ID and event ID
- **Alert Status Updates**: Logged when alert status is modified

Log format: `[LEVEL] TIMESTAMP MODULE - MESSAGE`

Example log output:
```
[INFO] 2024-01-15 10:30:45 events.serializers - Event created | id=1 | severity=High
[WARNING] 2024-01-15 10:30:45 events.serializers - Alert auto-created | alert_id=1 | event_id=1
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Anonymous users**: 20 requests per minute
- **Authenticated users**: 100 requests per minute

When the limit is exceeded, a `429 Too Many Requests` response is returned.

## Docker Setup

### Using Docker Compose

1. **Build and run the container**:
```bash
docker-compose up --build
```

2. **Run migrations** (in a separate terminal or exec into the container):
```bash
docker-compose exec web python manage.py migrate
```

3. **Create a superuser**:
```bash
docker-compose exec web python manage.py createsuperuser
```

The application will be available at `http://localhost:8000`

### Using Dockerfile Directly

1. **Build the image**:
```bash
docker build -t threat-monitoring-backend .
```

2. **Run the container**:
```bash
docker run -p 8000:8000 --env-file .env threat-monitoring-backend
```

**Note**: The Docker setup uses SQLite, so data persists only within the container volume.

## Deployment (AWS EC2 – Example)

This section provides example deployment steps for AWS EC2. These are documentation-only and do not include infrastructure automation.

### Prerequisites

- AWS EC2 instance (Ubuntu 22.04 LTS recommended)
- Security group configured to allow HTTP (port 80) and SSH (port 22)
- Domain name (optional, for production)

### Deployment Steps

1. **Connect to EC2 instance**:
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

2. **Update system packages**:
```bash
sudo apt update && sudo apt upgrade -y
```

3. **Install Python and dependencies**:
```bash
sudo apt install python3-pip python3-venv -y
```

4. **Clone the repository**:
```bash
git clone <repository-url>
cd threat-monitoring-backend
```

5. **Create virtual environment and install dependencies**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Configure environment variables**:
```bash
nano .env
```
Set `DEBUG=False`, `ALLOWED_HOSTS=your-ec2-ip,your-domain.com`, and a strong `SECRET_KEY`.

7. **Run migrations**:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

8. **Create superuser**:
```bash
python manage.py createsuperuser
```

9. **Run the server** (for testing):
```bash
python manage.py runserver 0.0.0.0:8000
```

10. **For production**, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn threat_monitoring.wsgi:application --bind 0.0.0.0:8000
```

11. **Set up a process manager** (e.g., systemd) to keep the application running and start on boot.

**Security Notes**:
- Use environment variables for sensitive data
- Configure firewall rules appropriately
- Consider using HTTPS with a reverse proxy (nginx) in production
- Regularly update dependencies and the operating system

## Assumptions Made

1. **User Management**: Users are created via Django Admin only; no signup API is provided
2. **Database**: SQLite is sufficient for the assignment scope; production would use PostgreSQL or MySQL
3. **Alert-Event Relationship**: One-to-one relationship between alerts and events (one alert per event)
4. **Status Values**: Alert status uses integer choices (1=Open, 2=Acknowledged, 3=Resolved)
5. **Severity Values**: Event severity uses integer choices (1=Low, 2=Medium, 3=High, 4=Critical)
6. **Deployment**: Simple deployment documentation is sufficient; no infrastructure automation required

## API Documentation

All APIs are documented in the README and can be tested using tools like Postman.

A Postman collection is included in the project root:
- `threat-monitoring-api.postman_collection.json`

This collection contains preconfigured requests for authentication, event creation, alert listing, filtering, and alert status updates.

### Manual Testing Checklist

1. **Authentication**:
   - Obtain JWT token with valid credentials
   - Verify token refresh functionality
   - Test access with invalid/expired tokens

2. **Event Creation** (Admin only):
   - Create events with different severity levels
   - Verify automatic alert creation for High/Critical events
   - Test validation errors for invalid data

3. **Alert Listing**:
   - List alerts as Admin and Analyst
   - Test pagination
   - Test filtering by status and severity

4. **Alert Status Update** (Admin only):
   - Update alert status to Acknowledged
   - Update alert status to Resolved
   - Verify Analyst cannot update alerts

5. **Rate Limiting**:
   - Verify rate limits are enforced
   - Check rate limit headers in responses

6. **Logging**:
   - Verify event creation is logged
   - Verify automatic alert creation is logged
   - Verify alert status updates are logged

## Final Notes

- The application follows Django REST Framework best practices
- All database queries use Django ORM to prevent SQL injection
- Input validation is handled through DRF serializers
- Permission checks are enforced at the view level
- The codebase is organized into separate apps (accounts, events, alerts) for maintainability
- Settings are split into base, development, and production configurations
- CORS is configured to allow cross-origin requests (adjust for production)
