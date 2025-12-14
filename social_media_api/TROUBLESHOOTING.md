# 🔧 Troubleshooting Guide

## Common Issues & Solutions

### Installation Issues

#### Problem: `ModuleNotFoundError: No module named 'django'`
**Solution:**
```bash
pip install -r requirements.txt
```
Ensure you've installed all dependencies listed in requirements.txt

---

#### Problem: `python` command not found
**Solution:**
- On Windows: Use `python.exe` or add Python to PATH
- On Mac/Linux: Use `python3`
- Check Python installation: `python --version`

---

#### Problem: Virtual environment issues
**Solution:**
```bash
# Create new virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

---

### Database Issues

#### Problem: `django.db.utils.OperationalError: no such table`
**Solution:**
```bash
python manage.py migrate
```
This creates all necessary database tables.

---

#### Problem: Migration conflicts
**Solution:**
```bash
# Check migration status
python manage.py showmigrations

# If needed, reset migrations (development only!)
python manage.py migrate accounts zero
python manage.py migrate
```

---

#### Problem: `ProgrammingError: column "xyz" does not exist`
**Solution:**
```bash
# Create new migrations for changed models
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

---

### Django Development Server Issues

#### Problem: `Port 8000 already in use`
**Solution:**
```bash
# Use different port
python manage.py runserver 8001

# Or find and kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :8000
kill -9 <PID>
```

---

#### Problem: `Address already in use`
**Solution:**
Try a different port: `python manage.py runserver 0.0.0.0:8001`

---

#### Problem: Server not responding / Connection refused
**Solution:**
1. Make sure server is running
2. Check if you're using correct port
3. Check if localhost/127.0.0.1 is in ALLOWED_HOSTS
4. Try `python manage.py check`

---

### API / Endpoint Issues

