# Deployment Guide - Social Media API

This guide covers various deployment options for the Social Media API.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [AWS Deployment](#aws-deployment)
5. [DigitalOcean Deployment](#digitalocean-deployment)
6. [Production Best Practices](#production-best-practices)

## Local Development

### Prerequisites
- Python 3.8+
- pip
- Virtual Environment (recommended)

### Setup

```bash
# Clone repository
git clone https://github.com/your-username/Alx_DjangoLearnLab.git
cd social_media_api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Access at: `http://localhost:8000`

## Docker Deployment

### Prerequisites
- Docker
- Docker Compose

### Setup

```bash
# Clone repository
git clone https://github.com/your-username/Alx_DjangoLearnLab.git
cd social_media_api

# Create .env file
cat > .env << EOF
DEBUG=False
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DATABASE_URL=postgres://postgres:postgres@db:5432/social_media_db
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
EOF

# Start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Create SSL certificates (for local testing)
docker-compose exec nginx openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/key.pem -out /etc/nginx/ssl/cert.pem
```

Access at: `https://localhost`

### Docker Commands

```bash
# View logs
docker-compose logs -f web

# Execute command in container
docker-compose exec web python manage.py shell

# Stop all services
docker-compose down

# Remove volumes
docker-compose down -v
```

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository

### Setup

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
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# View logs
heroku logs --tail
```

Access at: `https://your-app-name.herokuapp.com`

## AWS Deployment

### Prerequisites
- AWS account
- AWS CLI configured
- EC2 key pair created

### Option 1: Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize EB
eb init -p python-3.11 social-media-api
eb create social-media-api-env
eb deploy

# Set environment variables
eb setenv DEBUG=False SECRET_KEY=your-key-here DATABASE_URL=your-db-url

# View logs
eb logs
```

### Option 2: EC2 with Nginx

```bash
# SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Update system
sudo yum update -y
sudo yum install -y python3 python3-venv python3-devel gcc postgresql-devel nginx

# Clone repository
git clone https://github.com/your-username/Alx_DjangoLearnLab.git
cd social_media_api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@rds-endpoint:5432/social_media_db
ALLOWED_HOSTS=your-domain.com,your-ip
EOF

# Run migrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

# Configure Gunicorn
pip install gunicorn
gunicorn social_media_api.wsgi:application --bind 0.0.0.0:8000

# Create systemd service
sudo tee /etc/systemd/system/gunicorn.service > /dev/null << EOF
[Unit]
Description=Gunicorn instance for social media API
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/social_media_api
ExecStart=/home/ec2-user/social_media_api/venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          social_media_api.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

# Configure Nginx
sudo tee /etc/nginx/conf.d/social_media_api.conf > /dev/null << EOF
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /home/ec2-user/social_media_api/staticfiles/;
    }

    location /media/ {
        alias /home/ec2-user/social_media_api/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Start Nginx
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl reload nginx
```

## DigitalOcean Deployment

### Prerequisites
- DigitalOcean account
- Droplet created (Ubuntu 22.04)
- Domain configured

### Setup

```bash
# SSH into Droplet
ssh root@your-droplet-ip

# Update system
apt update && apt upgrade -y
apt install -y python3 python3-venv python3-dev build-essential postgresql postgresql-contrib nginx git curl wget

# Create application user
useradd -m -s /bin/bash django
su - django

# Clone repository
git clone https://github.com/your-username/Alx_DjangoLearnLab.git
cd social_media_api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://social_user:password@localhost:5432/social_media_db
ALLOWED_HOSTS=your-domain.com
EOF

# Setup PostgreSQL
exit  # Back to root
sudo -u postgres psql << EOF
CREATE DATABASE social_media_db;
CREATE USER social_user WITH PASSWORD 'password';
ALTER ROLE social_user SET client_encoding TO 'utf8';
ALTER ROLE social_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE social_user SET default_transaction_deferrable TO on;
ALTER ROLE social_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE social_media_db TO social_user;
\q
EOF

# Continue as django user
su - django
cd social_media_api
source venv/bin/activate

# Run migrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

# Exit back to root
exit

# Create systemd service
tee /etc/systemd/system/gunicorn.service > /dev/null << EOF
[Unit]
Description=Gunicorn instance for social media API
After=network.target

[Service]
User=django
WorkingDirectory=/home/django/social_media_api
ExecStart=/home/django/social_media_api/venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          social_media_api.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable gunicorn
systemctl start gunicorn

# Configure Nginx
tee /etc/nginx/sites-available/social_media_api > /dev/null << EOF
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 20M;

    location /static/ {
        alias /home/django/social_media_api/staticfiles/;
    }

    location /media/ {
        alias /home/django/social_media_api/media/;
    }

    location / {
        proxy_pass http://django;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ln -s /etc/nginx/sites-available/social_media_api /etc/nginx/sites-enabled/
nginx -t
systemctl enable nginx
systemctl start nginx

# Setup SSL with Let's Encrypt
apt install -y certbot python3-certbot-nginx
certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
systemctl enable certbot.timer
```

## Production Best Practices

### 1. Environment Variables
- Never commit `.env` file to repository
- Use strong, random SECRET_KEY
- Set DEBUG=False in production
- Configure ALLOWED_HOSTS properly

### 2. Database
- Use PostgreSQL in production (not SQLite)
- Regular backups
- Enable connection pooling with PgBouncer
- Monitor database performance

### 3. Security
- Enable HTTPS/TLS
- Set security headers
- Keep dependencies updated
- Regular security audits
- Use environment-specific configurations

### 4. Monitoring & Logging
- Set up error tracking (Sentry)
- Monitor application performance (New Relic, DataDog)
- Centralize logs (ELK Stack, Papertrail)
- Set up alerts for critical errors

### 5. Performance
- Use Redis for caching
- Implement database query optimization
- Enable gzip compression
- Use CDN for static files
- Implement rate limiting

### 6. Backup & Recovery
- Regular database backups
- Test recovery procedures
- Store backups off-site
- Document recovery process

### 7. Scaling
- Use load balancer for multiple instances
- Database replication
- Cache warming strategies
- Async task processing (Celery)

## Troubleshooting

### 500 Internal Server Error
```bash
# Check logs
docker-compose logs web
heroku logs --tail
systemctl status gunicorn
```

### Database Connection Error
- Verify DATABASE_URL
- Check database is running
- Verify credentials
- Check network connectivity

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput --clear
```

### Permission Denied Errors
```bash
chmod -R 755 /app
chown -R django:django /home/django/social_media_api
```

## Monitoring Commands

### Check Application Status
```bash
# Docker
docker-compose ps

# Heroku
heroku ps

# Systemd
systemctl status gunicorn
```

### View Real-time Logs
```bash
# Docker
docker-compose logs -f web

# Heroku
heroku logs --tail

# Systemd
journalctl -u gunicorn -f
```

### Check Database
```bash
# Check connection
psql -U postgres -d social_media_db -h localhost

# Heroku
heroku pg:info
```

---

**Last Updated**: December 2024
