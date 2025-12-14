# API Documentation - Social Media API

Complete API reference for the Social Media API endpoints.

## Base URL

```
http://localhost:8000/api/v1
https://yourdomain.com/api/v1  (Production)
```

## Authentication

All endpoints requiring authentication use **Token Authentication**.

### Get Token

**Endpoint:** `POST /auth/login/`

**Request:**
```json
{
  "username": "john",
  "password": "securepass123"
}
```

**Response:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Header Required:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## Authentication Endpoints

### 1. Register User

**Endpoint:** `POST /auth/register/`

**Access:** Public

**Request:**
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "securepass123"
}
```

**Response:** `201 Created`
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Error Responses:**
```json
{
  "username": ["A user with that username already exists."],
  "password": ["This password is too common."]
}
```

---

### 2. Login User

**Endpoint:** `POST /auth/login/`

**Access:** Public

**Request:**
```json
{
  "username": "alice",
  "password": "securepass123"
}
```

**Response:** `200 OK`
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Error Response:**
```json
{
  "error": "Invalid credentials"
}
```

---

### 3. Get User Profile

**Endpoint:** `GET /auth/profile/`

**Access:** Authenticated

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "bio": "I love coding!",
  "profile_picture": "http://localhost:8000/media/profile_pics/alice.jpg",
  "following_count": 5,
  "followers_count": 10
}
```

---

### 4. Follow User

**Endpoint:** `POST /auth/follow/<user_id>/`

**Access:** Authenticated

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**URL Parameters:**
- `user_id` (integer) - ID of user to follow

**Response:** `200 OK`
```json
{
  "message": "You are now following alice."
}
```

**Error Responses:**
```json
{
  "error": "User not found."
}

{
  "error": "You cannot follow yourself."
}
```

---

### 5. Unfollow User

**Endpoint:** `POST /auth/unfollow/<user_id>/`

**Access:** Authenticated

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**URL Parameters:**
- `user_id` (integer) - ID of user to unfollow

**Response:** `200 OK`
```json
{
  "message": "You have unfollowed alice."
}
```

---

## Post Endpoints

### 1. List Posts

**Endpoint:** `GET /posts/`

**Access:** Public

**Query Parameters:**
- `page` (integer) - Page number (default: 1)
- `search` (string) - Search by title or content
- `ordering` (string) - Order by field (`-created_at`, `title`, etc.)

**Example:**
```
GET /posts/?page=1&search=django&ordering=-created_at
```

**Response:** `200 OK`
```json
{
  "count": 5,
  "next": "http://localhost:8000/api/v1/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": "alice",
      "title": "Getting Started with Django",
      "content": "Django is a powerful web framework...",
      "created_at": "2024-12-14T10:30:00Z",
      "updated_at": "2024-12-14T10:30:00Z",
      "like_count": 5,
      "comment_count": 2
    }
  ]
}
```

---

### 2. Create Post

**Endpoint:** `POST /posts/`

**Access:** Authenticated

**Headers:**
```
Authorization: Token YOUR_TOKEN
Content-Type: application/json
```

**Request:**
```json
{
  "title": "My First Post",
  "content": "This is the content of my first post!"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "author": "alice",
  "title": "My First Post",
  "content": "This is the content of my first post!",
  "created_at": "2024-12-14T10:30:00Z",
  "updated_at": "2024-12-14T10:30:00Z",
  "like_count": 0,
  "comment_count": 0
}
```

---

### 3. Get Post Details

**Endpoint:** `GET /posts/<id>/`

**Access:** Public

**URL Parameters:**
- `id` (integer) - Post ID

**Response:** `200 OK`
```json
{
  "id": 1,
  "author": "alice",
  "title": "My First Post",
  "content": "This is the content of my first post!",
  "created_at": "2024-12-14T10:30:00Z",
  "updated_at": "2024-12-14T10:30:00Z",
  "like_count": 5,
  "comment_count": 2
}
```

---

### 4. Update Post

**Endpoint:** `PUT /posts/<id>/`

**Access:** Authenticated (author only)

**Headers:**
```
Authorization: Token YOUR_TOKEN
Content-Type: application/json
```

**URL Parameters:**
- `id` (integer) - Post ID

**Request:**
```json
{
  "title": "Updated Title",
  "content": "Updated content..."
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "author": "alice",
  "title": "Updated Title",
  "content": "Updated content...",
  "created_at": "2024-12-14T10:30:00Z",
  "updated_at": "2024-12-14T11:00:00Z",
  "like_count": 5,
  "comment_count": 2
}
```

---

### 5. Delete Post

**Endpoint:** `DELETE /posts/<id>/`

**Access:** Authenticated (author only)

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**URL Parameters:**
- `id` (integer) - Post ID

**Response:** `204 No Content`

---

### 6. Like Post

**Endpoint:** `POST /posts/<id>/like/`

**Access:** Authenticated

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**URL Parameters:**
- `id` (integer) - Post ID

**Response:** `200 OK`
```json
{
  "detail": "Post liked successfully."
}
```

**Error Response:**
```json
{
  "detail": "You have already liked this post."
}
```

---

### 7. Unlike Post

**Endpoint:** `POST /posts/<id>/unlike/`

**Access:** Authenticated

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**URL Parameters:**
- `id` (integer) - Post ID