#### Problem: `401 Unauthorized` on authenticated endpoints
**Solution:**
Make sure you're:
1. Including token in header: `Authorization: Token your_token_here`
2. Token is valid (hasn't expired)
3. User still exists in database

```bash
# Get a new token
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

---

#### Problem: `403 Forbidden` on POST/PUT/DELETE
**Solution:**
1. Check permissions - are you the author?
2. Make sure you're authenticated
3. Check if user has permission for this action

---

#### Problem: `404 Not Found` on endpoint
**Solution:**
1. Verify endpoint URL is correct
2. Check API.md for correct endpoints
3. Make sure Django server is running
4. Check base URL: should be `http://localhost:8000/api/v1/`

---

#### Problem: `400 Bad Request` - validation error
**Solution:**
Check error message for specific validation errors:
- Check field names match model
- Check data types (integers, strings, etc.)
- Check required fields are provided
- See API.md for request format examples

---

#### Problem: Pagination not working
**Solution:**
- Check response has `results` key for paginated endpoints
- Add `?page=2` to URL for other pages
- Default page size is 10 items

---

### Authentication Issues

#### Problem: Can't login / Invalid credentials
**Solution:**
1. Verify username and password are correct
2. Check user exists: `python manage.py shell`
   ```python
   from django.contrib.auth import get_user_model
   User = get_user_model()
   User.objects.filter(username='username').exists()
   ```
3. Reset password if needed

---

#### Problem: Token not generated after registration
**Solution:**
```bash
# Manually create token
python manage.py shell
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='username')
token = Token.objects.create(user=user)
print(token.key)
```

---

#### Problem: Token expired / invalid
**Solution:**
- Get new token by logging in again
- Token is indefinite unless Django-REST-Auth timeout is configured
- Restart development server if needed

---

### Testing Issues

#### Problem: `python test_api.py` fails
**Solution:**
```bash
# Make sure:
# 1. Django migrations are applied
python manage.py migrate

# 2. Database exists and is accessible
python manage.py check

# 3. Install test dependencies if needed
pip install -r requirements.txt

# 4. Run specific test for debugging
python -c "from test_api import APITestSuite; suite = APITestSuite(); suite.test_user_registration()"
```

---

#### Problem: `FAILED: Database error during tests`
**Solution:**
1. Reset test database: `rm db.sqlite3` (if using SQLite)
2. Run migrations: `python manage.py migrate`
3. Try tests again

---

### Docker Issues

#### Problem: Docker not found / not installed
**Solution:**
Download Docker from https://www.docker.com/products/docker-desktop

---

#### Problem: `docker-compose: command not found`
**Solution:**
Docker Compose is included with Docker Desktop. Reinstall if needed.

---

#### Problem: Container fails to start
**Solution:**
```bash
# Check logs
docker-compose logs web

# Rebuild container
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check container status
docker-compose ps
```

---

#### Problem: Permission denied error
**Solution:**
```bash
# On Linux/Mac, prefix with sudo:
sudo docker-compose up -d
```

---

#### Problem: Port already in use in Docker
**Solution:**
Edit `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Use 8001 instead of 8000
```

---

### Deployment Issues

#### Problem: Heroku deployment fails
**Solution:**
1. Check Procfile exists and is correct
2. Check runtime.txt has valid Python version
3. Check environment variables are set: `heroku config`
4. Check buildpack: `heroku buildpacks:list`
5. View logs: `heroku logs --tail`

---

#### Problem: Environment variables not working
**Solution:**
```bash
# For development, create .env file
echo "DEBUG=True" > .env
echo "SECRET_KEY=your_secret_key" >> .env
echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env
```

For production (Heroku):
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your_secret_key
```

---

#### Problem: Static files not serving
**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check static files directory exists
ls staticfiles/  # or dir staticfiles/ on Windows
```

---

#### Problem: Database connection error in production
**Solution:**
1. Check DATABASE_URL environment variable is set
2. Verify database credentials are correct
3. Check database server is running and accessible
4. For Heroku: `heroku addons:create heroku-postgresql:hobby-dev`

---

### Permission & Security Issues

#### Problem: `CSRF Failed` error
**Solution:**
1. Include CSRF token in headers for POST/PUT/DELETE
2. Or disable for API (already done in settings)
3. Check CORS configuration if cross-origin

---

#### Problem: Can only read, not write posts/comments
**Solution:**
1. Make sure you're authenticated (have token)
2. Use correct HTTP method (POST for create, PUT for update)
3. Check permissions - you can only edit your own content
4. Check if endpoint requires authentication

---

#### Problem: `Forbidden: You do not have permission`
**Solution:**
1. Only authors can edit/delete their own posts
2. Make sure authenticated user is the post author
3. Check if endpoint is read-only for your permission level

---

### Performance Issues

#### Problem: Slow response times
**Solution:**
1. Check if pagination is working (gets only 10 items)
2. Add indexes to frequently queried fields
3. Use select_related/prefetch_related in views
4. Cache frequently accessed data
5. Check database is optimized

---

#### Problem: Memory usage high
**Solution:**
1. Check for infinite loops in code
2. Limit query results with pagination
3. Close database connections properly
4. Use Django debugging tools to profile

---

### Code Issues

#### Problem: Syntax errors after editing code
**Solution:**
1. Check for typos and indentation
2. Use Python linter: `python -m pylint file.py`
3. Run Django check: `python manage.py check`
4. Look at error message traceback carefully

---

#### Problem: Import errors
**Solution:**
1. Check module names are correct
2. Make sure app is in INSTALLED_APPS
3. Verify relative imports are correct
4. Check file paths

---

#### Problem: View not found / URL doesn't work
**Solution:**
1. Check URL pattern is correct in urls.py
2. Verify view exists and is imported
3. Check regex pattern matches URL
4. Restart development server

---

### Git / Version Control Issues

#### Problem: Git not found
**Solution:**
Install Git from https://git-scm.com/

---

#### Problem: `fatal: not a git repository`
**Solution:**
```bash
# Initialize git
git init

# Add remote
git remote add origin https://github.com/username/repo.git
```

---

#### Problem: Commit fails / Authentication error
**Solution:**
1. Configure git: `git config --global user.name "Name"` and `git config --global user.email "email@example.com"`
2. Check SSH key or credentials
3. Try HTTPS instead of SSH

---

## General Troubleshooting Steps

1. **Read the error message carefully** - It usually tells you the problem
2. **Check the traceback** - See which file and line caused the error
3. **Run Django check** - `python manage.py check`
4. **Check logs** - Look at server output and application logs
5. **Verify requirements** - Ensure all dependencies are installed
6. **Check database** - Make sure migrations are applied
7. **Verify settings** - Check settings.py has correct configuration
8. **Test piece by piece** - Isolate the issue
9. **Google the error** - Often others have had the same issue
10. **Ask for help** - Post on Stack Overflow with complete error details

---

## Debugging Tips

### Enable Debug Mode
```bash
# In .env or settings
DEBUG=True
```

### Use Django Shell
```bash
python manage.py shell

# Then:
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='username')
print(user.bio)
```

### Check Database Directly
```bash
# SQLite
sqlite3 db.sqlite3

# PostgreSQL
psql -U postgres -d social_media_db
```

### View Server Logs
```bash
# Development server output shows in terminal

# Docker
docker-compose logs -f web

# Heroku
heroku logs --tail
```

---

## When All Else Fails

1. **Reset everything:**
   ```bash
   # Remove database
   rm db.sqlite3
   
   # Fresh migrations
   python manage.py migrate
   
   # Restart server
   python manage.py runserver
   ```

2. **Check requirements match:**
   ```bash
   pip list
   pip install -r requirements.txt --force-reinstall
   ```

3. **Verify Python version:**
   ```bash
   python --version  # Should be 3.8+
   ```

4. **Check system dependencies:**
   ```bash
   # On Linux/Mac
   pip install --upgrade pip setuptools wheel
   ```

---

## Getting Help

- **Documentation:** See [INDEX.md](INDEX.md) for documentation links
- **API Reference:** See [API.md](API.md)
- **Testing:** Run `python test_api.py`
- **Django Docs:** https://docs.djangoproject.com/
- **DRF Docs:** https://www.django-rest-framework.org/
- **Stack Overflow:** Tag your questions with `django` and `django-rest-framework`

---

## Reporting Issues

If you find a bug:
1. Create a minimal reproducible example
2. Document steps to reproduce
3. Include error messages and tracebacks
4. Include Python version and package versions
5. Include what you've already tried

---

**Last Updated:** December 14, 2025
**Status:** Complete and tested
