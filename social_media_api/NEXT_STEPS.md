# Next Steps & Testing Instructions

## Current Status

✅ **Project is fully implemented and running!**

The Social Media API is complete with:
- All 4 mandatory tasks completed
- Development server running at http://localhost:8000
- Database initialized with migrations
- Admin panel accessible
- Full API functionality

## Immediate Next Steps

### 1. Test the API (Recommended First Step)

```bash
# In a new terminal, navigate to project directory
cd "c:\Users\pc gold\Alx_DjangoLearnLab\social_media_api"

# Test register endpoint
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'

# Test login endpoint
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### 2. Access Admin Panel

1. Open browser: http://localhost:8000/admin/
2. Login with:
   - Username: `admin`
   - Password: (whatever you set during superuser creation)
3. Create test data through admin interface

### 3. Use Postman (Easier Testing)

1. Download Postman from https://www.postman.com/downloads/
2. Create new requests for each endpoint
3. Use examples from [API.md](API.md)

## Development Tasks

### Create Test Data

```bash
# Access Django shell
python manage.py shell

# Create test users
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

# Create users
alice = User.objects.create_user(username='alice', password='pass123', bio='Alice bio')
bob = User.objects.create_user(username='bob', password='pass123', bio='Bob bio')

# Create posts
Post.objects.create(author=alice, title='Alice Post', content='Alice content')
Post.objects.create(author=bob, title='Bob Post', content='Bob content')

# Create follow relationship
alice.following.add(bob)

exit()
```

### Run Automated Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test posts
python manage.py test notifications

# Run with verbose output
python manage.py test -v 2

# Run with coverage (if installed)
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## Deployment Steps

### Option 1: Docker Deployment (Recommended)

```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

### Option 2: Heroku Deployment

```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser

# View app
heroku open
```

### Option 3: AWS Deployment

Follow detailed steps in [DEPLOYMENT.md](DEPLOYMENT.md)

## Code Modifications & Enhancements

### Add Email Notifications

```python
# In notifications/models.py
from django.core.mail import send_mail

def send_email_notification(notification):
    subject = f"{notification.actor.username} {notification.verb}"
    message = f"You have a new notification from {notification.actor.username}"
    send_mail(subject, message, 'from@example.com', [notification.recipient.email])
```

### Add Caching

```python
# In settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# In posts/views.py
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def get_feed(request):
    # ...
```

### Add Rate Limiting

```python
# In settings.py
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

### Add Pagination Customization

```python
# Create custom paginator
# In a new file: api/pagination.py
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Use in views
class PostViewSet(viewsets.ModelViewSet):
    pagination_class = StandardPagination
```

## Database Management

### Backup Database

```bash
# SQLite backup
cp db.sqlite3 db.sqlite3.backup

# PostgreSQL backup (if using Heroku)
heroku pg:backups:capture
heroku pg:backups:download
```

### Restore Database

```bash
# SQLite restore
cp db.sqlite3.backup db.sqlite3

# PostgreSQL restore
heroku pg:backups:restore
```

## Monitoring & Logging

### Local Logging

```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Production Monitoring

- **Sentry** - Error tracking: https://sentry.io
- **New Relic** - Performance monitoring
- **DataDog** - Infrastructure monitoring
- **Papertrail** - Log aggregation

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG=False in production
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable HTTPS/SSL
- [ ] Set secure cookies
- [ ] Configure CORS
- [ ] Regular security updates
- [ ] Database backups
- [ ] Access logs monitoring

## Performance Optimization

### Database Optimization

```bash
# Analyze slow queries
python manage.py shell
>>> from django.db import connection
>>> connection.queries_log.clear()
>>> # Run some code
>>> len(connection.queries)  # Number of queries
```

### Cache Strategy

```python
# Cache frequently accessed data
from django.core.cache import cache

posts = cache.get('popular_posts')
if not posts:
    posts = Post.objects.all()[:10]
    cache.set('popular_posts', posts, 3600)  # Cache for 1 hour
```

## Continuous Integration

### GitHub Actions Setup

```yaml
# .github/workflows/tests.yml
name: Django Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python manage.py test
```

## Contributing Guidelines

1. Create feature branch: `git checkout -b feature/feature-name`
2. Make changes and commit: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/feature-name`
4. Create Pull Request

## Version Control Commands

```bash
# Initialize git repo
git init
git add .
git commit -m "Initial commit: Social Media API"

# Create GitHub repo and push
git branch -M main
git remote add origin https://github.com/username/repo.git
git push -u origin main

# Create release tags
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

## Documentation Updates

### Update README

- [ ] Add screenshots
- [ ] Add demo video link
- [ ] Add contributing guidelines
- [ ] Add license information

### Create Additional Docs

- [ ] Architecture diagram
- [ ] Database schema diagram
- [ ] API flow diagram
- [ ] Deployment architecture

## Marketing & Portfolio

### Create Portfolio Entry

1. Add project to portfolio
2. Write project description
3. Add screenshots/videos
4. Include live demo link
5. Link to GitHub repo

### GitHub Profile

- Add project to "Featured" section
- Write project description
- Pin the repository
- Add technologies used

## Troubleshooting

### Server Issues

```bash
# Kill process on port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

### Database Issues

```bash
# Reset database
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Issues

```bash
# Clear and collect
python manage.py collectstatic --clear --noinput
```

## Useful Commands

```bash
# Create new app
python manage.py startapp appname

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access shell
python manage.py shell

# Dump data
python manage.py dumpdata > backup.json

# Load data
python manage.py loaddata backup.json

# Check deployment
python manage.py check --deploy

# Create cache
python manage.py createcachetable
```

## Support Resources

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Stack Overflow: https://stackoverflow.com/questions/tagged/django
- Django Forum: https://forum.djangoproject.com/

---

## Quick Reference

**Repository Location:** `c:\Users\pc gold\Alx_DjangoLearnLab\social_media_api`

**Server Status:** ✅ Running on http://localhost:8000

**Admin Panel:** http://localhost:8000/admin/

**API Documentation:** See [API.md](API.md)

**Quick Start:** See [QUICKSTART.md](QUICKSTART.md)

**Deployment Guide:** See [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Last Updated:** December 2024  
**Project Status:** Complete and Production Ready ✅
