# Authentication API

This document describes the authentication endpoints for the application.

## Endpoints

### 1. Register a New User (`/signup`)

This endpoint allows new users to register an account by providing a unique username and a password.

-   **URL**: `/signup`
-   **Method**: `POST`
-   **Request Body**:
    -   `username` (string, **required**): A unique username for the new user.
    -   `password` (string, **required**): The user's password.

**Example Request:**

```bash
curl -X POST "http://127.0.0.1:8000/signup" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "securepassword"}'
```

**Example Success Response (Status: 200 OK):**

```json
{
  "id": 1,
  "username": "testuser"
}
```

**Example Error Response (Status: 400 Bad Request - Username already registered):**

```json
{
  "detail": "Username already registered"
}
```

### 2. User Login (`/login`)

This endpoint allows registered users to log in and obtain an access token. This token is then used to authenticate requests to protected endpoints.

-   **URL**: `/login`
-   **Method**: `POST`
-   **Request Body**:
    -   `username` (string, **required**): The registered username.
    -   `password` (string, **required**): The user's password.
    -   **Note**: This endpoint expects `application/x-www-form-urlencoded` content type.

**Example Request:**

```bash
curl -X POST "http://127.0.0.1:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=securepassword"
```

**Example Success Response (Status: 200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Example Error Response (Status: 401 Unauthorized - Incorrect credentials):**

```json
{
  "detail": "Incorrect username or password"
}
```

### 3. Get Current User Information (`/users/me`)

This endpoint returns the details of the currently authenticated user. It requires a valid JWT access token in the `Authorization` header.

-   **URL**: `/users/me`
-   **Method**: `GET`
-   **Headers**:
    -   `Authorization` (string, **required**): `Bearer <access_token>`

**Example Request:**

```bash
curl -X GET "http://127.0.0.1:8000/users/me" \
     -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```
*Replace `<YOUR_ACCESS_TOKEN>` with the actual token obtained from the `/login` endpoint.*

**Example Success Response (Status: 200 OK):**

```json
{
  "id": 1,
  "username": "testuser"
}
```

**Example Error Response (Status: 401 Unauthorized - Invalid or missing token):**

```json
{
  "detail": "Could not validate credentials"
}
```
