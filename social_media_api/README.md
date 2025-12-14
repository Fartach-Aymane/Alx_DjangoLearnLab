# Social Media API - Django REST Framework

A comprehensive Social Media API built with Django and Django REST Framework featuring user authentication, posts, comments, likes, notifications, and social interactions.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Features

### User Management
- User registration and authentication
- Custom user model with bio and profile picture
- Follow/unfollow system
- User profiles with follower counts

### Posts & Comments
- Create, read, update, delete (CRUD) posts
- Add comments to posts
- Paginated post listings
- Search and filter posts by title/content
- View feed of posts from followed users

### Likes & Notifications
- Like/unlike posts
- Automatic notifications for:
  - New followers
  - Post likes
  - Comments on posts
- Mark notifications as read

### REST API
- Token-based authentication
- RESTful API design
- Pagination and filtering
- Comprehensive error handling

## Project Structure

```
social_media_api/
├── accounts/                 # User authentication and profile management
│   ├── models.py            # Custom User model
│   ├── serializers.py       # User serializers
│   ├── views.py             # Registration, login, follow endpoints
│   ├── urls.py              # User routes
│   └── admin.py             # Admin configuration
│
├── posts/                    # Posts and comments functionality
│   ├── models.py            # Post, Comment, Like models
│   ├── serializers.py       # Post and comment serializers
│   ├── views.py             # CRUD viewsets and feed logic
│   ├── permissions.py       # Custom permissions
│   ├── urls.py              # Post routes
│   └── admin.py             # Admin configuration
│
├── notifications/           # Notifications system
│   ├── models.py            # Notification model
│   ├── serializers.py       # Notification serializer
│   ├── views.py             # Notification endpoints
│   ├── urls.py              # Notification routes
│   └── admin.py             # Admin configuration
│
├── social_media_api/        # Project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (create locally)
```

## Requirements

- Python 3.8+
- Django 5.2+
- Django REST Framework 3.14+
- PostgreSQL (recommended for production)
- SQLite (default for development)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Alx_DjangoLearnLab.git
cd social_media_api
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create .env File

```bash
# Create .env file in project root
cat > .env << EOF
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
EOF
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Create Test Data (Optional)

```bash
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> from posts.models import Post
>>> User = get_user_model()
>>> 
>>> # Create test users
>>> user1 = User.objects.create_user(username='alice', password='testpass123', bio='Alice bio')
>>> user2 = User.objects.create_user(username='bob', password='testpass123', bio='Bob bio')
>>> 
>>> # Create test posts
>>> Post.objects.create(author=user1, title='First Post', content='This is my first post')
>>> Post.objects.create(author=user2, title='Hello World', content='Hello to the world!')
>>> exit()
```

## Configuration

### Database Configuration

For **development** (SQLite):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

For **production** (PostgreSQL), set `DATABASE_URL`:
```bash
DATABASE_URL=postgres://user:password@localhost:5432/social_media_db
```

### REST Framework Settings

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

## Running the Application

### Development Server

```bash
python manage.py runserver
```

Server will be available at `http://localhost:8000`

### Admin Panel

```
http://localhost:8000/admin/
Username: admin
Password: (as set during superuser creation)
```

## API Endpoints

### Base URL
```
http://localhost:8000/api/v1/
```

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Register a new user |
| POST | `/auth/login/` | Login and get token |
| GET | `/auth/profile/` | Get current user profile |
| POST | `/auth/follow/<user_id>/` | Follow a user |
| POST | `/auth/unfollow/<user_id>/` | Unfollow a user |

#### Register Example
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

#### Login Example
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "securepass123"
  }'

# Response:
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Post Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/posts/` | List all posts (paginated) |
| POST | `/posts/` | Create a new post |
| GET | `/posts/<id>/` | Retrieve post details |
| PUT | `/posts/<id>/` | Update a post |
| DELETE | `/posts/<id>/` | Delete a post |
| POST | `/posts/<id>/like/` | Like a post |
| POST | `/posts/<id>/unlike/` | Unlike a post |
| GET | `/feed/` | Get feed of followed users' posts |

#### Create Post Example
```bash
curl -X POST http://localhost:8000/api/v1/posts/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first post!"
  }'
```

### Comment Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/comments/` | List all comments |
| POST | `/comments/` | Create a new comment |
| GET | `/comments/<id>/` | Retrieve comment details |
| PUT | `/comments/<id>/` | Update a comment |
| DELETE | `/comments/<id>/` | Delete a comment |

#### Add Comment Example
```bash
curl -X POST http://localhost:8000/api/v1/comments/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "Great post!"
  }'
```

### Notification Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notifications/` | List user notifications |
| POST | `/notifications/mark_as_read/` | Mark all notifications as read |
| POST | `/notifications/<id>/mark_read/` | Mark specific notification as read |

