# API Documentation

## Overview
This document provides an overview of the API endpoints available in the advanced API project. It includes details on request and response formats, as well as usage examples.

## Base URL
The base URL for accessing the API is:
```
http://127.0.0.1:8000/api/
```

## Endpoints

### 1. List Books
- **URL:** `/books/`
- **Method:** `GET`
- **Description:** Retrieve a list of all books.
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    [
      {
        "id": 1,
        "title": "Book Title 1",
        "author": "Author Name 1"
      },
      {
        "id": 2,
        "title": "Book Title 2",
        "author": "Author Name 2"
      }
    ]
    ```

### 2. Create a Book
- **URL:** `/books/`
- **Method:** `POST`
- **Description:** Create a new book.
- **Request Body:**
  ```json
  {
    "title": "New Book Title",
    "author": "New Author Name"
  }
  ```
- **Response:**
  - **Status Code:** 201 Created
  - **Body:**
    ```json
    {
      "id": 3,
      "title": "New Book Title",
      "author": "New Author Name"
    }
    ```

### 3. Retrieve a Book
- **URL:** `/books/{id}/`
- **Method:** `GET`
- **Description:** Retrieve a specific book by ID.
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "id": 1,
      "title": "Book Title 1",
      "author": "Author Name 1"
    }
    ```

### 4. Update a Book
- **URL:** `/books/{id}/`
- **Method:** `PUT`
- **Description:** Update an existing book.
- **Request Body:**
  ```json
  {
    "title": "Updated Book Title",
    "author": "Updated Author Name"
  }
  ```
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "id": 1,
      "title": "Updated Book Title",
      "author": "Updated Author Name"
    }
    ```

### 5. Delete a Book
- **URL:** `/books/{id}/`
- **Method:** `DELETE`
- **Description:** Delete a specific book by ID.
- **Response:**
  - **Status Code:** 204 No Content

## Authentication
Some endpoints may require authentication. Ensure to include the token in the request headers:
```
Authorization: Token <your_token>
```

## Error Handling
The API will return appropriate error messages and status codes for invalid requests. For example:
- **Status Code:** 400 Bad Request
- **Body:**
  ```json
  {
    "error": "Invalid data provided."
  }
  ```

## Conclusion
This API provides a simple interface for managing books and authors. For further details on specific endpoints or additional features, please refer to the source code or contact the development team.