**Response:** `200 OK`
```json
{
  "detail": "Post unliked successfully!"
}
```

**Error Response:**
```json
{
  "detail": "You haven't liked this post."
}
```

---

### 8. Get Feed

**Endpoint:** `GET /feed/`

**Access:** Authenticated

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**Query Parameters:**
- `page` (integer) - Page number

**Response:** `200 OK`
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/v1/feed/?page=2",
  "previous": null,
  "results": [
    {
      "id": 5,
      "author": "bob",
      "title": "Django Tips",
      "content": "Some useful Django tips...",
      "created_at": "2024-12-14T10:30:00Z",
      "updated_at": "2024-12-14T10:30:00Z",
      "like_count": 3,
      "comment_count": 1
    }
  ]
}
```

---

## Comment Endpoints

### 1. List Comments

**Endpoint:** `GET /comments/`

**Access:** Public

**Query Parameters:**
- `page` (integer) - Page number
- `post` (integer) - Filter by post ID

**Response:** `200 OK`
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": "bob",
      "post": 1,
      "content": "Great post!",
      "created_at": "2024-12-14T10:35:00Z",
      "updated_at": "2024-12-14T10:35:00Z"
    }
  ]
}
```

---

### 2. Create Comment

**Endpoint:** `POST /comments/`

**Access:** Authenticated

**Headers:**
```
Authorization: Token YOUR_TOKEN
Content-Type: application/json
```

**Request:**
```json
{
  "post": 1,
  "content": "Great post! Very helpful."
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "author": "bob",
  "post": 1,
  "content": "Great post! Very helpful.",
  "created_at": "2024-12-14T10:35:00Z",
  "updated_at": "2024-12-14T10:35:00Z"
}
```

---

### 3. Get Comment Details

**Endpoint:** `GET /comments/<id>/`

**Access:** Public

**URL Parameters:**
- `id` (integer) - Comment ID

**Response:** `200 OK`
```json
{
  "id": 1,
  "author": "bob",
  "post": 1,
  "content": "Great post! Very helpful.",
  "created_at": "2024-12-14T10:35:00Z",
  "updated_at": "2024-12-14T10:35:00Z"
}
```

---

### 4. Update Comment

**Endpoint:** `PUT /comments/<id>/`

**Access:** Authenticated (author only)

**Headers:**
```
Authorization: Token YOUR_TOKEN
Content-Type: application/json
```

**Request:**
```json
{
  "content": "Updated comment content"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "author": "bob",
  "post": 1,
  "content": "Updated comment content",
  "created_at": "2024-12-14T10:35:00Z",
  "updated_at": "2024-12-14T11:00:00Z"
}
```

---

### 5. Delete Comment

**Endpoint:** `DELETE /comments/<id>/`

**Access:** Authenticated (author only)

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**Response:** `204 No Content`

---

## Notification Endpoints

### 1. List Notifications

**Endpoint:** `GET /notifications/`

**Access:** Authenticated

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**Query Parameters:**
- `page` (integer) - Page number

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "actor": "bob",
    "recipient": "alice",
    "verb": "liked your post",
    "target_ct": 1,
    "target_id": 5,
    "timestamp": "2024-12-14T10:30:00Z",
    "read": false
  },
  {
    "id": 2,
    "actor": "charlie",
    "recipient": "alice",
    "verb": "commented on your post",
    "target_ct": 1,
    "target_id": 5,
    "timestamp": "2024-12-14T10:25:00Z",
    "read": true
  }
]
```

---

### 2. Mark All Notifications as Read

**Endpoint:** `POST /notifications/mark_as_read/`

**Access:** Authenticated

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**Response:** `200 OK`
```json
{
  "detail": "Marked 3 notifications as read."
}
```

---

### 3. Mark Specific Notification as Read

**Endpoint:** `POST /notifications/<id>/mark_read/`

**Access:** Authenticated

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**URL Parameters:**
- `id` (integer) - Notification ID

**Response:** `200 OK`
```json
{
  "detail": "Notification marked as read."
}
```

---

## Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Request successful, no content returned |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Permission denied |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Duplicate resource |
| 500 | Internal Server Error - Server error |

---

## Rate Limiting

Currently, the API does not have rate limiting. For production deployment, implement rate limiting:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

---

## Pagination

Responses with lists use pagination. Default page size: 10

**Pagination Parameters:**
```
GET /posts/?page=2&limit=20
```

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/v1/posts/?page=3",
  "previous": "http://localhost:8000/api/v1/posts/?page=1",
  "results": [...]
}
```

---

## Error Handling

### Standard Error Response
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

### Validation Error
```json
{
  "field_name": ["Error message"],
  "other_field": ["Another error message"]
}
```

---

## CURL Examples

### Get Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"securepass123"}'
```

### Create Post
```bash
curl -X POST http://localhost:8000/api/v1/posts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Post","content":"Post content"}'
```

### List Posts
```bash
curl -X GET http://localhost:8000/api/v1/posts/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Like Post
```bash
curl -X POST http://localhost:8000/api/v1/posts/1/like/ \
  -H "Authorization: Token YOUR_TOKEN"
```

---

## Webhooks (Future Feature)

Webhooks for real-time notifications are planned for future releases.

---

**Last Updated**: December 2024