#### Get Notifications Example
```bash
curl -X GET http://localhost:8000/api/v1/notifications/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## Authentication

The API uses **Token Authentication**. All authenticated requests require:

```bash
Authorization: Token <your-token-here>
```

### Obtaining a Token

1. Register: `POST /auth/register/`
2. Login: `POST /auth/login/`
3. Use returned token in all subsequent requests

### Example with Token
```bash
curl -X GET http://localhost:8000/api/v1/posts/ \
  -H "Authorization: Token your_token_here"
```

## Testing

### Using Postman

1. Import the API endpoints
2. Set Authorization header with your token
3. Test each endpoint

### Using curl

See examples in the API Endpoints section above.

### Running Django Tests

```bash
python manage.py test
```

## Deployment

### Preparing for Production

1. **Update .env for Production**
```bash
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-min-50-chars
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@host:5432/dbname
```

2. **Collect Static Files**
```bash
python manage.py collectstatic --noinput
```

3. **Run Security Check**
```bash
python manage.py check --deploy
```

### Deploy to Heroku

1. **Install Heroku CLI**
```bash
# Windows
choco install heroku-cli

# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku App**
```bash
heroku create your-app-name
```

4. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

5. **Set Environment Variables**
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
```

6. **Deploy**
```bash
git push heroku main
```

7. **Run Migrations on Heroku**
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Deploy to AWS Elastic Beanstalk

See the [AWS Deployment Guide](./docs/aws-deployment.md) for detailed instructions.

### Deploy to DigitalOcean

See the [DigitalOcean Deployment Guide](./docs/digitalocean-deployment.md) for detailed instructions.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DEBUG | True | Django debug mode |
| SECRET_KEY | dev-key | Django secret key (CHANGE IN PRODUCTION) |
| ALLOWED_HOSTS | localhost,127.0.0.1 | Allowed host domains |
| DATABASE_URL | - | Database connection string |
| DJANGO_SETTINGS_MODULE | social_media_api.settings | Django settings module |

## Project Models

### User Model
- Extends Django's AbstractUser
- Fields: username, email, password, bio, profile_picture, following (ManyToMany)

### Post Model
- Fields: author (FK), title, content, created_at, updated_at

### Comment Model
- Fields: post (FK), author (FK), content, created_at, updated_at

### Like Model
- Fields: post (FK), user (FK), timestamp
- Constraint: Unique together (post, user)

### Notification Model
- Fields: recipient (FK), actor (FK), verb, target_ct, target_id, timestamp, read

## API Response Format

All responses are in JSON format.

### Success Response
```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "bio": "I am John",
  "profile_picture": "https://...",
  "following_count": 5,
  "followers_count": 10
}
```

### Error Response
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

## Permissions

- **IsAuthenticated**: User must be logged in
- **IsAuthenticatedOrReadOnly**: Unauthenticated users can view, only authenticated can create/edit
- **IsAuthorOrReadOnly**: Only the post/comment author can edit/delete

## Performance Optimization

- Database queries are optimized with `select_related()` and `prefetch_related()`
- Pagination is implemented (10 items per page by default)
- Caching can be added for feed generation using Redis
- API rate limiting recommended for production

## Security Features

- Token-based authentication
- HTTPS enforced in production
- CSRF protection
- XSS protection
- SQL injection prevention via ORM
- Password hashing with PBKDF2

## Troubleshooting

### ModuleNotFoundError: No module named 'django'
```bash
pip install -r requirements.txt
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Database errors
```bash
python manage.py migrate
```

### Static files not loading
```bash
python manage.py collectstatic --clear --noinput
```

### Port 8000 already in use
```bash
python manage.py runserver 8001
```

## Common Use Cases

### Register a New User
```bash
POST /api/v1/auth/register/
{
  "username": "newuser",
  "email": "new@example.com",
  "password": "securepass123"
}
```

### Get Your Feed
```bash
GET /api/v1/feed/
Authorization: Token YOUR_TOKEN
```

### Create and Like a Post
```bash
# Create post
POST /api/v1/posts/
Authorization: Token YOUR_TOKEN
{
  "title": "Post Title",
  "content": "Post content"
}

# Like post
POST /api/v1/posts/1/like/
Authorization: Token YOUR_TOKEN
```

### Follow Another User
```bash
POST /api/v1/auth/follow/2/
Authorization: Token YOUR_TOKEN
```

## Contributors

- Project Lead: Your Name

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please create an issue in the GitHub repository.

## Changelog

### Version 1.0.0 (Current)
- Initial release with core features
- User authentication and profiles
- Posts and comments
- Like and notification system
- Follow/unfollow functionality

---

**Last Updated**: December 2024
