# Django SSO Authentication with JWT and Session Management

This repository implements a **Single Sign-On (SSO) authentication system** using **JWT** and **Django’s session management**. The API allows users to register, log in, and manage their sessions securely with JWT tokens.

## Features

- **User Registration**: Register new users by providing email, password, first name, and last name.
- **Login**: Login with email and password, and receive JWT **access token**, **refresh token**, and **session key**.
- **Session Management**: Use Django's built-in session management for handling user sessions.
- **JWT Authentication**: Secure authentication using JWT tokens to access protected APIs.

## Table of Contents

- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Postman Collection](#postman-collection)
- [Testing](#testing)

---

## Installation

### Prerequisites

- **Python 3.8+**
- **Django 4.x** (or higher)
- **djangorestframework** for RESTful API
- **djangorestframework-simplejwt** for JWT token management
- **django-cors-headers** for cross-origin resource sharing (optional)
- **SQLite** (default database) or any other relational database

### Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/akanshabaishwade/django-sso-authentication.git
cd django-sso-authentication
```

### Setup Virtual Environment

Set up a Python virtual environment:

```bash
python -m venv ssovenv
```

Activate the virtual environment:

- **For macOS/Linux**:
    ```bash
    source ssovenv/bin/activate
    ```
- **For Windows**:
    ```bash
    ssovenv\Scripts\activate
    ```

### Install Dependencies

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### Apply Migrations

Run migrations to set up the database:

```bash
python manage.py migrate
```

### Create a Superuser

To access the Django admin panel, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to create the superuser.

---

## API Endpoints

### 1. **POST /register/** - **User Registration**
- **Description**: Registers a new user.
- **Request Body**:
    ```json
    {
      "email": "admin@admin.com",
      "password": "admin",
      "first_name": "admin",
      "last_name": "admin"
    }
    ```
- **Response (Success)**:
    ```json
    {
      "user": {
        "email": "admin@admin.com",
        "first_name": "Admin",
        "last_name": "admin"
      },
      "message": "User successfully registered. Please log in to obtain access token."
    }
    ```

---

### 2. **POST /login/** - **User Login**
- **Description**: Logs in an existing user with email and password.
- **Request Body**:
    ```json
    {
      "email": "admin@admin.com",
      "password": "admin"
    }
    ```

- **Response (First-time Login)**:
    ```json
    {
      "user": {
        "email": "admin@admin.com",
        "first_name": "Admin",
        "last_name": "admin"
      },
      "access_token": "your_access_token_here",
      "refresh_token": "your_refresh_token_here",
      "session_key": "your_session_key_here"
    }
    ```

- **Response (Error - Invalid Credentials)**:
    ```json
    {
      "detail": "Invalid credentials"
    }
    ```

- **Response (Error - User Already Logged In)**:
    ```json
    {
      "detail": "User has already logged in. Please use 'Continue Login' API to refresh session."
    }
    ```

---

## Postman Collection

To test the API endpoints using Postman, import the following collection into Postman:

1. **Open Postman** and click on the **Import** button in the top-left corner.
2. Choose **Raw Text**.
3. Copy the following JSON and paste it into the text box, then click **Continue**.

```json
{
  "info": {
    "_postman_id": "xyz-collection-id",
    "name": "Django JWT Authentication with Session Management",
    "description": "Collection for testing JWT authentication and session management with Django."
  },
  "item": [
    {
      "name": "User Registration",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"admin@admin.com\",\n  \"password\": \"admin\",\n  \"first_name\": \"Admin\",\n  \"last_name\": \"User\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/register/",
          "host": [
            "http://localhost:8000"
          ],
          "path": [
            "register"
          ]
        }
      },
      "response": []
    },
    {
      "name": "User Login",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"admin@admin.com\",\n  \"password\": \"admin\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/login/",
          "host": [
            "http://localhost:8000"
          ],
          "path": [
            "login"
          ]
        }
      },
      "response": []
    }
  ]
}
```

---

## Testing

1. **Run the Django development server**:

    ```bash
    python manage.py runserver
    ```

2. **Test the registration and login** using the endpoints listed above with **Postman** or **Curl**.
3. **First-time login** will return `access_token`, `refresh_token`, and `session_key`.
4. **Subsequent logins** will prompt the user to use the "Continue Login" API, showing an error and asking for session refresh.

