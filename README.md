# Django Backend - Request Management System

This is a Django REST API backend ported from Node.js, powered by PostgreSQL. It provides user authentication and request management functionality.

## Features

- User authentication (JWT-based)
- Request management (CRUD operations)
- Role-based access control (Employee/Partner)
- Excel export functionality
- PostgreSQL database integration
- **Interactive API Documentation (Swagger UI & ReDoc)**

## Project Structure

```
backend/
├── apps/
│   ├── users/          # User management app
│   └── requests/       # Request management app
├── backend/            # Django project settings
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
└── manage.py          # Django management script
```

## Quick Setup

1. **Prerequisites**

   - Python 3.8+
   - PostgreSQL 12+
   - pip

2. **Database Setup**

   ```sql
   CREATE DATABASE requests_db;
   CREATE USER postgres WITH PASSWORD 'root';
   GRANT ALL PRIVILEGES ON DATABASE requests_db TO postgres;
   ```

3. **Environment Setup**

   ```bash
   # Run the setup script
   python setup.py
   ```

   Or manually:

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Unix/Linux/Mac:
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Run migrations
   python manage.py makemigrations
   python manage.py migrate

   # Create superuser (optional)
   python manage.py createsuperuser
   ```

4. **Start the server**

   ```bash
   python manage.py runserver 5100
   ```

5. **Access API Documentation**
   - Swagger UI: http://localhost:5100/api/docs/
   - ReDoc: http://localhost:5100/api/redoc/
   - OpenAPI Schema: http://localhost:5100/api/schema/

## Environment Variables

Update your `.env` file with your database credentials:

```env
JWT_SECRET=your-jwt-secret
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=requests_db
DB_USER=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=5432
```

## API Endpoints

### Users

- `GET /api/users/` - Get all users (with optional role filter)
- `POST /api/users/login/` - User login
- `POST /api/users/signup/` - User registration
- `PUT /api/users/edit-user/` - Update user profile
- `PUT /api/users/update-password/` - Update password
- `POST /api/users/reset-password/` - Reset password

### Requests

- `GET /api/requests/` - Get requests (with pagination, search, filters)
- `POST /api/requests/` - Create new request
- `GET /api/requests/export/` - Export approved requests to Excel
- `GET /api/requests/{id}/` - Get request by ID
- `PATCH /api/requests/{id}/` - Update request status (approvers only)
- `PUT /api/requests/{id}/` - Edit request details (requesters only, pending requests)
- `DELETE /api/requests/{id}/` - Delete request (requesters only, pending requests)

## Authentication

All request endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Role-Based Access

- **Employee**: Can only see and manage their own requests
- **Partner**: Can see and manage all requests, approve/reject requests

## Database Models

### User Model

- `user_id` (UUID, unique)
- `first_name`, `last_name`
- `email` (unique)
- `phone` (unique)
- `role` (Employee/Partner)
- `password` (hashed with bcrypt)

### Request Model

- `id` (UUID, primary key)
- `request_number` (unique integer)
- `request_by` (UUID, references User)
- `approver_id` (UUID, references User)
- `amount`, `currency`
- `purpose`, `description`
- `status` (Pending/Approved/Rejected)
- `initiated_on`, `required_on`

## Migration from Node.js

This Django backend maintains API compatibility with the original Node.js version:

- Same endpoint URLs and HTTP methods
- Same request/response formats
- Same authentication mechanism (JWT)
- Same business logic and access controls

## Development

```bash
# Run tests
python manage.py test

# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django admin
# Navigate to http://localhost:5100/admin/
```

## Production Deployment

1. Set `DEBUG=False` in settings
2. Configure proper database credentials
3. Set up static file serving
4. Use a production WSGI server (gunicorn, uWSGI)
5. Configure reverse proxy (nginx, Apache)

## API Documentation

This project includes comprehensive interactive API documentation:

### 📖 Swagger UI

- **URL**: http://localhost:5100/api/docs/
- **Features**: Interactive API explorer, try-it-out functionality, request/response examples
- **Best for**: Testing endpoints and understanding API structure

### 📚 ReDoc

- **URL**: http://localhost:5100/api/redoc/
- **Features**: Clean, readable documentation with detailed descriptions
- **Best for**: Reading comprehensive API documentation

### 🔧 OpenAPI Schema

- **URL**: http://localhost:5100/api/schema/
- **Features**: Raw OpenAPI 3.0 schema in JSON format
- **Best for**: Generating client SDKs or importing into other tools

### Testing Documentation

```bash
# Test if documentation is working
python test_docs.py
```

## Dependencies

- Django 5.0.1 - Web framework
- Django REST Framework - API framework
- drf-spectacular - OpenAPI 3.0 schema generation & Swagger UI
- psycopg2-binary - PostgreSQL adapter
- python-decouple - Environment variable management
- django-cors-headers - CORS handling
- PyJWT - JWT token handling
- bcrypt - Password hashing
- openpyxl - Excel file generation
