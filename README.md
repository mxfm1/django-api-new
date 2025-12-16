# Django API - Residence Management System

A Django REST API for managing residences, residents, and guest invitations. This system allows administrators to manage residential properties, assign residents to residences, and create invitation codes for guests.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Models](#models)
- [Permissions](#permissions)
- [Deployment](#deployment)

## ✨ Features

- **User Authentication**: JWT-based authentication with token refresh
- **Residence Management**: Create, read, update, and delete residential properties
- **Resident Management**: Assign users to residences with resident profiles
- **Invitation System**: Generate unique invitation codes for guests with expiration dates
- **Role-Based Access Control**: Admin and staff permissions for managing houses
- **User Management**: Admin endpoints for user registration and management

## 🛠 Technology Stack

- **Framework**: Django 5.2.8
- **API**: Django REST Framework 3.16.1
- **Authentication**: djangorestframework-simplejwt 5.5.1
- **Database**: 
  - SQLite (development)
  - PostgreSQL (production via psycopg2-binary)
- **Deployment**: 
  - Gunicorn (WSGI server)
  - WhiteNoise (static file serving)
- **Environment Management**: python-dotenv, environs

## 📁 Project Structure

```
django-api-new/
├── api/                    # Base API app
├── houses/                 # Residence management app
│   ├── models.py          # Residence and ResidentProfile models
│   ├── views.py           # Residence CRUD operations
│   ├── serializers.py     # Data serialization
│   ├── permissions.py     # Custom permission classes
│   └── urls.py            # Residence endpoints
├── invitations/           # Invitation management app
│   ├── models.py          # Invitation model
│   ├── views.py           # Invitation CRUD operations
│   ├── serializers.py     # Invitation serialization
│   └── urls.py            # Invitation endpoints
├── userauth/              # User authentication app
│   ├── views.py           # Login, register, logout views
│   ├── serializers.py     # User serialization
│   └── urls.py            # Auth endpoints
├── myproject/             # Main project settings
│   ├── settings.py        # Django configuration
│   └── urls.py            # Root URL configuration
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── build.sh              # Deployment build script
```

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django-api-new
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv env
   env\Scripts\activate

   # Linux/Mac
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   ADMIN_EMAILS=admin@example.com,admin2@example.com
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## ⚙️ Configuration

### Environment Variables

- `SECRET_KEY`: Django secret key (required)
- `ADMIN_EMAILS`: Comma-separated list of admin emails
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `RENDER_EXTERNAL_HOSTNAME`: External hostname for Render deployment (optional)
- `DEBUG`: Debug mode (automatically disabled on Render)

### JWT Settings

- Access token lifetime: 90 hours
- Refresh token lifetime: 1 day
- Token type: Bearer

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/token/` | Obtain JWT access and refresh tokens | No |
| POST | `/api/token/refresh/` | Refresh access token | No |
| POST | `/api/auth/login/` | User login | No |
| POST | `/api/auth/logout/` | User logout | Yes |
| POST | `/api/auth/register/` | Register new user | Admin only |
| GET | `/api/auth/users/` | List all users | Admin only |
| GET | `/api/auth/users/<id>/` | Get user details | Admin only |
| DELETE | `/api/auth/users/<id>/` | Delete user | Admin only |
| GET | `/api/auth/users/me` | Get current user data | Yes |

### Residences

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/houses/` | List all residences | No |
| POST | `/api/houses/create/` | Create new residence | Yes (Admin/Staff) |
| GET | `/api/houses/<identifier>/` | Get residence details | Yes |
| PUT | `/api/houses/<identifier>/` | Update residence | Yes (Owner/Admin) |
| DELETE | `/api/houses/<identifier>/` | Delete residence | Yes (Owner/Admin) |
| POST | `/api/houses/<identifier>/add-residents` | Add residents to residence | Yes |

### Invitations

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/invites/create` | Create invitation | Yes |
| GET | `/api/invites/user/all/` | Get user's residence invitations | Yes |
| GET | `/api/invites/user/invitations/` | Get user's residence invitations | Yes |
| GET | `/api/invites/all/` | Get all invitations | Yes |

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. **Obtain tokens** by calling `/api/token/` with username and password:
   ```json
   POST /api/token/
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

2. **Use the access token** in the Authorization header:
   ```
   Authorization: Bearer <access_token>
   ```

3. **Refresh the token** when it expires:
   ```json
   POST /api/token/refresh/
   {
     "refresh": "<refresh_token>"
   }
   ```

## 📊 Models

### Residence
- `identifier` (CharField, Primary Key): Unique identifier for the residence
- `owner` (ForeignKey to User): Owner of the residence
- `created_by` (ForeignKey to User): User who created the residence
- `created_at` (DateTimeField): Creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

### ResidentProfile
- `user` (OneToOneField to User): Associated user
- `residence` (ForeignKey to Residence): Residence assignment

### Invitation
- `id` (BigAutoField, Primary Key): Unique identifier
- `code` (CharField): Unique 8-character invitation code (auto-generated)
- `guest_name` (CharField): Name of the guest
- `reason` (CharField): Reason for the invitation
- `valid_until` (DateTimeField): Expiration date/time
- `aditional_information` (TextField): Optional additional information
- `residence` (ForeignKey to Residence): Associated residence
- `host` (ForeignKey to User): User who created the invitation
- `created_at` (DateTimeField): Creation timestamp

## 🔒 Permissions

### CanManageHouses Permission

- **Superusers**: Full access (GET, POST, PUT, DELETE)
- **Staff/Owners**: Can manage their own residences
- **Regular users**: Read-only access (GET only)

### Endpoint Permissions

- **Public**: List residences, token endpoints
- **Authenticated**: Create invitations, view own data
- **Admin/Staff**: User management, residence management

## 🚢 Deployment

The project includes a `build.sh` script for deployment (e.g., on Render):

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

### Deployment Checklist

1. Set environment variables in your hosting platform
2. Configure `DATABASE_URL` for PostgreSQL
3. Set `SECRET_KEY` to a secure random value
4. Configure `ALLOWED_HOSTS` in settings
5. Ensure `DEBUG=False` in production
6. Run migrations: `python manage.py migrate`
7. Collect static files: `python manage.py collectstatic`

### Render Deployment

The project is configured for Render deployment:
- Automatically detects Render environment
- Uses WhiteNoise for static file serving
- Supports PostgreSQL via `dj-database-url`

## 📝 Notes

- The API uses `APPEND_SLASH = False` in settings
- SQLite is used by default for development
- PostgreSQL is recommended for production
- Admin emails can be configured via `ADMIN_EMAILS` environment variable
- Invitation codes are automatically generated as 8-character uppercase hex strings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

[Specify your license here]

---

For more information, visit the [Django Documentation](https://docs.djangoproject.com/) and [Django REST Framework Documentation](https://www.django-rest-framework.org/).

