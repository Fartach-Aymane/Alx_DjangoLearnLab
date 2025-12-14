# Quick Start Guide - Social Media API

Get up and running with the Social Media API in 5 minutes!

## Prerequisites

- Python 3.8+
- pip and virtualenv
- Git

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/Alx_DjangoLearnLab.git
cd social_media_api
```

### 2. Setup Virtual Environment

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

### 4. Configure Project

```bash
# Create .env file
echo "DEBUG=True" > .env
echo "SECRET_KEY=dev-secret-key-change-in-production" >> .env
echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env
```

### 5. Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

Enter your credentials:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123` (or your choice)

### 6. Start Server

```bash
python manage.py runserver
```

Server is now running at: **http://localhost:8000**

---

## Quick API Test

### 1. Get Admin Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Response:**
```json
{
  "token": "your_token_here"
}
```

Copy the token for next requests.

### 2. Register New User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "secure123"
  }'
```

### 3. Create a Post

```bash
curl -X POST http://localhost:8000/api/v1/posts/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Hello World!",
    "content": "This is my first post on the Social Media API"
  }'
```

### 4. List All Posts

```bash
curl -X GET http://localhost:8000/api/v1/posts/
```

### 5. Like a Post

```bash
curl -X POST http://localhost:8000/api/v1/posts/1/like/ \
  -H "Authorization: Token your_token_here"
```

### 6. Add a Comment

```bash
curl -X POST http://localhost:8000/api/v1/comments/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "Great post!"
  }'
```

### 7. Follow Another User

```bash
curl -X POST http://localhost:8000/api/v1/auth/follow/1/ \
  -H "Authorization: Token your_token_here"
```

### 8. Get Your Feed

```bash
curl -X GET http://localhost:8000/api/v1/feed/ \
  -H "Authorization: Token your_token_here"
```

### 9. View Your Profile

```bash
curl -X GET http://localhost:8000/api/v1/auth/profile/ \
  -H "Authorization: Token your_token_here"
```

### 10. Get Notifications

```bash
curl -X GET http://localhost:8000/api/v1/notifications/ \
  -H "Authorization: Token your_token_here"
```

---

## Using with Postman

1. **Import Collection**
   - Open Postman
   - Click "Import"
   - Create new requests for each endpoint

2. **Set Authorization**
   - Get token from login endpoint
   - In Postman, go to "Authorization" tab
   - Select "Bearer Token"
   - Paste your token

3. **Test Endpoints**
   - Use requests to test functionality
   - Check responses

---

## Common Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Clear database (WARNING: deletes all data)
python manage.py flush

# Backup database
python manage.py dumpdata > backup.json

# Restore database
python manage.py loaddata backup.json
```

---

## Admin Panel

Access the admin panel at: **http://localhost:8000/admin/**

- **Username:** admin
- **Password:** (as set during superuser creation)

From here you can:
- Manage users
- Create/edit/delete posts
- Manage comments
- View notifications
- Create test data

---

## Project Structure

```
social_media_api/
├── accounts/           # User management
├── posts/              # Posts, comments, likes
├── notifications/      # Notifications system
├── social_media_api/   # Project settings
├── manage.py           # Django command-line tool
├── requirements.txt    # Python dependencies
└── db.sqlite3          # SQLite database
```

---

## Troubleshooting

### Port 8000 Already in Use

```bash
python manage.py runserver 8001
```

### Module Not Found Error

```bash
pip install -r requirements.txt
source venv/bin/activate
```

### Database Error

```bash
python manage.py migrate
```

### Static Files Issue

```bash
python manage.py collectstatic --noinput
```

---

## Next Steps

1. **Read Full Documentation:** See [README.md](README.md)
2. **API Reference:** See [API.md](API.md)
3. **Deployment Guide:** See [DEPLOYMENT.md](DEPLOYMENT.md)
4. **Explore Admin Panel:** Visit http://localhost:8000/admin/
5. **Test with Postman:** Import API collection

---

## Useful Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Guide](https://www.postgresql.org/docs/)
- [Heroku Django Deployment](https://devcenter.heroku.com/articles/deploying-python)

---

## Support

- **Issues:** Create an issue on GitHub
- **Questions:** Check documentation first
- **Contributing:** Submit pull requests

---

**Happy Coding!** 🚀
