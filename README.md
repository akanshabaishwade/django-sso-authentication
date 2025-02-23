# Django SSO Authentication with JWT and Session Management

This repository implements a **Single Sign-On (SSO) authentication system** using **JWT** (JSON Web Tokens) and **Django's session management**. The API allows users to register, log in, and manage their sessions securely with JWT tokens.

## Features

- **User Registration**: Register new users by providing email, password, first name, and last name.
- **Login**: Login with email and password, and receive **JWT access token**, **refresh token**, and **session key**.
- **Session Management**: Uses Django's built-in session management for handling user sessions.
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
- **djangorestframework** for building RESTful APIs
- **djangorestframework-simplejwt** for JWT token management
- **django-cors-headers** for handling cross-origin resource sharing (optional)
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
      "first_name": "Admin",
      "last_name": "Admin"
    }
    ```
- **Response (Success)**:
    ```json
    {
      "user": {
        "email": "admin@admin.com",
        "first_name": "Admin",
        "last_name": "Admin"
      },
      "message": "User successfully registered. Please log in to obtain access token."
    }
    ```

**Success Image**:
![Registration Success](https://github.com/user-attachments/assets/44fee2b7-b224-4001-9b57-39f918fa0f70)

**Error Image**:
![Registration Error](https://github.com/user-attachments/assets/be10a993-fa41-4fa1-b388-e31edaeae347)

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
        "last_name": "Admin"
      },
      "access_token": "your_access_token_here",
      "refresh_token": "your_refresh_token_here",
      "session_key": "your_session_key_here"
    }
    ```

**Login Image (First-time)**:
![Login Success](https://github.com/user-attachments/assets/9b37f3d4-5cdb-4857-8aaf-fc9c6aa8d92b)

**Error Image (Second-time)**:
![Second-time](https://github.com/user-attachments/assets/7a006c3e-4403-40d8-bf71-dd6d6351b9e5)

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

### 3. **POST /continue-login/** - **Continue Login**
- **Description**: Allows the user to continue their login if they are already logged in. This is used to refresh the session, and replace the old session and access token.
- **Request Body**:
    ```json
    {
      "email": "admin@admin.com",
      "password": "admin"
    }
    ```

- **Response (Session Refresh)**:
    ```json
    {
      "user": {
        "email": "admin@admin.com",
        "first_name": "Admin",
        "last_name": "Admin"
      },
      "access_token": "your_access_token_here",
      "refresh_token": "your_refresh_token_here",
      "session_key": "your_session_key_here"
    }
    ```

**Session Refresh Image**:
![Session Refresh](https://github.com/user-attachments/assets/cd4a8f3a-fff4-4833-b4ba-5fd56c12fdc0)

---

## Postman Collection

To test the API endpoints using Postman, import the following collection into Postman:

1. **Open Postman** and click on the **Import** button in the top-left corner.
2. Choose **Raw Text**.
3. Copy the following JSON and paste it into the text box, then click **Continue**.

---

## Testing

1. **Run the Django development server**:

    ```bash
    python manage.py runserver
    ```

2. **Test the registration and login** using the endpoints listed above with **Postman** or **Curl**.
3. **First-time login** will return `access_token`, `refresh_token`, and `session_key`.
4. **Subsequent logins** will prompt the user to use the "Continue Login" API, showing an error and asking for session refresh.
